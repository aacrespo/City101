# Lock Type 02 — Cargo Lock
# LOG400 Upgrade: ROUNDTABLE-APPROVED Execution Spec
# Status: APPROVED — ready for executor
# Approved by: Roundtable Reviewer
# Date: 2026-03-27

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry is built in METER-SCALE values (e.g., X=-24 means 24 as a number, displayed as "24 cm" but conceptually 24m).

**ALL coordinates in this spec are meter-scale. Use them exactly as written.**
**Do NOT multiply by 100. Do NOT convert.**

X = corridor axis (negative = West/Entry, positive = East/Exit)
Y = lateral axis (positive = North, negative = South)
Z = vertical (0 = finished floor level)

---

## CORRECTIONS FROM ROUNDTABLE REVIEW

| # | Issue | Resolution |
|---|-------|-----------|
| C1 | Observation Corridor roof slab coordinates written twice with conflicting values | Remove first (inner-face) set; use wall-outer-face extents: [-20.3,-4.3,10.0] → [20.3,4.3,10.3] |
| C2 | Corridor parapet inner-face reference inconsistency | Parapet inner faces: Y=±4.0 (N/S), X=±20.0 (E/W). Slab extends to outer face ±4.3/±20.3. Parapets extend wall tops — inner face of parapet = inner face of wall. Confirmed correct in draft; clarified here. |
| C3 | Roof assembly for corridor uses slab inner faces as bounds | Correct: assembly inset to parapet inner faces — Y=±4.0, X=±20.0. Assembly is bounded by parapet inner faces, not slab extents. |
| C4 | Facade panel joint geometry direction ambiguous for Y-face joints | Panel joints on N/S faces: 5mm in X (panel separation direction), 20mm deep in Y (into wall face). Draft coordinates are correct for this interpretation. |
| C5 | Cantilever brackets dimension labeling unclear | Brackets confirmed as bearing stubs only (0.4m projection from column face, not a 4m spanning element). Primary corridor cantilever structure is the floor slab. Bracket function = local bearing shelf. |
| C6 | Column top plates at Z=10.0 nominally overlap with slab bottom at Z=10.0 | Accepted: 20mm bearing plate embedded into slab by 20mm is standard RC practice. Plate at Z=[10.0, 10.02], slab at Z=[10.0, 10.3]. No correction — same convention used in Lock 01 APPROVED. |
| C7 | Logistics hall slab system: 550mm flat slab or 300mm beam+slab? | FLAG 1 resolved: 550mm flat slab (0.55 units). Rationale: (a) building carries heavy logistics loads (sorting machines, forklift traffic); (b) brief says "model as flat box"; (c) span/30 for 16m = 533mm → 550mm is the minimum structurally honest thickness. Beam+slab alternative noted in decision log. |
| C8 | Parapet height for logistics hall: 1100mm chosen; brief minimum is 1070mm | Confirmed: 1100mm (0.11 above 1070mm minimum). Height provides a 30mm margin over SIA 358 threshold. Parapet top Z=6.65 does not conflict with observation corridor floor Z=6 (parapets are at Y=±11, X=±24 — well outside corridor footprint at Y=±4, X=±20). |

---

## FLAG RESOLUTION TABLE

| Flag | Description | Verdict | Rationale |
|------|-------------|---------|-----------|
| FLAG 1 | Logistics hall slab: flat slab (550mm) vs beam+slab (300mm) | RESOLVED: 550mm flat slab | Heavy logistics loads + "model as flat box" directive + span/30=533mm → 550mm minimum. Accepted. |
| FLAG 2 | Logistics hall slab continuity over corridor column locations | RESOLVED: continuous slab, columns penetrate | Standard RC construction. No cutout. Columns at Y=±8 are within slab footprint; this is correct. |
| FLAG 3 | Parapet at X=±20 inner logistics hall edge | RESOLVED: no parapet required | Drop from Z=5.55 to corridor floor Z=6 is only +0.45m (upward). Drop from Z=5.55 to logistics hall floor Z=0 is 5.55m but this is the interior face, not an exposed edge — the observation corridor volume fills this space above Z=6. Exposed edge at X=±20 from Z=5.55 to Z=6 is only 0.45m above the slab — not a fall risk. No parapet added. |
| FLAG 4 | Observation corridor west parapet — included despite brief | RESOLVED: INCLUDE west parapet | The corridor west wall top at Z=10 is a fully exposed edge at Z=10 (4m above corridor floor). Drop to corridor floor = 4m >> 1m threshold. SIA 358 requires parapet. Brief note about "west face abuts stair" refers to the stair FLOOR LEVEL connection at Z=6, not the roof. West parapet at Z=[10.3,11.4] retained. |
| FLAG 5 | Loading dock canopy parapet — omitted as non-public roof | RESOLVED: OMIT parapet, add drip edges only | Canopy is a truck weather shelter, not publicly accessible. No parapet required under Swiss operational standards for non-public industrial roofs. Edge drip in Section 3.2 (canopy drip, see C9 below) added. |
| FLAG 6 | Cantilever bracket interpretation | RESOLVED: bearing stub | Brackets are 300×200×400mm bearing stubs at column faces, not spanning elements. The 4m corridor overhang is carried by the floor slab acting as a cantilever plate anchored to the column at Y=±8 face. Brackets provide the physical bearing shelf. This is the correct structural model. |
| FLAG 7 | Stair formwork lines — exterior/interior determination | RESOLVED: INCLUDE stair N/S faces | Entry and exit stair N/S outer faces (Y=±4.3) are exterior-facing. Stair volumes are not enclosed within the logistics hall. Their outer faces are exposed to weather and should have formwork lines. Included at Z=2.4. |

