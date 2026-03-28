# Lock Type 06 — GRADIENT DISPATCHER
# LOG400 Complete Building Spec
# Status: ACTIVE BUILD
# Date: 2026-03-27

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry authored in METER-SCALE values.
"12.0" in Rhino = 12.0 as a number, displayed as "12 cm" but conceptually 12m.

**ALL coordinates in this spec are meter-scale. Use them exactly as written.**
**Do NOT multiply by 100. Do NOT convert.**

X = lateral axis (building width)
Y = slope axis (building steps uphill as Y increases)
Z = vertical (0 = Dispatcher Lobby finished floor level)

**Key gradient:** The building steps up a hillside. Each terrace is at a higher Z.
- Lobby: Z = 0
- Level 1 (Staff): Z = 4
- Level 2 (Patients): Z = 8
- Level 3 (Cargo): Z = 12

---

## CONCEPT SUMMARY

A building that sorts multiple flows across a slope. The LOBBY at the base does the sorting — intelligence is at entry. Four dispatch lanes sort staff, patients, cargo, and emergency flows to their correct elevation via ramps and a vertical core. The building steps uphill visibly — the gradient IS the architecture.

**State transition:** Horizontal flow (arriving) -> Gradient flow (dispatched to correct level)

---

## RHINO TARGET

Instance: port 9001 (target: `"structure"`)
All MCP tool calls must include `target: "structure"`

---

## ARCHIBASE-GROUNDED DIMENSIONS

Source: `H:/Shared drives/City 101/archibase/source/knowledge/`

### Wall Assembly (Concrete + ETICS, from wall_systems.md)
| Layer | Thickness | Material |
|-------|-----------|----------|
| Exterior render | 0.010m | Mineral render |
| Insulation (EPS) | 0.160m | Expanded polystyrene |
| RC structure | 0.200m | C30/37 reinforced concrete |
| Interior plaster | 0.015m | Gypsum plaster |
| **TOTAL** | **0.385m** | |

For modeling: use WALL_T = 0.30m for the RC structural wall. Insulation + render modeled as a 0.17m outer layer on exposed faces.

### Floor Assembly (RC slab, from floor_systems.md)
| Layer | Thickness |
|-------|-----------|
| Floor finish (screed) | 0.050m |
| RC structural slab | 0.250m |
| **TOTAL** | **0.300m** |

SLAB_T = 0.30m total. Top surface = finished floor level.

### Structural Elements (from structural_grids.md, concrete_systems.md)
| Element | Dimension | Notes |
|---------|-----------|-------|
| Columns | 0.40m x 0.40m | C30/37, centered on grid |
| Primary beams | 0.40m wide x 0.60m deep | Span up to 8m |
| Secondary beams | 0.30m wide x 0.45m deep | Span up to 6m |
| Core walls | 0.25m thick | RC shear walls |

### Ramps (SIA 500 — accessibility_sia500.md)
| Parameter | Value | Standard |
|-----------|-------|----------|
| Max gradient | 6% (1:17) | SIA 500 |
| Min width | 1.50m | SIA 500 (preferred) |
| Landing every | 6.0m of run | SIA 500 |
| Landing depth | 1.50m | SIA 500 |
| Handrail height | 0.90m | SIA 500 |
| Handrail diameter | 0.044m | SIA 500 |
| Handrail extension | 0.30m beyond ramp | SIA 500 |
| Cross-slope | max 2% | SIA 500 |

### Safety (SIA 358, Swiss building code)
| Element | Value |
|---------|-------|
| Parapet / guardrail height | 1.07m |
| Railings required | Both sides, edges > 1.0m drop |
| Kick plate height | 0.10m |

### Roof
| Layer | Thickness |
|-------|-----------|
| Gravel ballast | 0.060m |
| Waterproof membrane | 0.010m |
| Insulation | 0.160m |
| Vapour barrier | 0.005m |
| RC slab | 0.250m |
| **TOTAL** | **0.485m** |

ROOF_T = 0.50m (rounded). Parapet rises 1.07m above roof surface.

---

## LAYERS TO CREATE

