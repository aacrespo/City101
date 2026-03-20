"""
LOCK 05 — GRADIENT DISPATCHER (v5 — Agent Team Build)
Node 5, km 65 — CHUV Lausanne campus, steep terrain
LOG 400: Full architectural detail — 709 objects across 10 layers

v5 CHANGES (from v3):
- 7-agent team build (Structure, Shell, Facade, Windows, Circulation,
  Elevator, Roof agents + coordination layer)
- 709 objects total (up from ~65 in v3)
- 10 active layers (was 6)
- Articulated wall system with piers, sills, heads, lintels
- Full window/mullion/glass assemblies
- Elevator cores with shafts, cabs, counterweights, rails, doors
- Detailed roof: parapets, copings, skylight, drainage, equipment pads
- Ground level: entry canopy, paving, curbs, bollards, foundations
- Ramps with landings, rails, posts, anti-slip strips
- All columns categorized: base, void-edge, continuity

CONCEPT: An elevator bank routing multiple supply chain flows across gradient
levels. Multi-level dispatcher following a 15% grade.

SPATIAL PLAN:
    SITE_ORIGIN = (-450, -400, 451.0)
    X = [-10, 10] (20m wide, centered)
    Y = [0, 34] (34m deep, 4 levels stepping uphill)
    Z = [0, 14] (14m total height)

    Central void: x=[-3, 3], y=[5, 29] (6m x 24m atrium shaft)

    LEVELS:
    L0: z=0.0,   y=[0, 10],  h=3.5  (Public)
    L1: z=3.5,   y=[8, 18],  h=3.5  (Staff)
    L2: z=7.0,   y=[16, 26], h=3.5  (Logistics)
    L3: z=10.5,  y=[24, 34], h=3.5  (Emergency)
"""

import rhinoscriptsyntax as rs


# ---------------------------------------------------------------------------
# SITE PLACEMENT
# ---------------------------------------------------------------------------
SITE_ORIGIN = (-450, -400, 451.0)


# ---------------------------------------------------------------------------
# DIMENSIONAL CONSTANTS
# ---------------------------------------------------------------------------
WALL_T = 0.3
SLAB_T = 0.3
COL_W = 0.4
BEAM_W = 0.3
BEAM_H = 0.3
MULLION_W = 0.05
GLASS_T = 0.02
GLASS_RECESS = 0.08
FRAME_D = 0.15
PARAPET_H = 1.0
COPING_T = 0.015
FOUND_DEPTH = 0.4
FOUND_W = 0.5
FOOTING_W = 1.0
FOOTING_D = 0.3
SHAFT_T = 0.15
DOOR_H = 2.1
DOOR_W_HALF = 0.6
RAIL_POST_W = 0.08
RAIL_H = 1.1
CANOPY_T = 0.2
CANOPY_COL_W = 0.3
RAMP_T = 0.3
ANTI_SLIP_W = 0.02
ANTI_SLIP_H = 0.005

# Level definitions: (name, z_floor, y_start, y_end, height)
LEVELS = [
    ("L0", 0.0,   0, 10, 3.5),
    ("L1", 3.5,   8, 18, 3.5),
    ("L2", 7.0,  16, 26, 3.5),
    ("L3", 10.5, 24, 34, 3.5),
]

# Void zone
VOID_X = (-3, 3)
VOID_Y = (5, 29)


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def box(x0, y0, z0, x1, y1, z1):
    """Create a box from min/max corners, offset by SITE_ORIGIN."""
    ox, oy, oz = SITE_ORIGIN
    pts = [
        (x0+ox, y0+oy, z0+oz), (x1+ox, y0+oy, z0+oz),
        (x1+ox, y1+oy, z0+oz), (x0+ox, y1+oy, z0+oz),
        (x0+ox, y0+oy, z1+oz), (x1+ox, y0+oy, z1+oz),
        (x1+ox, y1+oy, z1+oz), (x0+ox, y1+oy, z1+oz),
    ]
    return rs.AddBox(pts)


def box_pts(pts_list):
    """For wedge/ramp shapes with explicit 8 points, offset by SITE_ORIGIN."""
    ox, oy, oz = SITE_ORIGIN
    return rs.AddBox([(p[0]+ox, p[1]+oy, p[2]+oz) for p in pts_list])


def named(obj, name):
    """Name an object and return it."""
    rs.ObjectName(obj, name)
    return obj


def in_void(x, y):
    """Check if position is strictly inside the void zone."""
    return VOID_X[0] < x < VOID_X[1] and VOID_Y[0] < y < VOID_Y[1]


# ---------------------------------------------------------------------------
# LAYERS (10 active)
# ---------------------------------------------------------------------------
def setup_layers():
    layers = {
        "Lock_05::Structure":    (90, 95, 100),
        "Lock_05::Walls":        (180, 200, 220),
        "Lock_05::Facade":       (255, 220, 120),
        "Lock_05::Windows":      (180, 220, 240),
        "Lock_05::Circulation":  (230, 180, 140),
        "Lock_05::Elevator":     (150, 150, 160),
        "Lock_05::Roof":         (200, 210, 220),
        "Lock_05::Ground":       (140, 130, 120),
        "Lock_05::FloorPlates":  (210, 210, 200),
        "Lock_05::Terrain":      (160, 150, 130),
    }
    for name, color in layers.items():
        if not rs.IsLayer(name):
            rs.AddLayer(name, color)
    return layers