**Additional correction C9:** Canopy edge drip — the approved spec adds a minimal drip edge on the canopy slab perimeter (west, north, south faces) even without parapets, consistent with FLAG 5 verdict. These are added under Section 3.2.

---

## BASE MODEL RECAP

| Volume | X | Y | Z |
|--------|---|---|---|
| Logistics Hall | [-24, 24] | [-11, 11] | [0, 5] |
| Observation Corridor | [-20, 20] | [-4, 4] | [6, 10] |
| Entry Stair | [-24, -20] | [-4, 4] | [0, 6] |
| Exit Stair | [20, 24] | [-4, 4] | [0, 6] |
| Loading Dock Canopy | [-28, -24] | [-8, 8] | [3, 5.5] |

**Wall thickness:** 300mm (0.3 units) all enclosing walls.

**Column grid:**
- 6 main columns: X=[-16, 0, +16] × Y=[+8, -8], 400×400mm (0.4×0.4 units), Z=[0, 10]
- 4 dock columns: X=[-28, -24] × Y=[+8, -8], 150×150mm (0.15×0.15 units), Z=[0, 5.5]

**Key derived faces (wall outer):**
- Logistics Hall: N outer Y=+11.0, S outer Y=-11.0, W outer X=-24.0, E outer X=+24.0
- Logistics Hall: N inner Y=+10.7, S inner Y=-10.7, W inner X=-23.7, E inner X=+23.7
- Observation Corridor: N outer Y=+4.3, S outer Y=-4.3, W outer X=-20.3, E outer X=+20.3
- Observation Corridor: N inner Y=+4.0, S inner Y=-4.0, W inner X=-20.0, E inner X=+20.0

---

## LAYERS TO CREATE

```
Type_02_Cargo::L300_Roof     — RGB(200, 155, 100)  — roof slabs, parapets
Type_02_Cargo::L350_Detail   — RGB(160, 115, 70)   — connections, frames, brackets
Type_02_Cargo::L400_Material — RGB(120, 85, 50)    — formwork, joints, hardware, edge conditions
```

Do NOT rename or alter existing layers.

---

## SECTION 1 — ROOF SYSTEM (L300_Roof)

### Slab thickness rationale

| Roof zone | Governing span | Span/30 | Adopted thickness | Units |
|-----------|---------------|---------|------------------|-------|
| Logistics Hall | 16m (col-to-col Y) | 533mm | 550mm flat slab | 0.55 |
| Observation Corridor | 8m (Y width) | 267mm | 300mm | 0.30 |
| Loading Dock Canopy | 4m (X, col-to-col) | 133mm | 150mm | 0.15 |

Bearing rule: all slabs sit ON TOP of existing wall tops. Slab bottom = top of walls.

---

### 1.1 Logistics Hall Roof Slab

Layer: `Type_02_Cargo::L300_Roof`
Name: `L300_hall_roof_slab`

```
Corner A: [-24.0, -11.0, 5.0]
Corner B: [ 24.0,  11.0, 5.55]
```
Thickness: 0.55 units (550mm)
Bottom face Z=5.0 (bearing on existing 5.0m walls)
Top face Z=5.55

Drainage: 1.5% fall south (toward Y=-11.0). Drop = 22.0 × 0.015 = 0.33m over full Y span.
Modeled as flat box. Annotate fall direction as text dot on Annotations layer.

Structural note: slab is continuous across full logistics hall footprint. Main columns at Y=±8 penetrate the slab and continue to Z=10, supporting the observation corridor above. No cutout at column locations — standard RC construction.

---

### 1.2 Logistics Hall Parapets

Parapet height: 1100mm (1.1 units) — exceeds SIA 358 minimum 1070mm. ✓
Parapet Z range: [5.55, 6.65]
Parapet thickness: 0.3 units (300mm), extends existing walls upward.

```
L300_hall_parapet_N:   [-24.0, 10.7, 5.55] → [24.0,  11.0, 6.65]
L300_hall_parapet_S:   [-24.0, -11.0, 5.55] → [24.0, -10.7, 6.65]
L300_hall_parapet_W:   [-24.0, -10.7, 5.55] → [-23.7, 10.7, 6.65]
L300_hall_parapet_E:   [23.7,  -10.7, 5.55] → [24.0,  10.7, 6.65]
```

Parapet top Z=6.65 vs observation corridor floor Z=6.0: parapets are at Y=±11 and X=±24; corridor occupies Y=[-4,4], X=[-20,20]. No spatial conflict. ✓
No inner parapets at observation corridor perimeter (X=±20, Y=±4 faces): drop at these faces is ≤ 0.45m — below SIA 358 threshold. ✓

---

### 1.3 Observation Corridor Roof Slab

Layer: `Type_02_Cargo::L300_Roof`
Name: `L300_corridor_roof_slab`

Corridor wall tops at Z=10.0. Slab caps full assembly including wall outer faces.

```
Corner A: [-20.3, -4.3, 10.0]
Corner B: [ 20.3,  4.3, 10.3]
```
Thickness: 0.3 units (300mm)
Bottom face Z=10.0 (bearing on existing 10.0m corridor walls)
Top face Z=10.3

Drainage: 1.5% fall north (toward Y=+4.3). Drop = 8.6 × 0.015 = 0.13m over Y span.
Modeled as flat box. Annotate fall direction.

---

### 1.4 Observation Corridor Parapets

Parapet height: 1100mm (1.1 units) — SIA 358 compliant, publicly accessible roof. ✓
Parapet Z range: [10.3, 11.4]
Parapet thickness: 0.3 units

All 4 faces have parapets (west face included — stair abutment is at Z=6 floor level only; at Z=10 the west face is a free exposed edge with 4m drop to corridor floor).

