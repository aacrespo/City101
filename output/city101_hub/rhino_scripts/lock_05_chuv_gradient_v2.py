"""
LOCK 05 — GRADIENT DISPATCHER
Node 5, km 65 — CHUV Lausanne campus, steep terrain
LOG 200-300: Defined volumes, floor plates, structural rhythm, key openings

TWO STATES: Uphill <-> Downhill (Lausanne's extreme topography)
CONCEPT: An elevator bank routing multiple supply chain flows across gradient
levels. Multi-level dispatcher following a 15% grade.

SPATIAL PLAN:
=============
    Origin (0,0,0) = ground level at Level 0 (bottom/south), center of south facade
    X = East-West (building width ~20m)
    Y = South-North (building depth ~30m, follows slope uphill)
    Z = Up

    The slope rises north: 15% grade over 30m = +4.5m natural rise
    But we build 4 discrete levels stepping with the terrain.

    LEVELS (floor Z elevations):
    Level 0:  Z = 0.0    (arrival, public interface)     Y = [0, 10]
    Level 1:  Z = 3.5    (staff circulation)              Y = [8, 18]  (2m overlap with L0)
    Level 2:  Z = 7.0    (logistics sorting)              Y = [16, 26] (2m overlap with L1)
    Level 3:  Z = 10.5   (emergency access)               Y = [24, 34] (2m overlap with L2)

    Each level footprint: ~20m (X) x 10m (Y)
    Levels overlap 2m in Y to create transition zones

    X range: [-10, 10] (20m total, centered on origin)

    CENTRAL VOID / ATRIUM:
    - X = [-3, 3] (6m wide)
    - Runs through all levels from Y = 5 to Y = 29
    - Full height — the "shaft" of the elevator analogy

    RAMPS (not stairs):
    - Connecting each level pair, along east edge
    - X = [6, 10], spanning Y overlap zones
    - Each ramp rises 3.5m over ~10m run (35% — steep but compressed for model)

    FACADE:
    - North face (uphill): fully glazed (city view) — openings layer
    - South face (downhill): solid (slope-cut into terrain)

    STRUCTURE:
    - Columns at 5m grid on X, 5m grid on Y within each level
    - Column size: 0.4m x 0.4m (heavier — multi-story, medical loads)

    Overall: 20m (X) x 34m (Y) x ~14m (Z to top of Level 3 + roof)
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
        "Lock_05::Volumes":      (160, 190, 180),   # muted teal
        "Lock_05::Structure":    (90, 95, 100),      # charcoal
        "Lock_05::Openings":     (200, 230, 255),    # cool daylight blue
        "Lock_05::Circulation":  (230, 180, 140),    # warm terracotta
        "Lock_05::FloorPlates":  (210, 210, 200),    # warm concrete
        "Lock_05::Terrain":      (160, 150, 130),    # earth
    }
    for name, color in layers.items():
        if not rs.IsLayer(name):
            rs.AddLayer(name, color)
    return layers


# ---------------------------------------------------------------------------
# TERRAIN — Sloped ground reference
# ---------------------------------------------------------------------------
def create_terrain():
    rs.CurrentLayer("Lock_05::Terrain")
    objs = []

    # Approximate terrain slab following 15% grade
    # South edge at Z=0, north edge at Z ~+5.1 (15% over 34m)
    # Modeled as a wedge using 8-point box with tilted top
    terrain_pts = [
        (-14, -2, -3),  (14, -2, -3),  (14, 36, -3),  (-14, 36, -3),   # bottom
        (-14, -2,  0),  (14, -2,  0),  (14, 36, 5.1), (-14, 36, 5.1),  # top follows grade
    ]
    terrain = rs.AddBox(terrain_pts)
    rs.ObjectName(terrain, "Terrain_Slope")
    objs.append(terrain)

    return objs


# ---------------------------------------------------------------------------
# VOLUMES — Level envelopes
# ---------------------------------------------------------------------------
def create_volumes():
    rs.CurrentLayer("Lock_05::Volumes")
    objs = []

    levels = [
        ("Level_0_Public",     0.0,   0, 10, 3.5),
        ("Level_1_Staff",      3.5,   8, 18, 3.5),
        ("Level_2_Logistics",  7.0,  16, 26, 3.5),
        ("Level_3_Emergency", 10.5,  24, 34, 3.5),
    ]

    for name, z_floor, y0, y1, height in levels:
        vol = box(-10, y0, z_floor, 10, y1, z_floor + height)
        rs.ObjectName(vol, name + "_Envelope")
        objs.append(vol)

    return objs


# ---------------------------------------------------------------------------
# FLOOR PLATES
# ---------------------------------------------------------------------------
def create_floor_plates():
    rs.CurrentLayer("Lock_05::FloorPlates")
    objs = []
    slab = 0.3

    levels = [
        ("Level_0", 0.0,   0, 10),
        ("Level_1", 3.5,   8, 18),
        ("Level_2", 7.0,  16, 26),
        ("Level_3", 10.5, 24, 34),
    ]

    for name, z, y0, y1 in levels:
        # Floor slab
        fl = box(-10, y0, z - slab, 10, y1, z)
        rs.ObjectName(fl, "Floor_" + name)
        objs.append(fl)

        # Roof slab
        rf = box(-10, y0, z + 3.5, 10, y1, z + 3.5 + slab)
        rs.ObjectName(rf, "Roof_" + name)
        objs.append(rf)

    return objs


# ---------------------------------------------------------------------------
# CENTRAL VOID — The atrium / elevator shaft analogy
# ---------------------------------------------------------------------------
def create_void():
    rs.CurrentLayer("Lock_05::Openings")
    objs = []

    # Central void running through the building
    # X = [-3, 3], Y = [5, 29], full height from Z=0 to Z=14
    void = box(-3, 5, 0, 3, 29, 14)
    rs.ObjectName(void, "Central_Atrium_Void")
    objs.append(void)

    return objs


# ---------------------------------------------------------------------------
# STRUCTURE — Columns on 5m grid
# ---------------------------------------------------------------------------
def create_structure():
    rs.CurrentLayer("Lock_05::Structure")
    objs = []

    col_w = 0.4
    half = col_w / 2.0

    levels = [
        (0.0,   0, 10, 3.5),    # Level 0
        (3.5,   8, 18, 3.5),    # Level 1
        (7.0,  16, 26, 3.5),    # Level 2
        (10.5, 24, 34, 3.5),    # Level 3
    ]

    # X positions: -10, -5, 0, 5, 10
    x_positions = [-10, -5, 0, 5, 10]

    for level_idx, (z_floor, y_start, y_end, height) in enumerate(levels):
        # Y positions within each level at 5m spacing
        y_positions = list(range(y_start, y_end + 1, 5))
        for x in x_positions:
            for y in y_positions:
                # Skip columns inside the central void
                if -3 < x < 3 and 5 < y < 29:
                    continue
                col = box(x - half, y - half, z_floor, x + half, y + half, z_floor + height)
                rs.ObjectName(col, "Col_L{}_{}_{}".format(level_idx, x, y))
                objs.append(col)

    return objs


# ---------------------------------------------------------------------------
# OPENINGS — North facade glazing, south solid
# ---------------------------------------------------------------------------
def create_openings():
    rs.CurrentLayer("Lock_05::Openings")
    objs = []

    # North face of each level — fully glazed (city view toward lake)
    # Modeled as void volumes through the north wall
    levels = [
        ("L0", 0.0,  10, 3.5),
        ("L1", 3.5,  18, 3.5),
        ("L2", 7.0,  26, 3.5),
        ("L3", 10.5, 34, 3.5),
    ]

    for name, z, y_north, height in levels:
        # North glazing — full width minus structure, floor-to-ceiling
        # Two panels flanking the central void
        # West panel
        win_w = box(-9.5, y_north - 0.5, z + 0.8, -3.5, y_north + 0.5, z + height - 0.3)
        rs.ObjectName(win_w, "Glazing_{}_North_West".format(name))
        objs.append(win_w)
        # East panel
        win_e = box(3.5, y_north - 0.5, z + 0.8, 9.5, y_north + 0.5, z + height - 0.3)
        rs.ObjectName(win_e, "Glazing_{}_North_East".format(name))
        objs.append(win_e)

    # Level 0 south entrance — public arrival from metro
    entrance = box(-4, -0.5, 0, 4, 0.5, 3.2)
    rs.ObjectName(entrance, "Opening_L0_SouthEntrance")
    objs.append(entrance)

    # Level 3 north — emergency vehicle access
    emerg = box(-5, 33.5, 10.5, 5, 34.5, 14)
    rs.ObjectName(emerg, "Opening_L3_EmergencyAccess")
    objs.append(emerg)

    return objs


# ---------------------------------------------------------------------------
# CIRCULATION — Ramps connecting levels
# ---------------------------------------------------------------------------
def create_circulation():
    rs.CurrentLayer("Lock_05::Circulation")
    objs = []

    # Ramps along east edge, spanning overlap zones between levels
    # Each ramp: X = [6, 10], rising 3.5m
    # Modeled as sloped solid volumes (using skewed box corners)
    ramps = [
        ("Ramp_L0_L1", 6, 10,  5, 13, 0.0, 3.5),
        ("Ramp_L1_L2", 6, 10, 13, 21, 3.5, 7.0),
        ("Ramp_L2_L3", 6, 10, 21, 29, 7.0, 10.5),
    ]

    ramp_thick = 0.3

    for name, x0, x1, y0, y1, z_bot, z_top in ramps:
        # Ramp as a wedge — bottom at z_bot on south end, z_top on north end
        ramp_pts = [
            (x0, y0, z_bot),            (x1, y0, z_bot),
            (x1, y1, z_top),            (x0, y1, z_top),
            (x0, y0, z_bot + ramp_thick), (x1, y0, z_bot + ramp_thick),
            (x1, y1, z_top + ramp_thick), (x0, y1, z_top + ramp_thick),
        ]
        ramp = rs.AddBox(ramp_pts)
        rs.ObjectName(ramp, name)
        objs.append(ramp)

    # Ramp guardrails — simple extrusions along ramp edges
    rail_h = 1.1
    rail_w = 0.08
    for name, x0, x1, y0, y1, z_bot, z_top in ramps:
        # Inner rail (X = x0 side)
        rail_pts = [
            (x0, y0, z_bot + ramp_thick),             (x0 + rail_w, y0, z_bot + ramp_thick),
            (x0 + rail_w, y1, z_top + ramp_thick),    (x0, y1, z_top + ramp_thick),
            (x0, y0, z_bot + ramp_thick + rail_h),    (x0 + rail_w, y0, z_bot + ramp_thick + rail_h),
            (x0 + rail_w, y1, z_top + ramp_thick + rail_h), (x0, y1, z_top + ramp_thick + rail_h),
        ]
        rail = rs.AddBox(rail_pts)
        rs.ObjectName(rail, name + "_Rail_Inner")
        objs.append(rail)

    return objs


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    rs.EnableRedraw(False)

    setup_layers()

    all_objs = []
    all_objs += create_terrain()
    all_objs += create_volumes()
    all_objs += create_floor_plates()
    all_objs += create_void()
    all_objs += create_structure()
    all_objs += create_openings()
    all_objs += create_circulation()

    # Group everything
    rs.AddGroup("Lock_05_CHUV_Gradient")
    rs.AddObjectsToGroup(all_objs, "Lock_05_CHUV_Gradient")

    rs.EnableRedraw(True)
    rs.ZoomExtents()

    # Summary
    vol_count = 4
    floor_count = 8
    col_count = sum(1 for o in all_objs if rs.ObjectName(o) and rs.ObjectName(o).startswith("Col_"))
    opening_count = sum(1 for o in all_objs if rs.ObjectName(o) and ("Glazing" in rs.ObjectName(o) or "Opening" in rs.ObjectName(o) or "Void" in rs.ObjectName(o)))

    print("=" * 60)
    print("LOCK 05 — GRADIENT DISPATCHER (CHUV Lausanne, km 65)")
    print("=" * 60)
    print("Total objects created: {}".format(len(all_objs)))
    print("")
    print("Terrain:      1  (sloped ground reference)")
    print("Volumes:      4  (Level 0-3 envelopes)")
    print("Floor plates: 8  (4 floors + 4 roofs)")
    print("Central void: 1  (atrium shaft, 6m x 24m x 14m)")
    print("Columns:     ~{}  (5m grid, excluding void zone)".format(col_count))
    print("Openings:    11  (8 north glazing panels, entrance, emergency, void)")
    print("Circulation:  6  (3 ramps + 3 guardrails)")
    print("")
    print("Overall dimensions: 20m (X) x 34m (Y) x 14m (Z)")
    print("Grade: 15% over 34m (4 stepped levels at 3.5m)")
    print("LOG level: 200-300")
    print("=" * 60)


if __name__ == "__main__":
    main()
