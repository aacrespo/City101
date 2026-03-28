# Lock Type 02 — Cargo Lock
# LOG400 Complete Building Spec: DRAFT FOR ROUNDTABLE REVIEW
# Status: DRAFT
# Date: 2026-03-27

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry was built in METER-SCALE values (X=-24 to 24, Z=0 to 10.25).
"10.0" in Rhino = 10.0 as a number, displayed as "10 cm" but conceptually 10m.

**ALL coordinates in this spec are meter-scale. Use them exactly as written.**
**Do NOT multiply by 100. Do NOT convert.**

X = corridor axis (negative = Entry/West, positive = Exit/East)
Y = lateral axis (positive = North, negative = South)
Z = vertical (0 = finished floor level)

---

## LAYERS TO CREATE

```
Type_02_Cargo::Volumes       — RGB(255, 169, 77)  — primary massing solids (walls, floors)
Type_02_Cargo::Circulation   — RGB(255, 200, 140) — paths as polylines
Type_02_Cargo::Structure     — RGB(180, 120, 55)  — columns, beams
Type_02_Cargo::Openings      — RGB(255, 185, 110) — door/window voids (modeled as thin frames)
Type_02_Cargo::Annotations   — RGB(255, 220, 180) — text dots
Type_02_Cargo::L300_Roof     — RGB(200, 155, 100) — roof slabs, parapets
Type_02_Cargo::L350_Detail   — RGB(160, 115, 70)  — connections, frames, brackets, kickers
Type_02_Cargo::L400_Material — RGB(120, 85, 50)   — formwork, joints, hardware, edge conditions
```

---

## SECTION A — BASE BUILDING (Volumes layer)

### A1. Logistics Hall Walls

Layer: `Type_02_Cargo::Volumes`
4 wall shells, 300mm (0.3 units) thick, Z=[0, 5].

```
A1_logistics_wall_N:   [-24.0, 10.7, 0.0] → [24.0, 11.0, 5.0]
A1_logistics_wall_S:   [-24.0, -11.0, 0.0] → [24.0, -10.7, 5.0]
A1_logistics_wall_W:   [-24.0, -11.0, 0.0] → [-23.7, 11.0, 5.0]
A1_logistics_wall_E:   [23.7, -11.0, 0.0] → [24.0, 11.0, 5.0]
```

---

### A2. Logistics Hall Floor Slab

Layer: `Type_02_Cargo::Volumes`
Name: `A2_logistics_floor_slab`
300mm ground slab.

```
Corner A: [-24.0, -11.0, -0.3]
Corner B: [24.0, 11.0, 0.0]
```

---

### A3. Internal Sorting Bay Walls

Layer: `Type_02_Cargo::Volumes`
2 divider walls at X=-8 and X=+8, 200mm (0.2 units) thick, Z=[0, 5].

```
A3_sorting_wall_W:   [-8.1, -11.0, 0.0] → [-7.9, 11.0, 5.0]
A3_sorting_wall_E:   [7.9, -11.0, 0.0] → [8.1, 11.0, 5.0]
```

---

### A4. Observation Corridor Walls

Layer: `Type_02_Cargo::Volumes`
4 walls, Z=[6, 10]. North, East, West = 250mm (0.25 units) solid RC. South = glazing (thin mullion frame, see C3).

```
A4_obs_wall_N:   [-20.0, 3.75, 6.0] → [20.0, 4.0, 10.0]
A4_obs_wall_E:   [19.75, -4.0, 6.0] → [20.0, 4.0, 10.0]
A4_obs_wall_W:   [-20.0, -4.0, 6.0] → [-19.75, 4.0, 10.0]
```

South wall omitted as solid — replaced by curtain wall glazing (see Section C3).
A thin mullion frame placeholder:
```
A4_obs_wall_S_frame:   [-20.0, -4.0, 6.0] → [20.0, -3.95, 10.0]
```
(50mm deep mullion frame, not a solid wall)

---

### A5. Observation Corridor Floor Slab

Layer: `Type_02_Cargo::Volumes`
Name: `A5_obs_floor_slab`
250mm slab.

```
Corner A: [-20.0, -4.0, 5.75]
Corner B: [20.0, 4.0, 6.0]
```

Structural note: This slab spans 8m (Y direction) and is supported by transfer beams B3 at Y=±4. The 16m X-direction span between main columns is subdivided by the beams. 250mm is adequate for the 8m width span (span/30 = 267mm, rounded to 250mm for consistency with lighter public loads per SIA 261 Category C1).

---

### A6. Entry Stair Volume

Layer: `Type_02_Cargo::Volumes`
Solid shell: 4 walls + landing slab at Z=6.

Walls (300mm thick):
```
A6_stair_entry_wall_N:   [-24.0, 3.7, 0.0] → [-20.0, 4.0, 6.0]
A6_stair_entry_wall_S:   [-24.0, -4.0, 0.0] → [-20.0, -3.7, 6.0]
A6_stair_entry_wall_W:   [-24.0, -4.0, 0.0] → [-23.7, 4.0, 6.0]
A6_stair_entry_wall_E:   [-20.0, -4.0, 0.0] → [-19.7, 4.0, 6.0]
```

Landing slab (250mm):
```
A6_stair_entry_landing:   [-24.0, -4.0, 5.75] → [-20.0, 4.0, 6.0]
```

Note: Entry stair east wall at X=-20.0 to -19.7 overlaps with observation corridor west wall at X=-20.0 to -19.75. In practice these are the same wall — the stair east wall and corridor west wall merge. Model only the stair east wall (thicker at 300mm) and omit duplicate corridor west wall A4_obs_wall_W.

[FLAG 1] — Stair/corridor wall overlap at X=-20. Resolved: keep stair wall (300mm), remove corridor west wall duplicate. Same issue at east side.

---

### A7. Exit Stair Volume

Layer: `Type_02_Cargo::Volumes`
Walls (300mm thick):
```
A7_stair_exit_wall_N:   [20.0, 3.7, 0.0] → [24.0, 4.0, 6.0]
A7_stair_exit_wall_S:   [20.0, -4.0, 0.0] → [24.0, -3.7, 6.0]
A7_stair_exit_wall_W:   [19.7, -4.0, 0.0] → [20.0, 4.0, 6.0]
A7_stair_exit_wall_E:   [23.7, -4.0, 0.0] → [24.0, 4.0, 6.0]
```

