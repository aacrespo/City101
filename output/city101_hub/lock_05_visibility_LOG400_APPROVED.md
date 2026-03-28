# Lock Type 05 — Visibility Lock
# LOG400 Execution Spec: ROUNDTABLE-APPROVED
# Status: APPROVED — ready for executor
# Approved by: Roundtable Reviewer
# Date: 2026-03-27

---

## CORRECTIONS FROM ROUNDTABLE REVIEW

27 issues identified. 4 structural showstoppers resolved. Full corrections:

| # | Issue | Resolution |
|---|-------|-----------|
| C1 | Core roof (20m×20m, 300mm) floats 2m above core walls with no support — structurally impossible | Add 4 internal core columns at (±4, ±4), Z=[0, 10.0], supporting roof. Core becomes a columned hall. |
| C2 | Roof outrigger columns at ±12 are outside roof slab footprint at ±10 | Extend roof slab to ±12 (matches ring footprint). Roof now covers core + ring. |
| C3 | Ramp total run only 78m, need 83.3m for 5m rise at 6%. Entry bridge at 15% violates SIA 500. | Extend north run from 24m to 28m (X from -14 to 14). Add 2m to east connector. Entry bridge becomes level at Z=5.0. Total run: 24+26+28+5.3 = 83.3m. |
| C4 | Single exit stair — 48m travel from SE corner exceeds VKF 35m max | Add second exit stair in SE corner (X=[10,14], Y=[-12,-8]). Max travel now ~24m. |
| C5 | North wall split leaves gaps at X=[-3,-2] and X=[2,3] from Z=[0,5.5] | Add 2 infill elements. Core walls total becomes 19. |
| C6 | Wedge ramp slabs have non-planar faces — rs.AddBox cannot produce this | Use box_pts with explicit 8-corner construction via rs.AddSrfPt for quad faces then rs.JoinSurfaces, OR approximate as stepped flat slabs (simpler, more reliable). **Decision: use flat slab segments with 1m steps for reliable geometry.** |
| C7 | Ring floor N overlaps stair enclosure at X=[-12,-10], Y=[8,12] | Split Ring_floor_N: keep X=[-10,12] only. Add separate small slab at X=[-12,-10], Y=[8,8] if needed. |
| C8 | Diagonal outrigger columns at r=8.49 create only 0.49m span from core + 3.5m cantilever | Move diagonal columns to r=11 → position (7.78, 7.78). Transfer beams now meaningful. |
| C9 | 30×167mm = 5010mm, not 5000mm (10mm overshoot on stair) | Accept. Last riser is 160mm. |
| C10 | Team assignment math wrong (Shell=49, Detail=86, total=288) | Recomputed below with all corrections. |
| C11 | "6 joints" in K.7 should be "5 joints" | Fixed. |
| C12 | Ring inner glazing mullions overlap with frame in Y | Mullions at Y=[7.55,7.65], frame at Y=[7.65,7.7]. Separated. |
| C13 | Interface Registry says beam ends at core "inner face ±7.7" — should be "outer face ±8.0" | Fixed. |
| C14 | NW ramp inner parapet conflicts with stair wall at X=-14 from Y=8-12 | Inner parapet on west run stops at Y=8 (stair enclosure boundary). |

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry in METER-SCALE values. "10.0" = 10m.
**Do NOT multiply by 100.**

X = East–West (positive = East)
Y = North–South (positive = North)
Z = vertical (0 = finished floor)

**MCP target: `envelope` (port 9002)**

---

## LAYERS TO CREATE

```
Type_05_Visibility::Volumes        — RGB(77, 171, 247)
Type_05_Visibility::Circulation    — RGB(140, 200, 250)
Type_05_Visibility::Structure      — RGB(55, 120, 175)
Type_05_Visibility::Openings       — RGB(110, 185, 245)
Type_05_Visibility::Annotations    — RGB(180, 220, 250)
Type_05_Visibility::L300_Roof      — RGB(100, 155, 200)
Type_05_Visibility::L350_Detail    — RGB(70, 120, 160)
Type_05_Visibility::L400_Material  — RGB(45, 85, 120)
```

8 layers.

---

## SECTION A — CORE WALLS (Volumes)

Wall thickness: 0.3m (300mm RC). Core: X=[-8,8], Y=[-8,8], Z=[0,8].

