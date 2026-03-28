# Lock Type 05 — Visibility Lock
# LOG400 Complete Geometry Specification
# Status: DRAFT FOR ROUNDTABLE REVIEW — do NOT execute until approved
# Architect: Claude (Nova — Henna Max)
# Date: 2026-03-27

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry is authored in METER-SCALE values (X=-15.5 to 15.5, Y=-15.5 to 15.5, Z=0 to 11.56).
"10.0" in Rhino = 10.0 as a number, displayed as "10 cm" but conceptually 10m.

**ALL coordinates in this spec are meter-scale. Use them exactly as written.**
**Do NOT multiply by 100. Do NOT convert.**

X = East–West axis (positive = East)
Y = North–South axis (positive = North)
Z = vertical (0 = finished floor level)

**MCP target: `envelope` (port 9002)**

---

## BUILDING CONCEPT

**The Visibility Lock** — infrastructure made legible. A central opaque working core is surrounded by an elevated viewing ring. The public orbits the machine to understand it. Unlike the Cargo Lock (linear, stacked), the Visibility Lock is orbital — a panopticon inverted.

**State transition:** Opaque (hidden system) ↔ Transparent (legible system)

**Spatial logic:**
- Working Core (Z=0–8): the machine room. Opaque at ground, selectively glazed at upper level.
- Viewing Ring (Z=5–9): elevated gallery orbiting the core. Glass inward (look IN), solid outward.
- Ascending Ramp: wraps 3/4 of the building perimeter — the ascent IS the orbit.
- Exit Stair: compact descent, NW corner.
- Roof Canopy (Z=10–11): shelters core top + ring.

**Four circulations:**
1. Public: ground entry (SE) → ramp orbit → ring → exit stair (NW) → ground
2. Worker: ground entry (N face) → core interior
3. Cargo: ground entry (W face) → core interior (service door)
4. Visual: from ring, looking INTO core through glazing (the architecture of watching)

---

## SECTION A: LAYERS

Create ALL layers before placing any geometry.

```
Type_05_Visibility::Volumes        — RGB(77, 171, 247)   — primary massing (walls, floors)
Type_05_Visibility::Circulation    — RGB(140, 200, 250)  — ramp slabs, stair treads, paths
Type_05_Visibility::Structure      — RGB(55, 120, 175)   — columns, beams, transfer structure
Type_05_Visibility::Openings       — RGB(110, 185, 245)  — glazing frames, mullions, door voids
Type_05_Visibility::Annotations    — RGB(180, 220, 250)  — text dots
Type_05_Visibility::L300_Roof      — RGB(100, 155, 200)  — roof slabs, parapets
Type_05_Visibility::L350_Detail    — RGB(70, 120, 160)   — base plates, top plates, brackets, kickers, frames, lintels
Type_05_Visibility::L400_Material  — RGB(45, 85, 120)    — formwork lines, expansion joints, membrane, insulation, gravel, drip edges, upstands
```

**Total: 8 layers**

---

## SECTION B: WORKING CORE WALLS

Layer: `Type_05_Visibility::Volumes`
Wall thickness: 0.3 (300mm RC — Archibase: RC wall structural, REI 90)
Core structural envelope: X=[-8, 8], Y=[-8, 8], Z=[0, 8]

### B.1 South Wall (Y = -8.0 to -7.7)

Solid — worker entry on north side, cargo on west. South face is blank.

```
Core_wall_S: [-8.0, -8.0, 0.0] → [8.0, -7.7, 8.0]
```
1 element.

### B.2 North Wall (Y = 7.7 to 8.0)

Opening: Worker entry — X=[-2, 2], Z=[0, 3.5] (4m wide, 3.5m tall)
Opening: Upper viewing panel — X=[-3, 3], Z=[5.5, 7.5] (6m wide, 2m tall)

Split into 5 pieces:

```
Core_wall_N_left:     [-8.0, 7.7, 0.0] → [-2.0, 8.0, 8.0]
Core_wall_N_right:    [ 2.0, 7.7, 0.0] → [ 8.0, 8.0, 8.0]
Core_wall_N_lintel_L: [-2.0, 7.7, 3.5] → [ 2.0, 8.0, 5.5]
Core_wall_N_spandrel: [-3.0, 7.7, 7.5] → [ 3.0, 8.0, 8.0]
Core_wall_N_pier_mid: [-2.0, 7.7, 5.5] → [-3.0, 8.0, 7.5]
```

Wait — the two openings overlap in X-range but not in Z. Let me split more carefully:

Between Z=0–3.5: opening at X=[-2,2]
Between Z=3.5–5.5: solid (lintel zone for lower + sill zone for upper)
Between Z=5.5–7.5: opening at X=[-3,3]
Between Z=7.5–8.0: solid spandrel

```
Core_wall_N_left:      [-8.0, 7.7, 0.0] → [-2.0, 8.0, 8.0]
Core_wall_N_right:     [ 2.0, 7.7, 0.0] → [ 8.0, 8.0, 8.0]
Core_wall_N_lintel_lo: [-2.0, 7.7, 3.5] → [ 2.0, 8.0, 5.5]
Core_wall_N_pier_L:    [-3.0, 7.7, 5.5] → [-2.0, 8.0, 7.5]
Core_wall_N_pier_R:    [ 2.0, 7.7, 5.5] → [ 3.0, 8.0, 7.5]
Core_wall_N_spandrel:  [-3.0, 7.7, 7.5] → [ 3.0, 8.0, 8.0]
```
6 elements.

### B.3 East Wall (X = 7.7 to 8.0)

Opening: Upper viewing panel — Y=[-3, 3], Z=[5.5, 7.5]

```
Core_wall_E_left:     [7.7, -8.0, 0.0] → [8.0, -3.0, 8.0]
Core_wall_E_right:    [7.7,  3.0, 0.0] → [8.0,  8.0, 8.0]
Core_wall_E_sill:     [7.7, -3.0, 0.0] → [8.0,  3.0, 5.5]
Core_wall_E_spandrel: [7.7, -3.0, 7.5] → [8.0,  3.0, 8.0]
```
4 elements.

### B.4 West Wall (X = -8.0 to -7.7)

Opening: Cargo/service door — Y=[-2, 2], Z=[0, 4.0] (4m wide, 4m tall)
Opening: Upper viewing panel — Y=[-3, 3], Z=[5.5, 7.5]

```
Core_wall_W_left:      [-8.0, -8.0, 0.0] → [-7.7, -2.0, 8.0]
Core_wall_W_right:     [-8.0,  2.0, 0.0] → [-7.7,  8.0, 8.0]
Core_wall_W_lintel_lo: [-8.0, -2.0, 4.0] → [-7.7,  2.0, 5.5]
Core_wall_W_pier_L:    [-8.0, -3.0, 5.5] → [-7.7, -2.0, 7.5]
Core_wall_W_pier_R:    [-8.0,  2.0, 5.5] → [-7.7,  3.0, 7.5]
Core_wall_W_spandrel:  [-8.0, -3.0, 7.5] → [-7.7,  3.0, 8.0]
```
6 elements.

**Core walls subtotal: 17 elements**

---

## SECTION C: CORE FLOOR SLAB

Layer: `Type_05_Visibility::Volumes`

### C.1 Ground Floor Slab

300mm RC ground-bearing slab (Archibase: RC slab on grade, 300mm min for industrial loading).

```
Core_floor_slab: [-8.0, -8.0, -0.3] → [8.0, 8.0, 0.0]
```
1 element.

### C.2 Core Intermediate Floor

At Z=5.0. This is a partial floor inside the core (the machine room has a mezzanine).
250mm RC slab.

```
Core_mezz_slab: [-8.0, -8.0, 4.75] → [8.0, 8.0, 5.0]
```
1 element.