Landing slab (250mm):
```
A7_stair_exit_landing:   [20.0, -4.0, 5.75] → [24.0, 4.0, 6.0]
```

Note: Same overlap logic — exit stair west wall at X=19.7-20.0 replaces corridor east wall at X=19.75-20.0. Keep stair wall.

[FLAG 2] — Same as FLAG 1 for east side. Resolved same way.

---

### A8. Loading Dock Canopy Slab

Layer: `Type_02_Cargo::Volumes`
Name: `A8_canopy_slab`
150mm thin slab.

```
Corner A: [-28.0, -8.0, 5.35]
Corner B: [-24.0, 8.0, 5.5]
```

---

## SECTION B — STRUCTURE (Structure layer)

### B1. Main Columns (6)

Layer: `Type_02_Cargo::Structure`
400mm × 400mm RC, full height Z=[0, 10].

| Column | X | Y | Corner A | Corner B |
|--------|---|---|----------|----------|
| B1_col_1 | -16 | +8 | [-16.2, 7.8, 0.0] | [-15.8, 8.2, 10.0] |
| B1_col_2 | -16 | -8 | [-16.2, -8.2, 0.0] | [-15.8, -7.8, 10.0] |
| B1_col_3 | 0 | +8 | [-0.2, 7.8, 0.0] | [0.2, 8.2, 10.0] |
| B1_col_4 | 0 | -8 | [-0.2, -8.2, 0.0] | [0.2, -7.8, 10.0] |
| B1_col_5 | +16 | +8 | [15.8, 7.8, 0.0] | [16.2, 8.2, 10.0] |
| B1_col_6 | +16 | -8 | [15.8, -8.2, 0.0] | [16.2, -7.8, 10.0] |

Structural note: Columns at Y=±8 create a 16m main span across the logistics hall. The observation corridor (Y=±4) is supported by transfer beams at Y=±4, which span between these columns. Columns continue through both levels to carry observation corridor roof loads.

---

### B2. Dock Columns (4)

Layer: `Type_02_Cargo::Structure`
150mm × 150mm steel, Z=[0, 5.5].

| Column | X | Y | Corner A | Corner B |
|--------|---|---|----------|----------|
| B2_dock_1 | -28 | +8 | [-28.075, 7.925, 0.0] | [-27.925, 8.075, 5.5] |
| B2_dock_2 | -28 | -8 | [-28.075, -8.075, 0.0] | [-27.925, -7.925, 5.5] |
| B2_dock_3 | -24 | +8 | [-24.075, 7.925, 0.0] | [-23.925, 8.075, 5.5] |
| B2_dock_4 | -24 | -8 | [-24.075, -8.075, 0.0] | [-23.925, -7.925, 5.5] |

Note: Dock columns at X=-24 overlap with logistics hall west wall (X=-24 to -23.7). B2_dock_3 and B2_dock_4 are embedded in the wall — acceptable at LOG400 level.

---

### B3. Observation Corridor Transfer Beams (2)

Layer: `Type_02_Cargo::Structure`
At Y=+4 and Y=-4, spanning X=[-20, 20], Z=[5.5, 6.0].
Beam depth: 500mm (0.5 units). Width: 400mm (0.4 units).

```
B3_beam_N:   [-20.0, 3.8, 5.5] → [20.0, 4.2, 6.0]
B3_beam_S:   [-20.0, -4.2, 5.5] → [20.0, -3.8, 6.0]
```

Structural note: These beams support the observation corridor floor slab (Z=5.75-6.0). They span 16m between main columns at X=-16 and X=+16, with 4m cantilevers to X=±20. Beam depth 500mm for 16m span (span/30 = 533mm, rounded to 500mm with 400mm width providing additional stiffness). The corridor floor slab sits ON TOP of these beams (slab bottom at Z=5.75, beam top at Z=6.0).

[FLAG 3] — Beam top is Z=6.0 but corridor floor slab bottom is Z=5.75. The slab extends 250mm below the beam top. This means the slab is partially embedded in the beam zone. Resolution: Adjust — slab sits ON beams. Slab bottom = beam top = Z=6.0. Slab: Z=[6.0, 6.25]. This changes observation corridor wall bases to Z=6.25 and observation corridor internal height from 4.0m to 3.75m.

---

## SECTION C — OPENINGS (Openings layer)

### C1. West Truck Bay Opening

Layer: `Type_02_Cargo::Openings`
Name: `C1_truck_bay`
Thin frame box at X=-24 wall, Y=[-3, 3], Z=[0, 4.5].
Frame thickness: 100mm (0.1 units).

```
C1_truck_frame_top:    [-24.1, -3.0, 4.5] → [-23.9, 3.0, 4.6]
C1_truck_frame_jambN:  [-24.1, 2.9, 0.0] → [-23.9, 3.1, 4.6]
C1_truck_frame_jambS:  [-24.1, -3.1, 0.0] → [-23.9, -2.9, 4.6]
```

---

### C2. East Dispatch Opening

Layer: `Type_02_Cargo::Openings`
Name: `C2_dispatch`
At X=24 wall, Y=[-3, 3], Z=[0, 4.5].

```
C2_dispatch_frame_top:    [23.9, -3.0, 4.5] → [24.1, 3.0, 4.6]
C2_dispatch_frame_jambN:  [23.9, 2.9, 0.0] → [24.1, 3.1, 4.6]
C2_dispatch_frame_jambS:  [23.9, -3.1, 0.0] → [24.1, -2.9, 4.6]
```

---

### C3. South Glazing Wall (Observation Corridor)

Layer: `Type_02_Cargo::Openings`
Full curtain wall at Y=-4, X=[-20, 20], Z=[6.5, 9.5].
Modeled as outer frame (4 bars).

```
C3_curtain_top:    [-20.0, -4.05, 9.5] → [20.0, -3.95, 9.6]
C3_curtain_bot:    [-20.0, -4.05, 6.4] → [20.0, -3.95, 6.5]
C3_curtain_jambW:  [-20.0, -4.05, 6.4] → [-19.9, -3.95, 9.6]
C3_curtain_jambE:  [19.9, -4.05, 6.4] → [20.0, -3.95, 9.6]
```

