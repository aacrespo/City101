# Lock Type 04 — Temporal Lock
# LOG400 Complete Building Spec: DRAFT FOR ROUNDTABLE REVIEW
# Status: DRAFT
# Date: 2026-03-27

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry authored in METER-SCALE values (X=-18 to 18, Z=0 to 9.3).
"9.0" in Rhino = 9.0 as a number, displayed as "9 cm" but conceptually 9m.

**ALL coordinates in this spec are meter-scale. Use them exactly as written.**
**Do NOT multiply by 100. Do NOT convert.**

X = corridor axis (negative = Night/West/Entry, positive = Dawn/East/Exit)
Y = lateral axis (positive = North, negative = South)
Z = vertical (0 = Night Chamber finished floor level)

**Key asymmetry:** Dawn Chamber floor is at Z=0.3 (30cm step up — temporal passage raises you).

---

## CONCEPT SUMMARY

Three-part sequence: Night Chamber → Gate → Dawn Chamber.
The occupant enters at last service (01:30), rests through the dead window, exits at first service (05:00).
Night is compressed, protective, introverted. Dawn is open, bright, activating.
The Gate is the tallest, thinnest element — the temporal threshold.

---

## RHINO TARGET

Instance: port 9001 (target: `"structure"`)
All MCP tool calls must include `target: "structure"`

---

## LAYERS TO CREATE

### Base layers (LOG200)
```
Type_04_Temporal::Volumes       — RGB(105, 219, 124)  — wall shells, floor slabs
Type_04_Temporal::Circulation   — RGB(160, 235, 175)  — paths, stairs
Type_04_Temporal::Structure     — RGB(75, 155, 90)    — columns, beams
Type_04_Temporal::Openings      — RGB(130, 225, 150)  — door/window frames
Type_04_Temporal::Annotations   — RGB(200, 245, 210)  — text dots
```

### Detail layers (LOG300–400)
```
Type_04_Temporal::L300_Roof     — RGB(85, 180, 105)   — roof slabs, parapets, canopy slab
Type_04_Temporal::L350_Detail   — RGB(60, 135, 78)    — connections, frames, brackets, kickers, stair treads
Type_04_Temporal::L400_Material — RGB(45, 100, 60)    — formwork, joints, hardware, edge conditions, assembly layers
```

---

## SECTION A — BASE BUILDING (Volumes + Structure + Openings)

Wall thickness: 0.3m throughout (Night, Gate, Dawn).
Volume coordinates = inner face of walls.
Outer face = inner + 0.3m outward.

### Wall outer face reference
| Zone | Inner boundary | Outer face |
|------|---------------|------------|
| Night N | Y=+6.0 | Y=+6.3 |
| Night S | Y=-6.0 | Y=-6.3 |
| Night W | X=-18.0 | X=-18.3 |
| Night E (gate junction) | X=-3.0 | — (shared with gate) |
| Gate N | Y=+4.0 | Y=+4.3 |
| Gate S | Y=-4.0 | Y=-4.3 |
| Gate W | X=-3.0 | X=-3.3 |
| Gate E | X=+3.0 | X=+3.3 |
| Dawn N | Y=+6.0 | Y=+6.3 |
| Dawn S | Y=-6.0 | Y=-6.3 |
| Dawn W (gate junction) | X=+3.0 | — (shared with gate) |
| Dawn E | X=+18.0 | X=+18.3 |

---

### A1. Night Chamber Walls

Layer: `Type_04_Temporal::Volumes`
4 wall shells, 0.3m thick, Z=[0, 6.0].

```
A1_night_wall_N:   [-18.0, 6.0, 0.0] → [-3.0, 6.3, 6.0]
A1_night_wall_S:   [-18.0, -6.3, 0.0] → [-3.0, -6.0, 6.0]
A1_night_wall_W:   [-18.3, -6.3, 0.0] → [-18.0, 6.3, 6.0]
A1_night_wall_E:   [-3.3, -6.3, 0.0] → [-3.0, 6.3, 6.0]
```

Note: Night E wall runs full Y extent [-6.3, 6.3] to close the chamber. Gate opening is cut via the Openings layer (Section A7).

---

### A2. Gate Walls

Layer: `Type_04_Temporal::Volumes`
4 wall shells, 0.3m thick, Z=[0, 9.0].

```
A2_gate_wall_N:   [-3.0, 4.0, 0.0] → [3.0, 4.3, 9.0]
A2_gate_wall_S:   [-3.0, -4.3, 0.0] → [3.0, -4.0, 9.0]
A2_gate_wall_W:   [-3.3, -4.3, 0.0] → [-3.0, 4.3, 9.0]
A2_gate_wall_E:   [3.0, -4.3, 0.0] → [3.3, 4.3, 9.0]
```

Note: Gate W wall overlaps Night E wall at X=[-3.3, -3.0]. This is intentional — they are the same physical wall from different volumes. [FLAG 1: Should gate W and night E be merged into one wall, or kept as two overlapping shells?]

---

### A3. Dawn Chamber Walls

Layer: `Type_04_Temporal::Volumes`
4 wall shells, 0.3m thick, Z=[0.3, 7.0].
Dawn floor is at Z=0.3 — walls start there.

```
A3_dawn_wall_N:   [3.0, 6.0, 0.3] → [18.0, 6.3, 7.0]
A3_dawn_wall_S:   [3.0, -6.3, 0.3] → [18.0, -6.0, 7.0]
A3_dawn_wall_W:   [3.0, -6.3, 0.3] → [3.3, 6.3, 7.0]
A3_dawn_wall_E:   [18.0, -6.3, 0.3] → [18.3, 6.3, 7.0]
```

Note: Dawn W wall overlaps Gate E wall at X=[3.0, 3.3]. Same overlap situation as Night/Gate. [FLAG 1 applies here too]

---

### A4. Floor Slabs

Layer: `Type_04_Temporal::Volumes`

**Night Chamber ground slab** (300mm thick):
```
A4_night_floor_slab:   [-18.3, -6.3, -0.3] → [-3.0, 6.3, 0.0]
```

**Gate ground slab** (300mm thick, at Z=0 — continuous with Night):
```
A4_gate_floor_slab:   [-3.3, -4.3, -0.3] → [3.3, 4.3, 0.0]
```

**Dawn Chamber raised floor slab** (300mm thick, top at Z=0.3):
```
A4_dawn_floor_slab:   [3.0, -6.3, 0.0] → [18.3, 6.3, 0.3]
```

**Threshold step** (transition from Z=0 to Z=0.3 at the gate-dawn boundary):
```
A4_threshold_step:   [2.7, -4.0, 0.0] → [3.3, 4.0, 0.3]
```
The step is within the gate volume, 0.3m deep in X, at the east edge.

---

### A5. Ground Plane

Layer: `Type_04_Temporal::Volumes`
Extended slab beyond building footprint.

```
A5_ground_plane:   [-20.0, -8.0, -0.15] → [20.0, 8.0, -0.3]
```
Wait — this sits BELOW the floor slabs. Corrected Z:
```
A5_ground_plane:   [-20.0, -8.0, -0.45] → [20.0, 8.0, -0.3]
```
150mm thick slab, bottom of floor slabs at Z=-0.3, ground plane below that.