### Base layers
```
Type_06_Gradient::Structure::Columns    — RGB(110, 85, 180)
Type_06_Gradient::Structure::Beams      — RGB(110, 85, 180)
Type_06_Gradient::Structure::Slabs      — RGB(100, 75, 170)
Type_06_Gradient::Structure::CoreWalls  — RGB(120, 95, 190)
Type_06_Gradient::Envelope::Walls       — RGB(151, 117, 250)
Type_06_Gradient::Envelope::Insulation  — RGB(170, 145, 250)
Type_06_Gradient::Envelope::Roof        — RGB(140, 110, 220)
Type_06_Gradient::Envelope::Parapets    — RGB(130, 100, 210)
Type_06_Gradient::Circulation::Ramps    — RGB(190, 170, 252)
Type_06_Gradient::Circulation::Railings — RGB(200, 180, 255)
Type_06_Gradient::Circulation::Paths    — RGB(180, 160, 240)
Type_06_Gradient::Openings::Frames      — RGB(170, 145, 250)
Type_06_Gradient::Openings::Glass       — RGB(200, 200, 255)
Type_06_Gradient::Annotations           — RGB(210, 200, 252)
Type_06_Gradient::TerrainProxy          — RGB(120, 100, 160)
Type_06_Gradient::Ground::Foundation    — RGB(90, 70, 140)
```

---

## BILL OF OBJECTS

### Phase 1 — Structure (builds first, blocks everything)

| ID | Element | Layer | Dimensions | Count |
|----|---------|-------|------------|-------|
| S01-S06 | Lobby columns | Structure::Columns | 0.40x0.40, Z=[0, 5] | 6 |
| S07-S10 | L1 columns | Structure::Columns | 0.40x0.40, Z=[4, 8] | 4 |
| S11-S14 | L2 columns | Structure::Columns | 0.40x0.40, Z=[8, 12] | 4 |
| S15-S17 | L3 columns | Structure::Columns | 0.40x0.40, Z=[12, 16] | 3 |
| S18-S21 | Core columns | Structure::Columns | 0.40x0.40, Z=[0, 18] | 4 |
| S22 | Lobby floor slab | Structure::Slabs | 24x10, Z=[-0.30, 0] | 1 |
| S23 | L1 floor slab | Structure::Slabs | 12x10, Z=[3.70, 4.0] | 1 |
| S24 | L2 floor slab | Structure::Slabs | 12x10, Z=[7.70, 8.0] | 1 |
| S25 | L3 floor slab | Structure::Slabs | 8x10, Z=[11.70, 12.0] | 1 |
| S26 | Lobby roof slab | Structure::Slabs | 24x10, Z=[5.0, 5.30] | 1 |
| S27-S28 | Primary beams lobby | Structure::Beams | 0.40x0.60 | 2 |
| S29-S34 | Terrace edge beams | Structure::Beams | 0.40x0.60 | 6 |
| S35-S38 | Core walls (4 sides) | Structure::CoreWalls | 0.25 thick, 4x4, Z=[0,18] | 4 |
| **TOTAL** | | | | **~40** |

### Phase 1b — Envelope (after structure publishes grid)

| ID | Element | Layer | Count |
|----|---------|-------|-------|
| E01-E04 | Lobby walls (N,S,W,E) | Envelope::Walls | 4 |
| E05-E07 | L1 walls (N,S,W) | Envelope::Walls | 3 |
| E08-E10 | L2 walls (N,S,W) | Envelope::Walls | 3 |
| E11-E14 | L3 walls (N,S,W,E-cargo door) | Envelope::Walls | 4 |
| E15-E18 | Insulation panels (lobby exposed faces) | Envelope::Insulation | 4 |
| E19-E24 | Insulation panels (L1-L3 exposed faces) | Envelope::Insulation | 6 |
| E25-E28 | Roof slabs (lobby, L1, L2, L3) | Envelope::Roof | 4 |
| E29-E36 | Parapets (each roof edge) | Envelope::Parapets | 8 |
| E37 | Terrain proxy slope | TerrainProxy | 1 |
| E38-E39 | Foundation strips | Ground::Foundation | 2 |
| **TOTAL** | | | **~40** |

