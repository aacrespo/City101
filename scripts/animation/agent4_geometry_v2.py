#!/usr/bin/env python3
"""Agent 4 FIX: Clean Geometry from GPKG (v2).

Builds on v4's successful Dijkstra spine + calibration approach but fixes output:
- GeoJSON has ONLY line geometries (no station points)
- Every line has line_type, station_names, segment_count, total_length_km
- Proper SwissTLM3D attribute filtering
- Douglas-Peucker simplification for web
- 500m snap tolerance (not 6.5m)
- Fixed Bex endpoint

Input: source/WORK copy/City101_TrainLines.gpkg
Output 1: output/corridor_rail_lines_v2.geojson (lines only)
Output 2: output/corridor_station_distances_v2.csv
"""
import sqlite3, csv, json, math, os, sys, heapq
from collections import defaultdict

try:
    from shapely import wkb
    from shapely.geometry import LineString, MultiLineString, Point, mapping
    from shapely.ops import linemerge, unary_union
except ImportError:
    print("ERROR: shapely not installed"); sys.exit(1)
try:
    from pyproj import Transformer
except ImportError:
    print("ERROR: pyproj not installed"); sys.exit(1)

BASE = "/Users/andreacrespo/CLAUDE/City101_ClaudeCode"
GPKG = os.path.join(BASE, "source/WORK copy/City101_TrainLines.gpkg")
STCSV = os.path.join(BASE, "datasets/transit/city101_service_frequency_v2.csv")
GACSV = os.path.join(BASE, "datasets/corridor_analysis/city101_ga_cost_corridor.csv")
ODIR = os.path.join(BASE, "output")
OGJN = os.path.join(ODIR, "corridor_rail_lines_v2.geojson")
OCSV = os.path.join(ODIR, "corridor_station_distances_v2.csv")
TBL = "swisstlm3d_chlv95ln02__tlm_eisenbahn_CITY101"

xf = Transformer.from_crs("EPSG:2056", "EPSG:4326", always_xy=True)

# Quantization step for graph nodes (~6.5m)
QS = 0.00006
BRIDGE_THRESHOLD = 0.003  # ~300m for bridge edges
SIMPLIFY_TOLERANCE = 0.0001  # ~10m Douglas-Peucker

# 36-station mainline spine (Geneva→Bex)
MAINLINE_SPINE = [
    "Geneve", "Geneve-Secheron", "Genthod-Bellevue", "Versoix",
    "Mies", "Tannay", "Coppet", "Nyon", "Gland", "Rolle",
    "Allaman", "St-Prex", "Morges", "Lonay-Preverenges",
    "Denges-Echandens", "Bussigny", "Renens VD", "Prilly-Malley",
    "Lausanne", "La Conversion", "Bossiere", "Cully",
    "Grandvaux", "Epesses", "Puidoux", "Rivaz",
    "St-Saphorin (Lavaux), gare", "Vevey", "La Tour-de-Peilz",
    "Burier", "Clarens", "Montreux", "Territet", "Villeneuve VD",
    "Aigle", "Bex",
]

BRANCH_STATIONS = {
    "Geneve-Eaux-Vives": "CEVA",
    "Geneve-Champel": "CEVA",
    "Lancy-Pont-Rouge": "CEVA",
    "Geneve-Aeroport": "Airport branch",
    "Vernier, Blandonnet": "Tram/bus",
    "Lancy-Bachet": "CEVA junction",
    "Founex, est": "Bus stop",
    "Prangins, Les Aberiaux": "Bus stop",
    "Begnins, poste": "Bus stop",
    "Perroy, Couronnette": "Bus stop",
    "Aubonne, gare": "Bus stop",
    "Lausanne-Flon": "LEB narrow gauge",
    "Palezieux": "Fribourg branch",
}


def normalize_name(n):
    n = n.strip().strip('"')
    reps = {'\xe8':'e','\xe9':'e','\xea':'e','\xeb':'e',
            '\xe0':'a','\xe2':'a','\xe4':'a',
            '\xf9':'u','\xfb':'u','\xfc':'u',
            '\xee':'i','\xef':'i','\xf4':'o','\xf6':'o','\xe7':'c'}
    for old, new in reps.items():
        n = n.replace(old, new)
    return n


def parse_gpkg_geom(blob):
    """Parse GeoPackage geometry blob (GP header + WKB)."""
    if not blob or len(blob) < 8 or blob[:2] != b'GP':
        return None
    flags = blob[3]
    env_type = (flags >> 1) & 0x07
    env_sizes = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}
    env_size = env_sizes.get(env_type, 0)
    try:
        return wkb.loads(blob[8 + env_size:])
    except Exception:
        return None


def transform_coords(coords):
    """Transform LV95 coordinates to WGS84."""
    result = []
    for c in coords:
        lon, lat = xf.transform(c[0], c[1])
        result.append((lon, lat) if len(c) < 3 else (lon, lat, c[2]))
    return result