```
L300_corridor_parapet_N:   [-20.0,  4.0, 10.3] → [20.0,  4.3, 11.4]
L300_corridor_parapet_S:   [-20.0, -4.3, 10.3] → [20.0, -4.0, 11.4]
L300_corridor_parapet_E:   [20.0,  -4.0, 10.3] → [20.3,  4.0, 11.4]
L300_corridor_parapet_W:   [-20.3, -4.0, 10.3] → [-20.0, 4.0, 11.4]
```

---

### 1.5 Loading Dock Canopy Roof Slab

Layer: `Type_02_Cargo::L300_Roof`
Name: `L300_canopy_roof_slab`

Canopy structure tops at Z=5.5. Slab sits on top.

```
Corner A: [-28.0, -8.0, 5.5]
Corner B: [-24.0,  8.0, 5.65]
```
Thickness: 0.15 units (150mm)
Bottom face Z=5.5, top face Z=5.65

Drainage: 1.5% fall south. Drop = 16.0 × 0.015 = 0.24m over 16m Y span.
Modeled as flat box. Annotate drainage direction.
No parapet: non-public industrial maintenance roof. Edge drips only (see Section 3.2).

---

## SECTION 2 — ROOF ASSEMBLY LAYERS (L400_Material)

Build-up: 120mm XPS insulation + 5mm waterproofing membrane + 50mm gravel ballast = 175mm = 0.175 units.
Assembly sits inside parapet inner faces, on top of each roof slab.

---

### 2.1 Logistics Hall Roof Assembly

Slab top: Z=5.55
Parapet inner faces: N at Y=+10.7, S at Y=-10.7, W at X=-23.7, E at X=+23.7

```
L400_hall_insulation:   [-23.7, -10.7, 5.550] → [23.7,  10.7, 5.670]   (120mm)
L400_hall_membrane:     [-23.7, -10.7, 5.670] → [23.7,  10.7, 5.675]   (5mm)
L400_hall_gravel:       [-23.7, -10.7, 5.675] → [23.7,  10.7, 5.725]   (50mm)
```

Assembly top: Z=5.725
Note: assembly extends over full logistics hall slab including the zone beneath the observation corridor. This is the correct thermal envelope for the logistics hall.

---

### 2.2 Observation Corridor Roof Assembly

Slab top: Z=10.3
Parapet inner faces: N at Y=+4.0, S at Y=-4.0, W at X=-20.0, E at X=+20.0

```
L400_corridor_insulation:   [-20.0, -4.0, 10.300] → [20.0, 4.0, 10.420]   (120mm)
L400_corridor_membrane:     [-20.0, -4.0, 10.420] → [20.0, 4.0, 10.425]   (5mm)
L400_corridor_gravel:       [-20.0, -4.0, 10.425] → [20.0, 4.0, 10.475]   (50mm)
```

Assembly top: Z=10.475

---

### 2.3 Loading Dock Canopy Assembly

Slab top: Z=5.65
No parapets — assembly fills full canopy slab area.

```
L400_canopy_insulation:   [-28.0, -8.0, 5.650] → [-24.0, 8.0, 5.770]   (120mm)
L400_canopy_membrane:     [-28.0, -8.0, 5.770] → [-24.0, 8.0, 5.775]   (5mm)
L400_canopy_gravel:       [-28.0, -8.0, 5.775] → [-24.0, 8.0, 5.825]   (50mm)
```

Assembly top: Z=5.825

---

## SECTION 3 — PARAPET EDGE CONDITIONS (L400_Material)

### 3.1 Waterproofing Upstands

20mm wide × 150mm tall box against inner face of each parapet, at slab top level.

**Logistics Hall (slab top Z=5.55, upstand Z=[5.55, 5.70]):**

```
L400_hall_upstand_N:   [-23.7,  10.68, 5.55] → [23.7,  10.70, 5.70]
L400_hall_upstand_S:   [-23.7, -10.70, 5.55] → [23.7, -10.68, 5.70]
L400_hall_upstand_W:   [-23.72, -10.7, 5.55] → [-23.70, 10.7, 5.70]
L400_hall_upstand_E:   [ 23.70, -10.7, 5.55] → [ 23.72, 10.7, 5.70]
```

**Observation Corridor (slab top Z=10.3, upstand Z=[10.3, 10.45]):**

```
L400_corridor_upstand_N:   [-20.0,  3.98, 10.30] → [20.0,  4.00, 10.45]
L400_corridor_upstand_S:   [-20.0, -4.00, 10.30] → [20.0, -3.98, 10.45]
L400_corridor_upstand_E:   [ 19.98, -4.0, 10.30] → [20.00,  4.0, 10.45]
L400_corridor_upstand_W:   [-20.00, -4.0, 10.30] → [-19.98, 4.0, 10.45]
```

---

### 3.2 Drip Edges

30mm × 20mm box at outer top corner of each parapet.

**Logistics Hall parapets (parapet top Z=6.65):**

```
L400_hall_drip_N:   [-23.7,  10.97, 6.62] → [23.7,  11.00, 6.65]
L400_hall_drip_S:   [-23.7, -11.00, 6.62] → [23.7, -10.97, 6.65]
L400_hall_drip_W:   [-24.00, -10.7, 6.62] → [-23.97, 10.7, 6.65]
L400_hall_drip_E:   [ 23.97, -10.7, 6.62] → [ 24.00, 10.7, 6.65]
```

**Observation Corridor parapets (parapet top Z=11.4):**

```
L400_corridor_drip_N:   [-20.0,  4.27, 11.37] → [20.0,  4.30, 11.40]
L400_corridor_drip_S:   [-20.0, -4.30, 11.37] → [20.0, -4.27, 11.40]
L400_corridor_drip_E:   [ 20.27, -4.0, 11.37] → [ 20.30, 4.0, 11.40]
L400_corridor_drip_W:   [-20.30, -4.0, 11.37] → [-20.27, 4.0, 11.40]
```

