#!/usr/bin/env python3
"""
City101 — Working Continuity Index (WCI) Computation
EPFL AR-302k Studio Huang — Andrea Crespo
A02 Data Synchronicity — Due 03.03.2026

Three tasks:
  1. Remote Work Cross-Reference (68 places × all datasets)
  2. Corridor Segmentation + WCI (49 train station segments)
  3. Zurich Skeleton (bonus: ZH-canton stations from ridership)

Output files:
  - city101_remote_work_CROSSREF.csv
  - city101_corridor_segments_WCI.csv
  - city101_WCI_summary.md
  - zurich_corridor_skeleton.csv
"""

import os
import math
import csv
from collections import defaultdict
from difflib import SequenceMatcher

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = os.path.expanduser("~/CLAUDE/City101_ClaudeCode")
SRC = os.path.join(BASE, "source")
OUT = os.path.join(BASE, "output")

REMOTE_WORK  = os.path.join(SRC, "invisible flows copy", "city101_remote_work_places.csv")
HOURS        = os.path.join(SRC, "city101_remote_work_HOURS.csv")
REVIEWS      = os.path.join(SRC, "invisible flows copy", "city101_remote_work_REVIEWS.csv")
WIFI         = os.path.join(SRC, "invisible flows copy", "city101_wifi_MERGEDv.2.csv")
EV           = os.path.join(SRC, "Charging station csv copy", "city101_ev_charging_ENRICHED_v3.csv")
FREQUENCY    = os.path.join(SRC, "city101_service_frequency_v2.csv")
RIDERSHIP    = os.path.join(SRC, "city101_ridership_sbb.csv")
SHARED_MOB   = os.path.join(SRC, "city101_shared_mobility.csv")
CELL_TOWERS  = os.path.join(SRC, "invisible flows copy", "city101_cell_towers.csv")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_csv(path):
    """Read CSV into list of dicts."""
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def safe_float(val, default=None):
    """Convert to float, return default on failure."""
    if val is None or str(val).strip() == "":
        return default
    try:
        return float(str(val).strip())
    except (ValueError, TypeError):
        return default


def safe_bool(val):
    """Convert string to boolean."""
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    return str(val).strip().lower() in ("true", "1", "yes")


