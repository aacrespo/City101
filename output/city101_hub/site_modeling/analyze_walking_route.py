"""
Analyze the hospital→station walking route for Lock 03 re-siting.

Reads road GeoJSON to:
1. Extract Avenue de Marcelin segments (hospital descent)
2. Extract Pont de la Gare segments (bridge over rail)
3. Chain segments into a walking polyline
4. Produce elevation profile
5. Sample terrain at candidate lock positions
6. Output candidate positions in both LV95 and local coordinates

LV95→Local transform: local = LV95 - (2527500, 1151500, 0)
"""

import json
import csv
import math
from collections import defaultdict

# ── Config ──────────────────────────────────────────────────────
LV95_OFFSET = (2527500, 1151500, 0)

ROAD_FILE = "output/city101_hub/context/city101_node3_morges_road.geojson"
RAIL_FILE = "output/city101_hub/context/city101_node3_morges_railway.geojson"
TERRAIN_FILE = "output/city101_hub/terrain/city101_node3_morges_swissalti3d_2021_2527-1151_2_2056_5728_xyz.csv"

# Known landmarks (approximate LV95)
EHC_MORGES = (2527600, 1151900)  # Hospital (uphill, north)
GARE_MORGES = (2527380, 1151300)  # Station (at tracks, south)


def lv95_to_local(e, n, z=0):
    return (e - LV95_OFFSET[0], n - LV95_OFFSET[1], z)


