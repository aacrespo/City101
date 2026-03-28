# Lock Type 01 — Border Lock
# LOG400 Upgrade: ROUNDTABLE-APPROVED Execution Spec
# Status: APPROVED — ready for executor
# Approved by: Roundtable Reviewer
# Date: 2026-03-27

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry was built in METER-SCALE values (X=-16 to 16, Z=0 to 7.0).
"7.0" in Rhino = 7.0 as a number, displayed as "7 cm" but conceptually 7m.

**ALL coordinates in this spec are meter-scale. Use them exactly as written.**
**Do NOT multiply by 100. Do NOT convert.**

X = corridor axis (negative = System A / Entry, positive = System B / Exit)
Y = lateral axis (positive = North, negative = South)
Z = vertical (0 = finished floor level)

---

## CORRECTIONS FROM ROUNDTABLE REVIEW

The following errors in the draft spec were resolved before approval:

| # | Issue | Resolution |
|---|-------|-----------|
| C1 | Slab thickness 200mm too thin for 12m span | Entry/Exit slabs: 400mm (0.4 units). Gate slab: 300mm (0.3 units). |
| C2 | Gate column labels wrong — "NW(-4,-4)" is actually SW | Correct labels: NW=(-4,+4), NE=(+4,+4), SE=(+4,-4). The removed column was SW(-4,-4). |
| C3 | Wall kicker N/S labels swapped | "Entry Hall N base" at +Y, "Entry Hall S base" at -Y. Corrected throughout. |
| C4 | Gate roof: no separate parapet boxes needed | Gate walls extend to Z=7.0 and ARE the parapet. No separate gate parapet geometry. |
| C5 | Roof layer extents extend under parapet walls | Insulation/membrane/gravel inset from parapet inner face throughout. Corrected. |
| C6 | Draft formwork lift heights inconsistent with model | Lift lines at Z=2.4 and Z=4.8 (2400mm lifts). Confirmed correct. |

---

## LAYERS TO CREATE

```
Type_01_Border::L300_Roof    — RGB(200,180,160)  — roof structural slabs, parapets
Type_01_Border::L350_Detail  — RGB(160,140,120)  — connections, frames, kickers
Type_01_Border::L400_Material — RGB(120,100,80)  — formwork, joints, hardware, edge conditions
```

Do NOT rename or alter existing layers:
- `Type_01_Border::Volumes`
- `Type_01_Border::Circulation`
- `Type_01_Border::Structure`
- `Type_01_Border::Openings`
- `Type_01_Border::Annotations`

---

## SECTION 1 — ROOF SYSTEM (L300_Roof)

### Slab thickness rationale
- Entry Hall 12m span → span/30 = 400mm (0.4 units)
- Gate Zone 8m span → span/30 = 267mm → use 300mm (0.3 units, monumental)
- Exit Hall 12m span → span/30 = 400mm (0.4 units)
- Bearing: slabs sit ON TOP of existing wall shells (slabs begin at top of wall)

---

### 1.1 Entry Hall Roof Slab

Layer: `Type_01_Border::L300_Roof`
Name: `L300_entry_roof_slab`

```
Corner A: [-16.0, -7.0, 5.0]
Corner B: [-4.0,   7.0, 5.4]
```
Thickness: 0.4 units (400mm)
Top face at Z=5.4, bottom face at Z=5.0 (bearing on existing 5.0m walls)

Drainage: 1.5% fall south (toward Y=-7.0). Drop = 14.0 × 0.015 = 0.21 units over full Y span.
Modeled as flat box at LOG300. Annotate fall direction as text dot on Annotations layer.

---

### 1.2 Entry Hall Parapets

Parapet height: 500mm (0.5 units) above top of slab (Z=5.4)
Parapet thickness: 300mm (0.3 units) matching existing wall thickness
Parapet top: Z = 5.4 + 0.5 = 5.9
Parapet Z range: [5.4, 5.9]

Note: Parapets extend the existing wall above the roof slab. East face (X=-4) abuts Gate — no parapet there.

```
L300_entry_parapet_N:   [-16.0,  6.7, 5.4] → [-4.0,  7.0, 5.9]
L300_entry_parapet_S:   [-16.0, -7.0, 5.4] → [-4.0, -6.7, 5.9]
L300_entry_parapet_W:   [-16.0, -7.0, 5.4] → [-15.7, 7.0, 5.9]
```
(3 parapet boxes; no east parapet — gate wall continues above)

