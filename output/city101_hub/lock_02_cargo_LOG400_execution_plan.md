# Lock Type 02 — Cargo Lock
# LOG400 Upgrade: Execution Specification
# Status: DRAFT FOR ROUNDTABLE REVIEW — do NOT execute until approved
# Authored by: Design Architect Agent
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
- 6 main columns: X=[-16, 0, +16] × Y=[+8, -8], 400mm × 400mm (0.4 × 0.4 units), Z=[0, 10]
- 4 dock columns: X=[-28, -24] × Y=[+8, -8], 150mm × 150mm (0.15 × 0.15 units), Z=[0, 5.5]

**Observation corridor beams:** longitudinal at Y=±4, Z=6, spanning X=[-20, 20]

---

## LAYERS TO CREATE

```
Type_02_Cargo::L300_Roof     — RGB(200, 155, 100)  — roof slabs, parapets
Type_02_Cargo::L350_Detail   — RGB(160, 115, 70)   — connections, frames, brackets
Type_02_Cargo::L400_Material — RGB(120, 85, 50)    — formwork, joints, hardware, edge conditions
```

Do NOT rename or alter existing layers:
- `Type_02_Cargo::Volumes`
- `Type_02_Cargo::Circulation`
- `Type_02_Cargo::Structure`
- `Type_02_Cargo::Openings`
- `Type_02_Cargo::Annotations`

---

## SECTION 1 — ROOF SYSTEM (L300_Roof)

### Slab thickness rationale

**Logistics Hall:**
- Primary span: column-to-column across Y, from Y=-8 to Y=+8 = 16m clear span
- Cantilever: from column at Y=±8 to wall at Y=±11 = 3m overhang
- Governing span: 16m primary → span/30 = 533mm → use 550mm (0.55 units)
- Secondary consideration: the span/20 rule for two-way RC slabs at 16m gives 800mm — but the slab is beam-supported at Y=±4 and Y=±8 columns, making the effective span ≈ 8m. Corrected: 8m effective span → span/30 = 267mm → use 300mm (0.3 units) for the beam-and-slab system. Beams carry the 16m span; the slab infills between beams.
- [FLAG 1: Structural system choice — if the logistics hall roof is a FLAT SLAB (no downstand beams, modeled as flat box), the effective span is 16m and the slab needs 550mm. If it is a BEAM+SLAB system (concealed upstand beams cast with slab), effective slab span is 8m and slab can be 300mm. The concept prompt says "model as flat box" — defaulting to 550mm flat slab pending reviewer decision.]
- Using 550mm (0.55 units) for flat slab interpretation.

**Observation Corridor:**
- Span: Y=-4 to Y=+4 = 8m
- span/30 = 267mm → use 300mm (0.3 units)

**Loading Dock Canopy:**
- Short span: 4m (X direction, columns at X=-28 and X=-24)
- span/30 = 133mm → use 150mm (0.15 units)

**Bearing rule:** All slabs sit ON TOP of existing wall shells. Slab bottom face = top of walls.

---

### 1.1 Logistics Hall Roof Slab

Layer: `Type_02_Cargo::L300_Roof`
Name: `L300_hall_roof_slab`

Logistics Hall walls: outer face Y=±11 (N/S walls), outer face X=±24 (E/W walls).
Slab bearing on wall tops at Z=5. Slab extends over full hall footprint.

```
Corner A: [-24.0, -11.0, 5.0]
Corner B: [ 24.0,  11.0, 5.55]
```
Thickness: 0.55 units (550mm)
Bottom face at Z=5.0 (bearing on existing 5.0m walls)
Top face at Z=5.55

Drainage: 1.5% fall south (toward Y=-11). Drop = 22.0 × 0.015 = 0.33 units over full Y span.
Modeled as flat box at LOG400. Annotate fall direction as text dot on Annotations layer.

Note: The observation corridor (Z=[6,10]) sits on the inner portion (Y=[-4,4], X=[-20,20]). The logistics hall slab does NOT extend under the observation corridor — the observation corridor is structurally independent, bearing on columns that run Z=[0,10]. The logistics hall slab bears on perimeter walls and columns at Y=±8.

[FLAG 2: Logistics hall slab cutout — the slab as specified covers the full footprint [-24,24] × [-11,11]. However, the observation corridor columns at Y=±8 penetrate through this zone, and the corridor floor at Z=6 is 0.45m above slab top (Z=5.55). Should the slab have a cutout at the column locations (columns are already modeled as separate objects), or is it modeled as a continuous slab with columns passing through? Recommendation: model as continuous slab (no cutout). Columns penetrate slab — standard RC construction. Pending reviewer confirmation.]

---

### 1.2 Logistics Hall Parapets

Parapet height determination:
- Outer perimeter (N, S, E, W faces): drop from roof (Z=5.55) to ground = 5.55m > 1m → SIA 358 requires ≥ 1070mm parapet. Using 1100mm (1.1 units) above slab top.
- Inner perimeter at Y=±4 face (where observation corridor begins): this is the inner edge of the logistics hall roof where it meets the observation corridor underside. No parapet needed here — the observation corridor volume occupies this space from Z=6 upward. However the gap between Z=5.55 (slab top) and Z=6 (corridor floor) = 0.45m is a void — no parapet needed at this interface because the corridor structure fills it.

[FLAG 3: Parapet at X=±20 (logistics hall E/W inner face at observation corridor ends): the logistics hall slab extends to X=±24. Between X=±20 and X=±24, the roof is exposed (no observation corridor above). The N and S outer parapets already cover this. The inner face at X=±20 (where observation corridor ends) is an exposed edge from slab top (Z=5.55) to corridor floor (Z=6) — a 0.45m drop which is below the 1m SIA 358 threshold. No parapet required at X=±20 inner face. Confirm with reviewer.]

Parapet top Z = 5.55 + 1.1 = 6.65
Parapet Z range: [5.55, 6.65]
Parapet thickness: 0.3 units (300mm), matching wall thickness