### Phase 2 — Detail (after Phase 1 freeze + health check)

| ID | Element | Layer | Count |
|----|---------|-------|-------|
| D01 | Ramp to L1 (inclined slab) | Circulation::Ramps | 1 |
| D02 | Ramp to L2 (inclined slab) | Circulation::Ramps | 1 |
| D03 | Ramp to L3 (service ramp) | Circulation::Ramps | 1 |
| D04-D06 | Ramp landings (3 per ramp ~9 total) | Circulation::Ramps | 9 |
| D07-D12 | Handrails (2 per ramp, pipes) | Circulation::Railings | 6 |
| D13-D16 | Dispatch lane dividers (lobby) | Circulation::Paths | 4 |
| D17-D20 | Circulation path polylines (4 flows) | Circulation::Paths | 4 |
| D21 | Emergency vertical path | Circulation::Paths | 1 |
| D22 | Lobby south entry frame | Openings::Frames | 1 |
| D23 | L1 west window frame | Openings::Frames | 1 |
| D24 | L2 west window frame | Openings::Frames | 1 |
| D25 | L3 north cargo door frame | Openings::Frames | 1 |
| D26-D29 | Glass panes (4 openings) | Openings::Glass | 4 |
| D30-D33 | Core top lattice (4 open faces) | Openings::Frames | 4 |
| D34-D42 | Text dot annotations (9) | Annotations | 9 |
| **TOTAL** | | | **~48** |

**Grand total target: ~128 objects**

---

## SECTION A — STRUCTURE (Phase 1)

### A1. Lobby Columns (6)
Layer: `Type_06_Gradient::Structure::Columns`
Section: 0.40m x 0.40m, centered on grid position.

| ID | Name | Center X | Center Y | Z_base | Z_top |
|----|------|----------|----------|--------|-------|
| S01 | Col_Lobby_NW | -7.0 | 2.0 | 0 | 5.0 |
| S02 | Col_Lobby_NE | -1.0 | 2.0 | 0 | 5.0 |
| S03 | Col_Lobby_CE | 5.0 | 2.0 | 0 | 5.0 |
| S04 | Col_Lobby_SW | -7.0 | -2.0 | 0 | 5.0 |
| S05 | Col_Lobby_SE | -1.0 | -2.0 | 0 | 5.0 |
| S06 | Col_Lobby_CS | 5.0 | -2.0 | 0 | 5.0 |

Geometry (centered +-0.20):
```
Col_Lobby_NW: [-7.20, 1.80, 0] -> [-6.80, 2.20, 5.0]
Col_Lobby_NE: [-1.20, 1.80, 0] -> [-0.80, 2.20, 5.0]
Col_Lobby_CE: [4.80, 1.80, 0] -> [5.20, 2.20, 5.0]
Col_Lobby_SW: [-7.20, -2.20, 0] -> [-6.80, -1.80, 5.0]
Col_Lobby_SE: [-1.20, -2.20, 0] -> [-0.80, -1.80, 5.0]
Col_Lobby_CS: [4.80, -2.20, 0] -> [5.20, -1.80, 5.0]
```

### A2. L1 Perimeter Columns (4)
Layer: `Type_06_Gradient::Structure::Columns`

| ID | Name | Center X | Center Y | Z_base | Z_top |
|----|------|----------|----------|--------|-------|
| S07 | Col_L1_NW | -12.0 | 14.8 | 4.0 | 8.0 |
| S08 | Col_L1_NE | 0.0 | 14.8 | 4.0 | 8.0 |
| S09 | Col_L1_SW | -12.0 | 5.2 | 4.0 | 8.0 |
| S10 | Col_L1_SE | 0.0 | 5.2 | 4.0 | 8.0 |

### A3. L2 Perimeter Columns (4)

| ID | Name | Center X | Center Y | Z_base | Z_top |
|----|------|----------|----------|--------|-------|
| S11 | Col_L2_NW | -12.0 | 24.8 | 8.0 | 12.0 |
| S12 | Col_L2_NE | 0.0 | 24.8 | 8.0 | 12.0 |
| S13 | Col_L2_SW | -12.0 | 15.2 | 8.0 | 12.0 |
| S14 | Col_L2_SE | 0.0 | 15.2 | 8.0 | 12.0 |