**Floor subtotal: 2 elements**

---

## SECTION D: VIEWING RING

Layer: `Type_05_Visibility::Volumes`

### D.1 Ring Floor Slab

300mm RC slab at Z=[4.7, 5.0]. Forms a square ring around the core.
Inner edge at core outer face (±8.0). Outer edge at ±12.0.

4 rectangular slabs (avoiding overlap at corners — N/S strips run full width, E/W strips fill gaps):

```
Ring_floor_N: [-12.0,  8.0, 4.7] → [12.0, 12.0, 5.0]
Ring_floor_S: [-12.0,-12.0, 4.7] → [12.0, -8.0, 5.0]
Ring_floor_E: [ 8.0,  -8.0, 4.7] → [12.0,  8.0, 5.0]
Ring_floor_W: [-12.0, -8.0, 4.7] → [-8.0,  8.0, 5.0]
```
4 elements.

### D.2 Ring Ceiling Slab

250mm RC slab at Z=[8.75, 9.0].

```
Ring_ceil_N: [-12.0,  8.0, 8.75] → [12.0, 12.0, 9.0]
Ring_ceil_S: [-12.0,-12.0, 8.75] → [12.0, -8.0, 9.0]
Ring_ceil_E: [ 8.0,  -8.0, 8.75] → [12.0,  8.0, 9.0]
Ring_ceil_W: [-12.0, -8.0, 8.75] → [-8.0,  8.0, 9.0]
```
4 elements.

### D.3 Ring Outer Walls

250mm RC with outer slot windows (Z=[6, 8.5]). Height: Z=[5.0, 9.0].

**North outer wall** (Y = 11.75 to 12.0):
- Opening: continuous slot Z=[6.0, 8.5], X=[-10, 10] (20m wide)

```
Ring_outer_N_left:    [-12.0, 11.75, 5.0] → [-10.0, 12.0, 9.0]
Ring_outer_N_right:   [ 10.0, 11.75, 5.0] → [ 12.0, 12.0, 9.0]
Ring_outer_N_sill:    [-10.0, 11.75, 5.0] → [ 10.0, 12.0, 6.0]
Ring_outer_N_spandrel:[-10.0, 11.75, 8.5] → [ 10.0, 12.0, 9.0]
```
4 elements.

**South outer wall** (Y = -12.0 to -11.75):
Same pattern.
```
Ring_outer_S_left:    [-12.0,-12.0, 5.0] → [-10.0,-11.75, 9.0]
Ring_outer_S_right:   [ 10.0,-12.0, 5.0] → [ 12.0,-11.75, 9.0]
Ring_outer_S_sill:    [-10.0,-12.0, 5.0] → [ 10.0,-11.75, 6.0]
Ring_outer_S_spandrel:[-10.0,-12.0, 8.5] → [ 10.0,-11.75, 9.0]
```
4 elements.

**East outer wall** (X = 11.75 to 12.0):
Opening: slot Z=[6.0, 8.5], Y=[-6, 6] (12m wide)
```
Ring_outer_E_left:    [11.75, -8.0, 5.0] → [12.0, -6.0, 9.0]
Ring_outer_E_right:   [11.75,  6.0, 5.0] → [12.0,  8.0, 9.0]
Ring_outer_E_sill:    [11.75, -6.0, 5.0] → [12.0,  6.0, 6.0]
Ring_outer_E_spandrel:[11.75, -6.0, 8.5] → [12.0,  6.0, 9.0]
```
4 elements.

**West outer wall** (X = -12.0 to -11.75):
Same pattern.
```
Ring_outer_W_left:    [-12.0, -8.0, 5.0] → [-11.75, -6.0, 9.0]
Ring_outer_W_right:   [-12.0,  6.0, 5.0] → [-11.75,  8.0, 9.0]
Ring_outer_W_sill:    [-12.0, -6.0, 5.0] → [-11.75,  6.0, 6.0]
Ring_outer_W_spandrel:[-12.0, -6.0, 8.5] → [-11.75,  6.0, 9.0]
```
4 elements.

**Ring outer walls subtotal: 16 elements**

### D.4 Ring Inner Glazing Frame

The inner face of the ring (at the core wall line, ±8) is full curtain wall glazing — public looks INTO the core. Modeled as thin mullion frames (50mm deep) at Z=[5.0, 9.0].

```
Ring_inner_glaze_N: [-8.0,  7.65, 5.0] → [ 8.0,  7.7, 9.0]
Ring_inner_glaze_S: [-8.0, -7.7,  5.0] → [ 8.0, -7.65, 9.0]
Ring_inner_glaze_E: [ 7.65,-8.0,  5.0] → [ 7.7,  8.0, 9.0]
Ring_inner_glaze_W: [-7.7, -8.0,  5.0] → [-7.65, 8.0, 9.0]
```
4 elements.

**Ring subtotal: 28 elements**

---

## SECTION E: STRUCTURE

Layer: `Type_05_Visibility::Structure`

### E.1 Outrigger Columns

8 columns at 45° intervals around the ring, at 12m radius from center.
Column size: 0.4 × 0.4 (400×400mm RC — Archibase: minimum for 4-story public building).
Height: Z=[0, 9.0] (ground to ring ceiling).

Cardinal positions (centered on column):
```
Col_out_N:  [-0.2, 11.8, 0.0] → [ 0.2, 12.2, 9.0]
Col_out_S:  [-0.2,-12.2, 0.0] → [ 0.2,-11.8, 9.0]
Col_out_E:  [11.8, -0.2, 0.0] → [12.2,  0.2, 9.0]
Col_out_W:  [-12.2,-0.2, 0.0] → [-11.8, 0.2, 9.0]
```

Diagonal positions (at 8.49m from each axis):
```
Col_out_NE: [ 8.29, 8.29, 0.0] → [ 8.69, 8.69, 9.0]
Col_out_SE: [ 8.29,-8.69, 0.0] → [ 8.69,-8.29, 9.0]
Col_out_SW: [-8.69,-8.69, 0.0] → [-8.29,-8.29, 9.0]
Col_out_NW: [-8.69, 8.29, 0.0] → [-8.29, 8.69, 9.0]
```
8 elements.

### E.2 Roof Outrigger Columns

4 columns extending from ring ceiling to roof canopy. At cardinal positions only.
Column size: 0.3 × 0.3 (300×300mm RC).
Height: Z=[9.0, 10.0].

```
Col_roof_N: [-0.15, 11.85, 9.0] → [ 0.15, 12.15, 10.0]
Col_roof_S: [-0.15,-12.15, 9.0] → [ 0.15,-11.85, 10.0]
Col_roof_E: [11.85,-0.15,  9.0] → [12.15,  0.15, 10.0]
Col_roof_W: [-12.15,-0.15, 9.0] → [-11.85, 0.15, 10.0]
```
4 elements.

### E.3 Ramp Columns

6 columns supporting the perimeter ramp, at corners and midpoints of each run.
Column size: 0.25 × 0.25 (250×250mm steel — Archibase: hollow steel section).
Height: Z=[0, varies to ramp soffit].

South run supports (Y = -14.0):
```
Col_ramp_S1: [13.875,-14.125, 0.0] → [14.125,-13.875, 1.7]
Col_ramp_S2: [ 0.875,-14.125, 0.0] → [ 1.125,-13.875, 1.7]
```

West run supports (X = -14.0):
```
Col_ramp_W1: [-14.125,-13.875, 0.0] → [-13.875,-13.625, 3.36]
Col_ramp_W2: [-14.125,  0.875, 0.0] → [-13.875,  1.125, 3.36]
```