Outer N parapet (full hall length, exposed to drop):
```
L300_hall_parapet_N:   [-24.0, 10.7, 5.55] → [24.0, 11.0, 6.65]
```

Outer S parapet (full hall length):
```
L300_hall_parapet_S:   [-24.0, -11.0, 5.55] → [24.0, -10.7, 6.65]
```

West parapet (between N and S outer parapets):
Note: X=-24 face is the truck bay wall (with large openings at Y=[-3,3]). The roof parapet sits above the wall top at Z=5.55. Parapet runs full Y extent.
```
L300_hall_parapet_W:   [-24.0, -10.7, 5.55] → [-23.7, 10.7, 6.65]
```

East parapet (dispatch face):
Note: X=+24 face similarly has a dispatch opening below. Parapet above.
```
L300_hall_parapet_E:   [23.7, -10.7, 5.55] → [24.0, 10.7, 6.65]
```

Note on parapet conflict with observation corridor parapets: the logistics hall parapets top at Z=6.65. The observation corridor floor is at Z=6. The observation corridor volume occupies Y=[-4,4], X=[-20,20], Z=[6,10]. The logistics hall parapets are at Y=±11 and X=±24 — no geometry conflict. The inner face of the N and S parapets is at Y=±10.7, well clear of the corridor at Y=±4.

**Total parapet elements: 4**

---

### 1.3 Observation Corridor Roof Slab

Layer: `Type_02_Cargo::L300_Roof`
Name: `L300_corridor_roof_slab`

Observation corridor walls top at Z=10. Slab bears on wall tops.
Corridor wall outer faces: Y=±4 + 0.3 = Y=±4.3 (N and S outer faces); X=±20 + 0.3 = X=±20.3 (E and W outer faces).

Wait — check: the base volume is X=[-20,20] × Y=[-4,4] × Z=[6,10]. Wall thickness 0.3 units. Inner faces at Y=±3.7, X=±19.7. Outer faces at Y=±4.3, X=±20.3.

```
Corner A: [-20.0, -4.0, 10.0]
Corner B: [ 20.0,  4.0, 10.3]
```
Thickness: 0.3 units (300mm)
Bottom face at Z=10.0 (bearing on existing 10.0m walls)
Top face at Z=10.3

Note: The slab aligns with the volume outer edges (the walls form the perimeter, the slab caps the volume). The slab extends to the outer wall faces to cap the full assembly.

```
Corner A: [-20.3, -4.3, 10.0]
Corner B: [ 20.3,  4.3, 10.3]
```
Thickness: 0.3 units (300mm), lightweight public corridor slab.

Drainage: 1.5% fall north (toward Y=+4.3). Drop = 8.6 × 0.015 = 0.13 units over Y span.
Modeled as flat box. Annotate fall direction.

---

### 1.4 Observation Corridor Parapets

Parapet height: ≥ 1070mm (SIA 358 — publicly accessible roof, drop > 1m to logistics hall roof and beyond). Using 1100mm (1.1 units).
Parapet top Z = 10.3 + 1.1 = 11.4
Parapet Z range: [10.3, 11.4]
Parapet thickness: 0.3 units

N face parapet (exposed exterior — drop to logistics hall roof 5.55m below):
```
L300_corridor_parapet_N:   [-20.0, 4.0, 10.3] → [20.0, 4.3, 11.4]
```

S face parapet (exposed glazed face — drop to logistics hall roof):
```
L300_corridor_parapet_S:   [-20.0, -4.3, 10.3] → [20.0, -4.0, 11.4]
```

E face parapet (east end — abuts Exit Stair volume top at Z=6, but stair is only at Z=[0,6] and stair is at X=[20,24]. The corridor east wall is at X=+20. The stair is east of the corridor at X=[20,24]. No conflict — parapet on east face of corridor is free):
```
L300_corridor_parapet_E:   [20.0, -4.0, 10.3] → [20.3, 4.0, 11.4]
```

W face: abuts Entry Stair volume at X=-24 to -20, Y=[-4,4], Z=[0,6]. The stair top is at Z=6 which is the corridor floor — the stair volume meets the corridor floor. The corridor west wall is at X=-20. No conflict at roof level (Z=10). Add west parapet:
```
L300_corridor_parapet_W:   [-20.3, -4.0, 10.3] → [-20.0, 4.0, 11.4]
```

[FLAG 4: Observation corridor west parapet — the concept prompt states "West face abuts Entry Stair top." The stair top is at Z=6 (ground-to-corridor connection). At roof level (Z=10), there is no abutment — the stair does not reach Z=10. The west face is therefore open to sky above Z=6 from the stair landing. A parapet on the west face of the corridor at Z=[10.3,11.4] is structurally and safely correct. However, the Phase 1 spec briefing says "no parapet on west face." Verify whether this refers to the corridor roof west parapet or just the wall opening. Defaulting to including all 4 parapets for safety. Reviewer to confirm or remove west parapet.]

**Total corridor parapet elements: 4**

---

### 1.5 Loading Dock Canopy Roof Slab

Layer: `Type_02_Cargo::L300_Roof`
Name: `L300_canopy_roof_slab`

Canopy volume Z=[3, 5.5]. Slab sits ON TOP of canopy volume at Z=5.5.
Canopy volume: X=[-28,-24] × Y=[-8,8]. Canopy wall/structure outer faces: Y=±8 (canopy columns are at Y=±8, X=[-28,-24]).

```
Corner A: [-28.0, -8.0, 5.5]
Corner B: [-24.0,  8.0, 5.65]
```
Thickness: 0.15 units (150mm)
Bottom face at Z=5.5 (bearing on top of canopy structure)
Top face at Z=5.65

Drainage: 1.5% fall south. Drop = 16.0 × 0.015 = 0.24 units over 16m Y span.
Modeled as flat box. Annotate drainage direction as text dot.

Note: The canopy slab abuts the logistics hall west wall (X=-24). No parapet at X=-24 face (interior building face). Add parapet on W, N, S faces (exposed exterior) where drop from Z=5.65 to ground > 1m. However, the canopy slab is at Z=5.65 and trucks pass under it — this is not a publicly accessible roof. No parapet required at the canopy level per operational use. Add a nominal edge drip only.

