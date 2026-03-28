# Lock Type 03 — Altitude North (Funicular Lock)
# LOG400 Complete Geometry Specification
# Status: DRAFT FOR ROUNDTABLE REVIEW — do NOT execute until approved
# Architect: Claude (Roundtable)
# Date: 2026-03-27

---

## COORDINATE SYSTEM — READ FIRST

Rhino document units: Centimeters.
Geometry is authored in METER-SCALE values (X=-8 to 8, Y=-5 to 45, Z=0 to 32).
"8.0" in Rhino = 8.0 as a number, displayed as "8 cm" but conceptually 8m.

**ALL coordinates in this spec are meter-scale. Use them exactly as written.**
**Do NOT multiply by 100. Do NOT convert.**

X = transverse axis (negative = West, positive = East). Centerline at X=0.
Y = slope axis (Y=-5 valley approach, Y=45 hilltop exit)
Z = vertical (Z=0 valley floor)

**Building concept:** A funicular station — two horizontal stations connected by an inclined inhabited track. The building IS the slope. Valley station sits at valley floor (Z=0–6). Hilltop station sits at hilltop (Z=22–28). An inclined tube connects them along the slope, rising 16m over 30m of plan length.

**Slope vector:** (0, 30, 16) — the inclined track runs from Y=5,Z=6 to Y=35,Z=22.

---

## SECTION A: LAYERS

Create ALL of the following layers before placing any geometry.

```
Type_03_Altitude::Walls          — RGB(180, 170, 155) — all wall shells (RC structure)
Type_03_Altitude::Floors         — RGB(160, 155, 140) — floor slabs
Type_03_Altitude::L300_Roof      — RGB(200, 180, 160) — roof slabs, parapets
Type_03_Altitude::Structure      — RGB(140, 130, 120) — columns, beams, bracing
Type_03_Altitude::Circulation    — RGB(100, 140, 160) — stairs, ramps, paths, landings
Type_03_Altitude::L350_Detail    — RGB(160, 140, 120) — kickers, plates, frames, lintels
Type_03_Altitude::L400_Material  — RGB(120, 100,  80) — assembly layers, formwork, hardware
Type_03_Altitude::Openings       — RGB(255, 200, 200) — opening voids (reference only)
Type_03_Altitude::Annotations    — RGB(255, 255, 255) — text dots
Type_03_Altitude::TerrainProxy   — RGB( 80, 120,  60) — tilted reference surface
```

**Total: 10 layers**

---

## SECTION B: VALLEY STATION WALLS

Layer: `Type_03_Altitude::Walls`
Wall thickness: 0.3 (300mm simplified from 400mm archibase spec for visual clarity at this scale).
Valley station envelope: X=[-8, 8], Y=[-5, 5], Z=[0, 6].

### B.1 South Wall (Y = -5 to -4.7)

Opening: Entry door — X=[-4, 4], Z=[0.5, 4.5] (8m wide, 4m tall, with 0.5m sill).

Split into 4 pieces around opening:

```
VS_wall_S_left:    [-8.0, -5.0, 0.0] → [-4.0, -4.7, 6.0]
VS_wall_S_right:   [ 4.0, -5.0, 0.0] → [ 8.0, -4.7, 6.0]
VS_wall_S_lintel:  [-4.0, -5.0, 4.5] → [ 4.0, -4.7, 6.0]
VS_wall_S_sill:    [-4.0, -5.0, 0.0] → [ 4.0, -4.7, 0.5]
```

### B.2 North Wall (Y = 4.7 to 5.0)

Opening: Track connection — X=[-3, 3], Z=[3, 6] (6m wide, 3m tall at roof level where the inclined track departs).

Split into 4 pieces:

```
VS_wall_N_left:    [-8.0, 4.7, 0.0] → [-3.0, 5.0, 6.0]
VS_wall_N_right:   [ 3.0, 4.7, 0.0] → [ 8.0, 5.0, 6.0]
VS_wall_N_lintel:  [-3.0, 4.7, 6.0] → [ 3.0, 5.0, 6.0]
VS_wall_N_sill:    [-3.0, 4.7, 0.0] → [ 3.0, 5.0, 3.0]
```

Note: VS_wall_N_lintel is a zero-height element (Z=6.0 to 6.0). The track opening extends to the full wall height. Omit the lintel — the roof slab acts as the lintel. Corrected: **3 pieces only for north wall.**

```
VS_wall_N_left:    [-8.0, 4.7, 0.0] → [-3.0, 5.0, 6.0]
VS_wall_N_right:   [ 3.0, 4.7, 0.0] → [ 8.0, 5.0, 6.0]
VS_wall_N_sill:    [-3.0, 4.7, 0.0] → [ 3.0, 5.0, 3.0]
```

### B.3 West Wall (solid, no opening)

```
VS_wall_W:         [-8.0, -5.0, 0.0] → [-7.7, 5.0, 6.0]
```

### B.4 East Wall (solid, no opening)

```
VS_wall_E:         [ 7.7, -5.0, 0.0] → [ 8.0, 5.0, 6.0]
```

**Valley Station wall count: 4 + 3 + 1 + 1 = 9 elements**

---

## SECTION C: VALLEY STATION FLOOR + ROOF

Layer (floor): `Type_03_Altitude::Floors`
Layer (roof + parapets): `Type_03_Altitude::L300_Roof`

### C.1 Floor Slab

250mm RC slab. Top face at Z=0 (finished floor level). Slab below grade.

```
VS_floor_slab:     [-8.0, -5.0, -0.25] → [8.0, 5.0, 0.0]
```

### C.2 Roof Slab

300mm RC slab (span/30 for ~10m effective span with interior columns reducing it to ~5m; use 300mm for robustness). Top face at Z=6.3. Bears on wall tops at Z=6.0.

```
VS_roof_slab:      [-8.0, -5.0, 6.0] → [8.0, 5.0, 6.3]
```