[FLAG 2: Ground plane Z position relative to floor slabs — should it be flush with Night floor bottom (-0.3) or below it?]

---

### A6. Structure — Columns and Beams

Layer: `Type_04_Temporal::Structure`

**8 columns total**, 0.3m × 0.3m section:

| ID | Label | X | Y | Z_base | Z_top | Section |
|----|-------|---|---|--------|-------|---------|
| C1 | Gate NW | -3.0 | +4.0 | 0.0 | 9.0 | 0.3×0.3 |
| C2 | Gate NE | +3.0 | +4.0 | 0.0 | 9.0 | 0.3×0.3 |
| C3 | Gate SE | +3.0 | -4.0 | 0.0 | 9.0 | 0.3×0.3 |
| C4 | Gate SW | -3.0 | -4.0 | 0.0 | 9.0 | 0.3×0.3 |
| C5 | Night S | -10.0 | -3.0 | 0.0 | 6.0 | 0.3×0.3 |
| C6 | Night N | -10.0 | +3.0 | 0.0 | 6.0 | 0.3×0.3 |
| C7 | Dawn S | +10.0 | -3.0 | 0.3 | 7.0 | 0.3×0.3 |
| C8 | Dawn N | +10.0 | +3.0 | 0.3 | 7.0 | 0.3×0.3 |

Column geometry (centered on position, ±0.15):
```
A6_col_C1_gate_NW:   [-3.15, 3.85, 0.0]  → [-2.85, 4.15, 9.0]
A6_col_C2_gate_NE:   [2.85, 3.85, 0.0]   → [3.15, 4.15, 9.0]
A6_col_C3_gate_SE:   [2.85, -4.15, 0.0]  → [3.15, -3.85, 9.0]
A6_col_C4_gate_SW:   [-3.15, -4.15, 0.0] → [-2.85, -3.85, 9.0]
A6_col_C5_night_S:   [-10.15, -3.15, 0.0] → [-9.85, -2.85, 6.0]
A6_col_C6_night_N:   [-10.15, 2.85, 0.0]  → [-9.85, 3.15, 6.0]
A6_col_C7_dawn_S:    [9.85, -3.15, 0.3]   → [10.15, -2.85, 7.0]
A6_col_C8_dawn_N:    [9.85, 2.85, 0.3]    → [10.15, 3.15, 7.0]
```

**Gate canopy beam** — 0.3m × 0.3m section, spans X=[-4.5, 4.5] at Z=8:
```
A6_canopy_beam:   [-4.5, -0.15, 7.7] → [4.5, 0.15, 8.0]
```
Beam overhangs 1.5m beyond gate walls on each side (gate at X=±3, beam to X=±4.5).

**Night mezzanine beam** — spans Y=[-6, 6] at X=-10, Z=3.0:
```
A6_night_mezz_beam:   [-10.15, -6.0, 2.7] → [-9.85, 6.0, 3.0]
```
Supports mezzanine sleeping level. 0.3m deep beam.

[FLAG 3: Should Dawn Chamber also have a mezzanine beam at X=+10, Z=3.3 for symmetry with the preparation level?]

---

### A7. Openings

Layer: `Type_04_Temporal::Openings`
Modeled as thin frame boxes (0.05m thick) marking the opening boundary.

**Night Chamber openings:**

West entry door (modest, introverted):
```
A7_night_entry_door:   [-18.3, -1.5, 0.0] → [-18.25, 1.5, 3.5]
```
3.0m wide × 3.5m tall — understated arrival.

North face — 3 small high windows (Z=3.5–5.5, each 1.5m wide, spaced 4m apart):
```
A7_night_win_N1:   [-15.0, 6.25, 3.5] → [-13.5, 6.3, 5.5]
A7_night_win_N2:   [-11.0, 6.25, 3.5] → [-9.5, 6.3, 5.5]
A7_night_win_N3:   [-7.0, 6.25, 3.5]  → [-5.5, 6.3, 5.5]
```

**Gate openings:**

Night-side passage (west face of gate, Y=[-4, 4]):
```
A7_gate_passage_W:   [-3.35, -2.0, 0.0] → [-3.3, 2.0, 7.0]
```
4.0m wide × 7.0m tall — monumental vertical slot.

Dawn-side passage (east face of gate):
```
A7_gate_passage_E:   [3.3, -2.0, 0.3] → [3.35, 2.0, 7.0]
```
4.0m wide × 6.7m tall (starts at Z=0.3, dawn floor level).

[FLAG 4: Gate passages are 4m wide (Y=[-2,2]) per concept — not the full 8m gate width. The offset/angle for "not simultaneously visible" is achieved by the 6m depth of the gate volume, not by narrowing. Confirm this reading.]

**Dawn Chamber openings:**

East face — large window/opening (morning light):
```
A7_dawn_window_E:   [18.25, -3.0, 1.3] → [18.3, 3.0, 6.3]
```
6.0m wide × 5.0m tall (Z from 0.3+1.0=1.3 to 6.3). Generous, extroverted.

South face — 3 wider windows (each 2.4m wide):
```
A7_dawn_win_S1:   [5.5, -6.3, 1.1]  → [7.9, -6.25, 5.8]
A7_dawn_win_S2:   [9.3, -6.3, 1.1]  → [11.7, -6.25, 5.8]
A7_dawn_win_S3:   [13.1, -6.3, 1.1] → [15.5, -6.25, 5.8]
```
Each 2.4m wide × 4.7m tall — three generous punctuations.

East exit door:
```
A7_dawn_exit_door:   [18.25, -1.5, 0.3] → [18.3, 1.5, 4.0]
```
3.0m wide × 3.7m tall — departure.

---

### A8. Circulation

Layer: `Type_04_Temporal::Circulation`

**Primary path polyline:**
Points: (-18, 0, 0.5) → (-3, 0, 0.5) → (0, 0, 0.5) → (3, 0, 0.5) → (18, 0, 0.8)
Note: Z changes from 0.5 to 0.8 at dawn side (floor at Z=0.3 + 0.5m eye-level offset).

Actually, circulation at walking height:
```
A8_primary_path:   Polyline [(-18, 0, 0.0), (-3, 0, 0.0), (0, 0, 0.0), (3, 0, 0.3), (18, 0, 0.3)]
```

**Night stair** (Z=0 to Z=3, mezzanine sleeping level):
```
A8_night_stair_block:   [-15.0, -3.0, 0.0] → [-12.0, 3.0, 3.0]
```
3.0m × 6.0m × 3.0m stair block. 10 treads (300mm rise each = 3.0m total).

**Dawn stair** (Z=0.3 to Z=3.3, preparation level):
```
A8_dawn_stair_block:   [12.0, -3.0, 0.3] → [15.0, 3.0, 3.3]
```
3.0m × 6.0m × 3.0m stair block. 10 treads.

---

### A9. Annotations

Layer: `Type_04_Temporal::Annotations`
Text dots at:

```
(-10.5, 0, 3.0)   → "NIGHT / REST / 01:30"
(0, 0, 4.5)       → "THRESHOLD / TIME PASSES"
(10.5, 0, 3.5)    → "DAWN / PREPARATION / 05:00"
(-18, 0, 1.75)    → "ENTRY (LAST SERVICE)"
(18, 0, 2.15)     → "EXIT (FIRST SERVICE)"
(0, 0, 0.15)      → "Z+0.3 LEVEL CHANGE"
```

---

## SECTION A SUMMARY

| Sub | Elements | Layer | Count |
|-----|----------|-------|-------|
| A1 | Night walls | Volumes | 4 |
| A2 | Gate walls | Volumes | 4 |
| A3 | Dawn walls | Volumes | 4 |
| A4 | Floor slabs + threshold | Volumes | 4 |
| A5 | Ground plane | Volumes | 1 |
| A6 | Columns | Structure | 8 |
| A6 | Beams | Structure | 2 |
| A7 | Opening frames | Openings | 11 |
| A8 | Circulation path | Circulation | 1 |
| A8 | Stair blocks | Circulation | 2 |
| A9 | Text dots | Annotations | 6 |
| **TOTAL Section A** | | | **47** |

---

## SECTION 1 — ROOF SYSTEM (L300_Roof)

### Slab thickness rationale
- Night Chamber: 12m short span (Y direction) → span/30 = 400mm (0.4 units)
- Gate Zone: 8m span (Y direction) → span/30 = 267mm → use 300mm (0.3 units)
- Dawn Chamber: 12m short span → 400mm (0.4 units)
- Canopy: 9m span (X direction) → span/30 = 300mm (0.3 units)
- Bearing: slabs sit ON TOP of existing wall shells

---

### 1.1 Night Chamber Roof Slab

Layer: `Type_04_Temporal::L300_Roof`
Name: `L300_night_roof_slab`

```
Corner A: [-18.0, -6.0, 6.0]
Corner B: [-3.0,   6.0, 6.4]
```
Thickness: 0.4 units (400mm)
Top face at Z=6.4, bottom at Z=6.0 (bearing on existing 6.0m walls).

Drainage: 1.5% fall south (toward Y=-6.0). Drop = 12.0 × 0.015 = 0.18 units.
Modeled as flat box. Annotate fall direction on Annotations layer.

---

### 1.2 Night Chamber Parapets

Parapet height: 500mm (0.5 units) above slab top (Z=6.4).
Parapet thickness: 300mm (0.3 units) matching wall thickness.
Parapet top: Z = 6.4 + 0.5 = 6.9
Z range: [6.4, 6.9]

No east parapet — abuts Gate.

```
L300_night_parapet_N:   [-18.0, 5.7, 6.4] → [-3.0, 6.0, 6.9]
L300_night_parapet_S:   [-18.0, -6.0, 6.4] → [-3.0, -5.7, 6.9]
L300_night_parapet_W:   [-18.0, -6.0, 6.4] → [-17.7, 6.0, 6.9]
```
(3 parapet boxes)

---

### 1.3 Gate Roof Slab

Layer: `Type_04_Temporal::L300_Roof`
Name: `L300_gate_roof_slab`

```
Corner A: [-3.0, -4.0, 9.0]
Corner B: [3.0,   4.0, 9.3]
```
Thickness: 0.3 units (300mm)
Top at Z=9.3, bottom at Z=9.0 (bearing on existing 9.0m gate walls).

Drainage: FLAT (symbolic monument roof). Annotate.

Gate parapets: NOT modeled as separate elements.
Gate walls extend to Z=9.0. The wall top IS the parapet condition.

---

### 1.4 Dawn Chamber Roof Slab

Layer: `Type_04_Temporal::L300_Roof`
Name: `L300_dawn_roof_slab`

```
Corner A: [3.0,  -6.0, 7.0]
Corner B: [18.0,  6.0, 7.4]
```
Thickness: 0.4 units (400mm)
Top at Z=7.4, bottom at Z=7.0.

Drainage: 1.5% fall north (toward Y=+6.0). Annotate.

---

### 1.5 Dawn Chamber Parapets

Z range: [7.4, 7.9]
No west parapet — abuts Gate.

```
L300_dawn_parapet_N:   [3.0,  5.7, 7.4] → [18.0,  6.0, 7.9]
L300_dawn_parapet_S:   [3.0, -6.0, 7.4] → [18.0, -5.7, 7.9]
L300_dawn_parapet_E:   [17.7, -6.0, 7.4] → [18.0,  6.0, 7.9]
```
(3 parapet boxes)

---

### 1.6 Gate Canopy Slab

Layer: `Type_04_Temporal::L300_Roof`
Name: `L300_canopy_slab`

The canopy overhangs 1.5m on each side of the gate at Z=8.
Canopy slab sits ON the canopy beam (beam top at Z=8.0).
Canopy extends full gate width in Y ([-4.0, 4.0]).

```
Corner A: [-4.5, -4.0, 8.0]
Corner B: [4.5,   4.0, 8.3]
```
Thickness: 0.3 units (300mm). Span: 9m in X → 0.3m correct per span/30.

[FLAG 5: Canopy Y extent — should it match gate wall inner face (Y=±4.0) or extend slightly beyond for weather protection? Kept at ±4.0 for now.]

---

### Section 1 element count

| Sub | Name | Count |
|-----|------|-------|
| 1.1 | Night roof slab | 1 |
| 1.2 | Night parapets | 3 |
| 1.3 | Gate roof slab | 1 |
| 1.4 | Dawn roof slab | 1 |
| 1.5 | Dawn parapets | 3 |
| 1.6 | Canopy slab | 1 |
| **Total Section 1** | | **10** |

---

## SECTION 2 — ROOF ASSEMBLY LAYERS (L400_Material)

Total build-up: 120mm XPS + 5mm membrane + 50mm gravel = 175mm = 0.175 units.
Assembly sits inside parapets, on top of roof slab.

---

### 2.1 Night Chamber Roof Assembly

Slab top at Z=6.4. Inset from parapet inner faces.
Inner faces: Y=[-5.7, 5.7], X=[-17.7, -3.0].

```
L400_night_insulation:   [-17.7, -5.7, 6.40] → [-3.0, 5.7, 6.52]    (120mm)
L400_night_membrane:     [-17.7, -5.7, 6.52] → [-3.0, 5.7, 6.525]   (5mm)
L400_night_gravel:       [-17.7, -5.7, 6.525] → [-3.0, 5.7, 6.575]  (50mm)
```

---

### 2.2 Gate Roof Assembly

Slab top at Z=9.3. Inside gate wall perimeter.
Gate wall inner faces: ±3.0 in X, ±4.0 in Y (walls are 0.3m thick, inner face = outer - 0.3).
Wait — volume boundary IS the inner face. So inner faces at X=±3.0, Y=±4.0.
But parapets... gate walls go to Z=9 and ARE the parapet. Assembly sits inside wall tops.

Actually, the slab sits at Z=[9.0, 9.3], ON TOP of the walls. The walls define the inner boundary.
Assembly on top of slab, inset from wall inner faces:

