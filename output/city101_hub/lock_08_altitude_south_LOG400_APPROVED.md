# Lock Type 08 — Altitude Lock South
# LOG400 Complete Geometry Specification — APPROVED
# Status: APPROVED after roundtable review (27 corrections applied)
# Architect: Claude (Nova — Henna Max)
# Date: 2026-03-27

---

## ROUNDTABLE CORRECTIONS APPLIED

### Structural (from structural reviewer)
- S1: Added 2 intermediate hilltop columns at X=±5 → beam spans reduced to 10m (0.5m depth now valid)
- S2: Hilltop columns increased to 0.3×0.3m
- S3: Added lateral tie beams from core to hilltop frame at roof level
- S4: Added 6 garden platform support piers + beam grid
- S5: Terrace redesigned: 0.25m slab, columns at 5m spacing, 0.2×0.2m columns
- C6: Valley beams noted as bearing on 400mm RC walls (loadbearing)
- C8: Track walls increased to 400mm
- C9: Track floor increased to 300mm
- C10: Added schematic foundation section
- C11: Added transfer beams at track-station junctions
- C12: Core columns removed (300mm walls sufficient)

### Envelope (from envelope reviewer)
- S1: Added valley roof parapets
- S4: Added track tube roof waterproofing + insulation
- S5: Added track wall-roof junction flashing
- S15: Added terrace waterproofing assembly
- S21: Upgraded expansion joints to detailed assemblies
- C19: Wall insulation explicitly deferred (typological study — RC thicknesses only)

### Circulation (from circulation/fire/accessibility reviewer)
- S-A1: Added funicular carriage element; track extended into valley station
- S-A2: Garden slab raised to Z=20.975 at building interface (25mm max lip)
- S-F1: Added second exit on valley west wall
- S-F2: Added external escape stair on hilltop east face
- S-F3: Added fire-rated closures at both track junctions
- S-C1: Valley-to-track transition resolved (carriage boards at Z=0)
- C-A4: Core stair renamed to "Roof/Mechanical Access"
- C-A5: Added second handrails at 0.75m
- C-C2: Track rail spacing widened to 2.5m center-to-center

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

**Key design principle:** Valley = SMALLER, THICKER walls, FEW openings, HEAVY columns. Hilltop = LARGER, THINNER walls, PANORAMIC views, SLENDER columns. The asymmetry must be immediately visible.

**Wall insulation note:** Wall insulation is deferred for this typological study. All wall thicknesses are structural RC only. Roof insulation IS modeled (warm deck assembly).

---

## SECTION A: LAYERS

Create ALL layers before placing any geometry.

```
Type_08_AltitudeS::Volumes        — RGB(252, 196, 25)
Type_08_AltitudeS::Structure      — RGB(178, 140, 18)
Type_08_AltitudeS::Circulation    — RGB(253, 220, 120)
Type_08_AltitudeS::Openings       — RGB(252, 210, 80)
Type_08_AltitudeS::Annotations    — RGB(253, 235, 170)
Type_08_AltitudeS::L300_Roof      — RGB(200, 160, 20)
Type_08_AltitudeS::L350_Detail    — RGB(160, 125, 15)
Type_08_AltitudeS::L400_Material  — RGB(120, 95, 10)
```

**Total: 8 layers**

---

## SECTION B: VALLEY STATION — EMERGENCY INTERFACE

Layer: `Type_08_AltitudeS::Volumes`
Envelope: X=[-5, 5], Y=[-5, 5], Z=[0, 5]
Wall thickness: 0.4m (400mm RC C30/37, REI 90)

### B.1 South Wall (Y=-5.0 to -4.6)
Opening: Ambulance entry X=[-2, 2], Z=[0, 3.5]
```
Valley_wall_S_left:   [-5.0, -5.0, 0.0] → [-2.0, -4.6, 5.0]
Valley_wall_S_right:  [ 2.0, -5.0, 0.0] → [ 5.0, -4.6, 5.0]
Valley_wall_S_lintel: [-2.0, -5.0, 3.5] → [ 2.0, -4.6, 5.0]
```
3 elements.

### B.2 North Wall (Y=4.6 to 5.0)
Opening: Track connection X=[-3, 3], Z=[0, 4.5] (CORRECTED: track extends to Z=0 for carriage boarding)
```
Valley_wall_N_left:   [-5.0, 4.6, 0.0] → [-3.0, 5.0, 5.0]
Valley_wall_N_right:  [ 3.0, 4.6, 0.0] → [ 5.0, 5.0, 5.0]
Valley_wall_N_lintel: [-3.0, 4.6, 4.5] → [ 3.0, 5.0, 5.0]
```
3 elements.