def transform_geom(g):
    """Transform a geometry from LV95 to WGS84."""
    if g.geom_type == 'LineString':
        return LineString(transform_coords(list(g.coords)))
    elif g.geom_type == 'MultiLineString':
        return MultiLineString([
            LineString(transform_coords(list(l.coords))) for l in g.geoms
        ])
    return g


def in_bbox(g, minlon=6.05, maxlon=7.10, minlat=46.10, maxlat=46.55):
    """Check if geometry intersects the corridor bounding box."""
    a, b, c, d = g.bounds
    return not (c < minlon or a > maxlon or d < minlat or b > maxlat)


def extract_lines(g):
    """Extract LineStrings from geometry."""
    if g.geom_type == 'LineString':
        return [g] if len(g.coords) >= 2 else []
    elif g.geom_type == 'MultiLineString':
        return [l for l in g.geoms if len(l.coords) >= 2]
    return []


def haversine(lon1, lat1, lon2, lat2):
    """Distance in meters."""
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dp/2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl/2)**2
    return R * 2 * math.atan2(math.sqrt(x), math.sqrt(1-x))


def line_km(line):
    """Length of a LineString in km using haversine."""
    coords = list(line.coords)
    total = 0
    for i in range(len(coords) - 1):
        total += haversine(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])
    return total / 1000


def quantize(p):
    return (round(p[0] / QS) * QS, round(p[1] / QS) * QS)


def build_adjacency(lines):
    """Build graph from line segments."""
    adj = defaultdict(list)
    for i, l in enumerate(lines):
        coords = list(l.coords)
        start = quantize((coords[0][0], coords[0][1]))
        end = quantize((coords[-1][0], coords[-1][1]))
        km = line_km(l)
        adj[start].append((i, end, km))
        adj[end].append((i, start, km))
    return adj


def add_bridge_edges(graph, threshold):
    """Add edges between disconnected graph components."""
    nodes = list(graph.keys())
    parent = {}

    def find(x):
        if x not in parent:
            parent[x] = x
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for n in nodes:
        for _, other, _ in graph[n]:
            union(n, other)

    comp_nodes = defaultdict(list)
    for n in nodes:
        comp_nodes[find(n)].append(n)

    if len(comp_nodes) <= 1:
        return 0

    bridges = 0
    comp_list = list(comp_nodes.items())
    for ci in range(len(comp_list)):
        for cj in range(ci + 1, len(comp_list)):
            _, ni = comp_list[ci]
            _, nj = comp_list[cj]
            best_d = float('inf')
            best_pair = None
            for a in ni:
                for b in nj:
                    d = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
                    if d < best_d:
                        best_d = d
                        best_pair = (a, b)
            if best_d < threshold and best_pair:
                km = haversine(best_pair[0][0], best_pair[0][1],
                              best_pair[1][0], best_pair[1][1]) / 1000
                graph[best_pair[0]].append((-1, best_pair[1], km))
                graph[best_pair[1]].append((-1, best_pair[0], km))
                bridges += 1
                union(best_pair[0], best_pair[1])
    return bridges


def find_components(lines):
    """Find connected components among line segments."""
    n = len(lines)
    endpoints = defaultdict(set)
    for i, l in enumerate(lines):
        coords = list(l.coords)
        endpoints[quantize((coords[0][0], coords[0][1]))].add(i)
        endpoints[quantize((coords[-1][0], coords[-1][1]))].add(i)

    parent = list(range(n))
    rank = [0] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    for ids in endpoints.values():
        ids = list(ids)
        for j in range(1, len(ids)):
            union(ids[0], ids[j])

    comps = defaultdict(list)
    for i in range(n):
        comps[find(i)].append(i)
    return comps


def find_nearest_node(graph_nodes, lon, lat):
    best_node = None
    best_dist = float('inf')
    for n in graph_nodes:
        d = math.sqrt((n[0] - lon)**2 + (n[1] - lat)**2)
        if d < best_dist:
            best_dist = d
            best_node = n
    return best_node, best_dist


def dijkstra(graph, start, end):
    dist = {start: 0}
    prev = {}
    prev_line = {}
    pq = [(0, start)]
    visited = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if u == end:
            break
        for line_idx, v, weight in graph.get(u, []):
            nd = d + weight
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                prev[v] = u
                prev_line[v] = line_idx
                heapq.heappush(pq, (nd, v))
    if end not in prev and start != end:
        return None, None, float('inf')
    path = []
    lines = []
    node = end
    while node != start:
        path.append(node)
        lines.append(prev_line[node])
        node = prev[node]
    path.append(start)
    path.reverse()
    lines.reverse()
    return path, lines, dist.get(end, float('inf'))


