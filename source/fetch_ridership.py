#!/usr/bin/env python3
"""
SCRIPT 1: SBB Passagierfrequenz → City101 Corridor Ridership
=============================================================
Downloads SBB passenger frequency data, filters for Geneva-Villeneuve corridor,
takes most recent year per station, computes commuter index, outputs clean CSV.

Run locally: python3 fetch_ridership.py
Output: city101_ridership_sbb.csv (one row per station, most recent year)

Source: data.sbb.ch/passagierfrequenz
"""
import csv
import io
import urllib.request
import ssl
import os

# === CONFIG ===
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(OUTPUT_DIR, 'city101_ridership_sbb.csv')
SBB_URL = 'https://data.sbb.ch/api/v2/catalog/datasets/passagierfrequenz/exports/csv'

# Corridor bounding box (generous — Geneva to Villeneuve + hinterland)
LAT_MIN, LAT_MAX = 46.15, 46.55
LON_MIN, LON_MAX = 6.05, 6.97

# Cantons that are definitely in the corridor
CORRIDOR_CANTONS = {'GE', 'VD'}


# === MAIN ===
def main():
    print("Fetching SBB Passagierfrequenz data...")
    ctx = ssl.create_default_context()
    req = urllib.request.Request(SBB_URL, headers={'User-Agent': 'EPFL-Studio-Research/1.0'})
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
        raw = resp.read().decode('utf-8')
    
    reader = csv.DictReader(io.StringIO(raw), delimiter=';')
    all_rows = list(reader)
    print(f"Total rows in raw dataset: {len(all_rows)}")
    
    # Filter for corridor
    corridor_rows = []
    for row in all_rows:
        geopos = row.get('geopos', '')
        if not geopos or ',' not in geopos:
            continue
        try:
            parts = geopos.strip().split(',')
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
        except (ValueError, IndexError):
            continue
        
        in_bbox = (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX)
        in_canton = row.get('kt_ct_cantone', '') in CORRIDOR_CANTONS
        
        if in_bbox or in_canton:
            row['lat_wgs84'] = lat
            row['lon_wgs84'] = lon
            corridor_rows.append(row)
    
    print(f"Corridor rows (all years): {len(corridor_rows)}")
    
    # Group by station, keep most recent year
    stations = {}
    for row in corridor_rows:
        code = row.get('code_codice', '')
        name = row.get('bahnhof_gare_stazione', '')
        key = f"{code}_{name}"
        year = int(row.get('jahr_annee_anno', '0'))
        
        if key not in stations or year > stations[key]['year']:
            daily = float(row.get('dtv_tjm_tgm', '0') or '0')
            workday = float(row.get('dwv_tmjo_tfm', '0') or '0')
            nonworkday = float(row.get('dnwv_tmjno_tmgnl', '0') or '0')
            
            # Commuter index: workday/nonworkday ratio
            # >2.0 = strong commuter station, <1.0 = leisure/tourism
            commuter_index = round(workday / nonworkday, 2) if nonworkday > 0 else 0
            
            stations[key] = {
                'code': code,
                'uic': row.get('uic', ''),
                'name': name,
                'canton': row.get('kt_ct_cantone', ''),
                'infrastructure_manager': row.get('isb_gi', ''),
                'year': year,
                'daily_avg': daily,
                'workday_avg': workday,
                'nonworkday_avg': nonworkday,
                'commuter_index': commuter_index,
                'transport_companies': row.get('evu_ef_itf', ''),
                'lat_wgs84': row['lat_wgs84'],
                'lon_wgs84': row['lon_wgs84'],
                'remarks_de': row.get('bemerkungen', ''),
            }
    
    # Sort by daily average descending
    sorted_stations = sorted(stations.values(), key=lambda x: x['daily_avg'], reverse=True)
    
    # Write CSV
    fields = ['code', 'uic', 'name', 'canton', 'infrastructure_manager', 'year',
              'daily_avg', 'workday_avg', 'nonworkday_avg', 'commuter_index',
              'transport_companies', 'lat_wgs84', 'lon_wgs84', 'remarks_de']
    
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for s in sorted_stations:
            writer.writerow(s)
    
    # === SUMMARY ===
    print(f"\n{'='*70}")
    print(f"CITY101 CORRIDOR RIDERSHIP — SBB PASSAGIERFREQUENZ")
    print(f"{'='*70}")
    print(f"Unique stations: {len(sorted_stations)}")
    
    total_daily = sum(s['daily_avg'] for s in sorted_stations)
    print(f"Total daily passengers: {total_daily:,.0f}")
    
    # By canton
    cantons = {}
    for s in sorted_stations:
        c = s['canton']
        cantons.setdefault(c, {'count': 0, 'daily': 0})
        cantons[c]['count'] += 1
        cantons[c]['daily'] += s['daily_avg']
    print(f"\nBy canton:")
    for c, v in sorted(cantons.items(), key=lambda x: x[1]['daily'], reverse=True):
        print(f"  {c}: {v['count']} stations, {v['daily']:,.0f} daily passengers")
    
    # Top stations
    print(f"\nTop 20 by daily ridership:")
    print(f"{'Station':<35} {'Daily':>8} {'Workday':>8} {'CommIdx':>8} {'Canton':>6} {'Year':>5}")
    print("-" * 75)
    for s in sorted_stations[:20]:
        print(f"{s['name']:<35} {s['daily_avg']:>8,.0f} {s['workday_avg']:>8,.0f} {s['commuter_index']:>8.2f} {s['canton']:>6} {s['year']:>5}")
    
    # Highest commuter indices (strong commuter stations)
    commuter_stations = [s for s in sorted_stations if s['daily_avg'] > 200 and s['commuter_index'] > 0]
    commuter_stations.sort(key=lambda x: x['commuter_index'], reverse=True)
    print(f"\nTop 15 commuter stations (highest workday/nonworkday ratio):")
    for s in commuter_stations[:15]:
        print(f"  {s['name']:<35} {s['commuter_index']:.2f}x  ({s['workday_avg']:,.0f}/{s['nonworkday_avg']:,.0f})")
    
    # Tourism/leisure stations (ratio < 1.0 means more weekend than workday use)
    leisure = [s for s in sorted_stations if s['commuter_index'] > 0 and s['commuter_index'] < 1.0 and s['daily_avg'] > 100]
    leisure.sort(key=lambda x: x['commuter_index'])
    if leisure:
        print(f"\nLeisure/tourism stations (more weekend than workday use):")
        for s in leisure[:10]:
            print(f"  {s['name']:<35} {s['commuter_index']:.2f}x  ({s['workday_avg']:,.0f}/{s['nonworkday_avg']:,.0f})")
    
    # Bottom stations (smallest)
    print(f"\nSmallest stations:")
    for s in sorted_stations[-10:]:
        print(f"  {s['name']:<35} {s['daily_avg']:>8,.0f} daily  {s['canton']}")
    
    print(f"\nOutput: {OUTPUT_CSV}")
    print(f"{'='*70}")


if __name__ == '__main__':
    main()
