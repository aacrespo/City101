# Lock Type 02 — Cargo Lock
# LOG400 Complete Building Spec: ROUNDTABLE-APPROVED Execution Spec
# Status: APPROVED — ready for executor
# Approved by: Roundtable Reviewer
# Date: 2026-03-27

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry was built in METER-SCALE values (X=-28 to 24, Z=-0.3 to 11.61).
"10.0" in Rhino = 10.0 as a number, displayed as "10 cm" but conceptually 10m.

**ALL coordinates in this spec are meter-scale. Use them exactly as written.**
**Do NOT multiply by 100. Do NOT convert.**

X = corridor axis (negative = Entry/West, positive = Exit/East)
Y = lateral axis (positive = North, negative = South)
Z = vertical (0 = finished floor level)

---

## CORRECTIONS FROM ROUNDTABLE REVIEW

| # | Issue | Resolution |
|---|-------|-----------|
| C1 | FLAG 1/2: Stair E/W walls overlap obs corridor E/W walls at X=±20 | Remove A4_obs_wall_W and A4_obs_wall_E. Keep stair walls (300mm, Z=0-6). Add new upper corridor end walls at X=±19.75 from Z=6.25-10.0 (250mm, above stair zone). |
| C2 | FLAG 3: Obs floor slab (Z=5.75-6.0) embedded in transfer beams (Z=5.5-6.0) | Slab adjusted to Z=[6.0, 6.25] — sits ON TOP of beams. Corridor walls now start at Z=6.25. Internal ceiling height = 3.75m (10.0-6.25). |
| C3 | FLAG 3 cascade: All obs corridor Z-references updated | Walls Z=[6.25, 10.0]. South frame Z=[6.25, 10.0]. Glazing Z=[6.75, 9.5]. Slot windows Z=[7.25, 9.25]. Floor viewing slots at Z=6.0-6.25. Public path at Z=6.75. |
| C4 | FLAG 4: Glazing bottom relative to new floor | Glazing bottom Z=6.75 (500mm sill above Z=6.25 floor). Top Z=9.5 (500mm solid band below Z=10 ceiling). |
| C5 | FLAG 5: South parapet — 50mm RC upstand at 1100mm height | Changed to 250mm thick (matching other parapets) but only 300mm tall above slab (Z=10.25-10.55). Safety railing above is assumed steel (not modeled at LOG400). |
| C6 | FLAG 6: Element count discrepancy (199 vs 195) | Recounted: 4 elements double-counted between C-series openings and Section 5 frames. Resolved by removing duplicate truck/dispatch frame bars from C1/C2 (structural versions in Section 5 supersede). Also net changes from C1-C5 corrections. |
| C7 | Stair W walls overlap logistics hall walls at X=-24/+24 | Entry stair W wall shares face with logistics W wall. Exit stair E wall shares face with logistics E wall. Remove A6_stair_entry_wall_W and A7_stair_exit_wall_E — logistics walls serve as shared boundary. |
| C8 | Obs corridor formwork lift Z wrong | With walls starting at Z=6.25, first lift at Z=6.25+2.4=8.65, not Z=8.4. |
| C9 | Expansion joint obs floor Z wrong | Floor now at Z=[6.0, 6.25], not Z=[5.75, 6.0]. Joint updated. |
| C10 | Stair formwork W face overlap with logistics formwork | Entry stair W face (X=-24) and logistics W face (X=-24) are the same wall face. Keep logistics formwork only for that face. Remove L400_stair_entry_fw_W_L1 and L400_stair_entry_fw_W_L2. Similarly remove L400_stair_exit_fw_E_L1 and L400_stair_exit_fw_E_L2. |

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
Walls start at Z=6.25 (top of floor slab, per C2 correction), end at Z=10.0.
North wall: 250mm thick. South = glazing frame (see C3). East/West = separate upper end walls (per C1 correction).

```
A4_obs_wall_N:         [-20.0, 3.75, 6.25] → [20.0, 4.0, 10.0]
A4_obs_wall_S_frame:   [-20.0, -4.0, 6.25] → [20.0, -3.95, 10.0]
A4_obs_wall_E_upper:   [19.75, -4.0, 6.25] → [20.0, 4.0, 10.0]
A4_obs_wall_W_upper:   [-20.0, -4.0, 6.25] → [-19.75, 4.0, 10.0]
```

(South frame is 50mm deep mullion placeholder, not solid RC wall)

---

### A5. Observation Corridor Floor Slab

Layer: `Type_02_Cargo::Volumes`
Name: `A5_obs_floor_slab`
250mm slab, sitting ON TOP of transfer beams (per C2 correction).

```
Corner A: [-20.0, -4.0, 6.0]
Corner B: [20.0, 4.0, 6.25]
```

Structural note: Beam top at Z=6.0, slab bottom at Z=6.0, slab top at Z=6.25. The 8m Y-span (between beams at Y=±4) is the governing span. 250mm is adequate for SIA 261 Category C1 (public assembly, lighter loads). Span/30 = 267mm; 250mm acceptable given continuous slab action over beams.

---

### A6. Entry Stair Volume

Layer: `Type_02_Cargo::Volumes`
Solid shell: 3 walls (per C7 correction — west wall removed, shared with logistics W wall) + landing slab.

Walls (300mm thick):
```
A6_stair_entry_wall_N:   [-24.0, 3.7, 0.0] → [-20.0, 4.0, 6.0]
A6_stair_entry_wall_S:   [-24.0, -4.0, 0.0] → [-20.0, -3.7, 6.0]
A6_stair_entry_wall_E:   [-20.0, -4.0, 0.0] → [-19.7, 4.0, 6.0]
```