# ===================================================================
# 1. STRUCTURE — 138 objects (106 columns + 32 beams)
# ===================================================================
def create_structure():
    rs.CurrentLayer("Lock_05::Structure")
    objs = []
    half = COL_W / 2.0

    # --- BASE COLUMNS (50 total) ---
    # Grid positions per level, skip void interior and special removals
    for li, (lname, z_floor, y_start, y_end, h) in enumerate(LEVELS):
        x_positions = [-10, -5, 0, 5, 10]
        y_positions = list(range(y_start, y_end + 1, 5))

        for x in x_positions:
            for y in y_positions:
                # Skip void interior
                if in_void(x, y):
                    continue
                # Special removals
                if li == 0 and x == 0 and y == 0:
                    continue  # entrance column removed
                if li == 3 and x == 0 and y == 34:
                    continue  # emergency access column removed
                col = box(x - half, y - half, z_floor,
                          x + half, y + half, z_floor + h)
                objs.append(named(col, "Col_L{}_{}_{}".format(li, x, y)))

    # --- VOID EDGE COLUMNS (20 total) ---
    # Columns at x=+/-3 along void boundary
    for li, (lname, z_floor, y_start, y_end, h) in enumerate(LEVELS):
        y_positions = list(range(y_start, y_end + 1, 5))
        for x in [-3, 3]:
            for y in y_positions:
                # Only place if y is within void Y range (5 <= y <= 29)
                if VOID_Y[0] <= y <= VOID_Y[1]:
                    col = box(x - half, y - half, z_floor,
                              x + half, y + half, z_floor + h)
                    objs.append(named(col,
                        "Col_L{}_{}_{}_{}" .format(li, x, y, "void")))

    # --- CONTINUITY COLUMNS (36 total) ---
    # At overlap Y positions between adjacent levels
    overlaps = [
        (0, 8),    # L0 extends to y=8 (L1 starts at 8)
        (1, 10),   # L1 extends to y=10 (L0 ends at 10)
        (1, 16),   # L1 extends to y=16 (L2 starts at 16)
        (2, 18),   # L2 extends to y=18 (L1 ends at 18)
        (2, 24),   # L2 extends to y=24 (L3 starts at 24)
        (3, 26),   # L3 extends to y=26 (L2 ends at 26)
    ]
    for li, y_cont in overlaps:
        _, z_floor, _, _, h = LEVELS[li]
        for x in [-10, -5, -3, 3, 5, 10]:
            col = box(x - half, y_cont - half, z_floor,
                      x + half, y_cont + half, z_floor + h)
            objs.append(named(col,
                "Col_L{}_{}_{}_{}" .format(li, x, y_cont, "cont")))

    # --- BEAMS (32 total) ---

    # 1. Perimeter beams per level L1-L3 (15 beams: 5 per level)
    for li in [1, 2, 3]:
        _, z_floor, y_s, y_n, _ = LEVELS[li]
        bz0 = z_floor - BEAM_H
        bz1 = z_floor
        # South beam (full width)
        b = box(-10, y_s - BEAM_W/2, bz0, 10, y_s + BEAM_W/2, bz1)
        objs.append(named(b, "Beam_L{}_S".format(li)))
        # North beam (split at void: west and east)
        b = box(-10, y_n - BEAM_W/2, bz0, -3, y_n + BEAM_W/2, bz1)
        objs.append(named(b, "Beam_L{}_N_W".format(li)))
        b = box(3, y_n - BEAM_W/2, bz0, 10, y_n + BEAM_W/2, bz1)
        objs.append(named(b, "Beam_L{}_N_E".format(li)))
        # East beam
        b = box(10 - BEAM_W/2, y_s, bz0, 10 + BEAM_W/2, y_n, bz1)
        objs.append(named(b, "Beam_L{}_E".format(li)))
        # West beam
        b = box(-10 - BEAM_W/2, y_s, bz0, -10 + BEAM_W/2, y_n, bz1)
        objs.append(named(b, "Beam_L{}_W".format(li)))

    # 2. Void edge beams (7 beams)
    # L1, L2: void beams at x=+/-3
    for li in [1, 2]:
        _, z_floor, y_s, y_n, _ = LEVELS[li]
        bz0 = z_floor - BEAM_H
        bz1 = z_floor
        b = box(-3 - BEAM_W/2, y_s, bz0, -3 + BEAM_W/2, y_n, bz1)
        objs.append(named(b, "Beam_L{}_Void_W_y{}_{}".format(li, y_s, y_n)))
        b = box(3 - BEAM_W/2, y_s, bz0, 3 + BEAM_W/2, y_n, bz1)
        objs.append(named(b, "Beam_L{}_Void_E_y{}_{}".format(li, y_s, y_n)))
    # L3: void beams only to y=29 (void ends there)
    _, z_floor, y_s, _, _ = LEVELS[3]
    bz0 = z_floor - BEAM_H
    bz1 = z_floor
    b = box(-3 - BEAM_W/2, y_s, bz0, -3 + BEAM_W/2, 29, bz1)
    objs.append(named(b, "Beam_L3_Void_W_y{}_29".format(y_s)))
    b = box(3 - BEAM_W/2, y_s, bz0, 3 + BEAM_W/2, 29, bz1)
    objs.append(named(b, "Beam_L3_Void_E_y{}_29".format(y_s)))
    # Void close beam at y=29 (connecting x=-3 to x=3)
    b = box(-3, 29 - BEAM_W/2, bz0, 3, 29 + BEAM_W/2, bz1)
    objs.append(named(b, "Beam_L3_VoidClose_N"))

    # 3. Internal beams (5 beams) — at mid-Y, split at void
    for li, y_mid in [(1, 13), (2, 21)]:
        _, z_floor, _, _, _ = LEVELS[li]
        bz0 = z_floor - BEAM_H
        bz1 = z_floor
        b = box(-10, y_mid - BEAM_W/2, bz0, -3, y_mid + BEAM_W/2, bz1)
        objs.append(named(b, "Beam_L{}_Int_y{}_W".format(li, y_mid)))
        b = box(3, y_mid - BEAM_W/2, bz0, 10, y_mid + BEAM_W/2, bz1)
        objs.append(named(b, "Beam_L{}_Int_y{}_E".format(li, y_mid)))
    # L3 internal at y=29 (full span, void closed here)
    _, z_floor, _, _, _ = LEVELS[3]
    bz0 = z_floor - BEAM_H
    bz1 = z_floor
    b = box(-10, 29 - BEAM_W/2, bz0, 10, 29 + BEAM_W/2, bz1)
    objs.append(named(b, "Beam_L3_Int_y29"))

    # 4. Transfer beams (2 beams) — replacing removed columns
    # Entrance transfer (L0 south, deeper beam)
    b = box(-5, -BEAM_W/2, 3.2, 5, BEAM_W/2, 3.6)
    objs.append(named(b, "Beam_L0_Transfer_Entrance"))
    # Emergency transfer (L3 north)
    b = box(-6, 34 - BEAM_W/2, 14.0, 6, 34 + BEAM_W/2, 14.4)
    objs.append(named(b, "Beam_L3_Transfer_Emergency"))

    # 5. Ramp edge beams (3 beams) — at x=6, marking ramp inner edge
    ramp_beam_spans = [(5, 13), (13, 21), (21, 29)]
    for y0, y1 in ramp_beam_spans:
        # Find z at each end based on ramp slope
        # Ramps go from level floor to next level floor
        # y0=5: z~0 → y1=13: z~3.5 (ramp L0-L1)
        # y0=13: z~3.5 → y1=21: z~7.0
        # y0=21: z~7.0 → y1=29: z~10.5
        idx = ramp_beam_spans.index((y0, y1))
        z_bot = idx * 3.5
        z_top = (idx + 1) * 3.5
        pts = [
            (6 - BEAM_W/2, y0, z_bot - BEAM_H),
            (6 + BEAM_W/2, y0, z_bot - BEAM_H),
            (6 + BEAM_W/2, y1, z_top - BEAM_H),
            (6 - BEAM_W/2, y1, z_top - BEAM_H),
            (6 - BEAM_W/2, y0, z_bot),
            (6 + BEAM_W/2, y0, z_bot),
            (6 + BEAM_W/2, y1, z_top),
            (6 - BEAM_W/2, y1, z_top),
        ]
        b = box_pts(pts)
        objs.append(named(b, "Beam_RampEdge_x6_y{}_{}".format(y0, y1)))

    return objs


# ===================================================================
# 2. WALLS — 56 objects
# ===================================================================
def create_walls():
    rs.CurrentLayer("Lock_05::Walls")
    objs = []

    # Per-level wall generation
    for li, (lname, z_floor, y_s, y_n, h) in enumerate(LEVELS):
        z_top = z_floor + h

        # --- NORTH FACADE (articulated around glazing openings) ---
        # Glazing zones: west panel x[-9.5, -3.5], east panel x[3.5, 9.5]
        # Sill height: z_floor + 0.8, head height: z_top - 0.3

        if li < 3:
            # L0-L2: standard north facade with 8 pieces
            # West pier (x=-10 to -9.5)
            w = box(-10, y_n - WALL_T, z_floor, -9.5, y_n, z_top)
            objs.append(named(w, "Wall_{}_North_WestPier".format(lname)))
            # West sill (below west window)
            w = box(-9.5, y_n - WALL_T, z_floor, -3.5, y_n, z_floor + 0.8)
            objs.append(named(w, "Wall_{}_North_WestSill".format(lname)))
            # West head (above west window)
            w = box(-9.5, y_n - WALL_T, z_top - 0.3, -3.5, y_n, z_top)
            objs.append(named(w, "Wall_{}_North_WestHead".format(lname)))
            # Center pier west (x=-3.5 to -3.0)
            w = box(-3.5, y_n - WALL_T, z_floor, -3.0, y_n, z_top)
            objs.append(named(w, "Wall_{}_North_CenterPierW".format(lname)))
            # Center pier east (x=3.0 to 3.5)
            w = box(3.0, y_n - WALL_T, z_floor, 3.5, y_n, z_top)
            objs.append(named(w, "Wall_{}_North_CenterPierE".format(lname)))
            # East sill (below east window)
            w = box(3.5, y_n - WALL_T, z_floor, 9.5, y_n, z_floor + 0.8)
            objs.append(named(w, "Wall_{}_North_EastSill".format(lname)))
            # East head (above east window)
            w = box(3.5, y_n - WALL_T, z_top - 0.3, 9.5, y_n, z_top)
            objs.append(named(w, "Wall_{}_North_EastHead".format(lname)))
            # East pier (x=9.5 to 10)
            w = box(9.5, y_n - WALL_T, z_floor, 10, y_n, z_top)
            objs.append(named(w, "Wall_{}_North_EastPier".format(lname)))
        else:
            # L3: emergency opening replaces center piers (opening x[-5,5])
            # West pier
            w = box(-10, y_n - WALL_T, z_floor, -9.5, y_n, z_top)
            objs.append(named(w, "Wall_{}_North_WestPier".format(lname)))
            # East pier
            w = box(9.5, y_n - WALL_T, z_floor, 10, y_n, z_top)
            objs.append(named(w, "Wall_{}_North_EastPier".format(lname)))
            # West sill
            w = box(-9.5, y_n - WALL_T, z_floor, -3.5, y_n, z_floor + 0.8)
            objs.append(named(w, "Wall_{}_North_WestSill".format(lname)))
            # West head
            w = box(-9.5, y_n - WALL_T, z_top - 0.3, -3.5, y_n, z_top)
            objs.append(named(w, "Wall_{}_North_WestHead".format(lname)))
            # East sill
            w = box(3.5, y_n - WALL_T, z_floor, 9.5, y_n, z_floor + 0.8)
            objs.append(named(w, "Wall_{}_North_EastSill".format(lname)))
            # East head
            w = box(3.5, y_n - WALL_T, z_top - 0.3, 9.5, y_n, z_top)
            objs.append(named(w, "Wall_{}_North_EastHead".format(lname)))

        # --- SOUTH FACADE ---
        if li == 0:
            # L0: split for entrance (opening x[-4,4], z[0, 3.2])
            w = box(-10, y_s, z_floor, -4, y_s + WALL_T, z_top)
            objs.append(named(w, "Wall_{}_South_Left".format(lname)))
            w = box(4, y_s, z_floor, 10, y_s + WALL_T, z_top)
            objs.append(named(w, "Wall_{}_South_Right".format(lname)))
            w = box(-4, y_s, 3.2, 4, y_s + WALL_T, z_top)
            objs.append(named(w, "Wall_{}_South_AboveEntry".format(lname)))
        else:
            # L1-L3: solid south facade
            w = box(-10, y_s, z_floor, 10, y_s + WALL_T, z_top)
            objs.append(named(w, "Wall_{}_South_Solid".format(lname)))

        # --- EAST FACADE ---
        if li == 0:
            # L0 east: below ramp zone, plus ramp lintel
            w = box(10 - WALL_T, y_s, z_floor, 10, 8, z_top)
            objs.append(named(w, "Wall_{}_East_BelowRamp".format(lname)))
            w = box(10 - WALL_T, 8, 3.2, 10, y_n, z_top)
            objs.append(named(w, "Wall_{}_East_RampLintel".format(lname)))
        elif li == 3:
            # L3 east: above ramp zone, plus ramp lintel
            w = box(10 - WALL_T, 29, z_floor, 10, y_n, z_top)
            objs.append(named(w, "Wall_{}_East_AboveRamp".format(lname)))
            w = box(10 - WALL_T, y_s, z_floor, 10, 29, z_floor + 0.3)
            objs.append(named(w, "Wall_{}_East_RampLintel".format(lname)))
        else:
            # L1, L2: mid section with two ramp lintels (south and north)
            y_mid = (y_s + y_n) // 2
            w = box(10 - WALL_T, y_s + 2, z_floor, 10, y_n - 2, z_top)
            objs.append(named(w, "Wall_{}_East_MidSection".format(lname)))
            w = box(10 - WALL_T, y_s, z_floor, 10, y_s + 2, z_floor + 0.3)
            objs.append(named(w, "Wall_{}_East_RampLintelS".format(lname)))
            w = box(10 - WALL_T, y_n - 2, z_floor, 10, y_n, z_floor + 0.3)
            objs.append(named(w, "Wall_{}_East_RampLintelN".format(lname)))

        # --- WEST FACADE ---
        w = box(-10, y_s, z_floor, -10 + WALL_T, y_n, z_top)
        objs.append(named(w, "Wall_{}_West_Solid".format(lname)))

    # --- VOID SPANDREL WALLS (6 objects to reach 56) ---
    # Spandrel panels closing the void at floor plate edges
    # At each level transition, a short wall closes the gap above/below slab
    for li in range(4):
        _, z_floor, _, _, h = LEVELS[li]
        # West void spandrel (x=-3 wall, between void Y range within this level)
        y_void_s = max(VOID_Y[0], LEVELS[li][2])
        y_void_n = min(VOID_Y[1], LEVELS[li][3])
        if y_void_s < y_void_n:
            # Spandrel below slab on west side of void
            w = box(-3 - SHAFT_T, y_void_s, z_floor,
                    -3, y_void_n, z_floor + 0.3)
            objs.append(named(w, "Wall_L{}_Void_Spandrel_W".format(li)))
    # Spandrels at void north close (y=29) — east and west
    w = box(-3 - SHAFT_T, 29 - WALL_T, 0.0, -3, 29, 14.0)
    objs.append(named(w, "Wall_Void_Close_W"))
    w = box(3, 29 - WALL_T, 0.0, 3 + SHAFT_T, 29, 14.0)
    objs.append(named(w, "Wall_Void_Close_E"))

    return objs


