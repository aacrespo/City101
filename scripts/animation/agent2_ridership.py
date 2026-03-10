#!/usr/bin/env python3
"""
Agent 2: Passenger Counts & Ridership — City101 Corridor Animation
Consolidates existing ridership data, fills 8 station gaps, models 24h hourly curves.
Output: output/station_ridership.csv (49 rows)
"""

import subprocess, sys, os, csv, math, re
from pathlib import Path

# Ensure deps
for pkg in ['pandas', 'numpy']:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

import pandas as pd
import numpy as np

BASE = Path('/Users/andreacrespo/CLAUDE/City101_ClaudeCode')

# ── Step 1: Load canonical 49 stations ──
freq_df = pd.read_csv(BASE / 'datasets/transit/city101_service_frequency_v2.csv')
canonical = freq_df[['name', 'station_id', 'lat_wgs84', 'lon_wgs84', 'trains_per_hour']].copy()
canonical.rename(columns={'name': 'station_name'}, inplace=True)
print(f"Canonical stations: {len(canonical)}")

# ── Step 2: Load existing ridership ──
ridership_df = pd.read_csv(BASE / 'datasets/transit/city101_ridership_sbb.csv')
print(f"Ridership SBB rows: {len(ridership_df)}")

# Load raw national passagierfrequenz (skip header row "passagierfrequenz")
raw_lines = open(BASE / 'source/passagierfrequenz.csv', 'r', encoding='utf-8').readlines()
# First line is "passagierfrequenz", actual headers on line 2
if raw_lines[0].strip() == 'passagierfrequenz':
    raw_lines = raw_lines[1:]

from io import StringIO
raw_df = pd.read_csv(StringIO(''.join(raw_lines)))
print(f"Raw passagierfrequenz rows: {len(raw_df)}")

# ── Step 3: Match ridership to canonical stations ──

def normalize_name(s):
    """Normalize station name for matching"""
    s = str(s).strip().strip('"')
    # Common substitutions
    s = s.replace('ü', 'u').replace('ä', 'a').replace('ö', 'o')
    s = s.replace('è', 'e').replace('é', 'e').replace('ê', 'e')
    s = s.replace('à', 'a').replace('â', 'a')
    s = s.replace('ô', 'o').replace('î', 'i')
    return s.lower().strip()

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# Build lookup from ridership data
matched = {}
unmatched = []

# Stations that must be estimated (not CFF mainline — spatial match would be misleading)
force_estimate = {
    'Lausanne-Flon': {'daily_avg': 35000, 'source': 'estimated_metro_hub', 'ci': 1.5,
                      'note': 'Metro M2/LEB hub, ~80K/day across all M2 stops'},
    'Vernier, Blandonnet': {'daily_avg': 5000, 'source': 'estimated_tram_hub', 'ci': 1.3,
                            'note': 'TPG tram hub, 84 departures/hr but not CFF rail'},
}

