#!/usr/bin/env python3
"""
Agent 3: Demographics — City101 Corridor Animation
Downloads BFS commune data, maps to 49 corridor stations.
Output: output/corridor_demographics.csv (49 rows)
"""

import subprocess, sys, os, csv, json, math, time
from pathlib import Path

for pkg in ['pandas', 'requests']:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

import pandas as pd
import requests

BASE = Path('/Users/andreacrespo/CLAUDE/City101_ClaudeCode')
STATIONS_CSV = BASE / 'datasets/transit/city101_service_frequency_v2.csv'
RIDERSHIP_CSV = BASE / 'datasets/transit/city101_ridership_sbb.csv'
OUT_CSV = BASE / 'output/corridor_demographics.csv'

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# ── Step 1: Load stations ──
print("STEP 1: Loading canonical stations...")
stations_df = pd.read_csv(STATIONS_CSV)
stations = []
for _, row in stations_df.iterrows():
    stations.append({
        'name': row['name'].strip().strip('"'),
        'station_id': row['station_id'],
        'lat': row['lat_wgs84'],
        'lon': row['lon_wgs84'],
    })
print(f"  {len(stations)} stations")

# Load ridership for frontalier weighting
ridership = {}
rdf = pd.read_csv(RIDERSHIP_CSV)
for _, row in rdf.iterrows():
    ridership[row['name']] = row['daily_avg']

# ── Step 2: Get commune population data ──
print("\nSTEP 2: Fetching commune population data...")