# ===================================================================
# 3. FACADE — 38 objects
# ===================================================================
def create_facade():
    rs.CurrentLayer("Lock_05::Facade")
    objs = []

    # Facade cladding panels — exterior face of walls
    # North facade: rainscreen panels between piers (4 levels x 2 panels = 8)
    for li, (lname, z_floor, y_s, y_n, h) in enumerate(LEVELS):
        z_top = z_floor + h
        # West panel cladding
        f = box(-9.5, y_n, z_floor, -3.5, y_n + 0.05, z_top)
        objs.append(named(f, "Facade_{}_North_Panel_W".format(lname)))
        # East panel cladding
        f = box(3.5, y_n, z_floor, 9.5, y_n + 0.05, z_top)
        objs.append(named(f, "Facade_{}_North_Panel_E".format(lname)))

    # South facade cladding (4 levels)
    for li, (lname, z_floor, y_s, y_n, h) in enumerate(LEVELS):
        z_top = z_floor + h
        f = box(-10, y_s - 0.05, z_floor, 10, y_s, z_top)
        objs.append(named(f, "Facade_{}_South_Clad".format(lname)))

    # West facade cladding (4 levels)
    for li, (lname, z_floor, y_s, y_n, h) in enumerate(LEVELS):
        z_top = z_floor + h
        f = box(-10 - 0.05, y_s, z_floor, -10, y_n, z_top)
        objs.append(named(f, "Facade_{}_West_Clad".format(lname)))

    # East facade cladding (4 levels)
    for li, (lname, z_floor, y_s, y_n, h) in enumerate(LEVELS):
        z_top = z_floor + h
        f = box(10, y_s, z_floor, 10 + 0.05, y_n, z_top)
        objs.append(named(f, "Facade_{}_East_Clad".format(lname)))

    # Corner reveals / trim pieces (4 levels x 4 corners = 16, but we
    # group per level as 2 strips: NW+SW corner trim and NE+SE corner trim)
    # = 4 levels x 2 sides = 8 corner trims
    # Actually to reach 38: 8 + 4 + 4 + 4 = 20 so far. Need 18 more.

    # Soffit panels at each level transition (under overhanging slab)
    # 3 transitions x 2 sides (east, west) = 6
    for li in [1, 2, 3]:
        _, z_floor, y_s, _, _ = LEVELS[li]
        _, _, _, y_n_prev, _ = LEVELS[li - 1]
        # East soffit
        f = box(6, y_s, z_floor - SLAB_T, 10, y_n_prev, z_floor)
        objs.append(named(f, "Facade_L{}_Soffit_E".format(li)))
        # West soffit
        f = box(-10, y_s, z_floor - SLAB_T, -6, y_n_prev, z_floor)
        objs.append(named(f, "Facade_L{}_Soffit_W".format(li)))

    # Entry surround panels (L0 south entrance framing)
    # Left jamb, right jamb, head
    f = box(-4.1, -0.1, 0, -4, 0.3, 3.2)
    objs.append(named(f, "Facade_L0_Entry_Jamb_L"))
    f = box(4, -0.1, 0, 4.1, 0.3, 3.2)
    objs.append(named(f, "Facade_L0_Entry_Jamb_R"))
    f = box(-4.1, -0.1, 3.2, 4.1, 0.3, 3.4)
    objs.append(named(f, "Facade_L0_Entry_Head"))

    # Spandrel panels at floor levels (horizontal bands, north facade)
    # 4 levels x 1 band = 4
    for li, (lname, z_floor, y_s, y_n, h) in enumerate(LEVELS):
        f = box(-10, y_n, z_floor - 0.05, 10, y_n + 0.05, z_floor)
        objs.append(named(f, "Facade_{}_Spandrel_N".format(lname)))

    # Emergency surround at L3 north
    f = box(-5.1, 34 - 0.1, 10.5, -5, 34.3, 14.0)
    objs.append(named(f, "Facade_L3_Emergency_Jamb_L"))
    f = box(5, 34 - 0.1, 10.5, 5.1, 34.3, 14.0)
    objs.append(named(f, "Facade_L3_Emergency_Jamb_R"))
    f = box(-5.1, 34 - 0.1, 14.0, 5.1, 34.3, 14.15)
    objs.append(named(f, "Facade_L3_Emergency_Head"))

    # Base reveal strip (L0, ground level transition)
    f = box(-10, 0, -0.05, 10, 0.05, 0.15)
    objs.append(named(f, "Facade_L0_BaseReveal"))

    # Roof canopy drip edge (over L2 canopy south edge)
    f = box(-10, 16 - 0.1, 14.0 + CANOPY_T, 10, 16, 14.0 + CANOPY_T + 0.05)
    objs.append(named(f, "Facade_Canopy_DripEdge"))

    return objs


