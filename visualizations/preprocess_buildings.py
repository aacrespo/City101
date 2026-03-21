"""
Preprocess City101 buildings: merge CSV classifications with GPKG geometries,
simplify, and export as GeoJSON for the breathing city visualization.

Usage:
    python preprocess_buildings.py

Output:
    data/buildings_polygons.geojson  (~40-50 MB)
    data/communes.geojson
"""
import geopandas as gpd
import pandas as pd
import json
import os
import sys
import time

# ─── PATHS ───
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_IN = os.path.join(os.path.dirname(BASE), "data_henna")
DATA_OUT = os.path.join(BASE, "data")
EXISTING_DATA = os.path.join(os.path.dirname(BASE), "CLAUDE CODE 20260305", "data")

# Prefer enriched CSV if available, fall back to original
CSV_ENRICHED = os.path.join(DATA_IN, "city101_buildings_enriched.csv")
CSV_ORIGINAL = os.path.join(DATA_IN, "city101_buildings_classified_v3.csv")
CSV_PATH = CSV_ENRICHED if os.path.exists(CSV_ENRICHED) else CSV_ORIGINAL
GPKG_PATH = os.path.join(DATA_IN, "City101_Buildings.gpkg")
COMMUNES_GPKG = os.path.join(DATA_IN, "City101_Communes.gpkg")

os.makedirs(DATA_OUT, exist_ok=True)

# ─── OCCUPANCY CURVE TYPES ───
# Each curve type maps to a 24-element array (one float per hour, 0.0-1.0)
# Key: (night_status, sector_group) -> curve_type_index
SECTOR_GROUPS = {
    'residential': 'residential',
    'infrastructure': 'infrastructure',
    'sports_fitness': 'sports',
    'commercial': 'commercial',
    'hospitality': 'hospitality',
    'education': 'education',
    'food_retail': 'commercial',
    'religious': 'religious',
    'healthcare': 'healthcare',
    'heritage': 'culture',
    'agriculture': 'agriculture',
    'office_professional': 'office',
    'public_services': 'office',
    'culture': 'culture',
    'commercial_industrial': 'industrial',
    'utility': 'infrastructure',
    'automotive': 'commercial',
    'fashion_retail': 'commercial',
    'tourism': 'hospitality',
    'craft_artisan': 'industrial',
    'entertainment': 'entertainment',
    'finance': 'office',
    'events': 'entertainment',
    'energy': 'infrastructure',
    'cemetery': 'infrastructure',
    'logistics': 'industrial',
    'technology': 'office',
}