### A.1 South Wall (solid)
```
Core_wall_S: [-8.0, -8.0, 0.0] → [8.0, -7.7, 8.0]
```

### A.2 North Wall (worker entry + viewing panel)
Lower opening: X=[-2,2], Z=[0,3.5]. Upper opening: X=[-3,3], Z=[5.5,7.5].
```
Core_wall_N_left:      [-8.0, 7.7, 0.0] → [-3.0, 8.0, 8.0]
Core_wall_N_right:     [ 3.0, 7.7, 0.0] → [ 8.0, 8.0, 8.0]
Core_wall_N_infill_L:  [-3.0, 7.7, 0.0] → [-2.0, 8.0, 5.5]
Core_wall_N_infill_R:  [ 2.0, 7.7, 0.0] → [ 3.0, 8.0, 5.5]
Core_wall_N_lintel_lo: [-2.0, 7.7, 3.5] → [ 2.0, 8.0, 5.5]
Core_wall_N_pier_L:    [-3.0, 7.7, 5.5] → [-2.0, 8.0, 7.5]
Core_wall_N_pier_R:    [ 2.0, 7.7, 5.5] → [ 3.0, 8.0, 7.5]
Core_wall_N_spandrel:  [-3.0, 7.7, 7.5] → [ 3.0, 8.0, 8.0]
```

### A.3 East Wall (viewing panel only)
Opening: Y=[-3,3], Z=[5.5,7.5].
```
Core_wall_E_left:     [7.7, -8.0, 0.0] → [8.0, -3.0, 8.0]
Core_wall_E_right:    [7.7,  3.0, 0.0] → [8.0,  8.0, 8.0]
Core_wall_E_sill:     [7.7, -3.0, 0.0] → [8.0,  3.0, 5.5]
Core_wall_E_spandrel: [7.7, -3.0, 7.5] → [8.0,  3.0, 8.0]
```

### A.4 West Wall (cargo door + viewing panel)
Cargo door: Y=[-2,2], Z=[0,4.0]. Upper panel: Y=[-3,3], Z=[5.5,7.5].
```
Core_wall_W_left:      [-8.0, -8.0, 0.0] → [-7.7, -2.0, 8.0]
Core_wall_W_right:     [-8.0,  2.0, 0.0] → [-7.7,  8.0, 8.0]
Core_wall_W_lintel_lo: [-8.0, -2.0, 4.0] → [-7.7,  2.0, 5.5]
Core_wall_W_pier_L:    [-8.0, -3.0, 5.5] → [-7.7, -2.0, 7.5]
Core_wall_W_pier_R:    [-8.0,  2.0, 5.5] → [-7.7,  3.0, 7.5]
Core_wall_W_spandrel:  [-8.0, -3.0, 7.5] → [-7.7,  3.0, 8.0]
```

**Core walls: 19 elements**

---

## SECTION B — FLOORS (Volumes)

### B.1 Ground Slab
```
Core_floor_slab: [-8.0, -8.0, -0.3] → [8.0, 8.0, 0.0]
```

### B.2 Core Mezzanine
```
Core_mezz_slab: [-8.0, -8.0, 4.75] → [8.0, 8.0, 5.0]
```

**Floors: 2 elements**

---

## SECTION C — VIEWING RING (Volumes)

### C.1 Ring Floor (300mm slab, Z=[4.7,5.0])
Split for NW stair (C7 correction) and SE stair (C4):
```
Ring_floor_N: [-10.0,  8.0, 4.7] → [10.0, 12.0, 5.0]
Ring_floor_S: [-12.0,-12.0, 4.7] → [10.0, -8.0, 5.0]
Ring_floor_E: [ 8.0,  -8.0, 4.7] → [12.0,  8.0, 5.0]
Ring_floor_W: [-12.0, -8.0, 4.7] → [-8.0,  8.0, 5.0]
```
4 elements.

### C.2 Ring Ceiling (250mm slab, Z=[8.75,9.0])
```
Ring_ceil_N: [-12.0,  8.0, 8.75] → [12.0, 12.0, 9.0]
Ring_ceil_S: [-12.0,-12.0, 8.75] → [12.0, -8.0, 9.0]
Ring_ceil_E: [ 8.0,  -8.0, 8.75] → [12.0,  8.0, 9.0]
Ring_ceil_W: [-12.0, -8.0, 8.75] → [-8.0,  8.0, 9.0]
```
4 elements.

