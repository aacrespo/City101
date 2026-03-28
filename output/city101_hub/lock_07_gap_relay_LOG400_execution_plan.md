# Lock Type 07 — Gap Relay
# LOG400 Execution Spec: DRAFT FOR ROUNDTABLE REVIEW
# Status: DRAFT
# Date: 2026-03-27

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry authored in METER-SCALE values.
"10.0" in Rhino = 10.0 as a number, conceptually 10m.
**Do NOT multiply by 100. Do NOT convert.**

X = East–West (positive = East)
Y = North–South (positive = North)
Z = vertical (0 = finished floor)

**MCP target: `structure` (port 9001)**

---

## CONCEPT SUMMARY

Three-arm junction: Hub + Arm A (South/Rail) + Arm B (West/Lateral) + Arm C (NE/Uphill).
The occupant arrives from one direction and is redirected to another. Dwell time is minutes.
The Hub is the tallest element — a porous octagonal core where all flows converge.
Arms are lower, directional, reaching outward. Canopies mark transitions at arm tips.

**State transition:** Gap (broken chain) <-> Continuity (chain sustained)

**Key principle:** SMALLEST and most OPEN of all 9 types. Junction, not building.

---

## ARCHIBASE-GROUNDED DIMENSIONS

### Structural (from steel_structures.md, concrete_systems.md)

| Element | Dimension | Source |
|---------|-----------|--------|
| Hub columns (RC) | 0.30m x 0.30m | Archibase: ~350kN load, HEA 200 equiv -> 300mm RC |
| Arm columns (steel HEA 200) | 0.20m x 0.20m modeled | Archibase: steel_profiles, lightweight arms |
| Canopy columns (steel CHS 114.3) | 0.15m x 0.15m modeled | Archibase: light gauge, <100kN per column |
| Hub roof beams (steel IPE 270) | 0.27m depth x 0.135m | Archibase: span/25 for 7m radial span |
| Transfer beams at arm junctions | 0.40m depth x 0.30m | Archibase: 6m span, composite steel-concrete |
| Ground slab (RC) | 0.30m thick | Archibase: span/30 for 10m hub, concrete_systems.md |
| Arm floor slabs | 0.25m thick | Archibase: span/30 for 6m arm width |

### Envelope (from facade_systems.md, concrete_systems.md)

| Element | Dimension | Source |
|---------|-----------|--------|
| Hub walls (RC + insulation) | 0.30m total | 200mm RC + 80mm mineral wool + 20mm render |
| Arm walls (light steel frame) | 0.20m total | 150mm steel stud + 40mm insulation + 10mm panel |
| Curtain wall mullions | 0.05m x 0.05m aluminum | Archibase: facade_systems.md stick system |
| Glass panels (IGU triple) | 0.04m thick | Archibase: 6+16+6+16+6mm standard triple |
| Canopy roof (steel plate) | 0.01m (10mm) | Archibase: steel plate canopy, lightweight |

### Roof Assembly (from details_roof_parapet.md, Deplazes p.470)

Hub flat roof warm deck (top to bottom):
- Gravel ballast: 60mm
- Filter fleece: 2mm
- Bituminous membrane (2 layers): 10mm
- Insulation (EPS): 200mm
- Vapour barrier: 2mm
- RC slab: 250mm
- Interior plaster: 5mm
**Total assembly: 529mm -> modeled as 0.53m**

### Foundation (from foundation_types.md, vittone_foundations.md)

| Element | Dimension | Source |
|---------|-----------|--------|
| Pad footings (hub columns) | 1.0m x 1.0m x 0.40m | Archibase: 3x column width, 400mm depth |
| Strip footings (arm walls) | 0.60m wide x 0.40m deep | Archibase: continuous under walls |
| Frost depth | 0.80m minimum | Archibase: Swiss standard, non-alpine |

### Circulation (from stair_railing_systems.md, SIA 500)

| Element | Dimension | Source |
|---------|-----------|--------|
| Ramp gradient (Arm C) | 6% max (1:17) | SIA 500, Archibase |
| Ramp width | 1.50m minimum | SIA 500 |
| Landing every | 6.0m of run | SIA 500 |
| Railing height | 1.10m | SIA 358 (public building) |
| Railing post spacing | 1.50m max | SIA 358 |
| Handrail diameter | 0.044m (round) | SIA 500 |
| Handrail extension | 0.30m beyond ramp | SIA 500 |
| Infill gap max | 0.12m | SIA 358 (child safety) |

### Code Compliance (from swiss_fire_code.md, SIA)

