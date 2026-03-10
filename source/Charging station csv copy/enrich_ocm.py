#!/usr/bin/env python3
"""
Script 3: Open Charge Map enrichment + reviews collection.
Reads ENRICHED_v2 (34 cols), cross-references with OCM, adds metadata + extracts reviews.
Outputs:
  - city101_ev_charging_ENRICHED_v3.csv (stations with OCM columns)
  - city101_ev_charging_REVIEWS.csv (one row per review)
Prints ONLY a summary at the end.
"""

import csv
import json
import math
import urllib.request
import urllib.parse
import ssl
import time
from collections import Counter

# === CONFIG ===
INPUT_CSV = '/mnt/project/city101_ev_charging_ENRICHED_v2.csv'
OUTPUT_STATIONS = '/home/claude/city101_ev_charging_ENRICHED_v3.csv'
OUTPUT_REVIEWS = '/home/claude/city101_ev_charging_REVIEWS.csv'
OCM_API_KEY = '23617e07-95e4-4666-b1f6-f4dfcd6a8e64'
OCM_BASE = 'https://api.openchargemap.io/v3/poi/'
MATCH_THRESHOLD_M = 200  # max distance for matching
CORRIDOR_BBOX = '(46.10,6.05),(46.55,6.95)'

# === HELPERS ===
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def safe_float(val, default=None):
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

def fetch_json(url, max_retries=3):
    """Fetch JSON from URL with retries."""
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

def extract_connections_summary(connections):
    """Summarize connection types from OCM connections list."""
    if not connections:
        return '', '', ''
    
    types = []
    max_power = 0
    levels = set()
    
    for conn in connections:
        ct = conn.get('ConnectionType', {})
        if ct:
            types.append(ct.get('Title', ''))
        
        power = conn.get('PowerKW') or 0
        if power > max_power:
            max_power = power
        
        level = conn.get('Level', {})
        if level:
            levels.add(level.get('Title', ''))
    
    types_str = '; '.join(sorted(set(t for t in types if t)))
    levels_str = '; '.join(sorted(levels))
    
    return types_str, max_power if max_power > 0 else '', levels_str

def extract_usage_info(poi):
    """Extract usage/access information."""
    usage = poi.get('UsageType', {}) or {}
    return {
        'ocm_usage_type': usage.get('Title', ''),
        'ocm_is_pay_at_location': usage.get('IsPayAtLocation', ''),
        'ocm_is_membership_required': usage.get('IsMembershipRequired', ''),
        'ocm_is_access_key_required': usage.get('IsAccessKeyRequired', ''),
        'ocm_usage_cost': poi.get('UsageCost', ''),
    }

def extract_operator_info(poi):
    """Extract operator details."""
    op = poi.get('OperatorInfo', {}) or {}
    return {
        'ocm_operator': op.get('Title', ''),
        'ocm_operator_url': op.get('WebsiteURL', ''),
        'ocm_operator_phone': op.get('PhonePrimaryContact', ''),
    }


