"""
LOCK 05 — VISIBILITY LOCK (v0 — no knowledge base)
Node 5, km 58-62 — Crissier-Bussigny logistics belt
LOG 200: Massing volumes, basic columns, simple openings
THIS IS A DELIBERATE "v0" SCRIPT — no archibase, no assembly logic,
no material layers, no playbook doctrine. For presentation comparison only.

TWO STATES: Invisible <-> Visible
CONCEPT: Service elevator revealing hidden supply chain infrastructure.
Makes logistics (PLEXUS, CHUV kitchen, Galexis, B. Braun, La Poste)
legible as civic space.

SPATIAL PLAN:
=============
    SITE_ORIGIN = approximate placement (no terrain survey yet)
    Estimated LV95: E ~2,533,000  N ~1,151,500  Z ~465m

    X = East-West (building length ~60m, long logistics hall)
    Y = South-North (building depth ~18m)
    Z = Up

    The concept: a long transparent hall where supply chain flows
    become visible through glass walls. Two levels:
    - Ground: logistics sorting + public viewing corridor
    - Upper: staff coordination + observation deck

    Overall: 60m (X) x 18m (Y) x 8m (Z)
"""

import rhinoscriptsyntax as rs


# ---------------------------------------------------------------------------
# SITE PLACEMENT
# ---------------------------------------------------------------------------
# Approximate — no terrain data collected yet
# LV95 offset: E-2533000, N-1151500
SITE_ORIGIN = (0, 0, 465.0)


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
        "Lock_05_v0::Volumes":     (160, 190, 180),
        "Lock_05_v0::Structure":   (90, 95, 100),
        "Lock_05_v0::Openings":    (200, 230, 255),
        "Lock_05_v0::Circulation": (230, 180, 140),
        "Lock_05_v0::FloorPlates": (210, 210, 200),
    }
    for name, color in layers.items():
        if not rs.IsLayer(name):
            rs.AddLayer(name, color)
    return layers


# ---------------------------------------------------------------------------
# VOLUMES — Two-level logistics hall
# ---------------------------------------------------------------------------
def create_volumes():
    rs.CurrentLayer("Lock_05_v0::Volumes")
    objs = []

    # Ground level — logistics sorting + public corridor
    ground = box(-30, 0, 0, 30, 18, 4.0)
    rs.ObjectName(ground, "Volume_Ground_Logistics")
    objs.append(ground)

    # Upper level — staff coordination + observation
    upper = box(-30, 0, 4.0, 30, 18, 8.0)
    rs.ObjectName(upper, "Volume_Upper_Staff")
    objs.append(upper)

    return objs


# ---------------------------------------------------------------------------
# FLOOR PLATES
# ---------------------------------------------------------------------------
def create_floor_plates():
    rs.CurrentLayer("Lock_05_v0::FloorPlates")
    objs = []
    slab = 0.3

    # Ground floor
    ground = box(-30, 0, -slab, 30, 18, 0)
    rs.ObjectName(ground, "Floor_Ground")
    objs.append(ground)

    # First floor
    first = box(-30, 0, 4.0, 30, 18, 4.0 + slab)
    rs.ObjectName(first, "Floor_First")
    objs.append(first)

    # Roof
    roof = box(-30, 0, 8.0, 30, 18, 8.0 + slab)
    rs.ObjectName(roof, "Roof")
    objs.append(roof)

    return objs


# ---------------------------------------------------------------------------
# STRUCTURE — Columns on 6m grid (no structural logic, just boxes)
# ---------------------------------------------------------------------------
def create_structure():
    rs.CurrentLayer("Lock_05_v0::Structure")
    objs = []

    col_w = 0.3
    half = col_w / 2.0

    x_positions = range(-30, 31, 6)
    y_positions = [0, 9, 18]

    for x in x_positions:
        for y in y_positions:
            # Ground to roof — single column, no splice, no connection detail
            col = box(x - half, y - half, 0, x + half, y + half, 8.0)
            rs.ObjectName(col, "Col_{}_{}".format(x, y))
            objs.append(col)

    return objs