### B.3 East Wall (X=4.6 to 5.0)
2 slot windows: Z=[2,4], Y=[-1.5,-0.5] and Y=[1.5,2.5]
```
Valley_wall_E_base:     [4.6, -4.6, 0.0] → [5.0, 4.6, 2.0]
Valley_wall_E_top:      [4.6, -4.6, 4.0] → [5.0, 4.6, 5.0]
Valley_wall_E_pier_mid: [4.6, -0.5, 2.0] → [5.0, 1.5, 4.0]
Valley_wall_E_pier_S:   [4.6, -4.6, 2.0] → [5.0, -1.5, 4.0]
Valley_wall_E_pier_N:   [4.6, 2.5, 2.0] → [5.0, 4.6, 4.0]
```
5 elements.

### B.4 West Wall (X=-5.0 to -4.6)
2 slot windows + 1 emergency exit (ADDED: second exit, Y=[-1,1], Z=[0,2.1])
```
Valley_wall_W_base:     [-5.0, -4.6, 0.0] → [-4.6, -1.0, 2.0]
Valley_wall_W_base2:    [-5.0, 1.0, 0.0] → [-4.6, 4.6, 2.0]
Valley_wall_W_lintel_exit: [-5.0, -1.0, 2.1] → [-4.6, 1.0, 2.5]
Valley_wall_W_top:      [-5.0, -4.6, 4.0] → [-4.6, 4.6, 5.0]
Valley_wall_W_pier_mid: [-5.0, -0.5, 2.5] → [-4.6, 1.5, 4.0]
Valley_wall_W_pier_S:   [-5.0, -4.6, 2.0] → [-4.6, -1.5, 4.0]
Valley_wall_W_pier_N:   [-5.0, 2.5, 2.0] → [-4.6, 4.6, 4.0]
```
7 elements (2 more than east due to exit opening).

### B.5 Valley Floor Slab
```
Valley_floor_slab: [-5.0, -5.0, -0.3] → [5.0, 5.0, 0.0]
```
0.3m RC slab. Two-way spanning (10m square panel). Noted as loadbearing-wall-supported.
1 element.

### B.6 Valley Roof Slab
```
Valley_roof_slab: [-5.0, -5.0, 5.0] → [5.0, 5.0, 5.3]
```
0.3m RC slab.
1 element.

### B.7 Valley Roof Parapets (ADDED — Layer: L300_Roof)
0.3m thick, 0.6m high (maintenance-access kerb + gravel stop):
```
Valley_parapet_S: [-5.0, -5.0, 5.558] → [5.0, -4.7, 6.158]
Valley_parapet_N: [-5.0, 4.7, 5.558] → [5.0, 5.0, 6.158]
Valley_parapet_E: [4.7, -5.0, 5.558] → [5.0, 5.0, 6.158]
Valley_parapet_W: [-5.0, -5.0, 5.558] → [-4.7, 5.0, 6.158]
```
4 elements.

**Section B subtotal: 24 elements**

---

## SECTION C: INCLINED TRACK — INHABITED SLOPE

Start: Y=5, Z=0 (CORRECTED: track extends into valley station for carriage boarding)
End: Y=35, Z=21
Width: X=[-3, 3] (6m)
Grade formula: z_at_y = (y - 5) / 30 * 21 = 0.7 * (y - 5) for the sloped portion
Note: Track floor is level at Z=0 from Y=5 to Y=5 (boarding), then slopes from Z=5 at Y=5 (after valley roof) to Z=21 at Y=35.

**Revised geometry:** The track tube starts at the valley north wall (Y=5). Inside the valley station, the carriage descends to floor level via the track mechanism. The track tube proper (sloped) runs Y=5 to Y=35, Z=5 to Z=21.

### C.1 Track Tube Walls (Layer: Volumes, CORRECTED: 0.4m thick)
```
Track_wall_E: wedge box X=[2.6, 3.0], Y=[5, 35]
  South-bottom: Z=4.6, South-top: Z=8.0
  North-bottom: Z=20.6, North-top: Z=24.0

Track_wall_W: wedge box X=[-3.0, -2.6], Y=[5, 35]
  (mirror of east)
```
2 elements.

### C.2 Track Floor (CORRECTED: 0.3m thick)
```
Track_floor: wedge box X=[-3, 3], Y=[5, 35]
  Bottom: Z=[4.7, 4.7, 20.7, 20.7]
  Top: Z=[5.0, 5.0, 21.0, 21.0]
```
1 element.

### C.3 Track Roof
```
Track_roof: wedge box X=[-3, 3], Y=[5, 35]
  Bottom: Z=[8.0, 8.0, 24.0, 24.0]
  Top: Z=[8.25, 8.25, 24.25, 24.25]
```
1 element.

### C.4 Midpoint Landing (CORRECTED: 4m deep)
```
Track_landing: wedge box X=[-4, 4], Y=[18, 22]
  Floor Z at Y=18: 5 + (18-5)/30 * 16 = 11.93
  Floor Z at Y=22: 5 + (22-5)/30 * 16 = 14.07
  0.3m thick slab
```
1 element.

### C.5 Track Windows — Progressive Sizing (Layer: Openings)
East wall (glass thickness 0.02m):