| Requirement | Value | Standard |
|-------------|-------|----------|
| Floor-to-floor clearance | 2.70m min habitable | SIA 180 |
| Max travel distance to exit | 35m | VKF |
| Parapet/guardrail height | 1.07m min | SIA 358 |
| Fire rating (structure) | REI 60 | VKF, public building <11m |
| Door clear width | 0.90m min | SIA 500 |
| Turning radius | 1.50m at direction changes | SIA 500 |

---

## LAYERS TO CREATE (8 layers)

```
Type_07_GapRelay::Volumes        — RGB(240, 101, 149)  — wall shells, floor slabs, arm volumes
Type_07_GapRelay::Circulation    — RGB(245, 170, 190)  — paths, ramp, railings
Type_07_GapRelay::Structure      — RGB(170, 72, 105)   — columns, beams, footings
Type_07_GapRelay::Openings       — RGB(242, 140, 170)  — door/window frames, glass, mullions
Type_07_GapRelay::Annotations    — RGB(248, 200, 215)  — text dots
Type_07_GapRelay::L300_Roof      — RGB(200, 85, 130)   — roof slabs, parapets, canopy slabs
Type_07_GapRelay::L350_Detail    — RGB(160, 65, 100)   — connections, brackets, frames
Type_07_GapRelay::L400_Material  — RGB(120, 48, 75)    — formwork, joints, hardware, assembly layers
```

---

## SECTION A — HUB CORE (Volumes + Structure)

### Hub Geometry
Octagonal plan: 10m x 10m square with 2m corner chamfers at 45deg.
Z = [0, 7]. Double-height open interior.

Wall thickness: 0.30m (RC + insulation assembly).
Inner boundary: X=[-5, 5], Y=[-5, 5] with chamfered corners.

### A.1 Hub Walls (8 segments for octagon)

Layer: `Type_07_GapRelay::Volumes`

**South wall** (Arm A opening: X=[-3, 3], full height):
```
A1_hub_wall_S_left:    [-5.0, -5.3, 0.0] -> [-3.0, -5.0, 7.0]
A1_hub_wall_S_right:   [ 3.0, -5.3, 0.0] -> [ 5.0, -5.0, 7.0]
```

**North wall** (solid — no arm on north):
```
A1_hub_wall_N:         [-5.0,  5.0, 0.0] -> [ 5.0,  5.3, 7.0]
```

**West wall** (Arm B opening: Y=[-3, 3], full height):
```
A1_hub_wall_W_left:    [-5.3, -5.0, 0.0] -> [-5.0, -3.0, 7.0]
A1_hub_wall_W_right:   [-5.3,  3.0, 0.0] -> [-5.0,  5.0, 7.0]
```

**East wall** (solid — SE face has single window):
```
A1_hub_wall_E:         [ 5.0, -5.0, 0.0] -> [ 5.3,  5.0, 7.0]
```

**Chamfer walls** (4 diagonal infills at 45deg, 2m face width, 0.30m thick):
NW chamfer corner at (-5, 5): wall from (-5, 3) to (-3, 5), 0.3m outward
NE chamfer at (5, 5): from (3, 5) to (5, 3) — **OPENING for Arm C** (no wall here)
SW chamfer at (-5, -5): from (-5, -3) to (-3, -5)
SE chamfer at (5, -5): from (3, -5) to (5, -3) — solid wall with window

Diagonal walls modeled as box_pts (8 explicit corners for angled geometry):
```
A1_hub_chamfer_NW: diagonal wall (-5,3,0)->(-3,5,0), 0.3m outward NW, H=7.0
A1_hub_chamfer_SW: diagonal wall (-5,-3,0)->(-3,-5,0), 0.3m outward SW, H=7.0
A1_hub_chamfer_SE: diagonal wall (3,-5,0)->(5,-3,0), 0.3m outward SE, H=7.0
```
NE chamfer: OPEN (Arm C connection)

**Hub walls: 8 elements**

### A.2 Hub Floor Slab

Layer: `Type_07_GapRelay::Volumes`

```
A2_hub_floor_slab:     [-5.3, -5.3, -0.30] -> [5.3, 5.3, 0.0]
```

**Hub floor: 1 element**

### A.3 Hub Columns (8 at octagon vertices)

Layer: `Type_07_GapRelay::Structure`

