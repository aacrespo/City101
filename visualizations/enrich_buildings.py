"""
Enrich City101 buildings with opening hours from OSM Overpass and Google Places.

Usage:
    # OSM only (free, no API key):
    python enrich_buildings.py

    # OSM + Google Places:
    python enrich_buildings.py --google-key YOUR_API_KEY

Output:
    data_henna/city101_buildings_enriched.csv
"""
import pandas as pd
import requests
import time
import json
import os
import sys
import math
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE), "data_henna")
CSV_PATH = os.path.join(DATA_DIR, "city101_buildings_classified_v3.csv")
OUT_PATH = os.path.join(DATA_DIR, "city101_buildings_enriched.csv")

# Corridor bounding box (slightly expanded)
BBOX_S, BBOX_W = 46.12, 5.95
BBOX_N, BBOX_E = 46.61, 7.03

# ─── OSM OVERPASS ───

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def query_osm_opening_hours():
    """Query OSM for all POIs with opening_hours in the corridor."""
    print("Querying OSM Overpass for opening_hours data...")

    # Split the corridor into chunks to avoid timeout
    # The corridor is ~110km long, split into 4 longitudinal chunks
    lon_splits = [5.95, 6.22, 6.50, 6.78, 7.03]
    all_pois = []

    for i in range(len(lon_splits) - 1):
        w, e = lon_splits[i], lon_splits[i + 1]
        print(f"  Chunk {i+1}/4: lon {w:.2f}-{e:.2f}...")

        query = f"""
[out:json][timeout:120];
(
  node["opening_hours"]({BBOX_S},{w},{BBOX_N},{e});
  way["opening_hours"]({BBOX_S},{w},{BBOX_N},{e});
  relation["opening_hours"]({BBOX_S},{w},{BBOX_N},{e});
);
out center body;
"""
        try:
            resp = requests.post(OVERPASS_URL, data={'data': query}, timeout=180)
            resp.raise_for_status()
            data = resp.json()

            for el in data.get('elements', []):
                tags = el.get('tags', {})
                lat = el.get('lat') or (el.get('center', {}).get('lat'))
                lon = el.get('lon') or (el.get('center', {}).get('lon'))
                if lat and lon and tags.get('opening_hours'):
                    poi = {
                        'osm_id': el['id'],
                        'osm_type': el['type'],
                        'lat': lat,
                        'lon': lon,
                        'opening_hours': tags.get('opening_hours', ''),
                        'name': tags.get('name', ''),
                        'amenity': tags.get('amenity', ''),
                        'shop': tags.get('shop', ''),
                        'tourism': tags.get('tourism', ''),
                        'leisure': tags.get('leisure', ''),
                        'healthcare': tags.get('healthcare', ''),
                        'office': tags.get('office', ''),
                    }
                    all_pois.append(poi)

            print(f"    Found {len(data.get('elements', []))} elements, {len(all_pois)} total POIs so far")
            time.sleep(1)  # Rate limit
        except Exception as e:
            print(f"    Warning: chunk {i+1} failed: {e}")
            time.sleep(5)

    print(f"  Total OSM POIs with opening_hours: {len(all_pois)}")
    return all_pois


def haversine_m(lat1, lon1, lat2, lon2):
    """Haversine distance in meters."""
    R = 6371000
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def build_spatial_index(pois, grid_size=0.005):
    """Build a simple grid index for fast spatial lookup."""
    grid = defaultdict(list)
    for poi in pois:
        gx = int(poi['lon'] / grid_size)
        gy = int(poi['lat'] / grid_size)
        grid[(gx, gy)].append(poi)
    return grid, grid_size


def find_nearest_poi(lat, lon, grid, grid_size, max_dist_m=30):
    """Find nearest POI within max_dist_m meters."""
    gx = int(lon / grid_size)
    gy = int(lat / grid_size)

    best = None
    best_dist = max_dist_m + 1

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for poi in grid.get((gx + dx, gy + dy), []):
                d = haversine_m(lat, lon, poi['lat'], poi['lon'])
                if d < best_dist:
                    best_dist = d
                    best = poi

    return best, best_dist if best else (None, None)