[FLAG 5: Canopy parapet — the canopy slab is at Z=5.65, nominally accessible only for maintenance. Drop to ground = 5.65m > 1m. SIA 358 requires parapet if it is accessible. If canopy is not publicly accessible (logical given truck operations), a drip edge only suffices. Defaulting to NO parapet on canopy — edge drip only via L400_Material. Reviewer to confirm.]

---

## SECTION 2 — ROOF ASSEMBLY LAYERS (L400_Material)

Three-layer build-up inside parapets on top of each roof slab.
Layers: 120mm XPS insulation + 5mm waterproofing membrane + 50mm gravel ballast = 175mm = 0.175 units.

---

### 2.1 Logistics Hall Roof Assembly

Slab top: Z=5.55
Parapet inner faces: N at Y=+10.7, S at Y=-10.7, W at X=-23.7, E at X=+23.7
Assembly bounded by parapet inner faces.
Assembly top: Z = 5.55 + 0.175 = 5.725

```
L400_hall_insulation:   [-23.7, -10.7, 5.550] → [23.7, 10.7, 5.670]   (120mm)
L400_hall_membrane:     [-23.7, -10.7, 5.670] → [23.7, 10.7, 5.675]   (5mm)
L400_hall_gravel:       [-23.7, -10.7, 5.675] → [23.7, 10.7, 5.725]   (50mm)
```

Note: These extend under the observation corridor footprint (X=[-20,20], Y=[-4,4]). The observation corridor structure sits on columns, not on the logistics hall slab or its assembly. The insulation/membrane/gravel fill the full logistics hall roof — including under the corridor. This is the correct thermal envelope condition: the logistics hall roof is fully insulated across its entire area.

---

### 2.2 Observation Corridor Roof Assembly

Slab top: Z=10.3
Parapet inner faces: N at Y=+4.0, S at Y=-4.0, E at X=+20.0, W at X=-20.0
Assembly top: Z = 10.3 + 0.175 = 10.475

```
L400_corridor_insulation:   [-20.0, -4.0, 10.300] → [20.0, 4.0, 10.420]   (120mm)
L400_corridor_membrane:     [-20.0, -4.0, 10.420] → [20.0, 4.0, 10.425]   (5mm)
L400_corridor_gravel:       [-20.0, -4.0, 10.425] → [20.0, 4.0, 10.475]   (50mm)
```

---

### 2.3 Loading Dock Canopy Assembly

Slab top: Z=5.65
Canopy has no parapets (FLAG 5 — maintenance roof). Assembly fills full canopy slab area.
Assembly top: Z = 5.65 + 0.175 = 5.825

```
L400_canopy_insulation:   [-28.0, -8.0, 5.650] → [-24.0, 8.0, 5.770]   (120mm)
L400_canopy_membrane:     [-28.0, -8.0, 5.770] → [-24.0, 8.0, 5.775]   (5mm)
L400_canopy_gravel:       [-28.0, -8.0, 5.775] → [-24.0, 8.0, 5.825]   (50mm)
```

---

## SECTION 3 — PARAPET EDGE CONDITIONS (L400_Material)

### 3.1 Waterproofing Upstands

20mm wide × 150mm tall box against inner face of each parapet, at base of parapet (slab top level).

**Logistics Hall parapets (slab top Z=5.55, upstand Z=[5.55, 5.70]):**

```
L400_hall_upstand_N:   [-23.7, 10.68, 5.55] → [23.7, 10.70, 5.70]
L400_hall_upstand_S:   [-23.7, -10.70, 5.55] → [23.7, -10.68, 5.70]
L400_hall_upstand_W:   [-23.72, -10.7, 5.55] → [-23.70, 10.7, 5.70]
L400_hall_upstand_E:   [23.70, -10.7, 5.55] → [23.72, 10.7, 5.70]
```

**Observation Corridor parapets (slab top Z=10.3, upstand Z=[10.3, 10.45]):**

```
L400_corridor_upstand_N:   [-20.0, 3.98, 10.30] → [20.0, 4.00, 10.45]
L400_corridor_upstand_S:   [-20.0, -4.00, 10.30] → [20.0, -3.98, 10.45]
L400_corridor_upstand_E:   [19.98, -4.0, 10.30] → [20.00, 4.0, 10.45]
L400_corridor_upstand_W:   [-20.00, -4.0, 10.30] → [-19.98, 4.0, 10.45]
```

### 3.2 Drip Edges

30mm × 20mm box at outer top corner of each parapet.

**Logistics Hall parapets (parapet top Z=6.65):**

```
L400_hall_drip_N:   [-23.7, 10.97, 6.62] → [23.7, 11.00, 6.65]
L400_hall_drip_S:   [-23.7, -11.00, 6.62] → [23.7, -10.97, 6.65]
L400_hall_drip_W:   [-24.00, -10.7, 6.62] → [-23.97, 10.7, 6.65]
L400_hall_drip_E:   [23.97, -10.7, 6.62] → [24.00, 10.7, 6.65]
```

**Observation Corridor parapets (parapet top Z=11.4):**

```
L400_corridor_drip_N:   [-20.0, 4.27, 11.37] → [20.0, 4.30, 11.40]
L400_corridor_drip_S:   [-20.0, -4.30, 11.37] → [20.0, -4.27, 11.40]
L400_corridor_drip_E:   [20.27, -4.0, 11.37] → [20.30, 4.0, 11.40]
L400_corridor_drip_W:   [-20.30, -4.0, 11.37] → [-20.27, 4.0, 11.40]
```

---

## SECTION 4 — STRUCTURAL CONNECTIONS (L350_Detail)

### 4.1 Column Base Plates

Steel plate: 500mm × 500mm × 25mm (0.5 × 0.5 × 0.025 units)
Z position: [-0.025, 0] (plate cast into floor, top flush with finished floor)

**6 main columns at X=[-16, 0, +16] × Y=[+8, -8]:**