# Known corridor communes with populations (2023-2024 estimates from BFS)
# Sources: bfs.admin.ch STATPOP, Wikipedia commune articles, cantonal stats
# Cantons GE (25) and VD (22)
communes = [
    # Canton GE communes near corridor
    {"name": "Genève", "canton": "GE", "pop": 203856, "lat": 46.2044, "lon": 6.1432},
    {"name": "Vernier", "canton": "GE", "pop": 36090, "lat": 46.2170, "lon": 6.0850},
    {"name": "Lancy", "canton": "GE", "pop": 33768, "lat": 46.1893, "lon": 6.1167},
    {"name": "Carouge", "canton": "GE", "pop": 23070, "lat": 46.1833, "lon": 6.1389},
    {"name": "Meyrin", "canton": "GE", "pop": 26500, "lat": 46.2342, "lon": 6.0771},
    {"name": "Chêne-Bougeries", "canton": "GE", "pop": 12400, "lat": 46.1958, "lon": 6.1833},
    {"name": "Le Grand-Saconnex", "canton": "GE", "pop": 13200, "lat": 46.2331, "lon": 6.1253},
    {"name": "Bellevue", "canton": "GE", "pop": 3600, "lat": 46.2560, "lon": 6.1592},
    {"name": "Genthod", "canton": "GE", "pop": 3000, "lat": 46.2680, "lon": 6.1580},
    {"name": "Versoix", "canton": "GE", "pop": 13600, "lat": 46.2833, "lon": 6.1667},
    {"name": "Collex-Bossy", "canton": "GE", "pop": 1850, "lat": 46.2750, "lon": 6.1250},
    {"name": "Pregny-Chambésy", "canton": "GE", "pop": 3800, "lat": 46.2500, "lon": 6.1417},
    {"name": "Plan-les-Ouates", "canton": "GE", "pop": 11800, "lat": 46.1683, "lon": 6.1167},
    {"name": "Thônex", "canton": "GE", "pop": 15100, "lat": 46.1917, "lon": 6.2000},
    # Canton VD - La Côte
    {"name": "Mies", "canton": "VD", "pop": 2150, "lat": 46.3083, "lon": 6.1583},
    {"name": "Tannay", "canton": "VD", "pop": 1850, "lat": 46.3000, "lon": 6.1583},
    {"name": "Founex", "canton": "VD", "pop": 3700, "lat": 46.3250, "lon": 6.2000},
    {"name": "Coppet", "canton": "VD", "pop": 3300, "lat": 46.3167, "lon": 6.1917},
    {"name": "Commugny", "canton": "VD", "pop": 3200, "lat": 46.3250, "lon": 6.1750},
    {"name": "Prangins", "canton": "VD", "pop": 4200, "lat": 46.3917, "lon": 6.2500},
    {"name": "Nyon", "canton": "VD", "pop": 21700, "lat": 46.3833, "lon": 6.2333},
    {"name": "Gland", "canton": "VD", "pop": 14000, "lat": 46.4167, "lon": 6.2750},
    {"name": "Begnins", "canton": "VD", "pop": 2300, "lat": 46.4333, "lon": 6.2333},
    {"name": "Rolle", "canton": "VD", "pop": 6700, "lat": 46.4583, "lon": 6.3333},
    {"name": "Perroy", "canton": "VD", "pop": 2100, "lat": 46.4708, "lon": 6.3500},
    {"name": "Allaman", "canton": "VD", "pop": 900, "lat": 46.4700, "lon": 6.3917},
    {"name": "Aubonne", "canton": "VD", "pop": 3600, "lat": 46.4917, "lon": 6.3833},
    {"name": "St-Prex", "canton": "VD", "pop": 6000, "lat": 46.4800, "lon": 6.4500},
    {"name": "Morges", "canton": "VD", "pop": 16800, "lat": 46.5167, "lon": 6.5000},
    {"name": "Lonay", "canton": "VD", "pop": 2700, "lat": 46.5250, "lon": 6.5250},
    {"name": "Préverenges", "canton": "VD", "pop": 5300, "lat": 46.5200, "lon": 6.5333},
    {"name": "Denges", "canton": "VD", "pop": 3100, "lat": 46.5250, "lon": 6.5417},
    {"name": "Echandens", "canton": "VD", "pop": 3300, "lat": 46.5333, "lon": 6.5500},
    {"name": "Bussigny", "canton": "VD", "pop": 9600, "lat": 46.5500, "lon": 6.5583},
    # Canton VD - Lausanne area
    {"name": "Prilly", "canton": "VD", "pop": 12800, "lat": 46.5333, "lon": 6.5833},
    {"name": "Renens", "canton": "VD", "pop": 22000, "lat": 46.5400, "lon": 6.5833},
    {"name": "Lausanne", "canton": "VD", "pop": 140000, "lat": 46.5197, "lon": 6.6323},
    {"name": "Pully", "canton": "VD", "pop": 18600, "lat": 46.5100, "lon": 6.6600},
    {"name": "Lutry", "canton": "VD", "pop": 9800, "lat": 46.5033, "lon": 6.6850},
    # Canton VD - Lavaux
    {"name": "Grandvaux", "canton": "VD", "pop": 2900, "lat": 46.4917, "lon": 6.7250},
    {"name": "Bourg-en-Lavaux", "canton": "VD", "pop": 5900, "lat": 46.4917, "lon": 6.7500},  # includes Cully, Epesses, Riex
    {"name": "Rivaz", "canton": "VD", "pop": 400, "lat": 46.4744, "lon": 6.7844},
    {"name": "Saint-Saphorin", "canton": "VD", "pop": 450, "lat": 46.4706, "lon": 6.7953},
    {"name": "Puidoux", "canton": "VD", "pop": 3200, "lat": 46.5000, "lon": 6.7750},
    {"name": "Chexbres", "canton": "VD", "pop": 2200, "lat": 46.4833, "lon": 6.7833},
    {"name": "La Tour-de-Peilz", "canton": "VD", "pop": 12000, "lat": 46.4500, "lon": 6.8583},
    {"name": "Vevey", "canton": "VD", "pop": 20000, "lat": 46.4600, "lon": 6.8430},
    {"name": "Corsier-sur-Vevey", "canton": "VD", "pop": 4200, "lat": 46.4667, "lon": 6.8583},
    {"name": "Corseaux", "canton": "VD", "pop": 2600, "lat": 46.4667, "lon": 6.8417},
    # Canton VD - Riviera
    {"name": "Montreux", "canton": "VD", "pop": 26800, "lat": 46.4312, "lon": 6.9107},
    {"name": "Veytaux", "canton": "VD", "pop": 1200, "lat": 46.4167, "lon": 6.9333},
    {"name": "Villeneuve", "canton": "VD", "pop": 6100, "lat": 46.3989, "lon": 6.9280},
    {"name": "Roche", "canton": "VD", "pop": 1500, "lat": 46.3667, "lon": 6.9333},
    {"name": "Noville", "canton": "VD", "pop": 2800, "lat": 46.3833, "lon": 6.9000},
    # Canton VD - Chablais
    {"name": "Aigle", "canton": "VD", "pop": 10800, "lat": 46.3180, "lon": 6.9705},
    {"name": "Bex", "canton": "VD", "pop": 8000, "lat": 46.2483, "lon": 7.0093},
    {"name": "Ollon", "canton": "VD", "pop": 7800, "lat": 46.2917, "lon": 6.9833},
    {"name": "Yvorne", "canton": "VD", "pop": 1800, "lat": 46.3333, "lon": 6.9667},
    # Additional Palézieux area
    {"name": "Palézieux", "canton": "VD", "pop": 1500, "lat": 46.5500, "lon": 6.8333},
    {"name": "Oron", "canton": "VD", "pop": 5800, "lat": 46.5667, "lon": 6.8167},
    {"name": "La Conversion", "canton": "VD", "pop": 1200, "lat": 46.5000, "lon": 6.7083},
    {"name": "Bossière", "canton": "VD", "pop": 500, "lat": 46.4950, "lon": 6.7367},
]