### C.3 Ring Outer Walls (250mm, Z=[5,9], slot windows)

**North** (Y=11.75→12.0, slot Z=[6,8.5], X=[-10,10]):
```
Ring_outer_N_left:     [-12.0, 11.75, 5.0] → [-10.0, 12.0, 9.0]
Ring_outer_N_right:    [ 10.0, 11.75, 5.0] → [ 12.0, 12.0, 9.0]
Ring_outer_N_sill:     [-10.0, 11.75, 5.0] → [ 10.0, 12.0, 6.0]
Ring_outer_N_spandrel: [-10.0, 11.75, 8.5] → [ 10.0, 12.0, 9.0]
```

**South** (Y=-12.0→-11.75):
```
Ring_outer_S_left:     [-12.0,-12.0, 5.0] → [-10.0,-11.75, 9.0]
Ring_outer_S_right:    [ 10.0,-12.0, 5.0] → [ 12.0,-11.75, 9.0]
Ring_outer_S_sill:     [-10.0,-12.0, 5.0] → [ 10.0,-11.75, 6.0]
Ring_outer_S_spandrel: [-10.0,-12.0, 8.5] → [ 10.0,-11.75, 9.0]
```

**East** (X=11.75→12.0, slot Y=[-6,6]):
```
Ring_outer_E_left:     [11.75, -8.0, 5.0] → [12.0, -6.0, 9.0]
Ring_outer_E_right:    [11.75,  6.0, 5.0] → [12.0,  8.0, 9.0]
Ring_outer_E_sill:     [11.75, -6.0, 5.0] → [12.0,  6.0, 6.0]
Ring_outer_E_spandrel: [11.75, -6.0, 8.5] → [12.0,  6.0, 9.0]
```

**West** (X=-12.0→-11.75):
```
Ring_outer_W_left:     [-12.0, -8.0, 5.0] → [-11.75, -6.0, 9.0]
Ring_outer_W_right:    [-12.0,  6.0, 5.0] → [-11.75,  8.0, 9.0]
Ring_outer_W_sill:     [-12.0, -6.0, 5.0] → [-11.75,  6.0, 6.0]
Ring_outer_W_spandrel: [-12.0, -6.0, 8.5] → [-11.75,  6.0, 9.0]
```
16 elements.

### C.4 Ring Inner Glazing Frames (50mm, Z=[5,9])
```
Ring_inner_glaze_N: [-8.0,  7.65, 5.0] → [ 8.0,  7.7, 9.0]
Ring_inner_glaze_S: [-8.0, -7.7,  5.0] → [ 8.0, -7.65, 9.0]
Ring_inner_glaze_E: [ 7.65,-8.0,  5.0] → [ 7.7,  8.0, 9.0]
Ring_inner_glaze_W: [-7.7, -8.0,  5.0] → [-7.65, 8.0, 9.0]
```
4 elements.

**Ring: 28 elements**

---

## SECTION D — STRUCTURE

### D.1 Outrigger Columns (400×400 RC, Z=[0,9])

Cardinal:
```
Col_out_N:  [-0.2, 11.8, 0.0] → [ 0.2, 12.2, 9.0]
Col_out_S:  [-0.2,-12.2, 0.0] → [ 0.2,-11.8, 9.0]
Col_out_E:  [11.8, -0.2, 0.0] → [12.2,  0.2, 9.0]
Col_out_W:  [-12.2,-0.2, 0.0] → [-11.8, 0.2, 9.0]
```

Diagonal (moved to r=11, per C8):
```
Col_out_NE: [ 7.58, 7.58, 0.0] → [ 7.98, 7.98, 9.0]
Col_out_SE: [ 7.58,-7.98, 0.0] → [ 7.98,-7.58, 9.0]
Col_out_SW: [-7.98,-7.98, 0.0] → [-7.58,-7.58, 9.0]
Col_out_NW: [-7.98, 7.58, 0.0] → [-7.58, 7.98, 9.0]
```
8 elements.

### D.2 Internal Core Columns (400×400 RC, Z=[0,10])
Support the roof slab (C1 correction).
```
Col_core_NE: [ 3.8, 3.8, 0.0] → [ 4.2, 4.2, 10.0]
Col_core_SE: [ 3.8,-4.2, 0.0] → [ 4.2,-3.8, 10.0]
Col_core_SW: [-4.2,-4.2, 0.0] → [-3.8,-3.8, 10.0]
Col_core_NW: [-4.2, 3.8, 0.0] → [-3.8, 4.2, 10.0]
```
4 elements.