# Occupancy curves indexed by curve type
CURVES = {
    # Residential: high at night, low during work hours
    'res': [0.95,0.97,0.98,0.98,0.95,0.85, 0.70,0.50,0.40,0.35,0.35,0.35,
            0.40,0.35,0.35,0.35,0.40,0.55, 0.65,0.75,0.82,0.88,0.92,0.94],

    # Standard daytime office work
    'day_office': [0,0,0,0,0,0, 0.02,0.20,0.70,0.90,0.95,0.90,
                   0.60,0.85,0.90,0.85,0.70,0.30, 0.10,0.02,0,0,0,0],

    # Education (schools, universities)
    'day_edu': [0,0,0,0,0,0, 0.05,0.60,0.90,0.95,0.95,0.85,
                0.50,0.80,0.90,0.85,0.60,0.15, 0.05,0.02,0,0,0,0],

    # Commercial/retail
    'day_retail': [0,0,0,0,0,0, 0.02,0.10,0.30,0.70,0.85,0.90,
                   0.85,0.90,0.95,0.90,0.85,0.70, 0.50,0.20,0,0,0,0],

    # Hospitality (restaurants, cafes) - day focused
    'day_hosp': [0,0,0,0,0,0, 0.05,0.15,0.30,0.50,0.70,0.85,
                 0.90,0.75,0.55,0.50,0.60,0.75, 0.85,0.70,0.40,0.10,0,0],

    # Industrial/agriculture
    'day_ind': [0,0,0,0,0,0, 0.10,0.50,0.80,0.90,0.90,0.85,
                0.60,0.80,0.85,0.80,0.60,0.20, 0.05,0,0,0,0,0],

    # Sports/fitness
    'day_sports': [0,0,0,0,0,0.05, 0.15,0.30,0.35,0.40,0.50,0.55,
                   0.45,0.50,0.55,0.60,0.70,0.80, 0.85,0.75,0.50,0.20,0.05,0],

    # Culture/heritage/religious
    'day_culture': [0,0,0,0,0,0, 0.02,0.10,0.30,0.60,0.75,0.80,
                    0.70,0.75,0.80,0.75,0.60,0.30, 0.10,0.02,0,0,0,0],

    # Healthcare (day-focused, but some baseline)
    'day_health': [0.10,0.10,0.08,0.08,0.10,0.15, 0.30,0.60,0.85,0.95,0.95,0.90,
                   0.75,0.85,0.90,0.85,0.70,0.40, 0.20,0.12,0.10,0.10,0.10,0.10],

    # Default daytime work
    'day_default': [0,0,0,0,0,0, 0.02,0.30,0.70,0.85,0.90,0.85,
                    0.60,0.80,0.85,0.80,0.60,0.30, 0.10,0.02,0,0,0,0],

    # Entertainment (evening-focused, day closed)
    'day_ent': [0,0,0,0,0,0, 0,0.05,0.10,0.15,0.25,0.35,
                0.30,0.30,0.35,0.45,0.60,0.75, 0.85,0.80,0.50,0.15,0,0],

    # 24h infrastructure (power, water, telecom)
    'h24_infra': [0.70]*24,

    # 24h healthcare (hospitals)
    'h24_health': [0.60,0.55,0.50,0.50,0.50,0.55, 0.65,0.80,0.90,0.95,0.95,0.90,
                   0.85,0.90,0.95,0.90,0.85,0.75, 0.70,0.65,0.60,0.60,0.60,0.60],

    # 24h commercial/convenience
    'h24_default': [0.50,0.45,0.40,0.35,0.35,0.40, 0.50,0.60,0.70,0.80,0.85,0.85,
                    0.80,0.80,0.85,0.85,0.80,0.75, 0.70,0.65,0.60,0.55,0.55,0.50],

    # Open late (restaurants, bars, entertainment)
    'late_hosp': [0.05,0.02,0.01,0,0,0, 0.02,0.05,0.10,0.20,0.35,0.50,
                  0.65,0.50,0.40,0.45,0.55,0.70, 0.85,0.95,0.95,0.90,0.70,0.30],

    # Open late retail/other
    'late_default': [0.02,0.01,0,0,0,0, 0.02,0.10,0.25,0.50,0.70,0.80,
                     0.75,0.80,0.85,0.85,0.80,0.75, 0.70,0.65,0.55,0.35,0.15,0.05],

    # Night shift (inverse of day)
    'night': [0.80,0.85,0.85,0.85,0.80,0.70, 0.40,0.20,0.15,0.10,0.10,0.10,
              0.10,0.10,0.10,0.10,0.15,0.25, 0.40,0.55,0.65,0.70,0.75,0.80],

    # Other/unknown (mild daytime presence)
    'other': [0,0,0,0,0,0, 0.10,0.30,0.50,0.70,0.80,0.85,
              0.70,0.80,0.85,0.80,0.60,0.30, 0.10,0,0,0,0,0],
}

