"""
LOCK 07 — BRIDGE LOCK (v3 — Site-placed)
Node 7, km 89 — Between Villeneuve CFF station and HRC Rennaz hospital
LOG 200-300: Defined volumes, structural bays, circulation zones, key openings

v3 CHANGES:
- Added SITE_ORIGIN parameter for placement on real terrain
- All geometry offset by SITE_ORIGIN during creation
- Coordinate system: local origin with offset from LV95
  Offset: E-2560000, N-1137500 (stored as metadata dot on terrain)

TWO STATES: Rail <-> Off-rail (2km gap between station and hospital)
CONCEPT: A horizontal skybridge / connector. The lightest intervention —
linear, directional. The occupant moves through a covered link; the
landscape transitions from rail infrastructure to medical campus.

SPATIAL PLAN:
=============
    SITE_ORIGIN = where the lock sits on the terrain (local coords)
    All geometry is created relative to SITE_ORIGIN.

    Local origin of lock = ground level at center of the bridge span,
    THEN shifted by SITE_ORIGIN.

    X = East-West (cross-section width, 6m for walkway + 12m at ends)
    Y = South-North (length axis: south = station, north = hospital)
    Z = Up (deck at +4m, total height ~8m)

    Total modeled length: ~90m (Y = [-45, 45])
    Cross-section: 6m wide (bridge) / 12m wide (station end) x 4m tall
    Deck elevation: 4m above ground
"""

import rhinoscriptsyntax as rs


# ---------------------------------------------------------------------------
# SITE PLACEMENT — v3
# ---------------------------------------------------------------------------
# Local coordinates (offset from LV95 by E-2560000, N-1137500)
# Within Rennaz terrain tile, terrain elevation ~374m
SITE_ORIGIN = (200, 300, 374.0)


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


def box_pts(pts_list):
    """For wedge/ramp shapes with explicit 8 points, offset by SITE_ORIGIN."""
    ox, oy, oz = SITE_ORIGIN
    return rs.AddBox([(p[0]+ox, p[1]+oy, p[2]+oz) for p in pts_list])


# ---------------------------------------------------------------------------
# LAYERS
# ---------------------------------------------------------------------------
def setup_layers():
    layers = {
        "Lock_07::Volumes":      (220, 230, 240),   # light steel blue
        "Lock_07::Structure":    (120, 115, 105),    # warm grey (steel tone)
        "Lock_07::Openings":     (180, 220, 200),    # lake green
        "Lock_07::Circulation":  (240, 210, 180),    # warm sand
        "Lock_07::FloorPlates":  (200, 200, 195),    # light concrete
    }
    for name, color in layers.items():
        if not rs.IsLayer(name):
            rs.AddLayer(name, color)
    return layers


# ---------------------------------------------------------------------------
# VOLUMES — Main envelopes
# ---------------------------------------------------------------------------
def create_volumes():
    rs.CurrentLayer("Lock_07::Volumes")
    objs = []

    station = box(-6, -45, 4, 6, -30, 8)
    rs.ObjectName(station, "Station_Platform_Envelope")
    objs.append(station)

    bridge = box(-3, -30, 4, 3, 30, 8)
    rs.ObjectName(bridge, "Bridge_Span_Envelope")
    objs.append(bridge)

    hosp = box(-4, 30, 0, 4, 45, 8)
    rs.ObjectName(hosp, "Hospital_Ramp_Envelope")
    objs.append(hosp)

    return objs