| Column ID | Label | X center | Y center |
|-----------|-------|----------|----------|
| C1 | Main NW | -16.0 | +8.0 |
| C2 | Main SW | -16.0 | -8.0 |
| C3 | Main NC | 0.0 | +8.0 |
| C4 | Main SC | 0.0 | -8.0 |
| C5 | Main NE | +16.0 | +8.0 |
| C6 | Main SE | +16.0 | -8.0 |

```
L350_bp_C1_main_NW:   [-16.25,  7.75, -0.025] → [-15.75,  8.25, 0.0]
L350_bp_C2_main_SW:   [-16.25, -8.25, -0.025] → [-15.75, -7.75, 0.0]
L350_bp_C3_main_NC:   [ -0.25,  7.75, -0.025] → [  0.25,  8.25, 0.0]
L350_bp_C4_main_SC:   [ -0.25, -8.25, -0.025] → [  0.25, -7.75, 0.0]
L350_bp_C5_main_NE:   [ 15.75,  7.75, -0.025] → [ 16.25,  8.25, 0.0]
L350_bp_C6_main_SE:   [ 15.75, -8.25, -0.025] → [ 16.25, -7.75, 0.0]
```

**4 dock columns at X=[-28, -24] × Y=[+8, -8], 150mm × 150mm:**

| Column ID | Label | X center | Y center |
|-----------|-------|----------|----------|
| D1 | Dock NW | -28.0 | +8.0 |
| D2 | Dock SW | -28.0 | -8.0 |
| D3 | Dock NE | -24.0 | +8.0 |
| D4 | Dock SE | -24.0 | -8.0 |

```
L350_bp_D1_dock_NW:   [-28.25,  7.75, -0.025] → [-27.75,  8.25, 0.0]
L350_bp_D2_dock_SW:   [-28.25, -8.25, -0.025] → [-27.75, -7.75, 0.0]
L350_bp_D3_dock_NE:   [-24.25,  7.75, -0.025] → [-23.75,  8.25, 0.0]
L350_bp_D4_dock_SE:   [-24.25, -8.25, -0.025] → [-23.75, -7.75, 0.0]
```

Note: dock column base plates use same 500×500×25mm steel plate for constructability (oversize relative to 150mm column — standard practice for light canopy columns).

**Total base plates: 10 elements**

---

### 4.2 Column Top Bearing Plates

Steel plate: 500mm × 500mm × 20mm (0.5 × 0.5 × 0.02 units)

**Main columns: full height Z=[0,10] — top plates at Z=10.0:**

```
L350_tp_C1_main_NW:   [-16.25,  7.75, 10.0] → [-15.75,  8.25, 10.02]
L350_tp_C2_main_SW:   [-16.25, -8.25, 10.0] → [-15.75, -7.75, 10.02]
L350_tp_C3_main_NC:   [ -0.25,  7.75, 10.0] → [  0.25,  8.25, 10.02]
L350_tp_C4_main_SC:   [ -0.25, -8.25, 10.0] → [  0.25, -7.75, 10.02]
L350_tp_C5_main_NE:   [ 15.75,  7.75, 10.0] → [ 16.25,  8.25, 10.02]
L350_tp_C6_main_SE:   [ 15.75, -8.25, 10.0] → [ 16.25, -7.75, 10.02]
```

**Dock columns: top at Z=5.5 (canopy height):**

```
L350_tp_D1_dock_NW:   [-28.25,  7.75, 5.5] → [-27.75,  8.25, 5.52]
L350_tp_D2_dock_SW:   [-28.25, -8.25, 5.5] → [-27.75, -7.75, 5.52]
L350_tp_D3_dock_NE:   [-24.25,  7.75, 5.5] → [-23.75,  8.25, 5.52]
L350_tp_D4_dock_SE:   [-24.25, -8.25, 5.5] → [-23.75, -7.75, 5.52]
```

Note on main columns: the brief specifies main columns run Z=[0,10]. The column top plates at Z=10 sit just below the observation corridor roof slab (bottom at Z=10.0). The bearing plate transfers slab load to column. Columns also support logistics hall slab at Z=5 and corridor beams at Z=6 — these intermediate loads are transmitted by column continuity, no additional plates needed at Z=5 or Z=6 for the box model.

**Total top plates: 10 elements**

---

### 4.3 Cantilever Brackets

The observation corridor (Y=[-4,4]) cantilevers 4m from the main columns (Y=±8) to its edges (Y=±4). Brackets support the corridor overhang at each main column location.

Bracket design: 300mm wide (Y) × 200mm deep (Z) × 400mm projection from column face (X/Y horizontal)
In model units: 0.3 (width) × 0.2 (depth) × 0.4 (projection)

Bracket Z range: [5.8, 6.0] — bracket top at Z=6.0 (flush with corridor floor slab bottom)
Bracket attaches to column inner face (face closest to corridor centerline):
- North columns (Y=+8): inner face at Y=+7.8, bracket projects SOUTH toward Y=+4
- South columns (Y=-8): inner face at Y=-7.8, bracket projects NORTH toward Y=-4

**North-face brackets (6 locations — 3 X positions × N face):**

At X=-16 (columns C1):
```
L350_bracket_C1_N:   [-16.15, 7.4, 5.8] → [15.85, 7.8, 6.0]
```

[FLAG 6: Bracket geometry re-check. The bracket projects FROM the column inner face (at Y=7.8 for north columns) TOWARD the corridor edge (Y=+4). Projection = 7.8 - 4.0 = 3.8m — too large for a bracket. This is a 3.8m cantilever off the column face, not a 400mm bracket. The 4m overhang (from column center at Y=8 to corridor edge at Y=4) means the bracket must span the full 4m. This is a large cantilever beam element, not a typical bracket. Options: (a) a 400mm deep × 300mm wide RC cantilever beam projecting 4m from column face — much heavier than specified; (b) the observation corridor beams at Y=±4 are the cantilevering elements, spanning from column to column at Z=6, and brackets at column faces are just local connection plates. Defaulting to interpretation (b): the observation corridor beams at Y=±4 Z=6 are the primary structure, spanning X=[-20,20]. The "cantilever" from column at Y=±8 to beam at Y=±4 is NOT a bracket but rather the beam overhangs the column grid. The bracket in the spec is a local bearing stub at the column face. Modeled as spec says: 300mm×200mm×400mm projection stub at each column face, at Z=5.8–6.0. This is a bearing shelf for the corridor floor slab edge, not the primary spanning element.]

