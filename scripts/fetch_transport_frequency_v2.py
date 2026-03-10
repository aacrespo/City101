#!/usr/bin/env python3
"""
SCRIPT 2 v2: Transport API → City101 Service Frequency Profile
=============================================================
Queries transport.opendata.ch stationboard for each corridor station.
Measures trains per hour during a typical workday morning (7-9am).
This gives SERVICE FREQUENCY — different from ridership:
  - Ridership = how many people use it (Passagierfrequenz)
  - Frequency = how often trains come (promise of mobility)

v2 changes vs v1:
  - Uses limit=200 per API call (v1 used limit=30 which capped results)
  - Filters departures by actual timestamp to the 07:00-09:00 window
  - Single API call per station instead of two (7am + 8am)
  - Dropped capacity/occupancy columns (stationboard endpoint never returns them)
  - Avg wait time (minutes between departures) added

Note on capacity: transport.opendata.ch/v1/stationboard includes capacity1st
and capacity2nd fields in its schema but always returns None. The /v1/connections
endpoint can return capacity for specific journeys, but querying all station
pairs would be prohibitively slow. Capacity data omitted for now.

For "working continuity" narrative: frequency matters more than ridership.
Can I reliably catch a train every 15 min, or am I stuck waiting 45?

Run locally: python3 fetch_transport_frequency_v2.py
Output: city101_service_frequency_v2.csv

Source: transport.opendata.ch/v1/stationboard
Rate limit: Be gentle — 0.5s between calls, this is an unofficial API.
"""
import csv
import json
import urllib.request
import urllib.parse
import ssl
import time
import os
from datetime import datetime, timedelta

# === CONFIG ===
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(OUTPUT_DIR, 'city101_service_frequency_v2.csv')
API_BASE = 'https://transport.opendata.ch/v1'
DELAY_BETWEEN_CALLS = 0.5  # seconds
STATIONBOARD_LIMIT = 200   # API allows up to ~300; 200 is safe and covers 7+ hours

# Corridor stations: CFF main line + key regional stops
# (name, approx_lat, approx_lon) — name must match SBB/transport API naming
CORRIDOR_STATIONS = [
    # Geneva cluster
    ("Genève", 46.2100, 6.1422),
    ("Genève-Sécheron", 46.2264, 6.1444),
    ("Genève-Aéroport", 46.2310, 6.1095),
    ("Genève-Eaux-Vives", 46.2014, 6.1666),
    ("Genève-Champel", 46.1922, 6.1535),
    ("Lancy-Bachet", 46.1743, 6.1294),
    ("Lancy-Pont-Rouge", 46.1859, 6.1249),
    ("Genthod-Bellevue", 46.2567, 6.1540),
    ("Vernier", 46.2207, 6.0939),
    # Lac Léman north shore — Geneva to Lausanne
    ("Versoix", 46.2840, 6.1630),
    ("Coppet", 46.3128, 6.1914),
    ("Tannay", 46.3076, 6.1811),
    ("Mies", 46.3016, 6.1707),
    ("Founex", 46.3390, 6.2080),
    ("Nyon", 46.3832, 6.2399),
    ("Prangins", 46.3955, 6.2510),
    ("Gland", 46.4200, 6.2691),
    ("Begnins", 46.4430, 6.2620),
    ("Rolle", 46.4594, 6.3371),
    ("Perroy", 46.4667, 6.3617),
    ("Allaman", 46.4758, 6.3997),
    ("Aubonne", 46.4910, 6.3896),
    ("Saint-Prex", 46.4822, 6.4528),
    ("Morges", 46.5114, 6.4987),
    ("Lonay-Préverenges", 46.5231, 6.5195),
    ("Denges-Echandens", 46.5240, 6.5490),
    ("Bussigny", 46.5508, 6.5518),
    ("Renens VD", 46.5375, 6.5911),
    ("Prilly-Malley", 46.5267, 6.6026),
    # Lausanne cluster
    ("Lausanne", 46.5168, 6.6291),
    ("Lausanne-Flon", 46.5215, 6.6260),
    # East of Lausanne
    ("La Conversion", 46.5131, 6.6783),
    ("Bossière", 46.5097, 6.6993),
    ("Grandvaux", 46.5043, 6.7050),
    ("Cully", 46.4886, 6.7272),
    ("Épesses", 46.4870, 6.7400),
    ("Rivaz", 46.4760, 6.7550),
    ("Saint-Saphorin", 46.4726, 6.7970),
    ("Vevey", 46.4611, 6.8434),
    ("La Tour-de-Peilz", 46.4529, 6.8608),
    ("Burier", 46.4479, 6.8771),
    ("Clarens", 46.4427, 6.8958),
    ("Montreux", 46.4340, 6.9103),
    ("Territet", 46.4280, 6.9280),
    ("Villeneuve", 46.3980, 6.9280),
    # Beyond corridor but useful for comparison
    ("Aigle", 46.3188, 6.9640),
    ("Bex", 46.2515, 7.0007),
    # Key junction stations
    ("Palézieux", 46.5428, 6.8379),
    ("Puidoux", 46.4938, 6.7657),
]


