#!/usr/bin/env python3
"""
SCRIPT 2: Transport API → City101 Service Frequency Profile
=============================================================
Queries transport.opendata.ch stationboard for each corridor station.
Measures trains per hour during a typical workday morning (7-9am).
This gives SERVICE FREQUENCY — different from ridership:
  - Ridership = how many people use it (Passagierfrequenz)
  - Frequency = how often trains come (promise of mobility)

Also captures CAPACITY/OCCUPANCY data when available:
  - capacity1st / capacity2nd: 0=low, 1=medium, 2=high occupancy
  - Inverted into "workability" score: 2=empty (great for laptops), 0=packed
  - Coverage varies — not all departures report capacity

For "working continuity" narrative: frequency matters more than ridership.
Can I reliably catch a train every 15 min, or am I stuck waiting 45?
And when I'm on it — can I actually open my laptop?

Run locally: python3 fetch_transport_frequency.py
Output: city101_service_frequency.csv

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
OUTPUT_CSV = os.path.join(OUTPUT_DIR, 'city101_service_frequency.csv')
API_BASE = 'https://transport.opendata.ch/v1'
DELAY_BETWEEN_CALLS = 0.5  # seconds

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
            with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
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


def get_stationboard(station_id, datetime_str=None, limit=30):
    """Get departures from a station."""
    params = {
        'station': station_id,
        'limit': str(limit),
    }
    if datetime_str:
        params['datetime'] = datetime_str
    
    url = f"{API_BASE}/stationboard?" + urllib.parse.urlencode(params)
    return fetch_json(url)


def count_trains_in_window(stationboard_data, window_minutes=120):
    """Count unique train departures in a time window, including capacity."""
    entries = stationboard_data.get('stationboard', [])
    
    categories = {}  # category -> count
    operators = set()
    destinations = set()
    
    # Capacity tracking: 0=low occupancy, 1=medium, 2=high
    # Not all departures report capacity — track how many do
    cap1_values = []  # 1st class capacity scores
    cap2_values = []  # 2nd class capacity scores
    
    for entry in entries:
        cat = entry.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
        op = entry.get('operator', '')
        if op:
            operators.add(op)
        to = entry.get('to', '')
        if to:
            destinations.add(to)
        
        # Capacity data (when available)
        cap1 = entry.get('capacity1st')
        cap2 = entry.get('capacity2nd')
        if cap1 is not None:
            try:
                cap1_values.append(int(cap1))
            except (ValueError, TypeError):
                pass
        if cap2 is not None:
            try:
                cap2_values.append(int(cap2))
            except (ValueError, TypeError):
                pass
    
    return {
        'total_departures': len(entries),
        'categories': categories,
        'operators': operators,
        'destinations': destinations,
        'cap1_values': cap1_values,
        'cap2_values': cap2_values,
    }


def main():
    print("City101 Service Frequency Profile")
    print("=" * 70)
    
    # Use next Monday 7:00 AM as reference time for consistent workday query
    # (the API uses the current time if not specified, but we want workday morning)
    now = datetime.now()
    # Find next Monday
    days_ahead = (0 - now.weekday()) % 7  # 0 = Monday
    if days_ahead == 0 and now.hour >= 12:
        days_ahead = 7
    next_monday = now + timedelta(days=days_ahead)
    ref_time_7am = next_monday.replace(hour=7, minute=0, second=0, microsecond=0)
    ref_time_8am = next_monday.replace(hour=8, minute=0, second=0, microsecond=0)
    ref_time_str_7 = ref_time_7am.strftime('%Y-%m-%d %H:%M')
    ref_time_str_8 = ref_time_8am.strftime('%Y-%m-%d %H:%M')
    
    print(f"Reference times: {ref_time_str_7} and {ref_time_str_8}")
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
            
            # Step 2: Get departures at 7am (30 departures = ~1-2 hours window)
            sb_7am = get_stationboard(station_name, ref_time_str_7, limit=30)
            time.sleep(DELAY_BETWEEN_CALLS)
            
            # Step 3: Get departures at 8am
            sb_8am = get_stationboard(station_name, ref_time_str_8, limit=30)
            time.sleep(DELAY_BETWEEN_CALLS)
            
            info_7 = count_trains_in_window(sb_7am)
            info_8 = count_trains_in_window(sb_8am)
            
            # Combine categories
            all_cats = {}
            for cat, count in info_7['categories'].items():
                all_cats[cat] = all_cats.get(cat, 0) + count
            for cat, count in info_8['categories'].items():
                all_cats[cat] = all_cats.get(cat, 0) + count
            
            total_deps = info_7['total_departures'] + info_8['total_departures']
            # Rough trains/hour (we're looking at ~2 hours of departures)
            trains_per_hour = round(total_deps / 2, 1)
            
            # Breakdown by type
            ic_ir = sum(v for k, v in all_cats.items() if k in ('IC', 'IR', 'ICE', 'TGV', 'EC'))
            regional = sum(v for k, v in all_cats.items() if k in ('S', 'RE', 'R', 'RER'))
            metro_tram = sum(v for k, v in all_cats.items() if k in ('M', 'T'))
            other = total_deps - ic_ir - regional - metro_tram
            
            all_operators = info_7['operators'] | info_8['operators']
            all_destinations = info_7['destinations'] | info_8['destinations']
            
            # Aggregate capacity data
            all_cap1 = info_7['cap1_values'] + info_8['cap1_values']
            all_cap2 = info_7['cap2_values'] + info_8['cap2_values']
            
            has_capacity = len(all_cap1) > 0 or len(all_cap2) > 0
            cap1_avg = round(sum(all_cap1) / len(all_cap1), 2) if all_cap1 else None
            cap2_avg = round(sum(all_cap2) / len(all_cap2), 2) if all_cap2 else None
            cap_coverage = round(len(all_cap1) / total_deps * 100, 0) if total_deps > 0 else 0
            
            # Workability score: lower capacity = more space to work
            # 0 = empty (great for laptops), 2 = packed (sardine can)
            # Invert: workability = 2 - avg_cap, so higher = better for working
            work_score_1st = round(2 - cap1_avg, 2) if cap1_avg is not None else None
            work_score_2nd = round(2 - cap2_avg, 2) if cap2_avg is not None else None
            
            result = {
                'name': station_name,
                'station_id': station_id,
                'lat_wgs84': lat,
                'lon_wgs84': lon,
                'total_departures_2h': total_deps,
                'trains_per_hour': trains_per_hour,
                'ic_ir_departures': ic_ir,
                'regional_departures': regional,
                'metro_tram_departures': metro_tram,
                'other_departures': other,
                'has_capacity_data': has_capacity,
                'capacity_coverage_pct': cap_coverage,
                'avg_occupancy_1st': cap1_avg,
                'avg_occupancy_2nd': cap2_avg,
                'workability_1st': work_score_1st,
                'workability_2nd': work_score_2nd,
                'category_breakdown': '; '.join(f"{k}:{v}" for k, v in sorted(all_cats.items())),
                'operators': '; '.join(sorted(all_operators)),
                'sample_destinations': '; '.join(sorted(list(all_destinations)[:10])),
                'query_date': ref_time_str_7,
            }
            results.append(result)
            
            cap_str = ""
            if has_capacity:
                cap_str = f" | occ: 1st={cap1_avg}, 2nd={cap2_avg} ({cap_coverage:.0f}% coverage)"
            print(f"{trains_per_hour} trains/hr ({ic_ir} IC/IR, {regional} regional){cap_str}")
            
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
    print(f"SERVICE FREQUENCY PROFILE — City101 Corridor")
    print(f"{'='*70}")
    print(f"Stations queried: {len(CORRIDOR_STATIONS)}")
    print(f"Stations found: {len(results)}")
    print(f"Errors: {len(errors)}")
    
    if results:
        print(f"\nFrequency ranking (trains/hour, workday 7-9am):")
        print(f"{'Station':<30} {'Trains/hr':>10} {'IC/IR':>6} {'Regional':>9} {'Metro':>6} {'Occ1st':>7} {'Occ2nd':>7} {'Work1st':>8}")
        print("-" * 95)
        for r in results:
            o1 = f"{r['avg_occupancy_1st']:.1f}" if r['avg_occupancy_1st'] is not None else "-"
            o2 = f"{r['avg_occupancy_2nd']:.1f}" if r['avg_occupancy_2nd'] is not None else "-"
            w1 = f"{r['workability_1st']:.1f}" if r['workability_1st'] is not None else "-"
            print(f"{r['name']:<30} {r['trains_per_hour']:>10} {r['ic_ir_departures']:>6} {r['regional_departures']:>9} {r['metro_tram_departures']:>6} {o1:>7} {o2:>7} {w1:>8}")
    
    # Capacity coverage summary
    if results:
        with_cap = [r for r in results if r['has_capacity_data']]
        without_cap = [r for r in results if not r['has_capacity_data']]
        print(f"\n--- CAPACITY DATA COVERAGE ---")
        print(f"Stations with capacity data: {len(with_cap)}/{len(results)}")
        if with_cap:
            avg_cov = sum(r['capacity_coverage_pct'] for r in with_cap) / len(with_cap)
            print(f"Average coverage per station: {avg_cov:.0f}% of departures")
            
            # Best stations for working on the train
            workable = [r for r in with_cap if r['workability_1st'] is not None]
            if workable:
                workable.sort(key=lambda x: x['workability_1st'], reverse=True)
                print(f"\nBest stations for working on trains (1st class workability, 2=empty, 0=packed):")
                for r in workable[:10]:
                    print(f"  {r['name']:<30} work_score={r['workability_1st']:.2f}  ({r['trains_per_hour']} trains/hr)")
                print(f"\nWorst stations (most crowded 1st class):")
                for r in workable[-5:]:
                    print(f"  {r['name']:<30} work_score={r['workability_1st']:.2f}  ({r['trains_per_hour']} trains/hr)")
        
        if without_cap:
            print(f"\nStations with NO capacity data: {', '.join(r['name'] for r in without_cap)}")
    
    if errors:
        print(f"\nErrors:")
        for name, err in errors:
            print(f"  {name}: {err}")
    
    print(f"\nOutput: {OUTPUT_CSV}")
    
    # Narrative insight
    if results:
        max_freq = results[0]
        min_freq = results[-1]
        print(f"\n--- NARRATIVE INSIGHT ---")
        print(f"Highest frequency: {max_freq['name']} ({max_freq['trains_per_hour']} trains/hr)")
        print(f"Lowest frequency: {min_freq['name']} ({min_freq['trains_per_hour']} trains/hr)")
        ratio = max_freq['trains_per_hour'] / min_freq['trains_per_hour'] if min_freq['trains_per_hour'] > 0 else float('inf')
        print(f"Frequency ratio: {ratio:.1f}x")
        print(f"The 'promise of mobility' varies {ratio:.0f}-fold along the corridor.")
        print(f"High-frequency nodes = reliable working continuity.")
        print(f"Low-frequency gaps = forced dwell time → need infrastructure.")
    
    print(f"{'='*70}")


if __name__ == '__main__':
    main()