def match_osm_to_buildings(csv_df, pois):
    """Match OSM POIs to buildings by proximity.

    Enriches:
    - All buildings missing opening_hours (work + residential + other)
    - Building names from OSM POIs
    """
    print("Building spatial index...")
    grid, gs = build_spatial_index(pois)

    print("Matching OSM POIs to all buildings...")
    # Match ALL buildings missing opening_hours
    missing_mask = csv_df['opening_hours'].isna()
    missing_indices = csv_df.index[missing_mask]
    print(f"  Buildings missing opening_hours: {len(missing_indices)}")

    matched = 0
    enriched_hours = {}
    enriched_names = {}

    for i, idx in enumerate(missing_indices):
        row = csv_df.loc[idx]
        poi, dist = find_nearest_poi(row['latitude_wgs84'], row['longitude_wgs84'], grid, gs, max_dist_m=30)
        if poi:
            enriched_hours[idx] = poi['opening_hours']
            if poi['name'] and pd.isna(row.get('osm_poi_name', float('nan'))):
                enriched_names[idx] = poi['name']
            matched += 1

        if (i + 1) % 50000 == 0:
            print(f"    Processed {i+1}/{len(missing_indices)}...")

    if len(missing_indices) > 0:
        print(f"  Matched: {matched} buildings ({matched/len(missing_indices)*100:.1f}%)")
    else:
        print(f"  No buildings to enrich (all have opening_hours)")
    return enriched_hours, enriched_names


# ─── GOOGLE PLACES ───

def query_google_places(csv_df, api_key, enriched_hours, max_queries=5000):
    """Query Google Places for buildings still missing opening hours after OSM."""
    print(f"\nQuerying Google Places (max {max_queries} queries)...")

    # Focus on work buildings still missing hours
    work_mask = (csv_df['use_category'] == 'work') & (csv_df['opening_hours'].isna())
    remaining = [idx for idx in csv_df.index[work_mask] if idx not in enriched_hours]
    if len(remaining) == 0:
        # If all work buildings have hours, try other buildings
        other_mask = csv_df['opening_hours'].isna()
        remaining = [idx for idx in csv_df.index[other_mask] if idx not in enriched_hours]
    print(f"  Buildings still missing after OSM: {len(remaining)}")

    # Prioritize larger buildings (more likely to be significant businesses)
    remaining_df = csv_df.loc[remaining].sort_values('area_m2', ascending=False)
    to_query = remaining_df.head(max_queries)
    print(f"  Querying top {len(to_query)} by area...")

    google_hours = {}
    google_names = {}
    queries_made = 0

    for idx, row in to_query.iterrows():
        lat, lon = row['latitude_wgs84'], row['longitude_wgs84']
        sector = row['sector']

        # Map sector to Google Places type
        type_map = {
            'commercial': 'store', 'food_retail': 'grocery_or_supermarket',
            'hospitality': 'restaurant', 'healthcare': 'hospital',
            'education': 'school', 'office_professional': 'accounting',
            'sports_fitness': 'gym', 'entertainment': 'movie_theater',
            'automotive': 'car_repair', 'fashion_retail': 'clothing_store',
            'tourism': 'tourist_attraction', 'finance': 'bank',
        }
        place_type = type_map.get(sector, '')

        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': f'{lat},{lon}',
            'radius': 30,
            'key': api_key,
        }
        if place_type:
            params['type'] = place_type

        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            if data.get('results'):
                place = data['results'][0]
                place_id = place.get('place_id')

                # Get detailed hours via Place Details
                if place_id:
                    det_url = "https://maps.googleapis.com/maps/api/place/details/json"
                    det_params = {
                        'place_id': place_id,
                        'fields': 'opening_hours,name',
                        'key': api_key,
                    }
                    det_resp = requests.get(det_url, params=det_params, timeout=10)
                    det_data = det_resp.json()
                    result = det_data.get('result', {})

                    if 'opening_hours' in result:
                        periods = result['opening_hours'].get('weekday_text', [])
                        if periods:
                            google_hours[idx] = '; '.join(periods)
                    if 'name' in result:
                        google_names[idx] = result['name']

            queries_made += 1
            if queries_made % 100 == 0:
                print(f"    Queried {queries_made}/{len(to_query)}...")

            # Rate limit: ~10 QPS
            time.sleep(0.1)

        except Exception as e:
            if queries_made % 500 == 0:
                print(f"    Warning at query {queries_made}: {e}")
            time.sleep(0.5)

    print(f"  Google Places: {len(google_hours)} buildings enriched with hours")
    print(f"  Google Places: {len(google_names)} buildings enriched with names")
    return google_hours, google_names