for _, station in canonical.iterrows():
    sname = station['station_name']
    snorm = normalize_name(sname)
    slat, slon = station['lat_wgs84'], station['lon_wgs84']

    # Force-estimate certain non-CFF stations
    if sname in force_estimate:
        est = force_estimate[sname]
        matched[sname] = {
            'daily_avg': est['daily_avg'],
            'workday_avg': None,
            'nonworkday_avg': None,
            'commuter_index': est['ci'],
            'uic': None,
            'source': est['source'],
            'year': 2024
        }
        print(f"  Force-estimated {sname}: {est['daily_avg']} daily ({est['source']} — {est['note']})")
        continue

    # Try exact name match in ridership_sbb
    exact = ridership_df[ridership_df['name'].apply(normalize_name) == snorm]
    if len(exact) > 0:
        row = exact.iloc[0]
        matched[sname] = {
            'daily_avg': row['daily_avg'],
            'workday_avg': row['workday_avg'],
            'nonworkday_avg': row['nonworkday_avg'],
            'commuter_index': row['commuter_index'],
            'uic': row['uic'],
            'source': f"sbb_passagierfrequenz_{int(row['year'])}",
            'year': int(row['year'])
        }
        continue

    # Try spatial match in ridership_sbb (within 0.5km)
    best_dist = 999
    best_row = None
    for _, rrow in ridership_df.iterrows():
        if pd.notna(rrow['lat_wgs84']) and pd.notna(rrow['lon_wgs84']):
            d = haversine_km(slat, slon, rrow['lat_wgs84'], rrow['lon_wgs84'])
            if d < best_dist:
                best_dist = d
                best_row = rrow
    if best_dist < 0.5 and best_row is not None:
        matched[sname] = {
            'daily_avg': best_row['daily_avg'],
            'workday_avg': best_row['workday_avg'],
            'nonworkday_avg': best_row['nonworkday_avg'],
            'commuter_index': best_row['commuter_index'],
            'uic': best_row['uic'],
            'source': f"sbb_passagierfrequenz_{int(best_row['year'])}",
            'year': int(best_row['year'])
        }
        continue

    # Try raw passagierfrequenz (name match)
    raw_match = raw_df[raw_df['bahnhof_gare_stazione'].apply(normalize_name) == snorm]
    if len(raw_match) > 0:
        row = raw_match.iloc[0]
        ci = row['dwv_tmjo_tfm'] / row['dnwv_tmjno_tmgnl'] if row['dnwv_tmjno_tmgnl'] > 0 else 1.0
        matched[sname] = {
            'daily_avg': row['dtv_tjm_tgm'],
            'workday_avg': row['dwv_tmjo_tfm'],
            'nonworkday_avg': row['dnwv_tmjno_tmgnl'],
            'commuter_index': round(ci, 2),
            'uic': row['uic'],
            'source': f"sbb_passagierfrequenz_{int(row['jahr_annee_anno'])}",
            'year': int(row['jahr_annee_anno'])
        }
        continue

    # Try partial name match in raw data
    partial_found = False
    sname_parts = snorm.split(',')[0].split('-')[0].split('(')[0].strip()
    if len(sname_parts) > 3:
        for _, rrow in raw_df.iterrows():
            rname = normalize_name(rrow['bahnhof_gare_stazione'])
            if sname_parts in rname or rname in snorm:
                ci = rrow['dwv_tmjo_tfm'] / rrow['dnwv_tmjno_tmgnl'] if rrow['dnwv_tmjno_tmgnl'] > 0 else 1.0
                matched[sname] = {
                    'daily_avg': rrow['dtv_tjm_tgm'],
                    'workday_avg': rrow['dwv_tmjo_tfm'],
                    'nonworkday_avg': rrow['dnwv_tmjno_tmgnl'],
                    'commuter_index': round(ci, 2),
                    'uic': rrow['uic'],
                    'source': f"sbb_passagierfrequenz_{int(rrow['jahr_annee_anno'])}",
                    'year': int(rrow['jahr_annee_anno'])
                }
                partial_found = True
                break

    # Try spatial match in raw passagierfrequenz
    if not partial_found:
        best_dist = 999
        best_raw = None
        for _, rrow in raw_df.iterrows():
            if pd.notna(rrow['geopos']) and str(rrow['geopos']).strip():
                try:
                    parts = str(rrow['geopos']).split(',')
                    rlat, rlon = float(parts[0].strip()), float(parts[1].strip())
                    d = haversine_km(slat, slon, rlat, rlon)
                    if d < best_dist:
                        best_dist = d
                        best_raw = rrow
                except:
                    pass
        if best_dist < 0.5 and best_raw is not None:
            ci = best_raw['dwv_tmjo_tfm'] / best_raw['dnwv_tmjno_tmgnl'] if best_raw['dnwv_tmjno_tmgnl'] > 0 else 1.0
            matched[sname] = {
                'daily_avg': best_raw['dtv_tjm_tgm'],
                'workday_avg': best_raw['dwv_tmjo_tfm'],
                'nonworkday_avg': best_raw['dnwv_tmjno_tmgnl'],
                'commuter_index': round(ci, 2),
                'uic': best_raw['uic'],
                'source': f"sbb_passagierfrequenz_{int(best_raw['jahr_annee_anno'])}",
                'year': int(best_raw['jahr_annee_anno'])
            }
        else:
            unmatched.append(sname)

print(f"\nMatched: {len(matched)}/{len(canonical)}")
print(f"Unmatched: {unmatched}")

