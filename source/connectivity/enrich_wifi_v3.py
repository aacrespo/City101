#!/usr/bin/env python3
"""
City101 WiFi + Cell Tower enrichment script
Session 22-02

Step 1: Filter BAKOM cell towers for City101 corridor → city101_cell_towers.csv
Step 2: Google Places API searches for more WiFi venues → city101_wifi_MERGEDv3.csv
Step 3: Summary

Run from anywhere. Outputs to /mnt/user-data/outputs/
"""

import json
import urllib.request
import urllib.parse
import csv
import time
import math
import os

# ── Config ──────────────────────────────────────────────────────────────────
CORRIDOR_BBOX_LV95 = {
    "E_min": 2490000,  # Western edge (Geneva)
    "E_max": 2570000,  # Eastern edge (Villeneuve)
    "N_min": 1110000,  # Southern edge (lakeside)
    "N_max": 1155000,  # Northern edge (hills)
}

# WGS84 bbox for Google Places searches
CORRIDOR_LAT_MIN = 46.10
CORRIDOR_LAT_MAX = 46.55
CORRIDOR_LON_MIN = 6.05
CORRIDOR_LON_MAX = 6.95

OUTPUT_DIR = "/mnt/user-data/outputs"
INPUT_WIFI = "/mnt/project/city101_wifi_MERGEDv_2.csv"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Step 1: BAKOM Cell Towers ─────────────────────────────────────────────

def fetch_cell_towers():
    print("\n=== STEP 1: BAKOM Cell Tower Data ===")
    url = ("https://data.geo.admin.ch/ch.bakom.standorte-mobilfunkanlagen"
           "/standorte-mobilfunkanlagen/standorte-mobilfunkanlagen_2056.json")
    print("  Downloading (25MB)...")
    req = urllib.request.urlopen(url, timeout=90)
    data = json.loads(req.read())
    all_towers = data.get("features", [])
    print(f"  Total towers in Switzerland: {len(all_towers)}")

    bbox = CORRIDOR_BBOX_LV95
    corridor_towers = []

    for f in all_towers:
        coords = f.get("geometry", {}).get("coordinates", [])
        if not coords or len(coords) < 2:
            continue
        E, N = coords[0], coords[1]
        if bbox["E_min"] <= E <= bbox["E_max"] and bbox["N_min"] <= N <= bbox["N_max"]:
            props = f.get("properties", {})
            # Parse technology string
            tech_str = props.get("techno_en", props.get("techno_de", ""))
            has_3g = "3G" in tech_str
            has_4g = "4G" in tech_str
            has_5g = "5G" in tech_str

            # Power class
            power_str = props.get("power_en", "")
            if "low" in power_str.lower():
                power_class = "low"
            elif "medium" in power_str.lower():
                power_class = "medium"
            elif "high" in power_str.lower():
                power_class = "high"
            else:
                power_class = "unknown"

            # Station type (indoor/outdoor, size)
            typ = props.get("typ_en", "")
            is_indoor = "indoor" in typ.lower()

            # Convert LV95 to WGS84 (approximate, good enough for mapping)
            lat, lon = lv95_to_wgs84(E, N)

            corridor_towers.append({
                "tower_id": f"TOWER_{len(corridor_towers)+1:04d}",
                "operator": props.get("station", ""),
                "technology": tech_str,
                "has_3g": has_3g,
                "has_4g": has_4g,
                "has_5g": has_5g,
                "power_class": power_class,
                "station_type": typ,
                "is_indoor": is_indoor,
                "E_lv95": E,
                "N_lv95": N,
                "lat_wgs84": round(lat, 6),
                "lon_wgs84": round(lon, 6),
                "source": "BAKOM/geo.admin.ch (22.02.26)",
            })

    print(f"  Corridor towers (Geneva–Villeneuve): {len(corridor_towers)}")

    # Stats
    ops = {}
    for t in corridor_towers:
        op = t["operator"].split(" ")[0] if t["operator"] else "Unknown"
        ops[op] = ops.get(op, 0) + 1
    print("  By operator:")
    for op, count in sorted(ops.items(), key=lambda x: -x[1])[:8]:
        print(f"    {op}: {count}")

    has5g = sum(1 for t in corridor_towers if t["has_5g"])
    has4g = sum(1 for t in corridor_towers if t["has_4g"])
    print(f"  5G-capable: {has5g} | 4G-capable: {has4g}")

    # Write CSV
    out_path = os.path.join(OUTPUT_DIR, "city101_cell_towers.csv")
    fieldnames = list(corridor_towers[0].keys())
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(corridor_towers)
    print(f"  Saved: {out_path}")
    return corridor_towers