### A4. L3 Perimeter Columns (3)

| ID | Name | Center X | Center Y | Z_base | Z_top |
|----|------|----------|----------|--------|-------|
| S15 | Col_L3_NW | -12.0 | 34.8 | 12.0 | 16.0 |
| S16 | Col_L3_NE | -4.0 | 34.8 | 12.0 | 16.0 |
| S17 | Col_L3_SW | -12.0 | 25.2 | 12.0 | 16.0 |

### A5. Vertical Core Columns (4)
Full height tower, east side of building.

| ID | Name | Center X | Center Y | Z_base | Z_top |
|----|------|----------|----------|--------|-------|
| S18 | Col_Core_NW | 8.0 | 9.0 | 0 | 18.0 |
| S19 | Col_Core_NE | 12.0 | 9.0 | 0 | 18.0 |
| S20 | Col_Core_SW | 8.0 | 5.0 | 0 | 18.0 |
| S21 | Col_Core_SE | 12.0 | 5.0 | 0 | 18.0 |

### A6. Floor Slabs

Layer: `Type_06_Gradient::Structure::Slabs`
All 0.30m thick. Top surface = finished floor level.

```
S22_Lobby_floor:  [-12.0, -5.0, -0.30] -> [12.0, 5.0, 0.0]
S23_L1_floor:     [-12.0, 5.0, 3.70]   -> [0.0, 15.0, 4.0]
S24_L2_floor:     [-12.0, 15.0, 7.70]  -> [0.0, 25.0, 8.0]
S25_L3_floor:     [-12.0, 25.0, 11.70] -> [-4.0, 35.0, 12.0]
S26_Lobby_roof:   [-12.0, -5.0, 5.0]   -> [12.0, 5.0, 5.30]
```

### A7. Primary Beams

Layer: `Type_06_Gradient::Structure::Beams`
0.40m wide x 0.60m deep.

**Lobby span beams (Y-direction, at column lines):**
```
S27_Beam_Lobby_W:   [-7.20, -5.0, 4.40] -> [-6.80, 5.0, 5.0]
S28_Beam_Lobby_E:   [-1.20, -5.0, 4.40] -> [-0.80, 5.0, 5.0]
```

**Terrace edge beams (X-direction, at terrace front edges):**
```
S29_Beam_L1_front:  [-12.0, 5.0, 3.40]  -> [0.0, 5.40, 4.0]
S30_Beam_L1_back:   [-12.0, 14.60, 3.40] -> [0.0, 15.0, 4.0]
S31_Beam_L2_front:  [-12.0, 15.0, 7.40] -> [0.0, 15.40, 8.0]
S32_Beam_L2_back:   [-12.0, 24.60, 7.40] -> [0.0, 25.0, 8.0]
S33_Beam_L3_front:  [-12.0, 25.0, 11.40] -> [-4.0, 25.40, 12.0]
S34_Beam_L3_back:   [-12.0, 34.60, 11.40] -> [-4.0, 35.0, 12.0]
```

### A8. Core Walls (4 sides)

Layer: `Type_06_Gradient::Structure::CoreWalls`
0.25m thick RC shear walls, full height Z=[0, 18].

```
S35_Core_wall_N:  [8.0, 8.75, 0]  -> [12.0, 9.0, 18.0]
S36_Core_wall_S:  [8.0, 5.0, 0]   -> [12.0, 5.25, 18.0]
S37_Core_wall_W:  [8.0, 5.0, 0]   -> [8.25, 9.0, 18.0]
S38_Core_wall_E:  [11.75, 5.0, 0] -> [12.0, 9.0, 18.0]
```

---

## SECTION B — ENVELOPE (Phase 1b)

### B1. Lobby Walls
Layer: `Type_06_Gradient::Envelope::Walls`
RC structural wall = 0.30m thick. Inner face at volume boundary.