**Bottom third (Y=5–15): Small slots 0.8m × 1.0m** — 3 panes at Y=[7, 9.5, 12]
**Middle third (Y=15–25): Medium 1.2m × 1.5m** — 3 panes at Y=[17, 20, 23]
**Top third (Y=25–35): Large 2.0m × 2.0m** — 3 panes at Y=[27, 30, 33]

West wall: mirror all 9.
Glass at X=2.85 (CORRECTED: recessed to wall midplane, not flush).
**18 glass panes.**

### C.6 Track Window Mullions (Layer: Openings)
0.1m deep × 0.05m wide aluminum frames (CORRECTED: depth increased from 0.05 to 0.1 for weather resistance on slope).
4 frame members per window × 18 windows = **72 mullion elements.**

### C.7 Track Rails (Layer: Circulation, CORRECTED: 2.5m spacing)
```
Track_rail_ascending:  polyline (1.25, 5, 5.0) → (1.25, 35, 21.0)
Track_rail_descending: polyline (-1.25, 5, 5.0) → (-1.25, 35, 21.0)
```
2 elements.

### C.8 Funicular Carriage (ADDED — Layer: Circulation)
Schematic carriage at midpoint for representation:
```
Carriage: box at (-1.0, 19.5, z_floor+0.1) → (1.0, 21.5, z_floor+2.8)
```
Interior: 2.0m wide × 2.0m long × 2.7m tall (wheelchair accessible 1.1×1.4m min).
1 element.

### C.9 Fire Doors at Track Junctions (ADDED — Layer: Openings)
```
Fire_door_valley:  box at (-3.0, 5.0, 5.0) → (3.0, 5.1, 8.0)  — EI 60 roller shutter
Fire_door_hilltop: box at (-3.0, 34.9, 21.0) → (3.0, 35.0, 24.0)  — EI 60 roller shutter
```
2 elements (thin slab representing closed fire door position).

### C.10 Track Roof Waterproofing (ADDED — Layer: L400_Material)
```
Track_roof_membrane: wedge at Z=[8.25 to 8.257], matching track roof footprint
Track_roof_insulation: wedge at Z=[8.257 to 8.357] (100mm, reduced for sloped application)
```
2 elements.

**Section C subtotal: 102 elements**

---

## SECTION D: HILLTOP STATION — REHABILITATION PAVILION

Layer: `Type_08_AltitudeS::Volumes`
Envelope: X=[-10, 10], Y=[35, 50], Z=[21, 27]
Wall thickness: 0.2m (200mm RC C25/30, REI 90 confirmed with 25mm min cover)

### D.1 South Wall (Y=35.0 to 35.2)
Opening: Track connection X=[-3, 3], Z=[21, 25]
```
Hilltop_wall_S_left:   [-10.0, 35.0, 21.0] → [-3.0, 35.2, 27.0]
Hilltop_wall_S_right:  [ 3.0, 35.0, 21.0] → [10.0, 35.2, 27.0]
Hilltop_wall_S_lintel: [-3.0, 35.0, 25.0] → [ 3.0, 35.2, 27.0]
```
3 elements.

### D.2 North Wall — Panoramic Glazing (Y=49.8 to 50.0)
```
Hilltop_wall_N_pier_W:    [-10.0, 49.8, 21.0] → [-8.0, 50.0, 27.0]
Hilltop_wall_N_pier_E:    [ 8.0, 49.8, 21.0] → [10.0, 50.0, 27.0]
Hilltop_wall_N_spandrel:  [-8.0, 49.8, 26.0] → [ 8.0, 50.0, 27.0]
```
3 elements.

### D.3 East Wall (X=9.8 to 10.0)
2 floor-to-ceiling windows, piers between.
```
Hilltop_wall_E_pier_S:   [9.8, 35.2, 21.0] → [10.0, 38.0, 27.0]
Hilltop_wall_E_pier_mid: [9.8, 42.0, 21.0] → [10.0, 44.0, 27.0]
Hilltop_wall_E_pier_N:   [9.8, 48.0, 21.0] → [10.0, 49.8, 27.0]
Hilltop_wall_E_sill_1:   [9.8, 38.0, 21.0] → [10.0, 42.0, 21.5]
Hilltop_wall_E_sill_2:   [9.8, 44.0, 21.0] → [10.0, 48.0, 21.5]
```
5 elements.

### D.4 West Wall (X=-10.0 to -9.8)
Mirror of east:
5 elements.

### D.5 Hilltop Floor Slab
```
Hilltop_floor_slab: [-10.0, 35.0, 20.7] → [10.0, 50.0, 21.0]
```
0.3m RC slab.
1 element.

### D.6 Hilltop Roof Slab (Layer: L300_Roof)
```
Hilltop_roof_slab: [-10.0, 35.0, 27.0] → [10.0, 50.0, 27.2]
```
0.2m RC structural slab (CORRECTED: separated from assembly layers).
1 element.