def dist2d(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def dist3d(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)


# ── Load roads ──────────────────────────────────────────────────
print("=" * 70)
print("WALKING ROUTE ANALYSIS: EHC Morges → Gare de Morges")
print("=" * 70)

with open(ROAD_FILE) as f:
    roads = json.load(f)

# Group roads by street name
by_name = defaultdict(list)
bridges = []
for feat in roads["features"]:
    props = feat["properties"]
    name = props.get("STRASSENNAME") or props.get("NAME") or "unnamed"
    kunstbaute = props.get("KUNSTBAUTE", 100)
    stufe = props.get("STUFE", 0)

    coords_list = feat["geometry"]["coordinates"]
    for coords in coords_list:
        segment = [(c[0], c[1], c[2] if len(c) > 2 else 0) for c in coords]
        by_name[name].append({
            "coords": segment,
            "kunstbaute": kunstbaute,
            "stufe": stufe,
            "objectid": props.get("OBJECTID"),
            "name": name,
        })
        if kunstbaute == 200 or stufe >= 1:
            bridges.append({
                "coords": segment,
                "name": name,
                "objectid": props.get("OBJECTID"),
            })

# ── Key streets ─────────────────────────────────────────────────
print("\n── KEY STREETS FOR WALKING ROUTE ──")

key_streets = [
    "Avenue de Marcelin",
    "Pont de la Gare",
    "Rue de la Gare",
    "Rue de Lausanne",
    "Avenue Henri-Monod",
]

for street in key_streets:
    segs = by_name.get(street, [])
    if not segs:
        print(f"\n  {street}: NOT FOUND")
        continue
    all_pts = []
    for s in segs:
        all_pts.extend(s["coords"])
    e_vals = [p[0] for p in all_pts]
    n_vals = [p[1] for p in all_pts]
    z_vals = [p[2] for p in all_pts]
    print(f"\n  {street}: {len(segs)} segments, {len(all_pts)} vertices")
    print(f"    E range: {min(e_vals):.0f} – {max(e_vals):.0f}")
    print(f"    N range: {min(n_vals):.0f} – {max(n_vals):.0f}")
    print(f"    Z range: {min(z_vals):.1f} – {max(z_vals):.1f}")
    print(f"    Local X: {min(e_vals)-LV95_OFFSET[0]:.0f} – {max(e_vals)-LV95_OFFSET[0]:.0f}")
    print(f"    Local Y: {min(n_vals)-LV95_OFFSET[1]:.0f} – {max(n_vals)-LV95_OFFSET[1]:.0f}")

# ── Bridges ─────────────────────────────────────────────────────
print("\n\n── BRIDGES (KUNSTBAUTE=200 or STUFE>=1) ──")
for b in bridges:
    pts = b["coords"]
    z_vals = [p[2] for p in pts]
    print(f"  {b['name']} (OID {b['objectid']}): {len(pts)} pts, "
          f"Z {min(z_vals):.1f}–{max(z_vals):.1f}")
    print(f"    Start: E{pts[0][0]:.0f} N{pts[0][1]:.0f} → End: E{pts[-1][0]:.0f} N{pts[-1][1]:.0f}")

# ── Build walking route ─────────────────────────────────────────
# The walk goes: Hospital (N) → Avenue de Marcelin (descent) → Pont de la Gare (bridge) → station area
# Let's chain the relevant segments by proximity

print("\n\n── BUILDING WALKING ROUTE ──")

# Collect all segments from walking-relevant streets
walk_streets = ["Avenue de Marcelin", "Pont de la Gare"]
walk_segments = []
for street in walk_streets:
    for seg in by_name.get(street, []):
        walk_segments.append(seg)

# Also look for unnamed segments between Avenue de Marcelin and Pont de la Gare
# by checking STUFE=1 (elevated) and proximity
# And check roads near the rail crossing area

# Find all road segments in the corridor between hospital and station
# Corridor: E 2527300-2527700, N 1151300-1151900
corridor_segments = []
for name, segs in by_name.items():
    for seg in segs:
        pts = seg["coords"]
        in_corridor = any(
            2527300 <= p[0] <= 2527700 and 1151300 <= p[1] <= 1151900
            for p in pts
        )
        if in_corridor:
            corridor_segments.append(seg)

# Chain walk segments by proximity (greedy nearest-endpoint)
def chain_segments(segments, start_point, max_gap=50):
    """Chain segments into a route starting from start_point."""
    remaining = list(segments)
    route_pts = []
    current = start_point

    while remaining:
        best_idx = None
        best_dist = float('inf')
        best_reversed = False

        for i, seg in enumerate(remaining):
            pts = seg["coords"]
            d_start = dist2d(current, pts[0])
            d_end = dist2d(current, pts[-1])
            if d_start < best_dist:
                best_dist = d_start
                best_idx = i
                best_reversed = False
            if d_end < best_dist:
                best_dist = d_end
                best_idx = i
                best_reversed = True

        if best_dist > max_gap:
            break

        seg = remaining.pop(best_idx)
        pts = seg["coords"]
        if best_reversed:
            pts = list(reversed(pts))

        if route_pts:
            # Skip first point if it's close to last
            if dist2d(route_pts[-1], pts[0]) < 2:
                pts = pts[1:]
        route_pts.extend(pts)
        current = route_pts[-1]

    return route_pts


# Chain from hospital area southward
# Start from the northernmost point of Avenue de Marcelin
marcelin_segs = by_name.get("Avenue de Marcelin", [])
all_marcelin_pts = []
for seg in marcelin_segs:
    all_marcelin_pts.extend(seg["coords"])

if all_marcelin_pts:
    # Find northernmost point (highest N)
    start_pt = max(all_marcelin_pts, key=lambda p: p[1])
    print(f"  Route start (N-most Marcelin): E{start_pt[0]:.0f} N{start_pt[1]:.0f} Z{start_pt[2]:.1f}")
    print(f"    Local: ({start_pt[0]-LV95_OFFSET[0]:.0f}, {start_pt[1]-LV95_OFFSET[1]:.0f}, {start_pt[2]:.1f})")

    # Chain Marcelin + bridge segments
    walk_route = chain_segments(walk_segments, start_pt, max_gap=100)

    # If route doesn't reach the bridge, also try chaining from corridor segments
    if walk_route:
        last = walk_route[-1]
        # Continue from last point through any remaining corridor segments
        remaining_corridor = [s for s in corridor_segments
                             if s not in walk_segments]
        extension = chain_segments(remaining_corridor, last, max_gap=50)
        if extension:
            walk_route.extend(extension)

    print(f"  Route: {len(walk_route)} points chained")
    if walk_route:
        print(f"  Start: E{walk_route[0][0]:.0f} N{walk_route[0][1]:.0f} Z{walk_route[0][2]:.1f}")
        print(f"  End:   E{walk_route[-1][0]:.0f} N{walk_route[-1][1]:.0f} Z{walk_route[-1][2]:.1f}")

        # Cumulative distance along route
        cum_dist = [0]
        for i in range(1, len(walk_route)):
            cum_dist.append(cum_dist[-1] + dist3d(walk_route[i-1], walk_route[i]))
        total_dist = cum_dist[-1]
        print(f"  Total walking distance: {total_dist:.0f}m")

# ── Elevation profile ───────────────────────────────────────────
print("\n\n── ELEVATION PROFILE ALONG ROUTE ──")
print(f"  {'Dist(m)':>8}  {'E':>10}  {'N':>10}  {'Z':>7}  {'LocalX':>7}  {'LocalY':>7}  Notes")
print(f"  {'─'*8}  {'─'*10}  {'─'*10}  {'─'*7}  {'─'*7}  {'─'*7}  {'─'*20}")

# Print profile at ~25m intervals
step = 25
next_dist = 0
for i, pt in enumerate(walk_route):
    d = cum_dist[i]
    note = ""
    if i == 0:
        note = "START (near hospital)"
    elif i == len(walk_route) - 1:
        note = "END"
    elif abs(d - total_dist/2) < step/2:
        note = "*** MIDPOINT ***"

    # Check if this is on the bridge
    for b in bridges:
        for bp in b["coords"]:
            if dist2d(pt, bp) < 5:
                note = f"BRIDGE ({b['name']})"
                break

    if d >= next_dist or note:
        lx, ly, lz = lv95_to_local(pt[0], pt[1], pt[2])
        print(f"  {d:8.0f}  {pt[0]:10.0f}  {pt[1]:10.0f}  {pt[2]:7.1f}  {lx:7.0f}  {ly:7.0f}  {note}")
        if d >= next_dist:
            next_dist = d + step

# ── Load terrain for Z sampling ─────────────────────────────────
print("\n\n── TERRAIN SAMPLING ──")
print("  Loading terrain grid...")

terrain = {}
with open(TERRAIN_FILE) as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        x, y, z = float(row[0]), float(row[1]), float(row[2])
        terrain[(round(x, 1), round(y, 1))] = z

print(f"  Loaded {len(terrain)} terrain points")

def sample_terrain(e, n, radius=2):
    """Sample terrain Z at LV95 position using nearest grid points."""
    # Grid is 2m spacing
    e_r = round(e / 2) * 2
    n_r = round(n / 2) * 2
    z_vals = []
    for de in range(-radius, radius+1, 2):
        for dn in range(-radius, radius+1, 2):
            key = (e_r + de, n_r + dn)
            if key in terrain:
                z_vals.append(terrain[key])
    if z_vals:
        return sum(z_vals) / len(z_vals)
    return None


# ── Load rail for crossing detection ────────────────────────────
with open(RAIL_FILE) as f:
    rail = json.load(f)

rail_segments = []
for feat in rail["features"]:
    for coords in feat["geometry"]["coordinates"]:
        pts = [(c[0], c[1], c[2] if len(c) > 2 else 0) for c in coords]
        rail_segments.append(pts)

# Find rail crossing zone (where walking route is closest to rail)
print("\n── RAIL CROSSING ZONE ──")
min_rail_dist = float('inf')
crossing_pt = None
crossing_idx = None
for i, pt in enumerate(walk_route):
    for rail_seg in rail_segments:
        for rp in rail_seg:
            d = dist2d(pt, rp)
            if d < min_rail_dist:
                min_rail_dist = d
                crossing_pt = pt
                crossing_idx = i

if crossing_pt:
    print(f"  Closest approach to rail: {min_rail_dist:.1f}m")
    print(f"  At route point {crossing_idx}/{len(walk_route)}: "
          f"E{crossing_pt[0]:.0f} N{crossing_pt[1]:.0f} Z{crossing_pt[2]:.1f}")
    lx, ly, lz = lv95_to_local(crossing_pt[0], crossing_pt[1], crossing_pt[2])
    print(f"  Local: ({lx:.0f}, {ly:.0f}, {lz:.1f})")
    print(f"  At distance {cum_dist[crossing_idx]:.0f}m along route "
          f"({100*cum_dist[crossing_idx]/total_dist:.0f}% of total)")

# ── Candidate lock positions ────────────────────────────────────
print("\n\n── CANDIDATE LOCK POSITIONS ──")
print("  Lock footprint: 34m (X/E-W) × 10m (Y/N-S)")
print("  Looking for positions along the descent, near rail crossing")
print()

# Candidates:
# A) Current position: (-60, 0, 381.5) → LV95 (2527440, 1151500)
# B) On Av. de Marcelin at midpoint of descent
# C) Just before the bridge (Pont de la Gare approach)
# D) At the closest approach to rail tracks

candidates = {}

# A) Current
candidates["A_current"] = {
    "lv95": (2527440, 1151500),
    "desc": "Current position (15m N of tracks)",
}

# B) Midpoint of walking route
mid_idx = len(walk_route) // 2
mid_pt = walk_route[mid_idx]
candidates["B_midpoint"] = {
    "lv95": (mid_pt[0], mid_pt[1]),
    "desc": f"Walking route midpoint (~{cum_dist[mid_idx]:.0f}m)",
}

# C) Just before bridge - find first bridge point on route
for i, pt in enumerate(walk_route):
    for b in bridges:
        for bp in b["coords"]:
            if dist2d(pt, bp) < 5:
                # Go back ~30m from bridge start
                target_dist = cum_dist[i] - 30
                for j, d in enumerate(cum_dist):
                    if d >= target_dist:
                        pre_bridge = walk_route[j]
                        candidates["C_pre_bridge"] = {
                            "lv95": (pre_bridge[0], pre_bridge[1]),
                            "desc": f"30m before bridge ({cum_dist[j]:.0f}m along route)",
                        }
                        break
                break
        if "C_pre_bridge" in candidates:
            break
    if "C_pre_bridge" in candidates:
        break

# D) Near rail crossing
if crossing_pt:
    # Offset 15m north of crossing (uphill side)
    candidates["D_rail_approach"] = {
        "lv95": (crossing_pt[0], crossing_pt[1] + 15),
        "desc": f"15m N of rail closest approach ({cum_dist[crossing_idx]:.0f}m)",
    }

# E) On Avenue de Marcelin, where Z matches ~383-385 (transition zone)
for i, pt in enumerate(walk_route):
    if 383 <= pt[2] <= 385:
        # Find a point on Av. de Marcelin in this Z range
        for seg in marcelin_segs:
            for mp in seg["coords"]:
                if 383 <= mp[2] <= 385 and dist2d(pt, mp) < 20:
                    candidates["E_marcelin_transition"] = {
                        "lv95": (mp[0], mp[1]),
                        "desc": f"Av. de Marcelin at Z~{mp[2]:.1f} (descent transition)",
                    }
                    break
            if "E_marcelin_transition" in candidates:
                break
        if "E_marcelin_transition" in candidates:
            break

for label, cand in sorted(candidates.items()):
    e, n = cand["lv95"]
    lx, ly = e - LV95_OFFSET[0], n - LV95_OFFSET[1]
    terrain_z = sample_terrain(e, n)

    print(f"  {label}: {cand['desc']}")
    print(f"    LV95: E {e:.0f}, N {n:.0f}")
    print(f"    Local: ({lx:.0f}, {ly:.0f})")
    print(f"    Terrain Z: {terrain_z:.1f}" if terrain_z else "    Terrain Z: N/A (outside grid)")

    # Check terrain flatness across footprint (34m × 10m)
    if terrain_z:
        z_samples = []
        for de in range(-17, 18, 2):
            for dn in range(-5, 6, 2):
                z = sample_terrain(e + de, n + dn)
                if z:
                    z_samples.append(z)
        if z_samples:
            z_range = max(z_samples) - min(z_samples)
            z_mean = sum(z_samples) / len(z_samples)
            print(f"    Footprint Z: mean {z_mean:.1f}, range {z_range:.1f}m "
                  f"(min {min(z_samples):.1f}, max {max(z_samples):.1f})")
            cand["terrain_z"] = terrain_z
            cand["z_mean"] = z_mean
            cand["z_range"] = z_range
    print()


# ── Summary ─────────────────────────────────────────────────────
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"\nWalking route: {total_dist:.0f}m from Avenue de Marcelin (hospital) to station area")
print(f"Elevation change: {walk_route[0][2]:.1f}m → {walk_route[-1][2]:.1f}m "
      f"(Δ{walk_route[0][2] - walk_route[-1][2]:.1f}m descent)")
