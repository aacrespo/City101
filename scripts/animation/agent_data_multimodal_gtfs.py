#!/usr/bin/env python3
"""
Agent Data: Multimodal GTFS Extraction — City101 Corridor Animation v2

Downloads Swiss GTFS, filters ALL transport modes along the Geneva–Villeneuve
corridor, classifies by mode, and extracts route geometries.

Output:
  output/transport_pulse_v2/gtfs_multimodal_corridor.csv
  output/transport_pulse_v2/route_geometries.geojson
"""

import subprocess, sys, os, csv, math, time, zipfile, json, re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

for pkg in ['pandas']:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

import pandas as pd

BASE = Path('/Users/andreacrespo/CLAUDE/city101')
STATIONS_CSV = BASE / 'datasets/transit/city101_service_frequency_v2.csv'
TMP_DIR = Path('/tmp/city101_gtfs')
OUT_DIR = BASE / 'output/transport_pulse_v2'
OUT_CSV = OUT_DIR / 'gtfs_multimodal_corridor.csv'
OUT_GEO = OUT_DIR / 'route_geometries.geojson'
OUT_STOPS = OUT_DIR / 'gtfs_multimodal_stops.csv'

GTFS_URL = "https://gtfs.geops.ch/dl/gtfs_complete.zip"

# Bounding boxes
BBOX_STANDARD = {'lat': (46.15, 46.55), 'lon': (6.05, 7.10)}  # Rail/metro/tram/funicular/ferry
BBOX_BUS_WIDE = {'lat': (46.05, 46.65), 'lon': (5.90, 7.20)}  # Buses — wider to catch mountain routes

# Mode classification
MODE_MAP = {
    # GTFS route_type → base mode
    0: 'tram', 900: 'tram', 901: 'tram', 902: 'tram',
    1: 'metro', 400: 'metro', 401: 'metro', 402: 'metro',
    2: 'rail', 100: 'rail', 101: 'rail', 102: 'rail', 103: 'rail', 106: 'rail', 109: 'rail',
    3: 'bus', 700: 'bus', 701: 'bus', 702: 'bus', 704: 'bus', 710: 'bus', 712: 'bus', 714: 'bus', 715: 'bus',
    4: 'ferry', 1000: 'ferry', 1200: 'ferry',
    7: 'funicular', 1400: 'funicular',
}

SYMBOL_CODES = {
    'IC': 'ic', 'EC': 'ic', 'TGV': 'ic', 'ICE': 'ic',
    'IR': 'ir',
    'RE': 're',
    'S': 'sbahn',
    'R': 'regional',
}

NARROW_GAUGE_NAMES = {'LEB', 'BAM', 'MOB', 'MVR', 'NStCM', 'TPC', 'AOMC', 'ASD', 'AL'}
LEMAN_EXPRESS_PATTERNS = ['Léman Express', 'CEVA', 'RE L']


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def normalize(s):
    s = str(s).strip()
    for old, new in [('è','e'),('é','e'),('ê','e'),('ë','e'),('à','a'),('â','a'),
                     ('ô','o'),('ö','o'),('ü','u'),('ä','a'),('î','i'),('ï','i')]:
        s = s.replace(old, new)
    return s.lower().strip()


def classify_rail_route(route_name, agency_name=''):
    """Classify a rail route by its name into a symbol code."""
    rn = str(route_name).upper().strip()

    # Check narrow-gauge
    for ng in NARROW_GAUGE_NAMES:
        if ng.upper() in rn or ng.upper() in str(agency_name).upper():
            return 'narrowgauge'

    # Check Léman Express
    for pat in LEMAN_EXPRESS_PATTERNS:
        if pat.upper() in rn:
            return 'lemanexpress'

    if rn.startswith('IC ') or rn == 'IC': return 'ic'
    if rn.startswith('EC ') or rn == 'EC': return 'ic'
    if rn.startswith('TGV') or rn.startswith('ICE'): return 'ic'
    if rn.startswith('IR ') or rn == 'IR': return 'ir'
    if rn.startswith('RE ') or rn == 'RE': return 're'
    if re.match(r'^S\d', rn): return 'sbahn'
    if rn.startswith('R ') or rn == 'R': return 'regional'
    return 'regional'


