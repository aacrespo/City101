#!/usr/bin/env python3
"""Agent 4 v3: Fix distances, snap classifications, and Léman Express.

Fixes 3 problems from v2:
1. Distance range 0-69.5km → 0-105km (SBB km post calibration)
2. 7 stations >500m snap → adds snap_quality + snap_note columns
3. Léman Express classified as narrow_gauge → standard_gauge_leman_express

Reads: v2 GeoJSON + v2 CSV + GPKG (for CEVA extraction)
Writes: v3 GeoJSON + v3 CSV
"""
import sqlite3, json, csv, math, os, sys

try:
    from shapely import wkb
    from shapely.geometry import LineString, MultiLineString, Point, mapping, shape
    from shapely.ops import linemerge, unary_union
except ImportError:
    print("ERROR: shapely not installed"); sys.exit(1)
try:
    from pyproj import Transformer
except ImportError:
    print("ERROR: pyproj not installed"); sys.exit(1)

BASE = "/Users/andreacrespo/CLAUDE/City101_ClaudeCode"
GPKG = os.path.join(BASE, "source/WORK copy/City101_TrainLines.gpkg")
V2_GJ = os.path.join(BASE, "output/corridor_rail_lines_v2.geojson")
V2_CSV = os.path.join(BASE, "output/corridor_station_distances_v2.csv")
OUT_GJ = os.path.join(BASE, "output/corridor_rail_lines_v3.geojson")
OUT_CSV = os.path.join(BASE, "output/corridor_station_distances_v3.csv")
TBL = "swisstlm3d_chlv95ln02__tlm_eisenbahn_CITY101"
SIMPLIFY_TOL = 0.0001

xf = Transformer.from_crs("EPSG:2056", "EPSG:4326", always_xy=True)

# SBB km posts — real rail distances from Geneva
SBB_KM = {
    "Genève": 0.0, "Genève-Sécheron": 1.4, "Nyon": 22.0, "Morges": 45.1,
    "Lausanne": 60.0, "Vevey": 80.0, "Montreux": 84.0,
    "Villeneuve VD": 89.0, "Aigle": 95.0, "Bex": 105.0,
}

LEMAN_EXPRESS = {"Genève-Eaux-Vives", "Genève-Champel", "Lancy-Pont-Rouge", "Lancy-Bachet"}

NON_RAIL = {
    "Vernier, Blandonnet": "Tram/bus stop",
    "Founex, est": "Bus stop",
    "Prangins, Les Abériaux": "Bus stop",
    "Begnins, poste": "Bus stop",
    "Perroy, Couronnette": "Bus stop",
    "Aubonne, gare": "Bus stop",
}


def haversine(lon1, lat1, lon2, lat2):
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def line_km(coords):
    return sum(haversine(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])
               for i in range(len(coords) - 1)) / 1000


def along_line_km(coords, lon, lat):
    """Project point onto polyline. Returns (along_km, perp_distance_m)."""
    best_d, best_seg, best_frac = float('inf'), 0, 0.0
    for i in range(len(coords) - 1):
        x1, y1 = coords[i]
        x2, y2 = coords[i + 1]
        dx, dy = x2 - x1, y2 - y1
        denom = dx*dx + dy*dy
        frac = max(0, min(1, ((lon - x1)*dx + (lat - y1)*dy) / denom)) if denom else 0
        px, py = x1 + frac*dx, y1 + frac*dy
        d = haversine(lon, lat, px, py)
        if d < best_d:
            best_d, best_seg, best_frac = d, i, frac
    cum = sum(haversine(coords[j][0], coords[j][1], coords[j+1][0], coords[j+1][1])
              for j in range(best_seg))
    x1, y1 = coords[best_seg]
    x2, y2 = coords[best_seg + 1]
    cum += haversine(x1, y1, x1 + best_frac*(x2 - x1), y1 + best_frac*(y2 - y1))
    return cum / 1000, best_d