# ── Step 4: Fill gaps for unmatched stations ──

# Build regression model: log(daily_pax) ~ log(trains_per_hour) using matched stations
known_data = []
for _, station in canonical.iterrows():
    sname = station['station_name']
    tph = station['trains_per_hour']
    if sname in matched and tph > 0:
        known_data.append((math.log(tph), math.log(matched[sname]['daily_avg'])))

if known_data:
    x = np.array([d[0] for d in known_data])
    y = np.array([d[1] for d in known_data])
    # Simple linear regression
    n = len(x)
    x_mean, y_mean = x.mean(), y.mean()
    ss_xy = np.sum((x - x_mean) * (y - y_mean))
    ss_xx = np.sum((x - x_mean) ** 2)
    slope = ss_xy / ss_xx
    intercept = y_mean - slope * x_mean
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y_mean) ** 2)
    r_squared = 1 - ss_res / ss_tot
    print(f"\nRegression: log(pax) = {slope:.3f} * log(tph) + {intercept:.3f}, R² = {r_squared:.3f}")

# Manual estimates for known special cases
manual_estimates = {
    'Lausanne-Flon': {'daily_avg': 35000, 'source': 'estimated_metro_hub', 'ci': 1.5},
    'Vernier, Blandonnet': {'daily_avg': 5000, 'source': 'estimated_tram_hub', 'ci': 1.3},
}

for sname in unmatched:
    tph_row = canonical[canonical['station_name'] == sname]
    tph = tph_row['trains_per_hour'].values[0] if len(tph_row) > 0 else 2.0

    if sname in manual_estimates:
        est = manual_estimates[sname]
        matched[sname] = {
            'daily_avg': est['daily_avg'],
            'workday_avg': None,
            'nonworkday_avg': None,
            'commuter_index': est['ci'],
            'uic': None,
            'source': est['source'],
            'year': 2024
        }
    else:
        # Use regression
        if tph > 0:
            log_pax = slope * math.log(tph) + intercept
            daily_est = round(math.exp(log_pax))
        else:
            daily_est = 50  # Minimum for stations with 0 frequency
        matched[sname] = {
            'daily_avg': daily_est,
            'workday_avg': None,
            'nonworkday_avg': None,
            'commuter_index': 1.0,  # default for unknowns
            'uic': None,
            'source': 'estimated_from_frequency_model',
            'year': 2024
        }
    print(f"  Estimated {sname}: {matched[sname]['daily_avg']} daily ({matched[sname]['source']})")

# ── Step 5: Model hourly distribution curves ──

def model_hourly_distribution(ci):
    """Generate 24 hourly percentages based on commuter index."""
    hours = np.arange(24)

    # Gaussian peaks
    morning_peak = np.exp(-0.5 * ((hours - 8.0) / 0.8) ** 2)
    evening_peak = np.exp(-0.5 * ((hours - 17.5) / 1.2) ** 2)
    base = np.ones(24)

    # Weight by commuter index
    if ci > 1.5:
        morning_w, evening_w, base_w = 0.30, 0.28, 0.42
    elif ci > 1.0:
        morning_w, evening_w, base_w = 0.24, 0.24, 0.52
    else:
        morning_w, evening_w, base_w = 0.15, 0.18, 0.67

    # Combine and normalize
    dist = (morning_w * morning_peak / morning_peak.sum() +
            evening_w * evening_peak / evening_peak.sum() +
            base_w * base / base.sum())

    # Normalize to sum to 1.0
    dist = dist / dist.sum()
    return dist

# ── Step 6: Build output DataFrame ──

