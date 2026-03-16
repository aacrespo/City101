"""
LOCK 07 — BRIDGE LOCK
Node 7, km 89 — Between Villeneuve CFF station and HRC Rennaz hospital
LOG 200-300: Defined volumes, structural bays, circulation zones, key openings

TWO STATES: Rail <-> Off-rail (2km gap between station and hospital)
CONCEPT: A horizontal skybridge / connector. The lightest intervention —
linear, directional. The occupant moves through a covered link; the
landscape transitions from rail infrastructure to medical campus.

SPATIAL PLAN:
=============
    Origin (0,0,0) = ground level at center of the bridge span
    X = East-West (cross-section width, 6m for walkway + 12m at ends)
    Y = South-North (length axis: south = station, north = hospital)
    Z = Up (deck at +4m, total height ~8m)

    LAYOUT (section along Y axis):

    Station Platform (south)   Bridge Span (center)      Hospital Ramp (north)
    Y = [-45, -30]             Y = [-30, 30]             Y = [30, 45]
    12m x 8m platform          6m wide x 60m long        descends to grade
    Z = 4 (deck level)         Z = 4 (elevated)          Z = 4 -> 0 (ramp)

    STATION END (south):
    - Wider platform: X = [-6, 6], Y = [-45, -30], Z = [4, 8]
    - Waiting area / canopy

    BRIDGE SPAN (center):
    - Elevated walkway: X = [-3, 3], Y = [-30, 30], Z = [4, 8]
    - Two parallel zones:
      * Fast lane (east):  X = [0, 3] — cycling, mobility devices
      * Slow lane (west):  X = [-3, 0] — pedestrians, patients
    - Structural bays at 6m spacing along Y
    - Lateral openings every bay (lake/mountain views)

    HOSPITAL END (north):
    - Ramp down to grade: X = [-4, 4], Y = [30, 45]
    - Deck descends from Z=4 to Z=0 over 15m

    SUPPORT STRUCTURE:
    - V-columns at every other bay (12m spacing)
    - Column base at ground (Z=0), supporting deck at Z=4
    - Column pairs at X = -2.5 and X = 2.5

    Total modeled length: ~90m (Y = [-45, 45])
    Cross-section: 6m wide (bridge) / 12m wide (station end) x 4m tall
    Deck elevation: 4m above ground
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

    # Station platform envelope (south) — wider waiting area
    station = box(-6, -45, 4, 6, -30, 8)
    rs.ObjectName(station, "Station_Platform_Envelope")
    objs.append(station)

    # Bridge span envelope (center) — narrow elevated walkway
    bridge = box(-3, -30, 4, 3, 30, 8)
    rs.ObjectName(bridge, "Bridge_Span_Envelope")
    objs.append(bridge)

    # Hospital ramp envelope (north) — widens slightly, ramp volume
    # Top at Z=8 on south end, descending. Envelope is a bounding box.
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

    # Station platform deck
    station_deck = box(-6, -45, 4 - deck_thick, 6, -30, 4)
    rs.ObjectName(station_deck, "Deck_Station")
    objs.append(station_deck)

    # Bridge span deck
    bridge_deck = box(-3, -30, 4 - deck_thick, 3, 30, 4)
    rs.ObjectName(bridge_deck, "Deck_Bridge")
    objs.append(bridge_deck)

    # Hospital ramp — sloped deck from Z=4 down to Z=0
    ramp_pts = [
        (-4, 30, 4 - deck_thick),  (4, 30, 4 - deck_thick),
        (4, 45, -deck_thick),      (-4, 45, -deck_thick),
        (-4, 30, 4),               (4, 30, 4),
        (4, 45, 0),                (-4, 45, 0),
    ]
    ramp_deck = rs.AddBox(ramp_pts)
    rs.ObjectName(ramp_deck, "Deck_Ramp")
    objs.append(ramp_deck)

    # Station roof canopy
    station_roof = box(-6, -45, 8, 6, -30, 8 + 0.2)
    rs.ObjectName(station_roof, "Roof_Station")
    objs.append(station_roof)

    # Bridge roof
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

    col_w = 0.25   # slender steel columns
    half = col_w / 2.0

    # -- Bridge span: V-columns at 12m spacing --
    # Y positions for main supports (every other bay = 12m)
    bridge_support_ys = [-24, -12, 0, 12, 24]
    x_positions = [-2.5, 2.5]

    for y in bridge_support_ys:
        for x in x_positions:
            # Vertical column from ground to deck
            col = box(x - half, y - half, 0, x + half, y + half, 4)
            rs.ObjectName(col, "VCol_Bridge_{:.0f}_{:.0f}".format(y, x))
            objs.append(col)

    # -- Station platform: columns at edges --
    station_support_ys = [-42, -36, -30]
    station_xs = [-5.5, -2.5, 2.5, 5.5]

    for y in station_support_ys:
        for x in station_xs:
            col = box(x - half, y - half, 0, x + half, y + half, 4)
            rs.ObjectName(col, "Col_Station_{:.0f}_{:.0f}".format(y, x))
            objs.append(col)

    # -- Hospital ramp: columns descending with ramp --
    ramp_ys = [33, 39, 45]
    for y in ramp_ys:
        # Column height decreases as ramp descends
        # At Y=30 deck is at Z=4, at Y=45 deck is at Z=0
        frac = (y - 30.0) / 15.0
        z_deck = 4.0 * (1.0 - frac)
        for x in [-3.5, 3.5]:
            if z_deck > 0.5:  # only place column if ramp is still elevated
                col = box(x - half, y - half, 0, x + half, y + half, z_deck)
                rs.ObjectName(col, "Col_Ramp_{:.0f}_{:.0f}".format(y, x))
                objs.append(col)

    # -- Bay frames along bridge span (structural rhythm at 6m) --
    bay_ys = list(range(-30, 31, 6))
    beam_h = 0.3
    beam_w = 0.15

    for y in bay_ys:
        # Top beam spanning full width at roof level
        beam_top = box(-3, y - beam_w/2, 8 - beam_h, 3, y + beam_w/2, 8)
        rs.ObjectName(beam_top, "Beam_Top_{:.0f}".format(y))
        objs.append(beam_top)

        # Deck beam
        beam_deck = box(-3, y - beam_w/2, 4, 3, y + beam_w/2, 4 + beam_h)
        rs.ObjectName(beam_deck, "Beam_Deck_{:.0f}".format(y))
        objs.append(beam_deck)

        # Vertical mullions / posts at edges of walkway
        for x in [-3, 3]:
            post = box(x - beam_w/2, y - beam_w/2, 4, x + beam_w/2, y + beam_w/2, 8)
            rs.ObjectName(post, "Post_{:.0f}_{:.0f}".format(y, x))
            objs.append(post)

    return objs


# ---------------------------------------------------------------------------
# OPENINGS — Lateral views every bay, station entrance
# ---------------------------------------------------------------------------
def create_openings():
    rs.CurrentLayer("Lock_07::Openings")
    objs = []

    # Lateral openings between bays — views to lake and mountains
    # One opening per bay on each side (east and west)
    bay_ys = list(range(-30, 31, 6))

    for i in range(len(bay_ys) - 1):
        y0 = bay_ys[i] + 0.5     # inset from bay frame
        y1 = bay_ys[i + 1] - 0.5
        z0 = 4.8                   # sill height (above deck)
        z1 = 7.5                   # head height (below roof beam)

        # West opening (lake side)
        win_w = box(-3.3, y0, z0, -2.7, y1, z1)
        rs.ObjectName(win_w, "Opening_West_Bay_{:.0f}".format(bay_ys[i]))
        objs.append(win_w)

        # East opening (mountain side)
        win_e = box(2.7, y0, z0, 3.3, y1, z1)
        rs.ObjectName(win_e, "Opening_East_Bay_{:.0f}".format(bay_ys[i]))
        objs.append(win_e)

    # Station end — south entrance (arriving from platform)
    entrance_s = box(-3, -45.5, 4, 3, -44.5, 7)
    rs.ObjectName(entrance_s, "Opening_Station_South")
    objs.append(entrance_s)

    # Station — east and west openings (connection to existing platform)
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

    # Lane divider strip — separating fast (east) and slow (west) lanes
    # X = 0 centerline, thin raised strip
    divider = box(-0.05, -30, 4, 0.05, 30, 4.15)
    rs.ObjectName(divider, "Lane_Divider")
    objs.append(divider)

    # Tactile guidance strips — slow lane (west side)
    for y_start in range(-30, 30, 6):
        strip = box(-2, y_start, 4, -1.8, y_start + 5.5, 4.02)
        rs.ObjectName(strip, "Tactile_West_{:.0f}".format(y_start))
        objs.append(strip)

    # Ramp guardrails (hospital end)
    rail_h = 1.1
    rail_w = 0.06
    for x in [-3.8, 3.8]:
        # Rail follows ramp slope
        rail_pts = [
            (x, 30, 4),                 (x + rail_w, 30, 4),
            (x + rail_w, 45, 0),         (x, 45, 0),
            (x, 30, 4 + rail_h),        (x + rail_w, 30, 4 + rail_h),
            (x + rail_w, 45, rail_h),    (x, 45, rail_h),
        ]
        rail = rs.AddBox(rail_pts)
        rs.ObjectName(rail, "Guardrail_Ramp_{}".format("W" if x < 0 else "E"))
        objs.append(rail)

    # Bridge edge guardrails (full span)
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

    # Group everything
    rs.AddGroup("Lock_07_Rennaz_Bridge")
    rs.AddObjectsToGroup(all_objs, "Lock_07_Rennaz_Bridge")

    rs.EnableRedraw(True)
    rs.ZoomExtents()

    # Count categories
    beam_count = sum(1 for o in all_objs if rs.ObjectName(o) and "Beam" in rs.ObjectName(o))
    post_count = sum(1 for o in all_objs if rs.ObjectName(o) and "Post" in rs.ObjectName(o))
    col_count = sum(1 for o in all_objs if rs.ObjectName(o) and ("VCol" in rs.ObjectName(o) or "Col_" in rs.ObjectName(o)))
    opening_count = sum(1 for o in all_objs if rs.ObjectName(o) and "Opening" in rs.ObjectName(o))

    print("=" * 60)
    print("LOCK 07 — BRIDGE LOCK (Rennaz, km 89)")
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
    print("=" * 60)


if __name__ == "__main__":
    main()