### D.7 Hilltop Roof Parapets (Layer: L300_Roof)
1.1m high above finished roof (Z=27.458):
```
Hilltop_parapet_N: [-10.0, 49.8, 27.458] → [10.0, 50.0, 28.558]
Hilltop_parapet_E: [9.8, 35.0, 27.458] → [10.0, 49.8, 28.558]
Hilltop_parapet_W: [-10.0, 35.0, 27.458] → [-9.8, 49.8, 28.558]
Hilltop_parapet_S: [-10.0, 35.0, 27.458] → [10.0, 35.2, 28.558]
```
4 elements.

### D.8 North Panoramic Glazing (Layer: Openings)
Curtain wall X=[-8, 8], Z=[22, 26], Y=49.8.
Vertical mullions at 2m spacing (9 mullions), horizontal transoms at Z=24 (8 transoms), 16 glass panes.
**33 elements** (9 + 8 + 16).

### D.9 East Window Glazing (Layer: Openings)
2 windows, each with glass pane + 4 frame mullions = 10 elements.

### D.10 West Window Glazing (Layer: Openings)
Mirror of east = 10 elements.

### D.11 Hilltop Escape Stair — External (ADDED — Layer: Circulation)
East face, Z=21 to grade (~Z=18 at Y=42). Steel open stair, 1.5m wide:
```
Hilltop_escape_stair_landing: [10.0, 41.0, 21.0] → [11.5, 43.0, 21.15]
Hilltop_escape_stair_flight1: wedge [10.0, 43.0, 21.0] → [11.5, 46.0, 19.5]  (down)
Hilltop_escape_stair_landing2: [10.0, 46.0, 19.35] → [11.5, 48.0, 19.5]
Hilltop_escape_stair_flight2: wedge [10.0, 48.0, 19.5] → [11.5, 51.0, 18.0]  (down to grade)
Hilltop_escape_railing_E: pipe along stair east edge, Z+1.1m above tread
Hilltop_escape_railing_W: pipe along stair west edge
```
6 elements (2 flights + 2 landings + 2 railings).

**Section D subtotal: 81 elements**

---

## SECTION E: VERTICAL CORE — MECHANICAL ROOM + STAIR

Layer: `Type_08_AltitudeS::Volumes`
Envelope: X=[-3, 3], Y=[42, 48], Z=[21, 28]
Wall thickness: 0.3m RC

### E.1 Core Walls
Opening on west: door Y=[44.3, 46.0], Z=[21, 24.5]
```
Core_wall_S: [-3.0, 42.0, 21.0] → [3.0, 42.3, 28.0]
Core_wall_N: [-3.0, 47.7, 21.0] → [3.0, 48.0, 28.0]
Core_wall_E: [2.7, 42.3, 21.0] → [3.0, 47.7, 28.0]
Core_wall_W_lower: [-3.0, 42.3, 21.0] → [-2.7, 44.3, 28.0]
Core_wall_W_upper: [-3.0, 46.0, 21.0] → [-2.7, 47.7, 28.0]
Core_wall_W_lintel: [-3.0, 44.3, 24.5] → [-2.7, 46.0, 28.0]
```
6 elements. (CORRECTED: no separate columns — 300mm walls are loadbearing.)

### E.2 Core Roof Slab (Layer: L300_Roof)
```
Core_roof_slab: [-3.0, 42.0, 28.0] → [3.0, 48.0, 28.2]
```
0.2m RC structural slab.
1 element.

### E.3 Internal Stair — Roof/Mechanical Access (CORRECTED title)
7m rise (Z=21→28). R=0.165m, G=0.295m. 4 flights switchback.
Stair layout: two 1.5m-wide runs with 0.2m gap, centered in core.
```
Core_stair_flight_1: wedge Y=[42.5, 45.7], run 1 (X=[-2.5, -1.0])
Core_stair_landing_1: [-2.5, 45.7, 22.815] → [2.5, 47.5, 22.965]
Core_stair_flight_2: wedge Y=[47.5, 44.3], run 2 (X=[1.0, 2.5])
Core_stair_landing_2: [-2.5, 42.5, 24.78] → [2.5, 44.3, 24.93]
Core_stair_flight_3: wedge Y=[42.5, 45.7], run 1
Core_stair_landing_3: [-2.5, 45.7, 26.745] → [2.5, 47.5, 26.895]
Core_stair_flight_4: wedge Y=[47.5, 44.5], run 2
```
7 elements (4 flights + 3 landings).

### E.4 Stair Railings (Layer: Circulation)
Both sides per flight (SIA 500): 0.044m pipes at 1.1m + second rail at 0.75m.
4 flights × 2 sides × 2 heights = 16 railing pipes.
**16 elements** (CORRECTED: added second handrails).

### E.5 Tactile Warning Strips (ADDED — Layer: L350_Detail)
0.6m deep strip at top and bottom of each flight:
4 flights × 2 ends = 8 thin box elements.
**8 elements.**

**Section E subtotal: 38 elements**

---

## SECTION F: TERRACE / VERANDA

### F.1 Terrace Platform (Layer: Volumes, CORRECTED: 0.25m thick)
```
Terrace_platform: [-10.0, 48.0, 20.75] → [13.0, 53.0, 21.0]
```
0.25m RC slab on steel frame.
1 element.