# ---------------------------------------------------------------------------
# FLOOR PLATES — Deck, platform, ramp
# ---------------------------------------------------------------------------
def create_floor_plates():
    rs.CurrentLayer("Lock_07::FloorPlates")
    objs = []

    deck_thick = 0.25

    station_deck = box(-6, -45, 4 - deck_thick, 6, -30, 4)
    rs.ObjectName(station_deck, "Deck_Station")
    objs.append(station_deck)

    bridge_deck = box(-3, -30, 4 - deck_thick, 3, 30, 4)
    rs.ObjectName(bridge_deck, "Deck_Bridge")
    objs.append(bridge_deck)

    ramp_pts = [
        (-4, 30, 4 - deck_thick),  (4, 30, 4 - deck_thick),
        (4, 45, -deck_thick),      (-4, 45, -deck_thick),
        (-4, 30, 4),               (4, 30, 4),
        (4, 45, 0),                (-4, 45, 0),
    ]
    ramp_deck = box_pts(ramp_pts)
    rs.ObjectName(ramp_deck, "Deck_Ramp")
    objs.append(ramp_deck)

    station_roof = box(-6, -45, 8, 6, -30, 8 + 0.2)
    rs.ObjectName(station_roof, "Roof_Station")
    objs.append(station_roof)

    bridge_roof = box(-3, -30, 8, 3, 30, 8 + 0.15)
    rs.ObjectName(bridge_roof, "Roof_Bridge")
    objs.append(bridge_roof)

    return objs


# ---------------------------------------------------------------------------
# STRUCTURE — V-columns and bay frames
# ---------------------------------------------------------------------------
def create_structure():
    rs.CurrentLayer("Lock_07::Structure")
    objs = []

    col_w = 0.25
    half = col_w / 2.0

    # Bridge span: V-columns at 12m spacing
    for y in [-24, -12, 0, 12, 24]:
        for x in [-2.5, 2.5]:
            col = box(x - half, y - half, 0, x + half, y + half, 4)
            rs.ObjectName(col, "VCol_Bridge_{}_{}".format(int(y), int(x)))
            objs.append(col)

    # Station platform columns
    for y in [-42, -36, -30]:
        for x in [-5.5, -2.5, 2.5, 5.5]:
            col = box(x - half, y - half, 0, x + half, y + half, 4)
            rs.ObjectName(col, "Col_Station_{}_{}".format(y, x))
            objs.append(col)

    # Hospital ramp columns (descending with ramp)
    for y in [33, 39, 45]:
        frac = (y - 30.0) / 15.0
        z_deck = 4.0 * (1.0 - frac)
        for x in [-3.5, 3.5]:
            if z_deck > 0.5:
                col = box(x - half, y - half, 0, x + half, y + half, z_deck)
                rs.ObjectName(col, "Col_Ramp_{}_{}".format(y, x))
                objs.append(col)

    # Bay frames along bridge span (6m spacing)
    bay_ys = list(range(-30, 31, 6))
    beam_h = 0.3
    beam_w = 0.15

    for y in bay_ys:
        beam_top = box(-3, y - beam_w/2, 8 - beam_h, 3, y + beam_w/2, 8)
        rs.ObjectName(beam_top, "Beam_Top_{}".format(y))
        objs.append(beam_top)

        beam_deck = box(-3, y - beam_w/2, 4, 3, y + beam_w/2, 4 + beam_h)
        rs.ObjectName(beam_deck, "Beam_Deck_{}".format(y))
        objs.append(beam_deck)

        for x in [-3, 3]:
            post = box(x - beam_w/2, y - beam_w/2, 4, x + beam_w/2, y + beam_w/2, 8)
            rs.ObjectName(post, "Post_{}_{}".format(y, x))
            objs.append(post)

    return objs


# ---------------------------------------------------------------------------
# OPENINGS — Lateral views every bay, station entrance
# ---------------------------------------------------------------------------
def create_openings():
    rs.CurrentLayer("Lock_07::Openings")
    objs = []

    bay_ys = list(range(-30, 31, 6))

    for i in range(len(bay_ys) - 1):
        y0 = bay_ys[i] + 0.5
        y1 = bay_ys[i + 1] - 0.5
        z0 = 4.8
        z1 = 7.5

        win_w = box(-3.3, y0, z0, -2.7, y1, z1)
        rs.ObjectName(win_w, "Opening_West_Bay_{}".format(bay_ys[i]))
        objs.append(win_w)

        win_e = box(2.7, y0, z0, 3.3, y1, z1)
        rs.ObjectName(win_e, "Opening_East_Bay_{}".format(bay_ys[i]))
        objs.append(win_e)

    entrance_s = box(-3, -45.5, 4, 3, -44.5, 7)
    rs.ObjectName(entrance_s, "Opening_Station_South")
    objs.append(entrance_s)

    for side, x_out, x_in in [("West", -6.3, -5.7), ("East", 5.7, 6.3)]:
        for y_c in [-40, -35]:
            win = box(x_out, y_c - 2, 4.5, x_in, y_c + 2, 7.5)
            rs.ObjectName(win, "Opening_Station_{}_{}".format(side, y_c))
            objs.append(win)

    return objs


