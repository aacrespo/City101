# Lock Type 01 — Border Lock
# LOG400 Upgrade: Complete Geometry Execution Plan
# Status: DRAFT FOR ROUNDTABLE REVIEW — do NOT execute until approved
# Date: 2026-03-27

---

## COORDINATE SYSTEM NOTE
All coordinates in centimeters, matching the existing Rhino document.
Origin (0,0,0) = building corner reference.
X = corridor axis (negative = System A / Entry side, positive = System B / Exit side)
Y = lateral axis
Z = vertical (0 = finished floor level)

---

## NEW LAYERS TO CREATE BEFORE ANY GEOMETRY

| Layer name | RGB | Purpose |
|---|---|---|
| `Type_01_Border::L300_Roof` | (200, 180, 160) | Roof structural slabs, parapets |
| `Type_01_Border::L350_Detail` | (160, 140, 120) | Connections, railings, frames, ledges |
| `Type_01_Border::L400_Material` | (120, 100, 80) | Formwork lines, expansion joints, hardware, edge conditions |

Do NOT rename or alter existing layers:
- `Type_01_Border::Volumes`
- `Type_01_Border::Circulation`
- `Type_01_Border::Structure`
- `Type_01_Border::Openings`
- `Type_01_Border::Annotations`

---

## SECTION 1 — ROOF SYSTEM (LOG300 elements on L300_Roof)

### Design rationale
Flat RC roofs appropriate for civic/institutional RC construction. Drainage by fall, not by form.
Span/30 slab rule: Entry Hall 12m span → 400mm; Gate Zone 8m span → 270mm (use 300mm); Exit Hall 12m span → 400mm.
All roof slabs bear on top of existing wall shells.

---

### 1.1 Entry Hall Roof Slab

**Name**: `L300_entry_roof_slab`
**Geometry type**: Box
**Layer**: `Type_01_Border::L300_Roof`
**RhinoCommon method**: `Box(BoundingBox)` or `CreateSolid` from corner points

Coordinates (cm):
```
X: [-1600, -400]
Y: [-700, 700]
Z: [500, 540]
```
Thickness: 40cm (400mm) — span/30 for 12m span
Top face at Z=540, bottom face at Z=500 (bearing on top of 500cm walls)

Drainage fall: 1.5% toward Y=-700 (south face) = drop of 700 × 0.015 = 10.5cm across 700cm half-width.
Model as flat box for plan; drainage direction noted as annotation only at LOG300.

---

### 1.2 Entry Hall Parapet

**Name**: `L300_entry_parapet_north`
**Geometry type**: Box
**Layer**: `Type_01_Border::L300_Roof`

North face parapet:
```
X: [-1600, -400]
Y: [670, 700]      ← 300mm parapet wall (matches existing 300mm wall thickness)
Z: [540, 590]      ← 50cm above top of slab
```

**Name**: `L300_entry_parapet_south`
```
X: [-1600, -400]
Y: [-700, -670]
Z: [540, 590]
```

**Name**: `L300_entry_parapet_west`
```
X: [-1600, -1570]  ← 300mm wall
Y: [-700, 700]
Z: [540, 590]
```

Note: East face of Entry Hall (X=-400) abuts Gate Zone — no parapet there; roof slab terminates at gate wall face.

---

### 1.3 Gate / Control Zone Roof Slab

**Name**: `L300_gate_roof_slab`
**Geometry type**: Box
**Layer**: `Type_01_Border::L300_Roof`

```
X: [-400, 400]
Y: [-400, 400]
Z: [700, 730]      ← top of 700cm gate walls; 30cm slab (300mm for 8m span)
```
Top face at Z=730, bottom face at Z=700.

Drainage fall: 1.5% toward Y=400 (north face) = drop of 400 × 0.015 = 6cm across 400cm.
Notes annotation only.

---

### 1.4 Gate Zone Parapets

**Name**: `L300_gate_parapet_north`
```
X: [-400, 400]
Y: [370, 400]      ← 300mm parapet, inner face flush with gate wall inner face
Z: [730, 780]      ← 50cm parapet height above slab top
```