```
E01_Lobby_wall_N:  [-12.0, 5.0, 0]   -> [12.0, 5.30, 5.0]
E02_Lobby_wall_S:  [-12.0, -5.30, 0] -> [12.0, -5.0, 5.0]
E03_Lobby_wall_W:  [-12.30, -5.30, 0] -> [-12.0, 5.30, 5.0]
E04_Lobby_wall_E:  [12.0, -5.30, 0]  -> [12.30, 5.30, 5.0]
```

Note: Lobby south face (Y=-5) has large entry opening — wall is split around it (see Section D openings). Model full wall first, opening frame overlays.

### B2. Level 1 Walls (Staff)
```
E05_L1_wall_N:  [-12.0, 14.70, 4.0] -> [0.0, 15.0, 8.0]
E06_L1_wall_S:  [-12.0, 5.0, 4.0]   -> [0.0, 5.30, 8.0]
E07_L1_wall_W:  [-12.30, 5.0, 4.0]  -> [-12.0, 15.0, 8.0]
```
L1 east side open (connects to ramp / circulation zone).

### B3. Level 2 Walls (Patients)
```
E08_L2_wall_N:  [-12.0, 24.70, 8.0] -> [0.0, 25.0, 12.0]
E09_L2_wall_S:  [-12.0, 15.0, 8.0]  -> [0.0, 15.30, 12.0]
E10_L2_wall_W:  [-12.30, 15.0, 8.0] -> [-12.0, 25.0, 12.0]
```

### B4. Level 3 Walls (Cargo)
```
E11_L3_wall_N:  [-12.0, 34.70, 12.0] -> [-4.0, 35.0, 16.0]
E12_L3_wall_S:  [-12.0, 25.0, 12.0]  -> [-4.0, 25.30, 16.0]
E13_L3_wall_W:  [-12.30, 25.0, 12.0] -> [-12.0, 35.0, 16.0]
E14_L3_wall_E:  [-4.30, 25.0, 12.0]  -> [-4.0, 35.0, 16.0]
```

### B5. Insulation Panels
Layer: `Type_06_Gradient::Envelope::Insulation`
0.17m thick (insulation 0.16 + render 0.01), applied to exterior face of walls.

Lobby exterior:
```
E15_Ins_Lobby_S:  [-12.0, -5.47, 0]  -> [12.0, -5.30, 5.0]
E16_Ins_Lobby_W:  [-12.47, -5.47, 0] -> [-12.30, 5.47, 5.0]
E17_Ins_Lobby_N:  [-12.0, 5.30, 0]   -> [12.0, 5.47, 5.0]
E18_Ins_Lobby_E:  [12.30, -5.47, 0]  -> [12.47, 5.47, 5.0]
```

L1-L3 insulation follows same logic (0.17m outboard of RC wall).

### B6. Roof Slabs
Layer: `Type_06_Gradient::Envelope::Roof`
0.50m thick roof assembly.

```
E25_Roof_Lobby: [-12.47, -5.47, 5.30] -> [12.47, 5.47, 5.80]
E26_Roof_L1:    [-12.47, 5.0, 8.0]    -> [0.17, 15.17, 8.50]
E27_Roof_L2:    [-12.47, 15.0, 12.0]  -> [0.17, 25.17, 12.50]
E28_Roof_L3:    [-12.47, 25.0, 16.0]  -> [-3.83, 35.17, 16.50]
```

### B7. Parapets
Layer: `Type_06_Gradient::Envelope::Parapets`
1.07m above roof surface, 0.15m thick.

Lobby roof parapets (4 edges):
```
E29_Parapet_Lobby_N: [-12.47, 5.32, 5.80] -> [12.47, 5.47, 6.87]
E30_Parapet_Lobby_S: [-12.47, -5.47, 5.80] -> [12.47, -5.32, 6.87]
E31_Parapet_Lobby_W: [-12.47, -5.47, 5.80] -> [-12.32, 5.47, 6.87]
E32_Parapet_Lobby_E: [12.32, -5.47, 5.80]  -> [12.47, 5.47, 6.87]
```

L1/L2/L3 parapets follow same pattern at respective roof Z levels.

### B8. Terrain Proxy
Layer: `Type_06_Gradient::TerrainProxy`
Thin wedge showing hillside grade.