**Loading Dock Canopy edge drips (C9 — no parapets, drip edge only):**

Canopy slab top Z=5.65. Drip edge on W, N, S faces (not E — abuts logistics hall west wall):
```
L400_canopy_drip_W:   [-28.00, -8.0, 5.62] → [-27.97, 8.0, 5.65]
L400_canopy_drip_N:   [-28.0,  7.97, 5.62] → [-24.0,  8.00, 5.65]
L400_canopy_drip_S:   [-28.0, -8.00, 5.62] → [-24.0, -7.97, 5.65]
```

---

## SECTION 4 — STRUCTURAL CONNECTIONS (L350_Detail)

### 4.1 Column Base Plates

Steel plate: 500mm × 500mm × 25mm (0.5 × 0.5 × 0.025 units)
Z position: [-0.025, 0.0] — plate cast into floor, top flush with finished floor.

**6 main columns (X=[-16, 0, +16] × Y=[+8, -8]):**

```
L350_bp_C1_main_NW:   [-16.25,  7.75, -0.025] → [-15.75,  8.25, 0.0]
L350_bp_C2_main_SW:   [-16.25, -8.25, -0.025] → [-15.75, -7.75, 0.0]
L350_bp_C3_main_NC:   [ -0.25,  7.75, -0.025] → [  0.25,  8.25, 0.0]
L350_bp_C4_main_SC:   [ -0.25, -8.25, -0.025] → [  0.25, -7.75, 0.0]
L350_bp_C5_main_NE:   [ 15.75,  7.75, -0.025] → [ 16.25,  8.25, 0.0]
L350_bp_C6_main_SE:   [ 15.75, -8.25, -0.025] → [ 16.25, -7.75, 0.0]
```

**4 dock columns (X=[-28, -24] × Y=[+8, -8]):**

```
L350_bp_D1_dock_NW:   [-28.25,  7.75, -0.025] → [-27.75,  8.25, 0.0]
L350_bp_D2_dock_SW:   [-28.25, -8.25, -0.025] → [-27.75, -7.75, 0.0]
L350_bp_D3_dock_NE:   [-24.25,  7.75, -0.025] → [-23.75,  8.25, 0.0]
L350_bp_D4_dock_SE:   [-24.25, -8.25, -0.025] → [-23.75, -7.75, 0.0]
```

Note: dock columns are 150mm square but use 500mm base plates for constructability — oversize base plates standard practice for lightly-loaded canopy columns.

**Total: 10 base plate elements**

---

### 4.2 Column Top Bearing Plates

Steel plate: 500mm × 500mm × 20mm (0.5 × 0.5 × 0.02 units)

**6 main columns — top at Z=10.0 (columns run full height to observation corridor roof):**

```
L350_tp_C1_main_NW:   [-16.25,  7.75, 10.0] → [-15.75,  8.25, 10.02]
L350_tp_C2_main_SW:   [-16.25, -8.25, 10.0] → [-15.75, -7.75, 10.02]
L350_tp_C3_main_NC:   [ -0.25,  7.75, 10.0] → [  0.25,  8.25, 10.02]
L350_tp_C4_main_SC:   [ -0.25, -8.25, 10.0] → [  0.25, -7.75, 10.02]
L350_tp_C5_main_NE:   [ 15.75,  7.75, 10.0] → [ 16.25,  8.25, 10.02]
L350_tp_C6_main_SE:   [ 15.75, -8.25, 10.0] → [ 16.25, -7.75, 10.02]
```

Note: plates at Z=[10.0, 10.02] embed 20mm into corridor roof slab (slab bottom at Z=10.0). This is standard bearing plate practice — accepted convention per Lock 01 APPROVED precedent.

**4 dock columns — top at Z=5.5 (canopy height):**

```
L350_tp_D1_dock_NW:   [-28.25,  7.75, 5.5] → [-27.75,  8.25, 5.52]
L350_tp_D2_dock_SW:   [-28.25, -8.25, 5.5] → [-27.75, -7.75, 5.52]
L350_tp_D3_dock_NE:   [-24.25,  7.75, 5.5] → [-23.75,  8.25, 5.52]
L350_tp_D4_dock_SE:   [-24.25, -8.25, 5.5] → [-23.75, -7.75, 5.52]
```

**Total: 10 top plate elements**

---

### 4.3 Cantilever Brackets

Function: local bearing stubs at main column inner faces, supporting observation corridor floor slab edge. Bracket dimensions: 300mm wide (X) × 200mm deep (Z) × 400mm projection from column face (Y direction).

Bracket Z range: [5.8, 6.0] — top at Z=6.0 flush with corridor floor slab bottom.

**Structural interface note — Z=[5.55, 6.0] zone:**
This is the critical zone between logistics hall slab top (Z=5.55) and observation corridor floor (Z=6.0). Gap = 0.45m. In this zone:
- Columns are exposed (no slab, no wall)
- Cantilever brackets occupy Z=[5.8, 6.0] at column faces
- This gap is an intentional reveal — the observation corridor visibly "floats" above the logistics hall roof
- No additional geometry should be added to this zone

**Column faces toward corridor (inner face):**
- N-row columns (Y=+8): inner face at Y=+7.8 (outer face Y=+8.2)
- S-row columns (Y=-8): inner face at Y=-7.8 (outer face Y=-8.2)

Bracket width ±0.15m in X centered on column centers (±0.2 half-width of column; bracket 0.3m wide = center ±0.15):

**North-face brackets (3 brackets, columns C1, C3, C5):**