Corrected bracket interpretation: bracket is a bearing stub at each main column inner face, supporting the corridor slab edge. 6 brackets on north column faces (Y=+8 inner face at Y=+7.8), 6 on south column faces (Y=-8 inner face at Y=-7.8). Actually there are 3 X positions × 2 sides = 6 total brackets.

Bracket center in Y: projects 0.4 toward corridor from column face.
- North columns (inner face at Y=+7.8): bracket extends from Y=7.4 to Y=7.8
- South columns (inner face at Y=-7.8): bracket extends from Y=-7.8 to Y=-7.4

Bracket width in X: 300mm centered on column center (column ±0.15 from center in X since column is 0.4 wide, center ±0.2; bracket 0.3 wide = ±0.15).

**North-face brackets at Y=+8 columns:**

Column C1 (X=-16, inner face Y=7.8):
```
L350_bracket_C1_N:   [-16.15, 7.40, 5.8] → [-15.85, 7.80, 6.0]
```

Column C3 (X=0, inner face Y=7.8):
```
L350_bracket_C3_N:   [-0.15, 7.40, 5.8] → [0.15, 7.80, 6.0]
```

Column C5 (X=+16, inner face Y=7.8):
```
L350_bracket_C5_N:   [15.85, 7.40, 5.8] → [16.15, 7.80, 6.0]
```

**South-face brackets at Y=-8 columns:**

Column C2 (X=-16, inner face Y=-7.8):
```
L350_bracket_C2_S:   [-16.15, -7.80, 5.8] → [-15.85, -7.40, 6.0]
```

Column C4 (X=0, inner face Y=-7.8):
```
L350_bracket_C4_S:   [-0.15, -7.80, 5.8] → [0.15, -7.40, 6.0]
```

Column C6 (X=+16, inner face Y=-7.8):
```
L350_bracket_C6_S:   [15.85, -7.80, 5.8] → [16.15, -7.40, 6.0]
```

**Total bracket elements: 6**

Note: Brackets do not penetrate the logistics hall slab at Z=5.55 (brackets are at Z=[5.8,6.0], above the slab top). Structurally, the 0.25m gap between slab top (Z=5.55) and bracket bottom (Z=5.8) is the column zone between logistics hall roof and corridor floor. This is the critical Z=[5,6] structural interface.

---

## SECTION 5 — FORMWORK LINES (L400_Material)

RC walls cast in 2400mm (2.4 unit) lifts.
Formwork lift lines = thin horizontal box proud of wall face by 20mm (0.02 units), 20mm tall.
Wall thickness: 300mm (0.3 units).

**Wall outer faces:**
- Logistics Hall N/S walls: outer face at Y=±11
- Logistics Hall E/W walls: outer face at X=±24
- Observation Corridor N/S walls: outer face at Y=±4.3
- Observation Corridor E/W walls: outer face at X=±20.3
- Entry/Exit Stair E/W walls: outer face at X=-24 and X=-20 (entry), X=+20 and X=+24 (exit). The X=-24 and X=+24 faces are shared with logistics hall wall — no separate formwork.

**Lift elevations:**

Logistics Hall walls (5m tall): one lift at Z=2.4
Observation Corridor walls (4m tall, Z=[6,10]): one lift at Z=8.4 (2.4m above base at Z=6)
Entry/Exit Stair walls (6m tall, Z=[0,6]): one lift at Z=2.4

Note: Stair outer faces. Entry stair: W face at X=-24 (shared with logistics hall W wall outer — logistics hall lift at Z=2.4 covers this), N face at Y=+4.3 (but wait — stair volume is Y=[-4,4] with wall thickness → outer N face at Y=+4.3, outer S face at Y=-4.3), W face at X=-24.3. However, the stair X=-24 face is the same as the logistics hall west face — already covered. The stair north face (Y=+4.3 inner portion from X=-24 to X=-20) is distinct.

For stair volumes: exposed outer faces only — not the faces that share with logistics hall or observation corridor.

**Entry Stair (X=[-24,-20], Y=[-4,4], Z=[0,6], walls 0.3 thick):**
- Outer west face (X=-24.3): this is continuous with logistics hall west wall. Logistics hall formwork covers it. Skip.
- Outer north face (Y=+4.3): exposed Z=[0,6], X=[-24,-20]
- Outer south face (Y=-4.3): exposed Z=[0,6], X=[-24,-20]
- The east face (X=-19.7 inner face toward observation corridor) is interior. Skip.

**Exit Stair (X=[20,24], Y=[-4,4], Z=[0,6]):**
- Outer east face (X=+24.3): shared with logistics hall east wall. Skip.
- Outer north face (Y=+4.3): exposed, X=[20,24]
- Outer south face (Y=-4.3): exposed, X=[20,24]

[FLAG 7: Stair formwork — the entry stair north/south faces (Y=±4.3) from X=[-24,-20] at Z=2.4 will create a visible lift line that is continuous with the observation corridor north/south outer face (Y=±4.3) at Z=8.4. These are different faces — the stair face is at Y=±4.3 for Z=[0,6]; the corridor face starts at the same Y=±4.3 but for Z=[6,10]. Should the stair faces have formwork lines given they may be interior (stair may be interior to the building complex)? Defaulting to including them as exterior exposed faces. Reviewer to confirm.]

---

### 5.1 Logistics Hall Formwork Lines

Z=2.4 lift (Z range [2.39, 2.41]):