---

### 1.3 Gate / Control Zone Roof Slab

Layer: `Type_01_Border::L300_Roof`
Name: `L300_gate_roof_slab`

```
Corner A: [-4.0, -4.0, 7.0]
Corner B: [ 4.0,  4.0, 7.3]
```
Thickness: 0.3 units (300mm)
Top face at Z=7.3, bottom face at Z=7.0 (bearing on existing 7.0m gate walls)

Drainage: FLAT (symbolic monument roof). No drainage fall. Annotate.

Gate parapets: NOT modeled as separate elements.
The gate wall shells already extend to Z=7.0. The 7m wall top IS the parapet condition.
This is a deliberate architectural decision: the wall-as-parapet reads as a monumental plinth edge.

---

### 1.4 Exit Hall Roof Slab

Layer: `Type_01_Border::L300_Roof`
Name: `L300_exit_roof_slab`

```
Corner A: [4.0,  -7.0, 6.0]
Corner B: [16.0,  7.0, 6.4]
```
Thickness: 0.4 units (400mm)
Top face at Z=6.4, bottom face at Z=6.0 (bearing on existing 6.0m walls)

Drainage: 1.5% fall north (toward Y=+7.0). Annotate.

---

### 1.5 Exit Hall Parapets

Parapet Z range: [6.4, 6.9]
(0.5 units above slab top Z=6.4)

Note: West face (X=+4) abuts Gate — no parapet there.

```
L300_exit_parapet_N:   [4.0,  6.7, 6.4] → [16.0,  7.0, 6.9]
L300_exit_parapet_S:   [4.0, -7.0, 6.4] → [16.0, -6.7, 6.9]
L300_exit_parapet_E:   [15.7, -7.0, 6.4] → [16.0,  7.0, 6.9]
```
(3 parapet boxes)

---

### 1.6 Roof Assembly Layers — Entry Hall (L400_Material)

Sits inside parapets, on top of roof slab (Z=5.4).
Inset from parapet inner faces: inner faces at Y=±6.7 (N/S parapets) and X=-15.7 (W parapet).
East open face: insulation terminates at X=-4.0 (gate wall face).

Total build-up thickness: 120mm XPS + 5mm membrane + 50mm gravel = 175mm = 0.175 units
Assembly top: Z = 5.4 + 0.175 = 5.575

```
L400_entry_insulation:   [-15.7, -6.7, 5.40] → [-4.0, 6.7, 5.52]   (120mm)
L400_entry_membrane:     [-15.7, -6.7, 5.52] → [-4.0, 6.7, 5.525]  (5mm)
L400_entry_gravel:       [-15.7, -6.7, 5.525] → [-4.0, 6.7, 5.575] (50mm)
```

---

### 1.7 Roof Assembly Layers — Gate Zone (L400_Material)

Sits inside gate wall top perimeter, on top of gate slab (Z=7.3).
Gate wall inner faces: at ±3.6 (400mm walls, inner face = 4.0 - 0.4 = 3.6).

```
L400_gate_insulation:   [-3.6, -3.6, 7.30] → [3.6, 3.6, 7.42]   (120mm)
L400_gate_membrane:     [-3.6, -3.6, 7.42] → [3.6, 3.6, 7.425]  (5mm)
L400_gate_gravel:       [-3.6, -3.6, 7.425] → [3.6, 3.6, 7.475] (50mm)
```

---

### 1.8 Roof Assembly Layers — Exit Hall (L400_Material)

Sits inside parapets, on top of exit slab (Z=6.4).
Inset: X from +4.0 to +15.7, Y from -6.7 to +6.7.

```
L400_exit_insulation:   [4.0, -6.7, 6.40] → [15.7, 6.7, 6.52]   (120mm)
L400_exit_membrane:     [4.0, -6.7, 6.52] → [15.7, 6.7, 6.525]  (5mm)
L400_exit_gravel:       [4.0, -6.7, 6.525] → [15.7, 6.7, 6.575] (50mm)
```

---

### 1.9 Parapet Edge Conditions (L400_Material)