0.30m x 0.30m RC columns, Z=[0, 7.0]. Positioned at octagon vertices (r=5.0m from center):
```
A3_col_hub_N:     [-0.15,  4.85, 0.0] -> [ 0.15,  5.15, 7.0]
A3_col_hub_S:     [-0.15, -5.15, 0.0] -> [ 0.15, -4.85, 7.0]
A3_col_hub_E:     [ 4.85, -0.15, 0.0] -> [ 5.15,  0.15, 7.0]
A3_col_hub_W:     [-5.15, -0.15, 0.0] -> [-4.85,  0.15, 7.0]
A3_col_hub_NW:    [-3.68,  3.38, 0.0] -> [-3.38,  3.68, 7.0]
A3_col_hub_NE:    [ 3.38,  3.38, 0.0] -> [ 3.68,  3.68, 7.0]
A3_col_hub_SW:    [-3.68, -3.68, 0.0] -> [-3.38, -3.38, 7.0]
A3_col_hub_SE:    [ 3.38, -3.68, 0.0] -> [ 3.68, -3.38, 7.0]
```

**Hub columns: 8 elements**

### A.4 Hub Roof Beams (star pattern from center to each column)

Layer: `Type_07_GapRelay::Structure`

8 radial beams from center (0, 0, 6.73) to each column top. Beam: 0.27m deep x 0.135m wide.
Bottom of beam at Z=6.73, top at Z=7.0.
```
A4_beam_hub_N:    [-0.0675,  0.15, 6.73] -> [ 0.0675,  4.85, 7.0]
A4_beam_hub_S:    [-0.0675, -4.85, 6.73] -> [ 0.0675, -0.15, 7.0]
A4_beam_hub_E:    [ 0.15, -0.0675, 6.73] -> [ 4.85,  0.0675, 7.0]
A4_beam_hub_W:    [-4.85, -0.0675, 6.73] -> [-0.15,  0.0675, 7.0]
A4_beam_hub_NW:   [-3.53,  0.0675, 6.73] -> [-0.0675,  3.53, 7.0]
A4_beam_hub_NE:   [ 0.0675,  0.0675, 6.73] -> [ 3.53,  3.53, 7.0]
A4_beam_hub_SW:   [-3.53, -3.53, 6.73] -> [-0.0675, -0.0675, 7.0]
A4_beam_hub_SE:   [ 0.0675, -3.53, 6.73] -> [ 3.53, -0.0675, 7.0]
```

**Hub beams: 8 elements**

### A.5 Hub Roof Slab

Layer: `Type_07_GapRelay::L300_Roof`

RC slab 0.25m thick spanning hub footprint. Skylight opening at center (4m x 4m).
```
A5_hub_roof_N:     [-5.3,  2.0, 7.0] -> [ 5.3,  5.3, 7.25]
A5_hub_roof_S:     [-5.3, -5.3, 7.0] -> [ 5.3, -2.0, 7.25]
A5_hub_roof_E:     [ 2.0, -2.0, 7.0] -> [ 5.3,  2.0, 7.25]
A5_hub_roof_W:     [-5.3, -2.0, 7.0] -> [-2.0,  2.0, 7.25]
```
(4 slabs framing the 4m x 4m skylight void at center)

**Hub roof slab: 4 elements**

### A.6 Skylight Frame

Layer: `Type_07_GapRelay::L350_Detail`

Steel frame 4m x 4m at Z=6.5–7.0. Frame members 0.10m x 0.10m steel:
```
A6_skylight_N:     [-2.0,  1.9, 6.5] -> [ 2.0,  2.0, 7.0]
A6_skylight_S:     [-2.0, -2.0, 6.5] -> [ 2.0, -1.9, 7.0]
A6_skylight_E:     [ 1.9, -2.0, 6.5] -> [ 2.0,  2.0, 7.0]
A6_skylight_W:     [-2.0, -2.0, 6.5] -> [-1.9,  2.0, 7.0]
```

**Skylight frame: 4 elements**

### A.7 Hub Roof Assembly (LOG400)

Layer: `Type_07_GapRelay::L400_Material`

On top of hub roof slab (Z=7.25 upward):
```
A7_roof_vapour:      [-5.3, -5.3, 7.25] -> [5.3, 5.3, 7.252]   (2mm vapour barrier)
A7_roof_insulation:  [-5.3, -5.3, 7.252] -> [5.3, 5.3, 7.452]  (200mm EPS)
A7_roof_membrane:    [-5.3, -5.3, 7.452] -> [5.3, 5.3, 7.462]  (10mm bitumen)
A7_roof_fleece:      [-5.3, -5.3, 7.462] -> [5.3, 5.3, 7.464]  (2mm filter)
A7_roof_gravel:      [-5.3, -5.3, 7.464] -> [5.3, 5.3, 7.524]  (60mm gravel)
```