```
L400_gate_insulation:   [-3.0, -4.0, 9.30] → [3.0, 4.0, 9.42]    (120mm)
L400_gate_membrane:     [-3.0, -4.0, 9.42] → [3.0, 4.0, 9.425]   (5mm)
L400_gate_gravel:       [-3.0, -4.0, 9.425] → [3.0, 4.0, 9.475]  (50mm)
```

---

### 2.3 Dawn Chamber Roof Assembly

Slab top at Z=7.4. Inner faces: Y=[-5.7, 5.7], X=[3.0, 17.7].

```
L400_dawn_insulation:   [3.0, -5.7, 7.40] → [17.7, 5.7, 7.52]    (120mm)
L400_dawn_membrane:     [3.0, -5.7, 7.52] → [17.7, 5.7, 7.525]   (5mm)
L400_dawn_gravel:       [3.0, -5.7, 7.525] → [17.7, 5.7, 7.575]  (50mm)
```

---

### 2.4 Canopy Roof Assembly

Slab top at Z=8.3. No parapets on canopy — open edges.
Inset 50mm from edges for drip:

```
L400_canopy_insulation:   [-4.45, -3.95, 8.30] → [4.45, 3.95, 8.42]    (120mm)
L400_canopy_membrane:     [-4.45, -3.95, 8.42] → [4.45, 3.95, 8.425]   (5mm)
L400_canopy_gravel:       [-4.45, -3.95, 8.425] → [4.45, 3.95, 8.475]  (50mm)
```

**Total Section 2: 12 elements** (4 zones × 3 layers)

---

## SECTION 3 — PARAPET EDGE CONDITIONS (L400_Material)

### 3.1 Waterproofing Upstands

20mm wide × 150mm tall thin box against inner face of each parapet.

**Night Chamber** (slab top Z=6.4, upstand Z=[6.4, 6.55]):
```
L400_night_upstand_N:   [-17.7, 5.68, 6.4] → [-3.0, 5.70, 6.55]
L400_night_upstand_S:   [-17.7, -5.70, 6.4] → [-3.0, -5.68, 6.55]
L400_night_upstand_W:   [-17.72, -5.7, 6.4] → [-17.70, 5.7, 6.55]
```

**Dawn Chamber** (slab top Z=7.4, upstand Z=[7.4, 7.55]):
```
L400_dawn_upstand_N:   [3.0, 5.68, 7.4] → [17.7, 5.70, 7.55]
L400_dawn_upstand_S:   [3.0, -5.70, 7.4] → [17.7, -5.68, 7.55]
L400_dawn_upstand_E:   [17.68, -5.7, 7.4] → [17.70, 5.7, 7.55]
```

### 3.2 Drip Edges

30mm × 20mm at outer top corner of each parapet.

**Night Chamber** (parapet top Z=6.9):
```
L400_night_drip_N:   [-17.7, 5.97, 6.87] → [-3.0, 6.0, 6.9]
L400_night_drip_S:   [-17.7, -6.0, 6.87] → [-3.0, -5.97, 6.9]
L400_night_drip_W:   [-18.0, -6.0, 6.87] → [-17.97, 6.0, 6.9]
```

**Dawn Chamber** (parapet top Z=7.9):
```
L400_dawn_drip_N:   [3.0, 5.97, 7.87] → [17.7, 6.0, 7.9]
L400_dawn_drip_S:   [3.0, -6.0, 7.87] → [17.7, -5.97, 7.9]
L400_dawn_drip_E:   [17.97, -6.0, 7.87] → [18.0, 6.0, 7.9]
```

**Total Section 3: 12 elements** (6 upstands + 6 drip edges)

---

## SECTION 4 — FORMWORK LINES (L400_Material)

RC walls cast in 2400mm (2.4 unit) lifts.
Formwork lift lines = thin horizontal box proud of wall outer face by 20mm (0.02 units), 20mm tall.

### Lift elevations
- Night (6.0m total): lifts at Z=2.4 only (one lift below 6m)
- Gate (9.0m total): lifts at Z=2.4, Z=4.8, Z=7.2
- Dawn (7.0m total, starts Z=0.3): lifts at Z=2.7 (2.4 above floor), Z=5.1

[FLAG 6: Dawn formwork lifts — measured from dawn floor Z=0.3, so first lift at Z=0.3+2.4=2.7 and second at Z=0.3+4.8=5.1. Or measured from Z=0 globally? Using local floor for consistency with construction sequence.]

### Night formwork lines (3 elements)

Z=2.4 lift. Exposed outer faces: N (Y=6.3), S (Y=-6.3), W (X=-18.3).
East face (X=-3.0) is interior to gate junction — no formwork.

```
L400_night_fw_N_L1:   [-18.3, 6.30, 2.39] → [-3.0, 6.32, 2.41]
L400_night_fw_S_L1:   [-18.3, -6.32, 2.39] → [-3.0, -6.30, 2.41]
L400_night_fw_W_L1:   [-18.32, -6.3, 2.39] → [-18.30, 6.3, 2.41]
```

### Gate formwork lines (12 elements)

All 4 outer faces at each of 3 lifts.
Gate outer faces: X=±3.3, Y=±4.3.

Z=2.4 lift:
```
L400_gate_fw_N_L1:   [-3.3, 4.30, 2.39] → [3.3, 4.32, 2.41]
L400_gate_fw_S_L1:   [-3.3, -4.32, 2.39] → [3.3, -4.30, 2.41]
L400_gate_fw_E_L1:   [3.30, -4.3, 2.39] → [3.32, 4.3, 2.41]
L400_gate_fw_W_L1:   [-3.32, -4.3, 2.39] → [-3.30, 4.3, 2.41]
```

Z=4.8 lift:
```
L400_gate_fw_N_L2:   [-3.3, 4.30, 4.79] → [3.3, 4.32, 4.81]
L400_gate_fw_S_L2:   [-3.3, -4.32, 4.79] → [3.3, -4.30, 4.81]
L400_gate_fw_E_L2:   [3.30, -4.3, 4.79] → [3.32, 4.3, 4.81]
L400_gate_fw_W_L2:   [-3.32, -4.3, 4.79] → [-3.30, 4.3, 4.81]
```

Z=7.2 lift:
```
L400_gate_fw_N_L3:   [-3.3, 4.30, 7.19] → [3.3, 4.32, 7.21]
L400_gate_fw_S_L3:   [-3.3, -4.32, 7.19] → [3.3, -4.30, 7.21]
L400_gate_fw_E_L3:   [3.30, -4.3, 7.19] → [3.32, 4.3, 7.21]
L400_gate_fw_W_L3:   [-3.32, -4.3, 7.19] → [-3.30, 4.3, 7.21]
```

### Dawn formwork lines (6 elements)

Exposed outer faces: N (Y=6.3), S (Y=-6.3), E (X=18.3).
West face interior — no formwork.