**Name**: `L300_gate_parapet_south`
```
X: [-400, 400]
Y: [-400, -370]
Z: [730, 780]
```

**Name**: `L300_gate_parapet_east`
```
X: [370, 400]
Y: [-400, 400]
Z: [730, 780]
```

**Name**: `L300_gate_parapet_west`
```
X: [-400, -370]
Y: [-400, 400]
Z: [730, 780]
```

---

### 1.5 Exit Hall Roof Slab

**Name**: `L300_exit_roof_slab`
**Geometry type**: Box
**Layer**: `Type_01_Border::L300_Roof`

```
X: [400, 1600]
Y: [-700, 700]
Z: [600, 640]      ← top of 600cm Exit Hall walls; 40cm slab
```
Top face at Z=640, bottom face at Z=600.

Drainage fall: 1.5% toward Y=-700 (south) = 10.5cm drop.

---

### 1.6 Exit Hall Parapets

**Name**: `L300_exit_parapet_north`
```
X: [400, 1600]
Y: [670, 700]
Z: [640, 690]
```

**Name**: `L300_exit_parapet_south`
```
X: [400, 1600]
Y: [-700, -670]
Z: [640, 690]
```

**Name**: `L300_exit_parapet_east`
```
X: [1570, 1600]
Y: [-700, 700]
Z: [640, 690]
```

Note: West face of Exit Hall (X=400) abuts Gate Zone — no parapet.

---

### 1.7 Roof Assembly Layers (LOG400 — on L400_Material)

These are thin-layer representations modeled as flat boxes ON TOP of each structural slab.
They sit above the structural slab top face and represent the assembly build-up.

For ALL three zones the build-up is identical (total non-structural depth = 17.5cm):

| Layer | Thickness (cm) | Material |
|---|---|---|
| XPS insulation | 12 | Extruded polystyrene |
| Waterproofing membrane | 0.5 | Bituminous or TPO |
| Gravel ballast | 5 | 16-32mm washed gravel |

**Entry Hall roof assembly:**

`L400_entry_roof_insulation`
```
X: [-1600, -400], Y: [-700, 700]
Z: [540, 552]      ← 12cm above slab top (Z=540)
Layer: L400_Material
```

`L400_entry_roof_membrane`
```
X: [-1600, -400], Y: [-700, 700]
Z: [552, 552.5]    ← 5mm above insulation
Layer: L400_Material
```

`L400_entry_roof_gravel`
```
X: [-1600, -400], Y: [-700, 700]
Z: [552.5, 557.5]  ← 5cm ballast
Layer: L400_Material
```

**Gate zone roof assembly:**

`L400_gate_roof_insulation`
```
X: [-400, 400], Y: [-400, 400]
Z: [730, 742]
Layer: L400_Material
```

`L400_gate_roof_membrane`
```
Z: [742, 742.5]
Layer: L400_Material
```

`L400_gate_roof_gravel`
```
Z: [742.5, 747.5]
Layer: L400_Material
```

**Exit Hall roof assembly:**

`L400_exit_roof_insulation`
```
X: [400, 1600], Y: [-700, 700]
Z: [640, 652]
Layer: L400_Material
```

`L400_exit_roof_membrane`
```
Z: [652, 652.5]
Layer: L400_Material
```

`L400_exit_roof_gravel`
```
Z: [652.5, 657.5]
Layer: L400_Material
```

---

### 1.8 Parapet Edge Conditions (LOG400)

For each parapet, the waterproofing membrane turns up the inner face of the parapet wall and terminates with a drip edge at the outer top.

**Waterproofing upstand** (inner face of each parapet, 15cm up from slab top):

Model as a thin flat box, 1cm thick, against the inner face of each parapet.

Example: Entry Hall north parapet inner upstand:
`L400_entry_parapet_upstand_north`
```
X: [-1600, -400]
Y: [669, 670]      ← 1cm face standing against inner parapet face
Z: [540, 555]      ← 15cm upstand height
Layer: L400_Material
```
Repeat for all parapet inner faces (south, west for Entry; all 4 for Gate; north, south, east for Exit).