### C.3 Parapets

3 sides only — no parapet on north side (track connects there).
Parapet: 200mm thick RC, 500mm above roof slab top (Z=6.3).
Parapet top: Z = 6.3 + 0.5 = 6.8.
Parapet Z range: [6.3, 6.8].

```
VS_parapet_S:      [-8.0, -5.0, 6.3] → [ 8.0, -4.8, 6.8]
VS_parapet_W:      [-8.0, -5.0, 6.3] → [-7.8,  5.0, 6.8]
VS_parapet_E:      [ 7.8, -5.0, 6.3] → [ 8.0,  5.0, 6.8]
```

**Section C count: 1 floor + 1 roof + 3 parapets = 5 elements**

---

## SECTION D: HILLTOP STATION WALLS

Layer: `Type_03_Altitude::Walls`
Wall thickness: 0.3 (300mm).
Hilltop station envelope: X=[-8, 8], Y=[35, 45], Z=[22, 28].

### D.1 North Wall (Y = 44.7 to 45.0)

Opening: Exit door — X=[-4, 4], Z=[22.5, 26.5] (8m wide, 4m tall, with 0.5m sill above floor at Z=22).

Split into 4 pieces:

```
HS_wall_N_left:    [-8.0, 44.7, 22.0] → [-4.0, 45.0, 28.0]
HS_wall_N_right:   [ 4.0, 44.7, 22.0] → [ 8.0, 45.0, 28.0]
HS_wall_N_lintel:  [-4.0, 44.7, 26.5] → [ 4.0, 45.0, 28.0]
HS_wall_N_sill:    [-4.0, 44.7, 22.0] → [ 4.0, 45.0, 22.5]
```

### D.2 South Wall (Y = 35.0 to 35.3)

Opening: Track arrival — X=[-3, 3], Z=[22, 26] (6m wide, 4m tall, from floor to Z=26 where track roof meets).

Split into 3 pieces (track opening starts at floor level, so no sill):

```
HS_wall_S_left:    [-8.0, 35.0, 22.0] → [-3.0, 35.3, 28.0]
HS_wall_S_right:   [ 3.0, 35.0, 22.0] → [ 8.0, 35.3, 28.0]
HS_wall_S_lintel:  [-3.0, 35.0, 26.0] → [ 3.0, 35.3, 28.0]
```

### D.3 West Wall (solid)

```
HS_wall_W:         [-8.0, 35.0, 22.0] → [-7.7, 45.0, 28.0]
```

### D.4 East Wall (solid)

```
HS_wall_E:         [ 7.7, 35.0, 22.0] → [ 8.0, 45.0, 28.0]
```

**Hilltop Station wall count: 4 + 3 + 1 + 1 = 9 elements**

---

## SECTION E: HILLTOP STATION FLOOR + ROOF

Layer (floor): `Type_03_Altitude::Floors`
Layer (roof + parapets): `Type_03_Altitude::L300_Roof`

### E.1 Floor Slab

250mm RC slab. Top face at Z=22 (hilltop finished floor). Slab sits on structure below.

```
HS_floor_slab:     [-8.0, 35.0, 21.75] → [8.0, 45.0, 22.0]
```

### E.2 Roof Slab

300mm RC slab. Bears on wall tops at Z=28.

```
HS_roof_slab:      [-8.0, 35.0, 28.0] → [8.0, 45.0, 28.3]
```

### E.3 Parapets

3 sides only — no parapet on south side (track connects there).
Parapet top: Z = 28.3 + 0.5 = 28.8.

```
HS_parapet_N:      [-8.0, 44.8, 28.3] → [ 8.0, 45.0, 28.8]
HS_parapet_W:      [-8.0, 35.0, 28.3] → [-7.8, 45.0, 28.8]
HS_parapet_E:      [ 7.8, 35.0, 28.3] → [ 8.0, 45.0, 28.8]
```

**Section E count: 1 floor + 1 roof + 3 parapets = 5 elements**

---

## SECTION F: INCLINED TRACK — THE KEY ELEMENT

Layer (walls): `Type_03_Altitude::Walls`
Layer (floor/roof): `Type_03_Altitude::Floors` / `Type_03_Altitude::L300_Roof`

The track is a HOLLOW TUBE following the slope from valley station to hilltop station.
- Start: Y=5, Z_floor=6.0 (valley station roof level)
- End: Y=35, Z_floor=22.0 (hilltop station floor level)
- Slope vector: (0, 30, 16) over 30m plan distance
- Internal height: 4.0m (floor to ceiling)
- Internal width: 5.4m (X=-2.7 to X=2.7, between inner faces of 300mm side walls)

**These elements are SLOPED. They CANNOT be modeled as axis-aligned boxes.**
Use extrusion of a cross-section profile along the slope vector (0, 30, 16).

### F.1 Slope Geometry Reference

Slope angle: atan(16/30) = 28.07 degrees
Slope length: sqrt(30^2 + 16^2) = 34.0m
Unit slope direction: (0, 30/34, 16/34) = (0, 0.8824, 0.4706)

All cross-sections defined at Y=5 (valley end), then extruded along direction (0, 30, 16).

### F.2 West Side Wall

300mm thick, 4m internal height, following slope.
Cross-section at Y=5 (rectangle in X-Z plane):

```
Profile corners (at Y=5):
  Bottom-outer: (-3.0,  5.0,  5.75)
  Bottom-inner: (-2.7,  5.0,  5.75)
  Top-inner:    (-2.7,  5.0, 10.2)
  Top-outer:    (-3.0,  5.0, 10.2)
```

Extrude this rectangle along vector (0, 30, 16).

End corners (at Y=35):
```
  Bottom-outer: (-3.0,  35.0, 21.75)
  Bottom-inner: (-2.7,  35.0, 21.75)
  Top-inner:    (-2.7,  35.0, 26.2)
  Top-outer:    (-3.0,  35.0, 26.2)
```

