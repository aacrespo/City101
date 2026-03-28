# Lock Type 08 — Altitude Lock South
# LOG400 Complete Geometry Specification
# Status: DRAFT FOR ROUNDTABLE REVIEW — do NOT execute until approved
# Architect: Claude (Nova — Henna Max)
# Date: 2026-03-27

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry is authored in METER-SCALE values.
"10.0" in Rhino = 10.0 as a number, displayed as "10 cm" but conceptually 10m.

**ALL coordinates in this spec are meter-scale. Use them exactly as written.**
**Do NOT multiply by 100. Do NOT convert.**

X = East–West axis (positive = East)
Y = North–South axis (positive = North, slope axis — valley to hilltop)
Z = vertical (0 = finished floor level at valley station)

**MCP target: `envelope` (port 9002)**

---

## BUILDING CONCEPT

**The Altitude Lock — South Variant (Asymmetric)** — connects two opposite temporalities through altitude. Valley station = emergency (fast, compact, urgent). Hilltop station = rehabilitation (slow, expansive, peaceful). The funicular track between them is the gradient — not just of altitude but of SPEED.

**State transition:** Acute care (fast, below) ↔ Rehabilitation (slow, above)

**Spatial logic:**
- Valley Station (Z=0–5): emergency interface. Small (10×10m), thick walls (0.4m RC), minimal openings. Compressed, institutional.
- Inclined Track (Z=5–21): 6m wide tube, 30m long, 53% grade. Windows grow larger as you ascend — transition from urgency to calm.
- Hilltop Station (Z=21–27): rehabilitation pavilion. Large (20×15m), thin walls (0.2m RC), panoramic glazing. Open, generous.
- Vertical Core (Z=21–28): mechanical room + stair above hilltop.
- Garden Platform (Z=20.5–21): rehabilitation garden ground plane. 28×10m slab.
- Terrain Proxy: abstract tilted surface from valley to hilltop.

**Four circulations:**
1. Emergency arrival: South entry → valley hall → inclined track UP
2. Rehabilitation arrival: Track TOP → hilltop pavilion → terrace → garden
3. Visitor path: Same as emergency but slower (family visiting rehab patients)
4. Discharge: Hilltop → track DOWN → valley → exit south

**What makes it different from Type 03 (Altitude North):**
- Type 03: symmetric twins (valley ≈ hilltop, same program)
- Type 08: asymmetric opposites (emergency ≠ rehabilitation)
- Valley = SMALLER, THICKER walls, FEW openings
- Hilltop = LARGER, THINNER walls, PANORAMIC views

---

## SECTION A: LAYERS

Create ALL layers before placing any geometry.

```
Type_08_AltitudeS::Volumes        — RGB(252, 196, 25)   — primary massing (walls, floors, slabs)
Type_08_AltitudeS::Structure      — RGB(178, 140, 18)   — columns, beams, transfer structure, steel frames
Type_08_AltitudeS::Circulation    — RGB(253, 220, 120)  — track slabs, stairs, ramp paths, polylines
Type_08_AltitudeS::Openings       — RGB(252, 210, 80)   — glazing, mullions, door frames, glass panes
Type_08_AltitudeS::Annotations    — RGB(253, 235, 170)  — text dots
Type_08_AltitudeS::L300_Roof      — RGB(200, 160, 20)   — roof slabs, parapets, copings
Type_08_AltitudeS::L350_Detail    — RGB(160, 125, 15)   — base plates, top plates, kickers, lintels, thresholds, brackets
Type_08_AltitudeS::L400_Material  — RGB(120, 95, 10)    — membrane, insulation, gravel, drip edges, upstands, expansion joints, formwork lines
```

**Total: 8 layers**

---

## SECTION B: VALLEY STATION — EMERGENCY INTERFACE

Layer: `Type_08_AltitudeS::Volumes`
Envelope: X=[-5, 5], Y=[-5, 5], Z=[0, 5]
Wall thickness: 0.4 (400mm RC — Archibase: C30/37, REI 90, fair-face concrete)

### B.1 South Wall (Y = -5.0 to -4.6)

Opening: Ambulance entry — X=[-2, 2], Z=[0, 3.5] (4m wide, 3.5m tall — narrow, controlled)
Split into 3 pieces:

```
Valley_wall_S_left:   [-5.0, -5.0, 0.0] → [-2.0, -4.6, 5.0]
Valley_wall_S_right:  [ 2.0, -5.0, 0.0] → [ 5.0, -4.6, 5.0]
Valley_wall_S_lintel: [-2.0, -5.0, 3.5] → [ 2.0, -4.6, 5.0]
```
3 elements.

### B.2 North Wall (Y = 4.6 to 5.0)

Opening: Connection to inclined track — X=[-3, 3], Z=[0.5, 4.5] (6m wide, 4m tall)
Split into 3 pieces:

```
Valley_wall_N_left:   [-5.0, 4.6, 0.0] → [-3.0, 5.0, 5.0]
Valley_wall_N_right:  [ 3.0, 4.6, 0.0] → [ 5.0, 5.0, 5.0]
Valley_wall_N_lintel: [-3.0, 4.6, 4.5] → [ 3.0, 5.0, 5.0]
```
3 elements.

### B.3 East Wall (Y = -4.6 to 4.6, X = 4.6 to 5.0)