def classify_bus_route(route_name, stop_times_minutes=None):
    """Classify bus as regular or noctambus."""
    rn = str(route_name).strip()
    # Noctambus: route starts with "N" followed by digit, or service only after midnight
    if re.match(r'^N\d', rn):
        return 'noctambus'
    if stop_times_minutes and all(m >= 60 and m < 300 for m in stop_times_minutes):
        return 'noctambus'
    return 'bus'


def get_symbol_code(base_mode, route_name, agency_name=''):
    """Get the final symbol code for a route."""
    if base_mode == 'rail':
        return classify_rail_route(route_name, agency_name)
    if base_mode == 'bus':
        return classify_bus_route(route_name)
    if base_mode == 'metro':
        return 'metro'
    if base_mode == 'tram':
        return 'tram'
    if base_mode == 'ferry':
        return 'ferry'
    if base_mode == 'funicular':
        return 'funicular'
    return base_mode


# ── Step 1: Load canonical stations ──
print("STEP 1: Loading canonical stations...")
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
needed = ['stops.txt', 'stop_times.txt', 'trips.txt', 'routes.txt',
          'calendar.txt', 'calendar_dates.txt', 'shapes.txt', 'agency.txt']
with zipfile.ZipFile(zip_path, 'r') as zf:
    members = zf.namelist()
    for name in needed:
        if name in members:
            zf.extract(name, TMP_DIR)
            size = os.path.getsize(TMP_DIR / name) / 1024 / 1024
            print(f"    {name}: {size:.1f} MB")
        else:
            print(f"    {name}: NOT FOUND in archive")

# ── Step 3: Load stops with two bounding boxes ──
print("\nSTEP 3: Loading stops...")
stops_df = pd.read_csv(TMP_DIR / 'stops.txt', dtype=str, low_memory=False)
stops_df['stop_lat'] = stops_df['stop_lat'].astype(float)
stops_df['stop_lon'] = stops_df['stop_lon'].astype(float)
print(f"  Total stops in GTFS: {len(stops_df)}")

# Standard bbox (rail/metro/tram/funicular/ferry)
standard_stops = stops_df[
    (stops_df['stop_lat'] >= BBOX_STANDARD['lat'][0]) &
    (stops_df['stop_lat'] <= BBOX_STANDARD['lat'][1]) &
    (stops_df['stop_lon'] >= BBOX_STANDARD['lon'][0]) &
    (stops_df['stop_lon'] <= BBOX_STANDARD['lon'][1])
]
print(f"  Standard bbox: {len(standard_stops)} stops")

# Wide bbox (buses)
wide_stops = stops_df[
    (stops_df['stop_lat'] >= BBOX_BUS_WIDE['lat'][0]) &
    (stops_df['stop_lat'] <= BBOX_BUS_WIDE['lat'][1]) &
    (stops_df['stop_lon'] >= BBOX_BUS_WIDE['lon'][0]) &
    (stops_df['stop_lon'] <= BBOX_BUS_WIDE['lon'][1])
]
print(f"  Wide bbox (buses): {len(wide_stops)} stops")

# Match GTFS stops to canonical stations
stop_to_canonical = {}
canonical_to_stops = defaultdict(list)