```
L350_bracket_C1_N:   [-16.15, 7.40, 5.8] → [-15.85, 7.80, 6.0]
L350_bracket_C3_N:   [ -0.15, 7.40, 5.8] → [  0.15, 7.80, 6.0]
L350_bracket_C5_N:   [ 15.85, 7.40, 5.8] → [ 16.15, 7.80, 6.0]
```

**South-face brackets (3 brackets, columns C2, C4, C6):**

```
L350_bracket_C2_S:   [-16.15, -7.80, 5.8] → [-15.85, -7.40, 6.0]
L350_bracket_C4_S:   [ -0.15, -7.80, 5.8] → [  0.15, -7.40, 6.0]
L350_bracket_C6_S:   [ 15.85, -7.80, 5.8] → [ 16.15, -7.40, 6.0]
```

**Total: 6 bracket elements**

Clearance check: Brackets at Z=[5.8,6.0]. Logistics hall insulation assembly top Z=5.725. Gap between assembly top and bracket bottom = 5.8 - 5.725 = 0.075m (75mm clear). Brackets do not contact the roof assembly. ✓

---

## SECTION 5 — FORMWORK LINES (L400_Material)

RC walls cast in 2400mm (2.4 unit) lifts.
Formwork lines: 20mm (0.02) wide × 20mm (0.02) tall thin box, proud of wall outer face by 20mm.
Exposed outer faces only (not interior interfaces between volumes).

**Lift elevations by wall height:**
- Logistics Hall walls (5.0m tall): Z=2.4 only
- Observation Corridor walls (4.0m tall, base Z=6): Z=6+2.4=8.4 only
- Entry/Exit Stair walls (6.0m tall): Z=2.4 only

---

### 5.1 Logistics Hall Formwork Lines (Z=2.4 lift, Z=[2.39, 2.41])

All four outer faces:

```
L400_hall_fw_N_L1:   [-24.0,  11.00, 2.39] → [24.0,  11.02, 2.41]
L400_hall_fw_S_L1:   [-24.0, -11.02, 2.39] → [24.0, -11.00, 2.41]
L400_hall_fw_W_L1:   [-24.02, -11.0, 2.39] → [-24.00, 11.0, 2.41]
L400_hall_fw_E_L1:   [ 24.00, -11.0, 2.39] → [ 24.02, 11.0, 2.41]
```

Total: 4 elements

---

### 5.2 Observation Corridor Formwork Lines (Z=8.4 lift, Z=[8.39, 8.41])

All four outer faces:

```
L400_corridor_fw_N_L1:   [-20.0,  4.30, 8.39] → [20.0,  4.32, 8.41]
L400_corridor_fw_S_L1:   [-20.0, -4.32, 8.39] → [20.0, -4.30, 8.41]
L400_corridor_fw_W_L1:   [-20.32, -4.3, 8.39] → [-20.30, 4.3, 8.41]
L400_corridor_fw_E_L1:   [ 20.30, -4.3, 8.39] → [ 20.32, 4.3, 8.41]
```

Total: 4 elements

---

### 5.3 Entry Stair Formwork Lines (Z=2.4 lift, Z=[2.39, 2.41])

Outer N and S faces only. E face (X=-20) is interior shared wall. W face (X=-24) is continuous with logistics hall west face — covered by hall formwork.

```
L400_entry_stair_fw_N_L1:   [-24.0,  4.30, 2.39] → [-20.0,  4.32, 2.41]
L400_entry_stair_fw_S_L1:   [-24.0, -4.32, 2.39] → [-20.0, -4.30, 2.41]
```

Total: 2 elements

---

### 5.4 Exit Stair Formwork Lines (Z=2.4 lift, Z=[2.39, 2.41])

Outer N and S faces only. W face (X=+20) is interior. E face (X=+24) continuous with logistics hall east face.

```
L400_exit_stair_fw_N_L1:   [20.0,  4.30, 2.39] → [24.0,  4.32, 2.41]
L400_exit_stair_fw_S_L1:   [20.0, -4.32, 2.39] → [24.0, -4.30, 2.41]
```

Total: 2 elements

**Total formwork line elements: 4 + 4 + 2 + 2 = 12**

---

## SECTION 6 — EXPANSION JOINTS (L400_Material)

Logistics Hall 48m long. Joints at X=-8 and X=+8, dividing hall into three ~16m bays aligned with sorting bay separators.
20mm-wide colored solid boxes, continuous through walls AND roof slab.
Assign near-black display color to read as gaps.

**Joint at X=-8:**

```
L400_joint_X-8_wall:   [-8.01, -11.3, 0.0] → [-7.99,  11.3, 5.0]
L400_joint_X-8_slab:   [-8.01, -11.0, 5.0] → [-7.99,  11.0, 5.55]
```

**Joint at X=+8:**

```
L400_joint_X+8_wall:   [7.99, -11.3, 0.0] → [8.01,  11.3, 5.0]
L400_joint_X+8_slab:   [7.99, -11.0, 5.0] → [8.01,  11.0, 5.55]
```

Wall joint Y extent ±11.3 captures full wall thickness (outer face ±11.0 + 300mm wall = ±11.3 needed to penetrate fully). ✓
Slab joint Y extent ±11.0 = slab horizontal extent. ✓

**Total: 4 joint elements**

---

## SECTION 7 — OPENING FRAMES (L350_Detail)

Steel hollow section 100mm × 100mm (0.1 × 0.1 units) framing each opening.
Frame extends 100mm either side of wall face (projects 100mm out and 100mm in).

---

### 7.1 West Truck Bay Frame (X=-24.0 wall)

Opening: Y=[-3.0, 3.0], Z=[0, 4.5] — 6m wide × 4.5m tall.