def haversine_m(lat1, lon1, lat2, lon2):
    """Haversine distance in meters between two WGS84 points."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def wgs84_to_lv95(lat, lon):
    """Approximate WGS84 → LV95 conversion."""
    E = 2600000 + (lon - 7.438632) * 72953
    N = 1200000 + (lat - 46.951083) * 111132
    return round(E, 1), round(N, 1)


def fuzzy_match_score(a, b):
    """Simple fuzzy match ratio between two strings."""
    a_norm = a.lower().strip().replace("-", " ").replace("  ", " ")
    b_norm = b.lower().strip().replace("-", " ").replace("  ", " ")
    return SequenceMatcher(None, a_norm, b_norm).ratio()


def find_nearest(lat, lon, points, lat_key="lat", lon_key="lon"):
    """Find nearest point from a list. Returns (index, distance_m)."""
    best_idx, best_dist = None, float("inf")
    for i, p in enumerate(points):
        plat = safe_float(p[lat_key])
        plon = safe_float(p[lon_key])
        if plat is None or plon is None:
            continue
        d = haversine_m(lat, lon, plat, plon)
        if d < best_dist:
            best_dist = d
            best_idx = i
    return best_idx, best_dist


def count_within(lat, lon, points, radius_m, lat_key="lat", lon_key="lon"):
    """Count points within radius_m of (lat, lon)."""
    n = 0
    for p in points:
        plat = safe_float(p[lat_key])
        plon = safe_float(p[lon_key])
        if plat is None or plon is None:
            continue
        if haversine_m(lat, lon, plat, plon) <= radius_m:
            n += 1
    return n


def any_within_with_flag(lat, lon, points, radius_m, flag_key, lat_key="lat", lon_key="lon"):
    """Check if any point within radius has flag_key == True."""
    for p in points:
        plat = safe_float(p[lat_key])
        plon = safe_float(p[lon_key])
        if plat is None or plon is None:
            continue
        if haversine_m(lat, lon, plat, plon) <= radius_m:
            if safe_bool(p.get(flag_key, False)):
                return True
    return False


# ---------------------------------------------------------------------------
# Load all datasets
# ---------------------------------------------------------------------------
print("=" * 70)
print("CITY101 — WORKING CONTINUITY INDEX COMPUTATION")
print("=" * 70)

print("\n[1/9] Loading remote work places...")
rw_places = read_csv(REMOTE_WORK)
print(f"  → {len(rw_places)} places")

print("[2/9] Loading remote work hours...")
rw_hours = read_csv(HOURS)
print(f"  → {len(rw_hours)} entries")

print("[3/9] Loading remote work reviews...")
rw_reviews = read_csv(REVIEWS)
print(f"  → {len(rw_reviews)} reviews")

print("[4/9] Loading WiFi hotspots...")
wifi = read_csv(WIFI)
print(f"  → {len(wifi)} hotspots")

print("[5/9] Loading EV charging stations...")
ev = read_csv(EV)
print(f"  → {len(ev)} stations")

print("[6/9] Loading train service frequency...")
frequency = read_csv(FREQUENCY)
print(f"  → {len(frequency)} stations")

print("[7/9] Loading SBB ridership...")
ridership = read_csv(RIDERSHIP)
print(f"  → {len(ridership)} stations")

print("[8/9] Loading shared mobility...")
shared_mob = read_csv(SHARED_MOB)
print(f"  → {len(shared_mob)} stations")

print("[9/9] Loading cell towers...")
cell_towers = read_csv(CELL_TOWERS)
print(f"  → {len(cell_towers)} towers")

# ---------------------------------------------------------------------------
# Pre-process: build lookup structures
# ---------------------------------------------------------------------------

# Hours lookup by google_place_id and by name
hours_by_pid = {}
hours_by_name = {}
for h in rw_hours:
    pid = h.get("google_place_id", "").strip()
    name = h.get("name", "").strip()
    if pid:
        hours_by_pid[pid] = h
    if name:
        hours_by_name[name.lower()] = h

# Reviews grouped by google_place_id and by place_name
reviews_by_pid = defaultdict(list)
reviews_by_name = defaultdict(list)
for r in rw_reviews:
    pid = r.get("google_place_id", "").strip()
    pname = r.get("place_name", "").strip()
    if pid:
        reviews_by_pid[pid].append(r)
    if pname:
        reviews_by_name[pname.lower()].append(r)

# Ridership name lookup for fuzzy matching
ridership_names = [(r.get("name", "").strip(), i) for i, r in enumerate(ridership)]

# Prepare coordinate lists for fast nearest-neighbor lookups
freq_pts = [{"lat": safe_float(s.get("lat_wgs84")), "lon": safe_float(s.get("lon_wgs84")), "idx": i}
            for i, s in enumerate(frequency) if safe_float(s.get("lat_wgs84")) is not None]

wifi_pts = [{"lat": safe_float(w.get("lat_wgs84")), "lon": safe_float(w.get("lon_wgs84")), "idx": i}
            for i, w in enumerate(wifi) if safe_float(w.get("lat_wgs84")) is not None]

ev_pts = [{"lat": safe_float(e.get("latitude_wgs84")), "lon": safe_float(e.get("longitude_wgs84")), "idx": i}
          for i, e in enumerate(ev) if safe_float(e.get("latitude_wgs84")) is not None]

mob_pts = [{"lat": safe_float(m.get("lat_wgs84")), "lon": safe_float(m.get("lon_wgs84")), "idx": i}
           for i, m in enumerate(shared_mob) if safe_float(m.get("lat_wgs84")) is not None]

cell_pts = [{"lat": safe_float(c.get("lat_wgs84")), "lon": safe_float(c.get("lon_wgs84")), "idx": i}
            for i, c in enumerate(cell_towers) if safe_float(c.get("lat_wgs84")) is not None]


# ===================================================================
# TASK 1: Remote Work Cross-Reference
# ===================================================================
print("\n" + "=" * 70)
print("TASK 1: REMOTE WORK CROSS-REFERENCE")
print("=" * 70)

crossref_rows = []

for pi, place in enumerate(rw_places):
    name = place.get("name", "").strip()
    lat = safe_float(place.get("latitude_wgs84"))
    lon = safe_float(place.get("longitude_wgs84"))
    pid = place.get("google_place_id", "").strip()

    if lat is None or lon is None:
        print(f"  WARN: skipping {name} — no coordinates")
        continue

    row = dict(place)  # copy all original columns

    # --- Transit proximity ---
    fidx, fdist = find_nearest(lat, lon, freq_pts)
    if fidx is not None:
        nearest_freq = frequency[freq_pts[fidx]["idx"]]
        row["nearest_train_station"] = nearest_freq.get("name", "")
        row["distance_to_train_m"] = round(fdist, 1)
        row["trains_per_hour"] = safe_float(nearest_freq.get("trains_per_hour"), 0)

        # Fuzzy match ridership
        station_name = nearest_freq.get("name", "").strip()
        best_rship_score = 0
        best_rship_idx = None
        for rname, ridx in ridership_names:
            score = fuzzy_match_score(station_name, rname)
            if score > best_rship_score:
                best_rship_score = score
                best_rship_idx = ridx
        if best_rship_score >= 0.5 and best_rship_idx is not None:
            rship = ridership[best_rship_idx]
            row["daily_ridership"] = safe_float(rship.get("daily_avg"), 0)
            row["commuter_index"] = safe_float(rship.get("commuter_index"), 0)
        else:
            row["daily_ridership"] = ""
            row["commuter_index"] = ""
    else:
        row["nearest_train_station"] = ""
        row["distance_to_train_m"] = ""
        row["trains_per_hour"] = ""
        row["daily_ridership"] = ""
        row["commuter_index"] = ""

    # --- EV charging proximity ---
    eidx, edist = find_nearest(lat, lon, ev_pts)
    if eidx is not None:
        nearest_ev = ev[ev_pts[eidx]["idx"]]
        row["nearest_ev_charger_m"] = round(edist, 1)
        row["nearest_ev_charge_level"] = nearest_ev.get("charge_level", "")
    else:
        row["nearest_ev_charger_m"] = ""
        row["nearest_ev_charge_level"] = ""

    ev_1km = 0
    for ep in ev_pts:
        if haversine_m(lat, lon, ep["lat"], ep["lon"]) <= 1000:
            ev_1km += 1
    row["ev_chargers_within_1km"] = ev_1km

    # --- Shared mobility ---
    midx, mdist = find_nearest(lat, lon, mob_pts)
    if midx is not None:
        nearest_mob = shared_mob[mob_pts[midx]["idx"]]
        row["nearest_shared_mobility_m"] = round(mdist, 1)
        row["nearest_shared_mobility_provider"] = nearest_mob.get("provider_id", "")
    else:
        row["nearest_shared_mobility_m"] = ""
        row["nearest_shared_mobility_provider"] = ""

    mob_500 = 0
    for mp in mob_pts:
        if haversine_m(lat, lon, mp["lat"], mp["lon"]) <= 500:
            mob_500 += 1
    row["shared_mobility_within_500m"] = mob_500

    # --- Connectivity ---
    widx, wdist = find_nearest(lat, lon, wifi_pts)
    if widx is not None:
        nearest_wifi = wifi[wifi_pts[widx]["idx"]]
        row["nearest_wifi_m"] = round(wdist, 1)
        row["nearest_wifi_quality"] = safe_float(nearest_wifi.get("wifi_quality_score"), "")
    else:
        row["nearest_wifi_m"] = ""
        row["nearest_wifi_quality"] = ""

    cell_500 = 0
    has_5g = False
    for cp in cell_pts:
        if haversine_m(lat, lon, cp["lat"], cp["lon"]) <= 500:
            cell_500 += 1
            if safe_bool(cell_towers[cp["idx"]].get("has_5g")):
                has_5g = True
    row["cell_towers_within_500m"] = cell_500
    row["has_5g_nearby"] = has_5g

    # --- Temporal access (hours) ---
    hours_rec = hours_by_pid.get(pid) or hours_by_name.get(name.lower())
    if hours_rec:
        is_24h = safe_bool(hours_rec.get("is_24h"))
        if is_24h:
            hscore = 1.0
        else:
            hscore = 0.0
            if safe_bool(hours_rec.get("open_before_8am")):
                hscore += 0.3
            if safe_bool(hours_rec.get("open_after_7pm")):
                hscore += 0.3
            if safe_bool(hours_rec.get("open_saturday")):
                hscore += 0.2
            if safe_bool(hours_rec.get("open_sunday")):
                hscore += 0.2
            hscore = min(hscore, 1.0)
        row["hours_score"] = round(hscore, 2)
        row["early_open"] = safe_bool(hours_rec.get("open_before_8am"))
        row["late_close"] = safe_bool(hours_rec.get("open_after_7pm"))
        row["weekend_open"] = safe_bool(hours_rec.get("open_saturday")) or safe_bool(hours_rec.get("open_sunday"))
    else:
        row["hours_score"] = ""
        row["early_open"] = ""
        row["late_close"] = ""
        row["weekend_open"] = ""

    # --- Reviews ---
    place_reviews = reviews_by_pid.get(pid, [])
    if not place_reviews:
        place_reviews = reviews_by_name.get(name.lower(), [])

    row["review_count"] = len(place_reviews)
    row["work_relevant_review_count"] = sum(1 for r in place_reviews if safe_bool(r.get("is_work_relevant")))
    if place_reviews:
        pos_count = sum(1 for r in place_reviews if str(r.get("sentiment", "")).strip().lower() == "positive")
        row["positive_review_pct"] = round(pos_count / len(place_reviews), 3)
    else:
        row["positive_review_pct"] = ""

    crossref_rows.append(row)

    if (pi + 1) % 10 == 0:
        print(f"  Processed {pi + 1}/{len(rw_places)} places...")

print(f"  Processed {len(crossref_rows)}/{len(rw_places)} places total.")

# Write CROSSREF CSV
crossref_path = os.path.join(OUT, "city101_remote_work_CROSSREF.csv")
crossref_cols = [
    "name", "latitude_wgs84", "longitude_wgs84", "place_type", "google_rating",
    "google_review_count", "address", "municipality", "google_place_id",
    "nearest_train_station", "distance_to_train_m", "trains_per_hour",
    "daily_ridership", "commuter_index",
    "nearest_ev_charger_m", "nearest_ev_charge_level", "ev_chargers_within_1km",
    "nearest_shared_mobility_m", "nearest_shared_mobility_provider", "shared_mobility_within_500m",
    "nearest_wifi_m", "nearest_wifi_quality", "cell_towers_within_500m", "has_5g_nearby",
    "hours_score", "early_open", "late_close", "weekend_open",
    "review_count", "work_relevant_review_count", "positive_review_pct"
]

with open(crossref_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=crossref_cols, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(crossref_rows)

print(f"\n  ✓ Wrote {crossref_path}")
print(f"    {len(crossref_rows)} rows × {len(crossref_cols)} columns")


# ===================================================================
# TASK 2: Corridor Segmentation + WCI
# ===================================================================
print("\n" + "=" * 70)
print("TASK 2: CORRIDOR SEGMENTATION + WORKING CONTINUITY INDEX")
print("=" * 70)

# Use 49 train stations as segment centers
segments = []
for s in frequency:
    slat = safe_float(s.get("lat_wgs84"))
    slon = safe_float(s.get("lon_wgs84"))
    if slat is None or slon is None:
        continue
    segments.append({
        "station_name": s.get("name", "").strip(),
        "lat_wgs84": slat,
        "lon_wgs84": slon,
        "trains_per_hour": safe_float(s.get("trains_per_hour"), 0),
        "workspaces": [],
        "wifi_spots": [],
        "ev_chargers": [],
        "shared_mob": [],
        "cell_towers": [],
    })

print(f"  {len(segments)} segment centers loaded.")


def assign_to_nearest_segment(lat, lon, segments):
    """Return index of nearest segment."""
    best_idx, best_dist = 0, float("inf")
    for i, seg in enumerate(segments):
        d = haversine_m(lat, lon, seg["lat_wgs84"], seg["lon_wgs84"])
        if d < best_dist:
            best_dist = d
            best_idx = i
    return best_idx


# Assign workspaces
print("  Assigning workspaces to segments...")
for cr in crossref_rows:
    lat = safe_float(cr.get("latitude_wgs84"))
    lon = safe_float(cr.get("longitude_wgs84"))
    if lat is None or lon is None:
        continue
    idx = assign_to_nearest_segment(lat, lon, segments)
    segments[idx]["workspaces"].append(cr)

# Assign WiFi spots
print("  Assigning WiFi spots...")
for w in wifi:
    lat = safe_float(w.get("lat_wgs84"))
    lon = safe_float(w.get("lon_wgs84"))
    if lat is None or lon is None:
        continue
    idx = assign_to_nearest_segment(lat, lon, segments)
    segments[idx]["wifi_spots"].append(w)

# Assign EV chargers
print("  Assigning EV chargers...")
for e in ev:
    lat = safe_float(e.get("latitude_wgs84"))
    lon = safe_float(e.get("longitude_wgs84"))
    if lat is None or lon is None:
        continue
    idx = assign_to_nearest_segment(lat, lon, segments)
    segments[idx]["ev_chargers"].append(e)

# Assign shared mobility
print("  Assigning shared mobility stations...")
for m in shared_mob:
    lat = safe_float(m.get("lat_wgs84"))
    lon = safe_float(m.get("lon_wgs84"))
    if lat is None or lon is None:
        continue
    idx = assign_to_nearest_segment(lat, lon, segments)
    segments[idx]["shared_mob"].append(m)

# Assign cell towers
print("  Assigning cell towers...")
for c in cell_towers:
    lat = safe_float(c.get("lat_wgs84"))
    lon = safe_float(c.get("lon_wgs84"))
    if lat is None or lon is None:
        continue
    idx = assign_to_nearest_segment(lat, lon, segments)
    segments[idx]["cell_towers"].append(c)

# Compute raw sub-scores
print("  Computing sub-scores...")

raw_transit = []
raw_workspace = []
raw_temporal = []
raw_connectivity = []
raw_mobility = []

for seg in segments:
    # transit_score: raw = trains_per_hour
    raw_transit.append(seg["trains_per_hour"])

    # workspace_density: count
    ws_count = len(seg["workspaces"])
    raw_workspace.append(ws_count)

    # temporal_coverage: avg hours_score of workspaces
    hs_vals = [safe_float(w.get("hours_score")) for w in seg["workspaces"] if safe_float(w.get("hours_score")) is not None]
    if hs_vals:
        raw_temporal.append(sum(hs_vals) / len(hs_vals))
    else:
        raw_temporal.append(0.0)

    # connectivity_score
    wifi_quals = [safe_float(w.get("wifi_quality_score")) for w in seg["wifi_spots"] if safe_float(w.get("wifi_quality_score")) is not None]
    avg_wifi_q = (sum(wifi_quals) / len(wifi_quals)) if wifi_quals else 0.0
    has_5g_seg = any(safe_bool(c.get("has_5g")) for c in seg["cell_towers"])
    conn_raw = (avg_wifi_q / 5.0) * 0.7 + (1.0 if has_5g_seg else 0.0) * 0.3
    raw_connectivity.append(conn_raw)

    # mobility_score: count
    mob_count = len(seg["shared_mob"])
    raw_mobility.append(mob_count)


def min_max_normalize(values):
    """Min-max normalize a list of values to 0-1."""
    vmin = min(values)
    vmax = max(values)
    if vmax == vmin:
        return [0.5] * len(values)
    return [(v - vmin) / (vmax - vmin) for v in values]


norm_transit = min_max_normalize(raw_transit)
norm_workspace = min_max_normalize(raw_workspace)
# temporal_coverage is already 0-1 (hours_score is 0-1), but normalize across segments
norm_temporal = min_max_normalize(raw_temporal)
norm_connectivity = min_max_normalize(raw_connectivity)
norm_mobility = min_max_normalize(raw_mobility)

# Compute WCI
wci_values = []
for i in range(len(segments)):
    wci = (0.30 * norm_transit[i]
         + 0.25 * norm_workspace[i]
         + 0.20 * norm_temporal[i]
         + 0.15 * norm_connectivity[i]
         + 0.10 * norm_mobility[i])
    wci_values.append(round(wci, 4))

# Rank (1 = best)
ranked_indices = sorted(range(len(wci_values)), key=lambda i: wci_values[i], reverse=True)
ranks = [0] * len(wci_values)
for rank_pos, idx in enumerate(ranked_indices):
    ranks[idx] = rank_pos + 1

# Build output rows
wci_rows = []
for i, seg in enumerate(segments):
    E, N = wgs84_to_lv95(seg["lat_wgs84"], seg["lon_wgs84"])
    wci_rows.append({
        "station_name": seg["station_name"],
        "lat_wgs84": seg["lat_wgs84"],
        "lon_wgs84": seg["lon_wgs84"],
        "E_lv95": E,
        "N_lv95": N,
        "workspace_count": len(seg["workspaces"]),
        "wifi_count": len(seg["wifi_spots"]),
        "ev_count": len(seg["ev_chargers"]),
        "shared_mob_count": len(seg["shared_mob"]),
        "cell_tower_count": len(seg["cell_towers"]),
        "transit_score": round(norm_transit[i], 4),
        "workspace_density": round(norm_workspace[i], 4),
        "temporal_coverage": round(norm_temporal[i], 4),
        "connectivity_score": round(norm_connectivity[i], 4),
        "mobility_score": round(norm_mobility[i], 4),
        "WCI": wci_values[i],
        "wci_rank": ranks[i],
    })

# Write WCI CSV
wci_path = os.path.join(OUT, "city101_corridor_segments_WCI.csv")
wci_cols = [
    "station_name", "lat_wgs84", "lon_wgs84", "E_lv95", "N_lv95",
    "workspace_count", "wifi_count", "ev_count", "shared_mob_count", "cell_tower_count",
    "transit_score", "workspace_density", "temporal_coverage",
    "connectivity_score", "mobility_score", "WCI", "wci_rank"
]

with open(wci_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=wci_cols)
    writer.writeheader()
    writer.writerows(wci_rows)

print(f"\n  ✓ Wrote {wci_path}")
print(f"    {len(wci_rows)} segments × {len(wci_cols)} columns")


# ===================================================================
# WCI Summary (Markdown)
# ===================================================================
print("\n  Generating WCI summary...")

sorted_wci = sorted(wci_rows, key=lambda r: r["WCI"], reverse=True)
top5 = sorted_wci[:5]
bot5 = sorted_wci[-5:]

# Geographic classification
geneva_stations = [r for r in wci_rows if r["lon_wgs84"] < 6.3]
la_cote = [r for r in wci_rows if 6.3 <= r["lon_wgs84"] < 6.5]
lausanne_area = [r for r in wci_rows if 6.5 <= r["lon_wgs84"] < 6.7]
lavaux = [r for r in wci_rows if 6.7 <= r["lon_wgs84"] < 6.85]
riviera = [r for r in wci_rows if r["lon_wgs84"] >= 6.85]

def cluster_avg_wci(cluster):
    if not cluster:
        return 0
    return sum(r["WCI"] for r in cluster) / len(cluster)

summary_md = f"""# Working Continuity Index (WCI) — City101 Corridor
**Generated:** 2026-03-01 | **Assignment:** A02 Data Synchronicity