Landing slab (250mm):
```
A6_stair_entry_landing:   [-24.0, -4.0, 5.75] → [-20.0, 4.0, 6.0]
```

(West wall omitted — logistics hall west wall A1_logistics_wall_W serves as shared boundary. 4 elements total.)

---

### A7. Exit Stair Volume

Layer: `Type_02_Cargo::Volumes`
3 walls (per C7 correction — east wall removed) + landing slab.

Walls (300mm thick):
```
A7_stair_exit_wall_N:   [20.0, 3.7, 0.0] → [24.0, 4.0, 6.0]
A7_stair_exit_wall_S:   [20.0, -4.0, 0.0] → [24.0, -3.7, 6.0]
A7_stair_exit_wall_W:   [19.7, -4.0, 0.0] → [20.0, 4.0, 6.0]
```

Landing slab (250mm):
```
A7_stair_exit_landing:   [20.0, -4.0, 5.75] → [24.0, 4.0, 6.0]
```

(East wall omitted — logistics hall east wall A1_logistics_wall_E serves as shared boundary. 4 elements total.)

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
400mm x 400mm RC, full height Z=[0, 10].

| Column | X | Y | Corner A | Corner B |
|--------|---|---|----------|----------|
| B1_col_1 | -16 | +8 | [-16.2, 7.8, 0.0] | [-15.8, 8.2, 10.0] |
| B1_col_2 | -16 | -8 | [-16.2, -8.2, 0.0] | [-15.8, -7.8, 10.0] |
| B1_col_3 | 0 | +8 | [-0.2, 7.8, 0.0] | [0.2, 8.2, 10.0] |
| B1_col_4 | 0 | -8 | [-0.2, -8.2, 0.0] | [0.2, -7.8, 10.0] |
| B1_col_5 | +16 | +8 | [15.8, 7.8, 0.0] | [16.2, 8.2, 10.0] |
| B1_col_6 | +16 | -8 | [15.8, -8.2, 0.0] | [16.2, -7.8, 10.0] |

Structural note: Columns at Y=+-8 are inside the logistics hall walls (inner face at Y=+-10.7). They create a 16m clear span across the hall. The observation corridor transfer beams span between column pairs at X=-16, 0, +16. Columns extend full height through both levels to support corridor roof slab via intermediate beams.

---

### B2. Dock Columns (4)

Layer: `Type_02_Cargo::Structure`
150mm x 150mm steel, Z=[0, 5.5].

| Column | X | Y | Corner A | Corner B |
|--------|---|---|----------|----------|
| B2_dock_1 | -28 | +8 | [-28.075, 7.925, 0.0] | [-27.925, 8.075, 5.5] |
| B2_dock_2 | -28 | -8 | [-28.075, -8.075, 0.0] | [-27.925, -7.925, 5.5] |
| B2_dock_3 | -24 | +8 | [-24.075, 7.925, 0.0] | [-23.925, 8.075, 5.5] |
| B2_dock_4 | -24 | -8 | [-24.075, -8.075, 0.0] | [-23.925, -7.925, 5.5] |

Note: B2_dock_3 and B2_dock_4 at X=-24 are embedded in logistics west wall. Acceptable at LOG400.

---

### B3. Observation Corridor Transfer Beams (2)

Layer: `Type_02_Cargo::Structure`
At Y=+4 and Y=-4, spanning X=[-20, 20], Z=[5.5, 6.0].
Beam depth: 500mm. Width: 400mm.

```
B3_beam_N:   [-20.0, 3.8, 5.5] → [20.0, 4.2, 6.0]
B3_beam_S:   [-20.0, -4.2, 5.5] → [20.0, -3.8, 6.0]
```

Structural note: 16m main span between columns at X=-16 and X=+16, with 4m cantilevers to X=+-20. Beam depth 500mm for 16m span (span/30 = 533mm, rounded to 500mm). These beams bear on main columns at Y=+-8 via cantilever brackets. Corridor floor slab (Z=6.0-6.25) sits directly on beam tops.

---

## SECTION C — OPENINGS (Openings layer)

### C1. West Truck Bay Opening

Layer: `Type_02_Cargo::Openings`
At X=-24 wall, Y=[-3, 3], Z=[0, 4.5].
Modeled as thin marker box in opening plane (structural frame in Section 5).

```
C1_truck_bay_marker:   [-24.05, -3.0, 0.0] → [-23.95, 3.0, 4.5]
```

(1 element — thin plane marker. Structural frame/lintel on L350_Detail.)

---

### C2. East Dispatch Opening

Layer: `Type_02_Cargo::Openings`
At X=24 wall, Y=[-3, 3], Z=[0, 4.5].

```
C2_dispatch_marker:   [23.95, -3.0, 0.0] → [24.05, 3.0, 4.5]
```

(1 element)

---

### C3. South Glazing Wall (Observation Corridor)

Layer: `Type_02_Cargo::Openings`
Curtain wall at Y=-4, X=[-20, 20], Z=[6.75, 9.5] (per C3/C4 corrections).
Modeled as outer frame (4 bars).

```
C3_curtain_top:    [-20.0, -4.05, 9.5] → [20.0, -3.95, 9.6]
C3_curtain_bot:    [-20.0, -4.05, 6.65] → [20.0, -3.95, 6.75]
C3_curtain_jambW:  [-20.0, -4.05, 6.65] → [-19.9, -3.95, 9.6]
C3_curtain_jambE:  [19.9, -4.05, 6.65] → [20.0, -3.95, 9.6]
```

(4 elements. Sill at Z=6.75 = 500mm above floor at Z=6.25.)

---

### C4. North Slot Windows (5)