```
L400_hall_fw_N_L1:   [-24.0, 11.00, 2.39] → [24.0,  11.02, 2.41]
L400_hall_fw_S_L1:   [-24.0, -11.02, 2.39] → [24.0, -11.00, 2.41]
L400_hall_fw_W_L1:   [-24.02, -11.0, 2.39] → [-24.00, 11.0, 2.41]
L400_hall_fw_E_L1:   [24.00, -11.0, 2.39] → [24.02, 11.0, 2.41]
```

Total: 4 elements

---

### 5.2 Observation Corridor Formwork Lines

Corridor walls Z=[6,10]. One lift at Z = 6 + 2.4 = 8.4. Z range [8.39, 8.41]:

```
L400_corridor_fw_N_L1:   [-20.0, 4.30, 8.39] → [20.0,  4.32, 8.41]
L400_corridor_fw_S_L1:   [-20.0, -4.32, 8.39] → [20.0, -4.30, 8.41]
L400_corridor_fw_W_L1:   [-20.32, -4.3, 8.39] → [-20.30, 4.3, 8.41]
L400_corridor_fw_E_L1:   [20.30, -4.3, 8.39] → [20.32, 4.3, 8.41]
```

Total: 4 elements

---

### 5.3 Entry Stair Formwork Lines

Z=2.4 lift. Outer north and south faces:

```
L400_entry_stair_fw_N_L1:   [-24.0, 4.30, 2.39] → [-20.0,  4.32, 2.41]
L400_entry_stair_fw_S_L1:   [-24.0, -4.32, 2.39] → [-20.0, -4.30, 2.41]
```

Total: 2 elements

---

### 5.4 Exit Stair Formwork Lines

Z=2.4 lift. Outer north and south faces:

```
L400_exit_stair_fw_N_L1:   [20.0, 4.30, 2.39] → [24.0,  4.32, 2.41]
L400_exit_stair_fw_S_L1:   [20.0, -4.32, 2.39] → [24.0, -4.30, 2.41]
```

Total: 2 elements

**Total formwork line elements: 4 + 4 + 2 + 2 = 12**

---

## SECTION 6 — EXPANSION JOINTS (L400_Material)

Logistics Hall is 48m long. Joints at X=-8 and X=+8 (dividing hall into three ~16m bays).
20mm-wide colored solid boxes, continuous through walls and roof slab.

Joint at X=-8:
- Wall element: through full wall thickness + 20mm protrusion each side, full Y extent of logistics hall, full wall height Z=[0,5]
- Slab element: through roof slab Z=[5.0, 5.55]

```
L400_joint_X-8_wall:    [-8.01, -11.3, 0.0] → [-7.99,  11.3, 5.0]
L400_joint_X-8_slab:    [-8.01, -11.0, 5.0] → [-7.99,  11.0, 5.55]
```

Joint at X=+8:
```
L400_joint_X+8_wall:    [7.99, -11.3, 0.0] → [8.01,  11.3, 5.0]
L400_joint_X+8_slab:    [7.99, -11.0, 5.0] → [8.01,  11.0, 5.55]
```

Assign dark display color (near-black) to read as gaps.

**Total: 4 joint elements**

---

## SECTION 7 — OPENING FRAMES (L350_Detail)

Steel hollow section 100mm × 100mm (0.1 × 0.1 units) framing each opening.

### 7.1 West Truck Bay Frame (X=-24 wall)

Opening: Y=[-3, 3], Z=[0, 4.5] (6m wide × 4.5m tall per concept prompt)

Wall face at X=-24.0 (outer). Frame extends 100mm outside and 100mm inside wall face.
In wall plane: frame members at perimeter of opening.

```
L350_frame_truckbay_top:     [-24.1, -3.0, 4.5] → [-23.9, 3.0, 4.6]
L350_frame_truckbay_bot:     [-24.1, -3.0, -0.1] → [-23.9, 3.0, 0.0]
L350_frame_truckbay_jambN:   [-24.1,  2.9, -0.1] → [-23.9, 3.1, 4.6]
L350_frame_truckbay_jambS:   [-24.1, -3.1, -0.1] → [-23.9, -2.9, 4.6]
```

RC lintel above opening (300mm deep × full opening width + 150mm each side bearing):
```
L350_lintel_truckbay:   [-24.15, -3.0, 4.5] → [-23.85, 3.0, 4.8]
```

### 7.2 East Dispatch Frame (X=+24 wall)

Opening: Y=[-3, 3], Z=[0, 4.5] (matching west bay)

```
L350_frame_dispatch_top:     [23.9, -3.0, 4.5] → [24.1, 3.0, 4.6]
L350_frame_dispatch_bot:     [23.9, -3.0, -0.1] → [24.1, 3.0, 0.0]
L350_frame_dispatch_jambN:   [23.9,  2.9, -0.1] → [24.1, 3.1, 4.6]
L350_frame_dispatch_jambS:   [23.9, -3.1, -0.1] → [24.1, -2.9, 4.6]
```

RC lintel:
```
L350_lintel_dispatch:   [23.85, -3.0, 4.5] → [24.15, 3.0, 4.8]
```

### 7.3 Observation South Glazing Wall Frame (Y=-4 face)

Full glazing: Y=-4, X=[-20,20], Z=[6.5, 9.5] (per concept prompt)
Aluminum curtain wall frame — thin 50mm frame boxes at perimeter of glazed zone.
Frame thickness: 0.05 units (50mm), set in wall plane.

Wall outer face at Y=-4.3. Frame on inner face of wall at Y=-4.0.

```
L350_frame_glazing_top:     [-20.0, -4.05, 9.5] → [20.0, -4.00, 9.6]
L350_frame_glazing_bot:     [-20.0, -4.05, 6.4] → [20.0, -4.00, 6.5]
L350_frame_glazing_jambW:   [-20.05, -4.05, 6.4] → [-20.00, -4.00, 9.6]
L350_frame_glazing_jambE:   [20.00, -4.05, 6.4] → [20.05, -4.00, 9.6]
```

Note: glazing bottom at Z=6.5 (0.5m sill above corridor floor Z=6), top at Z=9.5 (0.5m from corridor ceiling Z=10). Frame matches these limits.

