# Wave 3: Site Context Integration Log

**Branch:** `andrea/prototypology-v2`
**Date:** 2026-03-18
**Session:** Cairn Code (CLI)

---

## Site 1: CHUV (Node 5) — Gradient Dispatcher

### Steps taken

1. **Layer hierarchy created:** `CHUV_Site/` with sublayers TERRAIN, BUILDINGS_3D, ROADS, RAIL, CONTEXT_2D
2. **Terrain imported:** Read `city101_node5_chuv_swissalti3d_2021_2538-1152_2_2056_5728_xyz.csv`
   - 250,000 points (500x500 grid, 2m spacing)
   - Subsampled every 4th point → 125x125 = 15,625 vertices, 15,376 quad faces
   - Created as structured quad mesh on TERRAIN layer
3. **Coordinate offset applied (Option A):** E-2538500, N-1152500
   - Stored as text dot at (0, 0, 400) on TERRAIN layer
   - All subsequent imports use the same offset
4. **Buildings imported:** Unzipped `city101_node5_chuv_swissbuildings3d.dxf.zip` (199MB DXF)
   - 9,355 mesh objects imported across 16 Swiss building type layers
   - **Discovery:** DXF coordinates are in **kilometers** (not meters) — required 1000x scale
   - Scaled from origin by (1000, 1000, 1000), then moved by offset
   - All objects reassigned to `CHUV_Site::BUILDINGS_3D`
   - Building types: Einzelhaus (8703), Offenes Gebaeude (341), Hochhaus (76), Sakrales Gebaeude (70), Im Bau (42), Flugdach (34), and others
5. **2D context imported:** `city101_node5_chuv_context.dxf`
   - Also in kilometers — same scale+offset treatment
   - Roads (680 polylines) → `CHUV_Site::ROADS`
   - Rail (7 polylines) → `CHUV_Site::RAIL`
   - Buildings 2D (1,075 polylines) → `CHUV_Site::CONTEXT_2D`
6. **500m boundary circle** created at (0, 0, 500) on CONTEXT_2D layer
7. **Lock placed (Option B — script modified):**
   - Created v3 script with `SITE_ORIGIN = (-450, -400, 451.0)`
   - All geometry offset by SITE_ORIGIN during creation
   - 68 objects: 4 volumes, 8 floor plates, 1 void, 52 columns, 10 openings, 6 circulation elements
   - Grouped as `Lock_05_CHUV_Gradient_Sited`

### Coordinate offset
- **LV95 offset:** E 2,538,500 / N 1,152,500
- **Terrain local range:** X [-500, +498], Y [-498, +500]
- **Lock position (local):** (-450, -400, 451.0)
- **Lock position (LV95):** E 2,538,050, N 1,152,100, Z 451m

### What worked
- Terrain mesh creation from CSV is fast and clean
- Building alignment with terrain is correct (verified from front/side views)
- Lock scale feels right relative to surrounding buildings (20m x 34m footprint)
- The SITE_ORIGIN pattern is clean and reusable

### Issues found
- **DXF coordinates in km:** swissBUILDINGS3D and 2D context DXFs use kilometers, not meters. Must scale by 1000. This was not documented in the handoff.
- **CHUV campus is at the edge of the terrain tile:** The actual CHUV coordinates (E 2,537,868) are ~132m west of the tile boundary (E 2,538,000). Lock is placed at the nearest terrain edge.
- **Text dot interferes with zoom-to-fit:** Large text dots dominate the viewport bounding box. Should use smaller dots or place at lock position instead of origin.

### Performance
- 11,119 total objects (9,356 meshes, 1,762 polylines, 1 text dot) + 68 lock objects
- Responsive in wireframe mode
- Building import (199MB DXF) took ~10 seconds

### Screenshots
1. **Perspective — lock in site context:** Lock visible among LOD2 buildings, stepping up the hillside
2. **Right/section — gradient section:** Shows 4 levels stepping with terrain slope
3. **Top — plan view:** Lock footprint relative to surrounding urban fabric

---

## Site 2: Morges (Node 3) — Temporal Lock

### Steps taken