Name: `Track_wall_W`
Layer: `Type_03_Altitude::Walls`

**Modeling method:** Create a closed polyline (the 4 profile corners at Y=5), then extrude it as a solid along vector (0, 30, 16). This produces a sloped prism.

### F.3 East Side Wall

Mirror of west wall at X=+2.7 to +3.0.

```
Profile corners (at Y=5):
  Bottom-inner: (2.7,  5.0,  5.75)
  Bottom-outer: (3.0,  5.0,  5.75)
  Top-outer:    (3.0,  5.0, 10.2)
  Top-inner:    (2.7,  5.0, 10.2)
```

Extrude along (0, 30, 16).

Name: `Track_wall_E`
Layer: `Type_03_Altitude::Walls`

### F.4 Floor Slab

250mm thick, 6m wide (full track width), following slope.

```
Profile corners (at Y=5):
  Bottom-left:  (-3.0,  5.0,  5.75)
  Bottom-right: ( 3.0,  5.0,  5.75)
  Top-right:    ( 3.0,  5.0,  6.0)
  Top-left:     (-3.0,  5.0,  6.0)
```

Extrude along (0, 30, 16).

End corners (at Y=35):
```
  Bottom-left:  (-3.0, 35.0, 21.75)
  Bottom-right: ( 3.0, 35.0, 21.75)
  Top-right:    ( 3.0, 35.0, 22.0)
  Top-left:     (-3.0, 35.0, 22.0)
```

Name: `Track_floor_slab`
Layer: `Type_03_Altitude::Floors`

### F.5 Roof Slab

200mm thick (6m span, span/30 = 200mm), following slope.
Roof sits on top of walls at Z=10.0 (at Y=5 end).

```
Profile corners (at Y=5):
  Bottom-left:  (-3.0,  5.0, 10.0)
  Bottom-right: ( 3.0,  5.0, 10.0)
  Top-right:    ( 3.0,  5.0, 10.2)
  Top-left:     (-3.0,  5.0, 10.2)
```

Extrude along (0, 30, 16).

End corners (at Y=35):
```
  Bottom-left:  (-3.0, 35.0, 26.0)
  Bottom-right: ( 3.0, 35.0, 26.0)
  Top-right:    ( 3.0, 35.0, 26.2)
  Top-left:     (-3.0, 35.0, 26.2)
```

Name: `Track_roof_slab`
Layer: `Type_03_Altitude::L300_Roof`

### F.6 Verification — Internal Dimensions

At any cross-section along the track:
- Floor top to roof bottom: 10.0 - 6.0 = 4.0m internal height (correct)
- Inner wall to inner wall: 2.7 - (-2.7) = 5.4m internal width (correct)
- Wall bottom to floor top: 5.75 to 6.0 = wall extends 0.25m below floor slab top (slab sits within wall height — correct)
- Wall top to roof top: 10.2 = matches roof slab top (walls carry roof — correct)

**Section F count: 2 side walls + 1 floor + 1 roof = 4 sloped extrusions**

---

## SECTION G: TOWER

Layer (walls): `Type_03_Altitude::Walls`
Layer (columns/bracing): `Type_03_Altitude::Structure`
Layer (detail): `Type_03_Altitude::L350_Detail`

Tower envelope: X=[-3, 3], Y=[35, 41], Z=[22, 32].
The tower rises from the hilltop station roof (Z=28.3) to Z=32.
Tower columns start at Z=22 (hilltop floor) and pass through the hilltop station for full structural continuity.

### G.1 Tower Columns (4 corners)

Column size: 300mm x 300mm (0.3 x 0.3).
Height: Z=22 to Z=32 (10m, through hilltop station and up).

```
Tower_col_SW:      [-3.0, 35.0, 22.0] → [-2.7, 35.3, 32.0]
Tower_col_SE:      [ 2.7, 35.0, 22.0] → [ 3.0, 35.3, 32.0]
Tower_col_NW:      [-3.0, 40.7, 22.0] → [-2.7, 41.0, 32.0]
Tower_col_NE:      [ 2.7, 40.7, 22.0] → [ 3.0, 41.0, 32.0]
```

Layer: `Type_03_Altitude::Structure`

### G.2 Tower Walls (thin, open on 2 faces)

200mm thick walls. Open on East and West for panoramic views.
Only North and South walls (solid screen walls for wind protection).

```
Tower_wall_S:      [-3.0, 35.0, 28.3] → [ 3.0, 35.2, 32.0]
Tower_wall_N:      [-3.0, 40.8, 28.3] → [ 3.0, 41.0, 32.0]
```

Note: Tower walls start at Z=28.3 (above hilltop roof slab top). Below that, the hilltop station walls enclose the space.

Layer: `Type_03_Altitude::Walls`

### G.3 Horizontal Bracing

Steel HEB braces at two levels to stiffen the open frame.
Modeled as 200mm deep x 150mm wide beams spanning column-to-column.

**Level 1 bracing at Z=29.5** (cross beams, E-W spanning):

```
Tower_brace_S_Z29:  [-2.7, 35.15, 29.5] → [2.7, 35.3, 29.7]
Tower_brace_N_Z29:  [-2.7, 40.7,  29.5] → [2.7, 40.85, 29.7]
```

**Level 2 bracing at Z=31.0** (cross beams, E-W spanning):

```
Tower_brace_S_Z31:  [-2.7, 35.15, 31.0] → [2.7, 35.3, 31.2]
Tower_brace_N_Z31:  [-2.7, 40.7,  31.0] → [2.7, 40.85, 31.2]
```

**N-S bracing (longitudinal ties at each level):**

```
Tower_brace_W_Z29:  [-3.0, 35.3, 29.5] → [-2.7, 40.7, 29.7]
Tower_brace_E_Z29:  [ 2.7, 35.3, 29.5] → [ 3.0, 40.7, 29.7]
Tower_brace_W_Z31:  [-3.0, 35.3, 31.0] → [-2.7, 40.7, 31.2]
Tower_brace_E_Z31:  [ 2.7, 35.3, 31.0] → [ 3.0, 40.7, 31.2]
```