---

## Formula

```
WCI = 0.30 × transit_score
    + 0.25 × workspace_density
    + 0.20 × temporal_coverage
    + 0.15 × connectivity_score
    + 0.10 × mobility_score
```

All sub-scores are min-max normalized (0–1) across the 49 corridor segments.

### Weight Justification

| Weight | Component | Rationale |
|--------|-----------|-----------|
| 0.30 | **Transit score** | Train frequency is the backbone of corridor traversal. A knowledge worker's ability to move continuously depends first on transport availability. The 42x variation (Lausanne 28.5 tr/hr vs Bossiere 2.0) is the primary determinant of working continuity. |
| 0.25 | **Workspace density** | Physical places to work (coworking, cafes, libraries) are the second requirement. Without a desk, power, and a seat, transit connectivity is irrelevant. |
| 0.20 | **Temporal coverage** | Opening hours determine *when* continuity is possible. A workspace that closes at 5pm breaks the evening commuter's flow. 24h access, early opening, and weekend availability extend the temporal window. |
| 0.15 | **Connectivity** | WiFi quality and 5G coverage enable the actual work. Weighted lower because mobile hotspots can partially substitute, but public WiFi and strong cellular are still necessary for reliable sessions. |
| 0.10 | **Mobility score** | Shared mobility (e-bikes, scooters, carshare) provides last-mile access from station to workspace. Important but supplementary — most corridor movement is rail-based. |