1. Layer hierarchy: `Morges_Site/` with TERRAIN, BUILDINGS_3D, ROADS, RAIL, CONTEXT_2D
2. Terrain mesh: 125x125 subsampled, offset E-2527500, N-1151500
3. Buildings: 1,366 meshes (Einzelhaus 1168, Offenes Gebaeude 185, etc.) — scaled 1000x, offset, reassigned
4. 2D context: Roads (503), Rail (74), Buildings 2D (956) — same scale+offset
5. Lock placed at SITE_ORIGIN = (0, 15, 392.0) — right at tile center, matching hospital location
6. 41 objects: 3 volumes, 6 floor plates, 20 columns, 10 openings, 2 stairs

### Coordinate offset
- **LV95 offset:** E 2,527,500 / N 1,151,500
- **Lock position (local):** (0, 15, 392.0) — essentially at tile center
- **Lock position (LV95):** E 2,527,500, N 1,151,515, Z 392m

### What worked
- Morges hospital is right at the tile center — ideal alignment
- Flat terrain (365–413m range, gentle slopes) — simplest site
- Much lighter model than CHUV (1,366 buildings vs 9,355)

### Issues
- Building tile extends well beyond terrain tile (same as CHUV)
- No significant issues — flat terrain is forgiving

### Screenshots
1. **Perspective — isolated lock:** Night/Dawn chambers with Gate threshold clearly visible
2. **Front elevation:** Gate rises above flanking chambers, openings in amber

### Performance
- ~2,900 total objects — very responsive
- File size: 11MB

---

## Site 3: Rennaz (Node 7) — Bridge Lock

### Steps taken

1. Layer hierarchy: `Rennaz_Site/` with TERRAIN, BUILDINGS_3D, ROADS, RAIL, CONTEXT_2D
2. Terrain mesh: 125x125 subsampled, offset E-2560000, N-1137500
3. Buildings: 1,215 meshes — scaled 1000x, offset, reassigned
4. 2D context: Roads (220), Buildings 2D (140), no Rail in this tile
5. Lock placed at SITE_ORIGIN = (200, 300, 374.0) — within terrain tile
6. 118 objects total (8 volumes/floors + 110 structure/openings/circulation)

### Coordinate offset
- **LV95 offset:** E 2,560,000 / N 1,137,500
- **Lock position (local):** (200, 300, 374.0)
- **Lock position (LV95):** E 2,560,200, N 1,137,800, Z 374m

### What worked
- Bridge Lock is the most visually striking — 90m span with clear structural rhythm
- Nearly flat terrain (372–381m) is ideal for a bridge concept
- Bay frames, lateral openings, lane divider all read clearly

### Issues
- **Hospital is outside terrain tile:** HRC Rennaz at N 1,138,644 is ~644m north of tile boundary. Lock placed within tile, oriented toward hospital.
- No rail data in context DXF for this tile

### Screenshots
1. **Perspective — isolated lock:** Full 90m bridge from station to hospital ramp
2. **Side elevation:** V-columns, elevated deck, ramp descending to grade

### Performance
- ~1,600 total objects — very light
- File size: 11MB

---

## Cross-site observations

- [x] **Is the workflow repeatable?** Yes — after CHUV, Morges and Rennaz each took ~5 minutes
- [x] **How long per site?** CHUV: ~20 min (first, discovery of DXF km issue). Morges: ~5 min. Rennaz: ~5 min.
- [x] **What should be automated for the remaining 4 sites?**
  - Layer creation (same hierarchy every time)
  - Terrain mesh from CSV (identical script, just change file path and offset)
  - Building import + scale 1000x + offset + layer reassign (identical flow)
  - Could be a single parameterized Python script: `import_site(name, csv, buildings_dxf, context_dxf, offset_e, offset_n)`
- [x] **Does the lock geometry make sense at real scale on real terrain?**
  - CHUV: 20x34m lock among dense buildings — scale is right, a medium institutional building
  - Morges: 34x10m lock is modest — fits the small-town context
  - Rennaz: 90m bridge is the biggest intervention — but bridges are inherently long, reads well
- [x] **Any script modifications needed?**
  - v3 scripts with SITE_ORIGIN parameter work well — this is the pattern for the app
  - The `box()` and `box_pts()` helpers with offset are the reusable template
  - Consider adding terrain Z-sampling so locks auto-match ground elevation

---

## Key discovery: DXF coordinate units

**swissBUILDINGS3D and 2D context DXFs are in kilometers, not meters.**

This is critical for all future imports:
1. Import DXF (objects land on DXF's own layers)
2. Scale all imported objects by (1000, 1000, 1000) from origin
3. Move by (-OFFSET_E, -OFFSET_N, 0) to local origin
4. Reassign to project layer hierarchy