Layer: `Type_02_Cargo::Openings`
Y=4 (north wall), each 2m wide, Z=[7.25, 9.25] (per C3 correction — shifted up to maintain proportions above new floor level).
Spaced at X = -12, -6, 0, +6, +12.

```
C4_slot_1:   [-13.0, 3.9, 7.25] → [-11.0, 4.1, 9.25]
C4_slot_2:   [-7.0, 3.9, 7.25] → [-5.0, 4.1, 9.25]
C4_slot_3:   [-1.0, 3.9, 7.25] → [1.0, 4.1, 9.25]
C4_slot_4:   [5.0, 3.9, 7.25] → [7.0, 4.1, 9.25]
C4_slot_5:   [11.0, 3.9, 7.25] → [13.0, 4.1, 9.25]
```

(5 elements)

---

### C5. Floor Viewing Slots (3)

Layer: `Type_02_Cargo::Openings`
In corridor floor at Z=[6.0, 6.25] (per C2 correction), at X=[-8, 0, +8], Y=[-2, 2], each 4m x 4m.
Modeled as thin frame boxes (100mm frame around void).

```
C5_viewslot_W_frameN:   [-10.0, 1.9, 6.0] → [-6.0, 2.1, 6.25]
C5_viewslot_W_frameS:   [-10.0, -2.1, 6.0] → [-6.0, -1.9, 6.25]
C5_viewslot_W_frameE:   [-6.1, -2.0, 6.0] → [-5.9, 2.0, 6.25]
C5_viewslot_W_frameW:   [-10.1, -2.0, 6.0] → [-9.9, 2.0, 6.25]

C5_viewslot_C_frameN:   [-2.0, 1.9, 6.0] → [2.0, 2.1, 6.25]
C5_viewslot_C_frameS:   [-2.0, -2.1, 6.0] → [2.0, -1.9, 6.25]
C5_viewslot_C_frameE:   [1.9, -2.0, 6.0] → [2.1, 2.0, 6.25]
C5_viewslot_C_frameW:   [-2.1, -2.0, 6.0] → [-1.9, 2.0, 6.25]

C5_viewslot_E_frameN:   [6.0, 1.9, 6.0] → [10.0, 2.1, 6.25]
C5_viewslot_E_frameS:   [6.0, -2.1, 6.0] → [10.0, -1.9, 6.25]
C5_viewslot_E_frameE:   [9.9, -2.0, 6.0] → [10.1, 2.0, 6.25]
C5_viewslot_E_frameW:   [5.9, -2.0, 6.0] → [6.1, 2.0, 6.25]
```

(12 elements)

---

## SECTION D — CIRCULATION (Circulation layer)

### D1. Logistics Path

Layer: `Type_02_Cargo::Circulation`
Name: `D1_logistics_path`
Polyline at Z=0.5, Y=0.

```
Points: (-24, 0, 0.5) → (-8, 0, 0.5) → (8, 0, 0.5) → (24, 0, 0.5)
```

---

### D2. Public Path

Layer: `Type_02_Cargo::Circulation`
Name: `D2_public_path`
Polyline: ground west → stair → corridor (Z=6.75 per C3 correction) → stair → ground east.

```
Points: (-24, 0, 0) → (-22, 0, 0) → (-20, 0, 6.75) → (20, 0, 6.75) → (22, 0, 0) → (24, 0, 0)
```

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

(7 text dots)

---

## SECTION 1 — ROOF SYSTEM (L300_Roof)

### Slab thickness rationale
- Logistics Hall: 16m column span (Y=+-8) → span/30 = 533mm → use 550mm (0.55 units). Archibase warehouse standard. Columns at Y=+-8 create 16m main span + 3m cantilevers to Y=+-11 walls.
- Observation Corridor: 8m width span (Y=+-4) → span/30 = 267mm → use 250mm (0.25 units). SIA 261 Category C1 public loads.
- Loading Dock Canopy: 4m span → 150mm. Already modeled in A8.

---

### 1.1 Logistics Hall Roof Slab

Layer: `Type_02_Cargo::L300_Roof`
Name: `L300_logistics_roof_slab`

```
Corner A: [-24.0, -11.0, 5.0]
Corner B: [24.0, 11.0, 5.55]
```

Thickness: 550mm. Bottom at Z=5.0 (bearing on 5.0m walls). Top at Z=5.55.
Drainage: 1.5% fall south. Annotate.

---

### 1.2 Logistics Hall Parapets

Non-public roof → SIA 358 minimum 150mm above finished surface.
Finished surface = gravel top = Z = 5.55 + 0.255 = 5.805.
Parapet top = 5.805 + 0.15 = 5.955 → Z = 5.96.
Parapet base = Z = 5.55. Thickness: 300mm matching wall.

```
L300_logistics_parapet_N:   [-24.0, 10.7, 5.55] → [24.0, 11.0, 5.96]
L300_logistics_parapet_S:   [-24.0, -11.0, 5.55] → [24.0, -10.7, 5.96]
L300_logistics_parapet_W:   [-24.0, -11.0, 5.55] → [-23.7, 11.0, 5.96]
L300_logistics_parapet_E:   [23.7, -11.0, 5.55] → [24.0, 11.0, 5.96]
```

(4 elements)

---

### 1.3 Observation Corridor Roof Slab

Layer: `Type_02_Cargo::L300_Roof`
Name: `L300_obs_roof_slab`

```
Corner A: [-20.0, -4.0, 10.0]
Corner B: [20.0, 4.0, 10.25]
```

Thickness: 250mm. Bottom at Z=10.0 (bearing on walls). Top at Z=10.25.
Drainage: 1.5% fall north. Annotate.

---

### 1.4 Observation Corridor Parapets

