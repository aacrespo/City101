"""
LOCK 03 — TEMPORAL LOCK (v3 — Site-placed)
Node 3, km 48 — EHC Morges hospital, next to Morges train station
LOG 200-300: Defined volumes, floor plates, structural rhythm, key openings

v3 CHANGES:
- Added SITE_ORIGIN parameter for placement on real terrain
- All geometry offset by SITE_ORIGIN during creation
- Coordinate system: local origin with offset from LV95
  Offset: E-2527500, N-1151500 (stored as metadata dot on terrain)

TWO STATES: Last train <-> First train (temporal gap 00:30-05:00)
CONCEPT: An airlock that holds night workers while time transitions.
Two chambers connected by a gate threshold.

SPATIAL PLAN:
=============
    SITE_ORIGIN = where the lock sits on the terrain (local coords)
    All geometry is created relative to SITE_ORIGIN.

    Local origin of lock = ground level, center of Gate Threshold (long axis),
    THEN shifted by SITE_ORIGIN.

    X = East-West (total ~34m: Night chamber west, Gate center, Dawn chamber east)
    Y = North-South (depth ~10m)
    Z = Up (max height ~8m at Gate)

    LAYOUT (plan view, X coordinates):

    Night Chamber (west)     Gate      Dawn Chamber (east)
    [-17, -2]               [-2, 2]   [2, 17]
    15m wide                4m wide    15m wide
    6m tall                 8m tall    6m tall

    Y range: [-5, 5] (10m depth for all)

    Overall: 34m (X) x 10m (Y) x 8m (Z at gate)
"""

import rhinoscriptsyntax as rs


# ---------------------------------------------------------------------------
# SITE PLACEMENT — v3
# ---------------------------------------------------------------------------
# Local coordinates (offset from LV95 by E-2527500, N-1151500)
# Morges hospital: terrain elevation ~392m
SITE_ORIGIN = (0, 15, 392.0)


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
        "Lock_03::Volumes":      (180, 200, 220),   # cool blue-grey
        "Lock_03::Structure":    (100, 100, 110),    # dark grey
        "Lock_03::Openings":     (255, 220, 120),    # warm amber
        "Lock_03::Circulation":  (200, 160, 160),    # muted rose
        "Lock_03::FloorPlates":  (220, 220, 210),    # off-white
    }
    for name, color in layers.items():
        if not rs.IsLayer(name):
            rs.AddLayer(name, color)
    return layers


# ---------------------------------------------------------------------------
# VOLUMES — Main envelopes for each chamber and gate
# ---------------------------------------------------------------------------
def create_volumes():
    rs.CurrentLayer("Lock_03::Volumes")
    objs = []

    night = box(-17, -5, 0, -2, 5, 6)
    rs.ObjectName(night, "Night_Chamber_Envelope")
    objs.append(night)

    gate = box(-2, -5, 0, 2, 5, 8)
    rs.ObjectName(gate, "Gate_Threshold_Envelope")
    objs.append(gate)

    dawn = box(2, -5, 0, 17, 5, 6)
    rs.ObjectName(dawn, "Dawn_Chamber_Envelope")
    objs.append(dawn)

    return objs


# ---------------------------------------------------------------------------
# FLOOR PLATES
# ---------------------------------------------------------------------------
def create_floor_plates():
    rs.CurrentLayer("Lock_03::FloorPlates")
    objs = []

    slab_thick = 0.3

    ground = box(-17, -5, -slab_thick, 17, 5, 0)
    rs.ObjectName(ground, "Ground_Slab")
    objs.append(ground)

    upper_night = box(-17, -5, 3.0, -2, 5, 3.0 + slab_thick)
    rs.ObjectName(upper_night, "Upper_Floor_Night")
    objs.append(upper_night)

    upper_dawn = box(2, -5, 3.0, 17, 5, 3.0 + slab_thick)
    rs.ObjectName(upper_dawn, "Upper_Floor_Dawn")
    objs.append(upper_dawn)

    roof_night = box(-17, -5, 6.0, -2, 5, 6.0 + slab_thick)
    rs.ObjectName(roof_night, "Roof_Night")
    objs.append(roof_night)

    roof_gate = box(-2, -5, 8.0, 2, 5, 8.0 + slab_thick)
    rs.ObjectName(roof_gate, "Roof_Gate")
    objs.append(roof_gate)

    roof_dawn = box(2, -5, 6.0, 17, 5, 6.0 + slab_thick)
    rs.ObjectName(roof_dawn, "Roof_Dawn")
    objs.append(roof_dawn)

    return objs