Layer: `Type_03_Altitude::Structure`

### G.4 Tower Crown — X-Braces (open lattice, NO roof slab)

Diagonal X-braces on East and West open faces, from Z=28.3 to Z=32.
Modeled as thin flat plates (50mm thick) for visual reading.

**West face X-brace** (two diagonals crossing):
These are sloped elements. Use line extrusion or thin solids.

Diagonal 1 (SW-bottom to NW-top):
```
Tower_Xbrace_W_d1:
  Start: (-3.0, 35.3, 28.3)
  End:   (-3.0, 40.7, 32.0)
  Cross-section: 150mm wide (Y) x 50mm deep (X) = 0.15 x 0.05
```

Diagonal 2 (NW-bottom to SW-top):
```
Tower_Xbrace_W_d2:
  Start: (-3.0, 40.7, 28.3)
  End:   (-3.0, 35.3, 32.0)
  Cross-section: 150mm wide (Y) x 50mm deep (X) = 0.15 x 0.05
```

**East face X-brace** (mirror):
```
Tower_Xbrace_E_d1:
  Start: (3.0, 35.3, 28.3)
  End:   (3.0, 40.7, 32.0)
  Cross-section: 150mm wide (Y) x 50mm deep (X) = 0.15 x 0.05

Tower_Xbrace_E_d2:
  Start: (3.0, 40.7, 28.3)
  End:   (3.0, 35.3, 32.0)
  Cross-section: 150mm wide (Y) x 50mm deep (X) = 0.15 x 0.05
```

**Modeling method:** Create a line between start and end points. Use Pipe or extrude a small rectangular profile along the line. Alternatively, create as thin boxes rotated into position — but extrusion along a line is cleaner.

Layer: `Type_03_Altitude::Structure`

### G.5 Column Cap Plates

Steel plates at column tops. 400mm x 400mm x 25mm (0.4 x 0.4 x 0.025).
Centered on each column top at Z=32.

```
Tower_cap_SW:      [-3.05, 34.95, 32.0] → [-2.65, 35.35, 32.025]
Tower_cap_SE:      [ 2.65, 34.95, 32.0] → [ 3.05, 35.35, 32.025]
Tower_cap_NW:      [-3.05, 40.65, 32.0] → [-2.65, 41.05, 32.025]
Tower_cap_NE:      [ 2.65, 40.65, 32.0] → [ 3.05, 41.05, 32.025]
```

Layer: `Type_03_Altitude::L350_Detail`

**Section G count: 4 columns + 2 walls + 8 braces + 4 X-braces + 4 cap plates = 22 elements**

---

## SECTION H: STRUCTURE (Interior Columns + Track Frames)

Layer: `Type_03_Altitude::Structure`

### H.1 Valley Station Interior Columns

4 columns to reduce roof span from 16m to ~5m segments.
Column size: 300mm x 300mm.
Height: Z=0 to Z=6 (floor to roof slab underside).

Column grid at X=[-4, 4] and Y=[-2, 2] (symmetric about center):

```
VS_col_SW:         [-4.15, -2.15, 0.0] → [-3.85, -1.85, 6.0]
VS_col_SE:         [ 3.85, -2.15, 0.0] → [ 4.15, -1.85, 6.0]
VS_col_NW:         [-4.15,  1.85, 0.0] → [-3.85,  2.15, 6.0]
VS_col_NE:         [ 3.85,  1.85, 0.0] → [ 4.15,  2.15, 6.0]
```

### H.2 Hilltop Station Interior Columns

Same arrangement, at hilltop level.
Height: Z=22 to Z=28.

```
HS_col_SW:         [-4.15, 37.85, 22.0] → [-3.85, 38.15, 28.0]
HS_col_SE:         [ 3.85, 37.85, 22.0] → [ 4.15, 38.15, 28.0]
HS_col_NW:         [-4.15, 41.85, 22.0] → [-3.85, 42.15, 28.0]
HS_col_NE:         [ 3.85, 41.85, 22.0] → [ 4.15, 42.15, 28.0]
```

### H.3 Track Transverse Beam Frames

Beams every 5m along the track (at Y = 10, 15, 20, 25, 30).
These are SLOPED beams connecting the two side walls, at roof level.
Beam size: 300mm wide (along slope) x 400mm deep (Z, hanging below roof slab).

At each beam location, compute Z from the slope:
- Z_floor(Y) = 6.0 + (Y - 5) * (16/30)
- Z_roof_bottom(Y) = Z_floor(Y) + 4.0 = 10.0 + (Y - 5) * (16/30)
- Beam hangs from Z_roof_bottom down 0.4m

| Y | Z_roof_bottom | Z_beam_bottom | Z_beam_top |
|---|---------------|---------------|------------|
| 10 | 10.0 + 5*(16/30) = 12.667 | 12.267 | 12.667 |
| 15 | 10.0 + 10*(16/30) = 15.333 | 14.933 | 15.333 |
| 20 | 10.0 + 15*(16/30) = 18.000 | 17.600 | 18.000 |
| 25 | 10.0 + 20*(16/30) = 20.667 | 20.267 | 20.667 |
| 30 | 10.0 + 25*(16/30) = 23.333 | 22.933 | 23.333 |

Beam extent: X=[-2.7, 2.7] (inner wall to inner wall), 300mm along Y.

```
Track_beam_Y10:    [-2.7,  9.85, 12.267] → [2.7, 10.15, 12.667]
Track_beam_Y15:    [-2.7, 14.85, 14.933] → [2.7, 15.15, 15.333]
Track_beam_Y20:    [-2.7, 19.85, 17.600] → [2.7, 20.15, 18.000]
Track_beam_Y25:    [-2.7, 24.85, 20.267] → [2.7, 25.15, 20.667]
Track_beam_Y30:    [-2.7, 29.85, 22.933] → [2.7, 30.15, 23.333]
```