North run supports (Y = 14.0):
```
Col_ramp_N1: [-13.875, 13.875, 0.0] → [-13.625, 14.125, 4.92]
Col_ramp_N2: [  0.875, 13.875, 0.0] → [  1.125, 14.125, 4.92]
```
6 elements.

### E.4 Transfer Beams (Core to Ring)

8 radial beams from core wall outer face to outrigger columns at ring floor level.
Beam depth: 0.5m (Z = 4.2 to 4.7). Beam width: 0.3m.

Cardinal beams:
```
Beam_N:  [-0.15,  8.0, 4.2] → [ 0.15, 12.0, 4.7]
Beam_S:  [-0.15,-12.0, 4.2] → [ 0.15, -8.0, 4.7]
Beam_E:  [ 8.0,  -0.15, 4.2] → [12.0,  0.15, 4.7]
Beam_W:  [-12.0, -0.15, 4.2] → [-8.0,  0.15, 4.7]
```

Diagonal beams (from core corners to diagonal columns):
```
Beam_NE: [ 8.0,  8.0, 4.2] → [ 8.69,  8.69, 4.7]
Beam_SE: [ 8.0, -8.69, 4.2] → [ 8.69, -8.0,  4.7]
Beam_SW: [-8.69,-8.69, 4.2] → [-8.0, -8.0,  4.7]
Beam_NW: [-8.69, 8.0,  4.2] → [-8.0,  8.69, 4.7]
```
8 elements.

### E.5 Roof Beams

4 beams from core top to ring outer edge at roof level.
Beam depth: 0.4m (Z = 9.6 to 10.0). Beam width: 0.3m.

```
Roof_beam_N: [-0.15,  8.0, 9.6] → [ 0.15, 12.0, 10.0]
Roof_beam_S: [-0.15,-12.0, 9.6] → [ 0.15, -8.0, 10.0]
Roof_beam_E: [ 8.0,  -0.15, 9.6] → [12.0,  0.15, 10.0]
Roof_beam_W: [-12.0, -0.15, 9.6] → [-8.0,  0.15, 10.0]
```
4 elements.

**Structure subtotal: 30 elements**

---

## SECTION F: ASCENDING RAMP (Perimeter Orbit)

Layer: `Type_05_Visibility::Circulation`

The ramp wraps 3/4 of the building perimeter counterclockwise from SE to NE. This IS the architectural event — you orbit the machine as you ascend.

Ramp width: 1.5m (SIA 500 preferred).
Ramp slab thickness: 0.2m (200mm RC).
Grade: 6% (SIA 500 compliant). Landings every 10m of ramp run minimum.
Handrails: both sides (modeled in L350_Detail).

Total rise: 5.0m (ground to ring floor at Z=5.0).
Total run at 6%: 83.3m. Perimeter available (3/4 orbit at 14m from center): ~84m.

### F.1 South Run (East to West)

Start: X=12, Y=-14, Z=0.0
End: X=-12, Y=-14, Z=1.44
Length: 24m. Rise: 1.44m. Grade: 6%.
Slab: wedge from Z=[-0.2, 0.0] at east end to Z=[1.24, 1.44] at west end.

Modeled as box_pts (8 explicit corners):
```
Ramp_S_run:
  pt0: [12.0, -15.5, -0.2]    pt1: [-12.0, -15.5, 1.24]
  pt2: [-12.0, -14.0, 1.24]   pt3: [12.0, -14.0, -0.2]
  pt4: [12.0, -15.5, 0.0]     pt5: [-12.0, -15.5, 1.44]
  pt6: [-12.0, -14.0, 1.44]   pt7: [12.0, -14.0, 0.0]
```
1 element.

### F.2 SW Corner Landing

Flat landing at Z=1.44. Size: 2.0 × 1.5m.
```
Ramp_landing_SW: [-14.0, -15.5, 1.24] → [-12.0, -14.0, 1.44]
```
1 element.

### F.3 West Run (South to North)

Start: X=-14, Y=-14, Z=1.44
End: X=-14, Y=12, Z=3.0
Length: 26m. Rise: 1.56m. Grade: 6%.

```
Ramp_W_run:
  pt0: [-15.5, -14.0, 1.24]   pt1: [-15.5, 12.0, 2.8]
  pt2: [-14.0, 12.0, 2.8]     pt3: [-14.0, -14.0, 1.24]
  pt4: [-15.5, -14.0, 1.44]   pt5: [-15.5, 12.0, 3.0]
  pt6: [-14.0, 12.0, 3.0]     pt7: [-14.0, -14.0, 1.44]
```
1 element.

### F.4 NW Corner Landing

Flat landing at Z=3.0.
```
Ramp_landing_NW: [-15.5, 12.0, 2.8] → [-14.0, 14.0, 3.0]
```
1 element.

### F.5 North Run (West to East)

Start: X=-12, Y=14, Z=3.0
End: X=12, Y=14, Z=4.44
Length: 24m. Rise: 1.44m. Grade: 6%.

```
Ramp_N_run:
  pt0: [-12.0, 14.0, 2.8]     pt1: [12.0, 14.0, 4.24]
  pt2: [12.0, 15.5, 4.24]     pt3: [-12.0, 15.5, 2.8]
  pt4: [-12.0, 14.0, 3.0]     pt5: [12.0, 14.0, 4.44]
  pt6: [12.0, 15.5, 4.44]     pt7: [-12.0, 15.5, 3.0]
```
1 element.

### F.6 NE Corner Landing

Flat landing at Z=4.44.
```
Ramp_landing_NE: [12.0, 14.0, 4.24] → [14.0, 15.5, 4.44]
```
1 element.

### F.7 East Connector (North to Ring Entry)

Start: X=14, Y=12, Z=4.44
End: X=14, Y=8, Z=4.68 (short 4m run + bridge to ring)
Then horizontal bridge to ring at Z=5.0.

Actually — model a final short ramp + level bridge:
```
Ramp_E_connector:
  pt0: [14.0, 12.0, 4.24]     pt1: [14.0, 8.0, 4.48]
  pt2: [15.5, 8.0, 4.48]      pt3: [15.5, 12.0, 4.24]
  pt4: [14.0, 12.0, 4.44]     pt5: [14.0, 8.0, 4.68]
  pt6: [15.5, 8.0, 4.68]      pt7: [15.5, 12.0, 4.44]
```
1 element.

### F.8 Ring Entry Bridge

Level bridge connecting ramp end to ring floor at Z=5.0.
Small ramp: X=[12, 14], Y=[7, 9], Z=[4.68 → 5.0] (2m × 2m, 16% — this is a threshold step, modeled as slab).

Actually for code compliance, use a short slab at ring level:
```
Ramp_entry_bridge: [12.0, 7.0, 4.7] → [14.0, 9.0, 5.0]
```
1 element.

### F.9 Ramp Perimeter Walls (Low Walls / Parapets)

Outer edge parapet wall, 1.1m tall (SIA 358 guardrail height for public buildings), 0.15m thick:

```
Ramp_parapet_S: [12.0, -15.5, 0.0] → [-12.0, -15.35, 1.1]
```
Wait — the parapet follows the ramp slope. Model as wedge.

For simplification at LOG 400, model ramp parapets as 4 sloped thin walls:

South parapet (outer edge):
```
Ramp_parapet_S_outer:
  pt0: [12.0, -15.5, 0.0]     pt1: [-12.0, -15.5, 1.44]
  pt2: [-12.0, -15.35, 1.44]  pt3: [12.0, -15.35, 0.0]
  pt4: [12.0, -15.5, 1.1]     pt5: [-12.0, -15.5, 2.54]
  pt6: [-12.0, -15.35, 2.54]  pt7: [12.0, -15.35, 1.1]
```