Z=2.7 lift:
```
L400_dawn_fw_N_L1:   [3.0, 6.30, 2.69] → [18.3, 6.32, 2.71]
L400_dawn_fw_S_L1:   [3.0, -6.32, 2.69] → [18.3, -6.30, 2.71]
L400_dawn_fw_E_L1:   [18.30, -6.3, 2.69] → [18.32, 6.3, 2.71]
```

Z=5.1 lift:
```
L400_dawn_fw_N_L2:   [3.0, 6.30, 5.09] → [18.3, 6.32, 5.11]
L400_dawn_fw_S_L2:   [3.0, -6.32, 5.09] → [18.3, -6.30, 5.11]
L400_dawn_fw_E_L2:   [18.30, -6.3, 5.09] → [18.32, 6.3, 5.11]
```

**Total Section 4: 21 elements** (3 + 12 + 6)

---

## SECTION 5 — EXPANSION JOINTS (L400_Material)

20mm-wide solid boxes, dark color (RGB 20,20,20).
Required every ~6m on long spans.

**Night Chamber** joint at X=-10.5 (midpoint of -18 to -3):
```
L400_night_joint_wall:   [-10.51, -6.3, 0.0] → [-10.49, 6.3, 6.0]
L400_night_joint_slab:   [-10.51, -6.0, 6.0] → [-10.49, 6.0, 6.4]
```

**Dawn Chamber** joint at X=+10.5 (midpoint of 3 to 18):
```
L400_dawn_joint_wall:   [10.49, -6.3, 0.3] → [10.51, 6.3, 7.0]
L400_dawn_joint_slab:   [10.49, -6.0, 7.0] → [10.51, 6.0, 7.4]
```

**Total Section 5: 4 elements**

---

## SECTION 6 — STRUCTURAL CONNECTIONS (L350_Detail)

### 6.1 Column Base Plates — 8 columns

Steel plate: 500mm × 500mm × 25mm (0.5 × 0.5 × 0.025 units).
Z position: [-0.025, 0] for Night/Gate columns (plate cast into slab, top flush with floor).
Dawn columns: Z=[0.275, 0.3] (flush with dawn floor at Z=0.3).

```
L350_bp_C1_gate_NW:   [-3.25, 3.75, -0.025] → [-2.75, 4.25, 0.0]
L350_bp_C2_gate_NE:   [2.75, 3.75, -0.025]  → [3.25, 4.25, 0.0]
L350_bp_C3_gate_SE:   [2.75, -4.25, -0.025] → [3.25, -3.75, 0.0]
L350_bp_C4_gate_SW:   [-3.25, -4.25, -0.025] → [-2.75, -3.75, 0.0]
L350_bp_C5_night_S:   [-10.25, -3.25, -0.025] → [-9.75, -2.75, 0.0]
L350_bp_C6_night_N:   [-10.25, 2.75, -0.025] → [-9.75, 3.25, 0.0]
L350_bp_C7_dawn_S:    [9.75, -3.25, 0.275] → [10.25, -2.75, 0.3]
L350_bp_C8_dawn_N:    [9.75, 2.75, 0.275]  → [10.25, 3.25, 0.3]
```

---

### 6.2 Column Top Bearing Plates

Steel plate: 500mm × 500mm × 20mm (0.5 × 0.5 × 0.02 units).
Sits at column top, below roof slab.

**Gate columns** top at Z=9.0 (support gate roof):
```
L350_tp_C1_gate_NW:   [-3.25, 3.75, 8.98] → [-2.75, 4.25, 9.0]
L350_tp_C2_gate_NE:   [2.75, 3.75, 8.98]  → [3.25, 4.25, 9.0]
L350_tp_C3_gate_SE:   [2.75, -4.25, 8.98] → [3.25, -3.75, 9.0]
L350_tp_C4_gate_SW:   [-3.25, -4.25, 8.98] → [-2.75, -3.75, 9.0]
```

**Night columns** top at Z=6.0:
```
L350_tp_C5_night_S:   [-10.25, -3.25, 5.98] → [-9.75, -2.75, 6.0]
L350_tp_C6_night_N:   [-10.25, 2.75, 5.98]  → [-9.75, 3.25, 6.0]
```

**Dawn columns** top at Z=7.0:
```
L350_tp_C7_dawn_S:    [9.75, -3.25, 6.98] → [10.25, -2.75, 7.0]
L350_tp_C8_dawn_N:    [9.75, 2.75, 6.98]  → [10.25, 3.25, 7.0]
```

---

### 6.3 Canopy Beam Brackets

Beam at Y=[-0.15, 0.15], X=[-4.5, 4.5], Z=[7.7, 8.0].
Brackets sit BELOW beam bottom (Z=7.7), embedded into gate wall.
Bracket: 300mm depth × 200mm height × 600mm width.

**Night-side bracket** (embedded in gate W wall inner face at X=-3.0):
```
L350_bracket_canopy_W:   [-3.3, -0.3, 7.5] → [-3.0, 0.3, 7.7]
```

**Dawn-side bracket** (embedded in gate E wall inner face at X=3.0):
```
L350_bracket_canopy_E:   [3.0, -0.3, 7.5] → [3.3, 0.3, 7.7]
```

---

### 6.4 Mezzanine Beam Brackets

Night mezzanine beam at X=[-10.15, -9.85], Z=[2.7, 3.0].
Brackets where beam meets Night N and S walls.

```
L350_bracket_mezz_N:   [-10.3, 5.7, 2.5] → [-9.7, 6.0, 2.7]
L350_bracket_mezz_S:   [-10.3, -6.0, 2.5] → [-9.7, -5.7, 2.7]
```

---

### 6.5 Wall Kickers

50mm × 50mm RC kicker at wall base (Z=[0, 0.05] for Night/Gate, Z=[0.3, 0.35] for Dawn).
Runs on outer face of wall.

**Night kickers:**
```
L350_kicker_night_N:   [-18.0, 6.0, 0.0]  → [-3.0, 6.05, 0.05]
L350_kicker_night_S:   [-18.0, -6.05, 0.0] → [-3.0, -6.0, 0.05]
L350_kicker_night_W:   [-18.05, -6.0, 0.0] → [-18.0, 6.0, 0.05]
```

**Gate kickers:**
```
L350_kicker_gate_N:   [-3.0, 4.0, 0.0]  → [3.0, 4.05, 0.05]
L350_kicker_gate_S:   [-3.0, -4.05, 0.0] → [3.0, -4.0, 0.05]
L350_kicker_gate_E:   [3.0, -4.0, 0.0]  → [3.05, 4.0, 0.05]
L350_kicker_gate_W:   [-3.05, -4.0, 0.0] → [-3.0, 4.0, 0.05]
```

**Dawn kickers (Z=[0.3, 0.35]):**
```
L350_kicker_dawn_N:   [3.0, 6.0, 0.3]  → [18.0, 6.05, 0.35]
L350_kicker_dawn_S:   [3.0, -6.05, 0.3] → [18.0, -6.0, 0.35]
L350_kicker_dawn_E:   [18.0, -6.0, 0.3] → [18.05, 6.0, 0.35]
```

**Total kickers: 3 + 4 + 3 = 10 elements**

---

### Section 6 element count

