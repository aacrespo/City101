# Lock Type 04 — Temporal Lock
# LOG400 Complete Building Spec: ROUNDTABLE-APPROVED
# Status: APPROVED — ready for executor
# Approved by: Structural + Envelope + Archibase Roundtable
# Date: 2026-03-27

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry authored in METER-SCALE values (X=-18 to 18, Z=0 to 9.3).

**ALL coordinates in this spec are meter-scale. Use them exactly as written.**
**Do NOT multiply by 100. Do NOT convert.**

X = corridor axis (negative = Night/West/Entry, positive = Dawn/East/Exit)
Y = lateral axis (positive = North, negative = South)
Z = vertical (0 = Night Chamber finished floor level)

**Key asymmetry:** Dawn Chamber floor at Z=0.3 (30cm level change — temporal passage).

---

## CORRECTIONS FROM ROUNDTABLE REVIEW

| # | Issue | Resolution |
|---|-------|-----------|
| C1 | Stair R=300mm, G=300mm (Blondel=900) — unusable | Redesigned: R=167mm, G=300mm, 18 risers. Stair blocks extended to 5.4m in X. Blondel=634mm. |
| C2 | Threshold 300mm step violates SIA 500 (max 25mm) | Added 5.0m ramp (6% gradient) inside gate volume alongside threshold. |
| C3 | Parapets placed at wall inner face, not outer | All parapets shifted to outer face. Cascading fixes to upstands, drips, roof assembly extents. |
| C4 | Roof slabs at inner face — no bearing | Extended all roof slabs to wall outer faces. |
| C5 | Gate roof flat — violates SIA 271 (min 1.5%) | Gate roof now has 1.5% fall south. |
| C6 | Canopy drips/fascia above slab bottom, not below | Inverted to hang below canopy slab. |
| C7 | Canopy brackets full wall depth (300mm through 300mm wall) | Reduced to 200mm embedment. |
| C8 | Mezzanine brackets inside room, not in wall | Repositioned into wall thickness. |
| C9 | Foundation depth 400mm — below frost protection (800mm) | Deepened to Z=-1.1 (800mm below slab bottom). |
| C10 | Missing gate E/W foundation strips | Added gate E and W foundations. |
| C11 | Kicker text says "outer face" but coordinates at inner | Corrected to outer face coordinates. |
| C12 | Foundation width text says 600mm, model is 900mm | Corrected text to 900mm. Accepted as appropriate. |
| C13 | Roof insulation 120mm XPS → U=0.29 W/m2K, fails SIA 380/1 | Increased to 200mm XPS (U=0.175). All roof assembly Z coords updated. |
| C14 | No Dawn mezzanine beam (FLAG 3) | Added beam at X=10, Z=3.3. |
| C15 | Canopy Y extent flush with gate walls (FLAG 5) | Extended to Y=±4.5 for weather protection. |

---

## RHINO TARGET

Instance: port 9001 (target: `"structure"`)
All MCP calls: `target: "structure"`

---

## LAYERS TO CREATE

### Base layers (LOG200)
```
Type_04_Temporal::Volumes       — RGB(105, 219, 124)
Type_04_Temporal::Circulation   — RGB(160, 235, 175)
Type_04_Temporal::Structure     — RGB(75, 155, 90)
Type_04_Temporal::Openings      — RGB(130, 225, 150)
Type_04_Temporal::Annotations   — RGB(200, 245, 210)
```

### Detail layers (LOG300–400)
```
Type_04_Temporal::L300_Roof     — RGB(85, 180, 105)
Type_04_Temporal::L350_Detail   — RGB(60, 135, 78)
Type_04_Temporal::L400_Material — RGB(45, 100, 60)
```

---

## WALL OUTER FACE REFERENCE

Volume coordinates = inner face. Walls 0.3m thick outward.

| Zone | Inner | Outer |
|------|-------|-------|
| Night N | Y=+6.0 | Y=+6.3 |
| Night S | Y=-6.0 | Y=-6.3 |
| Night W | X=-18.0 | X=-18.3 |
| Gate N | Y=+4.0 | Y=+4.3 |
| Gate S | Y=-4.0 | Y=-4.3 |
| Gate W | X=-3.0 | X=-3.3 |
| Gate E | X=+3.0 | X=+3.3 |
| Dawn N | Y=+6.0 | Y=+6.3 |
| Dawn S | Y=-6.0 | Y=-6.3 |
| Dawn E | X=+18.0 | X=+18.3 |

---

## SECTION A — BASE BUILDING

### A1. Night Chamber Walls (Volumes)

4 wall shells, 0.3m thick, Z=[0, 6.0].

```
A1_night_wall_N:   [-18.0, 6.0, 0.0] → [-3.0, 6.3, 6.0]
A1_night_wall_S:   [-18.0, -6.3, 0.0] → [-3.0, -6.0, 6.0]
A1_night_wall_W:   [-18.3, -6.3, 0.0] → [-18.0, 6.3, 6.0]
A1_night_wall_E:   [-3.3, -6.3, 0.0] → [-3.0, 6.3, 6.0]
```

### A2. Gate Walls (Volumes)

4 wall shells, 0.3m thick, Z=[0, 9.0].

```
A2_gate_wall_N:   [-3.0, 4.0, 0.0] → [3.0, 4.3, 9.0]
A2_gate_wall_S:   [-3.0, -4.3, 0.0] → [3.0, -4.0, 9.0]
A2_gate_wall_W:   [-3.3, -4.3, 0.0] → [-3.0, 4.3, 9.0]
A2_gate_wall_E:   [3.0, -4.3, 0.0] → [3.3, 4.3, 9.0]
```