def fetch_json(url, max_retries=3):
    """Fetch JSON with retries."""
    ctx = ssl.create_default_context()
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'EPFL-Studio-Research/1.0'})
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))
            else:
                raise e


def find_station(name):
    """Look up a station by name via the locations API."""
    params = urllib.parse.urlencode({'query': name, 'type': 'station'})
    url = f"{API_BASE}/locations?{params}"
    data = fetch_json(url)
    stations = data.get('stations', [])
    if stations:
        return stations[0]  # Best match
    return None


def get_stationboard(station_id, datetime_str=None, limit=200):
    """Get departures from a station."""
    params = {
        'station': station_id,
        'limit': str(limit),
    }
    if datetime_str:
        params['datetime'] = datetime_str

    url = f"{API_BASE}/stationboard?" + urllib.parse.urlencode(params)
    return fetch_json(url)


def filter_departures_in_window(stationboard_data, hour_start=7, hour_end=9):
    """Filter departures to those within the specified hour window [start, end).

    Returns only entries whose departure time falls within the window.
    This gives real frequency instead of the API limit count.
    """
    entries = stationboard_data.get('stationboard', [])
    filtered = []

    for entry in entries:
        dep_str = entry.get('stop', {}).get('departure', '')
        if not dep_str:
            continue
        try:
            dt = datetime.fromisoformat(dep_str)
            if hour_start <= dt.hour < hour_end:
                filtered.append(entry)
        except (ValueError, TypeError):
            continue

    return filtered


def analyze_departures(entries):
    """Analyze a list of departure entries."""
    categories = {}
    operators = set()
    destinations = set()

    for entry in entries:
        cat = entry.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
        op = entry.get('operator', '')
        if op:
            operators.add(op)
        to = entry.get('to', '')
        if to:
            destinations.add(to)

    return {
        'total_departures': len(entries),
        'categories': categories,
        'operators': operators,
        'destinations': destinations,
    }


def compute_avg_wait(entries):
    """Compute average minutes between consecutive departures."""
    dep_times = []
    for entry in entries:
        dep_str = entry.get('stop', {}).get('departure', '')
        if dep_str:
            try:
                dep_times.append(datetime.fromisoformat(dep_str))
            except (ValueError, TypeError):
                continue

    if len(dep_times) < 2:
        return None

    dep_times.sort()
    gaps = [(dep_times[i+1] - dep_times[i]).total_seconds() / 60.0
            for i in range(len(dep_times) - 1)]
    return round(sum(gaps) / len(gaps), 1)