2 slot windows: Z=[2, 4], Y=[-1.5, -0.5] and Y=[1.5, 2.5] (1m wide each)
Split into 5 pieces:

```
Valley_wall_E_base:     [4.6, -4.6, 0.0] → [5.0, 4.6, 2.0]
Valley_wall_E_top:      [4.6, -4.6, 4.0] → [5.0, 4.6, 5.0]
Valley_wall_E_pier_mid: [4.6, -0.5, 2.0] → [5.0, 1.5, 4.0]
Valley_wall_E_pier_S:   [4.6, -4.6, 2.0] → [5.0, -1.5, 4.0]
Valley_wall_E_pier_N:   [4.6, 2.5, 2.0] → [5.0, 4.6, 4.0]
```
5 elements.

### B.4 West Wall (Y = -4.6 to 4.6, X = -5.0 to -4.6)

2 slot windows: same pattern as east, mirrored.
Split into 5 pieces:

```
Valley_wall_W_base:     [-5.0, -4.6, 0.0] → [-4.6, 4.6, 2.0]
Valley_wall_W_top:      [-5.0, -4.6, 4.0] → [-4.6, 4.6, 5.0]
Valley_wall_W_pier_mid: [-5.0, -0.5, 2.0] → [-4.6, 1.5, 4.0]
Valley_wall_W_pier_S:   [-5.0, -4.6, 2.0] → [-4.6, -1.5, 4.0]
Valley_wall_W_pier_N:   [-5.0, 2.5, 2.0] → [-4.6, 4.6, 4.0]
```
5 elements.

### B.5 Valley Floor Slab

```
Valley_floor_slab: [-5.0, -5.0, -0.3] → [5.0, 5.0, 0.0]
```
RC slab 0.3m thick (300mm, Archibase: span/30 for 10m continuous = 0.33m, round to 0.3m with beam support).
1 element.

### B.6 Valley Roof Slab (= ceiling at Z=5)

```
Valley_roof_slab: [-5.0, -5.0, 5.0] → [5.0, 5.0, 5.3]
```
RC slab 0.3m thick.
1 element.

**Section B subtotal: 18 elements**

---

## SECTION C: INCLINED TRACK — INHABITED SLOPE

### Overall geometry
- Start: Y=5, Z=5 (top of valley station)
- End: Y=35, Z=21 (bottom of hilltop station)
- Width: X=[-3, 3] (6m)
- Grade: (21-5)/(35-5) = 53%
- Midpoint landing: Y=20, Z=13

### C.1 Track Tube Walls (Layer: Volumes)

East wall (X=2.7 to 3.0) and West wall (X=-3.0 to -2.7), 0.3m thick RC, sloped.
Each wall modeled as a wedge (8-point box with sloped top/bottom):

```
Track_wall_E: box_pts with corners:
  Bottom-south: (2.7, 5.0, 4.7)  Top-south: (3.0, 5.0, 4.7)
  Bottom-north: (2.7, 35.0, 20.7) Top-north: (3.0, 35.0, 20.7)
  Upper-south: (2.7, 5.0, 8.0)   Upper-south-outer: (3.0, 5.0, 8.0)
  Upper-north: (2.7, 35.0, 24.0)  Upper-north-outer: (3.0, 35.0, 24.0)

Track_wall_W: mirror of east at X=[-3.0, -2.7]
```
2 elements (wedge boxes).

### C.2 Track Floor (sloped slab, Layer: Volumes)

0.25m thick RC slab following the grade:

```
Track_floor: box_pts wedge:
  Bottom corners at Z = [4.75, 4.75, 20.75, 20.75] (slab underside)
  Top corners at Z = [5.0, 5.0, 21.0, 21.0] (slab top = track surface)
  Y = [5.0, 5.0, 35.0, 35.0]
  X = [-3.0, 3.0, 3.0, -3.0]
```
1 element.

### C.3 Track Roof (sloped slab, Layer: Volumes)

0.25m thick RC slab closing the tube:

```
Track_roof: box_pts wedge:
  Bottom at Z = [8.0, 8.0, 24.0, 24.0]
  Top at Z = [8.25, 8.25, 24.25, 24.25]
  Y = [5.0, 5.0, 35.0, 35.0]
  X = [-3.0, 3.0, 3.0, -3.0]
```
1 element.

### C.4 Midpoint Landing Platform (Layer: Volumes)

At Y=19–21, widened to X=[-4, 4] for passing:

```
Track_landing_platform: box_pts wedge:
  Floor Z at Y=19: 5 + (19-5)/30 * 16 = 12.47
  Floor Z at Y=21: 5 + (21-5)/30 * 16 = 13.53
  Bottom: Z = [12.17, 12.17, 13.23, 13.23] (0.3m thick)
  Top: Z = [12.47, 12.47, 13.53, 13.53]
  Y = [19.0, 19.0, 21.0, 21.0]
  X = [-4.0, 4.0, 4.0, -4.0]
```
1 element.

### C.5 Track Windows — Progressive Sizing (Layer: Openings)

**Key design element: windows grow larger ascending = transition from urgency to calm.**

East wall windows (mirrored on west):