**Roof assembly: 5 elements**

---

## SECTION B — ARM A: RAIL CORRIDOR (South)

### B.1 Arm A Walls

Layer: `Type_07_GapRelay::Volumes`

Arm: X=[-3, 3], Y=[-18, -5], Z=[0, 4]. Wall thickness: 0.20m.
East and west walls run full length. South face: OPEN (rail connection).
```
B1_armA_wall_E:    [ 3.0, -18.0, 0.0] -> [ 3.2, -5.0, 4.0]
B1_armA_wall_W:    [-3.2, -18.0, 0.0] -> [-3.0, -5.0, 4.0]
```

**Arm A walls: 2 elements**

### B.2 Arm A Floor Slab

Layer: `Type_07_GapRelay::Volumes`
```
B2_armA_floor:     [-3.2, -18.0, -0.25] -> [3.2, -5.0, 0.0]
```

**Arm A floor: 1 element**

### B.3 Arm A Roof Slab

Layer: `Type_07_GapRelay::L300_Roof`
```
B3_armA_roof:      [-3.2, -18.0, 4.0] -> [3.2, -5.0, 4.25]
```

**Arm A roof: 1 element**

### B.4 Arm A Columns (2 at midpoint)

Layer: `Type_07_GapRelay::Structure`

Steel columns 0.20m x 0.20m at Y=-11.5 (midpoint of arm):
```
B4_col_armA_E:     [ 2.9, -11.6, 0.0] -> [ 3.1, -11.4, 4.0]
B4_col_armA_W:     [-3.1, -11.6, 0.0] -> [-2.9, -11.4, 4.0]
```

**Arm A columns: 2 elements**

### B.5 Arm A Edge Beam

Layer: `Type_07_GapRelay::Structure`

Transfer beam at hub junction, spanning arm width:
```
B5_beam_armA_junction: [-3.0, -5.3, 3.6] -> [3.0, -5.0, 4.0]
```

**Arm A beam: 1 element**

---

## SECTION C — ARM B: LATERAL CONNECTION (West)

### C.1 Arm B Walls

Layer: `Type_07_GapRelay::Volumes`

Arm: X=[-18, -5], Y=[-3, 3], Z=[0, 4]. Wall thickness: 0.20m.
North and south walls. West face: OPEN.
```
C1_armB_wall_N:    [-18.0,  3.0, 0.0] -> [-5.0,  3.2, 4.0]
C1_armB_wall_S:    [-18.0, -3.2, 0.0] -> [-5.0, -3.0, 4.0]
```

**Arm B walls: 2 elements**

### C.2 Arm B Floor Slab

Layer: `Type_07_GapRelay::Volumes`
```
C2_armB_floor:     [-18.0, -3.2, -0.25] -> [-5.0, 3.2, 0.0]
```

**Arm B floor: 1 element**

### C.3 Arm B Roof Slab

Layer: `Type_07_GapRelay::L300_Roof`
```
C3_armB_roof:      [-18.0, -3.2, 4.0] -> [-5.0, 3.2, 4.25]
```

**Arm B roof: 1 element**

### C.4 Arm B Columns (2 at midpoint)

Layer: `Type_07_GapRelay::Structure`

Steel columns at X=-11.5:
```
C4_col_armB_N:     [-11.6,  2.9, 0.0] -> [-11.4,  3.1, 4.0]
C4_col_armB_S:     [-11.6, -3.1, 0.0] -> [-11.4, -2.9, 4.0]
```

**Arm B columns: 2 elements**

### C.5 Arm B Edge Beam

Layer: `Type_07_GapRelay::Structure`
```
C5_beam_armB_junction: [-5.3, -3.0, 3.6] -> [-5.0, 3.0, 4.0]
```

**Arm B beam: 1 element**

---

## SECTION D — ARM C: UPHILL/FUNICULAR (Northeast)

### D.1 Arm C Walls

Layer: `Type_07_GapRelay::Volumes`

Arm: X=[5, 16], Y=[5, 16], Z=[0, 5]. Angled at 45deg. Wall thickness: 0.20m.
Two parallel walls along the diagonal. NE face: OPEN.

Modeled as box_pts (8 explicit corners for diagonal geometry):
```
D1_armC_wall_NW: diagonal wall along NW edge of arm corridor
  Bottom: (3.86, 6.54, 0) -> (12.73, 15.41, 0), 0.20m offset NW, H=5.0
D1_armC_wall_SE: diagonal wall along SE edge of arm corridor
  Bottom: (6.54, 3.86, 0) -> (15.41, 12.73, 0), 0.20m offset SE, H=5.0
```