# ===================================================================
# 4. WINDOWS — 178 objects
# ===================================================================
def create_windows():
    rs.CurrentLayer("Lock_05::Windows")
    objs = []

    # North facade glazing assemblies per level
    # Each panel (west and east) has:
    #   - Frame (surround)
    #   - Glass pane
    #   - Mullions dividing the panel
    #   - Transom (horizontal divider)

    for li, (lname, z_floor, y_s, y_n, h) in enumerate(LEVELS):
        z_sill = z_floor + 0.8
        z_head = z_floor + h - 0.3
        glass_h = z_head - z_sill  # 2.4m

        for side, x_left, x_right in [("W", -9.5, -3.5), ("E", 3.5, 9.5)]:
            panel_w = x_right - x_left  # 6.0m

            # Glass pane (recessed from wall face)
            g = box(x_left + MULLION_W, y_n - GLASS_RECESS - GLASS_T,
                    z_sill + MULLION_W,
                    x_right - MULLION_W, y_n - GLASS_RECESS,
                    z_head - MULLION_W)
            objs.append(named(g, "Glass_{}_North_{}_Main".format(lname, side)))

            # Frame — four pieces (top, bottom, left, right)
            # Bottom rail
            f = box(x_left, y_n - FRAME_D, z_sill,
                    x_right, y_n, z_sill + MULLION_W)
            objs.append(named(f, "Frame_{}_North_{}_Bot".format(lname, side)))
            # Top rail
            f = box(x_left, y_n - FRAME_D, z_head - MULLION_W,
                    x_right, y_n, z_head)
            objs.append(named(f, "Frame_{}_North_{}_Top".format(lname, side)))
            # Left stile
            f = box(x_left, y_n - FRAME_D, z_sill,
                    x_left + MULLION_W, y_n, z_head)
            objs.append(named(f, "Frame_{}_North_{}_Left".format(lname, side)))
            # Right stile
            f = box(x_right - MULLION_W, y_n - FRAME_D, z_sill,
                    x_right, y_n, z_head)
            objs.append(named(f, "Frame_{}_North_{}_Right".format(lname, side)))

            # Vertical mullions (dividing 6m panel into ~1.5m bays = 3 mullions)
            n_mullions = 3
            for mi in range(1, n_mullions + 1):
                mx = x_left + (panel_w / (n_mullions + 1)) * mi
                m = box(mx - MULLION_W/2, y_n - FRAME_D, z_sill,
                        mx + MULLION_W/2, y_n, z_head)
                objs.append(named(m,
                    "Mullion_{}_North_{}_{}" .format(lname, side, mi)))

            # Horizontal transom (at mid-height of glass)
            z_transom = z_sill + glass_h / 2.0
            t = box(x_left, y_n - FRAME_D, z_transom - MULLION_W/2,
                    x_right, y_n, z_transom + MULLION_W/2)
            objs.append(named(t,
                "Transom_{}_North_{}".format(lname, side)))

            # Sub-panes (glass divided by mullions and transom)
            # 4 bays x 2 rows = 8 sub-panes per panel
            bay_xs = [x_left + MULLION_W]
            for mi in range(1, n_mullions + 1):
                mx = x_left + (panel_w / (n_mullions + 1)) * mi
                bay_xs.append(mx + MULLION_W/2)
            bay_xe = []
            for mi in range(1, n_mullions + 1):
                mx = x_left + (panel_w / (n_mullions + 1)) * mi
                bay_xe.append(mx - MULLION_W/2)
            bay_xe.append(x_right - MULLION_W)

            for bi in range(n_mullions + 1):
                # Lower sub-pane
                sp = box(bay_xs[bi], y_n - GLASS_RECESS - GLASS_T,
                         z_sill + MULLION_W,
                         bay_xe[bi], y_n - GLASS_RECESS,
                         z_transom - MULLION_W/2)
                objs.append(named(sp,
                    "SubPane_{}_North_{}_{}_{}" .format(lname, side, bi, "Lo")))
                # Upper sub-pane
                sp = box(bay_xs[bi], y_n - GLASS_RECESS - GLASS_T,
                         z_transom + MULLION_W/2,
                         bay_xe[bi], y_n - GLASS_RECESS,
                         z_head - MULLION_W)
                objs.append(named(sp,
                    "SubPane_{}_North_{}_{}_{}" .format(lname, side, bi, "Hi")))

    # Per panel: 1 main glass + 4 frame + 3 mullions + 1 transom + 8 sub-panes = 17
    # Per level: 2 panels x 17 = 34
    # 4 levels x 34 = 136

    # L0 south entrance glazing (double doors + sidelights)
    # Left sidelight
    g = box(-3.5, -0.05, 0.0, -1.2, 0.0, 2.8)
    objs.append(named(g, "Glass_L0_Entry_Sidelight_L"))
    # Right sidelight
    g = box(1.2, -0.05, 0.0, 3.5, 0.0, 2.8)
    objs.append(named(g, "Glass_L0_Entry_Sidelight_R"))
    # Left door leaf
    g = box(-1.2, -0.05, 0.0, -0.05, 0.0, DOOR_H)
    objs.append(named(g, "Glass_L0_Entry_Door_L"))
    # Right door leaf
    g = box(0.05, -0.05, 0.0, 1.2, 0.0, DOOR_H)
    objs.append(named(g, "Glass_L0_Entry_Door_R"))
    # Transom above doors
    g = box(-3.5, -0.05, DOOR_H, 3.5, 0.0, 2.8)
    objs.append(named(g, "Glass_L0_Entry_Transom"))
    # Entry door frames (4 verticals + 2 horizontals)
    for xp, nm in [(-3.5, "L_Outer"), (-1.2, "L_Inner"),
                    (1.2, "R_Inner"), (3.5, "R_Outer")]:
        f = box(xp - MULLION_W/2, -FRAME_D, 0.0,
                xp + MULLION_W/2, 0.0, 2.8)
        objs.append(named(f, "Frame_L0_Entry_{}".format(nm)))
    f = box(-3.5, -FRAME_D, 2.8, 3.5, 0.0, 2.8 + MULLION_W)
    objs.append(named(f, "Frame_L0_Entry_Head"))
    f = box(-3.5, -FRAME_D, DOOR_H, 3.5, 0.0, DOOR_H + MULLION_W)
    objs.append(named(f, "Frame_L0_Entry_Transom"))
    # Entry: 5 glass + 4 vert frames + 2 horiz frames = 11

    # L3 emergency glazing (wide opening at north)
    # Left panel
    g = box(-4.5, 34.0, 10.5, -1.5, 34.05, 13.5)
    objs.append(named(g, "Glass_L3_Emerg_Panel_L"))
    # Right panel
    g = box(1.5, 34.0, 10.5, 4.5, 34.05, 13.5)
    objs.append(named(g, "Glass_L3_Emerg_Panel_R"))
    # Center doors (double leaf)
    g = box(-1.5, 34.0, 10.5, -0.05, 34.05, DOOR_H + 10.5)
    objs.append(named(g, "Glass_L3_Emerg_Door_L"))
    g = box(0.05, 34.0, 10.5, 1.5, 34.05, DOOR_H + 10.5)
    objs.append(named(g, "Glass_L3_Emerg_Door_R"))
    # Transom above emergency doors
    g = box(-4.5, 34.0, DOOR_H + 10.5, 4.5, 34.05, 13.5)
    objs.append(named(g, "Glass_L3_Emerg_Transom"))
    # Emergency frames
    for xp, nm in [(-4.5, "L_Outer"), (-1.5, "L_Inner"),
                    (1.5, "R_Inner"), (4.5, "R_Outer")]:
        f = box(xp - MULLION_W/2, 34.0, 10.5,
                xp + MULLION_W/2, 34.0 + FRAME_D, 13.5)
        objs.append(named(f, "Frame_L3_Emerg_{}".format(nm)))
    f = box(-4.5, 34.0, 13.5, 4.5, 34.0 + FRAME_D, 13.5 + MULLION_W)
    objs.append(named(f, "Frame_L3_Emerg_Head"))
    f = box(-4.5, 34.0, DOOR_H + 10.5,
            4.5, 34.0 + FRAME_D, DOOR_H + 10.5 + MULLION_W)
    objs.append(named(f, "Frame_L3_Emerg_Transom"))
    # Emergency: 5 glass + 4 vert frames + 2 horiz frames = 11

    # Void-facing glazing (atrium glass at each level, west and east side)
    # Each level has glass panels looking into the void
    for li, (lname, z_floor, y_s, y_n, h) in enumerate(LEVELS):
        y_v_s = max(VOID_Y[0], y_s)
        y_v_n = min(VOID_Y[1], y_n)
        if y_v_s >= y_v_n:
            continue
        z_sill = z_floor + 0.8
        z_head = z_floor + h - 0.3
        # West void glass
        g = box(-3 - GLASS_T, y_v_s, z_sill, -3, y_v_n, z_head)
        objs.append(named(g, "Glass_{}_Void_W".format(lname)))
        # East void glass
        g = box(3, y_v_s, z_sill, 3 + GLASS_T, y_v_n, z_head)
        objs.append(named(g, "Glass_{}_Void_E".format(lname)))
        # Void guardrail frame (mullion at top of void glass)
        f = box(-3 - MULLION_W, y_v_s, z_head,
                -3, y_v_n, z_head + MULLION_W)
        objs.append(named(f, "Frame_{}_Void_W_Top".format(lname)))
        f = box(3, y_v_s, z_head,
                3 + MULLION_W, y_v_n, z_head + MULLION_W)
        objs.append(named(f, "Frame_{}_Void_E_Top".format(lname)))
    # Void glass: 4 levels x 4 objects (2 glass + 2 frames) = 16
    # But L0 void y range: max(5,0)=5 to min(29,10)=10 → valid
    # L1: max(5,8)=8 to min(29,18)=18 → valid
    # L2: max(5,16)=16 to min(29,26)=26 → valid
    # L3: max(5,24)=24 to min(29,34)=29 → valid
    # All 4 valid = 16 objects

    # Skylight glazing over void at roof level (4 panels)
    sky_xs = [(-3, -0.5), (0.5, 3)]
    sky_ys = [(5, 17), (17, 29)]
    si = 0
    for xs, xe in sky_xs:
        for ys, ye in sky_ys:
            g = box(xs, ys, 14.0 - GLASS_T, xe, ye, 14.0)
            objs.append(named(g, "Glass_Skylight_{}".format(si)))
            si += 1

    # Total windows: 136 + 11 + 11 + 16 + 4 = 178

    return objs