# ─── NIGHT STATUS REFINEMENT ───

def refine_night_status(opening_hours_str):
    """Infer night_status from opening_hours string."""
    if not opening_hours_str or pd.isna(opening_hours_str):
        return None

    oh = opening_hours_str.lower().strip()

    if '24/7' in oh or '24 hours' in oh:
        return 'open_24h'

    # Check for late hours (past 22:00)
    import re
    times = re.findall(r'(\d{1,2}):?(\d{2})?\s*-\s*(\d{1,2}):?(\d{2})?', oh)
    for match in times:
        close_h = int(match[2])
        if close_h >= 22 or close_h <= 4:
            return 'open_late'

    # Check for early morning starts (before 06:00)
    for match in times:
        open_h = int(match[0])
        if open_h <= 5:
            return 'night_shift'

    return 'closed_at_night'


# ─── MAIN ───

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--google-key', help='Google Places API key')
    parser.add_argument('--max-google', type=int, default=5000, help='Max Google Places queries')
    args = parser.parse_args()

    t0 = time.time()

    # Load CSV
    print("Loading CSV...")
    df = pd.read_csv(CSV_PATH)
    print(f"  Rows: {len(df)}")
    print(f"  opening_hours filled: {df['opening_hours'].notna().sum()}")
    print(f"  Work buildings: {(df['use_category'] == 'work').sum()}")
    print(f"  Work buildings missing opening_hours: {((df['use_category'] == 'work') & (df['opening_hours'].isna())).sum()}")

    # Step 1: OSM Overpass enrichment
    pois = query_osm_opening_hours()
    osm_hours, osm_names = match_osm_to_buildings(df, pois)

    # Step 2: Google Places enrichment (optional)
    google_hours = {}
    google_names = {}
    if args.google_key:
        google_hours, google_names = query_google_places(
            df, args.google_key, osm_hours, max_queries=args.max_google
        )

    # Step 3: Apply enrichments
    print("\nApplying enrichments...")

    # Create enriched columns
    df['opening_hours_enriched'] = df['opening_hours'].copy()
    df['enrichment_source'] = ''

    for idx, hours in osm_hours.items():
        if pd.isna(df.at[idx, 'opening_hours_enriched']):
            df.at[idx, 'opening_hours_enriched'] = hours
            df.at[idx, 'enrichment_source'] = 'osm'

    for idx, hours in google_hours.items():
        if pd.isna(df.at[idx, 'opening_hours_enriched']):
            df.at[idx, 'opening_hours_enriched'] = hours
            df.at[idx, 'enrichment_source'] = 'google'

    for idx, name in {**osm_names, **google_names}.items():
        if pd.isna(df.at[idx, 'osm_poi_name']) or df.at[idx, 'osm_poi_name'] == '':
            df.at[idx, 'osm_poi_name'] = name

    # Step 4: Refine night_status based on new opening hours
    df['night_status_enriched'] = df['night_status'].copy()
    refined_count = 0
    for idx in df.index:
        if df.at[idx, 'enrichment_source'] != '':
            new_ns = refine_night_status(df.at[idx, 'opening_hours_enriched'])
            if new_ns and new_ns != df.at[idx, 'night_status']:
                df.at[idx, 'night_status_enriched'] = new_ns
                refined_count += 1

    # Step 5: Save
    df.to_csv(OUT_PATH, index=False)
    print(f"\nSaved: {OUT_PATH}")

    # Summary
    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print(f"ENRICHMENT COMPLETE ({elapsed:.1f}s)")
    print(f"{'='*60}")
    print(f"  Original opening_hours filled: {df['opening_hours'].notna().sum()}")
    print(f"  After enrichment filled: {df['opening_hours_enriched'].notna().sum()}")
    print(f"  New from OSM: {len(osm_hours)}")
    print(f"  New from Google: {len(google_hours)}")
    print(f"  Night status refined: {refined_count}")
    print(f"\n  Night status distribution (enriched):")
    print(f"  {df['night_status_enriched'].value_counts().to_string()}")


if __name__ == '__main__':
    main()
