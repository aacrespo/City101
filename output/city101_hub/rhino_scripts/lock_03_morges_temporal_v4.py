"""
LOCK 03 — TEMPORAL LOCK (v4 — LOG 400)
Node 3, km 48 — EHC Morges hospital, next to Morges train station
LOG 400: Full assembly detail, materiality

v4 CHANGES (from v3 LOG 200-300):
- Volumes → 0.3m-thick wall panels split at openings
- Openings → recessed facade frames (0.15m depth reveals)
- Stair blocks → individual treads (10 per stair + landings)
- NEW: Ground connection (foundation strip, thresholds)
- NEW: Roof articulation (parapets, gate canopy overhang)
- Structure: existing columns + new perimeter edge beams

TWO STATES: Last train <-> First train (temporal gap 00:30-05:00)
CONCEPT: An airlock that holds night workers while time transitions.
Two chambers connected by a gate threshold.

SPATIAL PLAN (unchanged from v3):
    Night Chamber (west)     Gate      Dawn Chamber (east)
    [-17, -2]               [-2, 2]   [2, 17]
    15m wide                4m wide    15m wide
    6m tall                 8m tall    6m tall
    Y range: [-5, 5] (10m depth for all)
    Overall: 34m (X) x 10m (Y) x 8m (Z at gate)
"""

import rhinoscriptsyntax as rs


# ---------------------------------------------------------------------------
# SITE PLACEMENT
# ---------------------------------------------------------------------------
SITE_ORIGIN = (-60, 0, 381.5)

# ---------------------------------------------------------------------------
# WALL THICKNESS / DIMENSIONS
# ---------------------------------------------------------------------------
WALL_T = 0.3        # wall panel thickness
FRAME_D = 0.15      # facade frame depth (reveal)
SLAB_T = 0.3        # floor slab thickness
BEAM_W = 0.3        # beam width/height
COL_W = 0.3         # column width
PARAPET_H = 0.15    # parapet lip height
CANOPY_EXT = 1.5    # gate canopy extension beyond envelope
FOUND_DEPTH = 0.4   # foundation strip depth below grade
FOUND_W = 0.5       # foundation strip width


# ---------------------------------------------------------------------------
# HELPER
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


def named_box(x0, y0, z0, x1, y1, z1, name):
    """Create a named box."""
    obj = box(x0, y0, z0, x1, y1, z1)
    rs.ObjectName(obj, name)
    return obj


# ---------------------------------------------------------------------------
# LAYERS
# ---------------------------------------------------------------------------
def setup_layers():
    layers = {
        "Lock_03::Walls":       (180, 200, 220),
        "Lock_03::Structure":   (100, 100, 110),
        "Lock_03::FloorPlates": (220, 220, 210),
        "Lock_03::Facade":      (255, 220, 120),
        "Lock_03::Circulation": (200, 160, 160),
        "Lock_03::Ground":      (140, 130, 120),
        "Lock_03::Roof":        (200, 210, 220),
    }
    for name, color in layers.items():
        if not rs.IsLayer(name):
            rs.AddLayer(name, color)
    return layers


