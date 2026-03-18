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
- **QA issues found and fixed** — see "QA Pass: Rennaz Site Context Fix" section below

### Screenshots
1. **Perspective — isolated lock:** Full 90m bridge from station to hospital ramp
2. **Side elevation:** V-columns, elevated deck, ramp descending to grade

### Performance
- ~1,600 total objects — very light
- File size: 11MB

---

## QA Pass: Rennaz Site Context Fix (2026-03-18)

Visual inspection revealed several issues in the Rennaz model. All fixed via Rhino MCP.

### Issues found & fixed

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 1 | CRITICAL | Roads + Context_2D at Z=0 (374m below terrain) | Moved 360 polylines by (0, 0, 374) |
| 2 | MAJOR | 1,215 buildings scattered across 4km tile, only 18 near terrain | Deleted 1,197 buildings outside terrain extent (+50m buffer) |
| 3 | MODERATE | 20 empty DXF import + default layers cluttering panel | Deleted all 20 empty layers |
| 4 | MINOR | Text dot at (0, 0, 0) | Moved to terrain center (496, 0, 374) |
| 5 | MINOR | No 500m boundary circle (CHUV had one) | Added 500m circle at (496, 0, 374) on CONTEXT_2D |

### Not fixed (deferred)
- **Terrain X not centered:** E offset used tile edge (2,560,000) not center (2,560,500). Terrain bbox X is [0, 992] instead of [-496, 496]. Cosmetic — all data is consistent and metadata documents the offset. Fixing would require moving terrain + buildings + roads + lock all by (-496, 0, 0).

### After fix
- **Objects:** 499 (was 1,695) — 18 buildings, 360 polylines, 118 lock breps, 2 terrain, 1 circle, 1 textdot
- **Layers:** 12 clean layers (Rennaz_Site hierarchy + Lock_07 hierarchy)
- **Model Z range:** 371–390m (everything at terrain level)

### Root cause for future sites
- 2D context DXFs from SwissTLM3D have `has_height: false` — polylines import at Z=0. Must move to terrain Z after import.
- swissBUILDINGS3D tiles cover ~4km x 4km, much larger than the 1km terrain tile. Must cull buildings outside terrain extent.
- DXF import creates one layer per Swiss building type. These should be purged after reassigning objects.

### ~~Still to check: CHUV and Morges~~
All three sites QA'd — see sections below.

---

## QA Pass: CHUV Site Context Fix (2026-03-18)

Same root causes as Rennaz confirmed. All fixed via Rhino MCP.

### Issues found & fixed

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 1 | CRITICAL | Roads (680) at Z=0 (451m below terrain) | Moved all 680 polylines by (0, 0, 451) |
| 2 | CRITICAL | Context_2D (1,075) at Z=0 | Moved all 1,075 polylines by (0, 0, 451) |
| 3 | CRITICAL | Rail (7) at Z=0 | Moved all 7 polylines by (0, 0, 451) |
| 4 | MAJOR | 9,355 buildings scattered across 7km, only 1,316 near terrain | Deleted 8,039 buildings outside terrain extent (+50m buffer) |
| 5 | MODERATE | 26 empty DXF import + default layers | Deleted all 26 empty layers |
| 6 | MINOR | Text dot at (0, 0, 400) — below terrain | Moved to lock position (-450, -400, 451) |
| 7 | MINOR | Boundary circle at Z=500 — inconsistent with other 2D linework | Moved to Z=451 (matching roads/context reference plane) |
| 8 | MINOR | 1 rail polyline spanning 4km (X: -4493 to -497) ruining zoom-to-fit | Deleted — too extreme for site context |

### CHUV-specific notes
- **Terrain Z range is 447–577m** (130m elevation change, very hilly). Unlike Rennaz (flat, 372–381m), no single Z perfectly matches all terrain. Used Z=451 (lock elevation, near terrain min) as reference plane for all 2D linework.
- **Roads were also at Z=0** despite being imported via the DXF-in-km workflow. The km→m scaling preserved XY but Z was still 0 (has_height: false in source DXF).
- **4 remaining polylines extend 100–1100m beyond terrain** (2 rail, 2 road) — these are real infrastructure corridors approaching the site. Left in place as context.

### After fix
- **Objects:** ~3,162 (was 11,202) — 1,316 buildings, 1,761 polylines, 82 lock breps, 2 terrain, 1 circle, 1 textdot
- **Layers:** 14 clean layers (Default + CHUV_Site hierarchy + Lock_05 hierarchy)
- **Model Z range:** 439–625m (everything at terrain level)

---

## QA Pass: Morges Site Context Fix (2026-03-18)

Same root causes as Rennaz/CHUV, plus a **building tile mismatch** discovery.

### Issues found & fixed

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 1 | CRITICAL | Roads (503) at Z=0 (392m below terrain) | Moved all 503 polylines by (0, 0, 392) |
| 2 | CRITICAL | Context_2D (956) at Z=0 | Moved all 956 polylines by (0, 0, 392) |
| 3 | CRITICAL | Rail (74) at Z=0 | Moved all 74 polylines by (0, 0, 392) |
| 4 | MAJOR | 1,366 buildings — **none overlapping terrain tile** (see below) | Deleted 1,335 outside 200m buffer, kept 31 nearest |
| 5 | MODERATE | 17 empty DXF import + default layers | Deleted all 17 empty layers |
| 6 | MINOR | Text dot at (0, 0, 0) | Moved to lock position (0, 15, 392) |
| 7 | MINOR | No 500m boundary circle | Added 500m circle at (0, 0, 392) on CONTEXT_2D |

### Building tile mismatch (Morges-specific)
- **All 1,366 buildings** are at local X [626, 5000] — the terrain ends at X=492.
- The building DXF tile is offset **~134m east** of the terrain tile. Zero buildings actually overlap with the terrain.
- This means the **wrong swissBUILDINGS3D tile was imported** for Morges. The hospital (LV95 E 2,527,500) is west of the building tile coverage.
- **Action needed:** Download the correct building tile covering E ~2,526,000–2,528,000 and re-import.
- Kept 31 nearest buildings (within 200m of terrain east edge) as minimal edge context.

### After fix
- **Objects:** ~1,650 (was 2,942) — 31 buildings, 1,533 polylines, 41 lock breps, 2 terrain, 1 circle, 1 textdot
- **Layers:** 13 clean layers (Default + Morges_Site hierarchy + Lock_03 hierarchy)
- **Model Z range:** 366–412m (everything at terrain level)

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