Note: These beams are AXIS-ALIGNED BOXES approximating the sloped beam. At LOG400 this is acceptable — each beam is only 300mm along Y so the slope deviation over 300mm is negligible (300mm * sin(28°) = ~1.4mm). If the executor wants higher fidelity, rotate each beam to match the slope.

**Section H count: 4 + 4 + 5 = 13 elements**

---

## SECTION I: LOG400 DETAIL

### I.1 Wall Kickers (L350_Detail)

50mm x 50mm RC kicker at wall base, on outer face.

**Valley Station kickers** (Z = [0, 0.05]):

```
L350_kicker_VS_S:    [-8.0, -5.05, 0.0] → [ 8.0, -5.0,  0.05]
L350_kicker_VS_W:    [-8.05, -5.0, 0.0] → [-8.0,  5.0,  0.05]
L350_kicker_VS_E:    [ 8.0, -5.0, 0.0] → [ 8.05,  5.0,  0.05]
```
(No north kicker — track connects. No south kicker on opening face inner — kicker is on outer face, which has the opening. Kicker runs full length of outer face; opening is above the kicker.)

Actually — kicker runs at Z=[0, 0.05] which is BELOW the entry opening sill at Z=0.5. So the south wall kicker can run the full length:

```
L350_kicker_VS_S:    [-8.0, -5.05, 0.0] → [ 8.0, -5.0,  0.05]
L350_kicker_VS_N:    [-8.0,  5.0,  0.0] → [ 8.0,  5.05, 0.05]
L350_kicker_VS_W:    [-8.05, -5.0, 0.0] → [-8.0,  5.0,  0.05]
L350_kicker_VS_E:    [ 8.0, -5.0, 0.0] → [ 8.05,  5.0,  0.05]
```

**Hilltop Station kickers** (Z = [22, 22.05]):

```
L350_kicker_HS_N:    [-8.0, 45.0,  22.0] → [ 8.0, 45.05, 22.05]
L350_kicker_HS_S:    [-8.0, 34.95, 22.0] → [ 8.0, 35.0,  22.05]
L350_kicker_HS_W:    [-8.05, 35.0, 22.0] → [-8.0, 45.0,  22.05]
L350_kicker_HS_E:    [ 8.0, 35.0, 22.0] → [ 8.05, 45.0,  22.05]
```

**Total kickers: 4 + 4 = 8 elements**

### I.2 Column Base Plates (L350_Detail)

Steel plate: 500mm x 500mm x 25mm (0.5 x 0.5 x 0.025).
Flush with floor (plate top = floor level).

**Valley Station columns** (Z = [-0.025, 0]):

```
L350_bp_VS_SW:     [-4.25, -2.25, -0.025] → [-3.75, -1.75, 0.0]
L350_bp_VS_SE:     [ 3.75, -2.25, -0.025] → [ 4.25, -1.75, 0.0]
L350_bp_VS_NW:     [-4.25,  1.75, -0.025] → [-3.75,  2.25, 0.0]
L350_bp_VS_NE:     [ 3.75,  1.75, -0.025] → [ 4.25,  2.25, 0.0]
```

**Hilltop Station columns** (Z = [21.975, 22.0]):

```
L350_bp_HS_SW:     [-4.25, 37.75, 21.975] → [-3.75, 38.25, 22.0]
L350_bp_HS_SE:     [ 3.75, 37.75, 21.975] → [ 4.25, 38.25, 22.0]
L350_bp_HS_NW:     [-4.25, 41.75, 21.975] → [-3.75, 42.25, 22.0]
L350_bp_HS_NE:     [ 3.75, 41.75, 21.975] → [ 4.25, 42.25, 22.0]
```

**Tower columns** (Z = [21.975, 22.0] — same floor):

```
L350_bp_Twr_SW:    [-3.15, 34.85, 21.975] → [-2.55, 35.45, 22.0]
L350_bp_Twr_SE:    [ 2.55, 34.85, 21.975] → [ 3.15, 35.45, 22.0]
L350_bp_Twr_NW:    [-3.15, 40.55, 21.975] → [-2.55, 41.15, 22.0]
L350_bp_Twr_NE:    [ 2.55, 40.55, 21.975] → [ 3.15, 41.15, 22.0]
```

**Total base plates: 4 + 4 + 4 = 12 elements**

### I.3 Column Top Plates (L350_Detail)

Steel plate: 500mm x 500mm x 20mm (0.5 x 0.5 x 0.02).

**Valley Station columns** (top at Z=6.0):

```
L350_tp_VS_SW:     [-4.25, -2.25, 6.0] → [-3.75, -1.75, 6.02]
L350_tp_VS_SE:     [ 3.75, -2.25, 6.0] → [ 4.25, -1.75, 6.02]
L350_tp_VS_NW:     [-4.25,  1.75, 6.0] → [-3.75,  2.25, 6.02]
L350_tp_VS_NE:     [ 3.75,  1.75, 6.0] → [ 4.25,  2.25, 6.02]
```

**Hilltop Station columns** (top at Z=28.0):

```
L350_tp_HS_SW:     [-4.25, 37.75, 28.0] → [-3.75, 38.25, 28.02]
L350_tp_HS_SE:     [ 3.75, 37.75, 28.0] → [ 4.25, 38.25, 28.02]
L350_tp_HS_NW:     [-4.25, 41.75, 28.0] → [-3.75, 42.25, 28.02]
L350_tp_HS_NE:     [ 3.75, 41.75, 28.0] → [ 4.25, 42.25, 28.02]
```

**Total top plates: 4 + 4 = 8 elements**
(Tower cap plates already in Section G.5)

### I.4 Roof Assembly Layers (L400_Material)