**Arm C walls: 2 elements** (box_pts for diagonal)

### D.2 Arm C Floor (ramped)

Layer: `Type_07_GapRelay::Volumes`

Floor ramps from Z=0 at hub junction to Z=1.5 at far end. Slab: 0.25m thick.
Modeled as box_pts with explicit Z corners:
```
D2_armC_floor: 8-corner wedge
  Hub end: Z_top=0.0, Z_bot=-0.25
  Far end: Z_top=1.5, Z_bot=1.25
  Width: 6m along diagonal (~4.24m in X and Y each)
```

**Arm C floor: 1 element**

### D.3 Arm C Roof Slab

Layer: `Type_07_GapRelay::L300_Roof`

Follows arm slope. 0.25m thick:
```
D3_armC_roof: 8-corner box_pts
  Hub end: Z_top=5.25, Z_bot=5.0
  Far end: Z_top=5.25, Z_bot=5.0 (flat roof, arm walls step up)
```

**Arm C roof: 1 element**

### D.4 Arm C Columns (2 at midpoint)

Layer: `Type_07_GapRelay::Structure`

Steel columns at midpoint of diagonal arm:
```
D4_col_armC_NW:    [ 8.15,  9.85, 0.0] -> [ 8.35, 10.05, 5.0]
D4_col_armC_SE:    [ 9.85,  8.15, 0.0] -> [10.05,  8.35, 5.0]
```

**Arm C columns: 2 elements**

---

## SECTION E — CANOPIES (3 at arm tips)

Layer: `Type_07_GapRelay::L300_Roof` (slabs) + `Type_07_GapRelay::Structure` (columns)

### E.1 Canopy A (Arm A south tip)

Steel plate roof 0.01m thick:
```
E1_canopyA_roof:   [-4.0, -20.0, 4.0] -> [ 4.0, -18.0, 4.01]
```

4 thin steel columns (0.15m x 0.15m):
```
E1_canopyA_col_SW: [-3.925, -19.925, 0.0] -> [-3.775, -19.775, 4.0]
E1_canopyA_col_SE: [ 3.775, -19.925, 0.0] -> [ 3.925, -19.775, 4.0]
E1_canopyA_col_NW: [-3.925, -18.075, 0.0] -> [-3.775, -17.925, 4.0]
E1_canopyA_col_NE: [ 3.775, -18.075, 0.0] -> [ 3.925, -17.925, 4.0]
```

**Canopy A: 5 elements**

### E.2 Canopy B (Arm B west tip)

```
E2_canopyB_roof:   [-20.0, -4.0, 4.0] -> [-18.0,  4.0, 4.01]
```

4 columns:
```
E2_canopyB_col_SW: [-19.925, -3.925, 0.0] -> [-19.775, -3.775, 4.0]
E2_canopyB_col_NW: [-19.925,  3.775, 0.0] -> [-19.775,  3.925, 4.0]
E2_canopyB_col_SE: [-18.075, -3.925, 0.0] -> [-17.925, -3.775, 4.0]
E2_canopyB_col_NE: [-18.075,  3.775, 0.0] -> [-17.925,  3.925, 4.0]
```

**Canopy B: 5 elements**

### E.3 Canopy C (Arm C northeast tip)

Positioned at arm terminus, 4m x 4m at Z=4.5–5.5:
```
E3_canopyC_roof:   [14.0, 14.0, 5.5] -> [18.0, 18.0, 5.51]
```

4 columns:
```
E3_canopyC_col_SW: [14.075, 14.075, 0.0] -> [14.225, 14.225, 5.5]
E3_canopyC_col_NW: [14.075, 17.775, 0.0] -> [14.225, 17.925, 5.5]
E3_canopyC_col_SE: [17.775, 14.075, 0.0] -> [17.925, 14.225, 5.5]
E3_canopyC_col_NE: [17.775, 17.775, 0.0] -> [17.925, 17.925, 5.5]
```

**Canopy C: 5 elements**

---

## SECTION F — FOUNDATIONS

Layer: `Type_07_GapRelay::Structure`

### F.1 Hub Pad Footings (8, under hub columns)