# === MAIN ===
def main():
    results = {
        'ocm_fetched': 0,
        'matched': 0,
        'unmatched': 0,
        'reviews_total': 0,
        'reviews_by_station': Counter(),
        'match_distances': [],
        'ocm_operators': Counter(),
        'new_power_filled': 0,
        'new_operator_filled': 0,
    }
    
    # 1. Read our enriched CSV
    rows = []
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        original_fields = reader.fieldnames[:]
        for row in reader:
            rows.append(row)
    n = len(rows)
    
    # 2. Fetch OCM data for the corridor
    # OCM API limits to 500 per request, paginate if needed
    all_ocm = []
    
    # Fetch in chunks by shifting longitude windows if needed
    params = {
        'output': 'json',
        'maxresults': '500',
        'boundingbox': CORRIDOR_BBOX,
        'includecomments': 'true',
        'key': OCM_API_KEY,
        'compact': 'false',
    }
    url = OCM_BASE + '?' + urllib.parse.urlencode(params)
    
    try:
        ocm_data = fetch_json(url)
        all_ocm = ocm_data
        results['ocm_fetched'] = len(all_ocm)
    except Exception as e:
        print(f"ERROR fetching OCM data: {e}")
        return
    
    # 3. Build OCM lookup — extract key fields
    ocm_stations = []
    for poi in all_ocm:
        addr = poi.get('AddressInfo', {}) or {}
        lat = addr.get('Latitude')
        lon = addr.get('Longitude')
        if lat is None or lon is None:
            continue
        
        conn_types, max_power, levels = extract_connections_summary(poi.get('Connections', []))
        usage = extract_usage_info(poi)
        operator = extract_operator_info(poi)
        status = poi.get('StatusType', {}) or {}
        
        comments = poi.get('UserComments') or []
        
        ocm_stations.append({
            'lat': lat,
            'lon': lon,
            'ocm_id': poi.get('ID', ''),
            'ocm_uuid': poi.get('UUID', ''),
            'ocm_title': addr.get('Title', ''),
            'ocm_town': addr.get('Town', ''),
            'ocm_postcode': addr.get('Postcode', ''),
            'ocm_address': addr.get('AddressLine1', ''),
            'ocm_connection_types': conn_types,
            'ocm_max_power_kw': max_power,
            'ocm_charging_levels': levels,
            'ocm_n_points': poi.get('NumberOfPoints', ''),
            'ocm_status': status.get('Title', ''),
            'ocm_is_operational': status.get('IsOperational', ''),
            'ocm_general_comments': (poi.get('GeneralComments', '') or '')[:200],
            'ocm_date_last_verified': poi.get('DateLastVerified', ''),
            'ocm_date_created': poi.get('DateCreated', ''),
            **usage,
            **operator,
            'comments': comments,  # raw comments for reviews CSV
        })
        
        results['ocm_operators'][operator.get('ocm_operator', 'Unknown')] += 1
    
    # 4. Match OCM stations to our 194 stations by proximity
    # For each of our stations, find the closest OCM station within threshold
    reviews = []  # collect all reviews
    
    new_ocm_fields = [
        'ocm_id', 'ocm_uuid', 'ocm_title', 'ocm_status', 'ocm_is_operational',
        'ocm_connection_types', 'ocm_max_power_kw', 'ocm_charging_levels', 'ocm_n_points',
        'ocm_usage_type', 'ocm_usage_cost', 'ocm_is_pay_at_location', 
        'ocm_is_membership_required', 'ocm_is_access_key_required',
        'ocm_operator', 'ocm_operator_url',
        'ocm_general_comments', 'ocm_date_last_verified',
        'ocm_match_dist_m',
    ]
    
    for i, row in enumerate(rows):
        lat = safe_float(row.get('latitude_wgs84'))
        lon = safe_float(row.get('longitude_wgs84'))
        
        # Initialize all OCM fields as empty
        for field in new_ocm_fields:
            row[field] = ''
        
        if lat is None or lon is None:
            results['unmatched'] += 1
            continue
        
        # Find closest OCM station
        best_dist = float('inf')
        best_ocm = None
        
        for ocm in ocm_stations:
            d = haversine(lat, lon, ocm['lat'], ocm['lon'])
            if d < best_dist:
                best_dist = d
                best_ocm = ocm
        
        if best_ocm and best_dist <= MATCH_THRESHOLD_M:
            results['matched'] += 1
            results['match_distances'].append(best_dist)
            
            # Copy OCM fields
            row['ocm_id'] = best_ocm['ocm_id']
            row['ocm_uuid'] = best_ocm['ocm_uuid']
            row['ocm_title'] = best_ocm['ocm_title']
            row['ocm_status'] = best_ocm['ocm_status']
            row['ocm_is_operational'] = best_ocm['ocm_is_operational']
            row['ocm_connection_types'] = best_ocm['ocm_connection_types']
            row['ocm_max_power_kw'] = best_ocm['ocm_max_power_kw']
            row['ocm_charging_levels'] = best_ocm['ocm_charging_levels']
            row['ocm_n_points'] = best_ocm['ocm_n_points']
            row['ocm_usage_type'] = best_ocm['ocm_usage_type']
            row['ocm_usage_cost'] = best_ocm['ocm_usage_cost']
            row['ocm_is_pay_at_location'] = best_ocm['ocm_is_pay_at_location']
            row['ocm_is_membership_required'] = best_ocm['ocm_is_membership_required']
            row['ocm_is_access_key_required'] = best_ocm['ocm_is_access_key_required']
            row['ocm_operator'] = best_ocm['ocm_operator']
            row['ocm_operator_url'] = best_ocm['ocm_operator_url']
            row['ocm_general_comments'] = best_ocm['ocm_general_comments']
            row['ocm_date_last_verified'] = best_ocm['ocm_date_last_verified']
            row['ocm_match_dist_m'] = round(best_dist, 1)
            
            # Fill gaps in our data from OCM
            if (not row.get('power_kw') or row['power_kw'] == '') and best_ocm['ocm_max_power_kw']:
                row['power_kw'] = best_ocm['ocm_max_power_kw']
                results['new_power_filled'] += 1
            
            if (not row.get('operator') or row['operator'] == '') and best_ocm['ocm_operator']:
                row['operator'] = best_ocm['ocm_operator']
                results['new_operator_filled'] += 1
            
            # Extract reviews
            for comment in best_ocm.get('comments', []):
                review = {
                    'station_id': row['id'],
                    'station_name': row['name'],
                    'municipality': row.get('municipality', ''),
                    'platform': 'OpenChargeMap',
                    'date': (comment.get('DateCreated', '') or '')[:10],
                    'rating': comment.get('Rating', ''),
                    'username': comment.get('UserName', ''),
                    'comment': (comment.get('Comment', '') or '').replace('\n', ' ').replace('\r', ''),
                    'comment_type': (comment.get('CommentType', {}) or {}).get('Title', ''),
                    'checkin_status': (comment.get('CheckinStatusType', {}) or {}).get('Title', ''),
                    'ocm_comment_id': comment.get('ID', ''),
                }
                reviews.append(review)
                results['reviews_total'] += 1
                results['reviews_by_station'][row['name']] += 1
        else:
            results['unmatched'] += 1
    
    # 5. Write enriched stations CSV
    output_fields = original_fields + new_ocm_fields
    
    with open(OUTPUT_STATIONS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=output_fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    
    # 6. Write reviews CSV
    review_fields = ['station_id', 'station_name', 'municipality', 'platform', 'date',
                     'rating', 'username', 'comment', 'comment_type', 'checkin_status',
                     'ocm_comment_id']
    
    with open(OUTPUT_REVIEWS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=review_fields)
        writer.writeheader()
        for review in reviews:
            writer.writerow(review)
    
    # 7. Print summary
    print('=' * 60)
    print('ENRICHMENT SCRIPT 3 — OPEN CHARGE MAP')
    print('=' * 60)
    print(f'Input:  {INPUT_CSV} ({n} rows, {len(original_fields)} cols)')
    print(f'Output: {OUTPUT_STATIONS} ({n} rows, {len(output_fields)} cols)')
    print(f'Reviews: {OUTPUT_REVIEWS} ({results["reviews_total"]} reviews)')
    print(f'New columns: {len(new_ocm_fields)} → {", ".join(new_ocm_fields[:8])}...')
    print()
    
    print('--- OCM FETCH ---')
    print(f'  OCM stations in corridor: {results["ocm_fetched"]}')
    print(f'  With coordinates: {len(ocm_stations)}')
    print()
    
    print('--- MATCHING ---')
    print(f'  Matched: {results["matched"]}/{n} ({results["matched"]*100//n}%)')
    print(f'  Unmatched: {results["unmatched"]}/{n}')
    if results['match_distances']:
        avg_d = sum(results['match_distances']) / len(results['match_distances'])
        print(f'  Match distances: min={min(results["match_distances"]):.0f}m, max={max(results["match_distances"]):.0f}m, avg={avg_d:.0f}m')
    print(f'  Threshold: {MATCH_THRESHOLD_M}m')
    print()
    
    print('--- GAP FILLING ---')
    print(f'  power_kw filled from OCM: {results["new_power_filled"]}')
    print(f'  operator filled from OCM: {results["new_operator_filled"]}')
    print()
    
    print('--- REVIEWS ---')
    print(f'  Total reviews collected: {results["reviews_total"]}')
    if results['reviews_by_station']:
        print(f'  Stations with reviews:')
        for station, count in results['reviews_by_station'].most_common():
            print(f'    {station}: {count}')
    print()
    
    print('--- OCM OPERATORS (top 10) ---')
    for op, count in results['ocm_operators'].most_common(10):
        print(f'  {op}: {count}')
    print()
    
    # 8. Column inventory
    print('--- COLUMN INVENTORY ---')
    print(f'  Original (v2): {len(original_fields)} cols')
    print(f'  + OCM: {len(new_ocm_fields)} cols')
    print(f'  = Total: {len(output_fields)} cols')
    print()
    
    # Count remaining nulls in key fields
    key_fields = ['operator', 'connectors', 'capacity', 'address', 'power_kw', 
                  'dwell_context', 'location_type', 'ocm_status']
    print('--- REMAINING GAPS ---')
    for field in key_fields:
        if field in output_fields:
            nulls = sum(1 for r in rows if not r.get(field) or r[field] == '' or r[field] == 'unknown')
            print(f'  {field}: {nulls}/{n} empty/unknown')
    
    print(f'\n{"=" * 60}')
    print(f'DONE. CSV: {len(output_fields)} columns, {n} rows.')
    print(f'Reviews CSV: {results["reviews_total"]} reviews from OpenChargeMap.')
    print(f'Next: Google Places API for ratings + richer reviews.')
    print(f'{"=" * 60}')


if __name__ == '__main__':
    main()