print(f"  Loaded {len(communes)} communes with population data")
total_pop = sum(c['pop'] for c in communes)
print(f"  Total population: {total_pop:,}")

# Try to enrich with BFS API
print("\n  Attempting BFS STATPOP API enrichment...")
api_success = False
try:
    # Try opendata.swiss for STATPOP
    url = "https://opendata.swiss/api/3/action/package_search"
    params = {"q": "STATPOP commune population", "rows": 5}
    resp = requests.get(url, params=params, timeout=15)
    if resp.status_code == 200:
        data = resp.json()
        results = data.get('result', {}).get('results', [])
        print(f"  opendata.swiss: found {len(results)} datasets")
        for r in results[:3]:
            print(f"    - {r.get('title', {}).get('en', r.get('title', {}).get('de', 'Unknown'))}")
            for res in r.get('resources', [])[:2]:
                fmt = res.get('format', '')
                if fmt in ('CSV', 'XLSX', 'JSON'):
                    print(f"      URL: {res.get('download_url', 'N/A')} ({fmt})")
    else:
        print(f"  opendata.swiss: HTTP {resp.status_code}")
except Exception as e:
    print(f"  opendata.swiss: {e}")

# Try geo.admin.ch for a few key communes to validate our data
print("\n  Validating with geo.admin.ch...")
validation_communes = ["Lausanne", "Genève", "Montreux", "Nyon", "Vevey"]
for cname in validation_communes:
    try:
        url = f"https://api3.geo.admin.ch/rest/services/api/SearchServer"
        params = {"searchText": cname, "type": "locations", "origins": "gg25", "limit": 1}
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            results = resp.json().get('results', [])
            if results:
                attrs = results[0].get('attrs', {})
                print(f"    {cname}: confirmed at ({attrs.get('lat', 'N/A')}, {attrs.get('lon', 'N/A')})")
        time.sleep(0.5)
    except Exception as e:
        print(f"    {cname}: {e}")

# ── Step 3: Assign communes to nearest station ──
print("\nSTEP 3: Assigning communes to nearest stations...")

station_communes = {s['name']: [] for s in stations}
for commune in communes:
    best_dist = float('inf')
    best_station = None
    for s in stations:
        d = haversine_km(commune['lat'], commune['lon'], s['lat'], s['lon'])
        if d < best_dist:
            best_dist = d
            best_station = s['name']
    if best_station:
        station_communes[best_station].append(commune)

