#!/usr/bin/env python3
"""
Agent 1: GTFS Timetable — City101 Corridor Animation
Downloads Swiss GTFS, filters to 49 corridor stations, extracts weekday timetable.
Output: output/gtfs_corridor_trains.csv + output/gtfs_corridor_stops.csv
"""

import subprocess, sys, os, csv, math, time, zipfile, io, re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

for pkg in ['pandas']:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

import pandas as pd

BASE = Path('/Users/andreacrespo/CLAUDE/City101_ClaudeCode')
STATIONS_CSV = BASE / 'datasets/transit/city101_service_frequency_v2.csv'
FIRST_LAST_CSV = BASE / 'datasets/corridor_analysis/city101_first_last_trains.csv'
TMP_DIR = Path('/tmp/city101_gtfs')
OUT_TRAINS = BASE / 'output/gtfs_corridor_trains.csv'
OUT_STOPS = BASE / 'output/gtfs_corridor_stops.csv'

# GTFS source
GTFS_URL = "https://gtfs.geops.ch/dl/gtfs_complete.zip"

# Corridor bounding box
BBOX_LAT = (46.15, 46.55)
BBOX_LON = (6.05, 7.10)

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def normalize(s):
    s = str(s).strip()
    # Replace accented chars
    for old, new in [('è','e'),('é','e'),('ê','e'),('ë','e'),('à','a'),('â','a'),
                     ('ô','o'),('ö','o'),('ü','u'),('ä','a'),('î','i'),('ï','i')]:
        s = s.replace(old, new)
    return s.lower().strip()

# ── Step 1: Load canonical stations ──
print("STEP 1: Loading canonical 49 stations...")
canon_df = pd.read_csv(STATIONS_CSV)
canonical = {}
for _, row in canon_df.iterrows():
    name = row['name'].strip().strip('"')
    canonical[name] = {
        'station_id': str(row['station_id']),
        'lat': row['lat_wgs84'],
        'lon': row['lon_wgs84'],
        'name_norm': normalize(name),
    }
print(f"  {len(canonical)} stations loaded")

# ── Step 2: Download GTFS ──
print(f"\nSTEP 2: Downloading GTFS from {GTFS_URL}...")
os.makedirs(TMP_DIR, exist_ok=True)
zip_path = TMP_DIR / 'gtfs_complete.zip'

if zip_path.exists() and zip_path.stat().st_size > 50_000_000:
    print(f"  ZIP already exists ({zip_path.stat().st_size / 1024 / 1024:.1f} MB), reusing")
else:
    import urllib.request
    print("  Downloading... (this may take 1-3 minutes)")
    start = time.time()
    urllib.request.urlretrieve(GTFS_URL, str(zip_path))
    elapsed = time.time() - start
    size_mb = zip_path.stat().st_size / 1024 / 1024
    print(f"  Downloaded: {size_mb:.1f} MB in {elapsed:.0f}s")

# Extract needed files
print("  Extracting...")
needed = ['stops.txt', 'stop_times.txt', 'trips.txt', 'routes.txt', 'calendar.txt', 'calendar_dates.txt', 'shapes.txt']
with zipfile.ZipFile(zip_path, 'r') as zf:
    members = zf.namelist()
    for name in needed:
        if name in members:
            zf.extract(name, TMP_DIR)
            size = os.path.getsize(TMP_DIR / name) / 1024 / 1024
            print(f"    {name}: {size:.1f} MB")
        else:
            print(f"    {name}: NOT FOUND in archive")

# ── Step 3: Load stops and match to corridor ──
print("\nSTEP 3: Loading stops and matching to corridor...")
stops_df = pd.read_csv(TMP_DIR / 'stops.txt', dtype=str, low_memory=False)
print(f"  Total stops: {len(stops_df)}")

# Filter to bounding box first
stops_df['stop_lat'] = stops_df['stop_lat'].astype(float)
stops_df['stop_lon'] = stops_df['stop_lon'].astype(float)
bbox_stops = stops_df[
    (stops_df['stop_lat'] >= BBOX_LAT[0]) & (stops_df['stop_lat'] <= BBOX_LAT[1]) &
    (stops_df['stop_lon'] >= BBOX_LON[0]) & (stops_df['stop_lon'] <= BBOX_LON[1])
]
print(f"  In bounding box: {len(bbox_stops)}")

# Match GTFS stops to canonical stations
# Strategy: for each canonical station, find the closest GTFS stop (or parent station)
stop_to_canonical = {}  # gtfs_stop_id -> canonical_name
canonical_to_stops = defaultdict(list)  # canonical_name -> list of gtfs_stop_ids