**Drip edge trim** (outer top edge of each parapet):

Model as a thin extruded L-profile. Simplified as a 3cm × 3cm box at the outer top corner of each parapet.

Example: Entry Hall north parapet drip edge:
`L400_entry_drip_edge_north`
```
X: [-1600, -400]
Y: [697, 700]      ← outer 3cm of parapet top
Z: [587, 590]      ← top 3cm of parapet height
Layer: L400_Material
```
Repeat for all outer parapet edges.

---

## SECTION 2 — FORMWORK LINES (LOG400 — on L400_Material)

RC walls cast in 2400mm (240cm) lifts. Formwork lift lines modeled as thin extruded rectangles
protruding 2cm from wall face. Profile: 2cm wide × 2cm tall horizontal band.

### 2.1 Gate Zone Walls (700cm tall) — lifts at Z=240 and Z=480

Gate walls: 400mm (40cm) thick. Inner footprint [-400,400] × [-400,400]. Outer footprint [-440,440] × [-440,440].
Lift line geometry = thin box, 2cm proud of face, 2cm tall, running full wall face length.

**North face (Y=440 is outer face):**

`L400_gate_formwork_N_lift1` (Z=240)
```
X: [-440, 440]
Y: [440, 442]      ← 2cm proud of outer face
Z: [239, 241]      ← centered on lift line
Layer: L400_Material
```

`L400_gate_formwork_N_lift2` (Z=480)
```
X: [-440, 440], Y: [440, 442], Z: [479, 481]
Layer: L400_Material
```

**South face (Y=-440 is outer face):**

`L400_gate_formwork_S_lift1`
```
X: [-440, 440], Y: [-442, -440], Z: [239, 241]
```

`L400_gate_formwork_S_lift2`
```
X: [-440, 440], Y: [-442, -440], Z: [479, 481]
```

**East face (X=440 is outer face):**

`L400_gate_formwork_E_lift1`
```
X: [440, 442], Y: [-440, 440], Z: [239, 241]
```

`L400_gate_formwork_E_lift2`
```
X: [440, 442], Y: [-440, 440], Z: [479, 481]
```

**West face (X=-440 is outer face):**

`L400_gate_formwork_W_lift1`
```
X: [-442, -440], Y: [-440, 440], Z: [239, 241]
```

`L400_gate_formwork_W_lift2`
```
X: [-442, -440], Y: [-440, 440], Z: [479, 481]
```

Total Gate formwork lines: 8 elements (4 faces × 2 lifts).

---

### 2.2 Entry Hall Walls (500cm tall) — lift at Z=240 only

Entry Hall walls: 300mm (30cm) thick.
Outer footprint: X=[-1630,-370], Y=[-730,730].
(Outer face = 30cm beyond inner envelope.)

Note: only the exposed outer faces get formwork lines; the east end (X=-370) is inside the building and not exposed.

**North outer face (Y=730):**

`L400_entry_formwork_N_lift1`
```
X: [-1630, -370], Y: [730, 732], Z: [239, 241]
Layer: L400_Material
```

**South outer face (Y=-730):**

`L400_entry_formwork_S_lift1`
```
X: [-1630, -370], Y: [-732, -730], Z: [239, 241]
```

**West outer face (X=-1630):**

`L400_entry_formwork_W_lift1`
```
X: [-1632, -1630], Y: [-730, 730], Z: [239, 241]
```

Total Entry Hall formwork lines: 3 elements (3 exposed faces × 1 lift).

---

### 2.3 Exit Hall Walls (600cm tall) — lifts at Z=240 and Z=480

Exit Hall walls: 300mm thick.
Outer footprint: X=[370,1630], Y=[-730,730].

**North outer face (Y=730):**

`L400_exit_formwork_N_lift1`
```
X: [370, 1630], Y: [730, 732], Z: [239, 241]
```

`L400_exit_formwork_N_lift2`
```
X: [370, 1630], Y: [730, 732], Z: [479, 481]
```

**South outer face (Y=-730):**

`L400_exit_formwork_S_lift1`
```
X: [370, 1630], Y: [-732, -730], Z: [239, 241]
```