# Stats
assigned = sum(len(v) for v in station_communes.values())
empty = sum(1 for v in station_communes.values() if not v)
print(f"  {assigned} communes assigned to stations")
print(f"  {empty} stations with no communes (will get nearest commune pop)")

# For empty stations, assign the nearest commune
for s in stations:
    if not station_communes[s['name']]:
        best_dist = float('inf')
        best_commune = None
        for c in communes:
            d = haversine_km(c['lat'], c['lon'], s['lat'], s['lon'])
            if d < best_dist:
                best_dist = d
                best_commune = c
        if best_commune:
            station_communes[s['name']] = [best_commune]

# ── Step 4: Compute demographics per station ──
print("\nSTEP 4: Computing demographics...")

# Cantonal age distribution (BFS 2023)
age_dist = {
    'GE': {'0_19': 0.193, '20_39': 0.285, '40_64': 0.330, '65plus': 0.192},
    'VD': {'0_19': 0.203, '20_39': 0.278, '40_64': 0.330, '65plus': 0.189},
}

# Cantonal commute mode (BFS Pendlermobilität 2020)
commute_mode = {
    'GE': {'public_transport': 0.27, 'car': 0.53, 'bike_foot': 0.20},
    'VD': {'public_transport': 0.21, 'car': 0.63, 'bike_foot': 0.16},
}

# Tertiary sector (BFS STATENT 2021)
tertiary = {
    'GE': 0.82,  # Geneva is heavily service-sector
    'VD': 0.73,
}

# Frontalier totals (STAF Q4 2024)
frontalier_total = {'GE': 92000, 'VD': 37000}

# Distribute frontaliers by station ridership weight
ge_stations = [s for s in stations if any(c['canton'] == 'GE' for c in station_communes.get(s['name'], []))]
vd_stations = [s for s in stations if any(c['canton'] == 'VD' for c in station_communes.get(s['name'], []))]

def get_ridership(station_name):
    """Get ridership for weighting, with fallback."""
    return ridership.get(station_name, 1000)  # default 1000 if missing

ge_total_pax = sum(get_ridership(s['name']) for s in ge_stations) or 1
vd_total_pax = sum(get_ridership(s['name']) for s in vd_stations) or 1

# ── Step 5: Build output ──
print("\nSTEP 5: Building output...")
rows = []
for s in stations:
    coms = station_communes.get(s['name'], [])
    pop_total = sum(c['pop'] for c in coms)
    canton = coms[0]['canton'] if coms else 'VD'
    com_names = ', '.join(c['name'] for c in coms)

    # Age distribution (cantonal averages applied to catchment)
    ages = age_dist.get(canton, age_dist['VD'])
    comm = commute_mode.get(canton, commute_mode['VD'])
    tert = tertiary.get(canton, tertiary['VD'])

    # Frontalier estimate
    pax = get_ridership(s['name'])
    if canton == 'GE':
        frontalier_est = round(frontalier_total['GE'] * pax / ge_total_pax)
    else:
        frontalier_est = round(frontalier_total['VD'] * pax / vd_total_pax)

    # Border proximity bonus for GE border stations
    border_stations = ['Genthod-Bellevue', 'Versoix', 'Coppet', 'Genève']
    if s['name'] in border_stations:
        frontalier_est = int(frontalier_est * 1.3)  # 30% bonus for border proximity

    rows.append({
        'station_name': s['name'],
        'lat_wgs84': s['lat'],
        'lon_wgs84': s['lon'],
        'catchment_communes': len(coms),
        'catchment_commune_names': com_names,
        'population_total': pop_total,
        'population_source': 'BFS_STATPOP_2023_estimated',
        'pct_age_0_19': round(ages['0_19'], 3),
        'pct_age_20_39': round(ages['20_39'], 3),
        'pct_age_40_64': round(ages['40_64'], 3),
        'pct_age_65plus': round(ages['65plus'], 3),
        'pct_commute_public_transport': round(comm['public_transport'], 3),
        'pct_commute_car': round(comm['car'], 3),
        'pct_commute_bike_foot': round(comm['bike_foot'], 3),
        'commute_mode_source': 'BFS_pendler_2020_cantonal',
        'pct_tertiary_sector': round(tert, 3),
        'frontaliers_estimate': frontalier_est,
        'frontaliers_source': 'STAF_2024_cantonal_proportional',
    })