for cname, cdata in canonical.items():
    # Try name match first
    name_matches = bbox_stops[bbox_stops['stop_name'].apply(normalize) == cdata['name_norm']]
    if len(name_matches) > 0:
        for _, stop in name_matches.iterrows():
            stop_to_canonical[stop['stop_id']] = cname
            canonical_to_stops[cname].append(stop['stop_id'])
        continue

    # Try partial name match
    cname_base = normalize(cname).split(',')[0].split('(')[0].strip()
    if len(cname_base) > 3:
        partial = bbox_stops[bbox_stops['stop_name'].apply(lambda x: cname_base in normalize(x))]
        if len(partial) > 0:
            for _, stop in partial.iterrows():
                stop_to_canonical[stop['stop_id']] = cname
                canonical_to_stops[cname].append(stop['stop_id'])
            continue

    # Spatial match: find closest stop within 1km
    best_dist = float('inf')
    best_stops = []
    for _, stop in bbox_stops.iterrows():
        d = haversine_m(cdata['lat'], cdata['lon'], stop['stop_lat'], stop['stop_lon'])
        if d < 1000 and d < best_dist + 200:  # keep all within 200m of best
            if d < best_dist:
                best_dist = d
                best_stops = [(stop['stop_id'], d)]
            else:
                best_stops.append((stop['stop_id'], d))

    if best_stops:
        for sid, d in best_stops:
            stop_to_canonical[sid] = cname
            canonical_to_stops[cname].append(sid)

# Also include parent stations: if a stop's parent maps to a canonical station, map all children too
if 'parent_station' in stops_df.columns:
    parent_map = {}
    for sid, cname in list(stop_to_canonical.items()):
        parent_map[sid] = cname
    for _, stop in bbox_stops.iterrows():
        parent = stop.get('parent_station', '')
        if pd.notna(parent) and parent in parent_map and stop['stop_id'] not in stop_to_canonical:
            stop_to_canonical[stop['stop_id']] = parent_map[parent]
            canonical_to_stops[parent_map[parent]].append(stop['stop_id'])

matched = len(canonical_to_stops)
unmatched = [c for c in canonical if c not in canonical_to_stops]
print(f"  Matched: {matched}/{len(canonical)} canonical stations")
if unmatched:
    print(f"  Unmatched: {unmatched}")
print(f"  Total GTFS stop IDs mapped: {len(stop_to_canonical)}")

# ── Step 4: Find representative weekday ──
print("\nSTEP 4: Finding representative weekday...")
cal_df = pd.read_csv(TMP_DIR / 'calendar.txt', dtype=str)
cal_dates_path = TMP_DIR / 'calendar_dates.txt'
cal_dates_df = pd.read_csv(cal_dates_path, dtype=str) if os.path.exists(cal_dates_path) else pd.DataFrame()

# Find a Tuesday or Wednesday in the current calendar period
today = datetime.now()
target_date = today
# Find next Tuesday (1) or Wednesday (2)
while target_date.weekday() not in (1, 2):
    target_date += timedelta(days=1)
target_str = target_date.strftime('%Y%m%d')
day_name = target_date.strftime('%A').lower()
print(f"  Target date: {target_str} ({day_name})")

# Get active service_ids
active_services = set()
for _, row in cal_df.iterrows():
    start = row['start_date']
    end = row['end_date']
    if start <= target_str <= end and row.get(day_name, '0') == '1':
        active_services.add(row['service_id'])

# Apply calendar_dates exceptions
if len(cal_dates_df) > 0:
    adds = cal_dates_df[(cal_dates_df['date'] == target_str) & (cal_dates_df['exception_type'] == '1')]
    removes = cal_dates_df[(cal_dates_df['date'] == target_str) & (cal_dates_df['exception_type'] == '2')]
    active_services.update(adds['service_id'].tolist())
    active_services -= set(removes['service_id'].tolist())

print(f"  Active service IDs: {len(active_services)}")

# ── Step 5: Filter routes and trips ──
print("\nSTEP 5: Filtering rail routes and trips...")
routes_df = pd.read_csv(TMP_DIR / 'routes.txt', dtype=str)
print(f"  Total routes: {len(routes_df)}")

# Rail route types: 2 (standard), 100-199 (extended)
routes_df['route_type_int'] = routes_df['route_type'].astype(int)
rail_routes = routes_df[
    (routes_df['route_type_int'] == 2) |
    ((routes_df['route_type_int'] >= 100) & (routes_df['route_type_int'] < 200))
]
print(f"  Rail routes: {len(rail_routes)}")
rail_route_ids = set(rail_routes['route_id'])

# Build route name lookup
route_names = {}
for _, row in rail_routes.iterrows():
    short = row.get('route_short_name', '')
    long_name = row.get('route_long_name', '')
    route_names[row['route_id']] = short if pd.notna(short) and short else (long_name if pd.notna(long_name) else row['route_id'])