Sits inside parapets, on top of roof slab.
Build-up: 200mm XPS insulation + 5mm membrane + 50mm gravel = 255mm total.

**Valley Station** (slab top at Z=6.3, inset from parapet inner faces):
- Parapet inner faces: S at Y=-4.8, W at X=-7.8, E at X=7.8
- North edge: open (no parapet), terminate at Y=5.0

```
L400_VS_insulation:  [-7.8, -4.8, 6.30] → [7.8, 5.0, 6.50]    (200mm)
L400_VS_membrane:    [-7.8, -4.8, 6.50] → [7.8, 5.0, 6.505]   (5mm)
L400_VS_gravel:      [-7.8, -4.8, 6.505] → [7.8, 5.0, 6.555]  (50mm)
```

**Hilltop Station** (slab top at Z=28.3):
- Parapet inner faces: N at Y=44.8, W at X=-7.8, E at X=7.8
- South edge: open (no parapet), terminate at Y=35.0

```
L400_HS_insulation:  [-7.8, 35.0, 28.30] → [7.8, 44.8, 28.50]   (200mm)
L400_HS_membrane:    [-7.8, 35.0, 28.50] → [7.8, 44.8, 28.505]  (5mm)
L400_HS_gravel:      [-7.8, 35.0, 28.505] → [7.8, 44.8, 28.555] (50mm)
```

**Total roof assembly: 3 + 3 = 6 elements**

### I.5 Parapet Upstands (L400_Material)

Waterproofing upstand: 20mm wide x 200mm tall against inner face of each parapet.

**Valley Station** (base at Z=6.3, upstand top at Z=6.5):

```
L400_VS_upstand_S:   [-7.8, -4.82, 6.3] → [7.8, -4.80, 6.5]
L400_VS_upstand_W:   [-7.82, -4.8, 6.3] → [-7.80, 5.0, 6.5]
L400_VS_upstand_E:   [7.80, -4.8, 6.3] → [7.82, 5.0, 6.5]
```

**Hilltop Station** (base at Z=28.3, upstand top at Z=28.5):

```
L400_HS_upstand_N:   [-7.8, 44.78, 28.3] → [7.8, 44.80, 28.5]
L400_HS_upstand_W:   [-7.82, 35.0, 28.3] → [-7.80, 44.8, 28.5]
L400_HS_upstand_E:   [7.80, 35.0, 28.3] → [7.82, 44.8, 28.5]
```

**Total upstands: 3 + 3 = 6 elements**

### I.6 Parapet Drip Edges (L400_Material)

30mm x 20mm at outer top corner of each parapet.

**Valley Station** (parapet top at Z=6.8):

```
L400_VS_drip_S:      [-8.0, -5.03, 6.78] → [8.0, -5.0, 6.8]
L400_VS_drip_W:      [-8.03, -5.0, 6.78] → [-8.0, 5.0, 6.8]
L400_VS_drip_E:      [8.0, -5.0, 6.78] → [8.03, 5.0, 6.8]
```

**Hilltop Station** (parapet top at Z=28.8):

```
L400_HS_drip_N:      [-8.0, 45.0, 28.78] → [8.0, 45.03, 28.8]
L400_HS_drip_W:      [-8.03, 35.0, 28.78] → [-8.0, 45.0, 28.8]
L400_HS_drip_E:      [8.0, 35.0, 28.78] → [8.03, 45.0, 28.8]
```

**Total drip edges: 3 + 3 = 6 elements**

### I.7 Opening Frames (L350_Detail)

Steel hollow section 100mm x 100mm (0.1 x 0.1) framing each opening.

**Valley Station South Entry** (X=[-4, 4], Z=[0.5, 4.5], wall at Y=-5.0):

```
L350_frame_VS_S_top:    [-4.0, -5.05, 4.5] → [4.0, -4.95, 4.6]
L350_frame_VS_S_bot:    [-4.0, -5.05, 0.4] → [4.0, -4.95, 0.5]
L350_frame_VS_S_jambW:  [-4.1, -5.05, 0.4] → [-4.0, -4.95, 4.6]
L350_frame_VS_S_jambE:  [4.0, -5.05, 0.4] → [4.1, -4.95, 4.6]
```

**Hilltop Station North Exit** (X=[-4, 4], Z=[22.5, 26.5], wall at Y=45.0):

```
L350_frame_HS_N_top:    [-4.0, 44.95, 26.5] → [4.0, 45.05, 26.6]
L350_frame_HS_N_bot:    [-4.0, 44.95, 22.4] → [4.0, 45.05, 22.5]
L350_frame_HS_N_jambW:  [-4.1, 44.95, 22.4] → [-4.0, 45.05, 26.6]
L350_frame_HS_N_jambE:  [4.0, 44.95, 22.4] → [4.1, 45.05, 26.6]
```

**Total opening frames: 4 + 4 = 8 elements**

### I.8 RC Lintels (L350_Detail)

300mm deep RC lintels above openings. Full wall thickness. Extends 300mm past opening on each side.

**Valley Station South Entry lintel** (above Z=4.5, 300mm deep):
Already modeled as VS_wall_S_lintel in Section B.1 — that piece IS the lintel zone. Add a separate highlighted lintel box inside the wall for LOG400 emphasis:

```
L350_lintel_VS_S:   [-4.3, -5.0, 4.5] → [4.3, -4.7, 4.8]
```
(300mm deep x full wall thickness, extends 300mm past opening each side)

**Hilltop Station North Exit lintel:**

```
L350_lintel_HS_N:   [-4.3, 44.7, 26.5] → [4.3, 45.0, 26.8]
```

**Valley Station North track lintel** (above Z=6 — integrated into roof slab, annotate only):
No separate lintel needed — roof slab spans over this opening.

**Hilltop Station South track lintel:**

```
L350_lintel_HS_S:   [-3.3, 35.0, 26.0] → [3.3, 35.3, 26.3]
```

**Total lintels: 3 elements**