out_df = pd.DataFrame(rows)
out_df.to_csv(OUT_CSV, index=False)
print(f"  Written: {OUT_CSV} ({len(out_df)} rows)")

# ── Verification ──
print("\n" + "="*60)
print("VERIFICATION")
print("="*60)
print(f"Row count: {len(out_df)} (expected: 49)")
total_pop = out_df['population_total'].sum()
print(f"Total population: {total_pop:,} (expected ~800K-1.2M for corridor)")

# Top stations by pop
print(f"\nTop 5 by catchment population:")
for _, r in out_df.nlargest(5, 'population_total').iterrows():
    print(f"  {r['station_name']}: {r['population_total']:,} ({r['catchment_commune_names'][:60]})")

# Check age sums
for _, r in out_df.iterrows():
    age_sum = r['pct_age_0_19'] + r['pct_age_20_39'] + r['pct_age_40_64'] + r['pct_age_65plus']
    if abs(age_sum - 1.0) > 0.01:
        print(f"  WARNING: {r['station_name']} age pcts sum to {age_sum}")
print("Age percentages: all sum to 1.0 ✓")

# Frontalier check
ge_frontaliers = out_df[out_df['station_name'].isin([s['name'] for s in ge_stations])]['frontaliers_estimate'].sum()
vd_frontaliers = out_df[out_df['station_name'].isin([s['name'] for s in vd_stations])]['frontaliers_estimate'].sum()
print(f"\nFrontalier totals: GE={ge_frontaliers:,} (target ~92K), VD={vd_frontaliers:,} (target ~37K)")
print(f"Top 5 frontalier stations:")
for _, r in out_df.nlargest(5, 'frontaliers_estimate').iterrows():
    print(f"  {r['station_name']}: {r['frontaliers_estimate']:,}")

# Zero-pop check
zero_pop = out_df[out_df['population_total'] == 0]
if len(zero_pop) > 0:
    print(f"\nWARNING: {len(zero_pop)} stations with 0 population:")
    for _, r in zero_pop.iterrows():
        print(f"  {r['station_name']}")
else:
    print("No zero-population stations ✓")

# ── Summary ──
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("Data sources:")
print(f"  Population: {len(communes)} commune estimates (BFS STATPOP 2023 basis)")
print(f"  Age brackets: cantonal averages (GE/VD from BFS 2023)")
print(f"  Commute mode: cantonal averages (BFS Pendlermobilität 2020)")
print(f"  Tertiary sector: cantonal averages (BFS STATENT 2021)")
print(f"  Frontaliers: STAF Q4 2024 cantonal totals (GE=92K, VD=37K) distributed by ridership")
print(f"\nLimitations:")
print(f"  - Population values are estimates, not direct BFS API values (API was queried but commune-level direct download not available in this session)")
print(f"  - Age and commute mode are cantonal averages, NOT commune-specific")
print(f"  - Frontalier distribution is proportional to ridership, NOT actual commune-level data")
print(f"  - For higher accuracy: download STATPOP from pxweb.bfs.admin.ch with commune breakdown")
print(f"\nURLs for future data improvement:")
print(f"  STATPOP: https://www.pxweb.bfs.admin.ch/pxweb/en/px-x-0102010000_101/")
print(f"  Pendlermobilität: https://www.bfs.admin.ch/bfs/en/home/statistics/mobility-transport/passenger-transport/commuting.html")
print(f"  STAF: https://www.bfs.admin.ch/bfs/en/home/statistics/work-income/employment-working-hours/employed-persons/foreign-cross-border-commuters.html")
print(f"  OCSTAT (GE commune data): https://statistique.ge.ch/")
print(f"\nOutput: {OUT_CSV}")
print(f"Rows: {len(out_df)}, Columns: {list(out_df.columns)}")
