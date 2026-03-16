"""
LOCK 03 — TEMPORAL LOCK
Node 3, km 48 — EHC Morges hospital, next to Morges train station
LOG 200-300: Defined volumes, floor plates, structural rhythm, key openings

TWO STATES: Last train <-> First train (temporal gap 00:30-05:00)
CONCEPT: An airlock that holds night workers while time transitions.
Two chambers connected by a gate threshold.

SPATIAL PLAN:
=============
    Origin (0,0,0) = ground level, center of Gate Threshold (long axis)
    X = East-West (total ~34m: Night chamber west, Gate center, Dawn chamber east)
    Y = North-South (depth ~10m)
    Z = Up (max height ~8m at Gate)

    LAYOUT (plan view, X coordinates):

    Night Chamber (west)     Gate      Dawn Chamber (east)
    [-17, -2]               [-2, 2]   [2, 17]
    15m wide                4m wide    15m wide
    6m tall                 8m tall    6m tall

    Y range: [-5, 5] (10m depth for all)

    FLOOR PLATES:
    - Ground floor: Z = 0 (all chambers)
    - Upper floor:  Z = 3.0 (both chambers, slab thickness 0.3m)
    - Gate has no intermediate floor (full-height void)

    STRUCTURAL RHYTHM:
    - Columns at 5m spacing along X axis
    - Night chamber columns at X = -17, -12, -7, -2
    - Dawn chamber columns at X = 2, 7, 12, 17
    - Column pairs at Y = -4.5 and Y = 4.5 (inset 0.5m from facade)
    - Column size: 0.3m x 0.3m

    KEY OPENINGS:
    - East face of Dawn chamber: large window (catches first light)
      X = 17, Y = [-3, 3], Z = [1, 5.5]
    - West face of Night chamber: sheltered entrance
      X = -17, Y = [-1.5, 1.5], Z = [0, 3.5]
    - Gate threshold: open on north and south faces at ground level
      X = [-2, 2], Y = [-5, -5] and [5, 5], Z = [0, 6]
"""

import rhinoscriptsyntax as rs


# ---------------------------------------------------------------------------
# HELPER
# ---------------------------------------------------------------------------
def box(x0, y0, z0, x1, y1, z1):
    """Create a box from min/max corners. No ambiguity."""
    pts = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
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

    # Night Chamber envelope (west) — 15m x 10m x 6m
    night = box(-17, -5, 0, -2, 5, 6)
    rs.ObjectName(night, "Night_Chamber_Envelope")
    objs.append(night)

    # Gate Threshold envelope (center) — 4m x 10m x 8m (taller)
    gate = box(-2, -5, 0, 2, 5, 8)
    rs.ObjectName(gate, "Gate_Threshold_Envelope")
    objs.append(gate)

    # Dawn Chamber envelope (east) — 15m x 10m x 6m
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

    # Ground slab — full footprint
    ground = box(-17, -5, -slab_thick, 17, 5, 0)
    rs.ObjectName(ground, "Ground_Slab")
    objs.append(ground)

    # Upper floor — Night Chamber (Z = 3.0)
    upper_night = box(-17, -5, 3.0, -2, 5, 3.0 + slab_thick)
    rs.ObjectName(upper_night, "Upper_Floor_Night")
    objs.append(upper_night)

    # Upper floor — Dawn Chamber (Z = 3.0)
    upper_dawn = box(2, -5, 3.0, 17, 5, 3.0 + slab_thick)
    rs.ObjectName(upper_dawn, "Upper_Floor_Dawn")
    objs.append(upper_dawn)

    # Gate has NO intermediate floor — full-height void

    # Roof slabs
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

    col_w = 0.3   # column width
    half = col_w / 2.0

    # Column X positions
    night_xs = [-17, -12, -7, -2]
    dawn_xs  = [2, 7, 12, 17]
    gate_xs  = [-2, 2]

    # Column Y positions (inset 0.5m from facade edges at +/-5)
    ys = [-4.5, 4.5]

    # Night chamber columns (height 6m)
    for x in night_xs:
        for y in ys:
            col = box(x - half, y - half, 0, x + half, y + half, 6)
            rs.ObjectName(col, "Col_Night_{}_{:.0f}".format(x, y))
            objs.append(col)

    # Dawn chamber columns (height 6m)
    for x in dawn_xs:
        for y in ys:
            col = box(x - half, y - half, 0, x + half, y + half, 6)
            rs.ObjectName(col, "Col_Dawn_{}_{:.0f}".format(x, y))
            objs.append(col)

    # Gate threshold columns (height 8m) — only at edges X = -2 and X = 2
    for x in gate_xs:
        for y in ys:
            col = box(x - half, y - half, 0, x + half, y + half, 8)
            rs.ObjectName(col, "Col_Gate_{}_{:.0f}".format(x, y))
            objs.append(col)

    return objs