# ---------------------------------------------------------------------------
# CIRCULATION — Lane divider, ramp guardrails
# ---------------------------------------------------------------------------
def create_circulation():
    rs.CurrentLayer("Lock_07::Circulation")
    objs = []

    divider = box(-0.05, -30, 4, 0.05, 30, 4.15)
    rs.ObjectName(divider, "Lane_Divider")
    objs.append(divider)

    for y_start in range(-30, 30, 6):
        strip = box(-2, y_start, 4, -1.8, y_start + 5.5, 4.02)
        rs.ObjectName(strip, "Tactile_West_{}".format(y_start))
        objs.append(strip)

    rail_h = 1.1
    rail_w = 0.06
    for x in [-3.8, 3.8]:
        rail_pts = [
            (x, 30, 4),                 (x + rail_w, 30, 4),
            (x + rail_w, 45, 0),         (x, 45, 0),
            (x, 30, 4 + rail_h),        (x + rail_w, 30, 4 + rail_h),
            (x + rail_w, 45, rail_h),    (x, 45, rail_h),
        ]
        rail = box_pts(rail_pts)
        rs.ObjectName(rail, "Guardrail_Ramp_{}".format("W" if x < 0 else "E"))
        objs.append(rail)

    for x in [-3, 3]:
        rail_bridge = box(x - rail_w/2, -30, 4, x + rail_w/2, 30, 4 + rail_h)
        rs.ObjectName(rail_bridge, "Guardrail_Bridge_{}".format("W" if x < 0 else "E"))
        objs.append(rail_bridge)

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

    rs.AddGroup("Lock_07_Rennaz_Bridge_Sited")
    rs.AddObjectsToGroup(all_objs, "Lock_07_Rennaz_Bridge_Sited")

    rs.EnableRedraw(True)
    rs.ZoomExtents()

    col_count = sum(1 for o in all_objs if rs.ObjectName(o) and ("VCol" in rs.ObjectName(o) or "Col_" in rs.ObjectName(o)))
    beam_count = sum(1 for o in all_objs if rs.ObjectName(o) and "Beam" in rs.ObjectName(o))
    post_count = sum(1 for o in all_objs if rs.ObjectName(o) and "Post" in rs.ObjectName(o))
    opening_count = sum(1 for o in all_objs if rs.ObjectName(o) and "Opening" in rs.ObjectName(o))

    print("=" * 60)
    print("LOCK 07 — BRIDGE LOCK (Rennaz, km 89)")
    print("v3 — Site-placed at ({}, {}, {})".format(*SITE_ORIGIN))
    print("=" * 60)
    print("Total objects created: {}".format(len(all_objs)))
    print("")
    print("Volumes:      3  (station platform, bridge span, hospital ramp)")
    print("Floor plates: 5  (station deck, bridge deck, ramp, station roof, bridge roof)")
    print("Columns:     {}  (V-columns + station + ramp supports)".format(col_count))
    print("Bay frames:  {} beams + {} posts".format(beam_count, post_count))
    print("Openings:    {}  (lateral views + station entrances)".format(opening_count))
    print("Circulation: ~15 (lane divider, tactile strips, guardrails)")
    print("")
    print("Total length: 90m (Y = -45 to +45)")
    print("Cross-section: 6m wide (bridge) / 12m (station)")
    print("Deck elevation: 4m above ground")
    print("LOG level: 200-300")
    print("Site origin: local ({}, {}, {})".format(*SITE_ORIGIN))
    print("LV95 offset: E-2560000, N-1137500")
    print("=" * 60)


if __name__ == "__main__":
    main()