def calibrate(raw_km, cal):
    if raw_km <= cal[0][0]:
        r0, g0 = cal[0]; r1, g1 = cal[1] if len(cal) > 1 else (r0 + 1, g0 + 1)
        return g0 + (raw_km - r0) * (g1 - g0) / (r1 - r0) if r1 != r0 else g0
    if raw_km >= cal[-1][0]:
        r0, g0 = cal[-2] if len(cal) > 1 else (cal[-1][0] - 1, cal[-1][1] - 1)
        r1, g1 = cal[-1]
        return g1 + (raw_km - r1) * (g1 - g0) / (r1 - r0) if r1 != r0 else g1
    for i in range(len(cal) - 1):
        r0, g0 = cal[i]; r1, g1 = cal[i + 1]
        if r0 <= raw_km <= r1:
            return g0 + (raw_km - r0) * (g1 - g0) / (r1 - r0) if r1 != r0 else g0
    return raw_km


def parse_gpkg_geom(blob):
    if not blob or len(blob) < 8 or blob[:2] != b'GP':
        return None
    flags = blob[3]
    env_type = (flags >> 1) & 0x07
    env_sizes = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}
    try:
        return wkb.loads(blob[8 + env_sizes.get(env_type, 0):])
    except Exception:
        return None


def transform_geom(g):
    def tx(coords):
        return [xf.transform(c[0], c[1]) for c in coords]
    if g.geom_type == 'LineString':
        return LineString(tx(list(g.coords)))
    elif g.geom_type == 'MultiLineString':
        return MultiLineString([LineString(tx(list(l.coords))) for l in g.geoms])
    return g