Gate W overlaps Night E at X=[-3.3, -3.0]. Same physical wall — kept separate per Lock 01 convention.

### A3. Dawn Chamber Walls (Volumes)

4 wall shells, 0.3m thick, Z=[0.3, 7.0].

```
A3_dawn_wall_N:   [3.0, 6.0, 0.3] → [18.0, 6.3, 7.0]
A3_dawn_wall_S:   [3.0, -6.3, 0.3] → [18.0, -6.0, 7.0]
A3_dawn_wall_W:   [3.0, -6.3, 0.3] → [3.3, 6.3, 7.0]
A3_dawn_wall_E:   [18.0, -6.3, 0.3] → [18.3, 6.3, 7.0]
```

### A4. Floor Slabs (Volumes)

```
A4_night_floor_slab:   [-18.3, -6.3, -0.3] → [-3.0, 6.3, 0.0]
A4_gate_floor_slab:    [-3.3, -4.3, -0.3] → [3.3, 4.3, 0.0]
A4_dawn_floor_slab:    [3.0, -6.3, 0.0] → [18.3, 6.3, 0.3]
```

### A5. Threshold Ramp (Volumes) — C2 CORRECTION

SIA 500 ramp replacing 300mm step. 6% gradient, 5.0m long, within gate volume.
Ramp along south side of gate (Y=[-4.0, -2.5]), from Z=0 to Z=0.3.

```
A5_threshold_ramp:   [-2.0, -4.0, 0.0] → [3.0, -2.5, 0.3]
```
5.0m long (X=-2.0 to 3.0) × 1.5m wide (Y) × 0.3m rise = 6% gradient.
Ramp surface slopes linearly from Z=0 (west end) to Z=0.3 (east end).
Modeled as a wedge-shaped solid (box approximation at LOG400).

**Threshold stone** (flush with dawn floor, at ramp top):
```
A5_threshold_stone:   [2.85, -4.0, 0.27] → [3.15, 4.0, 0.3]
```

### A6. Ground Plane (Volumes)

```
A6_ground_plane:   [-20.0, -8.0, -0.45] → [20.0, 8.0, -0.3]
```

### A7. Structure — Columns and Beams (Structure)

**8 columns**, 0.3m × 0.3m:

```
A7_col_C1_gate_NW:   [-3.15, 3.85, 0.0]  → [-2.85, 4.15, 9.0]
A7_col_C2_gate_NE:   [2.85, 3.85, 0.0]   → [3.15, 4.15, 9.0]
A7_col_C3_gate_SE:   [2.85, -4.15, 0.0]  → [3.15, -3.85, 9.0]
A7_col_C4_gate_SW:   [-3.15, -4.15, 0.0] → [-2.85, -3.85, 9.0]
A7_col_C5_night_S:   [-10.15, -3.15, 0.0] → [-9.85, -2.85, 6.0]
A7_col_C6_night_N:   [-10.15, 2.85, 0.0]  → [-9.85, 3.15, 6.0]
A7_col_C7_dawn_S:    [9.85, -3.15, 0.3]   → [10.15, -2.85, 7.0]
A7_col_C8_dawn_N:    [9.85, 2.85, 0.3]    → [10.15, 3.15, 7.0]
```

**Canopy beam** (0.3×0.3, overhangs 1.5m each side):
```
A7_canopy_beam:   [-4.5, -0.15, 7.7] → [4.5, 0.15, 8.0]
```

**Night mezzanine beam** (spans Y at X=-10, Z=3.0):
```
A7_night_mezz_beam:   [-10.15, -6.0, 2.7] → [-9.85, 6.0, 3.0]
```

**Dawn mezzanine beam** (C14 — added per FLAG 3):
```
A7_dawn_mezz_beam:   [9.85, -6.0, 3.0] → [10.15, 6.0, 3.3]
```

### A8. Openings (Openings)

**Night Chamber:**
```
A8_night_entry_door:   [-18.3, -1.5, 0.0] → [-18.25, 1.5, 3.5]
A8_night_win_N1:   [-15.0, 6.25, 3.5] → [-13.5, 6.3, 5.5]
A8_night_win_N2:   [-11.0, 6.25, 3.5] → [-9.5, 6.3, 5.5]
A8_night_win_N3:   [-7.0, 6.25, 3.5]  → [-5.5, 6.3, 5.5]
```

**Gate passages:**
```
A8_gate_passage_W:   [-3.35, -2.0, 0.0] → [-3.3, 2.0, 7.0]
A8_gate_passage_E:   [3.3, -2.0, 0.3] → [3.35, 2.0, 7.0]
```

**Dawn Chamber:**
```
A8_dawn_window_E:    [18.25, -3.0, 1.3] → [18.3, 3.0, 6.3]
A8_dawn_win_S1:      [5.5, -6.3, 1.1]  → [7.9, -6.25, 5.8]
A8_dawn_win_S2:      [9.3, -6.3, 1.1]  → [11.7, -6.25, 5.8]
A8_dawn_win_S3:      [13.1, -6.3, 1.1] → [15.5, -6.25, 5.8]
A8_dawn_exit_door:   [18.25, -1.5, 0.3] → [18.3, 1.5, 4.0]
```

### A9. Circulation (Circulation)

```
A9_primary_path:   Polyline [(-18,0,0), (-3,0,0), (0,0,0), (3,0,0.3), (18,0,0.3)]
A9_night_stair_block:   [-15.4, -3.0, 0.0] → [-10.0, 3.0, 3.0]
A9_dawn_stair_block:    [10.0, -3.0, 0.3] → [15.4, 3.0, 3.3]
```
Stair blocks now 5.4m in X (C1 correction: 18 risers × 300mm going).