# ---------------------------------------------------------------------------
# OPENINGS — Simple rectangular holes (no frames, no glass, no reveals)
# ---------------------------------------------------------------------------
def create_openings():
    rs.CurrentLayer("Lock_05_v0::Openings")
    objs = []

    # South facade — large openings for logistics access (ground level)
    for i, x in enumerate(range(-24, 25, 12)):
        opening = box(x - 4, -0.3, 0.5, x + 4, 0.3, 3.5)
        rs.ObjectName(opening, "Opening_South_{}".format(i))
        objs.append(opening)

    # North facade — glazing panels (visibility concept, both levels)
    for level, z_base in [(0, 0), (1, 4.0)]:
        for i, x in enumerate(range(-27, 28, 6)):
            win = box(x - 2.5, 17.7, z_base + 0.8, x + 2.5, 18.3, z_base + 3.5)
            rs.ObjectName(win, "Glazing_North_L{}_{}".format(level, i))
            objs.append(win)

    # Main entrance
    entrance = box(-3, -0.3, 0, 3, 0.3, 3.2)
    rs.ObjectName(entrance, "Opening_MainEntrance")
    objs.append(entrance)

    return objs


# ---------------------------------------------------------------------------
# CIRCULATION — Single staircase + basic ramp (no detail)
# ---------------------------------------------------------------------------
def create_circulation():
    rs.CurrentLayer("Lock_05_v0::Circulation")
    objs = []

    # Staircase — just a solid block (no individual treads)
    stair = box(24, 2, 0, 29, 8, 4.0)
    rs.ObjectName(stair, "Stair_East_Block")
    objs.append(stair)

    # Ramp — single wedge (no landings, no anti-slip, no rails)
    ramp_pts = [
        (-29, 2, 0),    (-24, 2, 0),
        (-24, 8, 4.0),  (-29, 8, 4.0),
        (-29, 2, 0.3),  (-24, 2, 0.3),
        (-24, 8, 4.3),  (-29, 8, 4.3),
    ]
    ox, oy, oz = SITE_ORIGIN
    ramp = rs.AddBox([(p[0]+ox, p[1]+oy, p[2]+oz) for p in ramp_pts])
    rs.ObjectName(ramp, "Ramp_West_Block")
    objs.append(ramp)

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

    rs.AddGroup("Lock_05_v0_Crissier")
    rs.AddObjectsToGroup(all_objs, "Lock_05_v0_Crissier")

    rs.EnableRedraw(True)
    rs.ZoomExtents()

    print("=" * 60)
    print("LOCK 05 — VISIBILITY LOCK (Crissier-Bussigny, km 58)")
    print("v0 — No knowledge base, no playbook")
    print("=" * 60)
    print("Total objects: {}".format(len(all_objs)))
    print("")
    print("Volumes:      2  (ground + upper)")
    print("Floor plates: 3  (ground, first, roof)")
    print("Columns:     {}  (6m grid, no structural logic)".format(
        len([o for o in all_objs if rs.ObjectName(o) and rs.ObjectName(o).startswith("Col_")])))
    print("Openings:    {}  (simple rectangles, no frames)".format(
        len([o for o in all_objs if rs.ObjectName(o) and
             (rs.ObjectName(o).startswith("Opening_") or rs.ObjectName(o).startswith("Glazing_"))])))
    print("Circulation:  2  (stair block + ramp block)")
    print("")
    print("WHAT'S MISSING (no archibase):")
    print("  - No wall assemblies (just volumes)")
    print("  - No material layers or thermal envelope")
    print("  - No foundation detail")
    print("  - No window frames, reveals, or mullions")
    print("  - No stair treads or ramp landings")
    print("  - No guardrails or accessibility compliance")
    print("  - No roof drainage or parapets")
    print("  - No structural connections")
    print("")
    print("Overall: 60m (X) x 18m (Y) x 8m (Z)")
    print("LOG level: 200 (massing only)")
    print("=" * 60)


if __name__ == "__main__":
    main()