South parapet (inner edge):
```
Ramp_parapet_S_inner:
  pt0: [12.0, -14.0, 0.0]     pt1: [-12.0, -14.0, 1.44]
  pt2: [-12.0, -14.15, 1.44]  pt3: [12.0, -14.15, 0.0]
  pt4: [12.0, -14.0, 1.1]     pt5: [-12.0, -14.0, 2.54]
  pt6: [-12.0, -14.15, 2.54]  pt7: [12.0, -14.15, 1.1]
```

West parapet (outer):
```
Ramp_parapet_W_outer:
  pt0: [-15.5, -14.0, 1.44]   pt1: [-15.5, 12.0, 3.0]
  pt2: [-15.35, 12.0, 3.0]    pt3: [-15.35, -14.0, 1.44]
  pt4: [-15.5, -14.0, 2.54]   pt5: [-15.5, 12.0, 4.1]
  pt6: [-15.35, 12.0, 4.1]    pt7: [-15.35, -14.0, 2.54]
```

West parapet (inner):
```
Ramp_parapet_W_inner:
  pt0: [-14.0, -14.0, 1.44]   pt1: [-14.0, 12.0, 3.0]
  pt2: [-14.15, 12.0, 3.0]    pt3: [-14.15, -14.0, 1.44]
  pt4: [-14.0, -14.0, 2.54]   pt5: [-14.0, 12.0, 4.1]
  pt6: [-14.15, 12.0, 4.1]    pt7: [-14.15, -14.0, 2.54]
```

North parapet (outer):
```
Ramp_parapet_N_outer:
  pt0: [-12.0, 15.5, 3.0]     pt1: [12.0, 15.5, 4.44]
  pt2: [12.0, 15.35, 4.44]    pt3: [-12.0, 15.35, 3.0]
  pt4: [-12.0, 15.5, 4.1]     pt5: [12.0, 15.5, 5.54]
  pt6: [12.0, 15.35, 5.54]    pt7: [-12.0, 15.35, 4.1]
```

North parapet (inner):
```
Ramp_parapet_N_inner:
  pt0: [-12.0, 14.0, 3.0]     pt1: [12.0, 14.0, 4.44]
  pt2: [12.0, 14.15, 4.44]    pt3: [-12.0, 14.15, 3.0]
  pt4: [-12.0, 14.0, 4.1]     pt5: [12.0, 14.0, 5.54]
  pt6: [12.0, 14.15, 5.54]    pt7: [-12.0, 14.15, 4.1]
```

6 parapet elements (outer S, inner S, outer W, inner W, outer N, inner N).

### F.10 Public Path Polyline

```
Ramp_public_path: polyline through:
  (13.0, -14.75, 0.1) → (-13.0, -14.75, 1.44) →
  (-14.75, -13.0, 1.44) → (-14.75, 13.0, 3.0) →
  (-13.0, 14.75, 3.0) → (13.0, 14.75, 4.44) →
  (14.75, 10.0, 4.68) → (12.0, 8.0, 5.1)
```
1 polyline element.

**Ramp subtotal: 14 elements**

---

## SECTION G: EXIT STAIR

Layer: `Type_05_Visibility::Circulation`

NW quadrant: X=[-14, -10], Y=[8, 12]. From Z=5.0 to Z=0.

### G.1 Stair Enclosure Walls

250mm RC walls, Z=[0, 9.0] (full height to ring ceiling for fire compartment — VKF REI 90).

```
Stair_wall_N: [-14.0, 11.75, 0.0] → [-10.0, 12.0, 9.0]
Stair_wall_S: [-14.0,  8.0,  0.0] → [-10.0, 8.25, 9.0]
Stair_wall_W: [-14.0,  8.0,  0.0] → [-13.75,12.0, 9.0]
Stair_wall_E: [-10.25, 8.0,  0.0] → [-10.0, 12.0, 9.0]
```
4 elements.

### G.2 Stair Flights

3 flights of 10 risers each (total 30 risers × 167mm = 5.0m rise).
Rise: 167mm. Going: 290mm. 2R+G = 624mm (Blondel compliant).
Flight width: 1.5m (VKF: ≥1500mm for public buildings).

**Flight 1** (Z=5.0 → 3.33, descending): along Y from 11.5 to 8.5
```
Stair_flight_1:
  pt0: [-13.5, 11.5, 3.13]    pt1: [-13.5, 8.6, 4.8]
  pt2: [-12.0, 8.6, 4.8]      pt3: [-12.0, 11.5, 3.13]
  pt4: [-13.5, 11.5, 3.33]    pt5: [-13.5, 8.6, 5.0]
  pt6: [-12.0, 8.6, 5.0]      pt7: [-12.0, 11.5, 3.33]
```
1 element.

**Landing 1** at Z=3.33:
```
Stair_landing_1: [-13.5, 8.25, 3.13] → [-10.5, 8.6, 3.33]
```
1 element.

**Flight 2** (Z=3.33 → 1.67): along Y from 8.6 to 11.5 (return direction)
```
Stair_flight_2:
  pt0: [-12.0, 8.6, 1.47]     pt1: [-12.0, 11.5, 3.13]
  pt2: [-10.5, 11.5, 3.13]    pt3: [-10.5, 8.6, 1.47]
  pt4: [-12.0, 8.6, 1.67]     pt5: [-12.0, 11.5, 3.33]
  pt6: [-10.5, 11.5, 3.33]    pt7: [-10.5, 8.6, 1.67]
```
1 element.

**Landing 2** at Z=1.67:
```
Stair_landing_2: [-13.5, 11.5, 1.47] → [-10.5, 11.75, 1.67]
```
1 element.

**Flight 3** (Z=1.67 → 0.0): along Y from 11.5 to 8.5
```
Stair_flight_3:
  pt0: [-13.5, 11.5, -0.2]    pt1: [-13.5, 8.6, 1.47]
  pt2: [-12.0, 8.6, 1.47]     pt3: [-12.0, 11.5, -0.2]
  pt4: [-13.5, 11.5, 0.0]     pt5: [-13.5, 8.6, 1.67]
  pt6: [-12.0, 8.6, 1.67]     pt7: [-12.0, 11.5, 0.0]
```
1 element.

### G.3 Ground Exit Door Void

In stair south wall at Z=[0, 2.5], Y=8.0, X=[-13, -11]:
```
Stair_exit_void: [-13.0, 8.0, 0.0] → [-11.0, 8.25, 2.5]
```
Layer: `Type_05_Visibility::Openings`
1 element.

**Stair subtotal: 9 elements (+ 1 opening)**

---

## SECTION H: OPENINGS

Layer: `Type_05_Visibility::Openings`

### H.1 Core Viewing Panels (4 faces, upper level)

Large glazed panels on core walls visible from the ring. Modeled as thin glass panes (30mm IGU).

North panel: X=[-3, 3], Z=[5.5, 7.5], Y=7.7
```
Core_glass_N: [-3.0, 7.67, 5.5] → [3.0, 7.7, 7.5]
```

East panel: Y=[-3, 3], Z=[5.5, 7.5], X=7.7
```
Core_glass_E: [7.67, -3.0, 5.5] → [7.7, 3.0, 7.5]
```

South panel (no opening in south wall — skip. South core wall is solid).

West panel: Y=[-3, 3], Z=[5.5, 7.5], X=-7.7
```
Core_glass_W: [-7.7, -3.0, 5.5] → [-7.67, 3.0, 7.5]
```
3 elements.

### H.2 Worker Entry Door Frame

North face: X=[-2, 2], Z=[0, 3.5], Y=8.0. Modeled as frame (80mm × 80mm steel).
```
Worker_door_frame_L: [-2.0, 7.7, 0.0] → [-1.92, 7.78, 3.5]
Worker_door_frame_R: [ 1.92, 7.7, 0.0] → [ 2.0, 7.78, 3.5]
Worker_door_lintel:  [-2.0, 7.7, 3.42] → [ 2.0, 7.78, 3.5]
```
3 elements.