### A10. Annotations (Annotations)

```
(-10.5, 0, 3.0)   → "NIGHT / REST / 01:30"
(0, 0, 4.5)       → "THRESHOLD / TIME PASSES"
(10.5, 0, 3.5)    → "DAWN / PREPARATION / 05:00"
(-18, 0, 1.75)    → "ENTRY (LAST SERVICE)"
(18, 0, 2.15)     → "EXIT (FIRST SERVICE)"
(0.5, -3.25, 0.15) → "RAMP 6% (SIA 500)"
```

### Section A count: 49 elements
(12 walls + 3 floor slabs + 1 ramp + 1 threshold + 1 ground + 8 columns + 3 beams + 11 openings + 1 path + 2 stairs + 6 annotations)

---

## SECTION 1 — ROOF SYSTEM (L300_Roof)

### Slab thickness
- Night/Dawn: 12m span → span/30 = 400mm (0.4)
- Gate: 8m span → 300mm (0.3)
- Canopy: 9m span → 300mm (0.3)

### 1.1 Night Roof Slab (C4 — extended to outer faces)

```
L300_night_roof_slab:   [-18.3, -6.3, 6.0] → [-3.0, 6.3, 6.4]
```
Drainage: 1.5% fall south.

### 1.2 Night Parapets (C3 — outer face corrected)

Z=[6.4, 6.9]. No east parapet (gate junction).

```
L300_night_parapet_N:   [-18.3, 6.0, 6.4] → [-3.0, 6.3, 6.9]
L300_night_parapet_S:   [-18.3, -6.3, 6.4] → [-3.0, -6.0, 6.9]
L300_night_parapet_W:   [-18.3, -6.3, 6.4] → [-18.0, 6.3, 6.9]
```

### 1.3 Gate Roof Slab (C4 + C5 — outer faces + 1.5% slope)

```
L300_gate_roof_slab:   [-3.3, -4.3, 9.0] → [3.3, 4.3, 9.3]
```
Drainage: 1.5% fall south. Drop = 8.6 × 0.015 = 0.13. Annotate.

### 1.4 Dawn Roof Slab (C4 — extended to outer faces)

```
L300_dawn_roof_slab:   [3.0, -6.3, 7.0] → [18.3, 6.3, 7.4]
```
Drainage: 1.5% fall north.

### 1.5 Dawn Parapets (C3 — outer face corrected)

Z=[7.4, 7.9]. No west parapet (gate junction).

```
L300_dawn_parapet_N:   [3.0, 6.0, 7.4] → [18.3, 6.3, 7.9]
L300_dawn_parapet_S:   [3.0, -6.3, 7.4] → [18.3, -6.0, 7.9]
L300_dawn_parapet_E:   [18.0, -6.3, 7.4] → [18.3, 6.3, 7.9]
```

### 1.6 Canopy Slab (C15 — Y extended to ±4.5)

```
L300_canopy_slab:   [-4.5, -4.5, 8.0] → [4.5, 4.5, 8.3]
```

### Section 1: 10 elements

---

## SECTION 2 — ROOF ASSEMBLY (L400_Material)

Build-up (C13 — 200mm XPS): 200mm XPS + 5mm membrane + 50mm gravel = 255mm = 0.255 units.

### 2.1 Night Roof Assembly

Slab top Z=6.4. Inside parapets: inner faces at X=-18.0, Y=±6.0.

```
L400_night_insulation:   [-18.0, -6.0, 6.40] → [-3.0, 6.0, 6.60]    (200mm)
L400_night_membrane:     [-18.0, -6.0, 6.60] → [-3.0, 6.0, 6.605]   (5mm)
L400_night_gravel:       [-18.0, -6.0, 6.605] → [-3.0, 6.0, 6.655]  (50mm)
```

### 2.2 Gate Roof Assembly

Slab top Z=9.3. Inside walls: X=±3.0, Y=±4.0.

```
L400_gate_insulation:   [-3.0, -4.0, 9.30] → [3.0, 4.0, 9.50]    (200mm)
L400_gate_membrane:     [-3.0, -4.0, 9.50] → [3.0, 4.0, 9.505]   (5mm)
L400_gate_gravel:       [-3.0, -4.0, 9.505] → [3.0, 4.0, 9.555]  (50mm)
```

### 2.3 Dawn Roof Assembly

Slab top Z=7.4. Inside parapets: inner faces at X=18.0, Y=±6.0.

```
L400_dawn_insulation:   [3.0, -6.0, 7.40] → [18.0, 6.0, 7.60]    (200mm)
L400_dawn_membrane:     [3.0, -6.0, 7.60] → [18.0, 6.0, 7.605]   (5mm)
L400_dawn_gravel:       [3.0, -6.0, 7.605] → [18.0, 6.0, 7.655]  (50mm)
```

### 2.4 Canopy Roof Assembly

Slab top Z=8.3. No parapets — inset 50mm from edges.

```
L400_canopy_insulation:   [-4.45, -4.45, 8.30] → [4.45, 4.45, 8.50]    (200mm)
L400_canopy_membrane:     [-4.45, -4.45, 8.50] → [4.45, 4.45, 8.505]   (5mm)
L400_canopy_gravel:       [-4.45, -4.45, 8.505] → [4.45, 4.45, 8.555]  (50mm)
```

### Section 2: 12 elements

---

## SECTION 3 — EDGE CONDITIONS (L400_Material)