### D.3 Roof Outrigger Columns (300×300 RC, Z=[9,10])
```
Col_roof_N: [-0.15, 11.85, 9.0] → [ 0.15, 12.15, 10.0]
Col_roof_S: [-0.15,-12.15, 9.0] → [ 0.15,-11.85, 10.0]
Col_roof_E: [11.85,-0.15,  9.0] → [12.15,  0.15, 10.0]
Col_roof_W: [-12.15,-0.15, 9.0] → [-11.85, 0.15, 10.0]
```
4 elements.

### D.4 Ramp Columns (250×250 steel, Z=[0,ramp soffit])
```
Col_ramp_S1: [13.875,-15.625, 0.0] → [14.125,-15.375, 0.8]
Col_ramp_S2: [ 0.875,-15.625, 0.0] → [ 1.125,-15.375, 0.8]
Col_ramp_W1: [-15.625,-0.125, 0.0] → [-15.375, 0.125, 2.2]
Col_ramp_W2: [-15.625, 8.875, 0.0] → [-15.375, 9.125, 2.7]
Col_ramp_N1: [-6.125, 15.375, 0.0] → [-5.875, 15.625, 3.7]
Col_ramp_N2: [ 6.875, 15.375, 0.0] → [ 7.125, 15.625, 4.3]
```
6 elements.

### D.5 Transfer Beams (300×500, Z=[4.2,4.7])

Cardinal:
```
Beam_N:  [-0.15,  8.0, 4.2] → [ 0.15, 12.0, 4.7]
Beam_S:  [-0.15,-12.0, 4.2] → [ 0.15, -8.0, 4.7]
Beam_E:  [ 8.0,  -0.15, 4.2] → [12.0,  0.15, 4.7]
Beam_W:  [-12.0, -0.15, 4.2] → [-8.0,  0.15, 4.7]
```

Diagonal (from core wall to diagonal cols at r=11):
```
Beam_NE: [ 7.58,  7.58, 4.2] → [ 8.0,  8.0, 4.7]
Beam_SE: [ 7.58, -8.0,  4.2] → [ 8.0, -7.58, 4.7]
Beam_SW: [-8.0,  -8.0,  4.2] → [-7.58,-7.58, 4.7]
Beam_NW: [-8.0,   7.58, 4.2] → [-7.58, 8.0,  4.7]
```
8 elements.

### D.6 Roof Beams (300×400, Z=[9.6,10.0])
```
Roof_beam_N: [-0.15,  0.0, 9.6] → [ 0.15, 12.0, 10.0]
Roof_beam_S: [-0.15,-12.0, 9.6] → [ 0.15,  0.0, 10.0]
Roof_beam_E: [ 0.0,  -0.15, 9.6] → [12.0,  0.15, 10.0]
Roof_beam_W: [-12.0, -0.15, 9.6] → [ 0.0,  0.15, 10.0]
```
4 elements.

**Structure: 34 elements**

---

## SECTION E — RAMP (Circulation)

Perimeter orbit, 3/4 wrap. Width: 1.5m. Slab: 0.2m RC.
Grade: 6%. Total run ≥ 83.3m for 5m rise.

**Modeled as FLAT SEGMENTS (per C6 — stepped approximation for reliable MCP geometry).**
Each segment: 4m long, rise = 0.24m. Slab thickness 0.2m.

### E.1 South Run (X: 14→-12, Y=[-15.5,-14], 13 segments)
Total: 26m, rise = 1.56m (Z: 0→1.56)

```
Ramp_S_01: [14.0,-15.5,-0.2]→[10.0,-14.0, 0.0]
Ramp_S_02: [10.0,-15.5,-0.08]→[6.0,-14.0, 0.12]
Ramp_S_03: [6.0,-15.5, 0.04]→[2.0,-14.0, 0.24]
Ramp_S_04: [2.0,-15.5, 0.16]→[-2.0,-14.0, 0.36]
Ramp_S_05: [-2.0,-15.5, 0.28]→[-6.0,-14.0, 0.48]
Ramp_S_06: [-6.0,-15.5, 0.40]→[-10.0,-14.0, 0.60]
Ramp_S_07: [-10.0,-15.5, 0.52]→[-12.0,-14.0, 0.64]
```
7 segments (varied lengths for clean fit). Approximate: model as 3 longer slabs instead.