# ===================================================================
# 5. CIRCULATION — 121 objects
# ===================================================================
def create_circulation():
    rs.CurrentLayer("Lock_05::Circulation")
    objs = []

    # Ramp definitions: (name, x0, x1, y0, y1, z_bot, z_top)
    ramp_defs = [
        ("Ramp_L0_L1", 6, 10, 5, 13, 0.0, 3.5),
        ("Ramp_L1_L2", 6, 10, 13, 21, 3.5, 7.0),
        ("Ramp_L2_L3", 6, 10, 21, 29, 7.0, 10.5),
    ]

    for rname, x0, x1, y0, y1, z_bot, z_top in ramp_defs:
        run = y1 - y0  # 8m

        # --- Main ramp slab ---
        ramp_pts = [
            (x0, y0, z_bot),            (x1, y0, z_bot),
            (x1, y1, z_top),            (x0, y1, z_top),
            (x0, y0, z_bot + RAMP_T),   (x1, y0, z_bot + RAMP_T),
            (x1, y1, z_top + RAMP_T),   (x0, y1, z_top + RAMP_T),
        ]
        r = box_pts(ramp_pts)
        objs.append(named(r, rname))

        # --- Inner rail (x0 side = x=6) ---
        rail_pts = [
            (x0, y0, z_bot + RAMP_T),
            (x0 + RAIL_POST_W, y0, z_bot + RAMP_T),
            (x0 + RAIL_POST_W, y1, z_top + RAMP_T),
            (x0, y1, z_top + RAMP_T),
            (x0, y0, z_bot + RAMP_T + RAIL_H),
            (x0 + RAIL_POST_W, y0, z_bot + RAMP_T + RAIL_H),
            (x0 + RAIL_POST_W, y1, z_top + RAMP_T + RAIL_H),
            (x0, y1, z_top + RAMP_T + RAIL_H),
        ]
        rail = box_pts(rail_pts)
        objs.append(named(rail, rname + "_Rail_Inner"))

        # --- Outer rail (x1 side = x=10, inside wall face) ---
        rail_pts_o = [
            (x1 - RAIL_POST_W, y0, z_bot + RAMP_T),
            (x1, y0, z_bot + RAMP_T),
            (x1, y1, z_top + RAMP_T),
            (x1 - RAIL_POST_W, y1, z_top + RAMP_T),
            (x1 - RAIL_POST_W, y0, z_bot + RAMP_T + RAIL_H),
            (x1, y0, z_bot + RAMP_T + RAIL_H),
            (x1, y1, z_top + RAMP_T + RAIL_H),
            (x1 - RAIL_POST_W, y1, z_top + RAMP_T + RAIL_H),
        ]
        rail_o = box_pts(rail_pts_o)
        objs.append(named(rail_o, rname + "_Rail_Outer"))

        # --- Rail posts (vertical supports, ~1m spacing) ---
        n_posts = int(run) + 1  # 9 posts per ramp
        for pi in range(n_posts):
            frac = pi / float(run)
            py = y0 + pi
            pz = z_bot + (z_top - z_bot) * frac
            # Inner post
            p = box(x0, py - RAIL_POST_W/2, pz + RAMP_T,
                    x0 + RAIL_POST_W, py + RAIL_POST_W/2,
                    pz + RAMP_T + RAIL_H)
            objs.append(named(p, "{}_Post_Inner_{}".format(rname, pi)))
            # Outer post
            p = box(x1 - RAIL_POST_W, py - RAIL_POST_W/2, pz + RAMP_T,
                    x1, py + RAIL_POST_W/2,
                    pz + RAMP_T + RAIL_H)
            objs.append(named(p, "{}_Post_Outer_{}".format(rname, pi)))

        # --- Anti-slip strips (every 0.5m along ramp) ---
        n_strips = int(run / 0.5)  # 16 strips per ramp
        for si in range(n_strips):
            frac = (si * 0.5) / float(run)
            sy = y0 + si * 0.5
            sz = z_bot + (z_top - z_bot) * frac
            strip = box(x0, sy - ANTI_SLIP_W/2, sz + RAMP_T,
                        x1, sy + ANTI_SLIP_W/2,
                        sz + RAMP_T + ANTI_SLIP_H)
            objs.append(named(strip,
                "{}_AntiSlip_{}".format(rname, si)))

        # --- Landing at top of ramp ---
        landing = box(x0, y1, z_top, x1, y1 + 1.5, z_top + RAMP_T)
        objs.append(named(landing, rname + "_Landing"))

    # Per ramp: 1 slab + 2 rails + 18 posts + 16 strips + 1 landing = 38
    # 3 ramps x 38 = 114

    # Corridor links at each level (connecting ramp landings to floor)
    # 3 links
    for li in range(3):
        _, z_top_val, _, _, _ = LEVELS[li + 1]
        y_land = [13, 21, 29][li]
        link = box(3, y_land, z_top_val,
                   6, y_land + 1.5, z_top_val + RAMP_T)
        objs.append(named(link,
            "Corridor_Link_L{}_L{}".format(li, li + 1)))

    # Void guardrail segments at each level (connecting to ramp zone)
    # 4 segments (one per level along void east edge)
    for li, (lname, z_floor, y_s, y_n, h) in enumerate(LEVELS):
        y_v_s = max(VOID_Y[0], y_s)
        y_v_n = min(VOID_Y[1], y_n)
        if y_v_s >= y_v_n:
            continue
        gr = box(3, y_v_s, z_floor, 3 + RAIL_POST_W, y_v_n,
                 z_floor + RAIL_H)
        objs.append(named(gr, "VoidGuard_{}_E".format(lname)))

    # Total: 114 + 3 + 4 = 121

    return objs