### F.2 Terrace Waterproofing (ADDED — Layer: L400_Material)
```
Terrace_membrane: [-10.0, 48.0, 21.0] → [13.0, 53.0, 21.007]
Terrace_screed: [-10.0, 48.0, 21.007] → [13.0, 53.0, 21.037]  (30mm falls screed, 1.5% slope to north)
```
2 elements.

### F.3 Terrace Railings (Layer: Circulation)
SIA 358: 1.1m guardrails, 0.044m pipes:
```
Terrace_railing_N: pipe Y=53.0, Z=22.1, X=[-10, 13]
Terrace_railing_E: pipe X=13.0, Z=22.1, Y=[48, 53]
Terrace_railing_S_ext: pipe Y=48.0, Z=22.1, X=[10, 13]
```
3 elements.

### F.4 Terrace Columns (Layer: Structure, CORRECTED: 0.2×0.2m, 5m spacing)
```
Terrace_col_1: [12.8, 48.0, 17.0] → [13.0, 48.2, 21.0]
Terrace_col_2: [12.8, 53.0, 17.0] → [13.0, 53.2, 21.0]
Terrace_col_3: [7.8, 52.8, 18.5] → [8.0, 53.0, 21.0]
Terrace_col_4: [2.8, 52.8, 19.0] → [3.0, 53.0, 21.0]
Terrace_col_5: [-2.2, 52.8, 19.5] → [-2.0, 53.0, 21.0]
Terrace_col_6: [-7.2, 52.8, 19.8] → [-7.0, 53.0, 21.0]
```
6 elements (CORRECTED: 6 columns at ~5m spacing).

### F.5 Terrace Beams (ADDED — Layer: Structure)
Steel beams supporting terrace slab at 5m spacing:
```
Terrace_beam_1: [10.0, 48.0, 20.5] → [13.0, 48.2, 20.75]
Terrace_beam_2: [10.0, 53.0, 20.5] → [13.0, 53.2, 20.75]
Terrace_beam_3: [-10.0, 53.0, 20.5] → [13.0, 53.2, 20.75]
```
3 elements.

**Section F subtotal: 15 elements**

---

## SECTION G: GARDEN PLATFORM

### G.1 Garden Slab (Layer: Volumes)
```
Garden_platform: [-14.0, 45.0, 20.5] → [14.0, 55.0, 20.975]
```
0.475m RC platform (CORRECTED: top raised to Z=20.975, only 25mm below hilltop floor — accessible).
1 element.

### G.2 Garden Support Piers (ADDED — Layer: Structure)
6 piers supporting the 28m span:
```
Garden_pier_1: [-7.1, 48.0, 16.0] → [-6.9, 48.2, 20.5]
Garden_pier_2: [0.0, 48.0, 17.0] → [0.2, 48.2, 20.5]
Garden_pier_3: [6.9, 48.0, 17.5] → [7.1, 48.2, 20.5]
Garden_pier_4: [-7.1, 52.0, 17.0] → [-6.9, 52.2, 20.5]
Garden_pier_5: [0.0, 52.0, 18.0] → [0.2, 52.2, 20.5]
Garden_pier_6: [6.9, 52.0, 18.5] → [7.1, 52.2, 20.5]
```
6 elements.

### G.3 Garden Beam Grid (ADDED — Layer: Structure)
2 E-W beams supporting garden slab:
```
Garden_beam_1: [-14.0, 48.0, 20.2] → [14.0, 48.3, 20.5]
Garden_beam_2: [-14.0, 52.0, 20.2] → [14.0, 52.3, 20.5]
```
2 elements.

### G.4 Garden Edge Parapets (Layer: L300_Roof)
```
Garden_parapet_N: [-14.0, 54.8, 20.975] → [14.0, 55.0, 22.075]
Garden_parapet_E: [13.8, 45.0, 20.975] → [14.0, 54.8, 22.075]
Garden_parapet_W: [-14.0, 45.0, 20.975] → [-13.8, 54.8, 22.075]
```
3 elements.

### G.5 Garden Waterproofing (ADDED — Layer: L400_Material)
```
Garden_membrane: [-14.0, 45.0, 20.975] → [14.0, 55.0, 20.982]
Garden_root_barrier: [-14.0, 45.0, 20.982] → [14.0, 55.0, 20.984]
```
2 elements.

**Section G subtotal: 14 elements**

---

## SECTION H: TERRAIN PROXY

### H.1 Tilted Surface (Layer: Volumes)
```
Terrain_proxy: wedge box
  SW: (-20, -10, -1), SE: (20, -10, -1)
  NW: (-20, 55, 20), NE: (20, 55, 20)
  Thickness: 0.1m
```
1 element.

---

## SECTION I: STRUCTURE

Layer: `Type_08_AltitudeS::Structure`