for cname, cdata in canonical.items():
    name_matches = standard_stops[standard_stops['stop_name'].apply(normalize) == cdata['name_norm']]
    if len(name_matches) > 0:
        for _, stop in name_matches.iterrows():
            stop_to_canonical[stop['stop_id']] = cname
            canonical_to_stops[cname].append(stop['stop_id'])
        continue

    cname_base = normalize(cname).split(',')[0].split('(')[0].strip()
    if len(cname_base) > 3:
        partial = standard_stops[standard_stops['stop_name'].apply(lambda x: cname_base in normalize(x))]
        if len(partial) > 0:
            for _, stop in partial.iterrows():
                stop_to_canonical[stop['stop_id']] = cname
                canonical_to_stops[cname].append(stop['stop_id'])
            continue

    best_dist = float('inf')
    best_stops = []
    for _, stop in standard_stops.iterrows():
        d = haversine_m(cdata['lat'], cdata['lon'], stop['stop_lat'], stop['stop_lon'])
        if d < 1000 and d < best_dist + 200:
            if d < best_dist:
                best_dist = d
                best_stops = [(stop['stop_id'], d)]
            else:
                best_stops.append((stop['stop_id'], d))
    if best_stops:
        for sid, d in best_stops:
            stop_to_canonical[sid] = cname
            canonical_to_stops[cname].append(sid)

# Parent station expansion
if 'parent_station' in stops_df.columns:
    parent_map = {}
    for sid, cname in list(stop_to_canonical.items()):
        parent_map[sid] = cname
    for _, stop in standard_stops.iterrows():
        parent = stop.get('parent_station', '')
        if pd.notna(parent) and parent in parent_map and stop['stop_id'] not in stop_to_canonical:
            stop_to_canonical[stop['stop_id']] = parent_map[parent]
            canonical_to_stops[parent_map[parent]].append(stop['stop_id'])

matched = len(canonical_to_stops)
unmatched = [c for c in canonical if c not in canonical_to_stops]
print(f"  Matched: {matched}/{len(canonical)} canonical stations")
if unmatched:
    print(f"  Unmatched: {unmatched[:10]}")

# Build set of GTFS stops near canonical stations (for bus corridor classification)
# Any stop within 1km of a canonical station = "corridor stop"
corridor_stop_ids = set(stop_to_canonical.keys())
canonical_coords = [(c['lat'], c['lon']) for c in canonical.values()]

# For bus route classification: find all wide-bbox stops within 3km of canonical stations
stops_near_canonical = set()
print("  Finding stops near canonical stations (3km radius)...")
for _, stop in wide_stops.iterrows():
    for clat, clon in canonical_coords:
        if haversine_m(clat, clon, stop['stop_lat'], stop['stop_lon']) < 3000:
            stops_near_canonical.add(stop['stop_id'])
            break
print(f"  Stops within 3km of canonical: {len(stops_near_canonical)}")

# ── Step 4: Find representative weekday ──
print("\nSTEP 4: Finding representative weekday...")
cal_df = pd.read_csv(TMP_DIR / 'calendar.txt', dtype=str)
cal_dates_path = TMP_DIR / 'calendar_dates.txt'
cal_dates_df = pd.read_csv(cal_dates_path, dtype=str) if os.path.exists(cal_dates_path) else pd.DataFrame()

today = datetime.now()
target_date = today
while target_date.weekday() not in (1, 2):
    target_date += timedelta(days=1)
target_str = target_date.strftime('%Y%m%d')
day_name = target_date.strftime('%A').lower()
print(f"  Target date: {target_str} ({day_name})")

active_services = set()
for _, row in cal_df.iterrows():
    start = row['start_date']
    end = row['end_date']
    if start <= target_str <= end and row.get(day_name, '0') == '1':
        active_services.add(row['service_id'])

if len(cal_dates_df) > 0:
    adds = cal_dates_df[(cal_dates_df['date'] == target_str) & (cal_dates_df['exception_type'] == '1')]
    removes = cal_dates_df[(cal_dates_df['date'] == target_str) & (cal_dates_df['exception_type'] == '2')]
    active_services.update(adds['service_id'].tolist())
    active_services -= set(removes['service_id'].tolist())

print(f"  Active service IDs: {len(active_services)}")