| Sub | Elements | Count |
|-----|----------|-------|
| 6.1 | Column base plates | 8 |
| 6.2 | Column top plates | 8 |
| 6.3 | Canopy brackets | 2 |
| 6.4 | Mezzanine brackets | 2 |
| 6.5 | Wall kickers | 10 |
| **Total Section 6** | | **30** |

---

## SECTION 7 — OPENING FRAMES & LINTELS (L350_Detail)

Steel hollow section 100mm × 100mm (0.1 × 0.1 units) framing each opening.
RC lintel 300mm deep above each opening.

### 7.1 Night Entry Door Frame (X=-18.3 wall outer face)

Opening: Y=[-1.5, 1.5], Z=[0, 3.5], wall face X=-18.3.

```
L350_frame_night_entry_top:    [-18.4, -1.5, 3.5] → [-18.2, 1.5, 3.6]
L350_frame_night_entry_bot:    [-18.4, -1.5, -0.1] → [-18.2, 1.5, 0.0]
L350_frame_night_entry_jambN:  [-18.4, 1.4, -0.1] → [-18.2, 1.6, 3.6]
L350_frame_night_entry_jambS:  [-18.4, -1.6, -0.1] → [-18.2, -1.4, 3.6]
```

RC lintel:
```
L350_lintel_night_entry:   [-18.6, -1.5, 3.5] → [-18.0, 1.5, 3.8]
```

### 7.2 Night High Windows (3 windows, N wall at Y=6.3)

Each window: 1.5m wide × 2.0m tall (Z=3.5–5.5).

**Window N1** (X=[-15.0, -13.5]):
```
L350_frame_night_N1_top:    [-15.0, 6.2, 5.5] → [-13.5, 6.4, 5.6]
L350_frame_night_N1_bot:    [-15.0, 6.2, 3.4] → [-13.5, 6.4, 3.5]
L350_frame_night_N1_jambW:  [-15.1, 6.2, 3.4] → [-14.9, 6.4, 5.6]
L350_frame_night_N1_jambE:  [-13.6, 6.2, 3.4] → [-13.4, 6.4, 5.6]
L350_lintel_night_N1:       [-15.3, 6.0, 5.5] → [-13.2, 6.3, 5.8]
```

**Window N2** (X=[-11.0, -9.5]):
```
L350_frame_night_N2_top:    [-11.0, 6.2, 5.5] → [-9.5, 6.4, 5.6]
L350_frame_night_N2_bot:    [-11.0, 6.2, 3.4] → [-9.5, 6.4, 3.5]
L350_frame_night_N2_jambW:  [-11.1, 6.2, 3.4] → [-10.9, 6.4, 5.6]
L350_frame_night_N2_jambE:  [-9.6, 6.2, 3.4] → [-9.4, 6.4, 5.6]
L350_lintel_night_N2:       [-11.3, 6.0, 5.5] → [-9.2, 6.3, 5.8]
```

**Window N3** (X=[-7.0, -5.5]):
```
L350_frame_night_N3_top:    [-7.0, 6.2, 5.5] → [-5.5, 6.4, 5.6]
L350_frame_night_N3_bot:    [-7.0, 6.2, 3.4] → [-5.5, 6.4, 3.5]
L350_frame_night_N3_jambW:  [-7.1, 6.2, 3.4] → [-6.9, 6.4, 5.6]
L350_frame_night_N3_jambE:  [-5.6, 6.2, 3.4] → [-5.4, 6.4, 5.6]
L350_lintel_night_N3:       [-7.3, 6.0, 5.5] → [-5.2, 6.3, 5.8]
```

### 7.3 Dawn East Window Frame (X=18.3)

Opening: Y=[-3.0, 3.0], Z=[1.3, 6.3].

```
L350_frame_dawn_E_top:    [18.2, -3.0, 6.3] → [18.4, 3.0, 6.4]
L350_frame_dawn_E_bot:    [18.2, -3.0, 1.2] → [18.4, 3.0, 1.3]
L350_frame_dawn_E_jambN:  [18.2, 2.9, 1.2]  → [18.4, 3.1, 6.4]
L350_frame_dawn_E_jambS:  [18.2, -3.1, 1.2] → [18.4, -2.9, 6.4]
```

RC lintel:
```
L350_lintel_dawn_E:   [18.0, -3.0, 6.3] → [18.6, 3.0, 6.6]
```

### 7.4 Dawn South Windows (3 windows, S wall at Y=-6.3)

Each window: 2.4m wide × 4.7m tall (Z=1.1–5.8).

**Window S1** (X=[5.5, 7.9]):
```
L350_frame_dawn_S1_top:    [5.5, -6.4, 5.8] → [7.9, -6.2, 5.9]
L350_frame_dawn_S1_bot:    [5.5, -6.4, 1.0] → [7.9, -6.2, 1.1]
L350_frame_dawn_S1_jambW:  [5.4, -6.4, 1.0] → [5.6, -6.2, 5.9]
L350_frame_dawn_S1_jambE:  [7.8, -6.4, 1.0] → [8.0, -6.2, 5.9]
L350_lintel_dawn_S1:       [5.2, -6.6, 5.8] → [8.2, -6.0, 6.1]
```

**Window S2** (X=[9.3, 11.7]):
```
L350_frame_dawn_S2_top:    [9.3, -6.4, 5.8] → [11.7, -6.2, 5.9]
L350_frame_dawn_S2_bot:    [9.3, -6.4, 1.0] → [11.7, -6.2, 1.1]
L350_frame_dawn_S2_jambW:  [9.2, -6.4, 1.0] → [9.4, -6.2, 5.9]
L350_frame_dawn_S2_jambE:  [11.6, -6.4, 1.0] → [11.8, -6.2, 5.9]
L350_lintel_dawn_S2:       [9.0, -6.6, 5.8] → [12.0, -6.0, 6.1]
```

**Window S3** (X=[13.1, 15.5]):
```
L350_frame_dawn_S3_top:    [13.1, -6.4, 5.8] → [15.5, -6.2, 5.9]
L350_frame_dawn_S3_bot:    [13.1, -6.4, 1.0] → [15.5, -6.2, 1.1]
L350_frame_dawn_S3_jambW:  [13.0, -6.4, 1.0] → [13.2, -6.2, 5.9]
L350_frame_dawn_S3_jambE:  [15.4, -6.4, 1.0] → [15.6, -6.2, 5.9]
L350_lintel_dawn_S3:       [12.8, -6.6, 5.8] → [15.8, -6.0, 6.1]
```

### 7.5 Dawn Exit Door Frame (X=18.3)

Opening: Y=[-1.5, 1.5], Z=[0.3, 4.0].

```
L350_frame_dawn_exit_top:    [18.2, -1.5, 4.0] → [18.4, 1.5, 4.1]
L350_frame_dawn_exit_bot:    [18.2, -1.5, 0.2] → [18.4, 1.5, 0.3]
L350_frame_dawn_exit_jambN:  [18.2, 1.4, 0.2]  → [18.4, 1.6, 4.1]
L350_frame_dawn_exit_jambS:  [18.2, -1.6, 0.2] → [18.4, -1.4, 4.1]
```