**Waterproofing upstand** — 20mm wide × 150mm tall thin box against inner face of each parapet.
Runs at membrane level (Z = slab top = base of upstand).

Entry Hall (slab top Z=5.4, upstand Z=[5.4, 5.55]):
```
L400_entry_upstand_N:  [-15.7, 6.68, 5.4] → [-4.0, 6.70, 5.55]
L400_entry_upstand_S:  [-15.7, -6.70, 5.4] → [-4.0, -6.68, 5.55]
L400_entry_upstand_W:  [-15.72, -6.7, 5.4] → [-15.70, 6.7, 5.55]
```

Exit Hall (slab top Z=6.4, upstand Z=[6.4, 6.55]):
```
L400_exit_upstand_N:   [4.0, 6.68, 6.4] → [15.7, 6.70, 6.55]
L400_exit_upstand_S:   [4.0, -6.70, 6.4] → [15.7, -6.68, 6.55]
L400_exit_upstand_E:   [15.68, -6.7, 6.4] → [15.70, 6.7, 6.55]
```

**Drip edge** — 30mm × 20mm box at outer top corner of each parapet.

Entry Hall (parapet top Z=5.9, outer parapet faces at Y=±7.0 and X=-16.0):
```
L400_entry_drip_N:   [-15.7, 6.97, 5.87] → [-4.0, 7.0, 5.9]
L400_entry_drip_S:   [-15.7, -7.0, 5.87] → [-4.0, -6.97, 5.9]
L400_entry_drip_W:   [-16.0, -7.0, 5.87] → [-15.97, 7.0, 5.9]
```

Exit Hall (parapet top Z=6.9):
```
L400_exit_drip_N:    [4.0,  6.97, 6.87] → [15.7,  7.0, 6.9]
L400_exit_drip_S:    [4.0, -7.0,  6.87] → [15.7, -6.97, 6.9]
L400_exit_drip_E:    [15.97, -7.0, 6.87] → [16.0, 7.0, 6.9]
```

---

## SECTION 2 — FORMWORK LINES (L400_Material)

RC walls cast in 2400mm (2.4 unit) lifts.
Formwork lift lines = thin horizontal box proud of wall face by 20mm (0.02 units), 20mm tall.

Wall thicknesses: Gate = 400mm (0.4 units), Entry/Exit = 300mm (0.3 units).

Gate outer faces: X=±4.4 (E/W), Y=±4.4 (N/S).
Entry outer faces: X=-16.3 (W), Y=±7.3 (N/S). [wall outer = inner ±0.3]
Exit outer faces: X=+16.3 (E), Y=±7.3 (N/S).

**Lift elevations:**
- Gate (7.0m total): lifts at Z=2.4 and Z=4.8
- Entry Hall (5.0m total): lift at Z=2.4 only
- Exit Hall (6.0m total): lifts at Z=2.4 and Z=4.8

---

### Gate formwork lines (8 elements)

Z=2.4 lift (Z range [2.39, 2.41]):
```
L400_gate_fw_N_L1:  [-4.4, 4.40, 2.39] → [4.4,  4.42, 2.41]
L400_gate_fw_S_L1:  [-4.4, -4.42, 2.39] → [4.4, -4.40, 2.41]
L400_gate_fw_E_L1:  [4.40, -4.4, 2.39] → [4.42,  4.4, 2.41]
L400_gate_fw_W_L1:  [-4.42, -4.4, 2.39] → [-4.40, 4.4, 2.41]
```

Z=4.8 lift (Z range [4.79, 4.81]):
```
L400_gate_fw_N_L2:  [-4.4, 4.40, 4.79] → [4.4,  4.42, 4.81]
L400_gate_fw_S_L2:  [-4.4, -4.42, 4.79] → [4.4, -4.40, 4.81]
L400_gate_fw_E_L2:  [4.40, -4.4, 4.79] → [4.42,  4.4, 4.81]
L400_gate_fw_W_L2:  [-4.42, -4.4, 4.79] → [-4.40, 4.4, 4.81]
```

### Entry Hall formwork lines (3 elements)

Z=2.4 lift only. Exposed outer faces: N (Y=+7.3), S (Y=-7.3), W (X=-16.3).
East end (X=-4.3) is interior — no formwork line.