Note: Bottom of glazing at Z=6.5 (500mm above corridor floor at Z=6.0) to allow for a solid parapet/sill band at floor level.

[FLAG 4] — Glazing bottom: concept says Z=6.5 but corridor floor is now at Z=6.0 (per FLAG 3 resolution). The 500mm sill is appropriate for safety. Top at Z=9.5 leaves 500mm solid wall band below ceiling at Z=10. Acceptable.

---

### C4. North Slot Windows (5)

Layer: `Type_02_Cargo::Openings`
Y=4 (north wall of observation corridor), each 2m wide, Z=[7, 9].
Spaced at X = -12, -6, 0, +6, +12 (6m apart, centered in 40m corridor).
Frame thickness: 100mm.

```
C4_slot_1:   [-13.0, 3.9, 7.0] → [-11.0, 4.1, 9.0]
C4_slot_2:   [-7.0, 3.9, 7.0] → [-5.0, 4.1, 9.0]
C4_slot_3:   [-1.0, 3.9, 7.0] → [1.0, 4.1, 9.0]
C4_slot_4:   [5.0, 3.9, 7.0] → [7.0, 4.1, 9.0]
C4_slot_5:   [11.0, 3.9, 7.0] → [13.0, 4.1, 9.0]
```

(Modeled as thin boxes representing window openings in the north wall plane)

---

### C5. Floor Viewing Slots (3)

Layer: `Type_02_Cargo::Openings`
In corridor floor at Z=6.0, at X=[-8, 0, +8], Y=[-2, 2], each 4m × 4m.
Modeled as thin frame boxes (100mm frame around 4m×4m void).

```
C5_viewslot_W_frameN:   [-10.0, 1.9, 5.95] → [-6.0, 2.1, 6.05]
C5_viewslot_W_frameS:   [-10.0, -2.1, 5.95] → [-6.0, -1.9, 6.05]
C5_viewslot_W_frameE:   [-6.1, -2.0, 5.95] → [-5.9, 2.0, 6.05]
C5_viewslot_W_frameW:   [-10.1, -2.0, 5.95] → [-9.9, 2.0, 6.05]

C5_viewslot_C_frameN:   [-2.0, 1.9, 5.95] → [2.0, 2.1, 6.05]
C5_viewslot_C_frameS:   [-2.0, -2.1, 5.95] → [2.0, -1.9, 6.05]
C5_viewslot_C_frameE:   [1.9, -2.0, 5.95] → [2.1, 2.0, 6.05]
C5_viewslot_C_frameW:   [-2.1, -2.0, 5.95] → [-1.9, 2.0, 6.05]

C5_viewslot_E_frameN:   [6.0, 1.9, 5.95] → [10.0, 2.1, 6.05]
C5_viewslot_E_frameS:   [6.0, -2.1, 5.95] → [10.0, -1.9, 6.05]
C5_viewslot_E_frameE:   [9.9, -2.0, 5.95] → [10.1, 2.0, 6.05]
C5_viewslot_E_frameW:   [5.9, -2.0, 5.95] → [6.1, 2.0, 6.05]
```

Total: 12 frame elements (4 per slot × 3 slots)

---

## SECTION D — CIRCULATION (Circulation layer)

### D1. Logistics Path

Layer: `Type_02_Cargo::Circulation`
Name: `D1_logistics_path`
Polyline at Z=0.5, Y=0, X from -24 to 24.

```
Points: (-24, 0, 0.5) → (-8, 0, 0.5) → (8, 0, 0.5) → (24, 0, 0.5)
```

---

### D2. Public Path

Layer: `Type_02_Cargo::Circulation`
Name: `D2_public_path`
Polyline: ground west → stair up → corridor → stair down → ground east.

```
Points: (-24, 0, 0) → (-22, 0, 0) → (-20, 0, 6.5) → (20, 0, 6.5) → (22, 0, 0) → (24, 0, 0)
```

(Stair segments approximate linear ramp for polyline representation)

---

### D3. Visual Connection Lines (3)

Layer: `Type_02_Cargo::Circulation`
Dashed vertical lines at X=[-8, 0, +8] from Z=0.5 to Z=6.0.

```
D3_visual_W:   Line from (-8, 0, 0.5) to (-8, 0, 6.0)
D3_visual_C:   Line from (0, 0, 0.5) to (0, 0, 6.0)
D3_visual_E:   Line from (8, 0, 0.5) to (8, 0, 6.0)
```

---

## SECTION E — ANNOTATIONS (Annotations layer)

### E1. Text Dots

Layer: `Type_02_Cargo::Annotations`

| Name | Text | Position |
|------|------|----------|
| E1_label_logistics | "LOGISTICS / SORTING" | (0, 0, 2.5) |
| E1_label_observation | "PUBLIC OBSERVATION" | (0, 0, 8.0) |
| E1_label_viewslot_W | "VISUAL CONNECTION" | (-8, 0, 3.0) |
| E1_label_viewslot_C | "VISUAL CONNECTION" | (0, 0, 3.0) |
| E1_label_viewslot_E | "VISUAL CONNECTION" | (8, 0, 3.0) |
| E1_label_truckbay | "TRUCK BAY / ENTRY" | (-26, 0, 3.0) |
| E1_label_dispatch | "DISPATCH / EXIT" | (24, 0, 3.0) |

Total: 7 text dots

---

## SECTION 1 — ROOF SYSTEM (L300_Roof)

### Slab thickness rationale
- Logistics Hall: 16m column span (Y=±8) → span/30 = 533mm → use 550mm (0.55 units). Archibase warehouse standard.
- Observation Corridor: 8m width span (Y=±4) → span/30 = 267mm → use 250mm (0.25 units). Lighter public loads.
- Loading Dock Canopy: 4m span → 150mm. Already modeled in A8.

---

### 1.1 Logistics Hall Roof Slab

Layer: `Type_02_Cargo::L300_Roof`
Name: `L300_logistics_roof_slab`

```
Corner A: [-24.0, -11.0, 5.0]
Corner B: [24.0, 11.0, 5.55]
```