# Map (night_status, sector_group) -> curve key
def get_curve_type(night_status, sector):
    sg = SECTOR_GROUPS.get(sector, 'default')

    if night_status == 'residential':
        return 'res'
    elif night_status == 'closed_at_night':
        mapping = {
            'office': 'day_office', 'education': 'day_edu',
            'commercial': 'day_retail', 'hospitality': 'day_hosp',
            'industrial': 'day_ind', 'agriculture': 'day_ind',
            'sports': 'day_sports', 'culture': 'day_culture',
            'religious': 'day_culture', 'healthcare': 'day_health',
            'entertainment': 'day_ent', 'infrastructure': 'day_default',
        }
        return mapping.get(sg, 'day_default')
    elif night_status == 'open_24h':
        mapping = {
            'infrastructure': 'h24_infra', 'healthcare': 'h24_health',
        }
        return mapping.get(sg, 'h24_default')
    elif night_status == 'open_late':
        if sg in ('hospitality', 'entertainment'):
            return 'late_hosp'
        return 'late_default'
    elif night_status == 'night_shift':
        return 'night'
    else:
        return 'other'


def main():
    t0 = time.time()

    # ─── 1. Load CSV ───
    print(f"Loading CSV: {os.path.basename(CSV_PATH)}...")
    csv_df = pd.read_csv(CSV_PATH)
    print(f"  CSV rows: {len(csv_df)}")

    # Use enriched night_status if available
    if 'night_status_enriched' in csv_df.columns:
        print("  Using enriched night_status column")
        csv_df['night_status'] = csv_df['night_status_enriched']

    # ─── 2. Load GPKG ───
    print("Loading buildings GPKG (this may take a minute)...")
    gdf = gpd.read_file(GPKG_PATH)
    print(f"  GPKG features: {len(gdf)}")

    assert len(csv_df) == len(gdf), f"Row count mismatch: CSV={len(csv_df)}, GPKG={len(gdf)}"

    # ─── 3. Join by row order ───
    print("Joining CSV data to GPKG by row order...")
    gdf['use_category'] = csv_df['use_category'].values
    gdf['sector'] = csv_df['sector'].values
    gdf['night_status'] = csv_df['night_status'].values
    gdf['area_m2'] = csv_df['area_m2'].values
    gdf['commune'] = csv_df['commune'].values
    gdf['profession_type'] = csv_df['profession_type'].values

    # ─── 4. Filter small buildings ───
    before = len(gdf)
    gdf = gdf[gdf['area_m2'] >= 30].copy()
    print(f"  Filtered >= 30 m²: {before} -> {len(gdf)} ({before - len(gdf)} removed)")

    # ─── 5. Reproject to WGS84 ───
    print("Reprojecting to WGS84...")
    gdf = gdf.to_crs(epsg=4326)

    # ─── 6. Drop Z coordinates and simplify geometries ───
    print("Dropping Z coordinates...")
    from shapely.ops import transform
    def drop_z(geom):
        return transform(lambda x, y, z=None: (x, y), geom)
    gdf.geometry = gdf.geometry.apply(drop_z)

    print("Simplifying geometries...")
    gdf.geometry = gdf.geometry.simplify(tolerance=0.00002)
    gdf = gdf[gdf.geometry.is_valid & ~gdf.geometry.is_empty].copy()
    print(f"  After cleanup: {len(gdf)} features")

    # ─── 7. Assign curve types ───
    print("Assigning occupancy curve types...")
    # Build curve type index
    curve_keys = list(CURVES.keys())
    curve_idx = {k: i for i, k in enumerate(curve_keys)}

    # Encode categorical columns as numeric
    cat_map = {'residential': 1, 'work': 2, 'other': 0}
    ns_map = {'residential': 0, 'closed_at_night': 1, 'open_24h': 2, 'open_late': 3, 'night_shift': 4}

    # Build sector index
    all_sectors = sorted(csv_df['sector'].dropna().unique())
    sector_idx = {s: i for i, s in enumerate(all_sectors)}

    gdf['c'] = gdf['use_category'].map(cat_map).fillna(0).astype(int)
    gdf['n'] = gdf['night_status'].map(ns_map).fillna(5).astype(int)
    gdf['s'] = gdf['sector'].map(sector_idx).fillna(0).astype(int)
    gdf['a'] = gdf['area_m2'].clip(upper=65535).astype(int)

    # Compute curve type for each building
    gdf['ct'] = gdf.apply(
        lambda r: curve_idx[get_curve_type(r['night_status'], r['sector'])], axis=1
    )

    # Build commune index
    all_communes = sorted(gdf['commune'].dropna().unique())
    commune_idx = {c: i for i, c in enumerate(all_communes)}
    gdf['ci'] = gdf['commune'].map(commune_idx).fillna(0).astype(int)

    # ─── 8. Export GeoJSON ───
    print("Exporting GeoJSON...")
    export = gdf[['geometry', 'c', 'n', 's', 'a', 'ct', 'ci']].copy()
    export = export.reset_index(drop=True)

    out_path = os.path.join(DATA_OUT, "buildings_polygons.geojson")
    export.to_file(out_path, driver="GeoJSON", coordinate_precision=5)
    fsize = os.path.getsize(out_path) / (1024 * 1024)
    print(f"  Written: {out_path} ({fsize:.1f} MB)")

    # ─── 9. Export metadata JSON (curves, sectors, communes) ───
    meta = {
        'curves': {k: CURVES[k] for k in curve_keys},
        'curve_keys': curve_keys,
        'sectors': all_sectors,
        'communes': all_communes,
        'cat_labels': {0: 'Other', 1: 'Residential', 2: 'Work'},
        'ns_labels': {0: 'Residential', 1: 'Closed at night', 2: 'Open 24h', 3: 'Open late', 4: 'Night shift'},
        'stats': {
            'total_buildings': len(export),
            'residential': int((export['c'] == 1).sum()),
            'work': int((export['c'] == 2).sum()),
            'other': int((export['c'] == 0).sum()),
        }
    }
    meta_path = os.path.join(DATA_OUT, "building_meta.json")
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=1)
    print(f"  Written: {meta_path}")

    # ─── 10. Copy/convert communes ───
    # Check if communes GeoJSON exists already
    existing_communes = os.path.join(EXISTING_DATA, "communes.geojson")
    out_communes = os.path.join(DATA_OUT, "communes.geojson")
    if os.path.exists(existing_communes):
        import shutil
        shutil.copy2(existing_communes, out_communes)
        print(f"  Copied communes from existing: {out_communes}")
    else:
        print("  Converting communes GPKG...")
        communes = gpd.read_file(COMMUNES_GPKG)
        communes = communes.to_crs(epsg=4326)
        communes.to_file(out_communes, driver="GeoJSON", coordinate_precision=5)
        print(f"  Written: {out_communes}")

    # Copy population_24h if exists
    existing_pop = os.path.join(EXISTING_DATA, "population_24h.json")
    out_pop = os.path.join(DATA_OUT, "population_24h.json")
    if os.path.exists(existing_pop):
        import shutil
        shutil.copy2(existing_pop, out_pop)
        print(f"  Copied population_24h from existing: {out_pop}")

    # ─── Summary ───
    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print(f"PREPROCESSING COMPLETE ({elapsed:.1f}s)")
    print(f"{'='*60}")
    print(f"  Buildings: {len(export):,}")
    print(f"    Residential: {meta['stats']['residential']:,}")
    print(f"    Work: {meta['stats']['work']:,}")
    print(f"    Other: {meta['stats']['other']:,}")
    print(f"  Curve types: {len(curve_keys)}")
    print(f"  Sectors: {len(all_sectors)}")
    print(f"  Communes: {len(all_communes)}")
    print(f"\n  Output files:")
    for f_name in os.listdir(DATA_OUT):
        fp = os.path.join(DATA_OUT, f_name)
        sz = os.path.getsize(fp)
        if sz > 1024*1024:
            print(f"    {f_name}: {sz/1024/1024:.1f} MB")
        else:
            print(f"    {f_name}: {sz/1024:.0f} KB")


if __name__ == '__main__':
    main()