# ---------------------------------------------------------------------------
# OPENINGS — Subtractive voids (modeled as positive volumes on Openings layer)
# ---------------------------------------------------------------------------
def create_openings():
    rs.CurrentLayer("Lock_03::Openings")
    objs = []

    # East face of Dawn Chamber — large window catching first light
    # Full east wall void: X = 16.8-17.2 (through wall), Y = [-3, 3], Z = [1, 5.5]
    dawn_window = box(16.5, -3, 1, 17.5, 3, 5.5)
    rs.ObjectName(dawn_window, "Opening_Dawn_EastWindow")
    objs.append(dawn_window)

    # West face of Night Chamber — sheltered entrance
    # X = -17.5 to -16.5 (through wall), Y = [-1.5, 1.5], Z = [0, 3.5]
    night_entrance = box(-17.5, -1.5, 0, -16.5, 1.5, 3.5)
    rs.ObjectName(night_entrance, "Opening_Night_WestEntrance")
    objs.append(night_entrance)

    # Gate threshold — north passage (open at ground level)
    gate_north = box(-2, 4.5, 0, 2, 5.5, 6)
    rs.ObjectName(gate_north, "Opening_Gate_North")
    objs.append(gate_north)

    # Gate threshold — south passage (open at ground level)
    gate_south = box(-2, -5.5, 0, 2, -4.5, 6)
    rs.ObjectName(gate_south, "Opening_Gate_South")
    objs.append(gate_south)

    # Secondary windows — Night chamber north face (warmth/glow)
    for i, x_center in enumerate([-14.5, -9.5, -4.5]):
        win = box(x_center - 1, 4.5, 1.5, x_center + 1, 5.5, 4.5)
        rs.ObjectName(win, "Opening_Night_NorthWin_{}".format(i))
        objs.append(win)

    # Secondary windows — Dawn chamber south face (activation)
    for i, x_center in enumerate([4.5, 9.5, 14.5]):
        win = box(x_center - 1.2, -5.5, 0.8, x_center + 1.2, -4.5, 5.0)
        rs.ObjectName(win, "Opening_Dawn_SouthWin_{}".format(i))
        objs.append(win)

    return objs


# ---------------------------------------------------------------------------
# CIRCULATION — Internal stairs / ramps connecting floor levels
# ---------------------------------------------------------------------------
def create_circulation():
    rs.CurrentLayer("Lock_03::Circulation")
    objs = []

    # Stair in Night Chamber — connecting ground to upper floor
    # Located near the gate side, X = [-5, -3], Y = [-2, 2]
    # Modeled as a solid volume representing stair enclosure
    stair_night = box(-5, -2, 0, -3, 2, 3.3)
    rs.ObjectName(stair_night, "Stair_Night")
    objs.append(stair_night)

    # Stair in Dawn Chamber — connecting ground to upper floor
    # Located near the gate side, X = [3, 5], Y = [-2, 2]
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

    # Group everything
    rs.AddGroup("Lock_03_Morges_Temporal")
    rs.AddObjectsToGroup(all_objs, "Lock_03_Morges_Temporal")

    rs.EnableRedraw(True)
    rs.ZoomExtents()

    # Summary
    print("=" * 60)
    print("LOCK 03 — TEMPORAL LOCK (Morges, km 48)")
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
    print("=" * 60)


if __name__ == "__main__":
    main()