### H.3 Cargo Door Frame

West face: Y=[-2, 2], Z=[0, 4.0], X=-8.0.
```
Cargo_door_frame_L: [-8.0, -2.0, 0.0] → [-7.92, -1.92, 4.0]
Cargo_door_frame_R: [-8.0,  1.92, 0.0] → [-7.92,  2.0, 4.0]
Cargo_door_lintel:  [-8.0, -2.0, 3.92] → [-7.92,  2.0, 4.0]
```
3 elements.

### H.4 Ring Outer Slot Window Glass

Continuous slot glazing in ring outer walls. 30mm triple IGU.

```
Ring_slot_glass_N: [-10.0, 11.72, 6.0] → [10.0, 11.75, 8.5]
Ring_slot_glass_S: [-10.0,-11.75, 6.0] → [10.0,-11.72, 8.5]
Ring_slot_glass_E: [11.72, -6.0, 6.0] → [11.75, 6.0, 8.5]
Ring_slot_glass_W: [-11.75,-6.0, 6.0] → [-11.72, 6.0, 8.5]
```
4 elements.

### H.5 Ring Inner Curtain Wall Mullions

Vertical mullions at 2m spacing on ring inner face. 50mm × 100mm aluminum.
North face: 8 mullions from X=-8 to X=8 at 2m intervals.

```
Mullion_N_1: [-8.0, 7.6, 5.0] → [-7.95, 7.7, 9.0]
Mullion_N_2: [-6.0, 7.6, 5.0] → [-5.95, 7.7, 9.0]
Mullion_N_3: [-4.0, 7.6, 5.0] → [-3.95, 7.7, 9.0]
Mullion_N_4: [-2.0, 7.6, 5.0] → [-1.95, 7.7, 9.0]
Mullion_N_5: [ 0.0, 7.6, 5.0] → [ 0.05, 7.7, 9.0]
Mullion_N_6: [ 2.0, 7.6, 5.0] → [ 2.05, 7.7, 9.0]
Mullion_N_7: [ 4.0, 7.6, 5.0] → [ 4.05, 7.7, 9.0]
Mullion_N_8: [ 6.0, 7.6, 5.0] → [ 6.05, 7.7, 9.0]
```

South face: 8 mullions
```
Mullion_S_1: [-8.0, -7.7, 5.0] → [-7.95, -7.6, 9.0]
Mullion_S_2: [-6.0, -7.7, 5.0] → [-5.95, -7.6, 9.0]
Mullion_S_3: [-4.0, -7.7, 5.0] → [-3.95, -7.6, 9.0]
Mullion_S_4: [-2.0, -7.7, 5.0] → [-1.95, -7.6, 9.0]
Mullion_S_5: [ 0.0, -7.7, 5.0] → [ 0.05, -7.6, 9.0]
Mullion_S_6: [ 2.0, -7.7, 5.0] → [ 2.05, -7.6, 9.0]
Mullion_S_7: [ 4.0, -7.7, 5.0] → [ 4.05, -7.6, 9.0]
Mullion_S_8: [ 6.0, -7.7, 5.0] → [ 6.05, -7.6, 9.0]
```

East face: 8 mullions (along Y)
```
Mullion_E_1: [7.6, -8.0, 5.0] → [7.7, -7.95, 9.0]
Mullion_E_2: [7.6, -6.0, 5.0] → [7.7, -5.95, 9.0]
Mullion_E_3: [7.6, -4.0, 5.0] → [7.7, -3.95, 9.0]
Mullion_E_4: [7.6, -2.0, 5.0] → [7.7, -1.95, 9.0]
Mullion_E_5: [7.6,  0.0, 5.0] → [7.7,  0.05, 9.0]
Mullion_E_6: [7.6,  2.0, 5.0] → [7.7,  2.05, 9.0]
Mullion_E_7: [7.6,  4.0, 5.0] → [7.7,  4.05, 9.0]
Mullion_E_8: [7.6,  6.0, 5.0] → [7.7,  6.05, 9.0]
```

West face: 8 mullions
```
Mullion_W_1: [-7.7, -8.0, 5.0] → [-7.6, -7.95, 9.0]
Mullion_W_2: [-7.7, -6.0, 5.0] → [-7.6, -5.95, 9.0]
Mullion_W_3: [-7.7, -4.0, 5.0] → [-7.6, -3.95, 9.0]
Mullion_W_4: [-7.7, -2.0, 5.0] → [-7.6, -1.95, 9.0]
Mullion_W_5: [-7.7,  0.0, 5.0] → [-7.6,  0.05, 9.0]
Mullion_W_6: [-7.7,  2.0, 5.0] → [-7.6,  2.05, 9.0]
Mullion_W_7: [-7.7,  4.0, 5.0] → [-7.6,  4.05, 9.0]
Mullion_W_8: [-7.7,  6.0, 5.0] → [-7.6,  6.05, 9.0]
```
32 mullions total.

### H.6 Horizontal Transoms (Ring Inner Curtain Wall)

Horizontal members at Z=5.0, Z=7.0, Z=9.0 on each inner face. 50mm × 100mm.

Per face: 3 transoms × 4 faces = 12 transoms.

North face:
```
Transom_N_Z5: [-8.0, 7.6, 5.0] → [8.0, 7.7, 5.05]
Transom_N_Z7: [-8.0, 7.6, 7.0] → [8.0, 7.7, 7.05]
Transom_N_Z9: [-8.0, 7.6, 8.95] → [8.0, 7.7, 9.0]
```

South face:
```
Transom_S_Z5: [-8.0, -7.7, 5.0] → [8.0, -7.6, 5.05]
Transom_S_Z7: [-8.0, -7.7, 7.0] → [8.0, -7.6, 7.05]
Transom_S_Z9: [-8.0, -7.7, 8.95] → [8.0, -7.6, 9.0]
```

East face:
```
Transom_E_Z5: [7.6, -8.0, 5.0] → [7.7, 8.0, 5.05]
Transom_E_Z7: [7.6, -8.0, 7.0] → [7.7, 8.0, 7.05]
Transom_E_Z9: [7.6, -8.0, 8.95] → [7.7, 8.0, 9.0]
```

West face:
```
Transom_W_Z5: [-7.7, -8.0, 5.0] → [-7.6, 8.0, 5.05]
Transom_W_Z7: [-7.7, -8.0, 7.0] → [-7.6, 8.0, 7.05]
Transom_W_Z9: [-7.7, -8.0, 8.95] → [-7.6, 8.0, 9.0]
```
12 elements.

**Openings subtotal: 58 elements (incl. stair exit void)**

---

## SECTION I: ANNOTATIONS

Layer: `Type_05_Visibility::Annotations`

```
TextDot: "WORKING CORE / OPAQUE"      at (0, 0, 4)
TextDot: "VIEWING RING / ORBIT"        at (0, 10, 7)
TextDot: "LOOKING IN — NORTH"          at (0, 8, 7)
TextDot: "LOOKING IN — EAST"           at (8, 0, 7)
TextDot: "LOOKING IN — WEST"           at (-8, 0, 7)
TextDot: "ASCENT / REVEAL"             at (13, -14.75, 0.5)
TextDot: "WORKER ACCESS"               at (0, 8, 1.5)
TextDot: "CARGO ACCESS"                at (-8, 0, 2)
TextDot: "EXIT STAIR"                  at (-12, 10, 2.5)
```
9 elements.

---

## SECTION J: ROOF SYSTEM