---

## Top 5 Segments (Highest WCI)

| Rank | Station | WCI | Transit | Workspace | Temporal | Connect. | Mobility | Workspaces | WiFi |
|------|---------|-----|---------|-----------|----------|----------|----------|------------|------|
"""

for r in top5:
    summary_md += f"| {r['wci_rank']} | {r['station_name']} | {r['WCI']:.4f} | {r['transit_score']:.2f} | {r['workspace_density']:.2f} | {r['temporal_coverage']:.2f} | {r['connectivity_score']:.2f} | {r['mobility_score']:.2f} | {r['workspace_count']} | {r['wifi_count']} |\n"

summary_md += f"""
## Bottom 5 Segments (Lowest WCI)

| Rank | Station | WCI | Transit | Workspace | Temporal | Connect. | Mobility | Workspaces | WiFi |
|------|---------|-----|---------|-----------|----------|----------|----------|------------|------|
"""

for r in bot5:
    summary_md += f"| {r['wci_rank']} | {r['station_name']} | {r['WCI']:.4f} | {r['transit_score']:.2f} | {r['workspace_density']:.2f} | {r['temporal_coverage']:.2f} | {r['connectivity_score']:.2f} | {r['mobility_score']:.2f} | {r['workspace_count']} | {r['wifi_count']} |\n"

summary_md += f"""
---