1.0m x 1.0m x 0.40m pads centered on each hub column, top at Z=-0.30 (under slab):
```
F1_footing_hub_N:   [-0.5,  4.5, -0.70] -> [ 0.5,  5.5, -0.30]
F1_footing_hub_S:   [-0.5, -5.5, -0.70] -> [ 0.5, -4.5, -0.30]
F1_footing_hub_E:   [ 4.5, -0.5, -0.70] -> [ 5.5,  0.5, -0.30]
F1_footing_hub_W:   [-5.5, -0.5, -0.70] -> [-4.5,  0.5, -0.30]
F1_footing_hub_NW:  [-4.03, 3.03, -0.70] -> [-3.03, 4.03, -0.30]
F1_footing_hub_NE:  [ 3.03, 3.03, -0.70] -> [ 4.03, 4.03, -0.30]
F1_footing_hub_SW:  [-4.03,-4.03, -0.70] -> [-3.03,-3.03, -0.30]
F1_footing_hub_SE:  [ 3.03,-4.03, -0.70] -> [ 4.03,-3.03, -0.30]
```

### F.2 Arm Pad Footings (6, under arm columns)

0.60m x 0.60m x 0.40m:
```
F2_footing_armA_E:  [ 2.6, -11.8, -0.65] -> [ 3.4, -11.2, -0.25]
F2_footing_armA_W:  [-3.4, -11.8, -0.65] -> [-2.6, -11.2, -0.25]
F2_footing_armB_N:  [-11.8,  2.6, -0.65] -> [-11.2,  3.4, -0.25]
F2_footing_armB_S:  [-11.8, -3.4, -0.65] -> [-11.2, -2.6, -0.25]
F2_footing_armC_NW: [ 7.85,  9.55, -0.65] -> [ 8.65, 10.35, -0.25]
F2_footing_armC_SE: [ 9.55,  7.85, -0.65] -> [10.35,  8.65, -0.25]
```

**Foundations: 14 elements**

---

## SECTION G — OPENINGS

Layer: `Type_07_GapRelay::Openings`

### G.1 SE Window (hub east wall)

Single window in SE hub face: X=5.0, Y=[-3, -1], Z=[2, 5]:
Frame (0.05m aluminum):
```
G1_window_SE_frame_L: [5.3, -3.05, 2.0] -> [5.35, -2.95, 5.0]
G1_window_SE_frame_R: [5.3, -1.05, 2.0] -> [5.35, -0.95, 5.0]
G1_window_SE_frame_T: [5.3, -3.05, 4.95] -> [5.35, -0.95, 5.0]
G1_window_SE_frame_B: [5.3, -3.05, 2.0] -> [5.35, -0.95, 2.05]
```

Glass pane (0.04m IGU):
```
G1_window_SE_glass:   [5.26, -2.95, 2.05] -> [5.30, -1.05, 4.95]
```

**SE window: 5 elements**

### G.2 Arm A Open End Mullions

South face of Arm A (Y=-18, X=[-3, 3], Z=[0, 3.5]). Mullion grid at 1.5m spacing:
```
G2_mullion_armA_1: [-1.525, -18.05, 0.0] -> [-1.475, -18.0, 3.5]
G2_mullion_armA_2: [ 0.025, -18.05, 0.0] -> [-0.025, -18.0, 3.5]
G2_mullion_armA_3: [ 1.475, -18.05, 0.0] -> [ 1.525, -18.0, 3.5]
G2_mullion_armA_T: [-3.0, -18.05, 3.45] -> [ 3.0, -18.0, 3.5]
```

**Arm A mullions: 4 elements**

### G.3 Arm B Open End Mullions

West face of Arm B (X=-18, Y=[-3, 3], Z=[0, 3.5]):
```
G3_mullion_armB_1: [-18.05, -1.525, 0.0] -> [-18.0, -1.475, 3.5]
G3_mullion_armB_2: [-18.05, -0.025, 0.0] -> [-18.0,  0.025, 3.5]
G3_mullion_armB_3: [-18.05,  1.475, 0.0] -> [-18.0,  1.525, 3.5]
G3_mullion_armB_T: [-18.05, -3.0, 3.45] -> [-18.0,  3.0, 3.5]
```

**Arm B mullions: 4 elements**

---

## SECTION H — CIRCULATION

Layer: `Type_07_GapRelay::Circulation`

### H.1 Through-Flow Paths (polylines at Z=0.1)

4 circulation paths converging at hub center:
```
H1_path_ArmA_through: polyline Y=[-18, 0], X=0, Z=0.1 (straight through)
H1_path_ArmB_transfer: polyline from (0,-18,0.1) -> (0,0,0.1) -> (-18,0,0.1) (L-shaped)
H1_path_ArmC_diagonal: polyline from (0,0,0.1) -> (16,16,1.6) (diagonal with ramp)
H1_path_BC_transfer: polyline from (-18,0,0.1) -> (0,0,0.1) -> (16,16,1.6)
```