```
L400_entry_fw_N_L1:  [-16.3, 7.30, 2.39] → [-4.3,  7.32, 2.41]
L400_entry_fw_S_L1:  [-16.3, -7.32, 2.39] → [-4.3, -7.30, 2.41]
L400_entry_fw_W_L1:  [-16.32, -7.3, 2.39] → [-16.30, 7.3, 2.41]
```

### Exit Hall formwork lines (6 elements)

Exposed outer faces: N (Y=+7.3), S (Y=-7.3), E (X=+16.3).
West end (X=+4.3) is interior — no formwork line.

Z=2.4 lift:
```
L400_exit_fw_N_L1:   [4.3,  7.30, 2.39] → [16.3,  7.32, 2.41]
L400_exit_fw_S_L1:   [4.3, -7.32, 2.39] → [16.3, -7.30, 2.41]
L400_exit_fw_E_L1:   [16.30, -7.3, 2.39] → [16.32, 7.3, 2.41]
```

Z=4.8 lift:
```
L400_exit_fw_N_L2:   [4.3,  7.30, 4.79] → [16.3,  7.32, 4.81]
L400_exit_fw_S_L2:   [4.3, -7.32, 4.79] → [16.3, -7.30, 4.81]
L400_exit_fw_E_L2:   [16.30, -7.3, 4.79] → [16.32, 7.3, 4.81]
```

**Total formwork line boxes: 8 + 3 + 6 = 17**

---

## SECTION 3 — EXPANSION JOINTS (L400_Material)

Per FLAG 3 verdict: joints are continuous through walls AND roof slabs.
Modeled as 20mm-wide colored solid boxes (no boolean required).

Entry Hall joint at X = -10.0:
```
L400_entry_joint_wall:   [-10.01, -7.3, 0.0] → [-9.99, 7.3, 5.0]    (full wall height)
L400_entry_joint_slab:   [-10.01, -7.0, 5.0] → [-9.99, 7.0, 5.4]    (through roof slab)
```

Exit Hall joint at X = +10.0:
```
L400_exit_joint_wall:    [9.99, -7.3, 0.0] → [10.01, 7.3, 6.0]      (full wall height)
L400_exit_joint_slab:    [9.99, -7.0, 6.0] → [10.01, 7.0, 6.4]      (through roof slab)
```

Assign a dark display color to these objects (black or near-black) to read as gaps.
**Total: 4 joint elements**

---

## SECTION 4 — STRUCTURAL CONNECTIONS (L350_Detail)

### 4.1 Column Base Plates — 7 columns (per FLAG 1 verdict)

Verdict: Gate has 3 columns (NW, NE, SE). SW was removed. Plus 2 Entry + 2 Exit = 7 total.

**Corrected column positions (C2 correction applied):**
| Column ID | Label | X | Y |
|-----------|-------|---|---|
| C1 | Gate NW | -4.0 | +4.0 |
| C2 | Gate NE | +4.0 | +4.0 |
| C3 | Gate SE | +4.0 | -4.0 |
| C4 | Entry S | -10.0 | -3.5 |
| C5 | Entry N | -10.0 | +3.5 |
| C6 | Exit S  | +10.0 | -3.5 |
| C7 | Exit N  | +10.0 | +3.5 |

Note: Gate SW column (-4.0, -4.0) was removed at roundtable.

Steel plate: 500mm × 500mm × 25mm (0.5 × 0.5 × 0.025 units)
Z position: [-0.025, 0] (plate cast into floor slab, top flush with floor)

```
L350_bp_C1_gate_NW:   [-4.25, 3.75, -0.025] → [-3.75, 4.25, 0.0]
L350_bp_C2_gate_NE:   [3.75, 3.75, -0.025] → [4.25, 4.25, 0.0]
L350_bp_C3_gate_SE:   [3.75, -4.25, -0.025] → [4.25, -3.75, 0.0]
L350_bp_C4_entry_S:   [-10.25, -3.75, -0.025] → [-9.75, -3.25, 0.0]
L350_bp_C5_entry_N:   [-10.25, 3.25, -0.025] → [-9.75, 3.75, 0.0]
L350_bp_C6_exit_S:    [9.75, -3.75, -0.025] → [10.25, -3.25, 0.0]
L350_bp_C7_exit_N:    [9.75, 3.25, -0.025] → [10.25, 3.75, 0.0]
```