print(f"Bridge: Pont de la Gare at ~{min_rail_dist:.0f}m from rail")
print(f"\nCurrent lock position: local (-60, 0, 381.5) = LV95 (2527440, 1151500)")

# Recommend best candidate
best = None
for label, cand in candidates.items():
    if label == "A_current":
        continue
    if cand.get("z_range") and cand["z_range"] < 3.0:
        if best is None or cand.get("z_range", 99) < candidates[best].get("z_range", 99):
            best = label

if best:
    c = candidates[best]
    e, n = c["lv95"]
    lx, ly = e - LV95_OFFSET[0], n - LV95_OFFSET[1]
    print(f"\nRecommended: {best} — {c['desc']}")
    print(f"  SITE_ORIGIN = ({lx:.0f}, {ly:.0f}, {c.get('terrain_z', 381.5):.1f})")
    print(f"  LV95: E {e:.0f}, N {n:.0f}")

print("\n── ALL CANDIDATES (for decision) ──")
for label, cand in sorted(candidates.items()):
    e, n = cand["lv95"]
    lx, ly = e - LV95_OFFSET[0], n - LV95_OFFSET[1]
    tz = cand.get("terrain_z", "?")
    zr = cand.get("z_range", "?")
    tz_str = f"{tz:.1f}" if isinstance(tz, float) else tz
    zr_str = f"{zr:.1f}m" if isinstance(zr, float) else zr
    print(f"  {label}: local ({lx:.0f}, {ly:.0f}, {tz_str})  Z-range: {zr_str}  — {cand['desc']}")