**Bottom third (Y=5–15): Small slots — 0.8m × 1.0m**
3 windows at Y = [7, 9.5, 12]:
```
Track_win_E_slot_1: glass pane at X=3.0, Y=[6.6, 7.4], Z=[z_at_y + 1.5, z_at_y + 2.5]
Track_win_E_slot_2: glass pane at X=3.0, Y=[9.1, 9.9], Z=[z_at_y + 1.5, z_at_y + 2.5]
Track_win_E_slot_3: glass pane at X=3.0, Y=[11.6, 12.4], Z=[z_at_y + 1.5, z_at_y + 2.5]
```
Where z_at_y = 5 + (y-5)/30 * 16

**Middle third (Y=15–25): Medium windows — 1.2m × 1.5m**
3 windows at Y = [17, 20, 23]:
```
Track_win_E_med_1: glass pane at X=3.0, Y=[16.4, 17.6], Z=[z_at_y + 1.0, z_at_y + 2.5]
Track_win_E_med_2: glass pane at X=3.0, Y=[19.4, 20.6], Z=[z_at_y + 1.0, z_at_y + 2.5]
Track_win_E_med_3: glass pane at X=3.0, Y=[22.4, 23.6], Z=[z_at_y + 1.0, z_at_y + 2.5]
```

**Top third (Y=25–35): Large openings — 2.0m × 2.0m**
3 windows at Y = [27, 30, 33]:
```
Track_win_E_large_1: glass pane at X=3.0, Y=[26.0, 28.0], Z=[z_at_y + 0.5, z_at_y + 2.5]
Track_win_E_large_2: glass pane at X=3.0, Y=[29.0, 31.0], Z=[z_at_y + 0.5, z_at_y + 2.5]
Track_win_E_large_3: glass pane at X=3.0, Y=[32.0, 34.0], Z=[z_at_y + 0.5, z_at_y + 2.5]
```

West wall: mirror all 9 windows.
Glass thickness: 0.02m (triple IGU).

**18 glass panes total** (9 east + 9 west).

### C.6 Track Window Mullions (Layer: Openings)

Each window framed with 0.05m wide aluminum mullions:
- 4 mullions per window (top, bottom, left, right frame members)
- 18 windows × 4 = 72 mullion pieces

For efficiency, model as thin boxes (0.05 × 0.05m profile) around each glass pane.

**72 mullion elements.**

### C.7 Track Rails — Ascending + Descending (Layer: Circulation)

Two parallel polylines offset 1m in X, following the grade:

```
Track_rail_ascending: polyline from (1.0, 5.0, 5.0) to (1.0, 35.0, 21.0)
Track_rail_descending: polyline from (-1.0, 5.0, 5.0) to (-1.0, 35.0, 21.0)
```
2 polyline elements.

**Section C subtotal: 97 elements** (4 volumes + 1 landing + 18 glass + 72 mullions + 2 rails)

---

## SECTION D: HILLTOP STATION — REHABILITATION PAVILION

Layer: `Type_08_AltitudeS::Volumes`
Envelope: X=[-10, 10], Y=[35, 50], Z=[21, 27]
Wall thickness: 0.2 (200mm RC — Archibase: C25/30, thin, light, permeable)

### D.1 South Wall (Y = 35.0 to 35.2)

Opening: Connection from inclined track — X=[-3, 3], Z=[21, 25] (6m wide, 4m tall)
Split into 3 pieces:

```
Hilltop_wall_S_left:   [-10.0, 35.0, 21.0] → [-3.0, 35.2, 27.0]
Hilltop_wall_S_right:  [ 3.0, 35.0, 21.0] → [10.0, 35.2, 27.0]
Hilltop_wall_S_lintel: [-3.0, 35.0, 25.0] → [ 3.0, 35.2, 27.0]
```
3 elements.

### D.2 North Wall — Full-Width Glazing (Y = 49.8 to 50.0)

Panoramic view wall. Structure only — small piers at edges. Glazing fills the rest (Section D.8).

```
Hilltop_wall_N_pier_W: [-10.0, 49.8, 21.0] → [-8.0, 50.0, 27.0]
Hilltop_wall_N_pier_E: [ 8.0, 49.8, 21.0] → [10.0, 50.0, 27.0]
Hilltop_wall_N_spandrel: [-8.0, 49.8, 26.0] → [ 8.0, 50.0, 27.0]
```
3 elements.

### D.3 East Wall (X = 9.8 to 10.0, Y = 35.2 to 49.8)

Floor-to-ceiling windows, 4m wide each. Two windows + piers.
Split into 4 pieces:

```
Hilltop_wall_E_pier_S: [9.8, 35.2, 21.0] → [10.0, 38.0, 27.0]
Hilltop_wall_E_pier_mid: [9.8, 42.0, 21.0] → [10.0, 44.0, 27.0]
Hilltop_wall_E_pier_N: [9.8, 48.0, 21.0] → [10.0, 49.8, 27.0]
Hilltop_wall_E_sill_1: [9.8, 38.0, 21.0] → [10.0, 42.0, 21.5]
Hilltop_wall_E_sill_2: [9.8, 44.0, 21.0] → [10.0, 48.0, 21.5]
```
5 elements.

### D.4 West Wall (X = -10.0 to -9.8, Y = 35.2 to 49.8)

Mirror of east wall:
```
Hilltop_wall_W_pier_S: [-10.0, 35.2, 21.0] → [-9.8, 38.0, 27.0]
Hilltop_wall_W_pier_mid: [-10.0, 42.0, 21.0] → [-9.8, 44.0, 27.0]
Hilltop_wall_W_pier_N: [-10.0, 48.0, 21.0] → [-9.8, 49.8, 27.0]
Hilltop_wall_W_sill_1: [-10.0, 38.0, 21.0] → [-9.8, 42.0, 21.5]
Hilltop_wall_W_sill_2: [-10.0, 44.0, 21.0] → [-9.8, 48.0, 21.5]
```
5 elements.