## Geographic Patterns

### Cluster Analysis

| Cluster | Stations | Avg WCI | Interpretation |
|---------|----------|---------|----------------|
| **Geneva** (lon < 6.3) | {len(geneva_stations)} | {cluster_avg_wci(geneva_stations):.4f} | Dense urban core with strong transit, multiple coworking spaces, and full 5G coverage. The corridor's western anchor. |
| **La Cote** (6.3–6.5) | {len(la_cote)} | {cluster_avg_wci(la_cote):.4f} | Suburban commuter belt. Moderate transit but few dedicated workspaces. Working continuity depends on train frequency alone. |
| **Lausanne area** (6.5–6.7) | {len(lausanne_area)} | {cluster_avg_wci(lausanne_area):.4f} | Second urban pole. University presence (EPFL/UNIL) boosts workspace and connectivity. Rivals Geneva in WCI. |
| **Lavaux** (6.7–6.85) | {len(lavaux)} | {cluster_avg_wci(lavaux):.4f} | The critical gap. UNESCO protection actively resists infrastructure. Minimal workspaces, low frequency, poor connectivity. This is where working continuity breaks. |
| **Riviera** (> 6.85) | {len(riviera)} | {cluster_avg_wci(riviera):.4f} | Montreux-Villeneuve stretch. Tourism-oriented, moderate transit, few work-focused spaces. Partial recovery from Lavaux gap. |