# Load trips
trips_df = pd.read_csv(TMP_DIR / 'trips.txt', dtype=str)
print(f"  Total trips: {len(trips_df)}")

# Filter: rail routes, active services
rail_trips = trips_df[
    (trips_df['route_id'].isin(rail_route_ids)) &
    (trips_df['service_id'].isin(active_services))
]
print(f"  Rail trips on {day_name}: {len(rail_trips)}")
trip_to_route = dict(zip(rail_trips['trip_id'], rail_trips['route_id']))
trip_to_direction = dict(zip(rail_trips['trip_id'], rail_trips.get('direction_id', pd.Series(dtype=str))))

# ── Step 6: Extract corridor stop_times ──
print("\nSTEP 6: Reading stop_times (chunked)...")
corridor_stop_ids = set(stop_to_canonical.keys())
rail_trip_ids = set(rail_trips['trip_id'])

corridor_records = []
chunk_count = 0
total_rows = 0

for chunk in pd.read_csv(TMP_DIR / 'stop_times.txt', dtype=str, chunksize=500000):
    chunk_count += 1
    total_rows += len(chunk)

    # Filter: trip_id in rail trips AND stop_id in corridor
    mask = chunk['trip_id'].isin(rail_trip_ids) & chunk['stop_id'].isin(corridor_stop_ids)
    filtered = chunk[mask]

    for _, row in filtered.iterrows():
        corridor_records.append({
            'trip_id': row['trip_id'],
            'stop_id': row['stop_id'],
            'stop_sequence': int(row['stop_sequence']),
            'arrival_time': row['arrival_time'],
            'departure_time': row['departure_time'],
        })

    if chunk_count % 10 == 0:
        print(f"    Chunk {chunk_count}: {total_rows:,} rows read, {len(corridor_records)} corridor records")

print(f"  Total: {total_rows:,} rows in stop_times.txt")
print(f"  Corridor records: {len(corridor_records)}")

# ── Step 7: Filter to trips with ≥2 corridor stops ──
print("\nSTEP 7: Filtering to corridor trips (≥2 stops)...")
trip_stops = defaultdict(list)
for rec in corridor_records:
    trip_stops[rec['trip_id']].append(rec)

corridor_trips = {tid: stops for tid, stops in trip_stops.items() if len(stops) >= 2}
print(f"  Trips with ≥2 corridor stops: {len(corridor_trips)}")

# Sort stops within each trip
for tid in corridor_trips:
    corridor_trips[tid].sort(key=lambda x: x['stop_sequence'])

# ── Step 8: Build output ──
print("\nSTEP 8: Building output CSV...")

def parse_time(t):
    """Parse GTFS time (may be >24:00:00)."""
    parts = str(t).strip().split(':')
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0

def classify_route(route_name):
    """Classify route type from name."""
    rn = str(route_name).upper().strip()
    if rn.startswith('IC ') or rn == 'IC': return 'IC'
    if rn.startswith('IR ') or rn == 'IR': return 'IR'
    if rn.startswith('EC ') or rn == 'EC': return 'EC'
    if rn.startswith('TGV'): return 'TGV'
    if rn.startswith('RE '): return 'RE'
    if rn.startswith('S') and len(rn) <= 4 and rn[1:].strip().isdigit(): return 'S'
    if rn.startswith('R ') or rn == 'R': return 'R'
    return rn[:6]

rows_out = []
for tid, stops in corridor_trips.items():
    route_id = trip_to_route.get(tid, '')
    route_name = route_names.get(route_id, route_id)
    route_type = classify_route(route_name)

    # Determine direction
    first_stop = stop_to_canonical.get(stops[0]['stop_id'], '')
    last_stop = stop_to_canonical.get(stops[-1]['stop_id'], '')
    first_lat = canonical.get(first_stop, {}).get('lat', 0)
    last_lat = canonical.get(last_stop, {}).get('lat', 0)
    first_lon = canonical.get(first_stop, {}).get('lon', 0)
    last_lon = canonical.get(last_stop, {}).get('lon', 0)

    # Geneva is west (lon ~6.14), Villeneuve is east (lon ~6.93)
    if first_lon < last_lon:
        direction = "GE→East"
    elif first_lon > last_lon:
        direction = "East→GE"
    else:
        direction = "Unknown"

    for i, stop in enumerate(stops):
        cname = stop_to_canonical.get(stop['stop_id'], 'Unknown')
        cdata = canonical.get(cname, {})
        arr_sec = parse_time(stop['arrival_time'])
        dep_sec = parse_time(stop['departure_time'])
        dwell = dep_sec - arr_sec if dep_sec >= arr_sec else 0

        rows_out.append({
            'trip_id': tid,
            'route_name': route_name,
            'route_type_detail': route_type,
            'direction': direction,
            'stop_sequence': i + 1,
            'stop_name': cname,
            'stop_id': stop['stop_id'],
            'arrival_time': stop['arrival_time'].strip(),
            'departure_time': stop['departure_time'].strip(),
            'dwell_seconds': dwell,
            'lat_wgs84': cdata.get('lat', ''),
            'lon_wgs84': cdata.get('lon', ''),
        })