`L400_exit_formwork_S_lift2`
```
X: [370, 1630], Y: [-732, -730], Z: [479, 481]
```

**East outer face (X=1630):**

`L400_exit_formwork_E_lift1`
```
X: [1630, 1632], Y: [-730, 730], Z: [239, 241]
```

`L400_exit_formwork_E_lift2`
```
X: [1630, 1632], Y: [-730, 730], Z: [479, 481]
```

Total Exit Hall formwork lines: 6 elements (3 exposed faces × 2 lifts).

**Summary: 17 formwork line elements total.**

---

## SECTION 3 — EXPANSION JOINTS (LOG400 — on L400_Material)

Required every 600cm (6m) on long concrete elements.

### 3.1 Entry Hall — joint at X=-1000

Entry Hall runs X=[-1600,-400] = 1200cm. One joint at midpoint X=-1000.
Model as a 2cm-wide gap plane cutting through the full wall depth and height.

**Cutter geometry** (used conceptually — model as thin colored solid, not a boolean operation):

`L400_entry_expansion_joint`
```
X: [-1001, -999]    ← 2cm wide slot
Y: [-730, 730]      ← full building width including wall thickness
Z: [0, 500]         ← full wall height
Geometry: Box
Layer: L400_Material
```

Visual representation: render this as a dark gap (assign black/dark material or different display color).

### 3.2 Exit Hall — joint at X=1000

Exit Hall runs X=[400,1600] = 1200cm. One joint at X=1000.

`L400_exit_expansion_joint`
```
X: [999, 1001]
Y: [-730, 730]
Z: [0, 600]
Layer: L400_Material
```

**Decision flag**: Expansion joints on roof slab also required at same X positions. Modeled as surface lines (scored line) on top of roof slab — defer to LOG400 execution if team confirms.

---

## SECTION 4 — STRUCTURAL CONNECTIONS (LOG350+)

All on layer `Type_01_Border::L350_Detail`.
Steel plates in centimeters.

### 4.1 Column Base Plates — 7 columns total

Steel plate: 50cm × 50cm × 2.5cm at base of each column.
Z position: [-2.5, 0] (plate sits below floor level, cast into slab).

Column grid (from approved spec):
| Column ID | X (cm) | Y (cm) |
|---|---|---|
| C1 | -400 | -400 |
| C2 | -400 | +400 |
| C3 | +400 | -400 |
| C4 | +400 | +400 |
| C5 | -1000 | -350 |
| C6 | -1000 | +350 |
| C7 | +1000 | -350 |
| C8 | +1000 | +350 |

Wait — spec shows 4 gate corners + 2 Entry + 2 Exit = 8 columns. Brief says "7 columns." Checking spec:
- Gate: (±400, ±400) = 4 columns
- Entry: X=-1000, Y=±350 = 2 columns
- Exit: X=+1000, Y=±350 = 2 columns
**Total: 8 columns. Use 8. Flag: brief stated 7 — confirm with team.**

For each column CXX, base plate:
```
X: [column_X - 25, column_X + 25]
Y: [column_Y - 25, column_Y + 25]
Z: [-2.5, 0]
Name: L350_baseplate_CXX
Layer: L350_Detail
```

Enumerated:
```
L350_baseplate_C1: X[-425,-375], Y[-425,-375], Z[-2.5,0]
L350_baseplate_C2: X[-425,-375], Y[375,425], Z[-2.5,0]
L350_baseplate_C3: X[375,425], Y[-425,-375], Z[-2.5,0]
L350_baseplate_C4: X[375,425], Y[375,425], Z[-2.5,0]
L350_baseplate_C5: X[-1025,-975], Y[-375,-325], Z[-2.5,0]
L350_baseplate_C6: X[-1025,-975], Y[325,375], Z[-2.5,0]
L350_baseplate_C7: X[975,1025], Y[-375,-325], Z[-2.5,0]
L350_baseplate_C8: X[975,1025], Y[325,375], Z[-2.5,0]
```

---

### 4.2 Column Top Bearing Plates

Steel plate: 50cm × 50cm × 2cm at top of each column, at column-to-roof-slab interface.