### D.5 Hilltop Floor Slab

```
Hilltop_floor_slab: [-10.0, 35.0, 20.7] → [10.0, 50.0, 21.0]
```
RC slab 0.3m thick (supports 20m span with beam grid below).
1 element.

### D.6 Hilltop Roof Slab (Layer: L300_Roof)

```
Hilltop_roof_slab: [-10.0, 35.0, 27.0] → [10.0, 50.0, 27.47]
```
Full warm deck assembly: 0.47m total (0.2m RC + 0.2m insulation + 0.007m membrane + 0.003m fleece + 0.05m gravel + 0.01m plaster).
1 element.

### D.7 Hilltop Roof Parapets (Layer: L300_Roof)

0.2m thick, 1.1m high (SIA 358 — public building, drop > 12m):
```
Hilltop_parapet_N: [-10.0, 49.8, 27.47] → [10.0, 50.0, 28.57]
Hilltop_parapet_E: [9.8, 35.0, 27.47] → [10.0, 49.8, 28.57]
Hilltop_parapet_W: [-10.0, 35.0, 27.47] → [-9.8, 49.8, 28.57]
Hilltop_parapet_S: [-10.0, 35.0, 27.47] → [10.0, 35.2, 28.57]
```
4 elements.

### D.8 North Glazing — Panoramic Wall (Layer: Openings)

Full-width curtain wall: X=[-8, 8], Z=[22, 26], Y=49.8.
Stick system: vertical mullions at 2m spacing, horizontal transoms at mid-height (Z=24).

**Vertical mullions** (0.05 × 0.1m profile, 4m tall):
At X = [-8, -6, -4, -2, 0, 2, 4, 6, 8] — 9 mullions:
```
Hilltop_mullion_N_v1 through v9: [x-0.025, 49.75, 22.0] → [x+0.025, 49.85, 26.0]
```
9 elements.

**Horizontal transoms** (0.05 × 0.1m profile):
At Z=24, spanning between mullions — 8 transoms:
```
Hilltop_transom_N_h1 through h8: [x_left, 49.75, 23.975] → [x_right, 49.85, 24.025]
```
8 elements.

**Glass panes** (16m × 4m total, divided into 8×2 = 16 panes):
```
Hilltop_glass_N_1 through 16: thin boxes 0.02m thick at Y=49.82
```
16 elements.

### D.9 East Window Glazing (Layer: Openings)

2 windows: Y=[38, 42] and Y=[44, 48], Z=[21.5, 26], each 4m × 4.5m.

Per window: 1 glass pane + 4 frame mullions = 5 elements × 2 = 10 elements.
```
Hilltop_glass_E_1: [9.82, 38.0, 21.5] → [9.84, 42.0, 26.0]
Hilltop_glass_E_2: [9.82, 44.0, 21.5] → [9.84, 48.0, 26.0]
Hilltop_mullion_E_1_top through _bottom, _left, _right (×2 windows)
```
10 elements.

### D.10 West Window Glazing (Layer: Openings)

Mirror of east:
10 elements.

**Section D subtotal: 77 elements** (16 walls + 1 floor + 1 roof + 4 parapets + 33 north glazing + 10 east glazing + 10 west glazing + 2 sills counted in walls)

---

## SECTION E: VERTICAL CORE — MECHANICAL ROOM + STAIR

Layer: `Type_08_AltitudeS::Volumes`
Envelope: X=[-3, 3], Y=[42, 48], Z=[21, 28]
Wall thickness: 0.3 (300mm RC — structural core)

### E.1 Core Walls

```
Core_wall_S: [-3.0, 42.0, 21.0] → [3.0, 42.3, 28.0]
Core_wall_N: [-3.0, 47.7, 21.0] → [3.0, 48.0, 28.0]
Core_wall_E: [2.7, 42.3, 21.0] → [3.0, 47.7, 28.0]
Core_wall_W_lower: [-3.0, 42.3, 21.0] → [-2.7, 47.7, 24.5]
Core_wall_W_upper: [-3.0, 42.3, 25.5] → [-2.7, 47.7, 28.0]
Core_wall_W_lintel: [-3.0, 42.3, 24.5] → [-2.7, 44.3, 25.5]
```
Opening on west wall: door at Y=[44.3, 46.0], Z=[21, 24.5] for access from hilltop pavilion.
6 elements.

### E.2 Core Floor Slab

Shared with hilltop floor slab (already counted in D.5). No additional element.

### E.3 Core Roof Slab (Layer: L300_Roof)

```
Core_roof_slab: [-3.0, 42.0, 28.0] → [3.0, 48.0, 28.47]
```
Same warm deck assembly as hilltop.
1 element.

### E.4 Internal Stair — Valley Access (Layer: Circulation)

Stair from Z=21 to Z=28 (7m rise). Blondel: R=0.165m, G=0.295m (2×165+295=625mm).
7.0/0.165 = 42.4 → 43 risers, 4 flights of ~11 risers each with 3 landings.