---

### 4.2 Column Top Bearing Plates

Steel plate: 500mm × 500mm × 20mm (0.5 × 0.5 × 0.02 units)
Sits at column top, below roof slab.

Gate columns top at Z=5.5 (columns support bridge level, not roof slab):
```
L350_tp_C1_gate_NW:   [-4.25, 3.75, 5.5] → [-3.75, 4.25, 5.52]
L350_tp_C2_gate_NE:   [3.75, 3.75, 5.5] → [4.25, 4.25, 5.52]
L350_tp_C3_gate_SE:   [3.75, -4.25, 5.5] → [4.25, -3.75, 5.52]
```

Entry columns top at Z=5.0:
```
L350_tp_C4_entry_S:   [-10.25, -3.75, 5.0] → [-9.75, -3.25, 5.02]
L350_tp_C5_entry_N:   [-10.25, 3.25, 5.0] → [-9.75, 3.75, 5.02]
```

Exit columns top at Z=6.0:
```
L350_tp_C6_exit_S:    [9.75, -3.75, 6.0] → [10.25, -3.25, 6.02]
L350_tp_C7_exit_N:    [9.75, 3.25, 6.0] → [10.25, 3.75, 6.02]
```

---

### 4.3 Bridge Beam Brackets (per FLAG 2 verdict)

Beam at Y=0, X=[-4,4], Z=[4.7,5.0]. Bottom face at Z=4.7.
Brackets sit BELOW beam bottom, embedded 200mm into gate wall face.

Bracket dimensions: 300mm (X, depth into wall) × 200mm (Z, height) × 600mm (Y, width = beam width)
In model units: 0.3 (X) × 0.2 (Z) × 0.6 (Y)
Z range: [4.5, 4.7] (bracket top flush with beam bottom face at Z=4.7)

West bracket (embedded in Gate west wall, wall face at X=-4.0, inner face at X=-3.6):
- Extends 200mm into wall: X from -4.0 to -4.2
- Y centered on beam: [-0.3, +0.3]
```
L350_bracket_W:   [-4.2, -0.3, 4.5] → [-4.0, 0.3, 4.7]
```

East bracket (embedded in Gate east wall, wall face at X=+4.0):
- Extends 200mm into wall: X from +4.0 to +4.2
```
L350_bracket_E:   [4.0, -0.3, 4.5] → [4.2, 0.3, 4.7]
```

Note: brackets embed only 200mm into the 400mm-thick gate wall — they do not penetrate through.

---

### 4.4 Wall Kickers (L350_Detail)

50mm × 50mm RC kicker at wall base (Z=[0, 0.05]), full wall perimeter.
In model units: 0.05 wide × 0.05 tall.

Kicker runs on OUTER face of wall. Outer face coordinates:
- Entry Hall walls: outer Y=±7.3 (N/S), outer X=-16.3 (W)
- Gate walls: outer Y=±4.4 (N/S), outer X=±4.4 (E/W)
- Exit Hall walls: outer Y=±7.3 (N/S), outer X=+16.3 (E)

```
Entry kickers (C3 correction: N at +Y, S at -Y):
L350_kicker_entry_N:   [-16.0, 7.0,  0.0] → [-4.0,  7.05, 0.05]
L350_kicker_entry_S:   [-16.0, -7.05, 0.0] → [-4.0, -7.0,  0.05]
L350_kicker_entry_W:   [-16.05, -7.0, 0.0] → [-16.0, 7.0,  0.05]

Gate kickers:
L350_kicker_gate_N:    [-4.0, 4.0,  0.0] → [4.0,  4.05, 0.05]
L350_kicker_gate_S:    [-4.0, -4.05, 0.0] → [4.0, -4.0,  0.05]
L350_kicker_gate_E:    [4.0,  -4.0, 0.0] → [4.05, 4.0,  0.05]
L350_kicker_gate_W:    [-4.05, -4.0, 0.0] → [-4.0, 4.0,  0.05]

Exit kickers (no west kicker — abuts gate):
L350_kicker_exit_N:    [4.0,  7.0,  0.0] → [16.0,  7.05, 0.05]
L350_kicker_exit_S:    [4.0, -7.05, 0.0] → [16.0, -7.0,  0.05]
L350_kicker_exit_E:    [16.0, -7.0, 0.0] → [16.05, 7.0,  0.05]
```