# ---------------------------------------------------------------------------
# 1. WALLS — 0.3m perimeter panels, split at openings
# ---------------------------------------------------------------------------
def create_walls():
    """Replace v3 solid volume envelopes with wall segments.

    Each chamber has N/S/E/W walls. Walls are split where openings exist
    (gaps left for windows/doors). The gate has only E/W walls (N/S are open passages).
    """
    rs.CurrentLayer("Lock_03::Walls")
    objs = []
    t = WALL_T  # 0.3m

    # --- NIGHT CHAMBER (x: -17 to -2, y: -5 to 5, h: 6m) ---

    # West wall — split for entrance door (y: -1.5 to 1.5, z: 0 to 3.5)
    # Below door: nothing needed (door is full height from ground)
    # Left of door (south side)
    objs.append(named_box(-17, -5, 0, -17+t, -1.5, 6, "Wall_Night_W_South"))
    # Right of door (north side)
    objs.append(named_box(-17, 1.5, 0, -17+t, 5, 6, "Wall_Night_W_North"))
    # Above door
    objs.append(named_box(-17, -1.5, 3.5, -17+t, 1.5, 6, "Wall_Night_W_Above"))

    # East wall (shared with gate west wall — gate side handles it)
    objs.append(named_box(-2-t, -5, 0, -2, 5, 6, "Wall_Night_E"))

    # North wall — split for 3 windows at x_centers [-14.5, -9.5, -4.5], each 2m wide, z: 1.5-4.5
    # Segments between windows (from west to east)
    n_win_edges = [(-17+t, -15.5), (-13.5, -10.5), (-8.5, -5.5), (-3.5, -2)]
    for i, (xa, xb) in enumerate(n_win_edges):
        objs.append(named_box(xa, 5-t, 0, xb, 5, 6, "Wall_Night_N_Seg_{}".format(i)))
    # Below windows (continuous strip)
    for j, xc in enumerate([-14.5, -9.5, -4.5]):
        objs.append(named_box(xc-1, 5-t, 0, xc+1, 5, 1.5, "Wall_Night_N_Below_{}".format(j)))
    # Above windows
    for j, xc in enumerate([-14.5, -9.5, -4.5]):
        objs.append(named_box(xc-1, 5-t, 4.5, xc+1, 5, 6, "Wall_Night_N_Above_{}".format(j)))

    # South wall (solid — no openings on night south)
    objs.append(named_box(-17+t, -5, 0, -2, -5+t, 6, "Wall_Night_S"))

    # --- DAWN CHAMBER (x: 2 to 17, y: -5 to 5, h: 6m) ---

    # East wall — split for large window (y: -3 to 3, z: 1 to 5.5)
    objs.append(named_box(17-t, -5, 0, 17, -3, 6, "Wall_Dawn_E_South"))
    objs.append(named_box(17-t, 3, 0, 17, 5, 6, "Wall_Dawn_E_North"))
    objs.append(named_box(17-t, -3, 0, 17, 3, 1, "Wall_Dawn_E_Below"))
    objs.append(named_box(17-t, -3, 5.5, 17, 3, 6, "Wall_Dawn_E_Above"))

    # West wall (shared with gate east wall — gate side handles it)
    objs.append(named_box(2, -5, 0, 2+t, 5, 6, "Wall_Dawn_W"))

    # South wall — split for 3 windows at x_centers [4.5, 9.5, 14.5], each 2.4m wide, z: 0.8-5.0
    s_win_edges = [(2, 3.3), (5.7, 8.3), (10.7, 13.3), (15.7, 17-t)]
    for i, (xa, xb) in enumerate(s_win_edges):
        objs.append(named_box(xa, -5, 0, xb, -5+t, 6, "Wall_Dawn_S_Seg_{}".format(i)))
    for j, xc in enumerate([4.5, 9.5, 14.5]):
        objs.append(named_box(xc-1.2, -5, 0, xc+1.2, -5+t, 0.8, "Wall_Dawn_S_Below_{}".format(j)))
    for j, xc in enumerate([4.5, 9.5, 14.5]):
        objs.append(named_box(xc-1.2, -5, 5.0, xc+1.2, -5+t, 6, "Wall_Dawn_S_Above_{}".format(j)))

    # North wall (solid — no openings on dawn north)
    objs.append(named_box(2, 5-t, 0, 17-t, 5, 6, "Wall_Dawn_N"))

    # --- GATE (x: -2 to 2, y: -5 to 5, h: 8m) ---
    # N and S are open passages — only E/W walls
    objs.append(named_box(-2, -5, 0, -2+t, 5, 8, "Wall_Gate_W"))
    objs.append(named_box(2-t, -5, 0, 2, 5, 8, "Wall_Gate_E"))

    return objs