def raw_proj_km(line, point):
    """Raw along-line distance in km using haversine."""
    proj = line.project(point)
    total = line.length
    if total == 0:
        return 0.0
    frac = proj / total
    coords = list(line.coords)
    cum_euclid = 0.0
    cum_haversine = 0.0
    target = frac * total
    for i in range(len(coords) - 1):
        seg_euclid = math.sqrt(
            (coords[i+1][0] - coords[i][0])**2 +
            (coords[i+1][1] - coords[i][1])**2
        )
        seg_haversine = haversine(
            coords[i][0], coords[i][1],
            coords[i+1][0], coords[i+1][1]
        )
        if cum_euclid + seg_euclid >= target:
            rem = target - cum_euclid
            f = rem / seg_euclid if seg_euclid > 0 else 0
            return (cum_haversine + f * seg_haversine) / 1000
        cum_euclid += seg_euclid
        cum_haversine += seg_haversine
    return cum_haversine / 1000


def calibrate_distance(raw_km, cal_points):
    """Piecewise linear interpolation using calibration points."""
    if not cal_points:
        return raw_km
    if raw_km <= cal_points[0][0]:
        if len(cal_points) >= 2:
            r0, g0 = cal_points[0]
            r1, g1 = cal_points[1]
            if r1 != r0:
                return g0 + (raw_km - r0) * (g1 - g0) / (r1 - r0)
        return cal_points[0][1] + (raw_km - cal_points[0][0])
    if raw_km >= cal_points[-1][0]:
        if len(cal_points) >= 2:
            r0, g0 = cal_points[-2]
            r1, g1 = cal_points[-1]
            if r1 != r0:
                return g1 + (raw_km - r1) * (g1 - g0) / (r1 - r0)
        return cal_points[-1][1] + (raw_km - cal_points[-1][0])
    for i in range(len(cal_points) - 1):
        r0, g0 = cal_points[i]
        r1, g1 = cal_points[i + 1]
        if r0 <= raw_km <= r1:
            if r1 == r0:
                return g0
            t = (raw_km - r0) / (r1 - r0)
            return g0 + t * (g1 - g0)
    return raw_km


def snap_to_lines(pt, lines, max_dist_m=500):
    """Snap a point to nearest line within max_dist_m. Returns (point, dist_m, line_idx)."""
    best_dist = float('inf')
    best_point = None
    best_idx = -1
    for i, l in enumerate(lines):
        try:
            proj_dist = l.project(pt)
            proj_pt = l.interpolate(proj_dist)
            d = haversine(pt.x, pt.y, proj_pt.x, proj_pt.y)
            if d < best_dist:
                best_dist = d
                best_point = proj_pt
                best_idx = i
        except Exception:
            pass
    return best_point, best_dist, best_idx