RC lintel:
```
L350_lintel_dawn_exit:   [18.0, -1.5, 4.0] → [18.6, 1.5, 4.3]
```

### Section 7 element count

| Sub | Elements | Count |
|-----|----------|-------|
| 7.1 | Night entry frame + lintel | 5 |
| 7.2 | Night windows (3 × 5) | 15 |
| 7.3 | Dawn E window frame + lintel | 5 |
| 7.4 | Dawn S windows (3 × 5) | 15 |
| 7.5 | Dawn exit frame + lintel | 5 |
| **Total Section 7** | | **45** |

---

## SECTION 8 — STAIR TREADS (L350_Detail)

Individual treads modeled at LOG400.
Rise per tread: 300mm (0.3 units) for 10 treads over 3.0m height.
Going per tread: 300mm (0.3 units) in X.
Tread width: 6.0m (Y=[-3, 3]).
Tread thickness: 50mm (0.05 units).

### 8.1 Night Stair Treads (X=[-15, -12], Z=[0, 3], 10 treads)

Treads progress from X=-15 (bottom) to X=-12 (top), Z=0 to Z=3.
Each tread: 0.3m going in X, 0.05m thick, 6.0m wide in Y.

```
L350_night_tread_01:   [-15.0, -3.0, 0.25]  → [-14.7, 3.0, 0.30]
L350_night_tread_02:   [-14.7, -3.0, 0.55]  → [-14.4, 3.0, 0.60]
L350_night_tread_03:   [-14.4, -3.0, 0.85]  → [-14.1, 3.0, 0.90]
L350_night_tread_04:   [-14.1, -3.0, 1.15]  → [-13.8, 3.0, 1.20]
L350_night_tread_05:   [-13.8, -3.0, 1.45]  → [-13.5, 3.0, 1.50]
L350_night_tread_06:   [-13.5, -3.0, 1.75]  → [-13.2, 3.0, 1.80]
L350_night_tread_07:   [-13.2, -3.0, 2.05]  → [-12.9, 3.0, 2.10]
L350_night_tread_08:   [-12.9, -3.0, 2.35]  → [-12.6, 3.0, 2.40]
L350_night_tread_09:   [-12.6, -3.0, 2.65]  → [-12.3, 3.0, 2.70]
L350_night_tread_10:   [-12.3, -3.0, 2.95]  → [-12.0, 3.0, 3.00]
```

### 8.2 Dawn Stair Treads (X=[12, 15], Z=[0.3, 3.3], 10 treads)

Treads progress from X=12 (bottom) to X=15 (top).

```
L350_dawn_tread_01:   [12.0, -3.0, 0.55]  → [12.3, 3.0, 0.60]
L350_dawn_tread_02:   [12.3, -3.0, 0.85]  → [12.6, 3.0, 0.90]
L350_dawn_tread_03:   [12.6, -3.0, 1.15]  → [12.9, 3.0, 1.20]
L350_dawn_tread_04:   [12.9, -3.0, 1.45]  → [13.2, 3.0, 1.50]
L350_dawn_tread_05:   [13.2, -3.0, 1.75]  → [13.5, 3.0, 1.80]
L350_dawn_tread_06:   [13.5, -3.0, 2.05]  → [13.8, 3.0, 2.10]
L350_dawn_tread_07:   [13.8, -3.0, 2.35]  → [14.1, 3.0, 2.40]
L350_dawn_tread_08:   [14.1, -3.0, 2.65]  → [14.4, 3.0, 2.70]
L350_dawn_tread_09:   [14.4, -3.0, 2.95]  → [14.7, 3.0, 3.00]
L350_dawn_tread_10:   [14.7, -3.0, 3.25]  → [15.0, 3.0, 3.30]
```

### 8.3 Stair Landings

**Night landing** at top of stair (mezzanine level Z=3.0):
```
L350_night_landing:   [-12.0, -3.0, 2.85] → [-10.0, 3.0, 3.0]
```
150mm thick landing connecting stair to mezzanine beam.

**Dawn landing** at top of stair (Z=3.3):
```
L350_dawn_landing:   [10.0, -3.0, 3.15] → [12.0, 3.0, 3.3]
```

**Total Section 8: 22 elements** (10 + 10 + 2)

---

## SECTION 9 — CANOPY EDGE DETAIL (L400_Material)

### 9.1 Canopy Drip Edges

Canopy has open edges (no parapets). Drip edge around full perimeter.
30mm × 20mm at underside of canopy slab outer edge.
Canopy slab: X=[-4.5, 4.5], Y=[-4.0, 4.0], Z=[8.0, 8.3].

```
L400_canopy_drip_N:   [-4.5, 3.97, 8.0] → [4.5, 4.0, 8.03]
L400_canopy_drip_S:   [-4.5, -4.0, 8.0] → [4.5, -3.97, 8.03]
L400_canopy_drip_W:   [-4.5, -4.0, 8.0] → [-4.47, 4.0, 8.03]
L400_canopy_drip_E:   [4.47, -4.0, 8.0] → [4.5, 4.0, 8.03]
```

### 9.2 Canopy Fascia

Thin metal fascia band around canopy edge, 100mm deep.
```
L400_canopy_fascia_N:   [-4.5, 3.95, 8.0] → [4.5, 4.0, 8.1]
L400_canopy_fascia_S:   [-4.5, -4.0, 8.0] → [4.5, -3.95, 8.1]
L400_canopy_fascia_W:   [-4.5, -4.0, 8.0] → [-4.45, 4.0, 8.1]
L400_canopy_fascia_E:   [4.45, -4.0, 8.0] → [4.5, 4.0, 8.1]
```

**Total Section 9: 8 elements**

---

## SECTION 10 — FACADE PANEL JOINTS (L400_Material)

5mm wide × 20mm deep incised vertical joints on Dawn Chamber facades.
Dawn is the extroverted side — panel joints express facade rhythm.
Full height Z=[0.3, 7.0].

Joints at X=6.5, X=10.5, X=14.5 (3 joints, ~4m spacing on 15m facade).

**North face** (outer at Y=6.3):
```
L400_dawn_pj_N_X6:    [6.500, 6.28, 0.3] → [6.505, 6.30, 7.0]
L400_dawn_pj_N_X10:   [10.500, 6.28, 0.3] → [10.505, 6.30, 7.0]
L400_dawn_pj_N_X14:   [14.500, 6.28, 0.3] → [14.505, 6.30, 7.0]
```

**South face** (outer at Y=-6.3):
```
L400_dawn_pj_S_X6:    [6.500, -6.30, 0.3] → [6.505, -6.28, 7.0]
L400_dawn_pj_S_X10:   [10.500, -6.30, 0.3] → [10.505, -6.28, 7.0]
L400_dawn_pj_S_X14:   [14.500, -6.30, 0.3] → [14.505, -6.28, 7.0]
```

**Total Section 10: 6 elements**

---

## SECTION 11 — THRESHOLD DETAIL (L400_Material)

The Z=0 → Z=0.3 level change at the gate-dawn boundary is the key temporal threshold.