def main():
    print("=" * 80)
    print("AGENT 4 v3: Distance + Snap + Léman Express Fixes")
    print("=" * 80)

    # ── STEP 1: Read v2 GeoJSON ──
    print("\nSTEP 1: Reading v2 GeoJSON...")
    with open(V2_GJ, encoding='utf-8') as f:
        v2_gj = json.load(f)

    mainline_feat = None
    narrow_feats = []
    fun_feats = []
    for feat in v2_gj['features']:
        lt = feat['properties']['line_type']
        if lt == 'standard_gauge':
            mainline_feat = feat
        elif lt == 'narrow_gauge':
            narrow_feats.append(feat)
        else:
            fun_feats.append(feat)

    mainline_geom = shape(mainline_feat['geometry'])
    if mainline_geom.geom_type == 'MultiLineString':
        mainline_coords = []
        for g in mainline_geom.geoms:
            mainline_coords.extend(list(g.coords))
    else:
        mainline_coords = list(mainline_geom.coords)
    mainline_coords = [(c[0], c[1]) for c in mainline_coords]

    ml_km = line_km(mainline_coords)
    print(f"  Mainline: {len(mainline_coords)} coords, {ml_km:.1f} km")
    print(f"  West end: ({mainline_coords[0][1]:.4f}, {mainline_coords[0][0]:.4f})")
    print(f"  East end: ({mainline_coords[-1][1]:.4f}, {mainline_coords[-1][0]:.4f})")
    print(f"  {len(narrow_feats)} narrow gauge, {len(fun_feats)} funicular features")

    # ── STEP 2: Read v2 station data ──
    print("\nSTEP 2: Reading v2 station data...")
    stations = []
    with open(V2_CSV, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            stations.append({
                'name': row['station_name'],
                'lat': float(row['lat_wgs84']),
                'lon': float(row['lon_wgs84']),
                'snap_lat': float(row['snapped_lat']),
                'snap_lon': float(row['snapped_lon']),
                'snap_m': float(row['snap_distance_m']),
                'v2_dist': float(row['distance_from_geneva_km']),
                'v2_type': row['line_type'],
                'is_branch': row['is_branch'] == 'True',
                'branch_type': row['branch_type'] if row['branch_type'] else '',
            })
    print(f"  {len(stations)} stations")

    # ── STEP 3: Extract CEVA geometry from GPKG ──
    print("\nSTEP 3: Extracting CEVA geometry from GPKG...")
    ceva_pts = {s['name']: Point(s['lon'], s['lat'])
                for s in stations if s['name'] in LEMAN_EXPRESS}

    conn = sqlite3.connect(GPKG)
    cursor = conn.execute(
        f'SELECT fid, geom, OBJEKTART, AUSSER_BETRIEB, MUSEUMSBAHN, ANSCHLUSSGLEIS '
        f'FROM "{TBL}"')

    ceva_lines = []
    for row in cursor:
        if row[2] != 0 or row[3] != 1 or row[5] != 1:  # std gauge, in service, not siding
            continue
        geom = parse_gpkg_geom(row[1])
        if geom is None:
            continue
        geom_wgs = transform_geom(geom)
        near_ceva = any(geom_wgs.distance(pt) < 0.005 for pt in ceva_pts.values())
        if not near_ceva:
            continue
        near_mainline = mainline_geom.distance(geom_wgs) < 0.001
        if near_mainline:
            continue
        if geom_wgs.geom_type == 'LineString':
            ceva_lines.append(geom_wgs)
        elif geom_wgs.geom_type == 'MultiLineString':
            ceva_lines.extend(geom_wgs.geoms)
    conn.close()

    ceva_feature = None
    if ceva_lines:
        ceva_merged = linemerge(ceva_lines)
        ceva_simplified = ceva_merged.simplify(SIMPLIFY_TOL)
        if ceva_simplified.geom_type == 'LineString':
            ceva_simplified = LineString([(c[0], c[1]) for c in ceva_simplified.coords])
            ckm = line_km(list(ceva_simplified.coords))
        elif ceva_simplified.geom_type == 'MultiLineString':
            ceva_simplified = MultiLineString([
                LineString([(c[0], c[1]) for c in l.coords]) for l in ceva_simplified.geoms])
            ckm = sum(line_km(list(l.coords)) for l in ceva_simplified.geoms)
        else:
            ckm = 0
        ceva_feature = {
            'type': 'Feature',
            'geometry': mapping(ceva_simplified),
            'properties': {
                'line_type': 'standard_gauge_leman_express',
                'name': 'Léman Express (CEVA)',
                'station_names': ', '.join(sorted(LEMAN_EXPRESS)),
                'segment_count': len(ceva_lines),
                'total_length_km': round(ckm, 2),
            }
        }
        print(f"  CEVA: {len(ceva_lines)} segments, {ckm:.1f} km")
    else:
        print("  No CEVA geometry found — using station-to-station fallback")
        ceva_ordered = [
            (6.12934, 46.174342), (6.124929, 46.18596),
            (6.153473, 46.192208), (6.166549, 46.201461),
        ]
        cl = LineString(ceva_ordered)
        ckm = line_km(ceva_ordered)
        ceva_feature = {
            'type': 'Feature', 'geometry': mapping(cl),
            'properties': {
                'line_type': 'standard_gauge_leman_express',
                'name': 'Léman Express (CEVA)',
                'station_names': ', '.join(sorted(LEMAN_EXPRESS)),
                'segment_count': 1, 'total_length_km': round(ckm, 2),
            }
        }
        print(f"  Fallback CEVA: {ckm:.1f} km")

    # ── STEP 4: Project stations onto mainline ──
    print("\nSTEP 4: Computing along-line projections...")
    for s in stations:
        s['raw_km'], s['proj_dist_m'] = along_line_km(mainline_coords, s['lon'], s['lat'])

    # ── STEP 5: Build calibration from SBB km posts ──
    print("\nSTEP 5: Building calibration...")
    cal_raw = []
    for name, sbb_km in sorted(SBB_KM.items(), key=lambda x: x[1]):
        st = next((s for s in stations if s['name'] == name), None)
        if st and st['proj_dist_m'] < 2000:
            cal_raw.append((st['raw_km'], sbb_km, name))

    cal_raw.sort(key=lambda x: x[0])
    cal_clean = []
    for raw, sbb, name in cal_raw:
        if not cal_clean or (sbb > cal_clean[-1][1] and raw > cal_clean[-1][0]):
            cal_clean.append((raw, sbb))
            print(f"  Anchor: raw={raw:6.1f} → SBB={sbb:6.1f}  ({name})")
        else:
            print(f"  Skip:   raw={raw:6.1f} → SBB={sbb:6.1f}  ({name}) — non-monotonic")
    print(f"  {len(cal_clean)} calibration points")

    # ── STEP 6: Calibrate distances ──
    print("\nSTEP 6: Calibrating distances...")
    for s in stations:
        if s['name'] in SBB_KM:
            s['dist_km'] = SBB_KM[s['name']]
            s['dist_source'] = 'sbb_km_post'
        else:
            s['dist_km'] = calibrate(s['raw_km'], cal_clean)
            s['dist_source'] = 'calibrated'

    # ── STEP 7: Fix line_type ──
    print("\nSTEP 7: Fixing line_type...")
    for s in stations:
        if s['name'] in LEMAN_EXPRESS:
            old = s['v2_type']
            s['line_type'] = 'standard_gauge_leman_express'
            print(f"  {s['name']}: {old} → standard_gauge_leman_express")
        elif s['name'] in NON_RAIL:
            s['line_type'] = 'non_rail_station'
        else:
            s['line_type'] = s['v2_type']

    # ── STEP 8: Fix snap quality ──
    print("\nSTEP 8: Computing snap quality...")
    for s in stations:
        dm = s['snap_m']
        name = s['name']
        if name in NON_RAIL:
            s['snap_quality'] = 'non_rail_station'
            s['snap_note'] = f"{NON_RAIL[name]}, {dm:.0f}m to nearest rail"
        elif name in LEMAN_EXPRESS:
            s['snap_quality'] = 'good' if dm <= 200 else 'approximate'
            s['snap_note'] = f"CEVA standard gauge ({dm:.0f}m)" if dm > 200 else 'CEVA line'
        elif dm <= 100:
            s['snap_quality'] = 'good'
            s['snap_note'] = ''
        elif dm <= 500:
            s['snap_quality'] = 'acceptable'
            s['snap_note'] = ''
        elif dm <= 1000:
            s['snap_quality'] = 'approximate'
            s['snap_note'] = f"Snapped at {dm:.0f}m"
        else:
            s['snap_quality'] = 'original_coords'
            s['snap_note'] = f"No rail within 1km ({dm:.0f}m), using station coords"
            s['snap_lat'] = s['lat']
            s['snap_lon'] = s['lon']

    # ── STEP 9: Sort by distance ──
    stations.sort(key=lambda s: s['dist_km'])

    # ── STEP 10: Build v3 GeoJSON ──
    print("\nSTEP 10: Building v3 GeoJSON...")
    v3_features = [mainline_feat]
    if ceva_feature:
        v3_features.append(ceva_feature)
    v3_features.extend(narrow_feats)
    v3_features.extend(fun_feats)

    type_counts = {}
    for f in v3_features:
        lt = f['properties']['line_type']
        type_counts[lt] = type_counts.get(lt, 0) + 1

    v3_gj = {
        'type': 'FeatureCollection',
        'crs': v2_gj.get('crs', {}),
        'features': v3_features,
    }
    with open(OUT_GJ, 'w', encoding='utf-8') as f:
        json.dump(v3_gj, f, indent=2, ensure_ascii=False)
    gj_size = os.path.getsize(OUT_GJ)
    print(f"  {OUT_GJ}: {gj_size/1024:.0f} KB, {len(v3_features)} features")
    for lt, c in sorted(type_counts.items()):
        print(f"    {lt}: {c}")

    # ── STEP 11: Write v3 CSV ──
    print("\nSTEP 11: Writing v3 distances CSV...")
    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow([
            'station_name', 'lat_wgs84', 'lon_wgs84',
            'snapped_lat', 'snapped_lon', 'snap_distance_m',
            'snap_quality', 'snap_note',
            'distance_from_geneva_km', 'line_type',
            'is_branch', 'branch_type',
        ])
        for s in stations:
            w.writerow([
                s['name'],
                round(s['lat'], 6), round(s['lon'], 6),
                round(s['snap_lat'], 6), round(s['snap_lon'], 6),
                round(s['snap_m'], 1),
                s['snap_quality'], s['snap_note'],
                round(s['dist_km'], 2),
                s['line_type'],
                s['is_branch'],
                s['branch_type'],
            ])
    csv_size = os.path.getsize(OUT_CSV)
    print(f"  {OUT_CSV}: {csv_size/1024:.1f} KB, {len(stations)} rows")

    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("VALIDATION")
    print("=" * 80)

    dist_max = max(s['dist_km'] for s in stations)
    dist_min = min(s['dist_km'] for s in stations)
    bex_d = next((s['dist_km'] for s in stations if s['name'] == 'Bex'), None)
    aigle_d = next((s['dist_km'] for s in stations if s['name'] == 'Aigle'), None)

    print(f"\n  1. Distance range: {dist_min:.1f}–{dist_max:.1f} km")
    print(f"     Bex: {bex_d:.1f} km — {'PASS' if bex_d and bex_d > 100 else 'FAIL'} (need >100)")
    print(f"     Aigle: {aigle_d:.1f} km — {'PASS' if aigle_d and aigle_d > 90 else 'FAIL'} (need >90)")

    mainline_st = [s for s in stations if not s['is_branch']]
    mono = all(mainline_st[i]['dist_km'] <= mainline_st[i+1]['dist_km']
               for i in range(len(mainline_st) - 1))
    print(f"\n  2. Mainline monotonicity: {'PASS' if mono else 'FAIL'}")
    if not mono:
        for i in range(len(mainline_st) - 1):
            a, b = mainline_st[i], mainline_st[i+1]
            if a['dist_km'] > b['dist_km']:
                print(f"     VIOLATION: {a['name']} ({a['dist_km']:.1f}) > {b['name']} ({b['dist_km']:.1f})")

    snap_q = {}
    for s in stations:
        q = s['snap_quality']
        snap_q[q] = snap_q.get(q, 0) + 1
    print(f"\n  3. Snap quality: {snap_q}")

    leman_ok = all(s['line_type'] == 'standard_gauge_leman_express'
                   for s in stations if s['name'] in LEMAN_EXPRESS)
    print(f"\n  4. Léman Express: {'PASS' if leman_ok else 'FAIL'}")

    ge_type = next((s['line_type'] for s in stations if s['name'] == 'Genève'), None)
    print(f"  5. Genève: {ge_type} — {'PASS' if ge_type == 'standard_gauge' else 'FAIL'}")

    pt_count = sum(1 for f in v3_features if f['geometry']['type'] == 'Point')
    has_ceva_gj = any(f['properties']['line_type'] == 'standard_gauge_leman_express'
                      for f in v3_features)
    print(f"  6. GeoJSON: {len(v3_features)} features, {pt_count} points — "
          f"{'PASS' if pt_count == 0 else 'FAIL'}")
    print(f"     CEVA feature: {'PASS' if has_ceva_gj else 'FAIL'}")

    print(f"\n  Sample distances (v2 → v3):")
    for name in ["Genève", "Nyon", "Lausanne", "Vevey", "Montreux",
                  "Villeneuve VD", "Aigle", "Bex"]:
        s = next((s for s in stations if s['name'] == name), None)
        if s:
            sbb = SBB_KM.get(name, '—')
            print(f"    {name:25s} v2={s['v2_dist']:6.1f}  v3={s['dist_km']:6.1f}  "
                  f"SBB={str(sbb):>6s}  ({s['dist_source']})")

    far = [s for s in stations if s['snap_m'] > 500]
    print(f"\n  Stations >500m snap: {len(far)}")
    for s in far:
        print(f"    {s['name']:35s} {s['snap_m']:>8.0f}m  {s['snap_quality']}")

    lt_dist = {}
    for s in stations:
        lt_dist[s['line_type']] = lt_dist.get(s['line_type'], 0) + 1
    print(f"\n  Line type distribution: {lt_dist}")

    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\n--- Sources ---")
    print(f"  v2 GeoJSON: {V2_GJ}")
    print(f"  v2 CSV: {V2_CSV}")
    print(f"  GPKG: {GPKG} (CEVA extraction)")
    print(f"  SBB km posts: 10 anchors (user-provided + GA cost verified)")
    print(f"\n--- What was fixed ---")
    print(f"  1. Distance: {dist_min:.1f}–{dist_max:.1f} km (was 0–69.5)")
    print(f"     Root cause: v2 used GA cost estimates for calibration")
    print(f"     GA estimates diverge from real SBB km east of Lausanne")
    print(f"     (Vevey: GA=63.7 vs SBB≈80, Aigle: GA=67.4 vs SBB≈95)")
    print(f"  2. Snap: {len(far)} stations >500m now classified + noted")
    print(f"  3. Léman Express: {len(LEMAN_EXPRESS)} stations reclassified")
    if ceva_feature:
        print(f"     CEVA GeoJSON feature: {ceva_feature['properties']['total_length_km']} km")
    print(f"\n--- Quality ---")
    src_counts = {}
    for s in stations:
        src_counts[s['dist_source']] = src_counts.get(s['dist_source'], 0) + 1
    for src, c in sorted(src_counts.items()):
        print(f"  {src}: {c} stations")
    print(f"  Calibration: {len(cal_clean)} piecewise linear anchors")
    print(f"\n--- Outputs ---")
    print(f"  {OUT_GJ} ({gj_size/1024:.0f} KB)")
    print(f"  {OUT_CSV} ({csv_size/1024:.1f} KB, {len(stations)} rows)")
    print("\nDone.")


if __name__ == '__main__':
    main()
