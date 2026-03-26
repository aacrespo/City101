"""
LOCK 04 — VERTICAL CONNECTOR (v0 — no knowledge base)
Node 4, km 25 — Nyon (valley) to Genolier (hilltop)
LOG 200: Massing volumes, basic columns, simple openings
THIS IS A DELIBERATE "v0" SCRIPT — no archibase, no assembly logic,
no material layers, no playbook doctrine. For presentation comparison only.

TWO STATES: Valley <-> Hilltop
CONCEPT: A vertical connector bridging the 300m altitude difference
between Nyon station (lake level) and Genolier clinic (hilltop).
Dual-use infrastructure: commuter funicular by day, medical transport
by night. The "lock" is the threshold where horizontal rail meets
vertical ascent.

SPATIAL PLAN:
=============
    SITE_ORIGIN = approximate placement (no terrain survey yet)
    Estimated LV95: E ~2,510,000  N ~1,142,000  Z ~405m (Nyon station level)

    X = East-West (building width ~12m)
    Y = South-North (building depth ~24m, along valley-to-hill axis)
    Z = Up

    The concept: a station building at valley level with a tower element
    that marks the start of the vertical ascent. Three zones:
    - Base: arrival hall + waiting area (ground level, connects to rail)
    - Middle: transition zone + mechanical room (levels 1-2)
    - Tower: observation + signal (top, visible landmark)

    Overall: 12m (X) x 24m (Y) x 16m (Z, tower)
"""

import rhinoscriptsyntax as rs


# ---------------------------------------------------------------------------
# SITE PLACEMENT
# ---------------------------------------------------------------------------
# Approximate — no terrain data collected yet
# LV95 offset: E-2510000, N-1142000
SITE_ORIGIN = (0, 0, 405.0)


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


# ---------------------------------------------------------------------------
# LAYERS
# ---------------------------------------------------------------------------
def setup_layers():
    layers = {
        "Lock_04_v0::Volumes":     (160, 190, 180),
        "Lock_04_v0::Structure":   (90, 95, 100),
        "Lock_04_v0::Openings":    (200, 230, 255),
        "Lock_04_v0::Circulation": (230, 180, 140),
        "Lock_04_v0::FloorPlates": (210, 210, 200),
    }
    for name, color in layers.items():
        if not rs.IsLayer(name):
            rs.AddLayer(name, color)
    return layers


# ---------------------------------------------------------------------------
# VOLUMES — Base hall + tower
# ---------------------------------------------------------------------------
def create_volumes():
    rs.CurrentLayer("Lock_04_v0::Volumes")
    objs = []

    # Base — arrival hall (wide, low)
    base = box(-6, 0, 0, 6, 24, 4.5)
    rs.ObjectName(base, "Volume_Base_ArrivalHall")
    objs.append(base)

    # Tower — vertical signal element (narrow, tall)
    tower = box(-4, 8, 4.5, 4, 16, 16.0)
    rs.ObjectName(tower, "Volume_Tower_Vertical")
    objs.append(tower)

    return objs


# ---------------------------------------------------------------------------
# FLOOR PLATES
# ---------------------------------------------------------------------------
def create_floor_plates():
    rs.CurrentLayer("Lock_04_v0::FloorPlates")
    objs = []
    slab = 0.3

    # Ground floor (full base)
    ground = box(-6, 0, -slab, 6, 24, 0)
    rs.ObjectName(ground, "Floor_Ground")
    objs.append(ground)

    # Level 1 (base roof / tower floor)
    level1 = box(-6, 0, 4.5, 6, 24, 4.5 + slab)
    rs.ObjectName(level1, "Floor_Level1")
    objs.append(level1)

    # Tower levels
    level2 = box(-4, 8, 8.0, 4, 16, 8.0 + slab)
    rs.ObjectName(level2, "Floor_Level2_Tower")
    objs.append(level2)

    level3 = box(-4, 8, 12.0, 4, 16, 12.0 + slab)
    rs.ObjectName(level3, "Floor_Level3_Tower")
    objs.append(level3)

    # Tower roof
    roof = box(-4, 8, 16.0, 4, 16, 16.0 + slab)
    rs.ObjectName(roof, "Roof_Tower")
    objs.append(roof)

    return objs


# ---------------------------------------------------------------------------
# STRUCTURE — Columns (no structural logic, just boxes on a grid)
# ---------------------------------------------------------------------------
def create_structure():
    rs.CurrentLayer("Lock_04_v0::Structure")
    objs = []

    col_w = 0.3
    half = col_w / 2.0

    # Base columns — 6m grid
    x_positions = [-6, 0, 6]
    y_positions = [0, 6, 12, 18, 24]

    for x in x_positions:
        for y in y_positions:
            col = box(x - half, y - half, 0, x + half, y + half, 4.5)
            rs.ObjectName(col, "Col_Base_{}_{}".format(x, y))
            objs.append(col)

    # Tower columns — corners only
    tower_corners = [(-4, 8), (4, 8), (-4, 16), (4, 16)]
    for x, y in tower_corners:
        col = box(x - half, y - half, 4.5, x + half, y + half, 16.0)
        rs.ObjectName(col, "Col_Tower_{}_{}".format(x, y))
        objs.append(col)

    return objs