### I.9 Formwork Lift Lines (L400_Material)

RC walls cast in 2400mm (2.4 unit) lifts.
Formwork line: thin horizontal box, 20mm proud of wall outer face, 20mm tall.

**Valley Station** (walls 6m tall: lifts at Z=2.4):

South wall outer face at Y=-5.0:
```
L400_fw_VS_S_L1:     [-8.0, -5.02, 2.39] → [8.0, -5.0, 2.41]
```

North wall outer face at Y=5.0:
```
L400_fw_VS_N_L1:     [-8.0, 5.0, 2.39] → [8.0, 5.02, 2.41]
```

West wall outer face at X=-8.0:
```
L400_fw_VS_W_L1:     [-8.02, -5.0, 2.39] → [-8.0, 5.0, 2.41]
```

East wall outer face at X=8.0:
```
L400_fw_VS_E_L1:     [8.0, -5.0, 2.39] → [8.02, 5.0, 2.41]
```

Second lift at Z=4.8:
```
L400_fw_VS_S_L2:     [-8.0, -5.02, 4.79] → [8.0, -5.0, 4.81]
L400_fw_VS_N_L2:     [-8.0, 5.0, 4.79] → [8.0, 5.02, 4.81]
L400_fw_VS_W_L2:     [-8.02, -5.0, 4.79] → [-8.0, 5.0, 4.81]
L400_fw_VS_E_L2:     [8.0, -5.0, 4.79] → [8.02, 5.0, 4.81]
```

**Hilltop Station** (walls 6m tall: lifts at Z=24.4, Z=26.8):

South wall outer face at Y=35.0:
```
L400_fw_HS_S_L1:     [-8.0, 34.98, 24.39] → [8.0, 35.0, 24.41]
L400_fw_HS_N_L1:     [-8.0, 45.0, 24.39] → [8.0, 45.02, 24.41]
L400_fw_HS_W_L1:     [-8.02, 35.0, 24.39] → [-8.0, 45.0, 24.41]
L400_fw_HS_E_L1:     [8.0, 35.0, 24.39] → [8.02, 45.0, 24.41]
```

Second lift at Z=26.8:
```
L400_fw_HS_S_L2:     [-8.0, 34.98, 26.79] → [8.0, 35.0, 26.81]
L400_fw_HS_N_L2:     [-8.0, 45.0, 26.79] → [8.0, 45.02, 26.81]
L400_fw_HS_W_L2:     [-8.02, 35.0, 26.79] → [-8.0, 45.0, 26.81]
L400_fw_HS_E_L2:     [8.0, 35.0, 26.79] → [8.02, 45.0, 26.81]
```

**Total formwork lines: 8 + 8 = 16 elements**

---

## SECTION J: CIRCULATION + ANNOTATIONS

### J.1 Valley Station Internal Ramp (L=Circulation)

Simplified as a ramp solid from Z=0 (ground floor) to Z=6 (track departure level).
Located along the west side of the station interior.

```
Circ_VS_ramp:
  Profile at Y=-4 (bottom end):
    (-7.5, -4.0, 0.0) → (-5.5, -4.0, 0.3)   [2m wide, 0.3m thick slab]

  Profile at Y=4 (top end):
    (-7.5, 4.0, 5.7) → (-5.5, 4.0, 6.0)      [arrives at track floor level]
```

**Modeling method:** This is a SLOPED element. Create a rectangular profile (X=[-7.5, -5.5], Z_thickness=0.3) at Y=-4, Z_bottom=0.0. Extrude along vector (0, 8, 5.7). The ramp rises 5.7m over 8m plan length (switchback not modeled at LOG400).

Alternatively, model as a simple sloped box (approximate):
```
Circ_VS_ramp:      [-7.5, -4.0, 0.0] → [-5.5, 4.0, 6.0]
```
This is a bounding box — the actual ramp is the bottom 300mm slab within this volume. At LOG400, model as the slab extrusion described above.

Name: `Circ_VS_ramp`
Layer: `Type_03_Altitude::Circulation`

### J.2 Track Ascending Path

The track floor IS the ascending path. No separate geometry needed — the track floor slab (Section F.4) serves as the circulation surface. Annotate with text dots.

### J.3 Hilltop Station Landing

A flat landing slab at the track arrival inside the hilltop station. This is the hilltop floor slab (Section E.1). No separate element needed.

### J.4 Annotations (Text Dots)

Layer: `Type_03_Altitude::Annotations`

| Label | Position | Note |
|-------|----------|------|
| "VALLEY STATION" | (0, 0, 3) | Center of valley station |
| "HILLTOP STATION" | (0, 40, 25) | Center of hilltop station |
| "INCLINED TRACK" | (0, 20, 14) | Midpoint of track |
| "OBSERVATION TOWER" | (0, 38, 30) | Tower center |
| "ENTRY" | (0, -5, 2.5) | South face entry |
| "EXIT" | (0, 45, 24.5) | North face exit |
| "SLOPE: 28° / 53%" | (3.5, 20, 14) | Slope annotation |
| "FFL +0.00" | (-6, -4, 0.1) | Valley finished floor |
| "FFL +22.00" | (-6, 36, 22.1) | Hilltop finished floor |
| "ROOF +6.30" | (-6, -4, 6.4) | Valley roof level |
| "ROOF +28.30" | (-6, 36, 28.4) | Hilltop roof level |
| "TOWER TOP +32.00" | (-1, 38, 32.1) | Tower crown |

**Total text dots: 12**

### J.5 Terrain Proxy

Layer: `Type_03_Altitude::TerrainProxy`

A tilted surface representing the hillside the building sits on. Modeled as a thin slab (100mm) following the natural slope.

```
TerrainProxy:
  Corner 1: (-12, -10, -1.0)
  Corner 2: ( 12, -10, -1.0)
  Corner 3: ( 12,  50, 23.0)
  Corner 4: (-12,  50, 23.0)
```