**Paths: 4 elements**

### H.2 Hub Turntable Circle

Circle at hub center, radius 2m, Z=0.1:
```
H2_turntable: circle center (0,0,0.1), radius 2.0
```

**Turntable: 1 element**

### H.3 Arm C Ramp Railings

Ramp in Arm C: 1.5m wide, 6% grade, with railings on both sides.
Ramp run: ~25m diagonal (1.5m rise / 0.06 = 25m).
Railing height: 1.10m, posts at 1.50m spacing.

NW side railing (17 posts + top rail):
```
H3_railing_armC_NW_rail: pipe along NW wall, 0.044m diameter, at 1.1m above ramp
H3_railing_armC_NW_posts: 17 posts at 1.5m spacing, 0.044m diameter, 1.1m tall
```

SE side railing (same):
```
H3_railing_armC_SE_rail: pipe along SE wall
H3_railing_armC_SE_posts: 17 posts
```

**Arm C railings: 36 elements** (2 rails + 34 posts)

### H.4 Ramp Landing

Landing at midpoint of Arm C ramp (after 6m run), 1.5m x 1.5m flat:
```
H4_landing_armC: flat slab at ramp midpoint, 0.25m thick
```

**Landing: 1 element**

---

## SECTION I — PARAPETS

Layer: `Type_07_GapRelay::L350_Detail`

### I.1 Hub Roof Parapets

1.07m above finished roof (Z=7.524 to Z=8.594). 0.15m thick:
```
I1_parapet_N:      [-5.45,  5.15, 7.524] -> [ 5.45,  5.45, 8.594]
I1_parapet_S:      [-5.45, -5.45, 7.524] -> [ 5.45, -5.15, 8.594]
I1_parapet_E:      [ 5.15, -5.45, 7.524] -> [ 5.45,  5.45, 8.594]
I1_parapet_W:      [-5.45, -5.45, 7.524] -> [-5.15,  5.45, 8.594]
```

**Parapets: 4 elements**

---

## SECTION J — LOG400 MATERIAL DETAILS

Layer: `Type_07_GapRelay::L400_Material`

### J.1 Formwork Lines on Hub Walls (2.4m lifts)

Horizontal lines at Z=2.4 and Z=4.8 on all hub walls:
```
J1_formwork_Z2.4: 8 lines (one per wall segment) at Z=2.4
J1_formwork_Z4.8: 8 lines at Z=4.8
```

**Formwork lines: 16 elements**

### J.2 Expansion Joints on Arm Floors

Every 6m on arm floors. Arm A (13m long): joints at Y=-11, Y=-17:
```
J2_joint_armA_1: line X=[-3, 3], Y=-11, Z=0.01
J2_joint_armA_2: line X=[-3, 3], Y=-17, Z=0.01
```

Arm B (13m long): joints at X=-11, X=-17:
```
J2_joint_armB_1: line Y=[-3, 3], X=-11, Z=0.01
J2_joint_armB_2: line Y=[-3, 3], X=-17, Z=0.01
```

**Expansion joints: 4 elements**

### J.3 Column Base Plates (at all steel columns)

Steel base plates at arm + canopy columns (6 arm + 12 canopy = 18):
0.35m x 0.35m x 0.02m plates at Z=0:
```
J3_baseplate_[location]: 18 elements
```

**Base plates: 18 elements**

### J.4 DPC (Damp Proof Course)

2mm DPC at base of all walls at Z=0.15 (150mm above floor):
```
J4_dpc_hub: thin slab under hub walls at Z=0.148-0.150
J4_dpc_armA: under arm A walls
J4_dpc_armB: under arm B walls
J4_dpc_armC: under arm C walls
```

**DPC: 4 elements**

---

## SECTION K — ANNOTATIONS

Layer: `Type_07_GapRelay::Annotations`

```
K1: TextDot "RELAY HUB / JUNCTION" at (0, 0, 3.5)
K2: TextDot "RAIL CORRIDOR ->" at (0, -12, 2.0)
K3: TextDot "LATERAL CONNECTION ->" at (-12, 0, 2.0)
K4: TextDot "UPHILL / FUNICULAR ->" at (10, 10, 3.0)
K5: TextDot "OPEN TO SKY" at (0, 0, 7.5)
K6: TextDot "CANOPY A" at (0, -19, 3.5)
K7: TextDot "CANOPY B" at (-19, 0, 3.5)
K8: TextDot "CANOPY C" at (16, 16, 5.0)
```

**Annotations: 8 elements**

---

## BILL OF OBJECTS SUMMARY