```
L350_frame_truckbay_top:     [-24.1, -3.0,  4.5] → [-23.9,  3.0, 4.6]
L350_frame_truckbay_bot:     [-24.1, -3.0, -0.1] → [-23.9,  3.0, 0.0]
L350_frame_truckbay_jambN:   [-24.1,  2.9, -0.1] → [-23.9,  3.1, 4.6]
L350_frame_truckbay_jambS:   [-24.1, -3.1, -0.1] → [-23.9, -2.9, 4.6]
```

RC lintel (300mm deep, full opening width + 150mm bearing each side):
```
L350_lintel_truckbay:   [-24.15, -3.0, 4.5] → [-23.85, 3.0, 4.8]
```

---

### 7.2 East Dispatch Frame (X=+24.0 wall)

Opening: Y=[-3.0, 3.0], Z=[0, 4.5] — matching west bay.

```
L350_frame_dispatch_top:     [23.9, -3.0,  4.5] → [24.1,  3.0, 4.6]
L350_frame_dispatch_bot:     [23.9, -3.0, -0.1] → [24.1,  3.0, 0.0]
L350_frame_dispatch_jambN:   [23.9,  2.9, -0.1] → [24.1,  3.1, 4.6]
L350_frame_dispatch_jambS:   [23.9, -3.1, -0.1] → [24.1, -2.9, 4.6]
```

RC lintel:
```
L350_lintel_dispatch:   [23.85, -3.0, 4.5] → [24.15, 3.0, 4.8]
```

---

### 7.3 Observation South Glazing Wall Frame (Y=-4.0 face)

Full glazing band: X=[-20,20], Z=[6.5, 9.5].
Aluminum curtain wall — 50mm (0.05) frame boxes at perimeter.
Frame on corridor wall inner face at Y=-4.0.

```
L350_frame_glazing_top:    [-20.0, -4.05,  9.5] → [20.0, -4.00,  9.6]
L350_frame_glazing_bot:    [-20.0, -4.05,  6.4] → [20.0, -4.00,  6.5]
L350_frame_glazing_jambW:  [-20.05, -4.05, 6.4] → [-20.00, -4.00, 9.6]
L350_frame_glazing_jambE:  [ 20.00, -4.05, 6.4] → [ 20.05, -4.00, 9.6]
```

Note: frame bottom at Z=6.4 provides a 0.5m sill below glazing start Z=6.5. Frame head at Z=9.6 provides 0.4m above glazing top Z=9.5. Both within corridor wall height Z=[6,10]. ✓

---

### 7.4 North Slot Window Frames — 5 windows (Y=+4.0 face)

5 windows, each 2m wide (X=[center-1, center+1]), Z=[7.0, 9.0].
Centers at X = -12, -6, 0, +6, +12.
Frame on corridor wall inner face at Y=+4.0.

**Window N1 — center X=-12:**
```
L350_frame_slot_N1_top:    [-13.0,  4.00, 9.0] → [-11.0,  4.05, 9.1]
L350_frame_slot_N1_bot:    [-13.0,  4.00, 6.9] → [-11.0,  4.05, 7.0]
L350_frame_slot_N1_jambW:  [-13.05, 4.00, 6.9] → [-13.00, 4.05, 9.1]
L350_frame_slot_N1_jambE:  [-11.00, 4.00, 6.9] → [-10.95, 4.05, 9.1]
```

**Window N2 — center X=-6:**
```
L350_frame_slot_N2_top:    [-7.0,  4.00, 9.0] → [-5.0,  4.05, 9.1]
L350_frame_slot_N2_bot:    [-7.0,  4.00, 6.9] → [-5.0,  4.05, 7.0]
L350_frame_slot_N2_jambW:  [-7.05, 4.00, 6.9] → [-7.00, 4.05, 9.1]
L350_frame_slot_N2_jambE:  [-5.00, 4.00, 6.9] → [-4.95, 4.05, 9.1]
```

**Window N3 — center X=0:**
```
L350_frame_slot_N3_top:    [-1.0,  4.00, 9.0] → [1.0,  4.05, 9.1]
L350_frame_slot_N3_bot:    [-1.0,  4.00, 6.9] → [1.0,  4.05, 7.0]
L350_frame_slot_N3_jambW:  [-1.05, 4.00, 6.9] → [-1.00, 4.05, 9.1]
L350_frame_slot_N3_jambE:  [ 1.00, 4.00, 6.9] → [ 1.05, 4.05, 9.1]
```

**Window N4 — center X=+6:**
```
L350_frame_slot_N4_top:    [5.0,  4.00, 9.0] → [7.0,  4.05, 9.1]
L350_frame_slot_N4_bot:    [5.0,  4.00, 6.9] → [7.0,  4.05, 7.0]
L350_frame_slot_N4_jambW:  [4.95, 4.00, 6.9] → [5.00, 4.05, 9.1]
L350_frame_slot_N4_jambE:  [7.00, 4.00, 6.9] → [7.05, 4.05, 9.1]
```

**Window N5 — center X=+12:**
```
L350_frame_slot_N5_top:    [11.0,  4.00, 9.0] → [13.0,  4.05, 9.1]
L350_frame_slot_N5_bot:    [11.0,  4.00, 6.9] → [13.0,  4.05, 7.0]
L350_frame_slot_N5_jambW:  [10.95, 4.00, 6.9] → [11.00, 4.05, 9.1]
L350_frame_slot_N5_jambE:  [13.00, 4.00, 6.9] → [13.05, 4.05, 9.1]
```

All windows within corridor wall bounds Z=[6,10] and X=[-20,20]. ✓

---

### 7.5 Floor Viewing Slot Edge Frames — 3 slots (Z=6 floor)

Slots at X=[-8, 0, +8], Y=[-2, 2], 4m × 4m each.
X extents: Slot 1 at X=[-10,-6], Slot 2 at X=[-2,+2], Slot 3 at X=[+6,+10].
Steel edge frame: 80mm × 80mm (0.08 × 0.08 units) at slot perimeter.
Frame Z=[5.92, 6.00] — embedded in observation corridor floor slab.