Flight 1 (Z=21.0–22.815): 11 risers along Y direction
```
Core_stair_flight_1: box_pts wedge Y=[42.5, 45.7], Z bottom=[21.0], Z top=[22.815]
Core_stair_landing_1: [-2.5, 45.7, 22.815] → [2.5, 47.5, 22.965]
```

Flight 2 (Z=22.965–24.78): 11 risers returning
```
Core_stair_flight_2: box_pts wedge Y=[47.5, 44.3], Z bottom=[22.965], Z top=[24.78]
Core_stair_landing_2: [-2.5, 42.5, 24.78] → [2.5, 44.3, 24.93]
```

Flight 3 (Z=24.93–26.745): 11 risers
```
Core_stair_flight_3: box_pts wedge Y=[42.5, 45.7], Z bottom=[24.93], Z top=[26.745]
Core_stair_landing_3: [-2.5, 45.7, 26.745] → [2.5, 47.5, 26.895]
```

Flight 4 (Z=26.895–28.0): 10 risers (remaining)
```
Core_stair_flight_4: box_pts wedge Y=[47.5, 44.5], Z bottom=[26.895], Z top=[28.0]
```

4 flights + 3 landings = 7 elements.

### E.5 Stair Railings (Layer: Circulation)

Both sides, SIA 500 compliant. 0.044m diameter pipes, 1.1m above nosing.
8 railing pipes (2 per flight).
8 elements.

**Section E subtotal: 22 elements** (6 walls + 1 roof + 7 stair + 8 railings)

---

## SECTION F: TERRACE / VERANDA (wrapping hilltop)

Layer: `Type_08_AltitudeS::Volumes`

### F.1 Terrace Platform

Extends north and east beyond hilltop envelope:
```
Terrace_platform: [-10.0, 48.0, 20.85] → [13.0, 53.0, 21.0]
```
23m × 5m × 0.15m RC slab on steel supports.
1 element.

### F.2 Terrace Parapet / Railing (Layer: Circulation)

SIA 358: 1.1m guardrails at all edges (drop > 1m):
```
Terrace_railing_N: polyline/pipe at Y=53.0, Z=22.1, X=[-10, 13]
Terrace_railing_E: polyline/pipe at X=13.0, Z=22.1, Y=[48, 53]
Terrace_railing_S_ext: polyline/pipe at Y=48.0, Z=22.1, X=[10, 13]
```
3 pipe elements (0.044m diameter, 1.1m above platform).

### F.3 Terrace Columns (Layer: Structure)

4 thin columns supporting terrace overhang, 0.15 × 0.15m:
```
Terrace_col_1: [12.85, 48.0, 15.0] → [13.0, 48.15, 21.0]  (on slope)
Terrace_col_2: [12.85, 53.0, 15.0] → [13.0, 53.15, 21.0]
Terrace_col_3: [-10.0, 52.85, 18.0] → [-9.85, 53.0, 21.0]
Terrace_col_4: [0.0, 52.85, 19.0] → [0.15, 53.0, 21.0]
```
4 elements.

**Section F subtotal: 8 elements**

---

## SECTION G: GARDEN PLATFORM

Layer: `Type_08_AltitudeS::Volumes`

### G.1 Garden Slab

```
Garden_platform: [-14.0, 45.0, 20.5] → [14.0, 55.0, 21.0]
```
28m × 10m × 0.5m RC platform — rehabilitation garden ground plane.
1 element.

**Note:** Garden slab is BELOW hilltop floor (Z=20.5–21.0 vs Z=20.7–21.0). The hilltop building sits slightly above garden grade — a 0.2m step up from garden to interior.

### G.2 Garden Edge Parapets (Layer: L300_Roof)

Low walls at garden edges where drop exists:
```
Garden_parapet_N: [-14.0, 54.8, 21.0] → [14.0, 55.0, 22.1]
Garden_parapet_E: [13.8, 45.0, 21.0] → [14.0, 54.8, 22.1]
Garden_parapet_W: [-14.0, 45.0, 21.0] → [-13.8, 54.8, 22.1]
```
3 elements.

**Section G subtotal: 4 elements**

---

## SECTION H: TERRAIN PROXY

Layer: `Type_08_AltitudeS::Volumes` (sublayer TerrainProxy if available)

### H.1 Tilted Surface

Abstract slope from valley to hilltop:
```
Terrain_proxy: box_pts wedge:
  SW: (-20.0, -10.0, -1.0)
  SE: (20.0, -10.0, -1.0)
  NW: (-20.0, 55.0, 20.0)
  NE: (20.0, 55.0, 20.0)
  Thickness: 0.1m (thin proxy)
```
1 element.

**Section H subtotal: 1 element**

---

## SECTION I: STRUCTURE

Layer: `Type_08_AltitudeS::Structure`

### I.1 Valley Station Columns

4 corner columns, 0.4 × 0.4m (heavy — matches thick wall character):
```
Valley_col_SW: [-4.8, -4.8, -0.3] → [-4.4, -4.4, 5.0]
Valley_col_SE: [4.4, -4.8, -0.3] → [4.8, -4.4, 5.0]
Valley_col_NW: [-4.8, 4.4, -0.3] → [-4.4, 4.8, 5.0]
Valley_col_NE: [4.4, 4.4, -0.3] → [4.8, 4.8, 5.0]
```
4 elements.

### I.2 Valley Station Beams