rows = []
for _, station in canonical.iterrows():
    sname = station['station_name']
    data = matched.get(sname)
    if data is None:
        print(f"WARNING: No data for {sname}")
        continue

    ci = data['commuter_index'] if data['commuter_index'] is not None else 1.0
    hourly = model_hourly_distribution(ci)

    row = {
        'station_name': sname,
        'lat_wgs84': station['lat_wgs84'],
        'lon_wgs84': station['lon_wgs84'],
        'daily_avg': int(data['daily_avg']),
        'workday_avg': int(data['workday_avg']) if data['workday_avg'] is not None else '',
        'nonworkday_avg': int(data['nonworkday_avg']) if data['nonworkday_avg'] is not None else '',
        'commuter_index': ci,
        'source': data['source'],
        'year': data['year'],
        'uic': int(data['uic']) if data['uic'] is not None and not pd.isna(data['uic']) else '',
    }

    for h in range(24):
        row[f'pct_h{h:02d}'] = round(hourly[h], 6)

    row['peak_morning_pct'] = round(hourly[7] + hourly[8], 6)
    row['peak_evening_pct'] = round(hourly[16] + hourly[17] + hourly[18], 6)
    row['off_peak_pct'] = round(1.0 - row['peak_morning_pct'] - row['peak_evening_pct'], 6)

    rows.append(row)

out_df = pd.DataFrame(rows)
out_path = BASE / 'output/station_ridership.csv'
out_df.to_csv(out_path, index=False)
print(f"\n✓ Written: {out_path} ({len(out_df)} rows)")

# ── Step 7: Verification ──

print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

print(f"Row count: {len(out_df)} (expected: 49)")

# Check known stations
for check_name, check_val in [('Lausanne', 102800), ('Genève', 80600)]:
    row = out_df[out_df['station_name'] == check_name]
    if len(row) > 0:
        actual = row.iloc[0]['daily_avg']
        print(f"{check_name}: {actual} (expected ~{check_val}) {'✓' if abs(actual - check_val) < 1000 else '✗'}")

# Check hourly sums
pct_cols = [f'pct_h{h:02d}' for h in range(24)]
sums = out_df[pct_cols].sum(axis=1)
print(f"Hourly pct sums: min={sums.min():.6f}, max={sums.max():.6f} (should be 1.0)")

# Check high-CI stations
for sname in ['Lancy-Pont-Rouge', 'Renens VD']:
    row = out_df[out_df['station_name'] == sname]
    if len(row) > 0:
        pmp = row.iloc[0]['peak_morning_pct']
        ci = row.iloc[0]['commuter_index']
        print(f"{sname} (CI={ci}): peak_morning={pmp:.4f} {'✓ >0.25' if pmp > 0.25 else '✗ <0.25'}")

# Check low-CI stations
for sname in ['Montreux', 'Epesses']:
    row = out_df[out_df['station_name'] == sname]
    if len(row) > 0:
        pmp = row.iloc[0]['peak_morning_pct']
        ci = row.iloc[0]['commuter_index']
        print(f"{sname} (CI={ci}): peak_morning={pmp:.4f} {'✓ <0.18' if pmp < 0.18 else '✗ >0.18'}")

# Check no negatives
neg_count = (out_df[pct_cols] < 0).sum().sum()
print(f"Negative values: {neg_count} {'✓' if neg_count == 0 else '✗'}")

# Source breakdown
print(f"\nSource breakdown:")
for src, count in out_df['source'].value_counts().items():
    print(f"  {src}: {count}")

# ── Summary ──
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Sources read:")
print(f"  datasets/transit/city101_ridership_sbb.csv: {len(ridership_df)} rows")
print(f"  source/passagierfrequenz.csv: {len(raw_df)} rows")
print(f"  datasets/transit/city101_service_frequency_v2.csv: {len(freq_df)} rows")
print(f"\nStations matched directly: {len(matched) - len(unmatched)}")
print(f"Stations estimated: {len(unmatched)}")
if unmatched:
    print(f"Estimated stations: {', '.join(unmatched)}")
print(f"\nRegression model: log(pax) = {slope:.3f} * log(tph) + {intercept:.3f}, R² = {r_squared:.3f}")
print(f"\nOutput: {out_path}")
print(f"Rows: {len(out_df)}")
print(f"Columns: {list(out_df.columns)}")

# Top/bottom ridership
print(f"\nTop 5 by ridership:")
for _, r in out_df.nlargest(5, 'daily_avg').iterrows():
    print(f"  {r['station_name']}: {r['daily_avg']:,} daily ({r['source']})")
print(f"Bottom 5 by ridership:")
for _, r in out_df.nsmallest(5, 'daily_avg').iterrows():
    print(f"  {r['station_name']}: {r['daily_avg']:,} daily ({r['source']})")