# ---------------------------------------------------------------------------
# 2. FACADE — Recessed frames at openings
# ---------------------------------------------------------------------------
def create_facade():
    """Window and door frames creating depth/reveals at each opening."""
    rs.CurrentLayer("Lock_03::Facade")
    objs = []
    d = FRAME_D  # 0.15m frame depth

    # Night west entrance — door frame (y: -1.5 to 1.5, z: 0 to 3.5)
    # Frame surround: top + two sides
    objs.append(named_box(-17, -1.5, 3.5, -17+d, 1.5, 3.5+d, "Frame_Night_Door_Top"))
    objs.append(named_box(-17, -1.5, 0, -17+d, -1.5+d, 3.5, "Frame_Night_Door_Left"))
    objs.append(named_box(-17, 1.5-d, 0, -17+d, 1.5, 3.5, "Frame_Night_Door_Right"))

    # Night north windows — 3 frames at x_centers [-14.5, -9.5, -4.5], 2m wide, z: 1.5-4.5
    for j, xc in enumerate([-14.5, -9.5, -4.5]):
        # Top
        objs.append(named_box(xc-1, 5-d, 4.5, xc+1, 5, 4.5+d, "Frame_Night_NWin_{}_Top".format(j)))
        # Bottom (sill)
        objs.append(named_box(xc-1, 5-d, 1.5-d, xc+1, 5, 1.5, "Frame_Night_NWin_{}_Sill".format(j)))
        # Left
        objs.append(named_box(xc-1, 5-d, 1.5, xc-1+d, 5, 4.5, "Frame_Night_NWin_{}_L".format(j)))
        # Right
        objs.append(named_box(xc+1-d, 5-d, 1.5, xc+1, 5, 4.5, "Frame_Night_NWin_{}_R".format(j)))

    # Dawn east window — large frame (y: -3 to 3, z: 1 to 5.5)
    objs.append(named_box(17-d, -3, 5.5, 17, 3, 5.5+d, "Frame_Dawn_EWin_Top"))
    objs.append(named_box(17-d, -3, 1-d, 17, 3, 1, "Frame_Dawn_EWin_Sill"))
    objs.append(named_box(17-d, -3, 1, 17, -3+d, 5.5, "Frame_Dawn_EWin_L"))
    objs.append(named_box(17-d, 3-d, 1, 17, 3, 5.5, "Frame_Dawn_EWin_R"))

    # Dawn south windows — 3 frames at x_centers [4.5, 9.5, 14.5], 2.4m wide, z: 0.8-5.0
    for j, xc in enumerate([4.5, 9.5, 14.5]):
        objs.append(named_box(xc-1.2, -5, 5.0, xc+1.2, -5+d, 5.0+d, "Frame_Dawn_SWin_{}_Top".format(j)))
        objs.append(named_box(xc-1.2, -5, 0.8-d, xc+1.2, -5+d, 0.8, "Frame_Dawn_SWin_{}_Sill".format(j)))
        objs.append(named_box(xc-1.2, -5, 0.8, xc-1.2+d, -5+d, 5.0, "Frame_Dawn_SWin_{}_L".format(j)))
        objs.append(named_box(xc+1.2-d, -5, 0.8, xc+1.2, -5+d, 5.0, "Frame_Dawn_SWin_{}_R".format(j)))

    # Gate passage thresholds — floor strips marking N/S transitions
    objs.append(named_box(-2, 4.5, 0, 2, 5, 0.05, "Threshold_Gate_North"))
    objs.append(named_box(-2, -5, 0, 2, -4.5, 0.05, "Threshold_Gate_South"))

    return objs


# ---------------------------------------------------------------------------
# 3. CIRCULATION — Individual stair treads + landings
# ---------------------------------------------------------------------------
def create_circulation():
    """Replace solid stair blocks with 10 treads + landing per stair.

    Each stair: 3.0m total rise, 10 treads
    Tread: 0.30m rise x 0.28m run x 2.0m wide (4m span in Y: -2 to 2)
    Run direction: along X axis
    Night stair: x from -5 going east to -3 (landing at top)
    Dawn stair: x from 3 going east to 5 (landing at top)
    """
    rs.CurrentLayer("Lock_03::Circulation")
    objs = []

    rise = 0.30     # per tread
    run = 0.18      # tread depth (run) — 10 treads = 1.8m, leaves 0.2m landing
    width = 4.0     # Y span: -2 to 2
    tread_t = 0.05  # tread thickness

    # --- Night stair (x: -5 to -3, going up west to east) ---
    for i in range(10):
        z_bot = i * rise
        z_top = z_bot + tread_t
        x0 = -5 + i * run
        x1 = x0 + run
        objs.append(named_box(x0, -2, z_bot, x1, 2, z_top, "Tread_Night_{}".format(i)))

    # Night landing at top
    objs.append(named_box(-5 + 10*run, -2, 3.0 - tread_t, -3, 2, 3.0, "Landing_Night"))

    # --- Dawn stair (x: 3 to 5, going up west to east) ---
    for i in range(10):
        z_bot = i * rise
        z_top = z_bot + tread_t
        x0 = 3 + i * run
        x1 = x0 + run
        objs.append(named_box(x0, -2, z_bot, x1, 2, z_top, "Tread_Dawn_{}".format(i)))

    # Dawn landing at top
    objs.append(named_box(3 + 10*run, -2, 3.0 - tread_t, 5, 2, 3.0, "Landing_Dawn"))

    return objs