# ── Step 5: Load ALL routes and classify by mode ──
print("\nSTEP 5: Loading routes and classifying modes...")
routes_df = pd.read_csv(TMP_DIR / 'routes.txt', dtype=str)
routes_df['route_type_int'] = routes_df['route_type'].astype(int)
print(f"  Total routes: {len(routes_df)}")

# Load agency info if available
agency_map = {}
agency_path = TMP_DIR / 'agency.txt'
if os.path.exists(agency_path):
    agency_df = pd.read_csv(agency_path, dtype=str)
    for _, row in agency_df.iterrows():
        agency_map[row['agency_id']] = row.get('agency_name', '')

# Classify each route
route_info = {}
mode_counts = defaultdict(int)

for _, row in routes_df.iterrows():
    rt = row['route_type_int']
    base_mode = MODE_MAP.get(rt, None)
    if base_mode is None:
        # Try extended ranges
        if 100 <= rt < 200: base_mode = 'rail'
        elif 200 <= rt < 300: base_mode = 'bus'  # coach
        elif 400 <= rt < 500: base_mode = 'metro'
        elif 700 <= rt < 800: base_mode = 'bus'
        elif 900 <= rt < 1000: base_mode = 'tram'
        elif 1000 <= rt < 1100: base_mode = 'ferry'
        elif 1400 <= rt < 1500: base_mode = 'funicular'
        else:
            continue  # skip unknown types

    short = row.get('route_short_name', '')
    long_name = row.get('route_long_name', '')
    route_name = short if pd.notna(short) and short else (long_name if pd.notna(long_name) else row['route_id'])
    agency_id = row.get('agency_id', '')
    agency_name = agency_map.get(agency_id, '') if pd.notna(agency_id) else ''

    symbol = get_symbol_code(base_mode, route_name, agency_name)

    route_info[row['route_id']] = {
        'route_name': route_name,
        'base_mode': base_mode,
        'symbol_code': symbol,
        'route_type': rt,
        'agency_name': agency_name,
        'shape_id': None,  # filled from trips
    }
    mode_counts[base_mode] += 1

print("  Routes by mode:")
for mode, count in sorted(mode_counts.items()):
    print(f"    {mode}: {count}")

# ── Step 6: Filter trips ──
print("\nSTEP 6: Loading and filtering trips...")
trips_df = pd.read_csv(TMP_DIR / 'trips.txt', dtype=str)
print(f"  Total trips: {len(trips_df)}")

# Filter to known routes and active services
valid_route_ids = set(route_info.keys())
active_trips = trips_df[
    (trips_df['route_id'].isin(valid_route_ids)) &
    (trips_df['service_id'].isin(active_services))
]
print(f"  Active trips with known routes: {len(active_trips)}")

trip_to_route = dict(zip(active_trips['trip_id'], active_trips['route_id']))
trip_to_direction = {}
if 'direction_id' in active_trips.columns:
    trip_to_direction = dict(zip(active_trips['trip_id'], active_trips['direction_id']))
trip_to_shape = {}
if 'shape_id' in active_trips.columns:
    trip_to_shape = dict(zip(active_trips['trip_id'], active_trips['shape_id']))

# ── Step 7: Read stop_times (chunked) and filter to corridor ──
print("\nSTEP 7: Reading stop_times (chunked)...")
active_trip_ids = set(active_trips['trip_id'])

# We need ALL stop_ids in both bounding boxes
all_bbox_stop_ids = set(wide_stops['stop_id'])

corridor_records = []
chunk_count = 0
total_rows = 0
trip_stop_ids_all = defaultdict(set)  # track which stops each trip visits

for chunk in pd.read_csv(TMP_DIR / 'stop_times.txt', dtype=str, chunksize=500000):
    chunk_count += 1
    total_rows += len(chunk)

    mask = chunk['trip_id'].isin(active_trip_ids) & chunk['stop_id'].isin(all_bbox_stop_ids)
    filtered = chunk[mask]

    for _, row in filtered.iterrows():
        tid = row['trip_id']
        sid = row['stop_id']
        trip_stop_ids_all[tid].add(sid)
        corridor_records.append({
            'trip_id': tid,
            'stop_id': sid,
            'stop_sequence': int(row['stop_sequence']),
            'arrival_time': row['arrival_time'],
            'departure_time': row['departure_time'],
        })

    if chunk_count % 10 == 0:
        print(f"    Chunk {chunk_count}: {total_rows:,} rows read, {len(corridor_records)} records")