# ===================================================================
# 6. ELEVATOR — 64 objects
# ===================================================================
def create_elevator():
    rs.CurrentLayer("Lock_05::Elevator")
    objs = []

    # Two elevator cores in the void zone
    # Core A (west): x=[-3, -1], y=[12, 15] (3m x 3m shaft)
    # Core B (east): x=[1, 3], y=[12, 15]
    cores = [
        ("A", -3, -1, 12, 15),
        ("B",  1,  3, 12, 15),
    ]

    for core_name, cx0, cx1, cy0, cy1 in cores:
        shaft_w = cx1 - cx0
        shaft_d = cy1 - cy0

        # --- Shaft walls (4 sides, full height 0 to 14m) ---
        # South wall
        w = box(cx0, cy0, 0, cx1, cy0 + SHAFT_T, 14)
        objs.append(named(w, "Elev_{}_Shaft_S".format(core_name)))
        # North wall
        w = box(cx0, cy1 - SHAFT_T, 0, cx1, cy1, 14)
        objs.append(named(w, "Elev_{}_Shaft_N".format(core_name)))
        # West wall (with door openings simulated by splitting)
        w = box(cx0, cy0, 0, cx0 + SHAFT_T, cy1, 14)
        objs.append(named(w, "Elev_{}_Shaft_W".format(core_name)))
        # East wall
        w = box(cx1 - SHAFT_T, cy0, 0, cx1, cy1, 14)
        objs.append(named(w, "Elev_{}_Shaft_E".format(core_name)))

        # --- Shaft pit floor ---
        w = box(cx0, cy0, -FOUND_DEPTH, cx1, cy1, 0)
        objs.append(named(w, "Elev_{}_Pit".format(core_name)))

        # --- Machine room top ---
        w = box(cx0, cy0, 14, cx1, cy1, 14 + 0.5)
        objs.append(named(w, "Elev_{}_MachineRoom".format(core_name)))

        # --- Cab (positioned at L0) ---
        cab_margin = 0.1
        cab_x0 = cx0 + SHAFT_T + cab_margin
        cab_x1 = cx1 - SHAFT_T - cab_margin
        cab_y0 = cy0 + SHAFT_T + cab_margin
        cab_y1 = cy1 - SHAFT_T - cab_margin

        # Cab floor
        cf = box(cab_x0, cab_y0, 0, cab_x1, cab_y1, 0.05)
        objs.append(named(cf, "Elev_{}_Cab_Floor".format(core_name)))
        # Cab ceiling
        cc = box(cab_x0, cab_y0, 2.4, cab_x1, cab_y1, 2.45)
        objs.append(named(cc, "Elev_{}_Cab_Ceiling".format(core_name)))
        # Cab walls (3 sides — door side open, assume west for A, east for B)
        # Back wall
        cw = box(cab_x0, cab_y1 - 0.05, 0.05, cab_x1, cab_y1, 2.4)
        objs.append(named(cw, "Elev_{}_Cab_Back".format(core_name)))
        # Left wall
        cw = box(cab_x0, cab_y0, 0.05, cab_x0 + 0.05, cab_y1, 2.4)
        objs.append(named(cw, "Elev_{}_Cab_Left".format(core_name)))
        # Right wall
        cw = box(cab_x1 - 0.05, cab_y0, 0.05, cab_x1, cab_y1, 2.4)
        objs.append(named(cw, "Elev_{}_Cab_Right".format(core_name)))

        # --- Guide rails (4 rails per core, full height) ---
        rail_offset = 0.1
        rail_w = 0.05
        rail_positions = [
            (cx0 + SHAFT_T + rail_offset, cy0 + SHAFT_T + rail_offset),
            (cx1 - SHAFT_T - rail_offset, cy0 + SHAFT_T + rail_offset),
            (cx0 + SHAFT_T + rail_offset, cy1 - SHAFT_T - rail_offset),
            (cx1 - SHAFT_T - rail_offset, cy1 - SHAFT_T - rail_offset),
        ]
        for ri, (rx, ry) in enumerate(rail_positions):
            gr = box(rx - rail_w/2, ry - rail_w/2, 0,
                     rx + rail_w/2, ry + rail_w/2, 14)
            objs.append(named(gr,
                "Elev_{}_Rail_{}".format(core_name, ri)))

        # --- Counterweight ---
        cw_x = cx1 - SHAFT_T - 0.05 - 0.3 if core_name == "A" else cx0 + SHAFT_T + 0.05
        cw = box(cw_x, cy1 - SHAFT_T - 0.5, 7.0,
                 cw_x + 0.3, cy1 - SHAFT_T - 0.1, 9.5)
        objs.append(named(cw,
            "Elev_{}_Counterweight".format(core_name)))

        # --- Door assemblies at each level (4 levels x 1 door) ---
        for li, (lname, z_floor, _, _, _) in enumerate(LEVELS):
            # Door frame
            if core_name == "A":
                dx0 = cx0
                dx1 = cx0 + SHAFT_T
                dy0 = cy0 + shaft_d/2 - DOOR_W_HALF
                dy1 = cy0 + shaft_d/2 + DOOR_W_HALF
            else:
                dx0 = cx1 - SHAFT_T
                dx1 = cx1
                dy0 = cy0 + shaft_d/2 - DOOR_W_HALF
                dy1 = cy0 + shaft_d/2 + DOOR_W_HALF
            # Door frame surround
            df = box(dx0 - 0.05, dy0 - 0.05, z_floor,
                     dx1 + 0.05, dy1 + 0.05, z_floor + DOOR_H + 0.1)
            objs.append(named(df,
                "Elev_{}_DoorFrame_{}".format(core_name, lname)))
            # Door leaves (2 sliding panels)
            dl = box(dx0, dy0, z_floor,
                     dx1, cy0 + shaft_d/2, z_floor + DOOR_H)
            objs.append(named(dl,
                "Elev_{}_DoorLeaf_{}_{}" .format(core_name, lname, "L")))
            dr = box(dx0, cy0 + shaft_d/2, z_floor,
                     dx1, dy1, z_floor + DOOR_H)
            objs.append(named(dr,
                "Elev_{}_DoorLeaf_{}_{}" .format(core_name, lname, "R")))

    # Per core: 4 shaft walls + 1 pit + 1 machine room + 3 cab pieces
    #   (floor, ceiling, back) + 2 cab side walls + 4 guide rails
    #   + 1 counterweight + 4 levels x 3 door parts = 28
    #   Wait: 4+1+1+1+1+1+1+1+4+1 + 12 = 28. Let me recount:
    #   shaft walls: 4
    #   pit: 1
    #   machine room: 1
    #   cab: floor(1) + ceiling(1) + back(1) + left(1) + right(1) = 5
    #   rails: 4
    #   counterweight: 1
    #   doors: 4 levels x 3 (frame + 2 leaves) = 12
    #   Total per core: 4+1+1+5+4+1+12 = 28
    # 2 cores x 28 = 56

    # Elevator call panels at each level (both sides of void)
    # 4 levels x 2 panels = 8
    for li, (lname, z_floor, _, _, _) in enumerate(LEVELS):
        # West call panel (near Core A)
        cp = box(-3 - 0.3, 11.5, z_floor + 1.0,
                 -3 - 0.25, 11.5 + 0.2, z_floor + 1.4)
        objs.append(named(cp, "Elev_CallPanel_{}_W".format(lname)))
        # East call panel (near Core B)
        cp = box(3 + 0.25, 11.5, z_floor + 1.0,
                 3 + 0.3, 11.5 + 0.2, z_floor + 1.4)
        objs.append(named(cp, "Elev_CallPanel_{}_E".format(lname)))

    # Total: 56 + 8 = 64

    return objs


# ===================================================================
# 7. ROOF — 40 objects
# ===================================================================
def create_roof():
    rs.CurrentLayer("Lock_05::Roof")
    objs = []

    # Roof slab (top of L3, z=14.0)
    z_roof = 14.0

    # Main roof slab
    slab = box(-10, 24, z_roof, 10, 34, z_roof + SLAB_T)
    objs.append(named(slab, "Roof_Slab_Main"))

    # Extended roof canopy over L2 (cantilever)
    canopy = box(-10, 16, z_roof, 10, 24, z_roof + CANOPY_T)
    objs.append(named(canopy, "Roof_Canopy_L2"))

    # --- Parapets (perimeter wall at roof edge) ---
    # South parapet (y=24)
    p = box(-10, 24, z_roof + SLAB_T, 10, 24 + WALL_T, z_roof + SLAB_T + PARAPET_H)
    objs.append(named(p, "Roof_Parapet_S"))
    # North parapet (y=34)
    p = box(-10, 34 - WALL_T, z_roof + SLAB_T, 10, 34, z_roof + SLAB_T + PARAPET_H)
    objs.append(named(p, "Roof_Parapet_N"))
    # East parapet (x=10)
    p = box(10 - WALL_T, 24, z_roof + SLAB_T, 10, 34, z_roof + SLAB_T + PARAPET_H)
    objs.append(named(p, "Roof_Parapet_E"))
    # West parapet (x=-10)
    p = box(-10, 24, z_roof + SLAB_T, -10 + WALL_T, 34, z_roof + SLAB_T + PARAPET_H)
    objs.append(named(p, "Roof_Parapet_W"))

    # --- Parapet copings (cap on top of parapets) ---
    cz = z_roof + SLAB_T + PARAPET_H
    c = box(-10.05, 24 - 0.05, cz, 10.05, 24 + WALL_T + 0.05, cz + COPING_T)
    objs.append(named(c, "Roof_Coping_S"))
    c = box(-10.05, 34 - WALL_T - 0.05, cz, 10.05, 34 + 0.05, cz + COPING_T)
    objs.append(named(c, "Roof_Coping_N"))
    c = box(10 - WALL_T - 0.05, 24, cz, 10 + 0.05, 34, cz + COPING_T)
    objs.append(named(c, "Roof_Coping_E"))
    c = box(-10 - 0.05, 24, cz, -10 + WALL_T + 0.05, 34, cz + COPING_T)
    objs.append(named(c, "Roof_Coping_W"))

    # --- Canopy parapets (over L2 extension) ---
    p = box(-10, 16, z_roof + CANOPY_T, 10, 16 + WALL_T, z_roof + CANOPY_T + PARAPET_H)
    objs.append(named(p, "Roof_Canopy_Parapet_S"))
    p = box(-10, 16, z_roof + CANOPY_T, -10 + WALL_T, 24, z_roof + CANOPY_T + PARAPET_H)
    objs.append(named(p, "Roof_Canopy_Parapet_W"))
    p = box(10 - WALL_T, 16, z_roof + CANOPY_T, 10, 24, z_roof + CANOPY_T + PARAPET_H)
    objs.append(named(p, "Roof_Canopy_Parapet_E"))

    # Canopy copings
    ccz = z_roof + CANOPY_T + PARAPET_H
    c = box(-10.05, 16 - 0.05, ccz, 10.05, 16 + WALL_T + 0.05, ccz + COPING_T)
    objs.append(named(c, "Roof_Canopy_Coping_S"))
    c = box(-10 - 0.05, 16, ccz, -10 + WALL_T + 0.05, 24, ccz + COPING_T)
    objs.append(named(c, "Roof_Canopy_Coping_W"))
    c = box(10 - WALL_T - 0.05, 16, ccz, 10 + 0.05, 24, ccz + COPING_T)
    objs.append(named(c, "Roof_Canopy_Coping_E"))

    # So far: 2 slabs + 4 parapets + 4 copings + 3 canopy parapets + 3 canopy copings = 16

    # --- Skylight curb (around void opening at roof) ---
    # Void at roof: x[-3,3], y[24,29] (portion of void above L3)
    # Wait, the void runs y[5,29] but the roof is only over y[24,34].
    # So the skylight opening at roof level is x[-3,3], y[24,29]
    sk_x0, sk_x1 = -3, 3
    sk_y0, sk_y1 = 24, 29
    curb_h = 0.3
    # South curb
    c = box(sk_x0, sk_y0, z_roof + SLAB_T, sk_x1, sk_y0 + WALL_T,
            z_roof + SLAB_T + curb_h)
    objs.append(named(c, "Roof_Skylight_Curb_S"))
    # North curb
    c = box(sk_x0, sk_y1 - WALL_T, z_roof + SLAB_T, sk_x1, sk_y1,
            z_roof + SLAB_T + curb_h)
    objs.append(named(c, "Roof_Skylight_Curb_N"))
    # West curb
    c = box(sk_x0, sk_y0, z_roof + SLAB_T, sk_x0 + WALL_T, sk_y1,
            z_roof + SLAB_T + curb_h)
    objs.append(named(c, "Roof_Skylight_Curb_W"))
    # East curb
    c = box(sk_x1 - WALL_T, sk_y0, z_roof + SLAB_T, sk_x1, sk_y1,
            z_roof + SLAB_T + curb_h)
    objs.append(named(c, "Roof_Skylight_Curb_E"))

    # --- Drainage scuppers (small boxes at parapet base, 4 on each long side) ---
    scupper_w = 0.3
    scupper_h = 0.15
    for si in range(4):
        sx = -8 + si * 5.0  # positions along x
        # South scupper
        s = box(sx - scupper_w/2, 24, z_roof + SLAB_T,
                sx + scupper_w/2, 24 + WALL_T + 0.1, z_roof + SLAB_T + scupper_h)
        objs.append(named(s, "Roof_Scupper_S_{}".format(si)))
        # North scupper
        s = box(sx - scupper_w/2, 34 - WALL_T - 0.1, z_roof + SLAB_T,
                sx + scupper_w/2, 34, z_roof + SLAB_T + scupper_h)
        objs.append(named(s, "Roof_Scupper_N_{}".format(si)))

    # --- Mechanical equipment pads ---
    # HVAC unit pad
    eq = box(-8, 30, z_roof + SLAB_T, -5, 33, z_roof + SLAB_T + 0.15)
    objs.append(named(eq, "Roof_HVAC_Pad"))
    # HVAC unit
    eq = box(-7.5, 30.5, z_roof + SLAB_T + 0.15, -5.5, 32.5, z_roof + SLAB_T + 1.5)
    objs.append(named(eq, "Roof_HVAC_Unit"))
    # Elevator overrun housing (above machine rooms)
    eq = box(-3.5, 11.5, z_roof, 3.5, 15.5, z_roof + 1.0)
    objs.append(named(eq, "Roof_Elev_Overrun"))
    # Antenna/comm mast base
    eq = box(7, 31, z_roof + SLAB_T, 8, 32, z_roof + SLAB_T + 0.2)
    objs.append(named(eq, "Roof_Comm_Base"))

    # Total: 16 + 4 skylight curbs + 8 scuppers + 4 equipment = 32
    # Need 40 total. Add more detail:

    # Roof access hatch
    h = box(5, 28, z_roof, 6.5, 29.5, z_roof + SLAB_T + 0.1)
    objs.append(named(h, "Roof_Access_Hatch"))

    # Lightning protection bases (4 corners)
    for lx, ly, idx in [(-9.5, 24.5, 0), (9.5, 24.5, 1),
                         (-9.5, 33.5, 2), (9.5, 33.5, 3)]:
        lb = box(lx - 0.15, ly - 0.15, z_roof + SLAB_T + PARAPET_H,
                 lx + 0.15, ly + 0.15, z_roof + SLAB_T + PARAPET_H + 0.5)
        objs.append(named(lb, "Roof_Lightning_{}".format(idx)))

    # Roof membrane edge strip (perimeter flashing)
    # South
    f = box(-10, 24, z_roof + SLAB_T - 0.01, 10, 24.3, z_roof + SLAB_T)
    objs.append(named(f, "Roof_Flashing_S"))
    # North
    f = box(-10, 33.7, z_roof + SLAB_T - 0.01, 10, 34, z_roof + SLAB_T)
    objs.append(named(f, "Roof_Flashing_N"))
    # East
    f = box(9.7, 24, z_roof + SLAB_T - 0.01, 10, 34, z_roof + SLAB_T)
    objs.append(named(f, "Roof_Flashing_E"))

    # Total: 32 + 1 hatch + 4 lightning + 3 flashing = 40

    return objs