Layer: `Type_05_Visibility::L300_Roof`

### J.1 Core Roof Slab

300mm RC slab over the core, with 2m overhang on all sides.
Z = [10.0, 10.3].

```
Core_roof_slab: [-10.0, -10.0, 10.0] → [10.0, 10.0, 10.3]
```
1 element.

### J.2 Core Roof Parapets

150mm thick, 300mm tall upstands above roof level (SIA 271 minimum).
Z = [10.3, 10.6].

```
Core_parapet_N: [-10.0,  9.85, 10.3] → [10.0, 10.0, 10.6]
Core_parapet_S: [-10.0,-10.0,  10.3] → [10.0, -9.85, 10.6]
Core_parapet_E: [ 9.85,-10.0,  10.3] → [10.0, 10.0, 10.6]
Core_parapet_W: [-10.0,-10.0,  10.3] → [-9.85, 10.0, 10.6]
```
4 elements.

### J.3 Ring Roof Slab

250mm RC slab over the viewing ring. Z = [9.0, 9.25].
Already modeled as Ring_ceil in Section D.2 — this section adds the WATERPROOFING layers above it.

Skip structural slab (exists as D.2). Add assembly layers in Section K (L400_Material).

### J.4 Ring Roof Parapets

On ring outer edge. 150mm thick, 300mm tall. Z = [9.0, 9.3].

```
Ring_parapet_N: [-12.0, 11.85, 9.0] → [12.0, 12.0, 9.3]
Ring_parapet_S: [-12.0,-12.0,  9.0] → [12.0,-11.85, 9.3]
Ring_parapet_E: [11.85, -8.0,  9.0] → [12.0,  8.0, 9.3]
Ring_parapet_W: [-12.0, -8.0,  9.0] → [-11.85, 8.0, 9.3]
```
4 elements.

**Roof subtotal: 9 elements**

---

## SECTION K: L400 MATERIAL LAYERS

Layer: `Type_05_Visibility::L400_Material`

### K.1 Core Roof Assembly (warm flat roof — Archibase)

Built above Core_roof_slab (Z=10.3):

| Layer | Thickness | Z range |
|-------|-----------|---------|
| Vapor barrier | 0.005 | 10.30 – 10.305 |
| Insulation (EPS) | 0.25 | 10.305 – 10.555 |
| Waterproof membrane | 0.004 | 10.555 – 10.559 |
| Gravel ballast | 0.05 | 10.559 – 10.609 |

Inset 0.15m from parapet inner faces (inside parapets):

```
Core_roof_vapor:     [-9.85, -9.85, 10.3]   → [9.85, 9.85, 10.305]
Core_roof_insulation:[-9.85, -9.85, 10.305]  → [9.85, 9.85, 10.555]
Core_roof_membrane:  [-9.85, -9.85, 10.555]  → [9.85, 9.85, 10.559]
Core_roof_gravel:    [-9.85, -9.85, 10.559]  → [9.85, 9.85, 10.609]
```
4 elements.

### K.2 Ring Roof Assembly

Built above Ring_ceil slabs (Z=9.0). Same assembly:

North strip:
```
Ring_roof_vapor_N:     [-11.85,  8.0, 9.0]  → [11.85, 11.85, 9.005]
Ring_roof_insulation_N:[-11.85,  8.0, 9.005] → [11.85, 11.85, 9.255]
Ring_roof_membrane_N:  [-11.85,  8.0, 9.255] → [11.85, 11.85, 9.259]
Ring_roof_gravel_N:    [-11.85,  8.0, 9.259] → [11.85, 11.85, 9.309]
```

South strip:
```
Ring_roof_vapor_S:     [-11.85,-11.85, 9.0]  → [11.85, -8.0, 9.005]
Ring_roof_insulation_S:[-11.85,-11.85, 9.005] → [11.85, -8.0, 9.255]
Ring_roof_membrane_S:  [-11.85,-11.85, 9.255] → [11.85, -8.0, 9.259]
Ring_roof_gravel_S:    [-11.85,-11.85, 9.259] → [11.85, -8.0, 9.309]
```

East strip:
```
Ring_roof_vapor_E:     [ 8.0, -8.0, 9.0]  → [11.85, 8.0, 9.005]
Ring_roof_insulation_E:[ 8.0, -8.0, 9.005] → [11.85, 8.0, 9.255]
Ring_roof_membrane_E:  [ 8.0, -8.0, 9.255] → [11.85, 8.0, 9.259]
Ring_roof_gravel_E:    [ 8.0, -8.0, 9.259] → [11.85, 8.0, 9.309]
```

West strip:
```
Ring_roof_vapor_W:     [-11.85, -8.0, 9.0]  → [-8.0, 8.0, 9.005]
Ring_roof_insulation_W:[-11.85, -8.0, 9.005] → [-8.0, 8.0, 9.255]
Ring_roof_membrane_W:  [-11.85, -8.0, 9.255] → [-8.0, 8.0, 9.259]
Ring_roof_gravel_W:    [-11.85, -8.0, 9.259] → [-8.0, 8.0, 9.309]
```
16 elements.

### K.3 Waterproofing Upstands

At parapet bases. 0.004m thick membrane turned up parapet inner face, 0.15m tall.

Core parapets (4):
```
Core_upstand_N: [-9.85,  9.85, 10.3] → [9.85,  9.854, 10.45]
Core_upstand_S: [-9.85, -9.854, 10.3] → [9.85, -9.85, 10.45]
Core_upstand_E: [ 9.85, -9.85, 10.3] → [ 9.854, 9.85, 10.45]
Core_upstand_W: [-9.854,-9.85, 10.3] → [-9.85,  9.85, 10.45]
```

Ring parapets (4):
```
Ring_upstand_N: [-11.85, 11.85, 9.0] → [11.85, 11.854, 9.15]
Ring_upstand_S: [-11.85,-11.854, 9.0] → [11.85,-11.85, 9.15]
Ring_upstand_E: [11.85, -8.0, 9.0] → [11.854, 8.0, 9.15]
Ring_upstand_W: [-11.854,-8.0, 9.0] → [-11.85, 8.0, 9.15]
```
8 elements.

### K.4 Drip Edges

At parapet outer tops. Thin metal flashing, 0.003m thick, projecting 0.05m beyond parapet face.

Core parapets (4):
```
Core_drip_N: [-10.05,  10.0, 10.597] → [10.05, 10.05, 10.6]
Core_drip_S: [-10.05,-10.05, 10.597] → [10.05,-10.0,  10.6]
Core_drip_E: [ 10.0, -10.05, 10.597] → [10.05, 10.05, 10.6]
Core_drip_W: [-10.05,-10.05, 10.597] → [-10.0, 10.05, 10.6]
```

Ring parapets (4):
```
Ring_drip_N: [-12.05, 12.0, 9.297] → [12.05, 12.05, 9.3]
Ring_drip_S: [-12.05,-12.05, 9.297] → [12.05,-12.0,  9.3]
Ring_drip_E: [12.0, -8.05, 9.297] → [12.05, 8.05, 9.3]
Ring_drip_W: [-12.05,-8.05, 9.297] → [-12.0, 8.05, 9.3]
```
8 elements.

### K.5 Formwork Lines

Horizontal construction joint markers at pour lift heights (2.4m lifts per Archibase RC wall practice).