| Section | Element group | Count |
|---------|--------------|-------|
| A | Hub walls | 8 |
| A | Hub floor | 1 |
| A | Hub columns | 8 |
| A | Hub beams | 8 |
| A | Hub roof slabs | 4 |
| A | Skylight frame | 4 |
| A | Roof assembly (LOG400) | 5 |
| B | Arm A walls | 2 |
| B | Arm A floor | 1 |
| B | Arm A roof | 1 |
| B | Arm A columns | 2 |
| B | Arm A beam | 1 |
| C | Arm B walls | 2 |
| C | Arm B floor | 1 |
| C | Arm B roof | 1 |
| C | Arm B columns | 2 |
| C | Arm B beam | 1 |
| D | Arm C walls | 2 |
| D | Arm C floor | 1 |
| D | Arm C roof | 1 |
| D | Arm C columns | 2 |
| E | Canopy A | 5 |
| E | Canopy B | 5 |
| E | Canopy C | 5 |
| F | Foundations | 14 |
| G | SE window | 5 |
| G | Arm A mullions | 4 |
| G | Arm B mullions | 4 |
| H | Circulation paths | 4 |
| H | Turntable | 1 |
| H | Arm C railings | 36 |
| H | Ramp landing | 1 |
| I | Parapets | 4 |
| J | Formwork lines | 16 |
| J | Expansion joints | 4 |
| J | Base plates | 18 |
| J | DPC layers | 4 |
| K | Annotations | 8 |
| **TOTAL** | | **196** |

---

## TEAM ASSIGNMENT (Agent Team)

### Lead (coordinator — does NOT build)
- Owns coordination log
- Runs health checks after Phase 1 and Phase 2
- Resolves disputes per authority hierarchy

### Structure Agent
- Sections: A.3 (columns), A.4 (beams), B.4-B.5, C.4-C.5, D.4, E (canopy columns), F (foundations), J.3 (base plates)
- Elements: 8+8+2+1+2+1+2+12+14+18 = **68 elements**

### Shell Agent
- Sections: A.1 (hub walls), A.2 (floor), B.1-B.2, C.1-C.2, D.1-D.2, I (parapets), J.4 (DPC)
- Elements: 8+1+2+1+2+1+2+1+4+4 = **26 elements**

### Roof Agent
- Sections: A.5 (hub roof), A.6 (skylight), A.7 (roof assembly), B.3, C.3, D.3, E (canopy roofs), J.1 (formwork)
- Elements: 4+4+5+1+1+1+3+16 = **35 elements**

### Detail Agent
- Sections: G (openings), H (circulation), J.2 (expansion joints), K (annotations)
- Elements: 5+4+4+4+1+36+1+4+8 = **67 elements**

**Total: 196 elements across 4 agents + 1 lead**

---

## INTERFACE REGISTRY

| Interface | Owner | Reference | Rule |
|-----------|-------|-----------|------|
| Hub wall base -> hub slab | Shell | Structure (slab) | Walls start at Z=0.0, slab top at Z=0.0 |
| Arm wall base -> arm slab | Shell | Structure (slab) | Walls start at Z=0.0, slab top at Z=0.0 |
| Column -> footing | Structure | Structure | Footing centered on column, 3x width |
| Hub roof slab -> hub walls | Roof | Shell (wall tops) | Roof slab at Z=7.0, walls to Z=7.0 |
| Arm roof slab -> arm walls | Roof | Shell (wall tops) | Roof at Z=4.0, walls to Z=4.0 |
| Canopy roof -> canopy columns | Roof | Structure | Canopy at Z=4.0 (A,B) or Z=5.5 (C) |
| Window frame -> hub wall | Detail | Shell (wall void) | Frame at wall outer face, glass recessed 0.08m |
| Railing -> ramp edge | Detail | Shell (arm walls) | Railing along inner face of arm walls |
| Parapet -> roof edge | Shell | Roof (slab edge) | Parapet starts at finished roof level |
| Roof assembly -> roof slab | Roof | Roof | Assembly layers stack on slab top face |
| Base plate -> column base | Structure | Structure | Plate centered on column at Z=0 |
| Skylight -> roof slab | Roof | Roof | Skylight frame within roof void opening |

---

## HEALTH CHECK THRESHOLDS

| Agent | Expected | Min (85%) | Critical (<50%) |
|-------|----------|-----------|-----------------|
| Structure | 68 | 58 | 34 |
| Shell | 26 | 22 | 13 |
| Roof | 35 | 30 | 18 |
| Detail | 67 | 57 | 34 |
| **Total** | **196** | **167** | **98** |