### I.1 Valley Columns — 4 heavy (0.4×0.4m)
```
Valley_col_SW: [-4.8, -4.8, -0.3] → [-4.4, -4.4, 5.0]
Valley_col_SE: [4.4, -4.8, -0.3] → [4.8, -4.4, 5.0]
Valley_col_NW: [-4.8, 4.4, -0.3] → [-4.4, 4.8, 5.0]
Valley_col_NE: [4.4, 4.4, -0.3] → [4.8, 4.8, 5.0]
```
4 elements.

### I.2 Valley Beams — 2 (bearing on 400mm RC walls)
```
Valley_beam_S: [-5.0, -2.3, 4.5] → [5.0, -2.0, 5.0]
Valley_beam_N: [-5.0, 2.0, 4.5] → [5.0, 2.3, 5.0]
```
2 elements.

### I.3 Hilltop Columns — 8 slender (CORRECTED: 0.3×0.3m, added 2 at X=±5)
```
Hilltop_col_1: [-8.15, 37.85, 21.0] → [-7.85, 38.15, 27.0]
Hilltop_col_2: [-5.15, 37.85, 21.0] → [-4.85, 38.15, 27.0]  (ADDED)
Hilltop_col_3: [0.0, 37.85, 21.0] → [0.3, 38.15, 27.0]
Hilltop_col_4: [4.85, 37.85, 21.0] → [5.15, 38.15, 27.0]  (ADDED)
Hilltop_col_5: [7.85, 37.85, 21.0] → [8.15, 38.15, 27.0]
Hilltop_col_6: [-8.15, 46.85, 21.0] → [-7.85, 47.15, 27.0]
Hilltop_col_7: [0.0, 46.85, 21.0] → [0.3, 47.15, 27.0]
Hilltop_col_8: [7.85, 46.85, 21.0] → [8.15, 47.15, 27.0]
```
8 elements (CORRECTED: 2 more + all 0.3×0.3m).

### I.4 Hilltop Beams — 2 primary + 2 lateral tie beams (ADDED)
Primary E-W beams (10m spans with intermediate columns):
```
Hilltop_beam_1: [-10.0, 37.85, 26.5] → [10.0, 38.15, 27.0]
Hilltop_beam_2: [-10.0, 46.85, 26.5] → [10.0, 47.15, 27.0]
```

Lateral tie beams N-S connecting core to hilltop frame (ADDED for stability):
```
Hilltop_tie_beam_E: [2.7, 38.15, 26.7] → [3.0, 42.0, 27.0]
Hilltop_tie_beam_W: [-3.0, 38.15, 26.7] → [-2.7, 42.0, 27.0]
```
4 elements.

### I.5 Track Steel Frames — 5 frames at Y=[10, 15, 20, 25, 30]
Each frame: 2 posts (SHS 200×200) + 1 beam.
z_floor(y) = 5 + (y-5)/30 * 16
z_roof(y) = 8 + (y-5)/30 * 16

```
Frame at Y=10: z_floor=7.67, z_roof=10.67
Frame at Y=15: z_floor=10.33, z_roof=13.33
Frame at Y=20: z_floor=13.0, z_roof=16.0
Frame at Y=25: z_floor=15.67, z_roof=18.67
Frame at Y=30: z_floor=18.33, z_roof=21.33
```
5 × 3 = **15 elements.**

### I.6 Track Longitudinal Beams — 2 (IPE 200)
```
Track_long_beam_E: wedge X=[1.5, 1.7], Y=[5, 35], Z follows grade -0.2m
Track_long_beam_W: wedge X=[-1.7, -1.5], mirrored
```
2 elements.

### I.7 Transfer Beams at Track Junctions (ADDED)
```
Transfer_beam_valley: [-3.0, 4.6, 4.6] → [3.0, 5.0, 5.0]  (at valley-track junction)
Transfer_beam_hilltop: [-3.0, 35.0, 20.6] → [3.0, 35.2, 21.0]  (at track-hilltop junction)
```
2 elements.

### I.8 Foundations — Schematic (ADDED)
Valley pad footings (0.8×0.8×0.4m at Z=-1.0):
```
Foundation_valley_SW: [-5.2, -5.2, -1.0] → [-4.0, -4.0, -0.3]
Foundation_valley_SE: [4.0, -5.2, -1.0] → [5.2, -4.0, -0.3]
Foundation_valley_NW: [-5.2, 4.0, -1.0] → [-4.0, 5.2, -0.3]
Foundation_valley_NE: [4.0, 4.0, -1.0] → [5.2, 5.2, -0.3]
```
Valley strip footing (continuous under walls):
```
Foundation_valley_strip: [-5.4, -5.4, -1.0] → [5.4, 5.4, -0.6]
```
5 elements.

**Section I subtotal: 42 elements**

---

## SECTION J: ENTRY ELEMENTS (Layer: Openings)