**Modeling method:** Create 4 corner points, make a surface (SrfPt), then extrude down 0.1 for minimal thickness. Or model as a mesh quad.

**Section J count: 1 ramp + 12 text dots + 1 terrain proxy = 14 elements (plus text dots)**

---

## EXECUTION SUMMARY

### Element Count

| Section | Type | Count |
|---------|------|-------|
| B | Valley Station walls | 9 |
| C | Valley Station floor + roof + parapets | 5 |
| D | Hilltop Station walls | 9 |
| E | Hilltop Station floor + roof + parapets | 5 |
| F | Inclined track (sloped extrusions) | 4 |
| G.1 | Tower columns | 4 |
| G.2 | Tower walls | 2 |
| G.3 | Tower bracing | 8 |
| G.4 | Tower X-braces | 4 |
| G.5 | Tower cap plates | 4 |
| H.1 | Valley Station interior columns | 4 |
| H.2 | Hilltop Station interior columns | 4 |
| H.3 | Track transverse beams | 5 |
| I.1 | Wall kickers | 8 |
| I.2 | Column base plates | 12 |
| I.3 | Column top plates | 8 |
| I.4 | Roof assembly layers | 6 |
| I.5 | Parapet upstands | 6 |
| I.6 | Parapet drip edges | 6 |
| I.7 | Opening frames | 8 |
| I.8 | RC lintels | 3 |
| I.9 | Formwork lift lines | 16 |
| J.1 | Circulation ramp | 1 |
| J.4 | Text dot annotations | 12 |
| J.5 | Terrain proxy | 1 |
| **TOTAL** | | **152 elements** |

### Geometry Types

| Type | Count | Method |
|------|-------|--------|
| Axis-aligned boxes | ~130 | `Box(BoundingBox(Point3d, Point3d))` |
| Sloped extrusions | 7 | Profile polyline + `ExtrudeCurve` along vector (0,30,16) |
| Line extrusions (X-braces) | 4 | Line + pipe/profile sweep |
| Surface (terrain) | 1 | `SrfPt` or mesh |
| Text dots | 12 | `TextDot` |

### Build Order

1. Create 10 layers (Section A)
2. Valley Station walls — 9 boxes (Section B)
3. Valley Station floor/roof/parapets — 5 boxes (Section C)
4. Hilltop Station walls — 9 boxes (Section D)
5. Hilltop Station floor/roof/parapets — 5 boxes (Section E)
6. Inclined track — 4 sloped extrusions (Section F) — **key element, test first**
7. Tower — 22 elements (Section G)
8. Interior columns + track beams — 13 elements (Section H)
9. LOG400 detail — kickers, plates, assembly, formwork — 73 elements (Section I)
10. Circulation + annotations — 14 elements (Section J)

### Special Modeling Notes

1. **Sloped elements (Section F, J.1):** Cannot use axis-aligned Box(). Must create a closed polyline profile and extrude along vector (0, 30, 16). The executor should use `ExtrudeCurve` with a line defining the extrusion path.

2. **X-braces (Section G.4):** Create as pipe along a diagonal line, or sweep a small rectangular profile. These are the only truly diagonal elements in the model.

3. **Track beams (Section H.3):** Modeled as axis-aligned boxes for simplicity. The slope deviation over 300mm beam width is < 2mm — negligible at this scale.

4. **Terrain proxy (Section J.5):** Non-planar at building edges. Model as a simple tilted quad mesh or surface.

5. **All coordinates are meter-scale.** Do NOT multiply by 100.

---

## DECISION LOG

| Decision | Verdict | Rationale |
|----------|---------|-----------|
| Wall thickness | 300mm (simplified from 400mm archibase) | Visual clarity at building scale; 400mm total assembly, 300mm structural shell |
| Roof slab thickness | 300mm (stations), 200mm (track) | Stations: interior columns reduce effective span to ~5m, use 300mm for robustness. Track: 6m span, span/30 = 200mm |
| Track internal height | 4.0m | Clearance for funicular car + standing passengers |
| Track internal width | 5.4m (6m outer, 2x 300mm walls) | Single-track funicular with platform space |
| Tower height | +32m (10m above hilltop floor) | Observation function; open lattice crown avoids solid mass |
| Tower walls | N and S only (200mm), E and W open | Panoramic views east-west; wind screens north-south |
| Parapet thickness | 200mm | Thinner than main walls; maintenance-only roof access |
| Column grid (stations) | X=[-4,4], Y=[-2,2] / Y=[38,42] | Reduces 16m span to ~4-5m segments; avoids obstruction in center |
| Track beams | Every 5m, axis-aligned approximation | Sufficient structural rhythm; slope deviation negligible over beam width |
| Formwork lifts | 2.4m intervals | Standard Swiss RC formwork practice |
| Terrain proxy | Simple tilted quad, -1m below valley | Context surface; not architectural geometry |
| No expansion joints modeled | Omitted at LOG400 | Building length along slope is 50m — joints would be needed in reality but add complexity beyond this spec's scope. Add at LOG500 if needed. |

---

## KNOWN LIMITATIONS / FUTURE WORK

1. **Track-to-station junctions:** The track extrusions terminate at Y=5 and Y=35. The junction with station walls is not boolean-subtracted — the wall pieces are pre-split to accommodate the opening, but the exact intersection geometry (where sloped track walls meet vertical station walls) would need cleanup at LOG500.

2. **Funicular car:** Not modeled. Could be added as a separate object on the track floor.

3. **Interior fit-out:** No partitions, platforms, ticket halls, or MEP. LOG500+ scope.

4. **Waterproofing of inclined track:** The track roof assembly (insulation/membrane/gravel) is not modeled — only the structural slab. On a slope, waterproofing is critical but geometrically complex. Defer to LOG500.

5. **Foundation:** No foundation modeled below valley station floor slab. The -0.25m slab bottom is the lowest element.

---

*End of spec. Ready for roundtable review.*