### 3.1 Upstands (C3 cascade — at corrected parapet inner faces)

20mm wide × 150mm tall against parapet inner face.

**Night** (slab top Z=6.4):
```
L400_night_upstand_N:   [-18.0, 5.98, 6.4] → [-3.0, 6.0, 6.55]
L400_night_upstand_S:   [-18.0, -6.0, 6.4] → [-3.0, -5.98, 6.55]
L400_night_upstand_W:   [-18.02, -6.0, 6.4] → [-18.0, 6.0, 6.55]
```

**Dawn** (slab top Z=7.4):
```
L400_dawn_upstand_N:   [3.0, 5.98, 7.4] → [18.0, 6.0, 7.55]
L400_dawn_upstand_S:   [3.0, -6.0, 7.4] → [18.0, -5.98, 7.55]
L400_dawn_upstand_E:   [17.98, -6.0, 7.4] → [18.0, 6.0, 7.55]
```

### 3.2 Drip Edges (C3 cascade — at corrected parapet outer faces)

30mm × 20mm at outer top corner.

**Night** (parapet top Z=6.9, outer faces at Y=6.3, X=-18.3):
```
L400_night_drip_N:   [-18.3, 6.27, 6.87] → [-3.0, 6.3, 6.9]
L400_night_drip_S:   [-18.3, -6.3, 6.87] → [-3.0, -6.27, 6.9]
L400_night_drip_W:   [-18.3, -6.3, 6.87] → [-18.27, 6.3, 6.9]
```

**Dawn** (parapet top Z=7.9, outer faces at Y=6.3, X=18.3):
```
L400_dawn_drip_N:   [3.0, 6.27, 7.87] → [18.3, 6.3, 7.9]
L400_dawn_drip_S:   [3.0, -6.3, 7.87] → [18.3, -6.27, 7.9]
L400_dawn_drip_E:   [18.27, -6.3, 7.87] → [18.3, 6.3, 7.9]
```

### Section 3: 12 elements

---

## SECTION 4 — FORMWORK LINES (L400_Material)

2400mm lifts, 20mm proud of outer face, 20mm tall.

### Night (3 elements, Z=2.4 only)
```
L400_night_fw_N_L1:   [-18.3, 6.30, 2.39] → [-3.0, 6.32, 2.41]
L400_night_fw_S_L1:   [-18.3, -6.32, 2.39] → [-3.0, -6.30, 2.41]
L400_night_fw_W_L1:   [-18.32, -6.3, 2.39] → [-18.30, 6.3, 2.41]
```

### Gate (12 elements, lifts at Z=2.4, 4.8, 7.2)
```
L400_gate_fw_N_L1:   [-3.3, 4.30, 2.39] → [3.3, 4.32, 2.41]
L400_gate_fw_S_L1:   [-3.3, -4.32, 2.39] → [3.3, -4.30, 2.41]
L400_gate_fw_E_L1:   [3.30, -4.3, 2.39] → [3.32, 4.3, 2.41]
L400_gate_fw_W_L1:   [-3.32, -4.3, 2.39] → [-3.30, 4.3, 2.41]

L400_gate_fw_N_L2:   [-3.3, 4.30, 4.79] → [3.3, 4.32, 4.81]
L400_gate_fw_S_L2:   [-3.3, -4.32, 4.79] → [3.3, -4.30, 4.81]
L400_gate_fw_E_L2:   [3.30, -4.3, 4.79] → [3.32, 4.3, 4.81]
L400_gate_fw_W_L2:   [-3.32, -4.3, 4.79] → [-3.30, 4.3, 4.81]

L400_gate_fw_N_L3:   [-3.3, 4.30, 7.19] → [3.3, 4.32, 7.21]
L400_gate_fw_S_L3:   [-3.3, -4.32, 7.19] → [3.3, -4.30, 7.21]
L400_gate_fw_E_L3:   [3.30, -4.3, 7.19] → [3.32, 4.3, 7.21]
L400_gate_fw_W_L3:   [-3.32, -4.3, 7.19] → [-3.30, 4.3, 7.21]
```

### Dawn (6 elements, lifts at Z=2.7, 5.1 — local from Z=0.3 floor)
```
L400_dawn_fw_N_L1:   [3.0, 6.30, 2.69] → [18.3, 6.32, 2.71]
L400_dawn_fw_S_L1:   [3.0, -6.32, 2.69] → [18.3, -6.30, 2.71]
L400_dawn_fw_E_L1:   [18.30, -6.3, 2.69] → [18.32, 6.3, 2.71]

L400_dawn_fw_N_L2:   [3.0, 6.30, 5.09] → [18.3, 6.32, 5.11]
L400_dawn_fw_S_L2:   [3.0, -6.32, 5.09] → [18.3, -6.30, 5.11]
L400_dawn_fw_E_L2:   [18.30, -6.3, 5.09] → [18.32, 6.3, 5.11]
```

### Section 4: 21 elements

---

## SECTION 5 — EXPANSION JOINTS (L400_Material)

Dark color (RGB 20,20,20). 20mm wide.

```
L400_night_joint_wall:   [-10.51, -6.3, 0.0] → [-10.49, 6.3, 6.0]
L400_night_joint_slab:   [-10.51, -6.3, 6.0] → [-10.49, 6.3, 6.4]

L400_dawn_joint_wall:   [10.49, -6.3, 0.3] → [10.51, 6.3, 7.0]
L400_dawn_joint_slab:   [10.49, -6.3, 7.0] → [10.51, 6.3, 7.4]
```

### Section 5: 4 elements

---