# ---------------------------------------------------------------------------
# STRUCTURE — Columns at 5m rhythm
# ---------------------------------------------------------------------------
def create_structure():
    rs.CurrentLayer("Lock_03::Structure")
    objs = []

    col_w = 0.3
    half = col_w / 2.0

    night_xs = [-17, -12, -7, -2]
    dawn_xs  = [2, 7, 12, 17]
    gate_xs  = [-2, 2]
    ys = [-4.5, 4.5]

    for x in night_xs:
        for y in ys:
            col = box(x - half, y - half, 0, x + half, y + half, 6)
            rs.ObjectName(col, "Col_Night_{}_{}".format(x, int(y)))
            objs.append(col)

    for x in dawn_xs:
        for y in ys:
            col = box(x - half, y - half, 0, x + half, y + half, 6)
            rs.ObjectName(col, "Col_Dawn_{}_{}".format(x, int(y)))
            objs.append(col)

    for x in gate_xs:
        for y in ys:
            col = box(x - half, y - half, 0, x + half, y + half, 8)
            rs.ObjectName(col, "Col_Gate_{}_{}".format(x, int(y)))
            objs.append(col)

    return objs


# ---------------------------------------------------------------------------
# OPENINGS
# ---------------------------------------------------------------------------
def create_openings():
    rs.CurrentLayer("Lock_03::Openings")
    objs = []

    dawn_window = box(16.5, -3, 1, 17.5, 3, 5.5)
    rs.ObjectName(dawn_window, "Opening_Dawn_EastWindow")
    objs.append(dawn_window)

    night_entrance = box(-17.5, -1.5, 0, -16.5, 1.5, 3.5)
    rs.ObjectName(night_entrance, "Opening_Night_WestEntrance")
    objs.append(night_entrance)

    gate_north = box(-2, 4.5, 0, 2, 5.5, 6)
    rs.ObjectName(gate_north, "Opening_Gate_North")
    objs.append(gate_north)

    gate_south = box(-2, -5.5, 0, 2, -4.5, 6)
    rs.ObjectName(gate_south, "Opening_Gate_South")
    objs.append(gate_south)

    for i, x_center in enumerate([-14.5, -9.5, -4.5]):
        win = box(x_center - 1, 4.5, 1.5, x_center + 1, 5.5, 4.5)
        rs.ObjectName(win, "Opening_Night_NorthWin_{}".format(i))
        objs.append(win)

    for i, x_center in enumerate([4.5, 9.5, 14.5]):
        win = box(x_center - 1.2, -5.5, 0.8, x_center + 1.2, -4.5, 5.0)
        rs.ObjectName(win, "Opening_Dawn_SouthWin_{}".format(i))
        objs.append(win)

    return objs


# ---------------------------------------------------------------------------
# CIRCULATION
# ---------------------------------------------------------------------------
def create_circulation():
    rs.CurrentLayer("Lock_03::Circulation")
    objs = []

    stair_night = box(-5, -2, 0, -3, 2, 3.3)
    rs.ObjectName(stair_night, "Stair_Night")
    objs.append(stair_night)

    stair_dawn = box(3, -2, 0, 5, 2, 3.3)
    rs.ObjectName(stair_dawn, "Stair_Dawn")
    objs.append(stair_dawn)

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

    rs.AddGroup("Lock_03_Morges_Temporal_Sited")
    rs.AddObjectsToGroup(all_objs, "Lock_03_Morges_Temporal_Sited")

    rs.EnableRedraw(True)
    rs.ZoomExtents()

    print("=" * 60)
    print("LOCK 03 — TEMPORAL LOCK (Morges, km 48)")
    print("v3 — Site-placed at ({}, {}, {})".format(*SITE_ORIGIN))
    print("=" * 60)
    print("Total objects created: {}".format(len(all_objs)))
    print("")
    print("Volumes:     3  (Night Chamber, Gate Threshold, Dawn Chamber)")
    print("Floor plates: 6  (ground slab, 2 upper floors, 3 roof slabs)")
    print("Columns:     20 (8 night + 8 dawn + 4 gate)")
    print("Openings:    10 (dawn east window, night entrance, 2 gate passages, 6 secondary)")
    print("Circulation:  2  (night stair, dawn stair)")
    print("")
    print("Overall dimensions: 34m (X) x 10m (Y) x 8m (Z at gate)")
    print("LOG level: 200-300")
    print("Site origin: local ({}, {}, {})".format(*SITE_ORIGIN))
    print("LV95 offset: E-2527500, N-1151500")
    print("=" * 60)


if __name__ == "__main__":
    main()