### J.1 Valley Ambulance Canopy
```
Valley_canopy_slab: [-3.0, -7.0, 3.5] → [3.0, -5.0, 3.6]
Valley_canopy_col_W: [-2.9, -6.9, 0.0] → [-2.7, -6.7, 3.5]
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

### J.3 Valley West Emergency Exit Frame (ADDED)
```
Valley_exit_frame_L: [-5.0, -1.1, 0.0] → [-4.6, -1.0, 2.1]
Valley_exit_frame_R: [-5.0, 1.0, 0.0] → [-4.6, 1.1, 2.1]
Valley_exit_frame_head: [-5.0, -1.1, 2.0] → [-4.6, 1.1, 2.1]
```
3 elements.

### J.4 Hilltop Threshold
```
Hilltop_threshold_N: [-8.0, 49.8, 21.0] → [8.0, 50.0, 21.025]
```
1 element.

### J.5 Valley Entry Threshold (ADDED — flush, Z=0.0)
```
Valley_threshold_S: [-2.0, -5.1, -0.02] → [2.0, -5.0, 0.0]
```
1 element.

**Section J subtotal: 11 elements**

---

## SECTION K: L350 DETAIL

Layer: `Type_08_AltitudeS::L350_Detail`

### K.1 Valley Base Plates (under columns, 0.5×0.5×0.03m)
4 elements.

### K.2 Hilltop Base Plates (under columns, 0.4×0.4×0.025m)
8 elements (CORRECTED: 8 columns now).

### K.3 Valley Kickers (DPC strip at wall base, 0.01m thick)
4 elements (S, N, E, W walls).

### K.4 Hilltop Kickers
4 elements (S, E, W walls + N pier bases).

### K.5 Valley Lintels (steel, 0.1×0.3m profile)
3 elements (S entry + N track opening + W emergency exit).

### K.6 Hilltop Lintels
5 elements (S track + E×2 + W×2 windows).

### K.7 Track Frame Base Plates (0.3×0.3×0.025m)
10 elements (5 frames × 2 posts).

### K.8 Terrace Brackets (L-brackets)
4 elements.

### K.9 Core Door Fire Frame (ADDED — EI 30, Layer: L350_Detail)
```
Core_fire_frame: [-3.0, 44.3, 21.0] → [-2.7, 46.0, 24.5] (thin frame around opening)
```
1 element.

### K.10 Track Window Sill Flashings (ADDED — 18 flashings)
Thin sloped boxes at each window sill, draining outward.
18 elements.

### K.11 Hilltop Curtain Wall Head Flashing (ADDED)
```
Hilltop_head_flashing_N: [-8.0, 49.75, 25.98] → [8.0, 49.85, 26.0]
```
1 element.

**Section K subtotal: 62 elements**

---

## SECTION L: L400 MATERIAL

Layer: `Type_08_AltitudeS::L400_Material`

### L.1 Valley Roof Assembly (on Valley_roof_slab Z=5.3)
```
Valley_roof_vapour_barrier: [-5.0, -5.0, 5.3] → [5.0, 5.0, 5.301]
Valley_roof_insulation: [-5.0, -5.0, 5.301] → [5.0, 5.0, 5.501]
Valley_roof_membrane: [-5.0, -5.0, 5.501] → [5.0, 5.0, 5.508]
Valley_roof_gravel: [-5.0, -5.0, 5.508] → [5.0, 5.0, 5.558]
```
4 elements.

### L.2 Valley Roof Upstands (membrane turn-up, 0.15m)
4 elements (S, N, E, W).

### L.3 Valley Roof Drip Edges
4 elements.

### L.4 Hilltop Roof Assembly (on slab Z=27.2)
```
Hilltop_roof_vapour_barrier: [-10.0, 35.0, 27.2] → [10.0, 50.0, 27.201]
Hilltop_roof_insulation: [-10.0, 35.0, 27.201] → [10.0, 50.0, 27.401]
Hilltop_roof_membrane: [-10.0, 35.0, 27.401] → [10.0, 50.0, 27.408]
Hilltop_roof_gravel: [-10.0, 35.0, 27.408] → [10.0, 50.0, 27.458]
```
4 elements.

### L.5 Hilltop Roof Upstands
4 elements.

### L.6 Hilltop-to-Core Roof Upstand (ADDED)
```
Core_roof_upstand: membrane turn-up at core wall faces where they project above hilltop roof.
```
4 thin elements around core perimeter at Z=27.401 to 27.551.

### L.7 Expansion Joint Assemblies (CORRECTED: detailed)
```
Joint_valley_track: box [-3.0, 4.9, 5.0] → [3.0, 5.1, 8.0] (0.2m wide neoprene + cover flashing)
Joint_track_hilltop: box [-3.0, 34.9, 21.0] → [3.0, 35.1, 24.0]
```
2 elements (visible joint assemblies, not just lines).

### L.8 Formwork Lines (valley exterior — expressing concrete character)
12 lines at Z=[1.2, 2.4, 3.6] on 4 faces.

### L.9 Track Roof Waterproofing (counted in C.10)
Already counted.

**Section L subtotal: 38 elements**

---

## SECTION M: ANNOTATIONS

Layer: `Type_08_AltitudeS::Annotations`

```
TextDot_1:  "EMERGENCY / FAST / COMPACT" at (0, 0, 2.5)
TextDot_2:  "TRANSITION / WINDOWS GROW" at (0, 15, 10.3)
TextDot_3:  "MIDPOINT LANDING" at (0, 20, 13.5)
TextDot_4:  "REHABILITATION / SLOW / EXPANSIVE" at (0, 42.5, 24.0)
TextDot_5:  "GARDEN / RECOVERY" at (0, 50, 22.0)
TextDot_6:  "ASCENDING = DECELERATING" at (2, 25, 16.0)
TextDot_7:  "MECHANICAL CORE" at (0, 45, 25.0)
TextDot_8:  "AMBULANCE ENTRY" at (0, -6, 2.0)
TextDot_9:  "PANORAMIC VIEW NORTH" at (0, 50, 24.0)
TextDot_10: "TERRACE / VERANDA" at (5, 51, 22.0)
TextDot_11: "EMERGENCY EXIT WEST" at (-6, 0, 1.0)
TextDot_12: "ESCAPE STAIR" at (11, 45, 20.0)
```
**12 elements.**

---

## SECTION N: CIRCULATION PATHS

Layer: `Type_08_AltitudeS::Circulation`

### N.1 Emergency Arrival (CORRECTED: carriage at Z=0)
```
Circ_emergency: polyline [(0, -7, 0.1), (0, -5, 0.1), (0, 0, 0.1), (0, 5, 0.1)]
  → boards carriage → carriage ascends to (0, 35, 21.1)