def main():
    print("City101 Service Frequency Profile v2")
    print("=" * 70)

    # Use next Monday 7:00 AM as reference time for consistent workday query
    now = datetime.now()
    days_ahead = (0 - now.weekday()) % 7  # 0 = Monday
    if days_ahead == 0 and now.hour >= 12:
        days_ahead = 7
    next_monday = now + timedelta(days=days_ahead)
    ref_time_7am = next_monday.replace(hour=7, minute=0, second=0, microsecond=0)
    ref_time_str = ref_time_7am.strftime('%Y-%m-%d %H:%M')

    print(f"Reference window: {ref_time_7am.strftime('%Y-%m-%d')} 07:00–09:00")
    print(f"API limit per call: {STATIONBOARD_LIMIT}")
    print(f"Querying {len(CORRIDOR_STATIONS)} stations...\n")

    results = []
    errors = []

    for i, (name, approx_lat, approx_lon) in enumerate(CORRIDOR_STATIONS):
        print(f"  [{i+1}/{len(CORRIDOR_STATIONS)}] {name}...", end=' ', flush=True)

        try:
            # Step 1: Find station ID
            station = find_station(name)
            time.sleep(DELAY_BETWEEN_CALLS)

            if not station:
                print("NOT FOUND")
                errors.append((name, "Station not found"))
                continue

            station_name = station.get('name', name)
            station_id = station.get('id', '')
            coord = station.get('coordinate', {})
            lat = coord.get('x', approx_lat)  # Note: API uses x=lat, y=lon
            lon = coord.get('y', approx_lon)

            # Step 2: Single call with limit=200 starting at 7am
            sb_data = get_stationboard(station_name, ref_time_str, limit=STATIONBOARD_LIMIT)
            time.sleep(DELAY_BETWEEN_CALLS)

            # Step 3: Filter to 07:00-09:00 window by actual departure timestamps
            window_entries = filter_departures_in_window(sb_data, hour_start=7, hour_end=9)
            info = analyze_departures(window_entries)

            total_deps = info['total_departures']
            trains_per_hour = round(total_deps / 2, 1)  # 2-hour window
            avg_wait = compute_avg_wait(window_entries)

            # Breakdown by type
            cats = info['categories']
            ic_ir = sum(v for k, v in cats.items() if k in ('IC', 'IR', 'ICE', 'TGV', 'EC'))
            regional = sum(v for k, v in cats.items() if k in ('S', 'RE', 'R', 'RER'))
            metro_tram = sum(v for k, v in cats.items() if k in ('M', 'T'))
            other = total_deps - ic_ir - regional - metro_tram

            result = {
                'name': station_name,
                'station_id': station_id,
                'lat_wgs84': lat,
                'lon_wgs84': lon,
                'departures_7to9': total_deps,
                'trains_per_hour': trains_per_hour,
                'avg_wait_minutes': avg_wait,
                'ic_ir_departures': ic_ir,
                'regional_departures': regional,
                'metro_tram_departures': metro_tram,
                'other_departures': other,
                'category_breakdown': '; '.join(f"{k}:{v}" for k, v in sorted(cats.items())),
                'operators': '; '.join(sorted(info['operators'])),
                'sample_destinations': '; '.join(sorted(list(info['destinations'])[:10])),
                'query_date': ref_time_str,
            }
            results.append(result)

            wait_str = f", avg wait {avg_wait} min" if avg_wait is not None else ""
            print(f"{trains_per_hour} trains/hr ({ic_ir} IC/IR, {regional} regional{wait_str})")

        except Exception as e:
            print(f"ERROR: {e}")
            errors.append((name, str(e)))

    # Sort by frequency
    results.sort(key=lambda x: x['trains_per_hour'], reverse=True)

    # Write CSV
    if results:
        fields = list(results[0].keys())
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for r in results:
                writer.writerow(r)

    # === SUMMARY ===
    print(f"\n{'='*70}")
    print(f"SERVICE FREQUENCY PROFILE v2 — City101 Corridor")
    print(f"{'='*70}")
    print(f"Stations queried: {len(CORRIDOR_STATIONS)}")
    print(f"Stations found: {len(results)}")
    print(f"Errors: {len(errors)}")

    if results:
        print(f"\nFrequency ranking (trains/hour, workday 07:00–09:00):")
        print(f"{'Station':<35} {'Trains/hr':>10} {'Deps(2h)':>9} {'AvgWait':>8} {'IC/IR':>6} {'Regional':>9} {'Metro':>6}")
        print("-" * 95)
        for r in results:
            w = f"{r['avg_wait_minutes']:.0f}m" if r['avg_wait_minutes'] is not None else "-"
            print(f"{r['name']:<35} {r['trains_per_hour']:>10} {r['departures_7to9']:>9} {w:>8} {r['ic_ir_departures']:>6} {r['regional_departures']:>9} {r['metro_tram_departures']:>6}")

    if errors:
        print(f"\nErrors:")
        for name, err in errors:
            print(f"  {name}: {err}")

    print(f"\nOutput: {OUTPUT_CSV}")

    # Narrative insight
    if results:
        max_freq = results[0]
        min_freq = results[-1]
        # Find lowest non-zero
        min_nonzero = next((r for r in reversed(results) if r['trains_per_hour'] > 0), None)
        print(f"\n--- NARRATIVE INSIGHT ---")
        print(f"Highest frequency: {max_freq['name']} ({max_freq['trains_per_hour']} trains/hr)")
        print(f"Lowest frequency: {min_freq['name']} ({min_freq['trains_per_hour']} trains/hr)")
        if min_nonzero and min_nonzero['trains_per_hour'] > 0:
            ratio = max_freq['trains_per_hour'] / min_nonzero['trains_per_hour']
            print(f"Frequency ratio (excl. zero): {ratio:.1f}x ({max_freq['name']} vs {min_nonzero['name']})")
        print(f"The 'promise of mobility' varies dramatically along the corridor.")
        print(f"High-frequency nodes = reliable working continuity.")
        print(f"Low-frequency gaps = forced dwell time, need infrastructure.")

    # Note on capacity
    print(f"\n--- NOTE ON CAPACITY DATA ---")
    print(f"Capacity/occupancy columns dropped in v2.")
    print(f"The stationboard endpoint returns capacity1st/capacity2nd fields")
    print(f"but they are always None. The /v1/connections endpoint can return")
    print(f"capacity for specific journeys, but querying all station pairs")
    print(f"would be prohibitively slow ({len(CORRIDOR_STATIONS)}^2 = {len(CORRIDOR_STATIONS)**2} queries).")

    print(f"{'='*70}")


if __name__ == '__main__':
    main()