Core walls — lifts at Z=2.4 and Z=4.8:
```
Core_formwork_S_Z2.4: line [-8.0, -8.0, 2.4] → [8.0, -8.0, 2.4]
Core_formwork_S_Z4.8: line [-8.0, -8.0, 4.8] → [8.0, -8.0, 4.8]
Core_formwork_N_Z2.4: line [-8.0,  8.0, 2.4] → [8.0,  8.0, 2.4]
Core_formwork_N_Z4.8: line [-8.0,  8.0, 4.8] → [8.0,  8.0, 4.8]
Core_formwork_E_Z2.4: line [ 8.0, -8.0, 2.4] → [8.0,  8.0, 2.4]
Core_formwork_E_Z4.8: line [ 8.0, -8.0, 4.8] → [8.0,  8.0, 4.8]
Core_formwork_W_Z2.4: line [-8.0, -8.0, 2.4] → [-8.0, 8.0, 2.4]
Core_formwork_W_Z4.8: line [-8.0, -8.0, 4.8] → [-8.0, 8.0, 4.8]
```

Ring outer walls — lift at Z=7.4 (2.4m above ring floor):
```
Ring_formwork_N: line [-12.0, 12.0, 7.4] → [12.0, 12.0, 7.4]
Ring_formwork_S: line [-12.0,-12.0, 7.4] → [12.0,-12.0, 7.4]
Ring_formwork_E: line [12.0, -8.0, 7.4] → [12.0, 8.0, 7.4]
Ring_formwork_W: line [-12.0,-8.0, 7.4] → [-12.0, 8.0, 7.4]
```

Stair walls — lift at Z=2.4, Z=4.8:
```
Stair_formwork_N_Z2.4: line [-14.0, 12.0, 2.4] → [-10.0, 12.0, 2.4]
Stair_formwork_N_Z4.8: line [-14.0, 12.0, 4.8] → [-10.0, 12.0, 4.8]
Stair_formwork_S_Z2.4: line [-14.0,  8.0, 2.4] → [-10.0,  8.0, 2.4]
Stair_formwork_S_Z4.8: line [-14.0,  8.0, 4.8] → [-10.0,  8.0, 4.8]
```
16 elements.

### K.6 Expansion Joints

At core center (X=0 and Y=0) — core is 16m wide, joint at midpoint.
3mm wide gaps, modeled as thin boxes.

```
Core_joint_X0_S: [-0.0015, -8.0, 0.0] → [0.0015, -7.7, 8.0]
Core_joint_X0_N: [-0.0015,  7.7, 0.0] → [0.0015,  8.0, 8.0]
Core_joint_Y0_E: [ 7.7, -0.0015, 0.0] → [ 8.0, 0.0015, 8.0]
Core_joint_Y0_W: [-8.0, -0.0015, 0.0] → [-7.7, 0.0015, 8.0]
```
4 elements.

### K.7 Facade Panel Joints

Vertical joints on ring outer walls at 4m intervals. 3mm wide.

North face (6 joints at X = -8, -4, 0, 4, 8):
```
Ring_joint_N_X-8: [-8.0015, 11.75, 5.0] → [-7.9985, 12.0, 9.0]
Ring_joint_N_X-4: [-4.0015, 11.75, 5.0] → [-3.9985, 12.0, 9.0]
Ring_joint_N_X0:  [-0.0015, 11.75, 5.0] → [ 0.0015, 12.0, 9.0]
Ring_joint_N_X4:  [ 3.9985, 11.75, 5.0] → [ 4.0015, 12.0, 9.0]
Ring_joint_N_X8:  [ 7.9985, 11.75, 5.0] → [ 8.0015, 12.0, 9.0]
```

South face (5 joints):
```
Ring_joint_S_X-8: [-8.0015,-12.0, 5.0] → [-7.9985,-11.75, 9.0]
Ring_joint_S_X-4: [-4.0015,-12.0, 5.0] → [-3.9985,-11.75, 9.0]
Ring_joint_S_X0:  [-0.0015,-12.0, 5.0] → [ 0.0015,-11.75, 9.0]
Ring_joint_S_X4:  [ 3.9985,-12.0, 5.0] → [ 4.0015,-11.75, 9.0]
Ring_joint_S_X8:  [ 7.9985,-12.0, 5.0] → [ 8.0015,-11.75, 9.0]
```
10 elements.

**L400_Material subtotal: 66 elements**

---

## SECTION L: L350 DETAIL

Layer: `Type_05_Visibility::L350_Detail`

### L.1 Column Base Plates

Steel base plates under each outrigger column. 0.6 × 0.6 × 0.02m.

8 outrigger bases:
```
Base_plate_N:  [-0.3, 11.7, -0.02] → [ 0.3, 12.3, 0.0]
Base_plate_S:  [-0.3,-12.3, -0.02] → [ 0.3,-11.7, 0.0]
Base_plate_E:  [11.7, -0.3, -0.02] → [12.3,  0.3, 0.0]
Base_plate_W:  [-12.3,-0.3, -0.02] → [-11.7, 0.3, 0.0]
Base_plate_NE: [ 8.19, 8.19,-0.02] → [ 8.79, 8.79, 0.0]
Base_plate_SE: [ 8.19,-8.79,-0.02] → [ 8.79,-8.19, 0.0]
Base_plate_SW: [-8.79,-8.79,-0.02] → [-8.19,-8.19, 0.0]
Base_plate_NW: [-8.79, 8.19,-0.02] → [-8.19, 8.79, 0.0]
```
8 elements.

### L.2 Column Top Plates (at ring floor)

Bearing plates where outrigger columns meet transfer beams. 0.5 × 0.5 × 0.02m.

8 elements (same XY as columns, at Z = 4.7):
```
Top_plate_N:  [-0.25, 11.75, 4.68] → [ 0.25, 12.25, 4.7]
Top_plate_S:  [-0.25,-12.25, 4.68] → [ 0.25,-11.75, 4.7]
Top_plate_E:  [11.75,-0.25,  4.68] → [12.25, 0.25, 4.7]
Top_plate_W:  [-12.25,-0.25, 4.68] → [-11.75, 0.25, 4.7]
Top_plate_NE: [ 8.24, 8.24, 4.68] → [ 8.74, 8.74, 4.7]
Top_plate_SE: [ 8.24,-8.74, 4.68] → [ 8.74,-8.24, 4.7]
Top_plate_SW: [-8.74,-8.74, 4.68] → [-8.24,-8.24, 4.7]
Top_plate_NW: [-8.74, 8.24, 4.68] → [-8.24, 8.74, 4.7]
```
8 elements.

### L.3 Ramp Column Base Plates

0.4 × 0.4 × 0.02m under each ramp column.

```
Ramp_base_S1: [13.775,-14.225,-0.02] → [14.225,-13.775, 0.0]
Ramp_base_S2: [ 0.775,-14.225,-0.02] → [ 1.225,-13.775, 0.0]
Ramp_base_W1: [-14.225,-13.975,-0.02] → [-13.775,-13.525, 0.0]
Ramp_base_W2: [-14.225,  0.775,-0.02] → [-13.775,  1.225, 0.0]
Ramp_base_N1: [-13.975, 13.775,-0.02] → [-13.525, 14.225, 0.0]
Ramp_base_N2: [  0.775, 13.775,-0.02] → [  1.225, 14.225, 0.0]
```
6 elements.

### L.4 Wall Kickers

RC kickers at base of core walls. 0.3m wide × 0.15m tall × full wall length.
Z = [0, 0.15].

```
Kicker_core_S: [-8.0, -8.0, 0.0] → [8.0, -7.7, 0.15]
Kicker_core_N: [-8.0,  7.7, 0.0] → [8.0,  8.0, 0.15]
Kicker_core_E: [ 7.7, -8.0, 0.0] → [8.0,  8.0, 0.15]
Kicker_core_W: [-8.0, -8.0, 0.0] → [-7.7, 8.0, 0.15]
```
4 elements.

### L.5 Ring Outer Wall Kickers