## SECTION 6 — STRUCTURAL CONNECTIONS (L350_Detail)

### 6.1 Column Base Plates (8)

500mm × 500mm × 25mm. Z=[-0.025, 0] for Night/Gate; Z=[0.275, 0.3] for Dawn.

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

### 6.2 Column Top Plates (8)

500mm × 500mm × 20mm.

```
L350_tp_C1_gate_NW:   [-3.25, 3.75, 8.98] → [-2.75, 4.25, 9.0]
L350_tp_C2_gate_NE:   [2.75, 3.75, 8.98]  → [3.25, 4.25, 9.0]
L350_tp_C3_gate_SE:   [2.75, -4.25, 8.98] → [3.25, -3.75, 9.0]
L350_tp_C4_gate_SW:   [-3.25, -4.25, 8.98] → [-2.75, -3.75, 9.0]

L350_tp_C5_night_S:   [-10.25, -3.25, 5.98] → [-9.75, -2.75, 6.0]
L350_tp_C6_night_N:   [-10.25, 2.75, 5.98]  → [-9.75, 3.25, 6.0]

L350_tp_C7_dawn_S:    [9.75, -3.25, 6.98] → [10.25, -2.75, 7.0]
L350_tp_C8_dawn_N:    [9.75, 2.75, 6.98]  → [10.25, 3.25, 7.0]
```

### 6.3 Canopy Beam Brackets (C7 — 200mm embedment)

```
L350_bracket_canopy_W:   [-3.2, -0.3, 7.5] → [-3.0, 0.3, 7.7]
L350_bracket_canopy_E:   [3.0, -0.3, 7.5] → [3.2, 0.3, 7.7]
```

### 6.4 Mezzanine Beam Brackets (C8 — into wall thickness)

```
L350_bracket_mezz_night_N:   [-10.3, 6.0, 2.5] → [-9.7, 6.3, 2.7]
L350_bracket_mezz_night_S:   [-10.3, -6.3, 2.5] → [-9.7, -6.0, 2.7]
L350_bracket_mezz_dawn_N:    [9.7, 6.0, 2.8] → [10.3, 6.3, 3.0]
L350_bracket_mezz_dawn_S:    [9.7, -6.3, 2.8] → [10.3, -6.0, 3.0]
```

### 6.5 Wall Kickers (C11 — outer face corrected)

50mm × 50mm at wall base on outer face.

**Night** (Z=[0, 0.05]):
```
L350_kicker_night_N:   [-18.3, 6.3, 0.0]  → [-3.0, 6.35, 0.05]
L350_kicker_night_S:   [-18.3, -6.35, 0.0] → [-3.0, -6.3, 0.05]
L350_kicker_night_W:   [-18.35, -6.3, 0.0] → [-18.3, 6.3, 0.05]
```

**Gate** (Z=[0, 0.05]):
```
L350_kicker_gate_N:   [-3.3, 4.3, 0.0]  → [3.3, 4.35, 0.05]
L350_kicker_gate_S:   [-3.3, -4.35, 0.0] → [3.3, -4.3, 0.05]
L350_kicker_gate_E:   [3.3, -4.3, 0.0]  → [3.35, 4.3, 0.05]
L350_kicker_gate_W:   [-3.35, -4.3, 0.0] → [-3.3, 4.3, 0.05]
```

**Dawn** (Z=[0.3, 0.35]):
```
L350_kicker_dawn_N:   [3.3, 6.3, 0.3]  → [18.3, 6.35, 0.35]
L350_kicker_dawn_S:   [3.3, -6.35, 0.3] → [18.3, -6.3, 0.35]
L350_kicker_dawn_E:   [18.3, -6.3, 0.3] → [18.35, 6.3, 0.35]
```

### Section 6: 34 elements

---

## SECTION 7 — OPENING FRAMES + LINTELS (L350_Detail)

100mm × 100mm steel hollow section frames. RC lintels 300mm deep.

### 7.1 Night Entry (X=-18.3, Y=[-1.5,1.5], Z=[0,3.5])
```
L350_frame_night_entry_top:    [-18.4, -1.5, 3.5] → [-18.2, 1.5, 3.6]
L350_frame_night_entry_bot:    [-18.4, -1.5, -0.1] → [-18.2, 1.5, 0.0]
L350_frame_night_entry_jambN:  [-18.4, 1.4, -0.1] → [-18.2, 1.6, 3.6]
L350_frame_night_entry_jambS:  [-18.4, -1.6, -0.1] → [-18.2, -1.4, 3.6]
L350_lintel_night_entry:       [-18.6, -1.5, 3.5] → [-18.0, 1.5, 3.8]
```