Public roof (observation deck potential) → SIA 358: 1100mm above finished surface.
Finished surface = gravel top = Z = 10.25 + 0.255 = 10.505.
Parapet top = 10.505 + 1.1 = 11.605 → Z = 11.61.
Parapet base = Z = 10.25.

North, East, West: 250mm thick (matching corridor wall):
```
L300_obs_parapet_N:   [-20.0, 3.75, 10.25] → [20.0, 4.0, 11.61]
L300_obs_parapet_E:   [19.75, -4.0, 10.25] → [20.0, 4.0, 11.61]
L300_obs_parapet_W:   [-20.0, -4.0, 10.25] → [-19.75, 4.0, 11.61]
```

South: 250mm thick, 300mm tall (per C5 correction — upstand only, steel railing assumed above):
```
L300_obs_parapet_S:   [-20.0, -4.0, 10.25] → [20.0, -3.75, 10.55]
```

(4 elements)

---

### 1.5 Loading Dock Canopy

Already modeled as A8 (Z=[5.35, 5.5]).
Drainage: 2% fall west (away from building). Annotate only.

---

### 1.6 Roof Assembly Layers — Logistics Hall (L400_Material)

On top of logistics roof slab (Z=5.55), inside parapets.
Inner faces: N=Y10.7, S=Y-10.7, W=X-23.7, E=X23.7.
Build-up: 200mm XPS + 5mm membrane + 50mm gravel = 255mm.

```
L400_logistics_insulation:   [-23.7, -10.7, 5.55] → [23.7, 10.7, 5.75]    (200mm)
L400_logistics_membrane:     [-23.7, -10.7, 5.75] → [23.7, 10.7, 5.755]   (5mm)
L400_logistics_gravel:       [-23.7, -10.7, 5.755] → [23.7, 10.7, 5.805]  (50mm)
```

(3 elements)

---

### 1.7 Roof Assembly Layers — Observation Corridor (L400_Material)

On top of obs roof slab (Z=10.25), inside parapets.
Inner faces: N=Y3.75, S=Y-3.75 (250mm south parapet), W=X-19.75, E=X19.75.

```
L400_obs_insulation:   [-19.75, -3.75, 10.25] → [19.75, 3.75, 10.45]    (200mm)
L400_obs_membrane:     [-19.75, -3.75, 10.45] → [19.75, 3.75, 10.455]   (5mm)
L400_obs_gravel:       [-19.75, -3.75, 10.455] → [19.75, 3.75, 10.505]  (50mm)
```

(3 elements)

---

### 1.8 Roof Assembly Layers — Canopy (L400_Material)

On canopy slab top (Z=5.5). Membrane only (open-air canopy, no insulation).

```
L400_canopy_membrane:   [-28.0, -8.0, 5.5] → [-24.0, 8.0, 5.505]   (5mm)
```

(1 element)

---

### 1.9 Parapet Edge Conditions (L400_Material)