print(f"  Total: {total_rows:,} rows in stop_times.txt")
print(f"  Records in bounding boxes: {len(corridor_records)}")

# ── Step 8: Filter to trips with ≥2 stops in relevant bbox ──
print("\nSTEP 8: Filtering trips by mode and corridor relevance...")

# Group records by trip
trip_stops = defaultdict(list)
for rec in corridor_records:
    trip_stops[rec['trip_id']].append(rec)

# Classify trips
corridor_trips = {}
bus_corridor_trips = {}
bus_regional_trips = {}
mode_trip_counts = defaultdict(int)

for tid, stops in trip_stops.items():
    if len(stops) < 2:
        continue

    route_id = trip_to_route.get(tid, '')
    info = route_info.get(route_id, None)
    if info is None:
        continue

    base_mode = info['base_mode']
    stop_ids_in_trip = {s['stop_id'] for s in stops}

    if base_mode == 'bus':
        # Bus classification: corridor vs regional
        # Corridor bus: ≥2 stops within 1km of canonical station
        near_canonical = stop_ids_in_trip & stops_near_canonical
        if len(near_canonical) >= 2:
            bus_corridor_trips[tid] = stops
            info_copy = dict(info)
            info_copy['bus_layer'] = 'corridor'
            corridor_trips[tid] = stops
            mode_trip_counts['bus_corridor'] += 1
        else:
            bus_regional_trips[tid] = stops
            corridor_trips[tid] = stops
            mode_trip_counts['bus_regional'] += 1
    else:
        # Non-bus: need ≥2 stops in standard bbox
        std_bbox_stops = set()
        for s in stops:
            row_stop = stops_df[stops_df['stop_id'] == s['stop_id']]
            if len(row_stop) > 0:
                lat = row_stop.iloc[0]['stop_lat']
                lon = row_stop.iloc[0]['stop_lon']
                if (BBOX_STANDARD['lat'][0] <= lat <= BBOX_STANDARD['lat'][1] and
                    BBOX_STANDARD['lon'][0] <= lon <= BBOX_STANDARD['lon'][1]):
                    std_bbox_stops.add(s['stop_id'])
        if len(std_bbox_stops) >= 2:
            corridor_trips[tid] = stops
            mode_trip_counts[base_mode] += 1

print(f"  Total corridor trips: {len(corridor_trips)}")
print("  Trips by mode:")
for mode, count in sorted(mode_trip_counts.items()):
    print(f"    {mode}: {count}")

# Sort stops within each trip
for tid in corridor_trips:
    corridor_trips[tid].sort(key=lambda x: x['stop_sequence'])

# ── Step 9: Build stop coordinate lookup ──
print("\nSTEP 9: Building stop coordinate lookup...")
stop_coords = {}
for _, stop in stops_df.iterrows():
    stop_coords[stop['stop_id']] = (stop['stop_lat'], stop['stop_lon'])

# ── Step 10: Build output CSV ──
print("\nSTEP 10: Building output CSV...")

def parse_time(t):
    parts = str(t).strip().split(':')
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0