### 7.2 Night Windows N1–N3 (Y=6.3 outer, 1.5m×2.0m each)
```
L350_frame_night_N1_top:    [-15.0, 6.2, 5.5] → [-13.5, 6.4, 5.6]
L350_frame_night_N1_bot:    [-15.0, 6.2, 3.4] → [-13.5, 6.4, 3.5]
L350_frame_night_N1_jambW:  [-15.1, 6.2, 3.4] → [-14.9, 6.4, 5.6]
L350_frame_night_N1_jambE:  [-13.6, 6.2, 3.4] → [-13.4, 6.4, 5.6]
L350_lintel_night_N1:       [-15.3, 6.0, 5.5] → [-13.2, 6.3, 5.8]

L350_frame_night_N2_top:    [-11.0, 6.2, 5.5] → [-9.5, 6.4, 5.6]
L350_frame_night_N2_bot:    [-11.0, 6.2, 3.4] → [-9.5, 6.4, 3.5]
L350_frame_night_N2_jambW:  [-11.1, 6.2, 3.4] → [-10.9, 6.4, 5.6]
L350_frame_night_N2_jambE:  [-9.6, 6.2, 3.4] → [-9.4, 6.4, 5.6]
L350_lintel_night_N2:       [-11.3, 6.0, 5.5] → [-9.2, 6.3, 5.8]

L350_frame_night_N3_top:    [-7.0, 6.2, 5.5] → [-5.5, 6.4, 5.6]
L350_frame_night_N3_bot:    [-7.0, 6.2, 3.4] → [-5.5, 6.4, 3.5]
L350_frame_night_N3_jambW:  [-7.1, 6.2, 3.4] → [-6.9, 6.4, 5.6]
L350_frame_night_N3_jambE:  [-5.6, 6.2, 3.4] → [-5.4, 6.4, 5.6]
L350_lintel_night_N3:       [-7.3, 6.0, 5.5] → [-5.2, 6.3, 5.8]
```

### 7.3 Dawn East Window (X=18.3, Y=[-3,3], Z=[1.3,6.3])
```
L350_frame_dawn_E_top:    [18.2, -3.0, 6.3] → [18.4, 3.0, 6.4]
L350_frame_dawn_E_bot:    [18.2, -3.0, 1.2] → [18.4, 3.0, 1.3]
L350_frame_dawn_E_jambN:  [18.2, 2.9, 1.2]  → [18.4, 3.1, 6.4]
L350_frame_dawn_E_jambS:  [18.2, -3.1, 1.2] → [18.4, -2.9, 6.4]
L350_lintel_dawn_E:       [18.0, -3.0, 6.3] → [18.6, 3.0, 6.6]
```

### 7.4 Dawn South Windows S1–S3 (Y=-6.3, 2.4m×4.7m each)
```
L350_frame_dawn_S1_top:    [5.5, -6.4, 5.8] → [7.9, -6.2, 5.9]
L350_frame_dawn_S1_bot:    [5.5, -6.4, 1.0] → [7.9, -6.2, 1.1]
L350_frame_dawn_S1_jambW:  [5.4, -6.4, 1.0] → [5.6, -6.2, 5.9]
L350_frame_dawn_S1_jambE:  [7.8, -6.4, 1.0] → [8.0, -6.2, 5.9]
L350_lintel_dawn_S1:       [5.2, -6.6, 5.8] → [8.2, -6.0, 6.1]

L350_frame_dawn_S2_top:    [9.3, -6.4, 5.8] → [11.7, -6.2, 5.9]
L350_frame_dawn_S2_bot:    [9.3, -6.4, 1.0] → [11.7, -6.2, 1.1]
L350_frame_dawn_S2_jambW:  [9.2, -6.4, 1.0] → [9.4, -6.2, 5.9]
L350_frame_dawn_S2_jambE:  [11.6, -6.4, 1.0] → [11.8, -6.2, 5.9]
L350_lintel_dawn_S2:       [9.0, -6.6, 5.8] → [12.0, -6.0, 6.1]

L350_frame_dawn_S3_top:    [13.1, -6.4, 5.8] → [15.5, -6.2, 5.9]
L350_frame_dawn_S3_bot:    [13.1, -6.4, 1.0] → [15.5, -6.2, 1.1]
L350_frame_dawn_S3_jambW:  [13.0, -6.4, 1.0] → [13.2, -6.2, 5.9]
L350_frame_dawn_S3_jambE:  [15.4, -6.4, 1.0] → [15.6, -6.2, 5.9]
L350_lintel_dawn_S3:       [12.8, -6.6, 5.8] → [15.8, -6.0, 6.1]
```

### 7.5 Dawn Exit Door (X=18.3, Y=[-1.5,1.5], Z=[0.3,4.0])
```
L350_frame_dawn_exit_top:    [18.2, -1.5, 4.0] → [18.4, 1.5, 4.1]
L350_frame_dawn_exit_bot:    [18.2, -1.5, 0.2] → [18.4, 1.5, 0.3]
L350_frame_dawn_exit_jambN:  [18.2, 1.4, 0.2]  → [18.4, 1.6, 4.1]
L350_frame_dawn_exit_jambS:  [18.2, -1.6, 0.2] → [18.4, -1.4, 4.1]
L350_lintel_dawn_exit:       [18.0, -1.5, 4.0] → [18.6, 1.5, 4.3]
```

### Section 7: 45 elements

---

## SECTION 8 — STAIR TREADS (L350_Detail) — C1 REDESIGNED

R=167mm (3000/18), G=300mm, 18 risers. Blondel = 2(167)+300 = 634mm.
Tread thickness: 50mm. Width: 6.0m (Y=[-3, 3]).

### 8.1 Night Stair (X=[-15.4, -10.0], Z=[0, 3.0], 18 treads)