**Slot S1 — centered at X=-8 (extent X=[-10,-6]):**
```
L350_slot_frame_S1_N:   [-10.0,  1.92, 5.92] → [-6.0,  2.00, 6.00]
L350_slot_frame_S1_S:   [-10.0, -2.00, 5.92] → [-6.0, -1.92, 6.00]
L350_slot_frame_S1_W:   [-10.08, -2.0, 5.92] → [-10.00, 2.0, 6.00]
L350_slot_frame_S1_E:   [ -6.00, -2.0, 5.92] → [ -5.92, 2.0, 6.00]
```

**Slot S2 — centered at X=0 (extent X=[-2,+2]):**
```
L350_slot_frame_S2_N:   [-2.0,  1.92, 5.92] → [2.0,  2.00, 6.00]
L350_slot_frame_S2_S:   [-2.0, -2.00, 5.92] → [2.0, -1.92, 6.00]
L350_slot_frame_S2_W:   [-2.08, -2.0, 5.92] → [-2.00, 2.0, 6.00]
L350_slot_frame_S2_E:   [ 2.00, -2.0, 5.92] → [ 2.08, 2.0, 6.00]
```

**Slot S3 — centered at X=+8 (extent X=[+6,+10]):**
```
L350_slot_frame_S3_N:   [6.0,  1.92, 5.92] → [10.0,  2.00, 6.00]
L350_slot_frame_S3_S:   [6.0, -2.00, 5.92] → [10.0, -1.92, 6.00]
L350_slot_frame_S3_W:   [5.92,  -2.0, 5.92] → [ 6.00,  2.0, 6.00]
L350_slot_frame_S3_E:   [10.00, -2.0, 5.92] → [10.08,  2.0, 6.00]
```

All slots within corridor floor footprint X=[-20,20], Y=[-4,4]. Slot frames at Z=5.92–6.00 are embedded in the corridor floor slab (corridor volume starts Z=6 — this is the floor structure zone). ✓

**Section 7 total: 5+5 (truck+dispatch) + 4 (glazing) + 20 (slot windows) + 12 (floor slots) = 46 elements**

---

## SECTION 8 — FACADE PANEL JOINTS (L400_Material)

Logistics Hall N and S outer faces: vertical panel joints at X = -16, -8, 0, +8, +16.
5mm wide in X (0.005 units) × 20mm deep in Y (0.02 units) incised boxes.
Full wall height Z=[0, 5.0].

N outer face at Y=+11.0, joint depth from outer face inward (toward Y=+10.98):

```
L400_pj_hall_N_X-16:   [-16.005, 10.98, 0.0] → [-16.000, 11.00, 5.0]
L400_pj_hall_N_X-8:    [ -8.005, 10.98, 0.0] → [ -8.000, 11.00, 5.0]
L400_pj_hall_N_X0:     [ -0.005, 10.98, 0.0] → [  0.000, 11.00, 5.0]
L400_pj_hall_N_X+8:    [  7.995, 10.98, 0.0] → [  8.000, 11.00, 5.0]
L400_pj_hall_N_X+16:   [ 15.995, 10.98, 0.0] → [ 16.000, 11.00, 5.0]
```

S outer face at Y=-11.0, joint depth from outer face inward (toward Y=-10.98):

```
L400_pj_hall_S_X-16:   [-16.005, -11.00, 0.0] → [-16.000, -10.98, 5.0]
L400_pj_hall_S_X-8:    [ -8.005, -11.00, 0.0] → [ -8.000, -10.98, 5.0]
L400_pj_hall_S_X0:     [ -0.005, -11.00, 0.0] → [  0.000, -10.98, 5.0]
L400_pj_hall_S_X+8:    [  7.995, -11.00, 0.0] → [  8.000, -10.98, 5.0]
L400_pj_hall_S_X+16:   [ 15.995, -11.00, 0.0] → [ 16.000, -10.98, 5.0]
```

**Total: 10 facade panel joint elements**

---

## EXECUTION SUMMARY

### Element count

| Section | Type | Layer | Count |
|---------|------|-------|-------|
| 1.1 | Logistics Hall Roof Slab | L300_Roof | 1 |
| 1.2 | Logistics Hall Parapets | L300_Roof | 4 |
| 1.3 | Observation Corridor Roof Slab | L300_Roof | 1 |
| 1.4 | Observation Corridor Parapets | L300_Roof | 4 |
| 1.5 | Loading Dock Canopy Roof Slab | L300_Roof | 1 |
| **L300_Roof subtotal** | | | **11** |
| 2.1 | Logistics Hall Roof Assembly | L400_Material | 3 |
| 2.2 | Observation Corridor Roof Assembly | L400_Material | 3 |
| 2.3 | Canopy Roof Assembly | L400_Material | 3 |
| 3.1 | Waterproofing Upstands (hall 4 + corridor 4) | L400_Material | 8 |
| 3.2 | Drip Edges (hall 4 + corridor 4 + canopy 3) | L400_Material | 11 |
| 5.1 | Logistics Hall Formwork Lines | L400_Material | 4 |
| 5.2 | Observation Corridor Formwork Lines | L400_Material | 4 |
| 5.3 | Entry Stair Formwork Lines | L400_Material | 2 |
| 5.4 | Exit Stair Formwork Lines | L400_Material | 2 |
| 6 | Expansion Joints | L400_Material | 4 |
| 8 | Facade Panel Joints | L400_Material | 10 |
| **L400_Material subtotal** | | | **54** |
| 4.1 | Column Base Plates (6 main + 4 dock) | L350_Detail | 10 |
| 4.2 | Column Top Bearing Plates (6 main + 4 dock) | L350_Detail | 10 |
| 4.3 | Cantilever Brackets | L350_Detail | 6 |
| 7.1 | West Truck Bay Frame + Lintel | L350_Detail | 5 |
| 7.2 | East Dispatch Frame + Lintel | L350_Detail | 5 |
| 7.3 | South Glazing Wall Frame | L350_Detail | 4 |
| 7.4 | North Slot Window Frames (5 windows × 4) | L350_Detail | 20 |
| 7.5 | Floor Viewing Slot Edge Frames (3 slots × 4) | L350_Detail | 12 |
| **L350_Detail subtotal** | | | **72** |
| **GRAND TOTAL** | | | **137** |