Thickness: 0.55 units (550mm).
Bottom face at Z=5.0 (bearing on 5.0m walls). Top face at Z=5.55.

Drainage: 1.5% fall south (toward Y=-11). Drop = 22m × 0.015 = 0.33 units over full Y span.
Modeled as flat box at LOG300. Annotate fall direction.

---

### 1.2 Logistics Hall Parapets

Non-public roof → SIA 358 minimum 150mm above finished surface.
Finished surface = gravel top = Z = 5.55 + 0.255 = 5.805.
Parapet top = 5.805 + 0.15 = 5.955, round to Z = 5.96.
Parapet base = Z = 5.55 (top of slab).
Parapet thickness: 300mm (0.3 units) matching wall thickness.

```
L300_logistics_parapet_N:   [-24.0, 10.7, 5.55] → [24.0, 11.0, 5.96]
L300_logistics_parapet_S:   [-24.0, -11.0, 5.55] → [24.0, -10.7, 5.96]
L300_logistics_parapet_W:   [-24.0, -11.0, 5.55] → [-23.7, 11.0, 5.96]
L300_logistics_parapet_E:   [23.7, -11.0, 5.55] → [24.0, 11.0, 5.96]
```

(4 parapet boxes — full perimeter, non-public roof)

---

### 1.3 Observation Corridor Roof Slab

Layer: `Type_02_Cargo::L300_Roof`
Name: `L300_obs_roof_slab`

```
Corner A: [-20.0, -4.0, 10.0]
Corner B: [20.0, 4.0, 10.25]
```

Thickness: 0.25 units (250mm).
Bottom face at Z=10.0 (bearing on 10.0m walls). Top face at Z=10.25.

Drainage: 1.5% fall north (toward Y=+4). Annotate.

---

### 1.4 Observation Corridor Parapets

Public roof access → SIA 358: 1100mm height above finished surface.
Finished surface = gravel top = Z = 10.25 + 0.255 = 10.505.
Parapet top = 10.505 + 1.1 = 11.605, round to Z = 11.61.
Parapet base = Z = 10.25 (top of slab).
Parapet thickness: 250mm (matching obs corridor wall thickness).

North, East, West parapets (3 faces — south face is glazing, see note):
```
L300_obs_parapet_N:   [-20.0, 3.75, 10.25] → [20.0, 4.0, 11.61]
L300_obs_parapet_E:   [19.75, -4.0, 10.25] → [20.0, 4.0, 11.61]
L300_obs_parapet_W:   [-20.0, -4.0, 10.25] → [-19.75, 4.0, 11.61]
```

South parapet (above glazing wall, thinner at 50mm — minimal upstand above curtain wall head):
```
L300_obs_parapet_S:   [-20.0, -4.0, 10.25] → [20.0, -3.95, 11.61]
```

[FLAG 5] — South parapet: the south wall is a curtain wall (glazing). A full 250mm parapet would look wrong. Using 50mm upstand at curtain wall head with 1100mm height for safety compliance. Alternative: steel railing instead of RC parapet on south face. Keeping RC for consistency.

---

### 1.5 Loading Dock Canopy

Already modeled as A8 (Z=[5.35, 5.5]).
Add drainage annotation: 2% fall west (away from building). Drop = 4m × 0.02 = 0.08 units.

---

### 1.6 Roof Assembly Layers — Logistics Hall (L400_Material)

Sits inside parapets, on top of logistics roof slab (Z=5.55).
Inner faces: N at Y=10.7, S at Y=-10.7, W at X=-23.7, E at X=23.7.

Total build-up: 200mm XPS + 5mm membrane + 50mm gravel = 255mm = 0.255 units.
Assembly top: Z = 5.55 + 0.255 = 5.805.

```
L400_logistics_insulation:   [-23.7, -10.7, 5.55] → [23.7, 10.7, 5.75]    (200mm)
L400_logistics_membrane:     [-23.7, -10.7, 5.75] → [23.7, 10.7, 5.755]   (5mm)
L400_logistics_gravel:       [-23.7, -10.7, 5.755] → [23.7, 10.7, 5.805]  (50mm)
```

---

### 1.7 Roof Assembly Layers — Observation Corridor (L400_Material)

Sits inside parapets, on top of obs roof slab (Z=10.25).
Inner faces: N at Y=3.75, S at Y=-3.95 (south parapet 50mm), W at X=-19.75, E at X=19.75.

```
L400_obs_insulation:   [-19.75, -3.95, 10.25] → [19.75, 3.75, 10.45]    (200mm)
L400_obs_membrane:     [-19.75, -3.95, 10.45] → [19.75, 3.75, 10.455]   (5mm)
L400_obs_gravel:       [-19.75, -3.95, 10.455] → [19.75, 3.75, 10.505]  (50mm)
```

---

### 1.8 Roof Assembly Layers — Canopy (L400_Material)