```
1 element.

### N.2 Rehabilitation Path
```
Circ_rehab: polyline [(0, 35, 21.1), (0, 42, 21.1), (0, 48, 21.1), (0, 51, 21.1), (5, 51, 21.1)]
```
1 element.

### N.3 Terrace Loop (CORRECTED: reconnects to building)
```
Circ_garden_loop: polyline [(-5, 48, 21.1), (-5, 53, 21.1), (10, 53, 21.1), (10, 48, 21.1), (0, 48, 21.1), (0, 42, 21.1)]
```
1 element.

### N.4 Discharge Path (ADDED)
```
Circ_discharge: polyline [(0, 42, 21.1), (0, 35, 21.1), (0, 5, 5.1), (0, 0, 0.1), (0, -5, 0.1), (0, -7, 0.1)]
```
1 element.

**Section N subtotal: 4 elements**

---

## ELEMENT COUNT SUMMARY

| Section | Description | Count |
|---------|-------------|-------|
| B | Valley Station (walls + slabs + parapets) | 24 |
| C | Inclined Track (tube + windows + mullions + rails + carriage + fire doors + WP) | 102 |
| D | Hilltop Station (walls + floor + roof + glazing + escape stair) | 81 |
| E | Vertical Core (walls + roof + stair + railings + tactile strips) | 38 |
| F | Terrace (platform + WP + railings + columns + beams) | 15 |
| G | Garden Platform (slab + piers + beams + parapets + WP) | 14 |
| H | Terrain Proxy | 1 |
| I | Structure (columns + beams + frames + transfers + foundations) | 42 |
| J | Entry Elements (canopy + doors + thresholds) | 11 |
| K | L350 Detail (plates + kickers + lintels + flashings + fire frame) | 62 |
| L | L400 Material (roof assemblies + upstands + drips + joints + formwork) | 38 |
| M | Annotations | 12 |
| N | Circulation Paths | 4 |
| **TOTAL** | | **444** |

---

## BUILD ORDER

1. **Layers** (all 8, before any geometry)
2. **Structure** (I: columns, beams, frames, foundations, transfers) — 42 elements
3. **Volumes** (B, C.1-C.4, D.1-D.5, E.1, F.1, G.1, H) — primary massing — ~60 elements
4. **Health check #1**: verify structure + volumes count
5. **Openings** (C.5-C.6, C.9, D.8-D.10, J) — glazing, doors, canopy — ~100 elements
6. **Circulation** (C.7-C.8, D.11, E.3-E.5, F.3, N) — paths, stairs, railings — ~35 elements
7. **Roof** (B.7, D.6-D.7, E.2, G.4) — slabs, parapets — ~13 elements
8. **Health check #2**: verify all above
9. **Detail** (K) — base plates, kickers, lintels, flashings — 62 elements
10. **Material** (L) — roof assemblies, upstands, drips, joints, formwork — 38 elements
11. **Annotations** (M) — text dots — 12 elements
12. **Final health check**: total count vs 444

---

## SUCCESS CRITERIA

1. Valley station visibly SMALLER and more ENCLOSED than hilltop
2. Hilltop pavilion visibly LARGER and more OPEN
3. Track windows grow larger ascending — visible gradient
4. Terrace/garden reads as generous outdoor space
5. Asymmetry between heavy valley and light hilltop is immediate
6. All parapets at SIA 358 compliant heights
7. Stair meets Blondel formula
8. Two exits from each station (fire safety)
9. Fire compartmentation at track junctions (doors modeled)
10. Roof assemblies complete (warm deck stacks)
11. Garden accessible (25mm max lip)
12. Total element count within ±5% of 444