```
Kicker_ring_N: [-12.0, 11.75, 5.0] → [12.0, 12.0, 5.15]
Kicker_ring_S: [-12.0,-12.0,  5.0] → [12.0,-11.75, 5.15]
Kicker_ring_E: [11.75, -8.0,  5.0] → [12.0,  8.0, 5.15]
Kicker_ring_W: [-12.0, -8.0,  5.0] → [-11.75, 8.0, 5.15]
```
4 elements.

### L.6 Opening Lintels (Core Upper Viewing Panels)

RC lintels above each viewing panel opening. 0.3m deep × 0.3m tall.
Z = [7.5, 7.8]. Bearing 0.2m into wall on each side.

```
Lintel_core_N: [-3.2, 7.7, 7.5] → [3.2, 8.0, 7.8]
Lintel_core_E: [7.7, -3.2, 7.5] → [8.0, 3.2, 7.8]
Lintel_core_W: [-8.0,-3.2, 7.5] → [-7.7, 3.2, 7.8]
```
3 elements.

### L.7 Opening Lintels (Ring Outer Slot Windows)

RC lintels above slot window openings. Same depth as wall (0.25m).
Z = [8.5, 8.75]. Bearing 0.2m on each side.

```
Lintel_ring_N: [-10.2, 11.75, 8.5] → [10.2, 12.0, 8.75]
Lintel_ring_S: [-10.2,-12.0,  8.5] → [10.2,-11.75, 8.75]
Lintel_ring_E: [11.75,-6.2,  8.5] → [12.0, 6.2, 8.75]
Lintel_ring_W: [-12.0,-6.2,  8.5] → [-11.75, 6.2, 8.75]
```
4 elements.

### L.8 Worker Door Threshold

Stone threshold at worker entry, 0.05m tall, projecting 0.02m beyond wall face.
```
Worker_threshold: [-2.0, 7.68, 0.0] → [2.0, 8.02, 0.05]
```
1 element.

### L.9 Cargo Door Threshold

```
Cargo_threshold: [-8.02, -2.0, 0.0] → [-7.68, 2.0, 0.05]
```
1 element.

### L.10 Cantilever Brackets (Ring Floor)

At each outrigger column, a bracket supporting the ring floor cantilever.
Triangular in profile — modeled as tapered box. 0.3m wide × 0.5m tall × 0.8m projection.
8 brackets.

```
Bracket_N:  [-0.15,  11.8, 4.2] → [ 0.15, 12.6, 4.7]
Bracket_S:  [-0.15, -12.6, 4.2] → [ 0.15,-11.8, 4.7]
Bracket_E:  [11.8,  -0.15, 4.2] → [12.6,  0.15, 4.7]
Bracket_W:  [-12.6, -0.15, 4.2] → [-11.8, 0.15, 4.7]
Bracket_NE: [ 8.29,  8.29, 4.2] → [ 9.09, 9.09, 4.7]
Bracket_SE: [ 8.29, -9.09, 4.2] → [ 9.09,-8.29, 4.7]
Bracket_SW: [-9.09, -9.09, 4.2] → [-8.29,-8.29, 4.7]
Bracket_NW: [-9.09,  8.29, 4.2] → [-8.29, 9.09, 4.7]
```
8 elements.

**L350_Detail subtotal: 47 elements**

---

## ELEMENT COUNT SUMMARY

| Section | Layer | Count |
|---------|-------|-------|
| B. Core Walls | Volumes | 17 |
| C. Core Floors | Volumes | 2 |
| D. Viewing Ring | Volumes | 28 |
| E. Structure | Structure | 30 |
| F. Ascending Ramp | Circulation | 14 |
| G. Exit Stair | Circulation + Openings | 9+1 |
| H. Openings | Openings | 57 |
| I. Annotations | Annotations | 9 |
| J. Roof System | L300_Roof | 9 |
| K. Material Layers | L400_Material | 66 |
| L. Detail Elements | L350_Detail | 47 |
| **TOTAL** | | **289** |

---

## BILL OF OBJECTS — TEAM ASSIGNMENT

| Agent | Sections | Element Count |
|-------|----------|---------------|
| **Structure** | E (columns, beams), C.1 ground slab | 31 |
| **Shell** | B (core walls), D (ring volumes), G.1 (stair walls) | 51 |
| **Detail** | F (ramp), G.2-3 (stair flights), H (openings), I (annotations) | 91 |
| **Material** | J (roof), K (L400), L (L350 detail) | 122 |
| **TOTAL** | | **289** |

Note: Material agent has highest count but elements are simple boxes (assembly layers). Detail agent has complex geometry (wedges for ramp).

---

## INTERFACE REGISTRY

| Interface | Owner | Reference agent | Rule |
|-----------|-------|----------------|------|
| Core wall base → ground slab | Shell | Structure | Walls sit on slab top face (Z=0) |
| Ring floor → core walls | Shell | Shell | Ring slab inner edge at core wall outer face (±8.0) |
| Ring floor → outrigger columns | Shell | Structure | Slab outer edge at column center line (±12.0) |
| Transfer beams → core walls | Structure | Shell | Beam end at core wall inner face (±7.7) |
| Transfer beams → outrigger cols | Structure | Structure | Beam end at column center |
| Ring outer wall → ring floor | Shell | Shell | Wall base at ring floor top (Z=5.0) |
| Ramp → ring floor | Detail | Shell | Ramp entry bridge meets ring at Z=5.0 |
| Stair enclosure → ring | Shell | Shell | Stair walls rise to ring ceiling (Z=9.0) |
| Roof slab → core walls | Material | Shell | Roof bears on core wall tops (Z=8.0) |
| Roof assembly → parapet | Material | Material | Inset from parapet inner face |
| Ring glazing → core walls | Detail | Shell | Glazing at core wall face ±7.7 |
| Kickers → walls | Material | Shell | Kicker at wall base, same width |
| Lintels → openings | Material | Detail | Lintel Z matches opening top |

---

## CODE COMPLIANCE CHECKLIST

| Requirement | Standard | Compliance |
|-------------|----------|------------|
| Ramp gradient ≤ 6% | SIA 500 | ✅ 6% (83m run for 5m rise) |
| Ramp width ≥ 1.5m | SIA 500 | ✅ 1.5m |
| Handrails both sides, 850-900mm | SIA 500 | ✅ (modeled in L350) |
| Guardrail height ≥ 1100mm | SIA 358 | ✅ 1.1m ramp parapets |
| Stair riser 150-170mm | SIA 500 | ✅ 167mm |
| Stair going 290-310mm | SIA 500 | ✅ 290mm |
| Stair width ≥ 1500mm (public) | VKF | ✅ 1.5m |
| Max travel to exit ≤ 35m | VKF | ✅ Ring ≤ 24m to stair + 15m descent |
| Fire compartment ≤ 2400m² | VKF | ✅ Core = 256m², Ring = 320m² |
| Structure REI 90 | VKF | ✅ RC 300mm (inherent) |
| Parapet ≥ 150mm above roof | SIA 271 | ✅ 300mm parapets |
| Roof slope ≥ 1.5% | SIA 271 | ⚠️ Flat — slope in screed (not modeled) |
| DPC at wall bases | Archibase | ✅ Kickers modeled |

---

## EXECUTION NOTES

1. All ramp elements are WEDGES (box_pts with 8 explicit corners at different Z). Use `rs.AddBox()` with point list, NOT min/max corners.
2. Mullions are very thin (50mm) — use exact coordinates, do not round.
3. Core walls have complex splits around openings — build wall by wall, verify each face.
4. Expansion joints are 3mm wide — model as 0.003m boxes for visibility at model scale.
5. Ring floor is 4 separate slabs (N/S/E/W) — no overlaps at corners.
6. Landings must be FLAT (constant Z) despite connecting to sloped ramp runs.