# ── Step 2: Google Places WiFi Search ────────────────────────────────────

def google_places_search(query, lat, lon, radius=8000):
    """Text search via Google Places (maps.googleapis.com)"""
    params = {
        "query": query,
        "location": f"{lat},{lon}",
        "radius": radius,
        "key": "AIzaSyD-PLACEHOLDER",  # Not needed - handled by Claude's built-in integration
    }
    # NOTE: Claude.ai has Google Places built-in via maps.googleapis.com
    # We use the Places Text Search endpoint
    base = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    url = base + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.urlopen(url, timeout=15)
        return json.loads(req.read())
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def search_wifi_locations_along_corridor():
    """
    Search for WiFi venues systematically along the corridor.
    Strategy: grid of search points, multiple query types.
    Returns list of new venue dicts.
    """
    print("\n=== STEP 2: Google Places WiFi Search ===")

    # Search centers along corridor (roughly every 20km)
    search_points = [
        # (lat, lon, label)
        (46.204,  6.143,  "Geneva_center"),
        (46.238,  6.105,  "Geneva_airport"),
        (46.333,  6.235,  "Nyon"),
        (46.380,  6.310,  "Rolle"),
        (46.508,  6.495,  "Morges"),
        (46.521,  6.632,  "Lausanne_center"),
        (46.517,  6.680,  "Lausanne_east"),
        (46.467,  6.753,  "Vevey"),
        (46.432,  6.912,  "Montreux"),
        (46.402,  6.934,  "Villeneuve"),
        (46.310,  6.390,  "Coppet_area"),
        (46.370,  6.570,  "mid_corridor"),
    ]

    search_queries = [
        "coworking space",
        "wifi cafe laptop",
        "library public wifi",
        "McDonalds wifi",
        "Starbucks wifi",
    ]

    existing_names = set()
    results = []

    for lat, lon, label in search_points:
        for query in search_queries:
            full_query = f"{query} near {label.replace('_', ' ')}"
            data = google_places_search(full_query, lat, lon, radius=6000)
            time.sleep(0.3)

            if data.get("status") not in ("OK", "ZERO_RESULTS"):
                # API error - likely no API key available via this method
                print(f"  Places API status: {data.get('status')} for '{full_query}'")
                continue

            for place in data.get("results", []):
                name = place.get("name", "")
                if name in existing_names:
                    continue
                existing_names.add(name)

                # Location
                loc = place.get("geometry", {}).get("location", {})
                plat = loc.get("lat")
                plon = loc.get("lng")
                if not plat or not plon:
                    continue

                # Filter to corridor bbox
                if not (CORRIDOR_LAT_MIN <= plat <= CORRIDOR_LAT_MAX and
                        CORRIDOR_LON_MIN <= plon <= CORRIDOR_LON_MAX):
                    continue

                E, N = wgs84_to_lv95(plat, plon)

                # Classify
                types = place.get("types", [])
                cat = classify_place_type(types, query)

                results.append({
                    "place_id": place.get("place_id", ""),
                    "name": name,
                    "lat_wgs84": round(plat, 6),
                    "lon_wgs84": round(plon, 6),
                    "E_lv95": round(E, 1),
                    "N_lv95": round(N, 1),
                    "location_type": cat["location_type"],
                    "wifi_category": cat["wifi_category"],
                    "wifi_quality_score": cat["wifi_quality_score"],
                    "rating": place.get("rating", ""),
                    "review_count": place.get("user_ratings_total", ""),
                    "search_area": label,
                })

        print(f"  {label}: {len([r for r in results if r.get('search_area') == label])} new venues")

    print(f"  Total new Places found: {len(results)}")
    return results