8-point box_pts:
```
E37_Terrain: wedge from
  Y=-8, Z=-1 (south/downhill)
  to Y=38, Z=15 (north/uphill)
  X = [-15, 15]
  thickness = 0.15m
```

### B9. Foundation Strips
Layer: `Type_06_Gradient::Ground::Foundation`
0.50m wide x 0.40m deep, under lobby walls.

```
E38_Found_Lobby_N: [-12.47, 4.75, -0.70] -> [12.47, 5.25, -0.30]
E39_Found_Lobby_S: [-12.47, -5.25, -0.70] -> [12.47, -4.75, -0.30]
```

---

## SECTION C — CIRCULATION (Phase 2)

### C1. Ramp to L1 (Staff)
Layer: `Type_06_Gradient::Circulation::Ramps`
Rise = 4.0m. At 6% grade, run = 66.7m.
Simplified: 3 switchback runs of 22m each.
Width = 1.50m.

**Run 1:** X=[-10, -7.5], Y=[3, 13], Z rising from 0.15 to 1.48
**Landing 1:** X=[-10, -7.5], Y=[13, 14.5], Z=1.48, flat, 1.5m deep
**Run 2:** X=[-10, -7.5], Y=[14.5, 4.5] (returning), Z rising from 1.48 to 2.81
**Landing 2:** X=[-10, -7.5], Y=[3, 4.5], Z=2.81, flat
**Run 3:** X=[-10, -7.5], Y=[4.5, 14.5], Z rising from 2.81 to 4.0

Model as inclined slabs (0.15m thick wedges) with flat landing boxes.

### C2. Ramp to L2 (Patients)
Rise = 8.0m. At 6% grade, run = 133m.
Simplified: 6 switchback runs along east side.
X=[1, 4.5], Y=[3, 23]

Model as single inclined slab (simplified concept):
```
D02_Ramp_L2: inclined slab X=[1, 4.5], Y=[3, 23], Z=[0.15, 8.0], thickness=0.15
```

### C3. Service Ramp to L3 (Cargo)
Rise = 12.0m. Cargo grade allowed 10% = 120m run.
West exterior of building.
X=[-14, -12.5], Y=[5, 35]

```
D03_Ramp_L3: inclined slab X=[-14, -12.5], Y=[5, 35], Z=[0.15, 12.0], thickness=0.15
```

### C4. Handrails
Layer: `Type_06_Gradient::Circulation::Railings`
Pipe, diameter 0.044m, height 0.90m above ramp surface.
Both sides of each ramp. Extend 0.30m beyond top and bottom.

6 handrail pipes total (2 per ramp).

### C5. Dispatch Lane Dividers
Layer: `Type_06_Gradient::Circulation::Paths`
4 lanes in lobby, separated by 0.15m thick x 1.2m tall walls.

```
D13_Lane_div_1: [-7.0, -5.0, 0] -> [-6.85, 5.0, 1.2]   (between Lane 1-2)
D14_Lane_div_2: [-1.0, -5.0, 0] -> [-0.85, 5.0, 1.2]   (between Lane 2-3)
D15_Lane_div_3: [5.0, -5.0, 0]  -> [5.15, 5.0, 1.2]    (between Lane 3-4)
```

### C6. Circulation Path Polylines
4 polylines showing flow routes:
- Staff: Lobby Lane 1 -> Ramp -> L1
- Patients: Lobby Lane 2 -> Ramp -> L2
- Cargo: Lobby Lane 3 -> Ramp -> L3
- Emergency: Lobby Lane 4 -> Core -> vertical

### C7. Emergency Vertical Line
```
D21_Emergency_path: line from (10, 7, 0) to (10, 7, 18)
```

---

## SECTION D — OPENINGS (Phase 2)

### D1. Lobby South Entry
Layer: `Type_06_Gradient::Openings::Frames`
Full-width entry. Frame 0.05m thick.

```
D22_Lobby_entry_frame: [-10.0, -5.35, 0.15] -> [10.0, -5.30, 4.0]
```

Glass pane:
```
D26_Lobby_entry_glass: [-9.9, -5.33, 0.20] -> [9.9, -5.31, 3.9]
```