Total kickers: 3 (Entry) + 4 (Gate) + 3 (Exit) = **10 elements**

---

## SECTION 5 — GATE HARDWARE (L400_Material)

Passage dimensions from original brief:
- Primary passage: center of gate, Y=[-1.25, +1.25], full Z=[0, 3.5]
- Rejection passage: Y=[-3.0, -1.0] per FLAG 4 verdict

All hardware mounted on Gate west wall inner face at X=-4.0 (inner face = X=-3.6, but hardware plate surface sits at X=-4.0 outer face side, mounting through wall — simplified as surface-mounted on inner face).
Modeled as small solid boxes on inside face of west gate wall.

**Primary passage (Y=[-1.25, +1.25]):**

Bolt bar (horizontal, at Z=2.0, 30mm thick):
```
L400_gate_bolt_primary:   [-4.0, -1.2, 2.0] → [-3.97, 1.2, 2.03]
```

Hinges (3×, 150mm×150mm×20mm plates):
```
L400_gate_hinge_P1:   [-4.0, -0.075, 0.5] → [-3.98, 0.075, 0.65]
L400_gate_hinge_P2:   [-4.0, -0.075, 1.75] → [-3.98, 0.075, 1.90]
L400_gate_hinge_P3:   [-4.0, -0.075, 3.0] → [-3.98, 0.075, 3.15]
```

**Rejection passage (Y=[-3.0, -1.0], per FLAG 4 verdict):**

Bolt bar (at Z=1.8):
```
L400_gate_bolt_reject:   [-4.0, -2.9, 1.8] → [-3.97, -1.1, 1.83]
```

Hinges (2×):
```
L400_gate_hinge_R1:   [-4.0, -2.075, 0.5] → [-3.98, -1.925, 0.65]
L400_gate_hinge_R2:   [-4.0, -2.075, 2.25] → [-3.98, -1.925, 2.40]
```

---

## SECTION 6 — OPENING FRAMES (L350_Detail)

Steel hollow section 100mm × 100mm (0.1 × 0.1 units) framing each opening.
RC lintel above each opening.

Opening dimensions from original brief:
- West entry: Y=[-3.0, +3.0], Z=[0, 4.0] — 6m wide × 4m tall
- East exit: Y=[-2.0, +2.0], Z=[0, 4.5] — 4m wide × 4.5m tall

### West Entry Frame (X=-16.0 wall face)

Wall face at X=-16.0 (outer). Frame sits in wall plane, 100mm deep.

```
L350_frame_W_top:     [-16.1, -3.0, 4.0] → [-15.9, 3.0, 4.1]
L350_frame_W_bot:     [-16.1, -3.0, -0.1] → [-15.9, 3.0, 0.0]
L350_frame_W_jambN:   [-16.1, 2.9,  -0.1] → [-15.9, 3.1, 4.1]
L350_frame_W_jambS:   [-16.1, -3.1, -0.1] → [-15.9, -2.9, 4.1]
```

RC lintel (beam above opening, 300mm deep × full opening width + 300mm each side):
```
L350_lintel_W:   [-16.3, -3.0, 4.0] → [-15.7, 3.0, 4.3]
```

### East Exit Frame (X=+16.0 wall face)

```
L350_frame_E_top:     [15.9, -2.0, 4.5] → [16.1, 2.0, 4.6]
L350_frame_E_bot:     [15.9, -2.0, -0.1] → [16.1, 2.0, 0.0]
L350_frame_E_jambN:   [15.9, 1.9, -0.1] → [16.1, 2.1, 4.6]
L350_frame_E_jambS:   [15.9, -2.1, -0.1] → [16.1, -1.9, 4.6]
```

RC lintel:
```
L350_lintel_E:   [15.7, -2.0, 4.5] → [16.3, 2.0, 4.8]
```

---

## SECTION 7 — FACADE PANEL JOINTS (L400_Material, Exit Hall only)

5mm wide (0.005 units) × 20mm deep (0.02 units) incised vertical joints at X=7, 10, 13.
Full height of Exit Hall (Z=[0, 6.0]).