### 7.4 North Slot Windows — 5 windows (Y=+4 face)

5 windows, each 2m wide, spaced 6m apart, Y=+4, Z=[7,9]:
Centers at X = -12, -6, 0, +6, +12

Wall outer face at Y=+4.3, inner face at Y=+4.0. Frame on wall face.

For each window (2m wide = X ± 1.0 from center, 2m tall = Z=[7,9]):

```
L350_frame_slot_N1_top:    [-13.0, 4.00, 9.0] → [-11.0, 4.05, 9.1]
L350_frame_slot_N1_bot:    [-13.0, 4.00, 6.9] → [-11.0, 4.05, 7.0]
L350_frame_slot_N1_jambW:  [-13.05, 4.00, 6.9] → [-13.00, 4.05, 9.1]
L350_frame_slot_N1_jambE:  [-11.00, 4.00, 6.9] → [-10.95, 4.05, 9.1]

L350_frame_slot_N2_top:    [-7.0, 4.00, 9.0] → [-5.0, 4.05, 9.1]
L350_frame_slot_N2_bot:    [-7.0, 4.00, 6.9] → [-5.0, 4.05, 7.0]
L350_frame_slot_N2_jambW:  [-7.05, 4.00, 6.9] → [-7.00, 4.05, 9.1]
L350_frame_slot_N2_jambE:  [-5.00, 4.00, 6.9] → [-4.95, 4.05, 9.1]

L350_frame_slot_N3_top:    [-1.0, 4.00, 9.0] → [1.0, 4.05, 9.1]
L350_frame_slot_N3_bot:    [-1.0, 4.00, 6.9] → [1.0, 4.05, 7.0]
L350_frame_slot_N3_jambW:  [-1.05, 4.00, 6.9] → [-1.00, 4.05, 9.1]
L350_frame_slot_N3_jambE:  [ 1.00, 4.00, 6.9] → [ 1.05, 4.05, 9.1]

L350_frame_slot_N4_top:    [5.0, 4.00, 9.0] → [7.0, 4.05, 9.1]
L350_frame_slot_N4_bot:    [5.0, 4.00, 6.9] → [7.0, 4.05, 7.0]
L350_frame_slot_N4_jambW:  [4.95, 4.00, 6.9] → [5.00, 4.05, 9.1]
L350_frame_slot_N4_jambE:  [7.00, 4.00, 6.9] → [7.05, 4.05, 9.1]

L350_frame_slot_N5_top:    [11.0, 4.00, 9.0] → [13.0, 4.05, 9.1]
L350_frame_slot_N5_bot:    [11.0, 4.00, 6.9] → [13.0, 4.05, 7.0]
L350_frame_slot_N5_jambW:  [10.95, 4.00, 6.9] → [11.00, 4.05, 9.1]
L350_frame_slot_N5_jambE:  [13.00, 4.00, 6.9] → [13.05, 4.05, 9.1]
```

Total per window: 4 elements × 5 windows = 20 elements

### 7.5 Floor Viewing Slot Edge Frames (Z=6 floor)

3 slots at X=[-8, 0, +8], Y=[-2, 2], 4m × 4m each (glass floor zones).
Steel edge frame 80mm × 80mm (0.08 × 0.08 units) running perimeter of each slot.
Frame sits in the floor slab at Z=6, at slot perimeter.

For each slot (4m × 4m = X=[center-2, center+2], Y=[-2,2]):

**Slot 1 at X=-8:**
```
L350_slot_frame_S1_N:   [-10.0, 1.92, 5.92] → [-6.0, 2.00, 6.00]
L350_slot_frame_S1_S:   [-10.0, -2.00, 5.92] → [-6.0, -1.92, 6.00]
L350_slot_frame_S1_W:   [-10.08, -2.0, 5.92] → [-10.00, 2.0, 6.00]
L350_slot_frame_S1_E:   [-6.00, -2.0, 5.92] → [-5.92, 2.0, 6.00]
```

**Slot 2 at X=0:**
```
L350_slot_frame_S2_N:   [-2.0, 1.92, 5.92] → [2.0, 2.00, 6.00]
L350_slot_frame_S2_S:   [-2.0, -2.00, 5.92] → [2.0, -1.92, 6.00]
L350_slot_frame_S2_W:   [-2.08, -2.0, 5.92] → [-2.00, 2.0, 6.00]
L350_slot_frame_S2_E:   [ 2.00, -2.0, 5.92] → [ 2.08, 2.0, 6.00]
```

**Slot 3 at X=+8:**
```
L350_slot_frame_S3_N:   [6.0, 1.92, 5.92] → [10.0, 2.00, 6.00]
L350_slot_frame_S3_S:   [6.0, -2.00, 5.92] → [10.0, -1.92, 6.00]
L350_slot_frame_S3_W:   [5.92, -2.0, 5.92] → [6.00, 2.0, 6.00]
L350_slot_frame_S3_E:   [10.00, -2.0, 5.92] → [10.08, 2.0, 6.00]
```

Total viewing slot frames: 4 × 3 = 12 elements

**Total opening frame elements: 5 (truck bay) + 5 (dispatch) + 4 (glazing) + 20 (slot windows) + 12 (floor slots) = 46 elements**

---

## SECTION 8 — FACADE PANEL JOINTS (L400_Material)

Logistics Hall north and south outer faces: vertical panel joints at X = -16, -8, 0, +8, +16.
5mm wide (0.005 units) × 20mm deep (0.02 units) incised boxes.
Full wall height Z=[0, 5].

North face (outer face at Y=+11.0, inner face at Y=+10.7, joint depth from outer face):
```
L400_pj_hall_N_X-16:   [-16.005, 10.98, 0.0] → [-16.000, 11.00, 5.0]
L400_pj_hall_N_X-8:    [ -8.005, 10.98, 0.0] → [ -8.000, 11.00, 5.0]
L400_pj_hall_N_X0:     [ -0.005, 10.98, 0.0] → [  0.000, 11.00, 5.0]
L400_pj_hall_N_X+8:    [  7.995, 10.98, 0.0] → [  8.000, 11.00, 5.0]
L400_pj_hall_N_X+16:   [ 15.995, 10.98, 0.0] → [ 16.000, 11.00, 5.0]
```