Gate columns (C1–C4): column height = 700cm, plate at Z=[700, 702]
Entry columns (C5–C6): column height = 500cm, plate at Z=[500, 502]
Exit columns (C7–C8): column height = 600cm, plate at Z=[600, 602]

Note: plate sits AT top of column, BELOW the roof slab underside. The slab bearing zone begins at the plate top.

```
L350_topplate_C1: X[-425,-375], Y[-425,-375], Z[700,702]
L350_topplate_C2: X[-425,-375], Y[375,425], Z[700,702]
L350_topplate_C3: X[375,425], Y[-425,-375], Z[700,702]
L350_topplate_C4: X[375,425], Y[375,425], Z[700,702]
L350_topplate_C5: X[-1025,-975], Y[-375,-325], Z[500,502]
L350_topplate_C6: X[-1025,-975], Y[325,375], Z[500,502]
L350_topplate_C7: X[975,1025], Y[-375,-325], Z[600,602]
L350_topplate_C8: X[975,1025], Y[325,375], Z[600,602]
```

---

### 4.3 Bridge Beam End Brackets

The overhead bridge beam sits at Y=0, X=[-400,400], Z=500, section 40cm × 30cm (spec).
At each end (X=-400 and X=+400) a steel bracket is embedded in the gate wall face.

Bracket: 30cm × 20cm × 2cm steel plate.
Centered on beam: Z range = [500 - 15, 500 + 15] = [485, 515] vertical (beam height 30cm).
Y range = [-10, 10] (beam width 20cm, centered on Y=0).

**West bracket (embedded in gate west wall, outer face X=-400, pointing West):**
`L350_bridge_bracket_W`
```
X: [-402, -400]    ← 2cm plate sitting against wall face
Y: [-10, 10]       ← 20cm centered
Z: [485, 515]      ← 30cm height = beam depth
Layer: L350_Detail
```

**East bracket (gate east wall, face X=400, pointing East):**
`L350_bridge_bracket_E`
```
X: [400, 402]
Y: [-10, 10]
Z: [485, 515]
Layer: L350_Detail
```

**Decision flag**: Brief specifies bracket at Z=[470,500] while beam spec says Z=500 is beam center. Above coordinates use beam top at Z=500 + beam height 30cm seated below. Confirm: is Z=500 top of beam or bottom of beam? If Z=500 is TOP, beam runs Z=[470,500] and brackets should be at Z=[468,500].

---

### 4.4 Wall-to-Slab Junction Kicker (LOG350)

50mm × 50mm RC ledge/kicker at slab bearing line, runs full wall base perimeter.
This represents the thickened kicker at base of each wall where it meets the floor slab.

Entry Hall walls, full perimeter kicker at Z=[0, 5] (5cm tall) × 5cm wide:

`L350_kicker_entry_N`
```
X: [-1600, -400], Y: [700, 705], Z: [0, 5]
Layer: L350_Detail
```

`L350_kicker_entry_S`
```
X: [-1600, -400], Y: [-705, -700], Z: [0, 5]
```

`L350_kicker_entry_W`
```
X: [-1605, -1600], Y: [-705, 705], Z: [0, 5]
```

Gate walls kicker:
```
L350_kicker_gate_N: X[-400,400], Y[400,405], Z[0,5]
L350_kicker_gate_S: X[-400,400], Y[-405,-400], Z[0,5]
L350_kicker_gate_E: X[400,405], Y[-400,400], Z[0,5]
L350_kicker_gate_W: X[-405,-400], Y[-400,400], Z[0,5]
```

Exit Hall walls kicker:
```
L350_kicker_exit_N: X[400,1600], Y[700,705], Z[0,5]
L350_kicker_exit_S: X[400,1600], Y[-705,-700], Z[0,5]
L350_kicker_exit_E: X[1600,1605], Y[-700,700], Z[0,5]
```

**Total kicker elements: 10**

---

## SECTION 5 — FACADE DIVISIONS (LOG300 — on L300_Roof or L350_Detail)

### 5.1 Entry Hall — fully opaque RC