2 primary beams spanning E-W at Y=±2, supporting roof slab:
```
Valley_beam_S: [-5.0, -2.3, 4.5] → [5.0, -2.0, 5.0]   (0.3m wide × 0.5m deep)
Valley_beam_N: [-5.0, 2.0, 4.5] → [5.0, 2.3, 5.0]
```
2 elements.

### I.3 Hilltop Station Columns

6 slender columns, 0.2 × 0.2m (light — matches thin wall character):
```
Hilltop_col_1: [-8.0, 38.0, 21.0] → [-7.8, 38.2, 27.0]
Hilltop_col_2: [0.0, 38.0, 21.0] → [0.2, 38.2, 27.0]
Hilltop_col_3: [7.8, 38.0, 21.0] → [8.0, 38.2, 27.0]
Hilltop_col_4: [-8.0, 47.0, 21.0] → [-7.8, 47.2, 27.0]
Hilltop_col_5: [0.0, 47.0, 21.0] → [0.2, 47.2, 27.0]
Hilltop_col_6: [7.8, 47.0, 21.0] → [8.0, 47.2, 27.0]
```
6 elements.

### I.4 Hilltop Station Beams

2 primary beams spanning 20m E-W:
```
Hilltop_beam_1: [-10.0, 38.0, 26.5] → [10.0, 38.3, 27.0]  (0.3m wide × 0.5m deep)
Hilltop_beam_2: [-10.0, 47.0, 26.5] → [10.0, 47.3, 27.0]
```
2 elements.

### I.5 Inclined Track Steel Frames (Layer: Structure)

Support frames every 5m along the 30m track (at Y = 10, 15, 20, 25, 30):
Each frame = 2 vertical posts (SHS 200×200mm) + 1 horizontal beam:

```
Track_frame_1_postE: [2.5, 10.0, z_floor] → [2.7, 10.2, z_roof]
Track_frame_1_postW: [-2.7, 10.0, z_floor] → [-2.5, 10.2, z_roof]
Track_frame_1_beam: [-2.7, 10.0, z_roof-0.3] → [2.7, 10.2, z_roof]
```
Where z_floor and z_roof are computed per frame position on grade.

5 frames × 3 elements = 15 elements.

### I.6 Track Longitudinal Beams

2 continuous beams running the full 30m length, supporting the track rails:
```
Track_long_beam_E: [1.5, 5.0, z_at_y-0.2] → [1.7, 35.0, z_at_y]  (wedge)
Track_long_beam_W: [-1.7, 5.0, z_at_y-0.2] → [-1.5, 35.0, z_at_y]  (wedge)
```
2 elements (IPE 200 profiles modeled as boxes).

### I.7 Core Columns

4 columns at core corners, 0.3 × 0.3m:
```
Core_col_SW: [-2.85, 42.15, 21.0] → [-2.55, 42.45, 28.0]
Core_col_SE: [2.55, 42.15, 21.0] → [2.85, 42.45, 28.0]
Core_col_NW: [-2.85, 47.55, 21.0] → [-2.55, 47.85, 28.0]
Core_col_NE: [2.55, 47.55, 21.0] → [2.85, 47.85, 28.0]
```
4 elements.

**Section I subtotal: 35 elements**

---

## SECTION J: ENTRY ELEMENTS (Layer: Openings)

### J.1 Valley South Entry — Ambulance Canopy

Steel canopy projecting 2m south from entry:
```
Valley_canopy_slab: [-3.0, -7.0, 3.5] → [3.0, -5.0, 3.6]   (6m × 2m × 0.1m steel plate)
Valley_canopy_col_W: [-2.9, -6.9, 0.0] → [-2.7, -6.7, 3.5]  (0.2 × 0.2m)
Valley_canopy_col_E: [2.7, -6.9, 0.0] → [2.9, -6.7, 3.5]
```
3 elements.

### J.2 Valley South Door Frame

```
Valley_door_frame_L: [-2.1, -5.0, 0.0] → [-2.0, -4.6, 3.5]
Valley_door_frame_R: [2.0, -5.0, 0.0] → [2.1, -4.6, 3.5]
Valley_door_frame_head: [-2.1, -5.0, 3.4] → [2.1, -4.6, 3.5]
```
3 elements.

### J.3 Hilltop North Threshold

```
Hilltop_threshold_N: [-8.0, 49.8, 21.0] → [8.0, 50.0, 21.05]
```
1 element.

**Section J subtotal: 7 elements**

---

## SECTION K: LOG350 DETAIL

Layer: `Type_08_AltitudeS::L350_Detail`

### K.1 Valley Station Base Plates

Steel base plates at column bases (0.5 × 0.5 × 0.03m):
4 base plates under valley columns.
4 elements.

### K.2 Hilltop Station Base Plates

0.3 × 0.3 × 0.02m under hilltop columns:
6 elements.

### K.3 Valley Kickers (DPC at wall base)

DPC strip at base of all valley walls, 0.01m thick:
```
Valley_kicker_S: [-5.0, -5.0, 0.0] → [5.0, -4.6, 0.01]
Valley_kicker_N: [-5.0, 4.6, 0.0] → [5.0, 5.0, 0.01]
Valley_kicker_E: [4.6, -4.6, 0.0] → [5.0, 4.6, 0.01]
Valley_kicker_W: [-5.0, -4.6, 0.0] → [-4.6, 4.6, 0.01]
```
4 elements.

### K.4 Hilltop Kickers