South face (outer face at Y=-11.0, inner face at Y=-10.7):
```
L400_pj_hall_S_X-16:   [-16.005, -11.00, 0.0] → [-16.000, -10.98, 5.0]
L400_pj_hall_S_X-8:    [ -8.005, -11.00, 0.0] → [ -8.000, -10.98, 5.0]
L400_pj_hall_S_X0:     [ -0.005, -11.00, 0.0] → [  0.000, -10.98, 5.0]
L400_pj_hall_S_X+8:    [  7.995, -11.00, 0.0] → [  8.000, -10.98, 5.0]
L400_pj_hall_S_X+16:   [ 15.995, -11.00, 0.0] → [ 16.000, -10.98, 5.0]
```

**Total facade panel joint elements: 10**

---

## EXECUTION SUMMARY

### Element count

| Section | Type | Count |
|---------|------|-------|
| 1.1 | Logistics Hall Roof Slab | 1 |
| 1.2 | Logistics Hall Parapets | 4 |
| 1.3 | Observation Corridor Roof Slab | 1 |
| 1.4 | Observation Corridor Parapets | 4 |
| 1.5 | Loading Dock Canopy Roof Slab | 1 |
| 2.1 | Logistics Hall Roof Assembly (XPS/membrane/gravel) | 3 |
| 2.2 | Observation Corridor Roof Assembly | 3 |
| 2.3 | Canopy Roof Assembly | 3 |
| 3.1 | Waterproofing Upstands (hall 4 + corridor 4) | 8 |
| 3.2 | Drip Edges (hall 4 + corridor 4) | 8 |
| 4.1 | Column Base Plates (6 main + 4 dock) | 10 |
| 4.2 | Column Top Bearing Plates (6 main + 4 dock) | 10 |
| 4.3 | Cantilever Brackets | 6 |
| 5.1 | Logistics Hall Formwork Lines | 4 |
| 5.2 | Observation Corridor Formwork Lines | 4 |
| 5.3 | Entry Stair Formwork Lines | 2 |
| 5.4 | Exit Stair Formwork Lines | 2 |
| 6 | Expansion Joints (wall + slab at X=±8) | 4 |
| 7.1–7.2 | Truck Bay + Dispatch Frames + Lintels | 10 |
| 7.3 | South Glazing Wall Frame | 4 |
| 7.4 | North Slot Window Frames | 20 |
| 7.5 | Floor Viewing Slot Edge Frames | 12 |
| 8 | Facade Panel Joints | 10 |
| **TOTAL** | | **134 elements** |

---

## BUILD ORDER

1. Create 3 new layers (L300_Roof, L350_Detail, L400_Material)
2. Logistics Hall roof slab (1 box, L300_Roof)
3. Logistics Hall parapets (4 boxes, L300_Roof)
4. Observation Corridor roof slab (1 box, L300_Roof)
5. Observation Corridor parapets (4 boxes, L300_Roof)
6. Loading Dock Canopy roof slab (1 box, L300_Roof)
7. Roof assembly layers — all 3 zones (9 boxes total, L400_Material) — batch as one script
8. Waterproofing upstands (8 boxes, L400_Material)
9. Drip edges (8 boxes, L400_Material)
10. Column base plates (10 boxes, L350_Detail) — batch
11. Column top bearing plates (10 boxes, L350_Detail) — batch
12. Cantilever brackets (6 boxes, L350_Detail)
13. Formwork lines (12 boxes, L400_Material) — batch as one script
14. Expansion joints (4 boxes, L400_Material)
15. Truck bay and dispatch frames + lintels (10 boxes, L350_Detail)
16. South glazing wall frame (4 boxes, L350_Detail)
17. North slot window frames (20 boxes, L350_Detail) — batch as one script
18. Floor viewing slot frames (12 boxes, L350_Detail) — batch as one script
19. Facade panel joints (10 boxes, L400_Material)

---

## EXECUTOR NOTES

1. All coordinates are meter-scale in a centimeter-unit Rhino doc. Use numbers exactly as written.
2. Do NOT multiply by 100.
3. Use `rhino_execute_python_code` with `Box()` (BoundingBox from two corner points) for all elements.
4. Batch by section — formwork lines in one script, base plates in one script, etc.
5. If a boolean or complex operation fails, fall back to additive geometry only and note it.
6. After all geometry is placed: capture Perspective, Top, Front, and Section (Y=0 cut) viewports.
7. Target instance: `lock_02` (port 9002). All MCP calls must include `target: "lock_02"`.
8. The critical structural zone is Z=[5.55, 6.0] — between logistics hall roof top and observation corridor floor. Columns are exposed here. Do not add geometry to this zone except cantilever brackets.
9. Observation corridor viewing slots (floor at Z=6): the slot frame sits at Z=[5.92, 6.0] — this is within the observation corridor floor slab zone, NOT inside the logistics hall.

---

## FLAGS SUMMARY

| Flag | Description | Location |
|------|-------------|----------|
| FLAG 1 | Logistics hall slab system: flat slab (550mm) vs beam+slab (300mm) | Section 1.1 |
| FLAG 2 | Logistics hall slab continuity under observation corridor columns | Section 1.1 |
| FLAG 3 | Parapet at X=±20 inner logistics hall edge — not required (<1m drop) | Section 1.2 |
| FLAG 4 | Observation corridor west parapet — included despite brief hint to omit | Section 1.4 |
| FLAG 5 | Loading dock canopy parapet — omitted (non-public maintenance roof) | Section 1.5 |
| FLAG 6 | Cantilever bracket interpretation — bearing stub vs full cantilever beam | Section 4.3 |
| FLAG 7 | Stair formwork lines — exterior/interior face determination | Section 5 |

---

*Status: DRAFT FOR ROUNDTABLE REVIEW — do NOT execute until approved*