No glazing. Entry Hall exterior faces are monolithic RC.
No surface additions needed beyond existing wall geometry.
Formwork lines (Section 2) provide the only surface articulation.

### 5.2 Gate Zone — fair-face RC

Fully opaque, monumental. No facade divisions.
Gate south and north windows already modeled (Y=±400, X=[-200,200], Z=[300,600]).
Formwork lines (Section 2) provide surface reading.

### 5.3 Exit Hall — clerestory panel joints

Clerestory slots already exist (from existing openings geometry).
Panel joint lines between clerestory openings on North and South faces.

Panel joint spacing: column spacing ≈ 300cm. Panel joints align with column grid X=700 and X=1000 and X=1300.

Model panel joints as thin incised slots: 0.5cm wide × 2cm deep, full height of wall face.

**Exit Hall North face panel joints (Y=700 outer face, running in Z direction):**

`L350_exit_N_paneljoint_1` at X=700
```
X: [699.75, 700.25]    ← 0.5cm wide
Y: [698, 700]           ← 2cm deep into wall face
Z: [0, 600]             ← full wall height
Layer: L350_Detail
```

`L350_exit_N_paneljoint_2` at X=1000
```
X: [999.75, 1000.25], Y: [698, 700], Z: [0, 600]
```

`L350_exit_N_paneljoint_3` at X=1300
```
X: [1299.75, 1300.25], Y: [698, 700], Z: [0, 600]
```

**Exit Hall South face panel joints (Y=-700 outer face):**

`L350_exit_S_paneljoint_1` at X=700
```
X: [699.75, 700.25], Y: [-700, -698], Z: [0, 600]
```

`L350_exit_S_paneljoint_2` at X=1000
```
X: [999.75, 1000.25], Y: [-700, -698], Z: [0, 600]
```

`L350_exit_S_paneljoint_3` at X=1300
```
X: [1299.75, 1300.25], Y: [-700, -698], Z: [0, 600]
```

**Total panel joint elements: 6**

---

## SECTION 6 — GATE HARDWARE (LOG400 — on L400_Material)

All hardware is symbolic geometry — simplified solids representing correct location and scale.

### 6.1 Primary Passage Hardware (West face of Gate, Y=[-125,+125], Z=[0,350])

**Sliding bolt/bar:**
`L400_gate_hardware_bolt_primary`
```
X: [-442, -402]    ← 40cm bar sitting against west outer wall face (wall outer face at X=-440)
Y: [-120, 120]     ← 240cm = 2400mm bar length
Z: [199, 202]      ← 3cm square section, at Z=200 (2m height)
Geometry: Box (3cm × 240cm × 3cm)
Layer: L400_Material
```

**Hinges — 3 per side (primary passage):**

Left side hinge posts (Y=-125, door side):
`L400_gate_hinge_primary_L1` (Z=50, lower)
```
X: [-442, -422]    ← 20cm wide plate
Y: [-135, -125]    ← 10cm deep plate
Z: [45, 55]        ← 10cm tall
Layer: L400_Material
```

`L400_gate_hinge_primary_L2` (Z=175, mid)
```
X: [-442, -422], Y: [-135, -125], Z: [170, 180]
```

`L400_gate_hinge_primary_L3` (Z=300, upper)
```
X: [-442, -422], Y: [-135, -125], Z: [295, 305]
```

Right side hinge posts (Y=+125):
`L400_gate_hinge_primary_R1`
```
X: [-442, -422], Y: [125, 135], Z: [45, 55]
```

`L400_gate_hinge_primary_R2`
```
X: [-442, -422], Y: [125, 135], Z: [170, 180]
```

`L400_gate_hinge_primary_R3`
```
X: [-442, -422], Y: [125, 135], Z: [295, 305]
```

---

### 6.2 Rejection Passage Hardware (West face, Y=[-300,-100])

Rejection passage: Y=[-300,-100], Z=[0,300].

**Sliding bolt/bar:**
`L400_gate_hardware_bolt_rejection`
```
X: [-442, -402]
Y: [-290, -110]    ← 180cm = 1800mm bar (≈2000mm as specified — note: passage width is 200cm, bar 200cm)
Z: [149, 152]      ← 3cm square at Z=150 (1.5m height)
Layer: L400_Material
```