```
Hilltop_kicker_S: [-10.0, 35.0, 21.0] → [10.0, 35.2, 21.01]
Hilltop_kicker_E: [9.8, 35.2, 21.0] → [10.0, 49.8, 21.01]
Hilltop_kicker_W: [-10.0, 35.2, 21.0] → [-9.8, 49.8, 21.01]
```
3 elements.

### K.5 Valley Lintels

Steel lintels over openings (0.1m × 0.3m profile):
```
Valley_lintel_S: [-2.0, -5.0, 3.3] → [2.0, -4.6, 3.5]   (south entry)
Valley_lintel_N: [-3.0, 4.6, 4.3] → [3.0, 5.0, 4.5]     (north track opening)
```
2 elements.

### K.6 Hilltop Lintels

```
Hilltop_lintel_S: [-3.0, 35.0, 24.8] → [3.0, 35.2, 25.0]  (south track opening)
Hilltop_lintel_E1: [9.8, 38.0, 25.8] → [10.0, 42.0, 26.0]  (east window 1)
Hilltop_lintel_E2: [9.8, 44.0, 25.8] → [10.0, 48.0, 26.0]  (east window 2)
Hilltop_lintel_W1: [-10.0, 38.0, 25.8] → [-9.8, 42.0, 26.0]
Hilltop_lintel_W2: [-10.0, 44.0, 25.8] → [-9.8, 48.0, 26.0]
```
5 elements.

### K.7 Track Frame Base Plates

Steel base plates at each track frame post (0.3 × 0.3 × 0.025m):
5 frames × 2 posts = 10 base plates.
10 elements.

### K.8 Terrace Brackets

Steel angle brackets connecting terrace slab to hilltop structure:
4 L-brackets at connection points.
4 elements.

**Section K subtotal: 38 elements**

---

## SECTION L: LOG400 MATERIAL

Layer: `Type_08_AltitudeS::L400_Material`

### L.1 Valley Roof Assembly

On top of Valley_roof_slab (Z=5.3):
```
Valley_roof_vapour_barrier: [-5.0, -5.0, 5.3] → [5.0, 5.0, 5.301]
Valley_roof_insulation: [-5.0, -5.0, 5.301] → [5.0, 5.0, 5.501]
Valley_roof_membrane: [-5.0, -5.0, 5.501] → [5.0, 5.0, 5.508]
Valley_roof_gravel: [-5.0, -5.0, 5.508] → [5.0, 5.0, 5.558]
```
4 elements.

### L.2 Valley Roof WP Upstands

Membrane turns up at parapets (0.15m high):
```
Valley_upstand_S: [-5.0, -5.0, 5.501] → [5.0, -4.95, 5.651]
Valley_upstand_N: [-5.0, 4.95, 5.501] → [5.0, 5.0, 5.651]
Valley_upstand_E: [4.95, -5.0, 5.501] → [5.0, 5.0, 5.651]
Valley_upstand_W: [-5.0, -5.0, 5.501] → [-4.95, 5.0, 5.651]
```
4 elements.

### L.3 Valley Roof Drip Edges

Metal drip edges at roof perimeter:
```
Valley_drip_S: [-5.1, -5.1, 5.55] → [5.1, -5.0, 5.57]
Valley_drip_N: [-5.1, 5.0, 5.55] → [5.1, 5.1, 5.57]
Valley_drip_E: [5.0, -5.1, 5.55] → [5.1, 5.1, 5.57]
Valley_drip_W: [-5.1, -5.1, 5.55] → [-5.0, 5.1, 5.57]
```
4 elements.

### L.4 Hilltop Roof Assembly

On top of Hilltop_roof_slab (Z=27.47 is already the full assembly — model internal layers):
```
Hilltop_roof_vapour_barrier: [-10.0, 35.0, 27.2] → [10.0, 50.0, 27.201]
Hilltop_roof_insulation: [-10.0, 35.0, 27.201] → [10.0, 50.0, 27.401]
Hilltop_roof_membrane: [-10.0, 35.0, 27.401] → [10.0, 50.0, 27.408]
Hilltop_roof_gravel: [-10.0, 35.0, 27.408] → [10.0, 50.0, 27.458]
```
4 elements.

### L.5 Hilltop Roof Upstands

```
Hilltop_upstand_N: [-10.0, 49.75, 27.401] → [10.0, 49.8, 27.551]
Hilltop_upstand_E: [9.75, 35.0, 27.401] → [9.8, 49.8, 27.551]
Hilltop_upstand_W: [-9.8, 35.0, 27.401] → [-9.75, 49.8, 27.551]
Hilltop_upstand_S: [-10.0, 35.0, 27.401] → [10.0, 35.05, 27.551]
```
4 elements.

### L.6 Expansion Joints

At valley-to-track junction (Y=5) and track-to-hilltop junction (Y=35):
```
Expansion_joint_valley_track: line from (-3, 5, 5) to (3, 5, 5)
Expansion_joint_track_hilltop: line from (-3, 35, 21) to (3, 35, 21)
```
2 line elements.

### L.7 Formwork Lines (Valley — expressing concrete character)

Horizontal formwork lines on valley exterior walls at 0.6m spacing (Z = 0.6, 1.2, 1.8, 2.4, 3.0, 3.6, 4.2, 4.8):
4 walls × 8 lines = 32 lines. Model as representative subset: 12 lines (3 per wall face, at Z = 1.2, 2.4, 3.6).
12 line elements.