# ---------------------------------------------------------------------------
# OPENINGS — Simple rectangles (no frames, no glass, no reveals)
# ---------------------------------------------------------------------------
def create_openings():
    rs.CurrentLayer("Lock_04_v0::Openings")
    objs = []

    # South entrance (rail side)
    entrance = box(-3, -0.3, 0, 3, 0.3, 3.5)
    rs.ObjectName(entrance, "Opening_South_Entrance")
    objs.append(entrance)

    # North entrance (hill side)
    north = box(-2, 23.7, 0, 2, 24.3, 3.0)
    rs.ObjectName(north, "Opening_North_Exit")
    objs.append(north)

    # East/West windows — base level
    for side, y_face in [("East", 12), ("West", 12)]:
        x_face = 6 if side == "East" else -6
        for i in range(3):
            y = 4 + i * 8
            win = box(x_face - 0.3, y - 2, 1.0, x_face + 0.3, y + 2, 3.5)
            rs.ObjectName(win, "Window_Base_{}_{}".format(side, i))
            objs.append(win)

    # Tower windows — all four sides, each level
    for level, z_base in [(2, 8.0), (3, 12.0)]:
        # North and south tower faces
        for face, y_pos in [("North", 16), ("South", 8)]:
            win = box(-2.5, y_pos - 0.3, z_base + 0.8, 2.5, y_pos + 0.3, z_base + 3.0)
            rs.ObjectName(win, "Window_Tower_L{}_{}" .format(level, face))
            objs.append(win)
        # East and west tower faces
        for face, x_pos in [("East", 4), ("West", -4)]:
            win = box(x_pos - 0.3, 10, z_base + 0.8, x_pos + 0.3, 14, z_base + 3.0)
            rs.ObjectName(win, "Window_Tower_L{}_{}" .format(level, face))
            objs.append(win)

    return objs


# ---------------------------------------------------------------------------
# CIRCULATION — Single staircase in tower (no detail)
# ---------------------------------------------------------------------------
def create_circulation():
    rs.CurrentLayer("Lock_04_v0::Circulation")
    objs = []

    # Stair core — solid block (no individual treads, no rails)
    stair = box(-2, 9, 0, 2, 13, 16.0)
    rs.ObjectName(stair, "Stair_Tower_Block")
    objs.append(stair)

    return objs


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    rs.EnableRedraw(False)

    setup_layers()

    all_objs = []
    all_objs += create_volumes()
    all_objs += create_floor_plates()
    all_objs += create_structure()
    all_objs += create_openings()
    all_objs += create_circulation()

    rs.AddGroup("Lock_04_v0_Nyon")
    rs.AddObjectsToGroup(all_objs, "Lock_04_v0_Nyon")

    rs.EnableRedraw(True)
    rs.ZoomExtents()

    print("=" * 60)
    print("LOCK 04 — VERTICAL CONNECTOR (Nyon-Genolier, km 25)")
    print("v0 — No knowledge base, no playbook")
    print("=" * 60)
    print("Total objects: {}".format(len(all_objs)))
    print("")
    print("Volumes:      2  (base hall + tower)")
    print("Floor plates: 5  (ground, level 1, tower L2, tower L3, roof)")
    print("Columns:     {}  (grid + tower corners, no structural logic)".format(
        len([o for o in all_objs if rs.ObjectName(o) and rs.ObjectName(o).startswith("Col_")])))
    print("Openings:    {}  (simple rectangles, no frames)".format(
        len([o for o in all_objs if rs.ObjectName(o) and
             (rs.ObjectName(o).startswith("Opening_") or rs.ObjectName(o).startswith("Window_"))])))
    print("Circulation:  1  (stair block, no treads)")
    print("")
    print("WHAT'S MISSING (no archibase):")
    print("  - No wall assemblies (just volumes)")
    print("  - No material layers or thermal envelope")
    print("  - No foundation or ground interface")
    print("  - No window frames, reveals, or mullions")
    print("  - No stair treads, landings, or handrails")
    print("  - No accessibility compliance (SIA 500)")
    print("  - No roof drainage, parapets, or copings")
    print("  - No structural connections or load paths")
    print("  - No funicular/elevator mechanism")
    print("")
    print("Overall: 12m (X) x 24m (Y) x 16m (Z tower)")
    print("LOG level: 200 (massing only)")
    print("=" * 60)


if __name__ == "__main__":
    main()