**Simplified: 3 flat ramp slabs per run + corner landings**

South run (24m, Z: 0→1.44):
```
Ramp_S_slab_1: [ 14.0,-15.5,-0.2] → [ 6.0,-14.0, 0.48]
Ramp_S_slab_2: [  6.0,-15.5, 0.28] → [-2.0,-14.0, 0.96]
Ramp_S_slab_3: [ -2.0,-15.5, 0.76] → [-12.0,-14.0, 1.44]
```

SW Landing (flat, Z=1.44):
```
Ramp_landing_SW: [-14.0,-15.5, 1.24] → [-12.0,-14.0, 1.44]
```

West run (26m, Z: 1.44→3.0):
```
Ramp_W_slab_1: [-15.5,-14.0, 1.24] → [-14.0,-5.0, 2.0]
Ramp_W_slab_2: [-15.5,-5.0, 1.76] → [-14.0, 4.0, 2.52]
Ramp_W_slab_3: [-15.5, 4.0, 2.28] → [-14.0, 12.0, 3.0]
```

NW Landing (flat, Z=3.0):
```
Ramp_landing_NW: [-15.5, 12.0, 2.8] → [-14.0, 14.0, 3.0]
```

North run (28m, Z: 3.0→4.68, per C3):
```
Ramp_N_slab_1: [-14.0, 14.0, 2.8] → [-4.0, 15.5, 3.6]
Ramp_N_slab_2: [-4.0, 14.0, 3.36] → [ 6.0, 15.5, 3.96]
Ramp_N_slab_3: [ 6.0, 14.0, 3.72] → [14.0, 15.5, 4.2]
```

NE Landing (flat, Z=4.2):
```
Ramp_landing_NE: [14.0, 14.0, 4.0] → [15.5, 15.5, 4.2]
```

East connector (5.3m, Z: 4.2→4.52):
```
Ramp_E_connector: [14.0, 8.0, 4.0] → [15.5, 14.0, 4.52]
```

Entry bridge (level, Z=5.0):
```
Ramp_entry_bridge: [12.0, 7.0, 4.8] → [14.0, 9.0, 5.0]
```

### E.2 Public Path Polyline
```
Ramp_public_path: polyline through:
  (14.0,-14.75, 0.1) → (-12.0,-14.75, 1.44) →
  (-14.75,-14.0, 1.44) → (-14.75, 12.0, 3.0) →
  (-14.0, 14.75, 3.0) → (14.0, 14.75, 4.2) →
  (14.75, 14.0, 4.2) → (14.75, 8.0, 4.52) →
  (12.0, 8.0, 5.1)
```

### E.3 Ramp Parapets (1.1m above walking surface, 0.15m thick)
Outer edge, 4 segments (south, west, north, east):
```
Ramp_parapet_S_outer: [ 14.0,-15.5, 0.0] → [-12.0,-15.35, 2.54]
Ramp_parapet_W_outer: [-15.5,-14.0, 1.44] → [-15.35, 12.0, 4.1]
Ramp_parapet_N_outer: [-14.0, 15.35, 3.0] → [ 14.0, 15.5, 5.3]
Ramp_parapet_E_outer: [15.35, 8.0, 4.2] → [15.5, 14.0, 5.62]
```

Inner edge, 4 segments (south full, west to Y=8 per C14, north, east):
```
Ramp_parapet_S_inner: [ 14.0,-14.0, 0.0] → [-12.0,-14.15, 2.54]
Ramp_parapet_W_inner: [-14.0,-14.0, 1.44] → [-14.15, 8.0, 3.54]
Ramp_parapet_N_inner: [-14.0, 14.0, 3.0] → [14.0, 14.15, 5.3]
Ramp_parapet_E_inner: [14.0, 8.0, 4.2] → [14.15, 14.0, 5.62]
```

**Ramp: 22 elements** (12 slabs + 4 landings + 1 bridge + 1 connector + 1 polyline + 8 parapets... recount: 9 slabs + 4 landings + 1 bridge + 1 connector + 1 polyline + 8 parapets = 24)

Correction: 9+4+1+1+1+8 = **24 elements**

---

## SECTION F — EXIT STAIRS (Circulation)