**Section L subtotal: 30 elements**

---

## SECTION M: ANNOTATIONS

Layer: `Type_08_AltitudeS::Annotations`

```
TextDot_1: "EMERGENCY / FAST / COMPACT" at (0, 0, 2.5)
TextDot_2: "TRANSITION / WINDOWS GROW" at (0, 15, 10.3)
TextDot_3: "MIDPOINT LANDING" at (0, 20, 13.5)
TextDot_4: "REHABILITATION / SLOW / EXPANSIVE" at (0, 42.5, 24.0)
TextDot_5: "GARDEN / RECOVERY" at (0, 50, 22.0)
TextDot_6: "ASCENDING = DECELERATING" at (2, 25, 16.0)
TextDot_7: "MECHANICAL / VERTICAL CORE" at (0, 45, 25.0)
TextDot_8: "AMBULANCE ENTRY" at (0, -6, 2.0)
TextDot_9: "PANORAMIC VIEW NORTH" at (0, 50, 24.0)
TextDot_10: "TERRACE / VERANDA" at (5, 51, 22.0)
```

**Section M subtotal: 10 elements**

---

## SECTION N: CIRCULATION PATHS

Layer: `Type_08_AltitudeS::Circulation`

### N.1 Emergency Arrival Path

Polyline: south entry → valley hall → track base:
```
Circ_emergency: polyline [(0, -7, 0.1), (0, -5, 0.1), (0, 0, 0.1), (0, 5, 5.1)]
```
1 element.

### N.2 Rehabilitation Path

Polyline: track top → hilltop → terrace → garden:
```
Circ_rehab: polyline [(0, 35, 21.1), (0, 42, 21.1), (0, 48, 21.1), (0, 51, 21.1), (5, 51, 21.1)]
```
1 element.

### N.3 Terrace Stroll Loop

Polyline loop on garden:
```
Circ_garden_loop: polyline [(-5, 48, 21.1), (-5, 53, 21.1), (10, 53, 21.1), (10, 48, 21.1), (-5, 48, 21.1)]
```
1 element.

**Section N subtotal: 3 elements**

---

## ELEMENT COUNT SUMMARY

| Section | Description | Count |
|---------|-------------|-------|
| B | Valley Station walls + slabs | 18 |
| C | Inclined Track (tube + windows + mullions + rails) | 97 |
| D | Hilltop Station (walls + floor + roof + parapets + glazing) | 77 |
| E | Vertical Core (walls + roof + stair + railings) | 22 |
| F | Terrace (platform + railings + columns) | 8 |
| G | Garden Platform (slab + parapets) | 4 |
| H | Terrain Proxy | 1 |
| I | Structure (columns + beams + track frames) | 35 |
| J | Entry Elements (canopy + door frame + threshold) | 7 |
| K | L350 Detail (base plates + kickers + lintels + brackets) | 38 |
| L | L400 Material (roof assembly + upstands + drips + joints + formwork) | 30 |
| M | Annotations | 10 |
| N | Circulation paths | 3 |
| **TOTAL** | | **350** |

---

## ARCHIBASE REFERENCES

| Element | Source | Key Dimension |
|---------|--------|---------------|
| Valley RC wall 400mm | C30/37, REI 90, SIA 262 | 0.4m structural |
| Hilltop RC wall 200mm | C25/30, light structure | 0.2m structural |
| Flat roof warm deck | Deplazes p.470-476, SIA 271 | ~0.47m total assembly |
| Floor slab | SIA 262, span/30 rule | 0.3m RC |
| Steel track frames | S355, SHS 200×200 | 0.2m members |
| Curtain wall (hilltop N) | Stick system, triple IGU | 0.1m mullion depth |
| Parapet height | SIA 358, public building | 1.1m |
| Handrail | SIA 500, graspable profile | 0.044m diameter |
| Stair geometry | Blondel 2R+G=625mm | R=0.165, G=0.295 |
| Foundation depth | Swiss frost minimum | 0.8m |
| Column (valley heavy) | SIA 262 | 0.4 × 0.4m |
| Column (hilltop light) | SIA 262 | 0.2 × 0.2m |

---

## SUCCESS CRITERIA

1. Valley station is visibly SMALLER and more ENCLOSED than hilltop
2. Hilltop pavilion is visibly LARGER and more OPEN
3. Track windows grow larger as they ascend — visible gradient of transparency
4. Terrace/garden platform reads as generous outdoor space
5. Asymmetry between valley (heavy/thick/closed) and hilltop (light/thin/open) is immediately visible
6. All parapets at SIA 358 height (1.1m for public)
7. Stair meets Blondel formula
8. Roof assemblies are complete warm deck stacks
9. Every element has material metadata
10. Total element count within ±5% of 350

---

## EXECUTION NOTES

- Build order: Layers → Structure (I) → Volumes (B, C.1-C.4, D, E, F, G, H) → Openings (C.5-C.6, D.8-D.10, J) → Circulation (C.7, E.4-E.5, F.2, N) → Roof (D.6-D.7, E.3, G.2) → Detail (K) → Material (L) → Annotations (M)
- Track geometry requires wedge boxes (box_pts with 8 explicit corners for sloped elements)
- All Z values for track elements must be computed: z_at_y = 5 + (y-5)/30 * 16
- Helper function `box(x, y, z, L, W, H)` must be defined in every script call
- Name every object immediately after creation
- Set material metadata on every object