**Decision flag**: Rejection passage Y extents — brief states Y=[-3.0,-1.0] metres = Y=[-300,-100] cm. Confirm this aligns with existing rejection passage opening geometry.

**Hinges — 2 per side:**
`L400_gate_hinge_rejection_L1` (Z=50)
```
X: [-442, -422], Y: [-310, -300], Z: [45, 55]
```

`L400_gate_hinge_rejection_L2` (Z=200)
```
X: [-442, -422], Y: [-310, -300], Z: [195, 205]
```

`L400_gate_hinge_rejection_R1` (Z=50)
```
X: [-442, -422], Y: [-100, -90], Z: [45, 55]
```

`L400_gate_hinge_rejection_R2` (Z=200)
```
X: [-442, -422], Y: [-100, -90], Z: [195, 205]
```

---

## SECTION 7 — DOOR/OPENING FRAMES (LOG350 — on L350_Detail)

### 7.1 West Entry Opening Frame (6m × 4m, existing opening at X=-1600, Y=[-300,300], Z=[0,400])

Steel hollow section frame: 100mm × 100mm (10cm × 10cm) around all 4 sides.

Note: Frame sits within the wall reveal (wall is 300mm thick at X=-1600 side).
Frame centerline at X=-1600, flush with inner wall face.

**Head (top horizontal, at Z=400):**
`L350_frame_entry_head`
```
X: [-1610, -1590]   ← 10cm section
Y: [-310, 310]      ← spans full opening width + jamb overlap
Z: [400, 410]       ← 10cm section sitting above opening
Layer: L350_Detail
```

**Sill (bottom horizontal, at Z=0):**
`L350_frame_entry_sill`
```
X: [-1610, -1590]
Y: [-300, 300]
Z: [-5, 5]          ← 10cm section at floor level
```

**Left jamb (Y=-300):**
`L350_frame_entry_jamb_L`
```
X: [-1610, -1590]
Y: [-310, -300]
Z: [0, 400]
```

**Right jamb (Y=+300):**
`L350_frame_entry_jamb_R`
```
X: [-1610, -1590]
Y: [300, 310]
Z: [0, 400]
```

**RC lintel above opening:**
`L350_lintel_entry`
```
X: [-1600, -1600]   — this is the wall face; lintel runs INTO the wall
X: [-1630, -1570]   ← bearing 30cm into wall each side (300mm bearing)
Y: [-300, 300]
Z: [400, 430]       ← 30cm deep lintel
Layer: L350_Detail
```

---

### 7.2 East Exit Opening Frame (4m × 4.5m, at X=+1600, Y=[-200,200], Z=[0,450])

**Head:**
`L350_frame_exit_head`
```
X: [1590, 1610], Y: [-210, 210], Z: [450, 460]
```

**Sill:**
```
X: [1590, 1610], Y: [-200, 200], Z: [-5, 5]
```

**Left jamb:**
```
X: [1590, 1610], Y: [-210, -200], Z: [0, 450]
```

**Right jamb:**
```
X: [1590, 1610], Y: [200, 210], Z: [0, 450]
```

**RC lintel:**
`L350_lintel_exit`
```
X: [1570, 1630]
Y: [-200, 200]
Z: [450, 480]        ← 30cm deep lintel
Layer: L350_Detail
```

---

### 7.3 Gate Passages — raw RC reveal, no frame

Primary gate passage (W face, Y=[-125,+125], Z=[0,350]):
No steel frame. No lintel. RC wall returns as reveal.
Model reveal depth as annotation only — no new geometry needed.

Rejection gate passage (W face, Y=[-300,-100], Z=[0,300]):
Same — raw RC reveal, no additional geometry.

---

## BUILD SEQUENCE

Execute in this order to minimize conflicts:

| Step | Elements | Layer | Reason |
|---|---|---|---|
| 1 | Create 3 new layers | — | Must exist before any geometry |
| 2 | Roof structural slabs (1.1, 1.3, 1.5) | L300_Roof | Defines Z datum for all assembly layers |
| 3 | Parapets (1.2, 1.4, 1.6) | L300_Roof | Depends on slab top face Z |
| 4 | Column base plates (4.1) | L350_Detail | Independent of roof, add now |
| 5 | Column top bearing plates (4.2) | L350_Detail | Independent of roof |
| 6 | Bridge beam brackets (4.3) | L350_Detail | Independent |
| 7 | Wall kickers (4.4) | L350_Detail | Independent |
| 8 | Door/opening frames + lintels (7.1, 7.2) | L350_Detail | Independent |
| 9 | Facade panel joints (5.3) | L350_Detail | After walls confirmed |
| 10 | Formwork lines (Section 2) | L400_Material | After wall outer faces confirmed |
| 11 | Expansion joints (Section 3) | L400_Material | After formwork lines |
| 12 | Roof assembly layers (1.7) | L400_Material | After roof slabs |
| 13 | Parapet upstands + drip edges (1.8) | L400_Material | After parapets |
| 14 | Gate hardware (Section 6) | L400_Material | Last — symbolic, non-structural |

---

## FLAGS AND DECISIONS NEEDED BEFORE EXECUTION

| # | Flag | Location | Options |
|---|---|---|---|
| F1 | Column count: spec shows 8 columns (4 gate + 2 entry + 2 exit) but brief states 7. | Section 4.1 | Confirm 8 or 7 — affects base plate and top plate count |
| F2 | Bridge beam Z=500: is this top-of-beam or bottom-of-beam? | Section 4.3 | Affects bracket Z position by 30cm |
| F3 | Expansion joints continue through roof slab? | Section 3 | Adds 2 roof-slab expansion joints if yes |
| F4 | Rejection passage Y extents: verify Y=[-300,-100] matches existing opening geometry | Section 6.2 | Check against Openings layer in model |
| F5 | Roof drainage direction: south (toward Y=-700) for Entry + Exit, north (toward Y=+400) for Gate. Acceptable? | Section 1 | If not, swap fall direction — no geometry change, annotation only |
| F6 | Parapet height: 50cm above slab chosen. Minimum for accessible roof is 110cm (railing code). If roof is accessible, increase to 110cm parapets or add railing. | Section 1.2–1.6 | Confirm: accessible or not accessible? |

---

## ELEMENT COUNT SUMMARY

| Category | Layer | Count |
|---|---|---|
| Roof structural slabs | L300_Roof | 3 |
| Parapets | L300_Roof | 10 |
| Roof assembly layers (ins+membrane+gravel × 3 zones) | L400_Material | 9 |
| Parapet upstands | L400_Material | 9 (3 entry + 4 gate + 3 exit - corner shares) |
| Parapet drip edges | L400_Material | 9 (matching upstand faces) |
| Formwork lines | L400_Material | 17 |
| Expansion joints | L400_Material | 2 |
| Gate hardware (bolts + hinges) | L400_Material | 14 |
| Column base plates | L350_Detail | 8 |
| Column top bearing plates | L350_Detail | 8 |
| Bridge beam brackets | L350_Detail | 2 |
| Wall kickers | L350_Detail | 10 |
| Door frames (entry + exit, 4 sides each) | L350_Detail | 8 |
| RC lintels | L350_Detail | 2 |
| Facade panel joints | L350_Detail | 6 |
| **TOTAL NEW ELEMENTS** | | **~117** |

---

## RHINO EXECUTION NOTES (for modeler)

- All geometry: `rhino_create_object` with `Box` type, providing corner points A and B.
- Thin elements (formwork lines, joint slots): use Box with exact min/max coordinates.
- Layer assignment: set current layer before each batch, or pass layer name per object.
- Units: document is in centimeters — all coordinates above are in centimeters.
- After all elements created: lock existing Volumes/Structure layers, leave new LOG layers unlocked.
- No boolean operations required — all additions are additive solids sitting against or on existing geometry.
- Parapet upstand and drip edge elements can be created in a single `rhino_create_objects` batch call per zone.

---
*Plan produced 2026-03-27. For roundtable review — do not execute until flags F1–F6 resolved.*