On top of canopy slab (Z=5.5). Canopy has no parapets — open edges.
Simplified: membrane only (no insulation on canopy — it's an open-air covering).

```
L400_canopy_membrane:   [-28.0, -8.0, 5.5] → [-24.0, 8.0, 5.505]   (5mm)
```

---

### 1.9 Parapet Edge Conditions (L400_Material)

**Waterproofing upstand** — 20mm wide × 150mm tall thin box against inner face of each parapet.

Logistics Hall (slab top Z=5.55, upstand Z=[5.55, 5.7]):
```
L400_logistics_upstand_N:   [-23.7, 10.68, 5.55] → [23.7, 10.70, 5.70]
L400_logistics_upstand_S:   [-23.7, -10.70, 5.55] → [23.7, -10.68, 5.70]
L400_logistics_upstand_W:   [-23.72, -10.7, 5.55] → [-23.70, 10.7, 5.70]
L400_logistics_upstand_E:   [23.70, -10.7, 5.55] → [23.72, 10.7, 5.70]
```

Observation Corridor (slab top Z=10.25, upstand Z=[10.25, 10.40]):
```
L400_obs_upstand_N:   [-19.75, 3.73, 10.25] → [19.75, 3.75, 10.40]
L400_obs_upstand_S:   [-19.75, -3.95, 10.25] → [19.75, -3.93, 10.40]
L400_obs_upstand_E:   [19.73, -3.95, 10.25] → [19.75, 3.75, 10.40]
L400_obs_upstand_W:   [-19.75, -3.95, 10.25] → [-19.73, 3.75, 10.40]
```

**Drip edge** — 30mm × 20mm box at outer top corner of each parapet.

Logistics Hall (parapet top Z=5.96):
```
L400_logistics_drip_N:   [-24.0, 10.97, 5.94] → [24.0, 11.0, 5.96]
L400_logistics_drip_S:   [-24.0, -11.0, 5.94] → [24.0, -10.97, 5.96]
L400_logistics_drip_W:   [-24.0, -11.0, 5.94] → [-23.97, 11.0, 5.96]
L400_logistics_drip_E:   [23.97, -11.0, 5.94] → [24.0, 11.0, 5.96]
```

Observation Corridor (parapet top Z=11.61):
```
L400_obs_drip_N:   [-20.0, 3.97, 11.59] → [20.0, 4.0, 11.61]
L400_obs_drip_E:   [19.97, -4.0, 11.59] → [20.0, 4.0, 11.61]
L400_obs_drip_W:   [-20.0, -4.0, 11.59] → [-19.97, 4.0, 11.61]
L400_obs_drip_S:   [-20.0, -4.0, 11.59] → [20.0, -3.97, 11.61]
```

---

## SECTION 2 — FORMWORK LINES (L400_Material)

RC walls cast in 2400mm (2.4 unit) lifts.
Formwork lift lines = thin horizontal box proud of wall face by 20mm (0.02 units), 20mm tall (0.02 units).

### Logistics Hall formwork lines

Logistics walls are 5.0m tall → lifts at Z=2.4 only (second lift at Z=4.8 is only 200mm below top, not a full lift).
Exposed outer faces: N (Y=11.0), S (Y=-11.0), W (X=-24.0), E (X=24.0).

Z=2.4 lift (Z range [2.39, 2.41]):
```
L400_logistics_fw_N_L1:   [-24.0, 11.00, 2.39] → [24.0, 11.02, 2.41]
L400_logistics_fw_S_L1:   [-24.0, -11.02, 2.39] → [24.0, -11.00, 2.41]
L400_logistics_fw_W_L1:   [-24.02, -11.0, 2.39] → [-24.00, 11.0, 2.41]
L400_logistics_fw_E_L1:   [24.00, -11.0, 2.39] → [24.02, 11.0, 2.41]
```

(4 formwork elements)

### Observation Corridor formwork lines

Obs corridor walls are 4.0m tall (Z=6 to 10) → lifts at Z=8.4 (2.4m above Z=6.0).
Exposed outer faces: N (Y=4.0), E (X=20.0), W (X=-20.0). South is glazing — no formwork.

Z=8.4 lift (Z range [8.39, 8.41]):
```
L400_obs_fw_N_L1:   [-20.0, 4.00, 8.39] → [20.0, 4.02, 8.41]
L400_obs_fw_E_L1:   [20.00, -4.0, 8.39] → [20.02, 4.0, 8.41]
L400_obs_fw_W_L1:   [-20.02, -4.0, 8.39] → [-20.00, 4.0, 8.41]
```

(3 formwork elements)

### Stair volume formwork lines

Entry stair walls 6.0m tall → lifts at Z=2.4 and Z=4.8.
Exit stair walls 6.0m tall → lifts at Z=2.4 and Z=4.8.

Entry stair exposed outer faces: W (X=-24.0), N (Y=4.0), S (Y=-4.0).
East face is interior to observation corridor — no formwork.

Z=2.4:
```
L400_stair_entry_fw_W_L1:   [-24.02, -4.0, 2.39] → [-24.00, 4.0, 2.41]
L400_stair_entry_fw_N_L1:   [-24.0, 4.00, 2.39] → [-20.0, 4.02, 2.41]
L400_stair_entry_fw_S_L1:   [-24.0, -4.02, 2.39] → [-20.0, -4.00, 2.41]
```

Z=4.8:
```
L400_stair_entry_fw_W_L2:   [-24.02, -4.0, 4.79] → [-24.00, 4.0, 4.81]
L400_stair_entry_fw_N_L2:   [-24.0, 4.00, 4.79] → [-20.0, 4.02, 4.81]
L400_stair_entry_fw_S_L2:   [-24.0, -4.02, 4.79] → [-20.0, -4.00, 4.81]
```

Exit stair exposed outer faces: E (X=24.0), N (Y=4.0), S (Y=-4.0).

Z=2.4:
```
L400_stair_exit_fw_E_L1:   [24.00, -4.0, 2.39] → [24.02, 4.0, 2.41]
L400_stair_exit_fw_N_L1:   [20.0, 4.00, 2.39] → [24.0, 4.02, 2.41]
L400_stair_exit_fw_S_L1:   [20.0, -4.02, 2.39] → [24.0, -4.00, 2.41]
```

Z=4.8:
```
L400_stair_exit_fw_E_L2:   [24.00, -4.0, 4.79] → [24.02, 4.0, 4.81]
L400_stair_exit_fw_N_L2:   [20.0, 4.00, 4.79] → [24.0, 4.02, 4.81]
L400_stair_exit_fw_S_L2:   [20.0, -4.02, 4.79] → [24.0, -4.00, 4.81]
```

**Total formwork lines: 4 (logistics) + 3 (obs) + 6 (entry stair) + 6 (exit stair) = 19**

---

## SECTION 3 — EXPANSION JOINTS (L400_Material)

Per archibase: joints every 30-40m for RC. Logistics hall is 48m → one joint at X=0.
Observation corridor is 40m → one joint at X=0.
Modeled as 20mm-wide colored solid boxes (no boolean required).

### Logistics Hall joint at X=0

Through walls (N and S) and roof slab:
```
L400_logistics_joint_wallN:   [-0.01, 10.7, 0.0] → [0.01, 11.0, 5.0]
L400_logistics_joint_wallS:   [-0.01, -11.0, 0.0] → [0.01, -10.7, 5.0]
L400_logistics_joint_slab:    [-0.01, -11.0, 5.0] → [0.01, 11.0, 5.55]
```

### Sorting bay walls at X=0

The joint passes through where sorting walls would be — but sorting walls are at X=±8, not X=0. No sorting wall intersection at X=0.

### Observation Corridor joint at X=0

Through N wall and roof slab (S wall is glazing — joint in curtain wall frame):
```
L400_obs_joint_wallN:   [-0.01, 3.75, 6.0] → [0.01, 4.0, 10.0]
L400_obs_joint_slab:    [-0.01, -4.0, 10.0] → [0.01, 4.0, 10.25]
```

### Observation Corridor floor joint at X=0

```
L400_obs_joint_floor:   [-0.01, -4.0, 5.75] → [0.01, 4.0, 6.0]
```

Assign dark display color (black or near-black) to read as gaps.
**Total: 6 joint elements**

---

## SECTION 4 — STRUCTURAL CONNECTIONS (L350_Detail)

### 4.1 Column Base Plates — 10 columns total

Steel plate: 500mm × 500mm × 30mm (0.5 × 0.5 × 0.03 units) — warehouse loads heavier per archibase.
Z position: [-0.03, 0] (plate cast into floor slab, top flush with floor).

**Main columns (6):**
```
L350_bp_B1_col1:   [-16.25, 7.75, -0.03] → [-15.75, 8.25, 0.0]
L350_bp_B1_col2:   [-16.25, -8.25, -0.03] → [-15.75, -7.75, 0.0]
L350_bp_B1_col3:   [-0.25, 7.75, -0.03] → [0.25, 8.25, 0.0]
L350_bp_B1_col4:   [-0.25, -8.25, -0.03] → [0.25, -7.75, 0.0]
L350_bp_B1_col5:   [15.75, 7.75, -0.03] → [16.25, 8.25, 0.0]
L350_bp_B1_col6:   [15.75, -8.25, -0.03] → [16.25, -7.75, 0.0]
```

**Dock columns (4):**
```
L350_bp_B2_dock1:   [-28.25, 7.75, -0.03] → [-27.75, 8.25, 0.0]
L350_bp_B2_dock2:   [-28.25, -8.25, -0.03] → [-27.75, -7.75, 0.0]
L350_bp_B2_dock3:   [-24.25, 7.75, -0.03] → [-23.75, 8.25, 0.0]
L350_bp_B2_dock4:   [-24.25, -8.25, -0.03] → [-23.75, -7.75, 0.0]
```

---

### 4.2 Column Top Bearing Plates

Steel plate: 500mm × 500mm × 20mm (0.5 × 0.5 × 0.02 units).

**Main columns top at Z=10.0 (full height to observation corridor roof):**
```
L350_tp_B1_col1:   [-16.25, 7.75, 10.0] → [-15.75, 8.25, 10.02]
L350_tp_B1_col2:   [-16.25, -8.25, 10.0] → [-15.75, -7.75, 10.02]
L350_tp_B1_col3:   [-0.25, 7.75, 10.0] → [0.25, 8.25, 10.02]
L350_tp_B1_col4:   [-0.25, -8.25, 10.0] → [0.25, -7.75, 10.02]
L350_tp_B1_col5:   [15.75, 7.75, 10.0] → [16.25, 8.25, 10.02]
L350_tp_B1_col6:   [15.75, -8.25, 10.0] → [16.25, -7.75, 10.02]
```

**Dock columns top at Z=5.5 (canopy height):**
```
L350_tp_B2_dock1:   [-28.25, 7.75, 5.5] → [-27.75, 8.25, 5.52]
L350_tp_B2_dock2:   [-28.25, -8.25, 5.5] → [-27.75, -7.75, 5.52]
L350_tp_B2_dock3:   [-24.25, 7.75, 5.5] → [-23.75, 8.25, 5.52]
L350_tp_B2_dock4:   [-24.25, -8.25, 5.5] → [-23.75, -7.75, 5.52]
```

---

### 4.3 Cantilever Brackets at Main Columns

At each of the 6 main columns, brackets support the transfer beams (B3) at Z=5.5.
Bracket dimensions: 300mm (depth into column) × 200mm (Z, height) × 600mm (Y, width).
Z range: [5.3, 5.5] (bracket top flush with beam bottom at Z=5.5).

Each column gets 1 inward-facing bracket (toward Y=0, supporting the beam):

Columns at Y=+8 (bracket extends toward Y=+4, i.e., toward -Y from column):
```
L350_bracket_col1:   [-16.2, 7.5, 5.3] → [-15.8, 8.1, 5.5]
L350_bracket_col3:   [-0.2, 7.5, 5.3] → [0.2, 8.1, 5.5]
L350_bracket_col5:   [15.8, 7.5, 5.3] → [16.2, 8.1, 5.5]
```

Columns at Y=-8 (bracket extends toward Y=-4, i.e., toward +Y from column):
```
L350_bracket_col2:   [-16.2, -8.1, 5.3] → [-15.8, -7.5, 5.5]
L350_bracket_col4:   [-0.2, -8.1, 5.3] → [0.2, -7.5, 5.5]
L350_bracket_col6:   [15.8, -8.1, 5.3] → [16.2, -7.5, 5.5]
```

Total: 6 brackets

---

## SECTION 5 — OPENING FRAMES + LINTELS (L350_Detail)

Steel hollow section 100mm × 100mm (0.1 × 0.1 units) framing each opening.
RC lintel above each truck/dispatch opening.

### 5.1 West Truck Bay Frame (X=-24 wall face)

```
L350_truck_lintel:      [-24.3, -3.0, 4.5] → [-23.7, 3.0, 4.8]
L350_truck_frame_top:   [-24.1, -3.0, 4.5] → [-23.9, 3.0, 4.6]
L350_truck_frame_jambN: [-24.1, 2.9, 0.0] → [-23.9, 3.1, 4.6]
L350_truck_frame_jambS: [-24.1, -3.1, 0.0] → [-23.9, -2.9, 4.6]
```

### 5.2 East Dispatch Frame (X=+24 wall face)

```
L350_dispatch_lintel:      [23.7, -3.0, 4.5] → [24.3, 3.0, 4.8]
L350_dispatch_frame_top:   [23.9, -3.0, 4.5] → [24.1, 3.0, 4.6]
L350_dispatch_frame_jambN: [23.9, 2.9, 0.0] → [24.1, 3.1, 4.6]
L350_dispatch_frame_jambS: [23.9, -3.1, 0.0] → [24.1, -2.9, 4.6]
```

### 5.3 Curtain Wall Frame — South Glazing

Reinforced steel frame around full curtain wall. Already modeled in C3 on Openings layer.
Additional structural transom at mid-height:

```
L350_curtain_transom:   [-20.0, -4.05, 8.0] → [20.0, -3.95, 8.1]
```

### 5.4 Slot Window Frames (5)

Steel frames around each slot window. Simplified as single box per slot (frame around opening):
```
L350_slot_frame_1:   [-13.1, 3.9, 6.9] → [-10.9, 4.1, 9.1]
L350_slot_frame_2:   [-7.1, 3.9, 6.9] → [-4.9, 4.1, 9.1]
L350_slot_frame_3:   [-1.1, 3.9, 6.9] → [1.1, 4.1, 9.1]
L350_slot_frame_4:   [4.9, 3.9, 6.9] → [7.1, 4.1, 9.1]
L350_slot_frame_5:   [10.9, 3.9, 6.9] → [13.1, 4.1, 9.1]
```

### 5.5 Floor Viewing Slot Edge Frames (3)

Steel edge trim around each floor viewing slot. 50mm × 50mm angle at slab edge.
Already partially modeled in C5. Additional edge protection:

```
L350_viewslot_edge_W:   [-10.05, -2.05, 5.95] → [-5.95, 2.05, 6.0]
L350_viewslot_edge_C:   [-2.05, -2.05, 5.95] → [2.05, 2.05, 6.0]
L350_viewslot_edge_E:   [5.95, -2.05, 5.95] → [10.05, 2.05, 6.0]
```

(Thin rings — hollow in center. At LOG400, modeled as solid thin slabs representing the edge condition. The void is implicit.)

Total Section 5: 2 lintels + 6 frame bars + 1 transom + 5 slot frames + 3 edge frames = **17 elements**

---

## SECTION 6 — FACADE PANEL JOINTS (L400_Material)

5mm wide (0.005 units) × 20mm deep (0.02 units) incised vertical joints.
Logistics hall N/S faces, full height Z=[0, 5.0].
At X = -16, -8, 0, +8, +16 (column line positions — natural construction joint locations, 8m spacing).

North face (outer face at Y=+11.0):
```
L400_pj_N_X-16:   [-16.0025, 10.98, 0.0] → [-15.9975, 11.00, 5.0]
L400_pj_N_X-8:    [-8.0025, 10.98, 0.0] → [-7.9975, 11.00, 5.0]
L400_pj_N_X0:     [-0.0025, 10.98, 0.0] → [0.0025, 11.00, 5.0]
L400_pj_N_X8:     [7.9975, 10.98, 0.0] → [8.0025, 11.00, 5.0]
L400_pj_N_X16:    [15.9975, 10.98, 0.0] → [16.0025, 11.00, 5.0]
```

South face (outer face at Y=-11.0):
```
L400_pj_S_X-16:   [-16.0025, -11.00, 0.0] → [-15.9975, -10.98, 5.0]
L400_pj_S_X-8:    [-8.0025, -11.00, 0.0] → [-7.9975, -10.98, 5.0]
L400_pj_S_X0:     [-0.0025, -11.00, 0.0] → [0.0025, -10.98, 5.0]
L400_pj_S_X8:     [7.9975, -11.00, 0.0] → [8.0025, -10.98, 5.0]
L400_pj_S_X16:    [15.9975, -11.00, 0.0] → [16.0025, -10.98, 5.0]
```

**Total: 10 facade panel joints**

---

## SECTION 7 — WALL KICKERS (L350_Detail)

50mm × 50mm RC kicker at wall base (Z=[0, 0.05]), on outer face of walls.

### Logistics Hall kickers

Outer faces: N at Y=11.0, S at Y=-11.0, W at X=-24.0, E at X=24.0.

```
L350_kicker_logistics_N:   [-24.0, 11.0, 0.0] → [24.0, 11.05, 0.05]
L350_kicker_logistics_S:   [-24.0, -11.05, 0.0] → [24.0, -11.0, 0.05]
L350_kicker_logistics_W:   [-24.05, -11.0, 0.0] → [-24.0, 11.0, 0.05]
L350_kicker_logistics_E:   [24.0, -11.0, 0.0] → [24.05, 11.0, 0.05]
```

### Stair volume kickers

Entry stair outer faces: W (X=-24.0), N (Y=4.0), S (Y=-4.0). East is interior.
```
L350_kicker_stair_entry_W:   [-24.05, -4.0, 0.0] → [-24.0, 4.0, 0.05]
L350_kicker_stair_entry_N:   [-24.0, 4.0, 0.0] → [-20.0, 4.05, 0.05]
L350_kicker_stair_entry_S:   [-24.0, -4.05, 0.0] → [-20.0, -4.0, 0.05]
```

Exit stair outer faces: E (X=24.0), N (Y=4.0), S (Y=-4.0).
```
L350_kicker_stair_exit_E:   [24.0, -4.0, 0.0] → [24.05, 4.0, 0.05]
L350_kicker_stair_exit_N:   [20.0, 4.0, 0.0] → [24.0, 4.05, 0.05]
L350_kicker_stair_exit_S:   [20.0, -4.05, 0.0] → [24.0, -4.0, 0.05]
```

Note: Observation corridor is at Z=6, no ground-level kicker needed. Sorting bay walls are internal dividers — no kicker.

**Total kickers: 4 (logistics) + 3 (entry stair) + 3 (exit stair) = 10 elements**

---

## EXECUTION SUMMARY

### Element count by section

| Section | Type | Layer | Count |
|---------|------|-------|-------|
| A1 | Logistics walls | Volumes | 4 |
| A2 | Logistics floor slab | Volumes | 1 |
| A3 | Sorting bay walls | Volumes | 2 |
| A4 | Observation corridor walls | Volumes | 4 |
| A5 | Observation corridor floor | Volumes | 1 |
| A6 | Entry stair (walls + landing) | Volumes | 5 |
| A7 | Exit stair (walls + landing) | Volumes | 5 |
| A8 | Loading dock canopy | Volumes | 1 |
| B1 | Main columns | Structure | 6 |
| B2 | Dock columns | Structure | 4 |
| B3 | Transfer beams | Structure | 2 |
| C1 | Truck bay opening frames | Openings | 3 |
| C2 | Dispatch opening frames | Openings | 3 |
| C3 | South glazing curtain wall | Openings | 4 |
| C4 | North slot windows | Openings | 5 |
| C5 | Floor viewing slot frames | Openings | 12 |
| D1 | Logistics path | Circulation | 1 |
| D2 | Public path | Circulation | 1 |
| D3 | Visual connection lines | Circulation | 3 |
| E1 | Text dots | Annotations | 7 |
| 1.1 | Logistics roof slab | L300_Roof | 1 |
| 1.2 | Logistics parapets | L300_Roof | 4 |
| 1.3 | Obs corridor roof slab | L300_Roof | 1 |
| 1.4 | Obs corridor parapets | L300_Roof | 4 |
| 1.6 | Logistics roof assembly | L400_Material | 3 |
| 1.7 | Obs roof assembly | L400_Material | 3 |
| 1.8 | Canopy membrane | L400_Material | 1 |
| 1.9 | Upstands + drip edges | L400_Material | 16 |
| 2 | Formwork lines | L400_Material | 19 |
| 3 | Expansion joints | L400_Material | 6 |
| 4.1 | Column base plates | L350_Detail | 10 |
| 4.2 | Column top plates | L350_Detail | 10 |
| 4.3 | Cantilever brackets | L350_Detail | 6 |
| 5 | Opening frames + lintels | L350_Detail | 17 |
| 6 | Facade panel joints | L400_Material | 10 |
| 7 | Wall kickers | L350_Detail | 10 |
| **TOTAL** | | | **199 elements** |

### Element count by layer

| Layer | Count |
|-------|-------|
| Type_02_Cargo::Volumes | 23 |
| Type_02_Cargo::Circulation | 5 |
| Type_02_Cargo::Structure | 12 |
| Type_02_Cargo::Openings | 27 |
| Type_02_Cargo::Annotations | 7 |
| Type_02_Cargo::L300_Roof | 10 |
| Type_02_Cargo::L350_Detail | 53 |
| Type_02_Cargo::L400_Material | 58 |
| **TOTAL** | **195** |

[FLAG 6] — Count discrepancy: section sum = 199 vs layer sum = 195. Need to reconcile.

---

### Build order

1. Create 8 layers
2. Logistics Hall walls (4 boxes, Volumes)
3. Logistics floor slab (1 box, Volumes)
4. Sorting bay walls (2 boxes, Volumes)
5. Observation corridor walls (4 boxes, Volumes)
6. Observation corridor floor slab (1 box, Volumes)
7. Entry stair volume (5 boxes, Volumes)
8. Exit stair volume (5 boxes, Volumes)
9. Loading dock canopy (1 box, Volumes)
10. Main columns (6 boxes, Structure)
11. Dock columns (4 boxes, Structure)
12. Transfer beams (2 boxes, Structure)
13. Truck bay opening frames (3 boxes, Openings)
14. Dispatch opening frames (3 boxes, Openings)
15. South glazing curtain wall (4 boxes, Openings)
16. North slot windows (5 boxes, Openings)
17. Floor viewing slot frames (12 boxes, Openings)
18. Circulation paths (2 polylines + 3 lines, Circulation)
19. Text dots (7 dots, Annotations)
20. Logistics roof slab (1 box, L300_Roof)
21. Logistics parapets (4 boxes, L300_Roof)
22. Obs corridor roof slab (1 box, L300_Roof)
23. Obs corridor parapets (4 boxes, L300_Roof)
24. Roof assembly layers (7 boxes, L400_Material)
25. Parapet edge conditions (16 boxes, L400_Material)
26. Formwork lines (19 boxes, L400_Material) — batch as one Python script
27. Expansion joints (6 boxes, L400_Material)
28. Column base plates (10 boxes, L350_Detail)
29. Column top plates (10 boxes, L350_Detail)
30. Cantilever brackets (6 boxes, L350_Detail)
31. Opening frames + lintels (17 boxes, L350_Detail)
32. Facade panel joints (10 boxes, L400_Material)
33. Wall kickers (10 boxes, L350_Detail)

---

### Executor notes

1. All coordinates are meter-scale in a centimeter-unit Rhino doc. Use numbers exactly as written.
2. Do NOT multiply by 100.
3. Use `rhino_execute_python_code` with `Box()` (BoundingBox from two corner points) for all elements.
4. Batch by section — formwork lines in one script, base plates in one script, etc.
5. If a boolean or complex operation fails, fall back to additive geometry only and note it.
6. After all geometry is placed: capture Perspective, Top, and Section (X=0 cut) viewports.
7. **Target instance: `"envelope"` (port 9002). All MCP calls must include `target: "envelope"`.**
8. Opening frames (C1-C5) and structural frames (Section 5) are both present — C-series on Openings layer for visibility, Section 5 on L350_Detail for structural representation. Some overlap is intentional.

---

### FLAGS requiring resolution

| Flag | Issue | Proposed resolution |
|------|-------|-------------------|
| FLAG 1 | Stair entry east wall overlaps obs corridor west wall at X=-20 | Keep stair wall (300mm thick, A6), remove corridor west wall (A4_obs_wall_W) |
| FLAG 2 | Stair exit west wall overlaps obs corridor east wall at X=+20 | Keep stair wall (300mm thick, A7), remove corridor east wall (A4_obs_wall_E) |
| FLAG 3 | Transfer beam top (Z=6.0) vs corridor floor slab bottom (Z=5.75) — slab embedded in beam | Adjust slab to Z=[6.0, 6.25], corridor walls to Z=[6.25, 10] |
| FLAG 4 | South glazing bottom relative to adjusted floor level | With floor at Z=6.0→6.25, glazing Z=[6.75, 9.5] with 500mm sill |
| FLAG 5 | South parapet on glazing wall — RC vs steel railing | Keep 50mm RC upstand for consistency |
| FLAG 6 | Element count discrepancy (199 vs 195) | Recount in review |