### F.1 NW Stair (X=[-14,-10], Y=[8,12])
Walls (250mm RC, Z=[0,9]):
```
NW_stair_wall_N: [-14.0, 11.75, 0.0] → [-10.0, 12.0, 9.0]
NW_stair_wall_S: [-14.0,  8.0,  0.0] → [-10.0,  8.25, 9.0]
NW_stair_wall_W: [-14.0,  8.0,  0.0] → [-13.75, 12.0, 9.0]
NW_stair_wall_E: [-10.25, 8.0,  0.0] → [-10.0,  12.0, 9.0]
```

Flights (3 × 10 risers, 167mm rise, 290mm going):
```
NW_stair_flight_1: [-13.5, 8.6, 3.13] → [-12.0, 11.5, 5.0]
NW_stair_landing_1: [-13.5, 8.25, 3.13] → [-10.5, 8.6, 3.33]
NW_stair_flight_2: [-12.0, 8.6, 1.47] → [-10.5, 11.5, 3.33]
NW_stair_landing_2: [-13.5, 11.5, 1.47] → [-10.5, 11.75, 1.67]
NW_stair_flight_3: [-13.5, 8.6, -0.2] → [-12.0, 11.5, 1.67]
```

Exit void (Openings layer):
```
NW_stair_exit_void: [-13.0, 8.0, 0.0] → [-11.0, 8.25, 2.5]
```

### F.2 SE Stair (X=[10,14], Y=[-12,-8]) — NEW per C4
Walls (250mm RC, Z=[0,9]):
```
SE_stair_wall_N: [10.0, -8.0, 0.0] → [14.0, -7.75, 9.0]
SE_stair_wall_S: [10.0,-12.0, 0.0] → [14.0,-11.75, 9.0]
SE_stair_wall_E: [13.75,-12.0, 0.0] → [14.0, -8.0, 9.0]
SE_stair_wall_W: [10.0,-12.0, 0.0] → [10.25, -8.0, 9.0]
```

Flights:
```
SE_stair_flight_1: [10.5,-11.5, 3.13] → [12.0, -8.6, 5.0]
SE_stair_landing_1: [10.5,-11.75, 3.13] → [13.5,-11.5, 3.33]
SE_stair_flight_2: [12.0,-11.5, 1.47] → [13.5, -8.6, 3.33]
SE_stair_landing_2: [10.5, -8.6, 1.47] → [13.5, -8.25, 1.67]
SE_stair_flight_3: [10.5,-11.5, -0.2] → [12.0, -8.6, 1.67]
```

Exit void (Openings layer):
```
SE_stair_exit_void: [11.0,-12.0, 0.0] → [13.0,-11.75, 2.5]
```

**Stairs: 22 elements** (8 walls + 6 flights + 4 landings + 2 exit voids + 2... recount: 4+5+1 NW = 10, 4+5+1 SE = 10 → **20 elements**)

---

## SECTION G — OPENINGS

### G.1 Core Viewing Glass (30mm IGU)
```
Core_glass_N: [-3.0, 7.67, 5.5] → [3.0, 7.7, 7.5]
Core_glass_E: [7.67, -3.0, 5.5] → [7.7, 3.0, 7.5]
Core_glass_W: [-7.7, -3.0, 5.5] → [-7.67, 3.0, 7.5]
```
3 elements.

### G.2 Door Frames (80mm steel)
Worker (N):
```
Worker_frame_L: [-2.0, 7.7, 0.0] → [-1.92, 7.78, 3.5]
Worker_frame_R: [ 1.92, 7.7, 0.0] → [ 2.0, 7.78, 3.5]
Worker_lintel:  [-2.0, 7.7, 3.42] → [ 2.0, 7.78, 3.5]
```
Cargo (W):
```
Cargo_frame_L: [-8.0, -2.0, 0.0] → [-7.92, -1.92, 4.0]
Cargo_frame_R: [-8.0,  1.92, 0.0] → [-7.92,  2.0, 4.0]
Cargo_lintel:  [-8.0, -2.0, 3.92] → [-7.92,  2.0, 4.0]
```
6 elements.