rows_out = []
for tid, stops in corridor_trips.items():
    route_id = trip_to_route.get(tid, '')
    info = route_info.get(route_id, {})
    route_name = info.get('route_name', route_id)
    base_mode = info.get('base_mode', 'unknown')
    symbol_code = info.get('symbol_code', base_mode)

    # Re-check noctambus classification using actual stop times
    if base_mode == 'bus':
        stop_minutes = []
        for s in stops:
            sec = parse_time(s['departure_time'])
            stop_minutes.append(sec / 60)
        if all(60 <= m < 300 for m in stop_minutes):
            symbol_code = 'noctambus'
        bus_layer = 'corridor' if tid in bus_corridor_trips else 'regional'
    else:
        bus_layer = ''

    # Direction from first/last stop coords
    first_coords = stop_coords.get(stops[0]['stop_id'], (0, 0))
    last_coords = stop_coords.get(stops[-1]['stop_id'], (0, 0))
    if first_coords[1] < last_coords[1]:
        direction = "GE→East"
    elif first_coords[1] > last_coords[1]:
        direction = "East→GE"
    else:
        direction = "Unknown"

    for i, stop in enumerate(stops):
        coords = stop_coords.get(stop['stop_id'], (0, 0))
        # Try to get canonical name
        cname = stop_to_canonical.get(stop['stop_id'], '')
        if not cname:
            # Use GTFS stop name
            name_row = stops_df[stops_df['stop_id'] == stop['stop_id']]
            cname = name_row.iloc[0]['stop_name'] if len(name_row) > 0 else stop['stop_id']

        rows_out.append({
            'trip_id': tid,
            'route_name': route_name,
            'mode_label': base_mode,
            'symbol_code': symbol_code,
            'bus_layer': bus_layer,
            'direction': direction,
            'stop_sequence': i + 1,
            'stop_name': cname,
            'stop_id': stop['stop_id'],
            'arrival_time': stop['arrival_time'].strip(),
            'departure_time': stop['departure_time'].strip(),
            'lat_wgs84': coords[0],
            'lon_wgs84': coords[1],
        })

out_df = pd.DataFrame(rows_out)
out_df.to_csv(OUT_CSV, index=False)
print(f"  Written: {OUT_CSV} ({len(out_df)} rows, {out_df['trip_id'].nunique()} trips)")

# ── Step 11: Extract route geometries from shapes.txt ──
print("\nSTEP 11: Extracting route geometries...")
shapes_path = TMP_DIR / 'shapes.txt'
features = []

if os.path.exists(shapes_path):
    # Collect shape_ids used by corridor trips
    corridor_shape_ids = set()
    for tid in corridor_trips:
        sid = trip_to_shape.get(tid, '')
        if pd.notna(sid) and sid:
            corridor_shape_ids.add(sid)
    print(f"  Unique shape_ids in corridor trips: {len(corridor_shape_ids)}")

    if corridor_shape_ids:
        # Read shapes.txt — can be very large, read chunked
        shape_points = defaultdict(list)
        for chunk in pd.read_csv(shapes_path, dtype=str, chunksize=500000):
            chunk_filtered = chunk[chunk['shape_id'].isin(corridor_shape_ids)]
            for _, row in chunk_filtered.iterrows():
                shape_points[row['shape_id']].append({
                    'seq': int(row['shape_pt_sequence']),
                    'lat': float(row['shape_pt_lat']),
                    'lon': float(row['shape_pt_lon']),
                })

        print(f"  Loaded {len(shape_points)} shapes")

        # Map shape_id to route info (use first trip that uses this shape)
        shape_to_route = {}
        for tid in corridor_trips:
            sid = trip_to_shape.get(tid, '')
            if sid and sid not in shape_to_route:
                route_id = trip_to_route.get(tid, '')
                shape_to_route[sid] = route_info.get(route_id, {})

        for shape_id, points in shape_points.items():
            points.sort(key=lambda p: p['seq'])
            coords = [[p['lon'], p['lat']] for p in points]
            if len(coords) < 2:
                continue

            rinfo = shape_to_route.get(shape_id, {})
            features.append({
                'type': 'Feature',
                'properties': {
                    'shape_id': shape_id,
                    'mode': rinfo.get('base_mode', 'unknown'),
                    'symbol_code': rinfo.get('symbol_code', 'unknown'),
                    'route_name': rinfo.get('route_name', ''),
                },
                'geometry': {
                    'type': 'LineString',
                    'coordinates': coords,
                }
            })