# ---------------------------------------------------------------------------
# 4. GROUND — Foundation, thresholds, plinth
# ---------------------------------------------------------------------------
def create_ground():
    """Foundation strip, entrance threshold ramp, plinth step."""
    rs.CurrentLayer("Lock_03::Ground")
    objs = []

    fd = FOUND_DEPTH  # 0.4m below grade
    fw = FOUND_W      # 0.5m wide

    # Perimeter foundation strip (runs around entire lock footprint)
    # North edge
    objs.append(named_box(-17, 5-fw, -fd, 17, 5, 0, "Foundation_North"))
    # South edge
    objs.append(named_box(-17, -5, -fd, 17, -5+fw, 0, "Foundation_South"))
    # West edge
    objs.append(named_box(-17, -5+fw, -fd, -17+fw, 5-fw, 0, "Foundation_West"))
    # East edge
    objs.append(named_box(17-fw, -5+fw, -fd, 17, 5-fw, 0, "Foundation_East"))

    # Night west entrance threshold ramp (gentle slope, 1.5m long)
    # Modeled as a wedge-approximation: thin slab tapering from 0.1m to 0
    objs.append(named_box(-18.5, -1.5, -0.05, -17, 1.5, 0.1, "Threshold_Ramp_Night"))

    # Dawn east plinth step (0.15m high step at facade)
    objs.append(named_box(17, -3.5, 0, 17.5, 3.5, 0.15, "Plinth_Dawn_East"))

    return objs


# ---------------------------------------------------------------------------
# 5. ROOF — Parapets + gate canopy overhang
# ---------------------------------------------------------------------------
def create_roof():
    """Parapet lips on chamber roofs + gate canopy extending beyond envelope."""
    rs.CurrentLayer("Lock_03::Roof")
    objs = []

    p = PARAPET_H  # 0.15m
    slab_z_chamber = 6.0 + SLAB_T  # top of roof slab = 6.3
    slab_z_gate = 8.0 + SLAB_T     # top of gate roof = 8.3
    ext = CANOPY_EXT  # 1.5m

    # Night chamber parapets (on top of roof slab at z=6.3)
    objs.append(named_box(-17, 5-WALL_T, slab_z_chamber, -2, 5, slab_z_chamber+p, "Parapet_Night_N"))
    objs.append(named_box(-17, -5, slab_z_chamber, -2, -5+WALL_T, slab_z_chamber+p, "Parapet_Night_S"))
    objs.append(named_box(-17, -5, slab_z_chamber, -17+WALL_T, 5, slab_z_chamber+p, "Parapet_Night_W"))
    objs.append(named_box(-2-WALL_T, -5, slab_z_chamber, -2, 5, slab_z_chamber+p, "Parapet_Night_E"))

    # Dawn chamber parapets
    objs.append(named_box(2, 5-WALL_T, slab_z_chamber, 17, 5, slab_z_chamber+p, "Parapet_Dawn_N"))
    objs.append(named_box(2, -5, slab_z_chamber, 17, -5+WALL_T, slab_z_chamber+p, "Parapet_Dawn_S"))
    objs.append(named_box(17-WALL_T, -5, slab_z_chamber, 17, 5, slab_z_chamber+p, "Parapet_Dawn_W"))
    objs.append(named_box(2, -5, slab_z_chamber, 2+WALL_T, 5, slab_z_chamber+p, "Parapet_Dawn_E"))

    # Gate canopy — roof slab extends 1.5m beyond N and S
    # North canopy extension
    objs.append(named_box(-2, 5, 8.0, 2, 5+ext, 8.0+SLAB_T, "Canopy_Gate_North"))
    # South canopy extension
    objs.append(named_box(-2, -5-ext, 8.0, 2, -5, 8.0+SLAB_T, "Canopy_Gate_South"))

    return objs


# ---------------------------------------------------------------------------
# 6. FLOOR PLATES — Unchanged from v3
# ---------------------------------------------------------------------------
def create_floor_plates():
    rs.CurrentLayer("Lock_03::FloorPlates")
    objs = []

    t = SLAB_T

    objs.append(named_box(-17, -5, -t, 17, 5, 0, "Ground_Slab"))
    objs.append(named_box(-17, -5, 3.0, -2, 5, 3.0+t, "Upper_Floor_Night"))
    objs.append(named_box(2, -5, 3.0, 17, 5, 3.0+t, "Upper_Floor_Dawn"))
    objs.append(named_box(-17, -5, 6.0, -2, 5, 6.0+t, "Roof_Night"))
    objs.append(named_box(-2, -5, 8.0, 2, 5, 8.0+t, "Roof_Gate"))
    objs.append(named_box(2, -5, 6.0, 17, 5, 6.0+t, "Roof_Dawn"))

    return objs