# ===================================================================
# 8. GROUND — 65 objects
# ===================================================================
def create_ground():
    rs.CurrentLayer("Lock_05::Ground")
    objs = []

    # --- Entry canopy (at L0 south) ---
    # Canopy slab
    c = box(-6, -3, 3.0, 6, 0, 3.0 + CANOPY_T)
    objs.append(named(c, "Ground_Canopy_Slab"))
    # Canopy columns (4)
    for cx, cy, idx in [(-5, -2.5, 0), (5, -2.5, 1),
                         (-5, -0.5, 2), (5, -0.5, 3)]:
        cc = box(cx - CANOPY_COL_W/2, cy - CANOPY_COL_W/2, 0,
                 cx + CANOPY_COL_W/2, cy + CANOPY_COL_W/2, 3.0)
        objs.append(named(cc, "Ground_Canopy_Col_{}".format(idx)))
    # Canopy fascia (front edge)
    f = box(-6, -3, 3.0, 6, -3 + 0.1, 3.0 + CANOPY_T + 0.15)
    objs.append(named(f, "Ground_Canopy_Fascia"))

    # --- Entry paving ---
    pv = box(-6, -4, -0.1, 6, 0, 0)
    objs.append(named(pv, "Ground_Paving_Entry"))
    # Side paving (west approach)
    pv = box(-14, -2, -0.1, -6, 2, 0)
    objs.append(named(pv, "Ground_Paving_West"))
    # Side paving (east approach / ambulance)
    pv = box(6, -2, -0.1, 14, 2, 0)
    objs.append(named(pv, "Ground_Paving_East"))
    # Loading zone paving (north/uphill)
    pv = box(-14, 32, -0.1 + 5.1, 14, 38, 5.1)
    objs.append(named(pv, "Ground_Paving_North"))

    # --- Curbs ---
    # Entry curb (south)
    cu = box(-6, -4, 0, 6, -4 + 0.15, 0.15)
    objs.append(named(cu, "Ground_Curb_Entry_S"))
    cu = box(-6, -4, 0, -6 + 0.15, 0, 0.15)
    objs.append(named(cu, "Ground_Curb_Entry_W"))
    cu = box(6 - 0.15, -4, 0, 6, 0, 0.15)
    objs.append(named(cu, "Ground_Curb_Entry_E"))

    # --- Bollards (entry protection, 8 posts) ---
    for bi in range(8):
        bx = -5.25 + bi * 1.5
        b = box(bx - 0.1, -3.5, 0, bx + 0.1, -3.5 + 0.2, 0.9)
        objs.append(named(b, "Ground_Bollard_{}".format(bi)))

    # --- Foundations ---
    # Strip foundations along building perimeter
    # South foundation
    fnd = box(-10 - FOUND_W/2, -FOUND_W/2, -FOUND_DEPTH,
              10 + FOUND_W/2, FOUND_W/2, 0)
    objs.append(named(fnd, "Ground_Found_S"))
    # North foundation (at y=34, elevated by slope)
    fnd = box(-10 - FOUND_W/2, 34 - FOUND_W/2, 10.5 - FOUND_DEPTH,
              10 + FOUND_W/2, 34 + FOUND_W/2, 10.5)
    objs.append(named(fnd, "Ground_Found_N"))
    # West foundation
    fnd_pts = [
        (-10 - FOUND_W/2, 0, -FOUND_DEPTH),
        (-10 + FOUND_W/2, 0, -FOUND_DEPTH),
        (-10 + FOUND_W/2, 34, 10.5 - FOUND_DEPTH),
        (-10 - FOUND_W/2, 34, 10.5 - FOUND_DEPTH),
        (-10 - FOUND_W/2, 0, 0),
        (-10 + FOUND_W/2, 0, 0),
        (-10 + FOUND_W/2, 34, 10.5),
        (-10 - FOUND_W/2, 34, 10.5),
    ]
    fnd = box_pts(fnd_pts)
    objs.append(named(fnd, "Ground_Found_W"))
    # East foundation
    fnd_pts = [
        (10 - FOUND_W/2, 0, -FOUND_DEPTH),
        (10 + FOUND_W/2, 0, -FOUND_DEPTH),
        (10 + FOUND_W/2, 34, 10.5 - FOUND_DEPTH),
        (10 - FOUND_W/2, 34, 10.5 - FOUND_DEPTH),
        (10 - FOUND_W/2, 0, 0),
        (10 + FOUND_W/2, 0, 0),
        (10 + FOUND_W/2, 34, 10.5),
        (10 - FOUND_W/2, 34, 10.5),
    ]
    fnd = box_pts(fnd_pts)
    objs.append(named(fnd, "Ground_Found_E"))

    # --- Spread footings (under each L0 column, 13 footings) ---
    l0_cols = []
    for x in [-10, -5, 0, 5, 10]:
        for y in [0, 5, 10]:
            if in_void(x, y):
                continue
            if x == 0 and y == 0:
                continue  # entrance column removed
            l0_cols.append((x, y))

    for x, y in l0_cols:
        ft = box(x - FOOTING_W/2, y - FOOTING_W/2, -FOUND_DEPTH - FOOTING_D,
                 x + FOOTING_W/2, y + FOOTING_W/2, -FOUND_DEPTH)
        objs.append(named(ft, "Ground_Footing_{}_{}".format(x, y)))

    # --- Elevator pit foundations (2) ---
    ft = box(-3 - 0.2, 12 - 0.2, -FOUND_DEPTH - FOOTING_D - 0.3,
             -1 + 0.2, 15 + 0.2, -FOUND_DEPTH)
    objs.append(named(ft, "Ground_ElevPit_Found_A"))
    ft = box(1 - 0.2, 12 - 0.2, -FOUND_DEPTH - FOOTING_D - 0.3,
             3 + 0.2, 15 + 0.2, -FOUND_DEPTH)
    objs.append(named(ft, "Ground_ElevPit_Found_B"))

    # --- Retaining walls (east and west, stepping with terrain) ---
    # West retaining wall
    rw_pts = [
        (-12, 0, -1), (-10.5, 0, -1),
        (-10.5, 34, 9.5), (-12, 34, 9.5),
        (-12, 0, 0), (-10.5, 0, 0),
        (-10.5, 34, 10.5), (-12, 34, 10.5),
    ]
    rw = box_pts(rw_pts)
    objs.append(named(rw, "Ground_RetWall_W"))
    # East retaining wall
    rw_pts = [
        (10.5, 0, -1), (12, 0, -1),
        (12, 34, 9.5), (10.5, 34, 9.5),
        (10.5, 0, 0), (12, 0, 0),
        (12, 34, 10.5), (10.5, 34, 10.5),
    ]
    rw = box_pts(rw_pts)
    objs.append(named(rw, "Ground_RetWall_E"))

    # --- Drainage channel (perimeter) ---
    dc = box(-10.5, -1, -0.2, 10.5, -0.8, 0)
    objs.append(named(dc, "Ground_Drain_S"))
    dc = box(-10.5, -1, -0.2, -10.2, 34, 0)
    objs.append(named(dc, "Ground_Drain_W"))
    dc = box(10.2, -1, -0.2, 10.5, 34, 0)
    objs.append(named(dc, "Ground_Drain_E"))

    # --- Signage / wayfinding elements ---
    # Main entry sign
    sg = box(-2, -3.8, 1.5, 2, -3.7, 2.5)
    objs.append(named(sg, "Ground_Sign_Entry"))
    # Emergency sign (north)
    sg = box(-1.5, 35, 12.0, 1.5, 35.1, 13.0)
    objs.append(named(sg, "Ground_Sign_Emergency"))

    # --- Accessible ramp at entry (small ramp from paving to L0 floor) ---
    ramp_pts = [
        (-3, -3, 0), (3, -3, 0),
        (3, 0, 0), (-3, 0, 0),
        (-3, -3, 0.15), (3, -3, 0.15),
        (3, 0, 0.15), (-3, 0, 0.15),
    ]
    ar = box_pts(ramp_pts)
    objs.append(named(ar, "Ground_AccessRamp"))

    # --- Bike rack ---
    br = box(-12, -2, 0, -11, -1, 0.8)
    objs.append(named(br, "Ground_BikeRack"))

    # --- Waste enclosure ---
    we = box(11, -2, 0, 12.5, -0.5, 1.2)
    objs.append(named(we, "Ground_WasteEnclosure"))

    # Count:
    # Canopy: 1 slab + 4 cols + 1 fascia = 6
    # Paving: 4
    # Curbs: 3
    # Bollards: 8
    # Foundations: 4 strip + 13 footings + 2 elev pits = 19
    # Retaining: 2
    # Drainage: 3
    # Signage: 2
    # Access ramp: 1
    # Bike rack: 1
    # Waste: 1
    # Subtotal: 6+4+3+8+19+2+3+2+1+1+1 = 50

    # Need 65 total. Add landscape elements:

    # --- Landscape planters (4) ---
    for pi, (px, py) in enumerate([(-8, -3), (8, -3), (-13, 1), (13, 1)]):
        pl = box(px - 1, py - 0.5, 0, px + 1, py + 0.5, 0.6)
        objs.append(named(pl, "Ground_Planter_{}".format(pi)))

    # --- Light pole bases (6) ---
    for li, (lx, ly) in enumerate([(-7, -4), (0, -4), (7, -4),
                                     (-7, -1), (0, -1), (7, -1)]):
        lb = box(lx - 0.15, ly - 0.15, 0, lx + 0.15, ly + 0.15, 0.3)
        objs.append(named(lb, "Ground_LightBase_{}".format(li)))

    # --- Bench (entry waiting area) ---
    bn = box(-3, -3.2, 0, -1, -2.8, 0.45)
    objs.append(named(bn, "Ground_Bench_0"))
    bn = box(1, -3.2, 0, 3, -2.8, 0.45)
    objs.append(named(bn, "Ground_Bench_1"))

    # --- Utility vaults (below grade, 3) ---
    uv = box(-5, -2, -0.8, -3, -1, -0.1)
    objs.append(named(uv, "Ground_UtilVault_Elec"))
    uv = box(3, -2, -0.8, 5, -1, -0.1)
    objs.append(named(uv, "Ground_UtilVault_Water"))
    uv = box(-1, -2, -0.8, 1, -1, -0.1)
    objs.append(named(uv, "Ground_UtilVault_Comm"))

    # Additional: 4 planters + 6 lights + 2 benches + 3 vaults = 15
    # Total: 50 + 15 = 65

    return objs