out_df = pd.DataFrame(rows_out)
out_df.to_csv(OUT_TRAINS, index=False)
print(f"  Written: {OUT_TRAINS} ({len(out_df)} rows)")

# ── Build stops output ──
print("\nBuilding corridor stops output...")
stops_rows = []
for cname, cdata in canonical.items():
    gtfs_stops = canonical_to_stops.get(cname, [])
    stops_rows.append({
        'stop_name': cname,
        'canonical_name': cname,
        'station_id': cdata['station_id'],
        'lat_wgs84': cdata['lat'],
        'lon_wgs84': cdata['lon'],
        'gtfs_stop_ids': '|'.join(gtfs_stops[:5]),
        'platform_count': len(gtfs_stops),
    })

stops_out = pd.DataFrame(stops_rows)
stops_out.to_csv(OUT_STOPS, index=False)
print(f"  Written: {OUT_STOPS} ({len(stops_out)} rows)")

# ── Step 9: Verification ──
print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

print(f"Total output rows: {len(out_df)}")
print(f"Unique trips: {out_df['trip_id'].nunique()}")
print(f"Unique stations in output: {out_df['stop_name'].nunique()}")

# Direction balance
dir_counts = out_df.groupby('direction')['trip_id'].nunique()
print(f"\nTrips by direction:")
for d, c in dir_counts.items():
    print(f"  {d}: {c}")

# Route type breakdown
type_counts = out_df.groupby('route_type_detail')['trip_id'].nunique()
print(f"\nTrips by type:")
for t, c in type_counts.items():
    print(f"  {t}: {c}")

# First/last trains
first_dep = out_df['departure_time'].apply(lambda x: parse_time(x)).min()
last_dep = out_df['departure_time'].apply(lambda x: parse_time(x)).max()
print(f"\nFirst departure: {first_dep//3600:02d}:{(first_dep%3600)//60:02d}")
print(f"Last departure: {last_dep//3600:02d}:{(last_dep%3600)//60:02d}")

# Lausanne frequency check (07-09)
lausanne_stops = out_df[out_df['stop_name'] == 'Lausanne']
am_peak = lausanne_stops[lausanne_stops['departure_time'].apply(
    lambda x: 7*3600 <= parse_time(x) < 9*3600
)]
ls_trips_am = am_peak['trip_id'].nunique()
ls_tph = ls_trips_am / 2.0  # 2 hour window
print(f"\nLausanne AM peak (07-09): {ls_trips_am} trips ({ls_tph:.1f}/hr, expected ~28)")

# Missing stations
all_output_stations = set(out_df['stop_name'].unique())
missing = [c for c in canonical if c not in all_output_stations]
print(f"\nCanonical stations in output: {len(all_output_stations)}/{len(canonical)}")
if missing:
    print(f"Missing from timetable: {missing}")

# ── Summary ──
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"GTFS source: {GTFS_URL}")
zip_size = zip_path.stat().st_size / 1024 / 1024
print(f"ZIP size: {zip_size:.1f} MB")
print(f"Target date: {target_str} ({day_name})")
print(f"Active services: {len(active_services)}")
print(f"Rail routes in GTFS: {len(rail_routes)}")
print(f"Rail trips on target day: {len(rail_trips)}")
print(f"Corridor trips (≥2 stops): {len(corridor_trips)}")
print(f"Total stop_times rows: {total_rows:,}")
print(f"\nOutput files:")
print(f"  {OUT_TRAINS}: {len(out_df)} rows, {out_df['trip_id'].nunique()} trips")
print(f"  {OUT_STOPS}: {len(stops_out)} rows")
print(f"\nCanonical station matching: {matched}/{len(canonical)}")
if unmatched:
    print(f"  Unmatched: {unmatched}")
print(f"\nShapes.txt: {'Found' if os.path.exists(TMP_DIR / 'shapes.txt') else 'Not found'}")
if os.path.exists(TMP_DIR / 'shapes.txt'):
    shapes_size = os.path.getsize(TMP_DIR / 'shapes.txt') / 1024 / 1024
    print(f"  Size: {shapes_size:.1f} MB (available for corridor geometry extraction)")