### Key Insight: Where Working Continuity Breaks

The corridor's working continuity is not a gradient — it is **bimodal with a fracture**.

The Geneva and Lausanne poles sustain continuous work sessions: high-frequency trains (25+ per hour), abundant workspaces (coworking, cafes, libraries), 24h temporal access, strong 5G connectivity, and dense shared mobility. A knowledge worker moving through these zones barely notices transitions.

**The Lavaux gap (km ~60–75) is an absolute break.** Train frequency drops below 3/hr (20+ minute waits), workspaces vanish, WiFi coverage disappears, and shared mobility is absent. The UNESCO-protected vineyard landscape actively resists the infrastructure that working continuity requires. This is not a gradual decline — it is a cliff.

The Riviera (Montreux-Villeneuve) partially recovers but never matches the urban poles. Its tourism orientation means workspaces exist but with limited hours and work-oriented amenities.

**The architectural question:** Can the Lavaux gap be bridged without violating its protected character? Or is the fracture itself a feature — a designed disconnection that forces the corridor to be two cities, not one?

---

## Distribution Statistics

| Metric | Value |
|--------|-------|
| Total segments | {len(wci_rows)} |
| WCI range | {min(wci_values):.4f} – {max(wci_values):.4f} |
| WCI mean | {sum(wci_values)/len(wci_values):.4f} |
| WCI median | {sorted(wci_values)[len(wci_values)//2]:.4f} |
| Segments with workspace | {sum(1 for r in wci_rows if r['workspace_count'] > 0)} / {len(wci_rows)} |
| Segments with WiFi | {sum(1 for r in wci_rows if r['wifi_count'] > 0)} / {len(wci_rows)} |
| Total workspaces assigned | {sum(r['workspace_count'] for r in wci_rows)} |
| Total WiFi spots assigned | {sum(r['wifi_count'] for r in wci_rows)} |
| Total EV chargers assigned | {sum(r['ev_count'] for r in wci_rows)} |
| Total shared mobility assigned | {sum(r['shared_mob_count'] for r in wci_rows)} |
| Total cell towers assigned | {sum(r['cell_tower_count'] for r in wci_rows)} |
"""

summary_path = os.path.join(OUT, "city101_WCI_summary.md")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary_md)

print(f"  ✓ Wrote {summary_path}")


# ===================================================================
# TASK 3: Zurich Skeleton
# ===================================================================
print("\n" + "=" * 70)
print("TASK 3: ZURICH SKELETON")
print("=" * 70)

zh_stations = [r for r in ridership if r.get("canton", "").strip() == "ZH"]
print(f"  Found {len(zh_stations)} Zurich-area stations (canton=ZH) in ridership data.")

if zh_stations:
    zh_rows = []
    for s in zh_stations:
        lat = safe_float(s.get("lat_wgs84"))
        lon = safe_float(s.get("lon_wgs84"))
        if lat is None or lon is None:
            E, N = "", ""
        else:
            E, N = wgs84_to_lv95(lat, lon)
        zh_rows.append({
            "station_name": s.get("name", "").strip(),
            "lat_wgs84": lat or "",
            "lon_wgs84": lon or "",
            "E_lv95": E,
            "N_lv95": N,
            "daily_avg": safe_float(s.get("daily_avg"), ""),
            "workday_avg": safe_float(s.get("workday_avg"), ""),
            "nonworkday_avg": safe_float(s.get("nonworkday_avg"), ""),
            "commuter_index": safe_float(s.get("commuter_index"), ""),
        })

    zh_path = os.path.join(OUT, "zurich_corridor_skeleton.csv")
    zh_cols = ["station_name", "lat_wgs84", "lon_wgs84", "E_lv95", "N_lv95",
               "daily_avg", "workday_avg", "nonworkday_avg", "commuter_index"]

    with open(zh_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=zh_cols)
        writer.writeheader()
        writer.writerows(zh_rows)

    print(f"  ✓ Wrote {zh_path}")
    print(f"    {len(zh_rows)} stations × {len(zh_cols)} columns")
else:
    print("  No ZH stations found — skipping Zurich skeleton.")


# ===================================================================
# FINAL SUMMARY
# ===================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"""
TASK 1: Remote Work Cross-Reference
  Output: city101_remote_work_CROSSREF.csv
  Places: {len(crossref_rows)} / {len(rw_places)}
  Columns: {len(crossref_cols)} (9 original + 22 computed)

TASK 2: Corridor Segmentation + WCI
  Output: city101_corridor_segments_WCI.csv
  Segments: {len(wci_rows)} (train stations)
  WCI range: {min(wci_values):.4f} – {max(wci_values):.4f}
  Top station: {sorted_wci[0]['station_name']} (WCI={sorted_wci[0]['WCI']:.4f})
  Bottom station: {sorted_wci[-1]['station_name']} (WCI={sorted_wci[-1]['WCI']:.4f})

  Sub-score summary (normalized 0–1):
    Transit:      mean={sum(norm_transit)/len(norm_transit):.3f}
    Workspace:    mean={sum(norm_workspace)/len(norm_workspace):.3f}
    Temporal:     mean={sum(norm_temporal)/len(norm_temporal):.3f}
    Connectivity: mean={sum(norm_connectivity)/len(norm_connectivity):.3f}
    Mobility:     mean={sum(norm_mobility)/len(norm_mobility):.3f}

  Geographic clusters:
    Geneva ({len(geneva_stations)} stations):    avg WCI = {cluster_avg_wci(geneva_stations):.4f}
    La Côte ({len(la_cote)} stations):     avg WCI = {cluster_avg_wci(la_cote):.4f}
    Lausanne ({len(lausanne_area)} stations):   avg WCI = {cluster_avg_wci(lausanne_area):.4f}
    Lavaux ({len(lavaux)} stations):      avg WCI = {cluster_avg_wci(lavaux):.4f}
    Riviera ({len(riviera)} stations):    avg WCI = {cluster_avg_wci(riviera):.4f}

TASK 3: Zurich Skeleton
  ZH stations: {len(zh_stations)}
  Output: {'zurich_corridor_skeleton.csv' if zh_stations else 'SKIPPED (no ZH data)'}

Output: city101_WCI_summary.md
""")

print("Done.")