# ---------------------------------------------------------------------------
# 7. STRUCTURE — Columns (v3) + new perimeter edge beams
# ---------------------------------------------------------------------------
def create_structure():
    """20 columns from v3 + 8 perimeter beams at upper floor level (Z=3.0)."""
    rs.CurrentLayer("Lock_03::Structure")
    objs = []

    half = COL_W / 2.0

    # --- Columns (unchanged from v3) ---
    night_xs = [-17, -12, -7, -2]
    dawn_xs  = [2, 7, 12, 17]
    gate_xs  = [-2, 2]
    ys = [-4.5, 4.5]

    for x in night_xs:
        for y in ys:
            objs.append(named_box(x-half, y-half, 0, x+half, y+half, 6,
                                  "Col_Night_{}_{}".format(x, int(y))))

    for x in dawn_xs:
        for y in ys:
            objs.append(named_box(x-half, y-half, 0, x+half, y+half, 6,
                                  "Col_Dawn_{}_{}".format(x, int(y))))

    for x in gate_xs:
        for y in ys:
            objs.append(named_box(x-half, y-half, 0, x+half, y+half, 8,
                                  "Col_Gate_{}_{}".format(x, int(y))))

    # --- Edge beams at Z=3.0 (upper floor level) ---
    bw = BEAM_W  # 0.3m
    beam_z = 3.0 - bw  # beam bottom = 2.7, top = 3.0 (sits below slab)

    # Night chamber beams (along edges at y=-4.5 and y=4.5)
    objs.append(named_box(-17, 4.5-half, beam_z, -2, 4.5+half, 3.0, "Beam_Night_N"))
    objs.append(named_box(-17, -4.5-half, beam_z, -2, -4.5+half, 3.0, "Beam_Night_S"))
    # Night E-W beams (short spans along Y at x=-17 and x=-2)
    objs.append(named_box(-17, -4.5, beam_z, -17+bw, 4.5, 3.0, "Beam_Night_W"))
    objs.append(named_box(-2-bw, -4.5, beam_z, -2, 4.5, 3.0, "Beam_Night_E"))

    # Dawn chamber beams
    objs.append(named_box(2, 4.5-half, beam_z, 17, 4.5+half, 3.0, "Beam_Dawn_N"))
    objs.append(named_box(2, -4.5-half, beam_z, 17, -4.5+half, 3.0, "Beam_Dawn_S"))
    objs.append(named_box(2, -4.5, beam_z, 2+bw, 4.5, 3.0, "Beam_Dawn_W"))
    objs.append(named_box(17-bw, -4.5, beam_z, 17, 4.5, 3.0, "Beam_Dawn_E"))

    return objs


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    rs.EnableRedraw(False)

    setup_layers()

    all_objs = []
    counts = {}

    walls = create_walls()
    all_objs += walls
    counts["Walls"] = len(walls)

    facade = create_facade()
    all_objs += facade
    counts["Facade"] = len(facade)

    circulation = create_circulation()
    all_objs += circulation
    counts["Circulation"] = len(circulation)

    ground = create_ground()
    all_objs += ground
    counts["Ground"] = len(ground)

    roof = create_roof()
    all_objs += roof
    counts["Roof"] = len(roof)

    floors = create_floor_plates()
    all_objs += floors
    counts["FloorPlates"] = len(floors)

    structure = create_structure()
    all_objs += structure
    counts["Structure"] = len(structure)

    rs.AddGroup("Lock_03_Morges_Temporal_v4")
    rs.AddObjectsToGroup(all_objs, "Lock_03_Morges_Temporal_v4")

    rs.EnableRedraw(True)
    rs.ZoomExtents()

    total = len(all_objs)

    print("=" * 60)
    print("LOCK 03 — TEMPORAL LOCK (Morges, km 48)")
    print("v4 — LOG 400: Full assembly detail")
    print("Site-placed at ({}, {}, {})".format(*SITE_ORIGIN))
    print("=" * 60)
    print("Total objects created: {}".format(total))
    print("")
    for cat, n in counts.items():
        print("  {:<14s} {:>3d}".format(cat, n))
    print("")
    print("Overall dimensions: 34m (X) x 10m (Y) x 8m (Z at gate)")
    print("LOG level: 400")
    print("LV95 offset: E-2527500, N-1151500")
    print("=" * 60)

    return total


if __name__ == "__main__":
    main()