def classify_place_type(types, query):
    """Classify Google Places types into our schema."""
    if "coworking" in query:
        return {"location_type": "coworking", "wifi_category": "coworking", "wifi_quality_score": 8}
    if "library" in query:
        return {"location_type": "library", "wifi_category": "institutional_wifi", "wifi_quality_score": 6}
    if "cafe" in query or "coffee" in query or "starbucks" in query.lower():
        return {"location_type": "cafe_chain", "wifi_category": "cafe_chain_wifi", "wifi_quality_score": 5}
    if "mcdonalds" in query.lower() or "fast_food" in str(types):
        return {"location_type": "fast_food", "wifi_category": "cafe_chain_wifi", "wifi_quality_score": 4}
    return {"location_type": "unknown", "wifi_category": "commercial_wifi", "wifi_quality_score": 4}


# ── Step 3: Merge with existing WiFi dataset ──────────────────────────────

def load_existing_wifi():
    rows = []
    with open(INPUT_WIFI, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    print(f"\n  Loaded existing WiFi: {len(rows)} records")
    return rows


def merge_and_save(existing, new_places):
    """Deduplicate by name+proximity and merge."""
    print("\n=== STEP 3: Merge WiFi Data ===")

    existing_coords = [(float(r["lat_wgs84"]), float(r["lon_wgs84"])) for r in existing]

    added = 0
    skipped_dup = 0

    # Column order - keep existing schema, add google_place_id
    fieldnames = list(existing[0].keys())
    if "google_place_id" not in fieldnames:
        fieldnames.append("google_place_id")

    # Create new rows from Places results
    new_rows = []
    station_counter = len(existing) + 1

    for p in new_places:
        plat, plon = p["lat_wgs84"], p["lon_wgs84"]

        # Check for duplicates (within 80m)
        is_dup = False
        for elat, elon in existing_coords:
            d = haversine(plat, plon, elat, elon)
            if d < 80:
                is_dup = True
                break

        if is_dup:
            skipped_dup += 1
            continue

        # Determine connectivity cluster
        cluster = assign_cluster(plat, plon)
        wifi_desert = "no"  # If we found it via Places, it has WiFi

        # Map to existing schema
        row = {f: "" for f in fieldnames}
        row.update({
            "station_id": f"WIFI_{station_counter:03d}",
            "name": p["name"],
            "lat_wgs84": plat,
            "lon_wgs84": plon,
            "E_lv95": p["E_lv95"],
            "N_lv95": p["N_lv95"],
            "location_type": p["location_type"],
            "wifi_category": p["wifi_category"],
            "wifi_quality_score": p["wifi_quality_score"],
            "operator_network": "",
            "indoor_outdoor": "indoor" if p["location_type"] in ("coworking", "library", "fast_food", "cafe_chain") else "mixed",
            "hours": "",
            "has_power_outlets": "yes" if p["wifi_category"] == "coworking" else "unknown",
            "google_rating": p.get("rating", ""),
            "google_review_count": p.get("review_count", ""),
            "connectivity_cluster": cluster,
            "wifi_desert": wifi_desert,
            "review_mentions_remote_work": "yes" if "coworking" in p["wifi_category"] else "unknown",
            "day_pass_chf": "free" if p["location_type"] in ("fast_food", "cafe_chain", "library") else "varies",
            "review_snippet": "",
            "source": f"Google Places API (22.02.26)",
            "notes": f"Found via Places search: {p.get('search_area', '')}",
            "google_place_id": p.get("place_id", ""),
        })

        new_rows.append(row)
        existing_coords.append((plat, plon))
        station_counter += 1
        added += 1

    # Add google_place_id to existing rows
    for row in existing:
        if "google_place_id" not in row:
            row["google_place_id"] = ""

    all_rows = existing + new_rows

    # Save
    out_path = os.path.join(OUTPUT_DIR, "city101_wifi_MERGEDv3.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"  Existing records:  {len(existing)}")
    print(f"  New from Places:   {added}")
    print(f"  Skipped (dupes):   {skipped_dup}")
    print(f"  Total merged:      {len(all_rows)}")
    print(f"  Saved: {out_path}")
    return all_rows


# ── Coordinate conversions ────────────────────────────────────────────────

def lv95_to_wgs84(E, N):
    """Approximate LV95 → WGS84. Good to ~1m."""
    y = (E - 2600000) / 1000000
    x = (N - 1200000) / 1000000
    lon_raw = (2.6779094
               + 4.728982 * y
               + 0.791484 * y * x
               + 0.1306 * y * x * x
               - 0.0436 * y * y * y)
    lat_raw = (16.9023892
               + 3.238272 * x
               - 0.270978 * y * y
               - 0.002528 * x * x
               - 0.0447 * y * y * x
               - 0.0140 * x * x * x)
    lon = lon_raw * 100 / 36
    lat = lat_raw * 100 / 36
    return lat, lon


def wgs84_to_lv95(lat, lon):
    """Approximate WGS84 → LV95."""
    lat_s = (lat * 3600 - 169028.66) / 10000
    lon_s = (lon * 3600 - 26782.5) / 10000
    E = (2600072.37
         + 211455.93 * lon_s
         - 10938.51 * lon_s * lat_s
         - 0.36 * lon_s * lat_s * lat_s
         - 44.54 * lon_s * lon_s * lon_s)
    N = (1200147.07
         + 308807.95 * lat_s
         + 3745.25 * lon_s * lon_s
         + 76.63 * lat_s * lat_s
         - 194.56 * lon_s * lon_s * lat_s
         + 119.79 * lat_s * lat_s * lat_s)
    return E, N


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def assign_cluster(lat, lon):
    if lon < 6.25:
        return "Geneva"
    elif lon < 6.45:
        return "Nyon"
    elif 6.45 <= lon < 6.55:
        return "mid-corridor"
    elif 6.55 <= lon < 6.70:
        return "Morges"
    elif 6.70 <= lon < 6.80:
        return "Lausanne"
    elif 6.80 <= lon < 6.90:
        return "Vevey"
    else:
        return "Montreux"


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("City101 WiFi + Cell Tower Enrichment")
    print("=" * 60)

    # Step 1: Cell towers from BAKOM
    towers = fetch_cell_towers()

    # Step 2: Load existing WiFi, attempt Google Places search
    existing_wifi = load_existing_wifi()

    print("\n=== STEP 2: Google Places WiFi Search ===")
    print("  NOTE: Google Places text search API requires an active API key.")
    print("  Attempting search — if status returns REQUEST_DENIED, the Places")
    print("  API isn't available via this tool and we'll skip to merge with existing.")

    # Test one query first
    test_result = google_places_search("coworking wifi Lausanne", 46.52, 6.63, 5000)
    status = test_result.get("status", "ERROR")
    print(f"  Test query status: {status}")

    if status == "OK":
        new_places = search_wifi_locations_along_corridor()
    else:
        print(f"  Places API not available ({status}) — skipping to merge with existing data.")
        print("  WiFi v3 will be identical to v2 + google_place_id column + cell towers separate.")
        new_places = []

    # Step 3: Merge
    all_wifi = merge_and_save(existing_wifi, new_places)

    # Print final summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Cell towers (City101 corridor): {len(towers)}")
    print(f"  Outputs: city101_cell_towers.csv")
    print(f"WiFi locations total: {len(all_wifi)}")
    print(f"  Outputs: city101_wifi_MERGEDv3.csv")

    # Tower stats
    ops = {}
    for t in towers:
        op = t["operator"].split(" ")[0]
        ops[op] = ops.get(op, 0) + 1

    print(f"\nTop operators in corridor:")
    for op, c in sorted(ops.items(), key=lambda x: -x[1])[:5]:
        print(f"  {op}: {c} towers")

    has5g = sum(1 for t in towers if t["has_5g"])
    has4g_only = sum(1 for t in towers if t["has_4g"] and not t["has_5g"])
    has3g_only = sum(1 for t in towers if t["has_3g"] and not t["has_4g"] and not t["has_5g"])
    print(f"\nTechnology breakdown:")
    print(f"  5G (any): {has5g}")
    print(f"  4G only:  {has4g_only}")
    print(f"  3G only:  {has3g_only}")

    print("\nFiles ready in /mnt/user-data/outputs/")


if __name__ == "__main__":
    main()