```
L350_night_tread_01:   [-15.40, -3.0, 0.117] → [-15.10, 3.0, 0.167]
L350_night_tread_02:   [-15.10, -3.0, 0.284] → [-14.80, 3.0, 0.334]
L350_night_tread_03:   [-14.80, -3.0, 0.451] → [-14.50, 3.0, 0.501]
L350_night_tread_04:   [-14.50, -3.0, 0.617] → [-14.20, 3.0, 0.667]
L350_night_tread_05:   [-14.20, -3.0, 0.784] → [-13.90, 3.0, 0.834]
L350_night_tread_06:   [-13.90, -3.0, 0.951] → [-13.60, 3.0, 1.001]
L350_night_tread_07:   [-13.60, -3.0, 1.117] → [-13.30, 3.0, 1.167]
L350_night_tread_08:   [-13.30, -3.0, 1.284] → [-13.00, 3.0, 1.334]
L350_night_tread_09:   [-13.00, -3.0, 1.451] → [-12.70, 3.0, 1.501]
L350_night_tread_10:   [-12.70, -3.0, 1.617] → [-12.40, 3.0, 1.667]
L350_night_tread_11:   [-12.40, -3.0, 1.784] → [-12.10, 3.0, 1.834]
L350_night_tread_12:   [-12.10, -3.0, 1.951] → [-11.80, 3.0, 2.001]
L350_night_tread_13:   [-11.80, -3.0, 2.117] → [-11.50, 3.0, 2.167]
L350_night_tread_14:   [-11.50, -3.0, 2.284] → [-11.20, 3.0, 2.334]
L350_night_tread_15:   [-11.20, -3.0, 2.451] → [-10.90, 3.0, 2.501]
L350_night_tread_16:   [-10.90, -3.0, 2.617] → [-10.60, 3.0, 2.667]
L350_night_tread_17:   [-10.60, -3.0, 2.784] → [-10.30, 3.0, 2.834]
L350_night_tread_18:   [-10.30, -3.0, 2.950] → [-10.00, 3.0, 3.000]
```

### 8.2 Dawn Stair (X=[10.0, 15.4], Z=[0.3, 3.3], 18 treads)

```
L350_dawn_tread_01:   [10.00, -3.0, 0.417] → [10.30, 3.0, 0.467]
L350_dawn_tread_02:   [10.30, -3.0, 0.584] → [10.60, 3.0, 0.634]
L350_dawn_tread_03:   [10.60, -3.0, 0.751] → [10.90, 3.0, 0.801]
L350_dawn_tread_04:   [10.90, -3.0, 0.917] → [11.20, 3.0, 0.967]
L350_dawn_tread_05:   [11.20, -3.0, 1.084] → [11.50, 3.0, 1.134]
L350_dawn_tread_06:   [11.50, -3.0, 1.251] → [11.80, 3.0, 1.301]
L350_dawn_tread_07:   [11.80, -3.0, 1.417] → [12.10, 3.0, 1.467]
L350_dawn_tread_08:   [12.10, -3.0, 1.584] → [12.40, 3.0, 1.634]
L350_dawn_tread_09:   [12.40, -3.0, 1.751] → [12.70, 3.0, 1.801]
L350_dawn_tread_10:   [12.70, -3.0, 1.917] → [13.00, 3.0, 1.967]
L350_dawn_tread_11:   [13.00, -3.0, 2.084] → [13.30, 3.0, 2.134]
L350_dawn_tread_12:   [13.30, -3.0, 2.251] → [13.60, 3.0, 2.301]
L350_dawn_tread_13:   [13.60, -3.0, 2.417] → [13.90, 3.0, 2.467]
L350_dawn_tread_14:   [13.90, -3.0, 2.584] → [14.20, 3.0, 2.634]
L350_dawn_tread_15:   [14.20, -3.0, 2.751] → [14.50, 3.0, 2.801]
L350_dawn_tread_16:   [14.50, -3.0, 2.917] → [14.80, 3.0, 2.967]
L350_dawn_tread_17:   [14.80, -3.0, 3.084] → [15.10, 3.0, 3.134]
L350_dawn_tread_18:   [15.10, -3.0, 3.250] → [15.40, 3.0, 3.300]
```

### 8.3 Landings

```
L350_night_landing:   [-10.0, -3.0, 2.85] → [-8.0, 3.0, 3.0]
L350_dawn_landing:    [8.0, -3.0, 3.15] → [10.0, 3.0, 3.3]
```

### Section 8: 38 elements

---

## SECTION 9 — CANOPY EDGE (L400_Material) — C6 corrected

### 9.1 Drip Edges (below slab, Z=[7.97, 8.0])
```
L400_canopy_drip_N:   [-4.5, 4.47, 7.97] → [4.5, 4.5, 8.0]
L400_canopy_drip_S:   [-4.5, -4.5, 7.97] → [4.5, -4.47, 8.0]
L400_canopy_drip_W:   [-4.5, -4.5, 7.97] → [-4.47, 4.5, 8.0]
L400_canopy_drip_E:   [4.47, -4.5, 7.97] → [4.5, 4.5, 8.0]
```

### 9.2 Fascia (below slab, Z=[7.9, 8.0])
```
L400_canopy_fascia_N:   [-4.5, 4.45, 7.9] → [4.5, 4.5, 8.0]
L400_canopy_fascia_S:   [-4.5, -4.5, 7.9] → [4.5, -4.45, 8.0]
L400_canopy_fascia_W:   [-4.5, -4.5, 7.9] → [-4.45, 4.5, 8.0]
L400_canopy_fascia_E:   [4.45, -4.5, 7.9] → [4.5, 4.5, 8.0]
```

### Section 9: 8 elements

---

## SECTION 10 — FACADE PANEL JOINTS (L400_Material)

Dawn facades only. 5mm × 20mm, full height Z=[0.3, 7.0].

**North** (Y=6.3):
```
L400_dawn_pj_N_X6:    [6.500, 6.28, 0.3] → [6.505, 6.30, 7.0]
L400_dawn_pj_N_X10:   [10.500, 6.28, 0.3] → [10.505, 6.30, 7.0]
L400_dawn_pj_N_X14:   [14.500, 6.28, 0.3] → [14.505, 6.30, 7.0]
```