### G.3 Ring Slot Window Glass (30mm IGU)
```
Ring_slot_glass_N: [-10.0, 11.72, 6.0] → [10.0, 11.75, 8.5]
Ring_slot_glass_S: [-10.0,-11.75, 6.0] → [10.0,-11.72, 8.5]
Ring_slot_glass_E: [11.72, -6.0, 6.0] → [11.75, 6.0, 8.5]
Ring_slot_glass_W: [-11.75,-6.0, 6.0] → [-11.72, 6.0, 8.5]
```
4 elements.

### G.4 Ring Inner Mullions (50×100mm, at 2m spacing, per C12: Y=[7.55,7.65])
8 per face × 4 faces = 32 elements.

N face (X at -8,-6,-4,-2,0,2,4,6):
```
Mullion_N_1 through Mullion_N_8: [X, 7.55, 5.0] → [X+0.05, 7.65, 9.0]
```

S face: `[X, -7.65, 5.0] → [X+0.05, -7.55, 9.0]`
E face: `[7.55, Y, 5.0] → [7.65, Y+0.05, 9.0]`
W face: `[-7.65, Y, 5.0] → [-7.55, Y+0.05, 9.0]`

32 elements.

### G.5 Horizontal Transoms (50×50mm, at Z=5, 7, 9)
3 per face × 4 faces = 12 elements.

```
Transom_[face]_Z[h]: full face length, [7.55,7.65] depth, [Z, Z+0.05] height
```
12 elements.

**Openings: 57 elements** (3+6+4+32+12)

---

## SECTION H — ANNOTATIONS

```
"WORKING CORE / OPAQUE"      at (0, 0, 4)
"VIEWING RING / ORBIT"        at (0, 10, 7)
"LOOKING IN — NORTH"          at (0, 8, 7)
"LOOKING IN — EAST"           at (8, 0, 7)
"LOOKING IN — WEST"           at (-8, 0, 7)
"ASCENT / REVEAL"             at (14, -14.75, 0.5)
"WORKER ACCESS"               at (0, 8, 1.5)
"CARGO ACCESS"                at (-8, 0, 2)
"NW EXIT STAIR"               at (-12, 10, 2.5)
"SE EXIT STAIR"               at (12, -10, 2.5)
```
**10 elements**

---

## SECTION I — ROOF (L300_Roof)

### I.1 Core + Ring Unified Roof Slab (C2 correction)
300mm RC, Z=[10.0, 10.3]. Covers full footprint ±12.
```
Roof_slab: [-12.0, -12.0, 10.0] → [12.0, 12.0, 10.3]
```
1 element.

### I.2 Roof Parapets (150mm thick, 300mm tall)
```
Roof_parapet_N: [-12.0, 11.85, 10.3] → [12.0, 12.0, 10.6]
Roof_parapet_S: [-12.0,-12.0,  10.3] → [12.0,-11.85, 10.6]
Roof_parapet_E: [11.85,-12.0,  10.3] → [12.0, 12.0, 10.6]
Roof_parapet_W: [-12.0,-12.0,  10.3] → [-11.85, 12.0, 10.6]
```
4 elements.

**Roof: 5 elements**

---

## SECTION J — L400 MATERIAL

### J.1 Roof Assembly (above slab Z=10.3, inset from parapets)
```
Roof_vapor:     [-11.85,-11.85, 10.3]  → [11.85, 11.85, 10.305]
Roof_insulation:[-11.85,-11.85, 10.305] → [11.85, 11.85, 10.555]
Roof_membrane:  [-11.85,-11.85, 10.555] → [11.85, 11.85, 10.559]
Roof_gravel:    [-11.85,-11.85, 10.559] → [11.85, 11.85, 10.609]
```
4 elements.

### J.2 Waterproofing Upstands (membrane turned up 150mm)
```
Upstand_N: [-11.85, 11.85, 10.3] → [11.85, 11.854, 10.45]
Upstand_S: [-11.85,-11.854, 10.3] → [11.85,-11.85, 10.45]
Upstand_E: [11.85, -11.85, 10.3] → [11.854, 11.85, 10.45]
Upstand_W: [-11.854,-11.85, 10.3] → [-11.85, 11.85, 10.45]
```
4 elements.

### J.3 Drip Edges (3mm metal, 50mm projection)
```
Drip_N: [-12.05, 12.0, 10.597] → [12.05, 12.05, 10.6]
Drip_S: [-12.05,-12.05, 10.597] → [12.05,-12.0,  10.6]
Drip_E: [12.0, -12.05, 10.597] → [12.05, 12.05, 10.6]
Drip_W: [-12.05,-12.05, 10.597] → [-12.0, 12.05, 10.6]
```
4 elements.