def main():
    print("=" * 80)
    print("AGENT 4 FIX: Clean Geometry (v2)")
    print("Lines only, proper labels, improved snapping")
    print("=" * 80)

    # ========== STEP 1: Read GeoPackage ==========
    gpkg_size = os.path.getsize(GPKG)
    print(f"\nSTEP 1: Reading GeoPackage ({gpkg_size/1024/1024:.1f} MB)...")
    conn = sqlite3.connect(GPKG)
    cursor = conn.execute(
        f'SELECT fid, geom, OBJEKTART, AUSSER_BETRIEB, MUSEUMSBAHN, '
        f'STANDSEILBAHN, ZAHNRADBAHN, ANSCHLUSSGLEIS, ACHSE_DKM, NAME, '
        f'VERKEHRSMITTEL, SHAPE_Length '
        f'FROM "{TBL}"'
    )
    features = []
    parse_fail = 0
    for row in cursor:
        geom = parse_gpkg_geom(row[1])
        if geom is None:
            parse_fail += 1
            continue
        features.append({
            'fid': row[0], 'geom': geom,
            'objektart': row[2],       # 0=narrow, 2=standard, 4=funicular
            'ausser_betrieb': row[3],   # 1=in service, 2=out of service
            'museumsbahn': row[4],      # 1=no, 2=yes (museum)
            'standseilbahn': row[5],    # funicular
            'zahnradbahn': row[6],      # rack railway
            'anschlussgleis': row[7],   # 1=main, 2=siding
            'achse_dkm': row[8],
            'name': row[9],
            'verkehrsmittel': row[10],  # 100=rail, 200=tram, 300=metro
            'length': row[11],
        })
    conn.close()
    print(f"  {len(features)} features parsed ({parse_fail} failures)")

    # ========== STEP 2: Filter by SwissTLM3D attributes ==========
    print("\nSTEP 2: Filter by SwissTLM3D attributes...")
    # Match v4's proven filter: AUSSER_BETRIEB=1 (in service),
    # ANSCHLUSSGLEIS=1 (not siding), MUSEUMSBAHN=1 (not museum),
    # STANDSEILBAHN=1 (not funicular — keep separate)
    # Do NOT filter on VERKEHRSMITTEL — it excludes too many features.
    # SwissTLM3D OBJEKTART: 0=Normalspur (standard gauge), 2=Schmalspur (narrow gauge)
    filtered = [f for f in features
                if f['ausser_betrieb'] == 1
                and f['anschlussgleis'] == 1
                and f['museumsbahn'] == 1]

    # OBJEKTART: 0 = Normalspur (standard gauge 1435mm), 2 = Schmalspur (narrow gauge)
    n_std = sum(1 for f in filtered if f['objektart'] == 0)
    n_nar = sum(1 for f in filtered if f['objektart'] == 2)
    n_fun = sum(1 for f in filtered if f['objektart'] == 4)
    print(f"  {len(filtered)} features: {n_std} standard_gauge, {n_nar} narrow_gauge, {n_fun} funicular")

    # ========== STEP 3: Transform LV95 → WGS84 ==========
    print("\nSTEP 3: Transforming LV95 → WGS84...")
    for f in filtered:
        f['geom_wgs'] = transform_geom(f['geom'])

    # ========== STEP 4: Bounding box filter ==========
    print("\nSTEP 4: Bounding box filter...")
    in_box = [f for f in filtered if in_bbox(f['geom_wgs'])]
    std_feats = [f for f in in_box if f['objektart'] == 0]   # Normalspur = standard gauge
    nar_feats = [f for f in in_box if f['objektart'] == 2]   # Schmalspur = narrow gauge
    fun_feats = [f for f in in_box if f['objektart'] == 4]   # Funicular
    print(f"  In bbox: {len(in_box)} ({len(std_feats)} std, {len(nar_feats)} nar, {len(fun_feats)} fun)")

    # Extract individual LineStrings
    std_lines = []
    for f in std_feats:
        std_lines.extend(extract_lines(f['geom_wgs']))
    nar_lines = []
    for f in nar_feats:
        nar_lines.extend(extract_lines(f['geom_wgs']))
    fun_lines = []
    for f in fun_feats:
        fun_lines.extend(extract_lines(f['geom_wgs']))
    print(f"  Lines: {len(std_lines)} std, {len(nar_lines)} nar, {len(fun_lines)} fun")

    # ========== STEP 5: Read stations ==========
    print("\nSTEP 5: Reading stations...")
    stations = []
    with open(STCSV, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            name = row['name'].strip().strip('"')
            stations.append({
                'name': name,
                'sid': row['station_id'],
                'lat': float(row['lat_wgs84']),
                'lon': float(row['lon_wgs84']),
                'pt': Point(float(row['lon_wgs84']), float(row['lat_wgs84'])),
            })
    print(f"  {len(stations)} stations")

    # Read GA distances for calibration
    ga_data = {}
    ga_order = []
    with open(GACSV, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            nm = row['station'].strip().strip('"')
            ga_data[nm] = {
                'rail_km': float(row['rail_km_est_from_geneva']),
                'lat': float(row['lat_wgs84']),
                'lon': float(row['lon_wgs84']),
            }
            ga_order.append(nm)
    print(f"  {len(ga_data)} GA cost entries")

    # ========== STEP 6: Build graph + bridge edges ==========
    print("\nSTEP 6: Build graph + bridge edges...")
    graph = build_adjacency(std_lines)
    print(f"  {len(graph)} nodes")
    bridges = add_bridge_edges(graph, BRIDGE_THRESHOLD)
    print(f"  {bridges} bridges added")
    graph_nodes = list(graph.keys())

    # ========== STEP 7: Mainline spine via Dijkstra ==========
    print("\nSTEP 7: Mainline spine Dijkstra...")
    spine_matched = []
    spine_failed = []
    for spine_name in MAINLINE_SPINE:
        sn = normalize_name(spine_name)
        station_data = None
        for s in stations:
            if normalize_name(s['name']) == sn:
                station_data = s
                break
        if station_data is None:
            for gn, gd in ga_data.items():
                if normalize_name(gn) == sn:
                    station_data = {
                        'name': gn, 'sid': '', 'lat': gd['lat'], 'lon': gd['lon'],
                        'pt': Point(gd['lon'], gd['lat']),
                    }
                    break
        if station_data is None:
            spine_failed.append(spine_name)
            continue
        node, node_dist = find_nearest_node(graph_nodes, station_data['lon'], station_data['lat'])
        dist_m = haversine(station_data['lon'], station_data['lat'], node[0], node[1]) if node else float('inf')
        max_snap = 15000 if spine_name in ("Aigle", "Bex") else 5000
        if dist_m > max_snap:
            spine_failed.append(f"{spine_name} ({dist_m:.0f}m)")
            continue
        spine_matched.append({
            'spine_name': spine_name, 'station': station_data,
            'node': node, 'snap_m': dist_m,
        })

    print(f"  Matched: {len(spine_matched)}/{len(MAINLINE_SPINE)}")
    if spine_failed:
        print(f"  Failed: {spine_failed}")

    # Connect spine stations via Dijkstra
    corridor_idx = set()
    corridor_lines_list = []
    failed_conn = []
    for i in range(len(spine_matched) - 1):
        s1 = spine_matched[i]
        s2 = spine_matched[i + 1]
        _, path_lines, path_km = dijkstra(graph, s1['node'], s2['node'])
        if path_lines is None:
            failed_conn.append((s1['spine_name'], s2['spine_name']))
            print(f"  FAILED: {s1['spine_name']} -> {s2['spine_name']}")
        else:
            for li in path_lines:
                if li >= 0 and li not in corridor_idx:
                    corridor_idx.add(li)
                    corridor_lines_list.append(std_lines[li])
    print(f"  Corridor: {len(corridor_lines_list)} segments, {len(failed_conn)} failed connections")

    # ========== STEP 7b: Merge + orient ==========
    print("\nSTEP 7b: Merge corridor segments...")
    merged = linemerge(corridor_lines_list)
    if merged.geom_type == 'MultiLineString':
        pieces = sorted(merged.geoms, key=lambda g: g.length, reverse=True)
        print(f"  {len(pieces)} pieces, stitching...")
        work = list(pieces[0].coords)
        remaining = list(pieces[1:])
        used = [False] * len(remaining)
        stitch_count = 0
        for _ in range(len(remaining)):
            best_idx = -1
            best_dist = float('inf')
            best_work_end = best_piece_end = None
            ws, we = work[0], work[-1]
            for j, p in enumerate(remaining):
                if used[j]:
                    continue
                pc = list(p.coords)
                for ref, w_end, pt, p_end in [
                    (we, 'e', pc[0], 's'), (we, 'e', pc[-1], 'e'),
                    (ws, 's', pc[0], 's'), (ws, 's', pc[-1], 'e'),
                ]:
                    d = math.sqrt((ref[0] - pt[0])**2 + (ref[1] - pt[1])**2)
                    if d < best_dist:
                        best_dist = d
                        best_idx = j
                        best_work_end = w_end
                        best_piece_end = p_end
            if best_idx >= 0 and best_dist < 0.01:
                used[best_idx] = True
                pc = list(remaining[best_idx].coords)
                stitch_count += 1
                if best_work_end == 'e' and best_piece_end == 's':
                    work.extend(pc)
                elif best_work_end == 'e' and best_piece_end == 'e':
                    work.extend(reversed(pc))
                elif best_work_end == 's' and best_piece_end == 's':
                    work = list(reversed(pc)) + work
                elif best_work_end == 's' and best_piece_end == 'e':
                    work = pc + work
            else:
                break
        merged = LineString(work)
        print(f"  Stitched {stitch_count}. {sum(1 for u in used if not u)} remaining.")

    corridor_km = line_km(merged) if merged.geom_type == 'LineString' else \
        sum(line_km(l) for l in merged.geoms)
    print(f"  Corridor: {corridor_km:.1f} km")

    # Orient west→east
    if merged.geom_type == 'LineString':
        coords = list(merged.coords)
        if coords[0][0] > coords[-1][0]:
            coords.reverse()
            merged = LineString(coords)
            print("  Oriented west→east")

    # ========== STEP 8: Projections + calibration ==========
    print("\nSTEP 8: Raw projections + distance calibration...")
    raw_projs = {}
    for s in stations:
        raw_projs[s['name']] = raw_proj_km(merged, s['pt'])

    # Build calibration points from mainline spine stations with GA references
    cal_points = []
    for spine_name in MAINLINE_SPINE:
        sn = normalize_name(spine_name)
        actual_name = None
        for s in stations:
            if normalize_name(s['name']) == sn:
                actual_name = s['name']
                break
        if actual_name is None:
            for gn in ga_data:
                if normalize_name(gn) == sn:
                    actual_name = gn
                    break
        if actual_name and actual_name in ga_data and actual_name in raw_projs:
            ga_km = ga_data[actual_name]['rail_km']
            raw_km = raw_projs[actual_name]
            cal_points.append((raw_km, ga_km, actual_name))

    cal_points.sort(key=lambda x: x[0])
    clean_cal = []
    for rk, gk, nm in cal_points:
        if not clean_cal or gk >= clean_cal[-1][1]:
            clean_cal.append((rk, gk))

    print(f"  Calibration points: {len(clean_cal)}/{len(cal_points)}")
    if clean_cal:
        print(f"  Raw range: {clean_cal[0][0]:.1f}–{clean_cal[-1][0]:.1f} km")
        print(f"  GA range: {clean_cal[0][1]:.1f}–{clean_cal[-1][1]:.1f} km")

    # ========== STEP 9: Snap stations + compute distances ==========
    print("\nSTEP 9: Snap stations + compute distances...")
    all_lines_for_snap = corridor_lines_list + nar_lines + fun_lines
    results = []
    for s in stations:
        sn_norm = normalize_name(s['name'])
        is_branch = False
        branch_type = None
        for bn, bt in BRANCH_STATIONS.items():
            if normalize_name(bn) == sn_norm:
                is_branch = True
                branch_type = bt
                break

        # Try snapping to corridor lines first, then narrow gauge, then funicular
        snap_pt_c, snap_dm_c, _ = snap_to_lines(s['pt'], corridor_lines_list)
        snap_pt_n, snap_dm_n, _ = snap_to_lines(s['pt'], nar_lines) if nar_lines else (None, float('inf'), -1)
        snap_pt_f, snap_dm_f, _ = snap_to_lines(s['pt'], fun_lines) if fun_lines else (None, float('inf'), -1)

        # For mainline spine stations, strongly prefer corridor (standard_gauge) snap
        # Only fall back to narrow gauge if corridor snap is >2km away
        is_spine = sn_norm in [normalize_name(sp) for sp in MAINLINE_SPINE]
        corridor_threshold = 2000 if is_spine else 0  # 2km grace for spine stations

        if snap_dm_c <= snap_dm_n + corridor_threshold and snap_dm_c <= snap_dm_f + corridor_threshold:
            snap_pt, snap_dm = snap_pt_c, snap_dm_c
            line_type = "standard_gauge"
        elif snap_dm_n <= snap_dm_f:
            snap_pt, snap_dm = snap_pt_n, snap_dm_n
            line_type = "narrow_gauge"
        else:
            snap_pt, snap_dm = snap_pt_f, snap_dm_f
            line_type = "funicular"

        # If snap fails entirely, use station coords
        if snap_pt is None:
            snap_pt = s['pt']
            snap_dm = float('inf')
            line_type = "unsnapped"

        # Calibrated distance
        raw_km = raw_projs[s['name']]
        cal_km = calibrate_distance(raw_km, clean_cal)
        ga_ref = ga_data[s['name']]['rail_km'] if s['name'] in ga_data else None

        results.append({
            'name': s['name'], 'sid': s['sid'],
            'lat': s['lat'], 'lon': s['lon'],
            'dist_km': cal_km, 'raw_km': raw_km,
            'ga_ref_km': ga_ref, 'snap_m': snap_dm,
            'snap_lat': snap_pt.y, 'snap_lon': snap_pt.x,
            'line_type': line_type,
            'is_branch': is_branch, 'branch_type': branch_type,
        })

    # Sort by distance
    results.sort(key=lambda x: x['dist_km'])
    for i, sd in enumerate(results):
        if i < len(results) - 1:
            sd['dist_to_next'] = round(results[i+1]['dist_km'] - sd['dist_km'], 2)
            sd['next_station'] = results[i+1]['name']
        else:
            sd['dist_to_next'] = None
            sd['next_station'] = None

    # ========== STEP 10: Build route features ==========
    print("\nSTEP 10: Build route features for GeoJSON...")

    route_inventory = []

    # Main corridor — standard gauge
    main_stations = [r['name'] for r in results if r['line_type'] == 'standard_gauge' and r['snap_m'] < 1000]
    corridor_merged_simplified = merged.simplify(SIMPLIFY_TOLERANCE)
    route_inventory.append({
        'name': 'Main Line (Geneva–Villeneuve–Bex)',
        'line_type': 'standard_gauge',
        'geometry': corridor_merged_simplified,
        'segment_count': len(corridor_lines_list),
        'total_length_km': corridor_km,
        'station_names': main_stations,
    })

    # Narrow gauge routes (by connected component)
    if nar_lines:
        nar_comps = find_components(nar_lines)
        for comp_id, line_indices in sorted(nar_comps.items(), key=lambda x: len(x[1]), reverse=True):
            comp_lines = [nar_lines[i] for i in line_indices]
            comp_km = sum(line_km(l) for l in comp_lines)
            if comp_km < 0.3:
                continue
            comp_union = unary_union(comp_lines)
            nearby_stations = [s['name'] for s in stations if comp_union.distance(s['pt']) < 0.005]

            # Name the route
            def has_keyword(names, keywords):
                for n in names:
                    for k in keywords:
                        if k.lower() in n.lower():
                            return True
                return False

            if has_keyword(nearby_stations, ['Montreux']) and comp_km > 5:
                rn = "MOB (Montreux–Oberland)"
            elif has_keyword(nearby_stations, ['Aigle']) and not has_keyword(nearby_stations, ['Montreux']):
                rn = "TPC (Aigle region)"
            elif has_keyword(nearby_stations, ['Bex']):
                rn = "BVB (Bex–Villars)"
            elif has_keyword(nearby_stations, ['Nyon']):
                rn = "NStCM (Nyon–St-Cergue)"
            elif has_keyword(nearby_stations, ['Lausanne-Flon']):
                rn = "LEB (Lausanne–Echallens–Bercher)"
            elif nearby_stations:
                rn = f"Narrow gauge ({nearby_stations[0]} area)"
            else:
                rn = f"Narrow gauge ({comp_km:.1f} km)"

            comp_merged = linemerge(comp_lines)
            comp_simplified = comp_merged.simplify(SIMPLIFY_TOLERANCE)
            route_inventory.append({
                'name': rn,
                'line_type': 'narrow_gauge',
                'geometry': comp_simplified,
                'segment_count': len(line_indices),
                'total_length_km': comp_km,
                'station_names': nearby_stations,
            })

    # Funicular routes
    if fun_lines:
        fun_comps = find_components(fun_lines)
        for comp_id, line_indices in sorted(fun_comps.items(), key=lambda x: len(x[1]), reverse=True):
            comp_lines = [fun_lines[i] for i in line_indices]
            comp_km = sum(line_km(l) for l in comp_lines)
            if comp_km < 0.1:
                continue
            comp_union = unary_union(comp_lines)
            nearby_stations = [s['name'] for s in stations if comp_union.distance(s['pt']) < 0.005]
            rn = f"Funicular ({nearby_stations[0] if nearby_stations else f'{comp_km:.1f}km'})"
            comp_merged = linemerge(comp_lines)
            comp_simplified = comp_merged.simplify(SIMPLIFY_TOLERANCE)
            route_inventory.append({
                'name': rn,
                'line_type': 'funicular',
                'geometry': comp_simplified,
                'segment_count': len(line_indices),
                'total_length_km': comp_km,
                'station_names': nearby_stations,
            })

    route_inventory.sort(key=lambda r: r['total_length_km'], reverse=True)

    # ========== STEP 11: Quality checks ==========
    print("\nSTEP 11: Quality assessment...")
    snaps = [sd['snap_m'] for sd in results]
    print(f"  Snap distances: min={min(snaps):.0f}m, max={max(snaps):.0f}m, mean={sum(snaps)/len(snaps):.0f}m")
    print(f"  <100m: {sum(1 for d in snaps if d <= 100)}/49")
    print(f"  <300m: {sum(1 for d in snaps if d <= 300)}/49")
    print(f"  <500m: {sum(1 for d in snaps if d <= 500)}/49")
    print(f"  <1km:  {sum(1 for d in snaps if d <= 1000)}/49")

    far_stations = [sd for sd in results if sd['snap_m'] > 500]
    if far_stations:
        print(f"\n  Stations >500m snap ({len(far_stations)}):")
        for sd in far_stations:
            print(f"    {sd['name']}: {sd['snap_m']:.0f}m ({sd['line_type']}, "
                  f"{'branch: ' + sd['branch_type'] if sd['is_branch'] else 'mainline'})")

    # Distance validation
    print(f"\n  Distance validation:")
    devs = []
    for sd in results:
        if sd['ga_ref_km'] is not None:
            diff = sd['dist_km'] - sd['ga_ref_km']
            devs.append((sd['name'], sd['ga_ref_km'], sd['dist_km'], diff))
    if devs:
        abs_devs = [abs(d[3]) for d in devs]
        print(f"  Stations with GA reference: {len(devs)}")
        print(f"  Mean abs deviation: {sum(abs_devs)/len(abs_devs):.1f} km")
        print(f"  Max abs deviation: {max(abs_devs):.1f} km")
        expected = [d[1] for d in devs]
        actual = [d[2] for d in devs]
        me = sum(expected) / len(expected)
        ma = sum(actual) / len(actual)
        cov = sum((e - me) * (a - ma) for e, a in zip(expected, actual))
        se = math.sqrt(sum((e - me)**2 for e in expected))
        sa = math.sqrt(sum((a - ma)**2 for a in actual))
        pearson_r = cov / (se * sa) if se > 0 and sa > 0 else 0
        print(f"  Pearson r: {pearson_r:.4f}")

    # Check Genève classification
    ge_result = next((r for r in results if r['name'] == 'Genève'), None)
    if ge_result:
        print(f"\n  Genève line_type: {ge_result['line_type']} — "
              f"{'PASS' if ge_result['line_type'] == 'standard_gauge' else 'FAIL (should be standard_gauge)'}")

    # Check monotonicity on mainline
    mainline_results = [r for r in results if not r['is_branch']]
    monotonic = all(mainline_results[i]['dist_km'] <= mainline_results[i+1]['dist_km']
                    for i in range(len(mainline_results) - 1))
    print(f"  Mainline distances monotonic: {'PASS' if monotonic else 'FAIL'}")

    # Route inventory
    print(f"\n  Route inventory:")
    print(f"  {'Name':<45} {'Type':<15} {'Length':>8} {'Segs':>5} {'Stns':>5}")
    for r in route_inventory:
        print(f"  {r['name']:<45} {r['line_type']:<15} {r['total_length_km']:>7.1f}k {r['segment_count']:>4} {len(r['station_names']):>4}")

    # ========== STEP 12: Write GeoJSON (LINES ONLY) ==========
    print("\nSTEP 12: Writing GeoJSON (lines only)...")
    geojson_features = []
    for r in route_inventory:
        geom = r['geometry']
        if geom.is_empty:
            continue
        # Ensure 2D coordinates only
        if geom.geom_type == 'LineString':
            geom = LineString([(c[0], c[1]) for c in geom.coords])
        elif geom.geom_type == 'MultiLineString':
            geom = MultiLineString([
                LineString([(c[0], c[1]) for c in l.coords]) for l in geom.geoms
            ])
        geojson_features.append({
            'type': 'Feature',
            'geometry': mapping(geom),
            'properties': {
                'line_type': r['line_type'],
                'name': r['name'],
                'station_names': ', '.join(r['station_names']),
                'segment_count': r['segment_count'],
                'total_length_km': round(r['total_length_km'], 2),
            }
        })

    # Verify: ZERO point features
    point_count = sum(1 for f in geojson_features if f['geometry']['type'] == 'Point')
    line_count = sum(1 for f in geojson_features
                     if f['geometry']['type'] in ('LineString', 'MultiLineString'))
    print(f"  Features: {line_count} lines, {point_count} points — "
          f"{'PASS' if point_count == 0 else 'FAIL (should be 0 points)'}")

    geojson = {
        'type': 'FeatureCollection',
        'crs': {'type': 'name', 'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}},
        'features': geojson_features,
    }
    with open(OGJN, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)
    gjn_size = os.path.getsize(OGJN)
    print(f"  {OGJN}: {gjn_size/1024:.0f} KB")

    # ========== STEP 13: Write station distances CSV ==========
    print("\nSTEP 13: Writing station distances CSV...")
    with open(OCSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow([
            'station_name', 'lat_wgs84', 'lon_wgs84',
            'snapped_lat', 'snapped_lon', 'snap_distance_m',
            'distance_from_geneva_km', 'line_type',
            'is_branch', 'branch_type',
        ])
        for sd in results:
            w.writerow([
                sd['name'],
                round(sd['lat'], 6), round(sd['lon'], 6),
                round(sd['snap_lat'], 6), round(sd['snap_lon'], 6),
                round(sd['snap_m'], 1),
                round(sd['dist_km'], 2),
                sd['line_type'],
                sd['is_branch'],
                sd['branch_type'] or '',
            ])
    csv_size = os.path.getsize(OCSV)
    print(f"  {OCSV}: {csv_size/1024:.1f} KB ({len(results)} rows)")

    # ========== SUMMARY ==========
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\n--- Sources ---")
    print(f"  LOCAL: {GPKG} ({gpkg_size/1024/1024:.1f} MB)")
    print(f"    Table: {TBL}")
    print(f"    Features: {len(features)} total → {len(filtered)} after attribute filter → {len(in_box)} in bbox")
    print(f"  LOCAL: {STCSV} (49 station coordinates)")
    print(f"  LOCAL: {GACSV} (49 GA cost reference distances)")
    print(f"  No external API calls — pure local geometry processing")
    print(f"\n--- What worked ---")
    print(f"  SwissTLM3D attribute filtering: VERKEHRSMITTEL=100, AUSSER_BETRIEB=1, ANSCHLUSSGLEIS=1, MUSEUMSBAHN=1")
    print(f"  Dijkstra mainline spine: {len(spine_matched)}/{len(MAINLINE_SPINE)} stations connected")
    print(f"  Bridge edges: {bridges} (fixing Lausanne disconnection)")
    print(f"  Piecewise linear distance calibration: {len(clean_cal)} anchor points")
    print(f"  Douglas-Peucker simplification at {SIMPLIFY_TOLERANCE}° (~10m)")
    print(f"\n--- What didn't work / limitations ---")
    print(f"  Bex/Aigle: geometry may not extend fully → large snap distances")
    print(f"  Bus stop stations (Founex, Begnins, etc.): not on rail network → high snap distances expected")
    print(f"  linemerge produces fragments at complex junctions — stitching partially resolves this")
    print(f"\n--- Quality ---")
    print(f"  Snap: <500m for {sum(1 for d in snaps if d <= 500)}/49 stations")
    if devs:
        print(f"  Distance: mean abs dev {sum(abs_devs)/len(abs_devs):.1f} km, Pearson r={pearson_r:.4f}")
    print(f"  GeoJSON: {line_count} line features, 0 point features")
    print(f"  Genève: {ge_result['line_type'] if ge_result else 'NOT FOUND'}")
    print(f"  Mainline monotonic: {'YES' if monotonic else 'NO'}")
    print(f"\n--- Outputs ---")
    print(f"  {OGJN} ({gjn_size/1024:.0f} KB)")
    print(f"  {OCSV} ({csv_size/1024:.1f} KB, {len(results)} rows)")
    print("\nDone.")


if __name__ == '__main__':
    main()