**South** (Y=-6.3):
```
L400_dawn_pj_S_X6:    [6.500, -6.30, 0.3] → [6.505, -6.28, 7.0]
L400_dawn_pj_S_X10:   [10.500, -6.30, 0.3] → [10.505, -6.28, 7.0]
L400_dawn_pj_S_X14:   [14.500, -6.30, 0.3] → [14.505, -6.28, 7.0]
```

### Section 10: 6 elements

---

## SECTION 11 — FOUNDATION (L400_Material) — C9/C10 corrected

900mm wide strip, depth to Z=-1.1 (800mm below slab bottom at Z=-0.3).

### Night perimeter:
```
L400_foundation_night_N:   [-18.6, 5.7, -1.1] → [-3.0, 6.6, -0.3]
L400_foundation_night_S:   [-18.6, -6.6, -1.1] → [-3.0, -5.7, -0.3]
L400_foundation_night_W:   [-18.6, -6.6, -1.1] → [-17.7, 6.6, -0.3]
```

### Gate perimeter (C10 — added E/W strips):
```
L400_foundation_gate_N:   [-3.6, 3.7, -1.1] → [3.6, 4.6, -0.3]
L400_foundation_gate_S:   [-3.6, -4.6, -1.1] → [3.6, -3.7, -0.3]
L400_foundation_gate_W:   [-3.6, -4.6, -1.1] → [-2.7, 4.6, -0.3]
L400_foundation_gate_E:   [2.7, -4.6, -1.1] → [3.6, 4.6, -0.3]
```

### Dawn perimeter:
```
L400_foundation_dawn_N:   [3.0, 5.7, -1.1] → [18.6, 6.6, -0.3]
L400_foundation_dawn_S:   [3.0, -6.6, -1.1] → [18.6, -5.7, -0.3]
L400_foundation_dawn_E:   [17.7, -6.6, -1.1] → [18.6, 6.6, -0.3]
```

### Section 11: 10 elements

---

## EXECUTION SUMMARY

| Section | Layer | Count |
|---------|-------|-------|
| A — Base building | Volumes, Structure, Openings, Circulation, Annotations | 49 |
| 1 — Roof system | L300_Roof | 10 |
| 2 — Roof assembly | L400_Material | 12 |
| 3 — Edge conditions | L400_Material | 12 |
| 4 — Formwork lines | L400_Material | 21 |
| 5 — Expansion joints | L400_Material | 4 |
| 6 — Structural connections | L350_Detail | 34 |
| 7 — Opening frames | L350_Detail | 45 |
| 8 — Stair treads | L350_Detail | 38 |
| 9 — Canopy edge | L400_Material | 8 |
| 10 — Facade joints | L400_Material | 6 |
| 11 — Foundation | L400_Material | 10 |
| **GRAND TOTAL** | | **249** |

---

## BUILD ORDER

1. Create 8 layers
2. **Batch 1 — Walls** (12 boxes): A1, A2, A3
3. **Batch 2 — Floors** (5 boxes): A4, A5, A6
4. **Batch 3 — Structure** (12 boxes): A7 columns + beams
5. **Batch 4 — Openings** (11 boxes): A8
6. **Batch 5 — Circulation** (3 elements): A9
7. **Batch 6 — Annotations** (6 text dots): A10
8. **Batch 7 — Roof** (10 boxes): Section 1
9. **Batch 8 — Roof assembly** (12 boxes): Section 2
10. **Batch 9 — Edge conditions** (12 boxes): Section 3
11. **Batch 10 — Formwork** (21 boxes): Section 4
12. **Batch 11 — Joints** (4 boxes): Section 5
13. **Batch 12 — Connections** (34 boxes): Section 6
14. **Batch 13 — Frames** (45 boxes): Section 7
15. **Batch 14 — Stairs** (38 boxes): Section 8
16. **Batch 15 — Canopy edge** (8 boxes): Section 9
17. **Batch 16 — Facade joints** (6 boxes): Section 10
18. **Batch 17 — Foundation** (10 boxes): Section 11

---

## EXECUTOR NOTES

1. All coordinates are meter-scale in a centimeter-unit Rhino doc. Use exactly as written.
2. Do NOT multiply by 100.
3. Target: port 9001 (`target: "structure"`).
4. Batch by section using `rhino_execute_python_code`.
5. After all geometry: capture Perspective, Top, Front, Right viewports.
6. Verify: Gate tallest (9m), Night compressed (6m), Dawn open (7m).
7. Verify: Z=0.3 level change visible at gate-dawn boundary.
8. Verify: Ramp visible alongside threshold.
9. Expansion joints and formwork use dark display color (RGB 20,20,20).

## DECISION LOG

| Decision | Verdict | Rationale |
|----------|---------|-----------|
| Wall overlap at gate junctions | Keep separate shells | Lock 01 convention; no structural issue |
| Stair dimensions | R=167mm, G=300mm, 18 risers | SIA 500 + Blondel 634mm |
| Threshold | 5.0m ramp at 6% | SIA 500 accessibility |
| Gate roof drainage | 1.5% fall south | SIA 271 minimum |
| Foundation depth | Z=-1.1 (800mm) | Swiss frost protection |
| Roof insulation | 200mm XPS | SIA 380/1 U≤0.17 |
| Canopy Y extent | ±4.5m | Weather protection overhang |
| Dawn mezzanine beam | Added | Structural necessity for landing |
| Formwork lifts Dawn | Local (Z=2.7, 5.1) | Construction sequence logic |
| Kickers | Outer face of walls | Corrected from draft |
| Parapets | Outer face alignment | Corrected from draft per Lock 01 |