### 11.1 Threshold Stone

Natural stone threshold slab at the gate-dawn boundary.
300mm wide (X) × 4m long (Y, gate width) × 30mm thick.

```
L400_threshold_stone:   [2.85, -2.0, 0.27] → [3.15, 2.0, 0.3]
```
Sits flush with dawn floor, slightly proud of gate floor.

### 11.2 Weatherstrip Groove

5mm × 5mm groove line at threshold:
```
L400_threshold_groove:   [2.975, -2.0, 0.295] → [3.025, 2.0, 0.3]
```

### 11.3 Foundation Strip

Perimeter foundation below ground slab.
600mm wide × 400mm deep strip below all exterior walls.

**Night perimeter:**
```
L400_foundation_night_N:   [-18.6, 5.7, -0.7] → [-3.0, 6.6, -0.3]
L400_foundation_night_S:   [-18.6, -6.6, -0.7] → [-3.0, -5.7, -0.3]
L400_foundation_night_W:   [-18.6, -6.6, -0.7] → [-17.7, 6.6, -0.3]
```

**Gate perimeter:**
```
L400_foundation_gate_N:   [-3.6, 3.7, -0.7] → [3.6, 4.6, -0.3]
L400_foundation_gate_S:   [-3.6, -4.6, -0.7] → [3.6, -3.7, -0.3]
```

**Dawn perimeter:**
```
L400_foundation_dawn_N:   [3.0, 5.7, -0.7] → [18.6, 6.6, -0.3]
L400_foundation_dawn_S:   [3.0, -6.6, -0.7] → [18.6, -5.7, -0.3]
L400_foundation_dawn_E:   [17.7, -6.6, -0.7] → [18.6, 6.6, -0.3]
```

[FLAG 7: Foundation depth — using 400mm below slab bottom (Z=-0.3 to Z=-0.7). Swiss frost protection requires 800mm below ground. If ground level is at Z=-0.45 (ground plane bottom), frost line is at Z=-1.25. Should foundation go deeper?]

**Total Section 11: 10 elements** (2 threshold + 8 foundation)

---

## EXECUTION SUMMARY

### Element count by section

| Section | Type | Count |
|---------|------|-------|
| A (Base building) | Volumes, Structure, Openings, Circulation, Annotations | 47 |
| 1 (Roof system) | L300_Roof | 10 |
| 2 (Roof assembly) | L400_Material | 12 |
| 3 (Edge conditions) | L400_Material | 12 |
| 4 (Formwork lines) | L400_Material | 21 |
| 5 (Expansion joints) | L400_Material | 4 |
| 6 (Structural connections) | L350_Detail | 30 |
| 7 (Opening frames) | L350_Detail | 45 |
| 8 (Stair treads) | L350_Detail | 22 |
| 9 (Canopy edge) | L400_Material | 8 |
| 10 (Facade joints) | L400_Material | 6 |
| 11 (Threshold + foundation) | L400_Material | 10 |
| **GRAND TOTAL** | | **227** |

---

### Build order

1. Create 8 layers (5 base + 3 detail)
2. Section A: Base building (47 elements)
   - A1–A3: Walls (12 boxes)
   - A4–A5: Floor slabs + ground (5 boxes)
   - A6: Columns + beams (10 boxes)
   - A7: Opening frames (11 boxes)
   - A8: Circulation (3 elements)
   - A9: Annotations (6 text dots)
3. Section 1: Roof slabs + parapets (10 boxes)
4. Section 2: Roof assembly layers (12 boxes)
5. Section 3: Edge conditions (12 boxes)
6. Section 4: Formwork lines (21 boxes)
7. Section 5: Expansion joints (4 boxes)
8. Section 6: Structural connections (30 boxes)
9. Section 7: Opening frames + lintels (45 boxes)
10. Section 8: Stair treads (22 boxes)
11. Section 9: Canopy edge (8 boxes)
12. Section 10: Facade joints (6 boxes)
13. Section 11: Threshold + foundation (10 boxes)

---

### FLAG REGISTER (for roundtable review)

| Flag | Question | Default |
|------|----------|---------|
| FLAG 1 | Night E wall / Gate W wall overlap (and Gate E / Dawn W). Merge into single wall or keep as overlapping shells from different volumes? | Keep separate (matches Lock 01 pattern) |
| FLAG 2 | Ground plane Z position — should it be a thin slab below all floor slabs, or a separate landscape element? | 150mm slab at Z=[-0.45, -0.3] |
| FLAG 3 | Dawn mezzanine beam — should Dawn Chamber also have a mezzanine beam at Z=3.3 for the preparation level, symmetric with Night? | Yes — add beam at X=10, Z=3.3 |
| FLAG 4 | Gate passage width — 4m (Y=[-2,2]) per concept, depth handles "not simultaneously visible". Correct? | Yes |
| FLAG 5 | Canopy Y extent — match gate inner (±4.0) or extend for weather protection? | Keep at ±4.0 |
| FLAG 6 | Dawn formwork lifts — measured from dawn floor Z=0.3 (local) or from Z=0 (global)? | Local (Z=2.7, Z=5.1) |
| FLAG 7 | Foundation depth — 400mm below slab sufficient, or must reach 800mm frost protection? | Deepen to Z=-1.1 (800mm below ground) |

---

### Executor notes

1. All coordinates are meter-scale in a centimeter-unit Rhino doc. Use numbers exactly as written.
2. Do NOT multiply by 100.
3. Use `rhino_execute_python_code` with Box() from two corner points for all elements.
4. Batch by section — walls in one script, columns in one script, etc.
5. Target instance: port 9001 (target: "structure"). All MCP calls must include `target: "structure"`.
6. After all geometry: capture Perspective, Top, Front, Right viewports.
7. Night Chamber should feel enclosed, compressed — verify visually.
8. Dawn Chamber should feel open, generous — verify visually.
9. Gate should be tallest element (9m) — verify in elevation.
10. Z=0.3 level change must be visible at gate-dawn boundary.

---

### Archibase references used

| Topic | Source | Applied to |
|-------|--------|-----------|
| Slab thickness | span/30 rule (Archibase L2: roof_systems.md) | Section 1 |
| Parapet height | SIA 358, 500mm non-public (Archibase L2: norms_guidelines) | Section 1 |
| Roof assembly | XPS 120 + membrane 5 + gravel 50 (Archibase L2: roof_systems.md) | Section 2 |
| Formwork lifts | 2400mm lifts (Archibase L2: concrete_systems.md) | Section 4 |
| Base plates | 500×500×25mm steel (Archibase L1: steel profiles) | Section 6 |
| Stair dimensions | R=300mm, G=300mm (SIA/Blondel, Archibase L2: stairs) | Section 8 |
| Foundation | 800mm frost protection (Archibase L2: norms_guidelines) | Section 11 |
| Door dimensions | SIA 500: ≥900mm clear width (Archibase L2: accessibility) | Section A7 |
| Drip edge | 30×20mm standard (Archibase L2: construction_details) | Sections 3, 9 |
| Kicker | 50×50mm RC (Archibase L2: wall_floor_details) | Section 6 |