else:
    print("  shapes.txt not found — skipping geometry extraction")

geojson = {
    'type': 'FeatureCollection',
    'features': features,
}
with open(OUT_GEO, 'w') as f:
    json.dump(geojson, f, separators=(',', ':'))
geo_size = os.path.getsize(OUT_GEO) / 1024 / 1024
print(f"  Written: {OUT_GEO} ({len(features)} features, {geo_size:.1f} MB)")

# ── Step 12: Build stops output ──
print("\nSTEP 12: Building stops output...")
stops_rows = []
for cname, cdata in canonical.items():
    gtfs_stops = canonical_to_stops.get(cname, [])
    stops_rows.append({
        'stop_name': cname,
        'lat_wgs84': cdata['lat'],
        'lon_wgs84': cdata['lon'],
        'station_id': cdata['station_id'],
        'gtfs_stop_ids': '|'.join(gtfs_stops[:5]),
    })

# Also add non-canonical stops that appear in corridor trips (bus stops, etc.)
seen_names = {s['stop_name'] for s in stops_rows}
for _, row in out_df.drop_duplicates('stop_id').iterrows():
    if row['stop_name'] not in seen_names:
        stops_rows.append({
            'stop_name': row['stop_name'],
            'lat_wgs84': row['lat_wgs84'],
            'lon_wgs84': row['lon_wgs84'],
            'station_id': '',
            'gtfs_stop_ids': row['stop_id'],
        })
        seen_names.add(row['stop_name'])

stops_out = pd.DataFrame(stops_rows)
stops_out.to_csv(OUT_STOPS, index=False)
print(f"  Written: {OUT_STOPS} ({len(stops_out)} rows)")

# ── Verification ──
print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

print(f"Total output rows: {len(out_df)}")
print(f"Unique trips: {out_df['trip_id'].nunique()}")

# Mode breakdown
print(f"\nTrips by symbol_code:")
for sc, count in out_df.groupby('symbol_code')['trip_id'].nunique().sort_values(ascending=False).items():
    print(f"  {sc}: {count}")

print(f"\nTrips by mode_label:")
for ml, count in out_df.groupby('mode_label')['trip_id'].nunique().sort_values(ascending=False).items():
    print(f"  {ml}: {count}")

# Bus layers
if 'bus_layer' in out_df.columns:
    bus_df = out_df[out_df['mode_label'] == 'bus']
    if len(bus_df) > 0:
        print(f"\nBus layer breakdown:")
        for layer, count in bus_df.groupby('bus_layer')['trip_id'].nunique().items():
            print(f"  {layer}: {count} trips")

# Direction balance
dir_counts = out_df.groupby('direction')['trip_id'].nunique()
print(f"\nTrips by direction:")
for d, c in dir_counts.items():
    print(f"  {d}: {c}")

# Coordinate ranges
print(f"\nCoordinate ranges:")
print(f"  Lat: [{out_df['lat_wgs84'].min():.4f}, {out_df['lat_wgs84'].max():.4f}]")
print(f"  Lon: [{out_df['lon_wgs84'].min():.4f}, {out_df['lon_wgs84'].max():.4f}]")

# Time range
first_dep = out_df['departure_time'].apply(lambda x: parse_time(x)).min()
last_dep = out_df['departure_time'].apply(lambda x: parse_time(x)).max()
print(f"\nFirst departure: {first_dep//3600:02d}:{(first_dep%3600)//60:02d}")
print(f"Last departure: {last_dep//3600:02d}:{(last_dep%3600)//60:02d}")

print(f"\nOutput files:")
print(f"  {OUT_CSV}: {len(out_df)} rows, {out_df['trip_id'].nunique()} trips")
print(f"  {OUT_GEO}: {len(features)} route shapes")
print(f"  {OUT_STOPS}: {len(stops_out)} stops")
print("\nDone.")