Note: 137 vs 134 in draft — correction accounts for 3 additional canopy drip edges (C9 addition).

---

## BUILD ORDER

1. Create 3 new layers: L300_Roof, L350_Detail, L400_Material
2. Logistics Hall roof slab — 1 box (L300_Roof)
3. Logistics Hall parapets — 4 boxes (L300_Roof)
4. Observation Corridor roof slab — 1 box (L300_Roof)
5. Observation Corridor parapets — 4 boxes (L300_Roof)
6. Loading Dock Canopy roof slab — 1 box (L300_Roof)
7. Roof assembly layers — 9 boxes total, all 3 zones (L400_Material) — batch one script
8. Waterproofing upstands — 8 boxes (L400_Material)
9. Drip edges — 11 boxes (L400_Material)
10. Column base plates — 10 boxes (L350_Detail) — batch
11. Column top bearing plates — 10 boxes (L350_Detail) — batch
12. Cantilever brackets — 6 boxes (L350_Detail)
13. Formwork lines — 12 boxes total (L400_Material) — batch one script
14. Expansion joints — 4 boxes (L400_Material)
15. West truck bay and east dispatch frames + lintels — 10 boxes (L350_Detail)
16. South glazing wall frame — 4 boxes (L350_Detail)
17. North slot window frames — 20 boxes (L350_Detail) — batch one script
18. Floor viewing slot edge frames — 12 boxes (L350_Detail) — batch one script
19. Facade panel joints — 10 boxes (L400_Material)

---

## EXECUTOR NOTES

1. All coordinates are meter-scale in a centimeter-unit Rhino doc. Use numbers exactly as written.
2. Do NOT multiply by 100.
3. Use `rhino_execute_python_code` with `Box()` (BoundingBox from two corner points) for all elements.
4. Batch by section — formwork lines in one script, base plates in one script, etc.
5. If a boolean or complex operation fails, fall back to additive geometry only and note it.
6. After all geometry is placed: capture Perspective, Top, Front, and Section (Y=0 cut) viewports.
7. Target instance: `lock_02` (port 9002). All MCP calls must include `target: "lock_02"`.
8. The structural zone Z=[5.55, 6.0] is the intentional reveal gap between logistics hall roof and observation corridor floor. Only the 6 cantilever bracket stubs occupy this zone — no other geometry should be placed here.
9. Floor viewing slot frames at Z=[5.92, 6.0] are embedded in the observation corridor floor slab. They are at the corridor level, not in the logistics hall.
10. Expansion joint boxes at X=±8 use near-black display color. Set object display color override, not layer color.
11. Building extents for reference: X=[-28, 24], Y=[-11, 11], Z=[0, 11.4] (parapet top). Dock canopy extends to X=-28.

---

## DECISION LOG

| Decision | Verdict | Rationale |
|----------|---------|-----------|
| Logistics hall slab system | 550mm flat slab | Heavy industrial loads + span/30 = 533mm. "Flat box" modeling instruction honored. |
| Logistics hall slab continuity | Continuous, no cutout at columns | Standard RC construction — columns penetrate slab. |
| Hall parapet height | 1100mm | SIA 358 minimum 1070mm + 30mm margin. Parapet top Z=6.65. |
| Hall inner parapets at observation corridor edge | None | Drop from Z=5.55 to adjacent Z=6.0 corridor floor = +0.45m (ascending). Not a fall condition. |
| Observation corridor parapet — all 4 faces | 4 parapets including west | West face at Z=10 is a free edge (4m drop to corridor floor Z=6). Safety requires parapet. Stair abutment at Z=6 does not affect roof level. |
| Canopy parapet | None — drip edge only | Non-public industrial roof. Not publicly accessible. |
| Cantilever bracket type | Bearing stub (0.4m projection) | 4m corridor cantilever carried by floor slab structure. Brackets = local bearing shelf at column face. |
| Column top plates | At Z=10.0 (embed 20mm into slab) | Standard bearing plate convention; precedent from Lock 01 APPROVED. |
| Dock column base plates | 500mm (oversize) | Standard constructability practice for light canopy columns. |
| Formwork lift elevations | Hall: Z=2.4; Corridor: Z=8.4; Stairs: Z=2.4 | 2400mm standard form height. Corridor base at Z=6, so lift at 6+2.4=8.4. |
| Stair formwork lines | Include N/S outer faces | Stair volumes are exterior-facing on N/S faces — exposed faces require formwork representation. |
| Expansion joints | X=-8 and X=+8, through wall AND slab | Structural continuity required. 16m bays match sorting bay separators. |
| Facade panel joints | 5 joints per N/S face at column grid lines | Column grid lines (X=±16, ±8, 0) plus midpoints (±8) match structural bay logic. |
| Z=[5.55, 6.0] structural zone | Intentional reveal — no infill geometry | This gap is the architectural moment: the corridor visibly floats over the logistics hall. Only bracket stubs occupy this zone. |
| Coordinate system | Meter-scale throughout | Match existing model. No ×100 conversion. |