# ===================================================================
# 9. FLOOR PLATES — 8 objects
# ===================================================================
def create_floor_plates():
    rs.CurrentLayer("Lock_05::FloorPlates")
    objs = []

    for li, (lname, z_floor, y_s, y_n, h) in enumerate(LEVELS):
        # Floor slab (underside of floor)
        fl = box(-10, y_s, z_floor - SLAB_T, 10, y_n, z_floor)
        objs.append(named(fl, "Floor_{}_Slab".format(lname)))
        # Ceiling/roof slab of this level
        cl = box(-10, y_s, z_floor + h, 10, y_n, z_floor + h + SLAB_T)
        objs.append(named(cl, "Floor_{}_Ceiling".format(lname)))

    # 4 levels x 2 = 8

    return objs


# ===================================================================
# 10. TERRAIN — 1 object
# ===================================================================
def create_terrain():
    rs.CurrentLayer("Lock_05::Terrain")
    objs = []

    # Sloped ground — 15% grade over 34m = 5.1m rise
    terrain_pts = [
        (-14, -4, -3),  (14, -4, -3),
        (14, 38, -3),   (-14, 38, -3),
        (-14, -4,  0),  (14, -4,  0),
        (14, 38, 5.1),  (-14, 38, 5.1),
    ]
    terrain = box_pts(terrain_pts)
    objs.append(named(terrain, "Terrain_Slope"))

    return objs


# ===================================================================
# MAIN
# ===================================================================
def main():
    rs.EnableRedraw(False)

    setup_layers()

    all_objs = []
    counts = {}

    sections = [
        ("Structure",    create_structure),
        ("Walls",        create_walls),
        ("Facade",       create_facade),
        ("Windows",      create_windows),
        ("Circulation",  create_circulation),
        ("Elevator",     create_elevator),
        ("Roof",         create_roof),
        ("Ground",       create_ground),
        ("FloorPlates",  create_floor_plates),
        ("Terrain",      create_terrain),
    ]

    for section_name, create_fn in sections:
        section_objs = create_fn()
        counts[section_name] = len(section_objs)
        all_objs += section_objs

    # Group all objects
    group_name = "Lock_05_CHUV_Gradient_v5"
    if rs.IsGroup(group_name):
        rs.DeleteGroup(group_name)
    rs.AddGroup(group_name)
    rs.AddObjectsToGroup(all_objs, group_name)

    rs.EnableRedraw(True)
    rs.ZoomExtents()

    total = len(all_objs)

    print("=" * 64)
    print("LOCK 05 — GRADIENT DISPATCHER (v5 — Agent Team Build)")
    print("CHUV Lausanne, km 65 — LOG 400")
    print("=" * 64)
    print("Site origin: ({}, {}, {})".format(*SITE_ORIGIN))
    print("LV95 offset: E-2538500, N-1152500")
    print("Dimensions:  20m (X) x 34m (Y) x 14m (Z)")
    print("Grade:       15% over 34m (4 stepped levels at 3.5m)")
    print("-" * 64)
    print("LAYER COUNTS:")
    for section_name, _ in sections:
        print("  Lock_05::{:<14s} {:>4d} objects".format(
            section_name, counts[section_name]))
    print("-" * 64)
    print("TOTAL: {} objects".format(total))
    print("")
    print("Built by 7-agent team:")
    print("  Structure | Shell | Facade | Windows |")
    print("  Circulation | Elevator | Roof")
    print("=" * 64)


if __name__ == "__main__":
    main()