North face (outer face at Y=+7.3):
```
L400_pj_N_X7:    [7.000, 7.28, 0.0] → [7.005, 7.30, 6.0]
L400_pj_N_X10:   [10.000, 7.28, 0.0] → [10.005, 7.30, 6.0]
L400_pj_N_X13:   [13.000, 7.28, 0.0] → [13.005, 7.30, 6.0]
```

South face (outer face at Y=-7.3):
```
L400_pj_S_X7:    [7.000, -7.30, 0.0] → [7.005, -7.28, 6.0]
L400_pj_S_X10:   [10.000, -7.30, 0.0] → [10.005, -7.28, 6.0]
L400_pj_S_X13:   [13.000, -7.30, 0.0] → [13.005, -7.28, 6.0]
```

---

## EXECUTION SUMMARY

### Element count

| Section | Type | Count |
|---------|------|-------|
| 1.1–1.5 | Roof slabs | 3 |
| 1.2+1.5 | Parapets | 6 (3 Entry + 3 Exit) |
| 1.6–1.8 | Roof assembly layers | 9 (3 zones × 3 layers) |
| 1.9 | Upstand + drip edge | 12 (3+3 upstand, 3+3 drip) |
| 2 | Formwork lines | 17 |
| 3 | Expansion joints | 4 |
| 4.1 | Column base plates | 7 |
| 4.2 | Column top plates | 7 |
| 4.3 | Bridge beam brackets | 2 |
| 4.4 | Wall kickers | 10 |
| 5 | Gate hardware | 7 (2 bolts + 5 hinges) |
| 6 | Opening frames + lintels | 10 |
| 7 | Facade panel joints | 6 |
| **TOTAL** | | **100 elements** |

---

### Build order

1. Create 3 new layers
2. Roof slabs (3 boxes, L300_Roof)
3. Parapets (6 boxes, L300_Roof)
4. Roof assembly layers (9 boxes, L400_Material)
5. Parapet edge conditions (12 boxes, L400_Material)
6. Formwork lines (17 boxes, L400_Material) — batch as one Python script
7. Expansion joints (4 boxes, L400_Material)
8. Column base plates (7 boxes, L350_Detail)
9. Column top plates (7 boxes, L350_Detail)
10. Bridge beam brackets (2 boxes, L350_Detail)
11. Wall kickers (10 boxes, L350_Detail)
12. Gate hardware (7 boxes, L400_Material)
13. Opening frames + lintels (10 boxes, L350_Detail)
14. Facade panel joints (6 boxes, L400_Material)

---

### Executor notes

1. All coordinates are meter-scale in a centimeter-unit Rhino doc. Use numbers exactly as written.
2. Do NOT multiply by 100.
3. Use `rhino_execute_python_code` with `Box()` (BoundingBox from two corner points) for all elements.
4. Batch by section — formwork lines in one script, base plates in one script, etc.
5. If a boolean or complex operation fails, fall back to additive geometry only and note it.
6. After all geometry is placed: capture Perspective, Top, and Section (X=0 cut) viewports.
7. Target instance: `lock_01` (port 9001). All MCP calls must include `target: "lock_01"`.

---

## DECISION LOG

| Decision | Verdict | Rationale |
|----------|---------|-----------|
| Column count | 7 (not 8) | Gate SW column removed; 3 gate + 2 entry + 2 exit |
| Column labels | NW=(-4,+4), NE=(+4,+4), SE=(+4,-4) | N=+Y in this coordinate system |
| Bridge bracket Z | [4.5, 4.7] | Below beam bottom at Z=4.7; embedded 200mm into gate wall |
| Expansion joints | Through walls AND slabs | Structural continuity required |
| Rejection passage Y | [-3.0, -1.0] model units | FLAG 4 cm→m conversion confirmed |
| Roof drainage | Entry fall S, Exit fall N, Gate flat | Away from primary path; monument roof symbolic |
| Parapet height | 500mm (0.5 units) | Maintenance-only roof; not publicly accessible |
| Gate parapets | None (wall is parapet) | Gate walls extend to Z=7.0; wall-top IS the parapet |
| Slab thickness | Entry/Exit 400mm, Gate 300mm | Span/30 rule; gate thicker for monument weight |
| Coordinate system | Meter-scale throughout | Match existing model; no ×100 conversion |