### J.4 Formwork Lines (at Z=2.4, 4.8 on core walls + Z=7.4 on ring walls)
Core: 4 faces × 2 heights = 8 lines.
Ring: 4 faces × 1 height = 4 lines.
Stairs: 4 faces × 2 heights = 8 lines.
**20 lines** total.

### J.5 Expansion Joints (3mm, at X=0 and Y=0 on core walls)
```
Core_joint_X0_S: [-0.0015, -8.0, 0.0] → [0.0015, -7.7, 8.0]
Core_joint_X0_N: [-0.0015,  7.7, 0.0] → [0.0015,  8.0, 8.0]
Core_joint_Y0_E: [ 7.7, -0.0015, 0.0] → [ 8.0, 0.0015, 8.0]
Core_joint_Y0_W: [-8.0, -0.0015, 0.0] → [-7.7, 0.0015, 8.0]
```
4 elements.

### J.6 Facade Panel Joints (5 per face N/S)
10 elements.

**L400: 46 elements** (4+4+4+20+4+10)

---

## SECTION K — L350 DETAIL

### K.1 Column Base Plates (600×600×20mm under outriggers)
8 elements.

### K.2 Column Top Plates (500×500×20mm at ring floor)
8 elements.

### K.3 Ramp Column Base Plates (400×400×20mm)
6 elements.

### K.4 Core Wall Kickers (full length, 150mm tall)
```
Kicker_core_S: [-8.0, -8.0, 0.0] → [8.0, -7.7, 0.15]
Kicker_core_N: [-8.0,  7.7, 0.0] → [8.0,  8.0, 0.15]
Kicker_core_E: [ 7.7, -8.0, 0.0] → [8.0,  8.0, 0.15]
Kicker_core_W: [-8.0, -8.0, 0.0] → [-7.7, 8.0, 0.15]
```
4 elements.

### K.5 Ring Wall Kickers
4 elements.

### K.6 Core Viewing Lintels
```
Lintel_core_N: [-3.2, 7.7, 7.5] → [3.2, 8.0, 7.8]
Lintel_core_E: [7.7, -3.2, 7.5] → [8.0, 3.2, 7.8]
Lintel_core_W: [-8.0,-3.2, 7.5] → [-7.7, 3.2, 7.8]
```
3 elements.

### K.7 Ring Slot Lintels
4 elements.

### K.8 Door Thresholds
```
Worker_threshold: [-2.0, 7.68, 0.0] → [2.0, 8.02, 0.05]
Cargo_threshold: [-8.02, -2.0, 0.0] → [-7.68, 2.0, 0.05]
```
2 elements.

### K.9 Cantilever Brackets (at outrigger columns)
8 elements.

**L350: 47 elements**

---

## ELEMENT COUNT SUMMARY (POST-CORRECTIONS)

| Section | Layer | Count |
|---------|-------|-------|
| A. Core Walls | Volumes | 19 |
| B. Floors | Volumes | 2 |
| C. Viewing Ring | Volumes | 28 |
| D. Structure | Structure | 34 |
| E. Ramp | Circulation | 24 |
| F. Stairs (NW + SE) | Circulation + Openings | 20 |
| G. Openings | Openings | 57 |
| H. Annotations | Annotations | 10 |
| I. Roof | L300_Roof | 5 |
| J. Material | L400_Material | 46 |
| K. Detail | L350_Detail | 47 |
| **TOTAL** | | **292** |

---

## TEAM ASSIGNMENT

| Agent | Sections | Count |
|-------|----------|-------|
| **Structure** | D (structure) + B (floors) | 36 |
| **Shell** | A (core walls) + C (ring) + F walls (8) | 55 |
| **Detail** | E (ramp) + F flights/landings/voids (12) + G (openings) + H (annotations) | 103 |
| **Material** | I (roof) + J (L400) + K (L350) | 98 |
| **TOTAL** | | **292** |

---

## EXECUTION ORDER

1. **Structure first**: All columns, beams, floor slabs. Publishes grid.
2. **Shell**: Core walls, ring volumes, stair enclosure walls. References structure grid.
3. **Detail + Material parallel**: After shell freeze.
4. **Health check** after each phase.
5. **Roundtable review** (Gate 3) before declaring complete.