**Waterproofing upstand** — 20mm wide x 150mm tall.

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
L400_obs_upstand_S:   [-19.75, -3.75, 10.25] → [19.75, -3.73, 10.40]
L400_obs_upstand_E:   [19.73, -3.75, 10.25] → [19.75, 3.75, 10.40]
L400_obs_upstand_W:   [-19.75, -3.75, 10.25] → [-19.73, 3.75, 10.40]
```

**Drip edge** — 30mm x 20mm at outer parapet top corner.

Logistics Hall (parapet top Z=5.96):
```
L400_logistics_drip_N:   [-24.0, 10.97, 5.94] → [24.0, 11.0, 5.96]
L400_logistics_drip_S:   [-24.0, -11.0, 5.94] → [24.0, -10.97, 5.96]
L400_logistics_drip_W:   [-24.0, -11.0, 5.94] → [-23.97, 11.0, 5.96]
L400_logistics_drip_E:   [23.97, -11.0, 5.94] → [24.0, 11.0, 5.96]
```

Observation Corridor (parapet top Z=11.61 for N/E/W, Z=10.55 for S):
```
L400_obs_drip_N:   [-20.0, 3.97, 11.59] → [20.0, 4.0, 11.61]
L400_obs_drip_E:   [19.97, -4.0, 11.59] → [20.0, 4.0, 11.61]
L400_obs_drip_W:   [-20.0, -4.0, 11.59] → [-19.97, 4.0, 11.61]
L400_obs_drip_S:   [-20.0, -4.0, 10.53] → [20.0, -3.97, 10.55]
```

(16 elements total: 8 upstands + 8 drip edges)

---

## SECTION 2 — FORMWORK LINES (L400_Material)

RC walls cast in 2400mm (2.4 unit) lifts.
Formwork lift lines = thin horizontal box proud of wall face by 20mm (0.02 units), 20mm tall.

### Logistics Hall formwork lines

5.0m tall walls → lift at Z=2.4 only.
Exposed outer faces: N (Y=11.0), S (Y=-11.0), W (X=-24.0), E (X=24.0).

Z=2.4 (Z range [2.39, 2.41]):
```
L400_logistics_fw_N_L1:   [-24.0, 11.00, 2.39] → [24.0, 11.02, 2.41]
L400_logistics_fw_S_L1:   [-24.0, -11.02, 2.39] → [24.0, -11.00, 2.41]
L400_logistics_fw_W_L1:   [-24.02, -11.0, 2.39] → [-24.00, 11.0, 2.41]
L400_logistics_fw_E_L1:   [24.00, -11.0, 2.39] → [24.02, 11.0, 2.41]
```

(4 elements)

### Observation Corridor formwork lines

Walls 3.75m tall (Z=6.25 to 10.0, per C8 correction) → lift at Z=8.65 (6.25+2.4).

Exposed outer faces: N (Y=4.0), E (X=20.0), W (X=-20.0). South is glazing — no formwork.

Z=8.65 (Z range [8.64, 8.66]):
```
L400_obs_fw_N_L1:   [-20.0, 4.00, 8.64] → [20.0, 4.02, 8.66]
L400_obs_fw_E_L1:   [20.00, -4.0, 8.64] → [20.02, 4.0, 8.66]
L400_obs_fw_W_L1:   [-20.02, -4.0, 8.64] → [-20.00, 4.0, 8.66]
```

(3 elements)

### Stair volume formwork lines

6.0m tall walls → lifts at Z=2.4 and Z=4.8.

Entry stair exposed faces: N (Y=4.0), S (Y=-4.0). W face removed per C10 (shared with logistics). E face is interior.

Z=2.4:
```
L400_stair_entry_fw_N_L1:   [-24.0, 4.00, 2.39] → [-20.0, 4.02, 2.41]
L400_stair_entry_fw_S_L1:   [-24.0, -4.02, 2.39] → [-20.0, -4.00, 2.41]
```

Z=4.8:
```
L400_stair_entry_fw_N_L2:   [-24.0, 4.00, 4.79] → [-20.0, 4.02, 4.81]
L400_stair_entry_fw_S_L2:   [-24.0, -4.02, 4.79] → [-20.0, -4.00, 4.81]
```

Exit stair exposed faces: N (Y=4.0), S (Y=-4.0). E face removed per C10 (shared with logistics). W face is interior.

Z=2.4:
```
L400_stair_exit_fw_N_L1:   [20.0, 4.00, 2.39] → [24.0, 4.02, 2.41]
L400_stair_exit_fw_S_L1:   [20.0, -4.02, 2.39] → [24.0, -4.00, 2.41]
```

Z=4.8:
```
L400_stair_exit_fw_N_L2:   [20.0, 4.00, 4.79] → [24.0, 4.02, 4.81]
L400_stair_exit_fw_S_L2:   [20.0, -4.02, 4.79] → [24.0, -4.00, 4.81]
```

**Total formwork lines: 4 (logistics) + 3 (obs) + 4 (entry stair) + 4 (exit stair) = 15**

---

## SECTION 3 — EXPANSION JOINTS (L400_Material)

Joint at X=0 through both buildings. 20mm-wide solid boxes. Dark display color.

### Logistics Hall joint at X=0

```
L400_logistics_joint_wallN:   [-0.01, 10.7, 0.0] → [0.01, 11.0, 5.0]
L400_logistics_joint_wallS:   [-0.01, -11.0, 0.0] → [0.01, -10.7, 5.0]
L400_logistics_joint_slab:    [-0.01, -11.0, 5.0] → [0.01, 11.0, 5.55]
```

### Observation Corridor joint at X=0

```
L400_obs_joint_wallN:   [-0.01, 3.75, 6.25] → [0.01, 4.0, 10.0]
L400_obs_joint_slab:    [-0.01, -4.0, 10.0] → [0.01, 4.0, 10.25]
L400_obs_joint_floor:   [-0.01, -4.0, 6.0] → [0.01, 4.0, 6.25]
```

(6 elements)

---

## SECTION 4 — STRUCTURAL CONNECTIONS (L350_Detail)

### 4.1 Column Base Plates — 10 columns

Steel plate: 500mm x 500mm x 30mm (warehouse loads per archibase).
Z position: [-0.03, 0].

Main columns (6):
```
L350_bp_B1_col1:   [-16.25, 7.75, -0.03] → [-15.75, 8.25, 0.0]
L350_bp_B1_col2:   [-16.25, -8.25, -0.03] → [-15.75, -7.75, 0.0]
L350_bp_B1_col3:   [-0.25, 7.75, -0.03] → [0.25, 8.25, 0.0]
L350_bp_B1_col4:   [-0.25, -8.25, -0.03] → [0.25, -7.75, 0.0]
L350_bp_B1_col5:   [15.75, 7.75, -0.03] → [16.25, 8.25, 0.0]
L350_bp_B1_col6:   [15.75, -8.25, -0.03] → [16.25, -7.75, 0.0]
```

Dock columns (4):
```
L350_bp_B2_dock1:   [-28.25, 7.75, -0.03] → [-27.75, 8.25, 0.0]
L350_bp_B2_dock2:   [-28.25, -8.25, -0.03] → [-27.75, -7.75, 0.0]
L350_bp_B2_dock3:   [-24.25, 7.75, -0.03] → [-23.75, 8.25, 0.0]
L350_bp_B2_dock4:   [-24.25, -8.25, -0.03] → [-23.75, -7.75, 0.0]
```

(10 elements)

---

### 4.2 Column Top Bearing Plates

Steel plate: 500mm x 500mm x 20mm.

Main columns top at Z=10.0:
```
L350_tp_B1_col1:   [-16.25, 7.75, 10.0] → [-15.75, 8.25, 10.02]
L350_tp_B1_col2:   [-16.25, -8.25, 10.0] → [-15.75, -7.75, 10.02]
L350_tp_B1_col3:   [-0.25, 7.75, 10.0] → [0.25, 8.25, 10.02]
L350_tp_B1_col4:   [-0.25, -8.25, 10.0] → [0.25, -7.75, 10.02]
L350_tp_B1_col5:   [15.75, 7.75, 10.0] → [16.25, 8.25, 10.02]
L350_tp_B1_col6:   [15.75, -8.25, 10.0] → [16.25, -7.75, 10.02]
```

Dock columns top at Z=5.5:
```
L350_tp_B2_dock1:   [-28.25, 7.75, 5.5] → [-27.75, 8.25, 5.52]
L350_tp_B2_dock2:   [-28.25, -8.25, 5.5] → [-27.75, -7.75, 5.52]
L350_tp_B2_dock3:   [-24.25, 7.75, 5.5] → [-23.75, 8.25, 5.52]
L350_tp_B2_dock4:   [-24.25, -8.25, 5.5] → [-23.75, -7.75, 5.52]
```

(10 elements)

---

### 4.3 Cantilever Brackets at Main Columns

At each of 6 main columns, bracket supports transfer beam at Z=5.5.
Bracket: 400mm(X) x 200mm(Z) x 600mm(Y). Z range: [5.3, 5.5].

Columns at Y=+8 (bracket extends inward toward beam at Y=+4):
```
L350_bracket_col1:   [-16.2, 7.5, 5.3] → [-15.8, 8.1, 5.5]
L350_bracket_col3:   [-0.2, 7.5, 5.3] → [0.2, 8.1, 5.5]
L350_bracket_col5:   [15.8, 7.5, 5.3] → [16.2, 8.1, 5.5]
```

Columns at Y=-8 (bracket extends inward toward beam at Y=-4):
```
L350_bracket_col2:   [-16.2, -8.1, 5.3] → [-15.8, -7.5, 5.5]
L350_bracket_col4:   [-0.2, -8.1, 5.3] → [0.2, -7.5, 5.5]
L350_bracket_col6:   [15.8, -8.1, 5.3] → [16.2, -7.5, 5.5]
```

(6 elements)

---

## SECTION 5 — OPENING FRAMES + LINTELS (L350_Detail)

### 5.1 West Truck Bay Frame + Lintel

Steel frame 100mm x 100mm. RC lintel 300mm deep, extends 300mm beyond opening each side.

```
L350_truck_lintel:       [-24.3, -3.0, 4.5] → [-23.7, 3.0, 4.8]
L350_truck_frame_top:    [-24.1, -3.0, 4.5] → [-23.9, 3.0, 4.6]
L350_truck_frame_jambN:  [-24.1, 2.9, 0.0] → [-23.9, 3.1, 4.6]
L350_truck_frame_jambS:  [-24.1, -3.1, 0.0] → [-23.9, -2.9, 4.6]
```

(4 elements)

### 5.2 East Dispatch Frame + Lintel

```
L350_dispatch_lintel:       [23.7, -3.0, 4.5] → [24.3, 3.0, 4.8]
L350_dispatch_frame_top:    [23.9, -3.0, 4.5] → [24.1, 3.0, 4.6]
L350_dispatch_frame_jambN:  [23.9, 2.9, 0.0] → [24.1, 3.1, 4.6]
L350_dispatch_frame_jambS:  [23.9, -3.1, 0.0] → [24.1, -2.9, 4.6]
```

(4 elements)

### 5.3 Curtain Wall Transom

Structural transom at mid-height of south glazing:
```
L350_curtain_transom:   [-20.0, -4.05, 8.1] → [20.0, -3.95, 8.2]
```

(1 element)

### 5.4 Slot Window Frames (5)

Steel frames around each north wall slot window:
```
L350_slot_frame_1:   [-13.1, 3.9, 7.15] → [-10.9, 4.1, 9.35]
L350_slot_frame_2:   [-7.1, 3.9, 7.15] → [-4.9, 4.1, 9.35]
L350_slot_frame_3:   [-1.1, 3.9, 7.15] → [1.1, 4.1, 9.35]
L350_slot_frame_4:   [4.9, 3.9, 7.15] → [7.1, 4.1, 9.35]
L350_slot_frame_5:   [10.9, 3.9, 7.15] → [13.1, 4.1, 9.35]
```

(5 elements)

### 5.5 Floor Viewing Slot Edge Frames (3)

Steel edge trim around floor viewing slots. 50mm x 50mm angle at slab edge.
Modeled as thin solid slab representing edge condition (void is implicit).

```
L350_viewslot_edge_W:   [-10.05, -2.05, 6.2] → [-5.95, 2.05, 6.25]
L350_viewslot_edge_C:   [-2.05, -2.05, 6.2] → [2.05, 2.05, 6.25]
L350_viewslot_edge_E:   [5.95, -2.05, 6.2] → [10.05, 2.05, 6.25]
```

(3 elements)

**Total Section 5: 4 + 4 + 1 + 5 + 3 = 17 elements**

---

## SECTION 6 — FACADE PANEL JOINTS (L400_Material)

5mm wide x 20mm deep incised vertical joints on logistics hall N/S faces.
Full height Z=[0, 5.0]. At X = -16, -8, 0, +8, +16 (column lines).

North face (outer at Y=+11.0):
```
L400_pj_N_X-16:   [-16.0025, 10.98, 0.0] → [-15.9975, 11.00, 5.0]
L400_pj_N_X-8:    [-8.0025, 10.98, 0.0] → [-7.9975, 11.00, 5.0]
L400_pj_N_X0:     [-0.0025, 10.98, 0.0] → [0.0025, 11.00, 5.0]
L400_pj_N_X8:     [7.9975, 10.98, 0.0] → [8.0025, 11.00, 5.0]
L400_pj_N_X16:    [15.9975, 10.98, 0.0] → [16.0025, 11.00, 5.0]
```

South face (outer at Y=-11.0):
```
L400_pj_S_X-16:   [-16.0025, -11.00, 0.0] → [-15.9975, -10.98, 5.0]
L400_pj_S_X-8:    [-8.0025, -11.00, 0.0] → [-7.9975, -10.98, 5.0]
L400_pj_S_X0:     [-0.0025, -11.00, 0.0] → [0.0025, -10.98, 5.0]
L400_pj_S_X8:     [7.9975, -11.00, 0.0] → [8.0025, -10.98, 5.0]
L400_pj_S_X16:    [15.9975, -11.00, 0.0] → [16.0025, -10.98, 5.0]
```

(10 elements)

---

## SECTION 7 — WALL KICKERS (L350_Detail)

50mm x 50mm RC kicker at wall base (Z=[0, 0.05]), outer face.

### Logistics Hall kickers

```
L350_kicker_logistics_N:   [-24.0, 11.0, 0.0] → [24.0, 11.05, 0.05]
L350_kicker_logistics_S:   [-24.0, -11.05, 0.0] → [24.0, -11.0, 0.05]
L350_kicker_logistics_W:   [-24.05, -11.0, 0.0] → [-24.0, 11.0, 0.05]
L350_kicker_logistics_E:   [24.0, -11.0, 0.0] → [24.05, 11.0, 0.05]
```

### Stair volume kickers

Entry stair (N and S faces only — W shared with logistics, E is interior):
```
L350_kicker_stair_entry_N:   [-24.0, 4.0, 0.0] → [-20.0, 4.05, 0.05]
L350_kicker_stair_entry_S:   [-24.0, -4.05, 0.0] → [-20.0, -4.0, 0.05]
```

Exit stair (N and S faces only — E shared with logistics, W is interior):
```
L350_kicker_stair_exit_N:   [20.0, 4.0, 0.0] → [24.0, 4.05, 0.05]
L350_kicker_stair_exit_S:   [20.0, -4.05, 0.0] → [24.0, -4.0, 0.05]
```

(8 elements total: 4 logistics + 2 entry stair + 2 exit stair)

Note: Stair W/E kickers removed per C7/C10 — those faces are shared with logistics walls which have their own kickers.

---

## EXECUTION SUMMARY

### Element count by section

| Section | Type | Layer | Count |
|---------|------|-------|-------|
| A1 | Logistics walls | Volumes | 4 |
| A2 | Logistics floor slab | Volumes | 1 |
| A3 | Sorting bay walls | Volumes | 2 |
| A4 | Observation corridor walls (N + S frame + E/W upper) | Volumes | 4 |
| A5 | Observation corridor floor | Volumes | 1 |
| A6 | Entry stair (3 walls + landing) | Volumes | 4 |
| A7 | Exit stair (3 walls + landing) | Volumes | 4 |
| A8 | Loading dock canopy | Volumes | 1 |
| B1 | Main columns | Structure | 6 |
| B2 | Dock columns | Structure | 4 |
| B3 | Transfer beams | Structure | 2 |
| C1 | Truck bay marker | Openings | 1 |
| C2 | Dispatch marker | Openings | 1 |
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
| 2 | Formwork lines | L400_Material | 15 |
| 3 | Expansion joints | L400_Material | 6 |
| 4.1 | Column base plates | L350_Detail | 10 |
| 4.2 | Column top plates | L350_Detail | 10 |
| 4.3 | Cantilever brackets | L350_Detail | 6 |
| 5 | Opening frames + lintels | L350_Detail | 17 |
| 6 | Facade panel joints | L400_Material | 10 |
| 7 | Wall kickers | L350_Detail | 8 |
| **TOTAL** | | | **183 elements** |

### Element count by layer

| Layer | Count |
|-------|-------|
| Type_02_Cargo::Volumes | 21 |
| Type_02_Cargo::Circulation | 5 |
| Type_02_Cargo::Structure | 12 |
| Type_02_Cargo::Openings | 23 |
| Type_02_Cargo::Annotations | 7 |
| Type_02_Cargo::L300_Roof | 10 |
| Type_02_Cargo::L350_Detail | 51 |
| Type_02_Cargo::L400_Material | 54 |
| **TOTAL** | **183** |

(Section sum and layer sum agree: 183 elements.)

---

### Z-Stack Summary

| Z Level | What |
|---------|------|
| -0.30 | Bottom of logistics ground slab |
| -0.03 | Bottom of column base plates |
| 0.00 | Finished floor level (logistics hall) |
| 0.05 | Top of wall kickers |
| 0.50 | Logistics circulation path |
| 2.40 | First formwork lift line (logistics, stairs) |
| 2.50 | Logistics annotation height |
| 4.50 | Top of truck bay / dispatch openings |
| 4.80 | Second formwork lift (stairs), lintel top |
| 5.00 | Top of logistics hall walls / bottom of logistics roof slab |
| 5.30 | Bottom of cantilever brackets |
| 5.35 | Bottom of loading dock canopy |
| 5.50 | Top of transfer beams / bottom of dock canopy slab / top of cantilever brackets |
| 5.55 | Top of logistics roof slab |
| 5.75 | Bottom of stair landing slabs |
| 5.805 | Top of logistics gravel (finished roof surface) |
| 5.96 | Top of logistics parapets |
| 6.00 | Top of stair volumes / bottom of obs corridor floor slab / bottom of transfer beam top |
| 6.25 | Top of obs corridor floor slab / base of obs corridor walls |
| 6.75 | Walking level in obs corridor / bottom of south glazing |
| 7.25 | Bottom of north slot windows |
| 8.10 | Curtain wall transom |
| 8.65 | Obs corridor formwork lift line |
| 9.25 | Top of north slot windows |
| 9.50 | Top of south glazing |
| 10.00 | Top of obs corridor walls / bottom of obs roof slab |
| 10.02 | Top of column top bearing plates |
| 10.25 | Top of obs roof slab |
| 10.505 | Top of obs gravel (finished roof surface) |
| 10.55 | Top of south parapet (obs corridor) |
| 11.61 | Top of N/E/W parapets (obs corridor) — highest point |

---

### Build order

1. Create 8 layers
2. A1: Logistics Hall walls (4 boxes, Volumes)
3. A2: Logistics floor slab (1 box, Volumes)
4. A3: Sorting bay walls (2 boxes, Volumes)
5. A5: Observation corridor floor slab (1 box, Volumes)
6. A4: Observation corridor walls (4 boxes, Volumes)
7. A6: Entry stair volume (4 boxes, Volumes)
8. A7: Exit stair volume (4 boxes, Volumes)
9. A8: Loading dock canopy (1 box, Volumes)
10. B1: Main columns (6 boxes, Structure)
11. B2: Dock columns (4 boxes, Structure)
12. B3: Transfer beams (2 boxes, Structure)
13. C1-C2: Opening markers (2 boxes, Openings)
14. C3: South glazing curtain wall (4 boxes, Openings)
15. C4: North slot windows (5 boxes, Openings)
16. C5: Floor viewing slot frames (12 boxes, Openings)
17. D1-D2: Circulation paths (2 polylines, Circulation)
18. D3: Visual connection lines (3 lines, Circulation)
19. E1: Text dots (7 dots, Annotations)
20. 1.1: Logistics roof slab (1 box, L300_Roof)
21. 1.2: Logistics parapets (4 boxes, L300_Roof)
22. 1.3: Obs corridor roof slab (1 box, L300_Roof)
23. 1.4: Obs corridor parapets (4 boxes, L300_Roof)
24. 1.6-1.8: Roof assembly layers (7 boxes, L400_Material)
25. 1.9: Parapet edge conditions (16 boxes, L400_Material)
26. Sec 2: Formwork lines (15 boxes, L400_Material) — batch as one Python script
27. Sec 3: Expansion joints (6 boxes, L400_Material)
28. Sec 4.1: Column base plates (10 boxes, L350_Detail)
29. Sec 4.2: Column top plates (10 boxes, L350_Detail)
30. Sec 4.3: Cantilever brackets (6 boxes, L350_Detail)
31. Sec 5: Opening frames + lintels (17 boxes, L350_Detail)
32. Sec 6: Facade panel joints (10 boxes, L400_Material)
33. Sec 7: Wall kickers (8 boxes, L350_Detail)

---

### Executor notes

1. All coordinates are meter-scale in a centimeter-unit Rhino doc. Use numbers exactly as written.
2. Do NOT multiply by 100.
3. Use `rhino_execute_python_code` with `Box()` (BoundingBox from two corner points) for all box elements.
4. Use `AddPolyline()` for D1/D2, `AddLine()` for D3, `AddTextDot()` for E1.
5. Batch by section — formwork lines in one script, base plates in one script, etc.
6. If a boolean or complex operation fails, fall back to additive geometry only and note it.
7. After all geometry is placed: capture Perspective, Top, and Section (X=0 cut) viewports.
8. **Target instance: `"envelope"` (port 9002). All MCP calls must include `target: "envelope"`.** NOT "lock_02".
9. Opening markers (C1/C2) and structural frames (Section 5) both exist — C-series on Openings layer for visibility toggle, Section 5 on L350_Detail for structural representation.
10. Expansion joint boxes should be assigned dark/black display color to read as gaps.
11. D3 visual connection lines should be set to dashed linetype if available.

---

## DECISION LOG

| Decision | Verdict | Rationale |
|----------|---------|-----------|
| Logistics roof slab thickness | 550mm | 16m span (Y=+-8), span/30 = 533mm, rounded up. Archibase warehouse industrial standard with 0.4-0.6% rebar. |
| Obs corridor floor slab thickness | 250mm | 8m span (Y direction between beams), span/30 = 267mm, rounded to 250mm. SIA 261 Cat C1 lighter loads. |
| Obs corridor roof slab thickness | 250mm | Same 8m span logic. |
| Floor slab Z position | Z=[6.0, 6.25] | Slab sits ON TOP of transfer beams (Z=5.5-6.0). Original Z=5.75-6.0 created beam/slab conflict. |
| Obs corridor wall base | Z=6.25 | Walls start at slab top. Internal ceiling height 3.75m (acceptable for public corridor). |
| Transfer beam depth | 500mm | 16m main span (span/30 = 533mm), 400mm width provides additional stiffness. 4m cantilevers to stair zones. |
| Logistics parapets | 150mm above gravel, full perimeter | SIA 358 non-public roof minimum. |
| Obs corridor parapets N/E/W | 1100mm above gravel | SIA 358 public access requirement. |
| Obs corridor parapet S | 300mm RC upstand + assumed steel railing | Curtain wall head condition — full RC parapet inappropriate over glazing. |
| Stair/corridor wall overlap | Keep stair walls (300mm), add separate upper corridor end walls | Stair walls thicker (300mm vs 250mm), structurally govern. Upper walls start above stair top. |
| Stair/logistics wall overlap | Remove duplicate stair W/E walls | Logistics perimeter walls serve as shared boundary. |
| Expansion joints | At X=0, through all walls and slabs | 48m logistics hall and 40m corridor both exceed 30m threshold. |
| Base plate thickness | 30mm | Heavier than lock_01 (25mm) per archibase warehouse loads. |
| Formwork lifts | 2400mm per archibase | Standard RC formwork height. |
| Facade panel joints | At column lines X=-16,-8,0,+8,+16 | Natural construction joint locations at structural grid. |
| Coordinate system | Meter-scale throughout | Match existing model convention. No x100 conversion. |
| MCP target | "envelope" (port 9002) | Per project instruction — NOT "lock_02". |