### D2. L1 West Window
```
D23_L1_window_frame: [-12.35, 7.0, 5.0] -> [-12.30, 13.0, 7.5]
D27_L1_window_glass: [-12.33, 7.1, 5.1]  -> [-12.31, 12.9, 7.4]
```

### D3. L2 West Window
```
D24_L2_window_frame: [-12.35, 17.0, 9.0] -> [-12.30, 23.0, 11.5]
D28_L2_window_glass: [-12.33, 17.1, 9.1]  -> [-12.31, 22.9, 11.4]
```

### D4. L3 North Cargo Door
```
D25_L3_cargo_frame: [-10.0, 34.95, 12.15] -> [-6.0, 35.0, 15.5]
D29_L3_cargo_glass: [-9.9, 34.97, 12.25]  -> [-6.1, 34.99, 15.4]
```

### D5. Core Top Lattice
4 open frame rectangles at Z=[16, 18]:
```
D30_Core_lattice_N: [8.0, 8.95, 16.0]  -> [12.0, 9.0, 18.0]
D31_Core_lattice_S: [8.0, 5.0, 16.0]   -> [12.0, 5.05, 18.0]
D32_Core_lattice_W: [8.0, 5.0, 16.0]   -> [8.05, 9.0, 18.0]
D33_Core_lattice_E: [11.95, 5.0, 16.0] -> [12.0, 9.0, 18.0]
```

---

## SECTION E — ANNOTATIONS (Phase 2)

Layer: `Type_06_Gradient::Annotations`
Text dots at key positions:

| ID | Position | Text |
|----|----------|------|
| D34 | (0, 0, 2.5) | DISPATCHER LOBBY / SORTING |
| D35 | (-9.5, 0, 0.5) | STAFF -> |
| D36 | (-3.5, 0, 0.5) | PATIENTS -> |
| D37 | (3.0, 0, 0.5) | CARGO -> |
| D38 | (9.5, 0, 0.5) | EMERGENCY ^ |
| D39 | (-6.0, 10.0, 6.0) | LEVEL 1 / STAFF |
| D40 | (-6.0, 20.0, 10.0) | LEVEL 2 / PATIENTS |
| D41 | (-8.0, 30.0, 14.0) | LEVEL 3 / CARGO |
| D42 | (10.0, 7.0, 19.0) | EMERGENCY CORE |

---

## SUCCESS CRITERIA

1. Building clearly steps up — 4 visible terraces at Z=0, 4, 8, 12
2. Lobby reads as wide sorting space with dispatch lane dividers
3. Each terrace is a distinct platform narrowing as it rises
4. Vertical core is an independent tower (Z=0-18) on east side
5. 3 ramps visible as separate inclined paths from lobby to each level
6. Wall assemblies show RC + insulation layers (not single boxes)
7. Floor slabs have proper 0.30m thickness
8. Parapets at 1.07m on all roof edges
9. Handrails on ramps at 0.90m
10. All objects named, layered, tagged with material
11. Section test: clipping plane reveals credible layer thicknesses
12. Someone sees: "this sorts multiple flows to different elevations on a hillside"

---

## INTERFACE REGISTRY

| Interface | Owner | Reference | Rule |
|-----------|-------|-----------|------|
| Wall base -> slab edge | Envelope | Structure | Flush interior face, wall sits on slab |
| Parapet -> roof slab | Envelope::Parapets | Envelope::Roof | Parapet base = roof slab top |
| Ramp -> slab | Circulation | Structure | Ramp start at slab top + 0.15m |
| Column -> slab | Structure::Columns | Structure::Slabs | Column bears on slab, passes through |
| Core wall -> slab | Structure::CoreWalls | Structure::Slabs | Core walls continuous, slabs frame into core |
| Insulation -> wall | Envelope::Insulation | Envelope::Walls | Insulation outer face of RC wall, no gap |
| Opening frame -> wall | Openings | Envelope | Frame recessed 0.08m from wall exterior face |
| Foundation -> slab | Ground | Structure | Foundation centered under wall, below slab |

---

## COORDINATION LOG

File: `output/city101_hub/lock_06_gradient_LOG400_coordination_log.md`
Created at build start. Updated by each agent after every round.
