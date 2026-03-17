# Site Modeling Handoff — Terrain + Buildings Pipeline

**Author:** Andrea + Claude (Cairn Code)
**Date:** 2026-03-17
**For:** Henna (or anyone continuing the Rhino site modeling)
**Branch:** `andrea/prototypology-v2`

---

## What this is

A complete pipeline for generating 3D site models for the 7 lock sites along the Geneva–Villeneuve corridor. The goal: terrain mesh + 3D buildings + infrastructure context in Rhino, ready for architectural intervention design.

**Current status: 3 of 7 sites have data downloaded and preprocessed. Rhino import not yet done.**

---

## The 3 sites with data ready

| Site | Lock type | Center (LV95) | Terrain | Buildings 3D | Context 2D |
|------|-----------|---------------|---------|-------------|-----------|
| **Node 3 — Morges** | Temporal Lock | E 2'527'500, N 1'151'500 | 250k pts, 365–413m elev | LOD2 DXF (1.2 MB zip) | roads + rail + footprints |
| **Node 5 — CHUV** | Gradient Dispatcher | E 2'538'500, N 1'152'500 | 250k pts, 445–577m elev | LOD2 DXF (11.1 MB zip) | roads + rail + footprints |
| **Node 7 — Rennaz** | Bridge Lock | E 2'560'000, N 1'137'500 | 250k pts, 372–381m elev | LOD2 DXF (1.0 MB zip) | roads + footprints (no rail) |

### Why these 3 first
These were selected as Wave 1 because they span the corridor's diversity:
- **Morges** — flat lakeside town, hospital gap
- **CHUV** — steep urban hillside (132m elevation change!), densest site
- **Rennaz** — flat plain, isolated hospital island

---

## Where everything lives

### Terrain data — `output/city101_hub/terrain/`

| File | What | Size |
|------|------|------|
| `*_swissalti3d_*_2_2056_5728.tif` | Raw GeoTIFF (2m resolution). **Gitignored** — lives locally only. | ~1 MB each |
| `*_swissalti3d_*_xyz.csv` | XYZ point grid (X,Y,Z in LV95/LHN95). **Ready for Rhino.** | ~7 MB each |
| `*_swissalti3d_*_summary.json` | Grid metadata (bounds, elevation range, point count) | <1 KB each |
| `*_context.dxf` | 2D DXF with buildings, roads, rail from swissTLM3D | 200KB–1.4MB |
| `swissalti3d_download_urls.json` | URLs for all tiles (2m + 0.5m) for all 3 sites | — |

### Context data — `output/city101_hub/context/`

| File | What | Size |
|------|------|------|
| `*_swissbuildings3d.dxf.zip` | **LOD2 buildings with roof geometry** (swisstopo). In git. | 1–11 MB |
| `*_swissbuildings3d.dxf` | Extracted DXF. **Gitignored** (CHUV is 199MB). Unzip locally. | 18–199 MB |
| `*_building_footprint.geojson` | 2D building footprints (from swissTLM3D GeoPackage) | 0.3–2.4 MB |
| `*_road.geojson` | Road network | 0.3–0.9 MB |
| `*_railway.geojson` | Railway lines (not all sites have rail) | 48–88 KB |
| `*_metadata.json` | Site metadata (center coords, feature counts, columns) | ~3 KB |
| `swissbuildings3d_download_log.json` | Download provenance (STAC IDs, URLs, dates) | — |

### Pipeline research — `output/city101_hub/`

| File | What |
|------|------|
| `point_cloud_pipeline_research.md` | Full research doc: data sources, tool comparison, step-by-step pipeline, effort estimates |

---

## How to get data into Rhino

### Step 1: Terrain mesh

The XYZ CSV files contain a regular 500x500 grid of points at 2m spacing in LV95 coordinates.

**Option A — Rhino MCP (Claude does it):**
When Rhino is open with the MCP addon running, Claude can:
1. Read the CSV
2. Create a NURBS surface or mesh from the point grid
3. Place it on a TERRAIN layer

**Option B — Grasshopper:**
1. Open Grasshopper
2. Use `Read File` → parse CSV → `Construct Point` → `Delaunay Mesh`
3. Bake to TERRAIN layer

**Option C — Rhino command line:**
1. `Import` the CSV as points
2. `Patch` or `Drape` to create a surface
3. Or use `MeshPatch` for a mesh directly

### Step 2: 3D buildings

1. Unzip `*_swissbuildings3d.dxf.zip` (if not already extracted)
2. In Rhino: `File > Import > DXF` → select the extracted `.dxf`
3. These are LOD2 — they have actual roof geometry, not just extruded footprints
4. Move to a BUILDINGS layer

**Note:** The DXFs are in LV95 coordinates (same as the terrain), so they should align automatically.

### Step 3: 2D context (roads, rail)

The `*_context.dxf` files contain 2D polylines for roads, rail, and building outlines already separated by layer. Import directly into Rhino.

### Proposed layer structure in Rhino

```
Site_Name/
  TERRAIN/          -- ground mesh from swissALTI3D
  BUILDINGS/        -- 3D buildings from swissBUILDINGS3D (LOD2)
  BUILDINGS_2D/     -- 2D footprints (backup/reference)
  ROADS/            -- road network
  RAIL/             -- railway lines
  INTERVENTION/     -- (empty — for design work)
```

---

## Data sources explained

### swissALTI3D — terrain
- **What:** Digital terrain model (bare earth, no buildings/trees)
- **Resolution:** 2m grid (we have this) or 0.5m grid (URLs saved, not downloaded)
- **Format:** GeoTIFF → converted to XYZ CSV
- **CRS:** EPSG:2056 (LV95) horizontal, LHN95 heights
- **Source:** swisstopo, free open data (OGD)

### swissBUILDINGS3D 2.0 — 3D buildings
- **What:** 3D building models with roof geometry (LOD2)
- **Format:** DXF (directly importable into Rhino)
- **CRS:** EPSG:2056
- **Coverage:** All of Switzerland, updated ~annually
- **Source:** swisstopo, free OGD
- **Note:** These are real roof shapes, not just extruded footprints. Much better than what we had from the swissTLM3D GeoPackage (which was 2D only).

### swissTLM3D — 2D vector context
- **What:** Topographic landscape model — building footprints, roads, rail, water
- **Limitation:** No building heights in the GeoPackage we have
- **Used for:** Roads, rail, and building outlines as 2D context

### swissSURFACE3D — point cloud (NOT yet downloaded)
- **What:** Classified airborne LiDAR (15-20 pts/m2)
- **Why you might want it:** Vegetation canopy, precise roof geometry, bridge details
- **Size:** ~143 MB per km2 tile (need ~4 tiles per site = ~572 MB)
- **When to use:** Only if LOD2 buildings + 2m terrain aren't detailed enough
- **Pipeline:** Requires PDAL installation — see `point_cloud_pipeline_research.md`

---

## How to get data for the other 4 sites

The STAC API workflow is proven and repeatable. For any new site:

### 1. swissALTI3D terrain

```
STAC endpoint: https://data.geo.admin.ch/api/stac/v0.9/collections/ch.swisstopo.swissalti3d/items
Query: ?bbox={lon_min},{lat_min},{lon_max},{lat_max}
```

Bbox should be ~0.012 degrees around the center (WGS84). Download the `_2_2056_5728.tif` files (2m resolution).

Then convert to XYZ with Python:
```python
import rasterio, numpy as np
with rasterio.open("tile.tif") as src:
    data = src.read(1)
    # ... generate XYZ grid (see existing CSVs for format)
```

### 2. swissBUILDINGS3D

```
STAC endpoint: https://data.geo.admin.ch/api/stac/v0.9/collections/ch.swisstopo.swissbuildings3d_2/items
Query: ?bbox={lon_min},{lat_min},{lon_max},{lat_max}
```

Look for assets ending in `.dxf.zip`. Pick the most recent vintage (2021-09 is latest with DXF tiles).

### 3. 2D context (if needed)

Already extracted from the swissTLM3D GeoPackage at `source/00-datasets 2/lhiamrossier/GPKG/190226_TLM3D_City101_v3_EN.gpkg`. Can be re-extracted for any site center + radius using geopandas/fiona.

### Remaining sites

| Site | Center WGS84 | Center LV95 | Status |
|------|-------------|-------------|--------|
| Node 1 — Geneva North | 46.222, 6.097 | E 2'496'500, N 1'122'500 | Not started |
| Node 2 — Nyon | 46.384, 6.236 | E 2'507'500, N 1'139'500 | Not started |
| Node 4 — Crissier-Bussigny | 46.548, 6.552 | E 2'533'500, N 1'153'500 | Not started |
| Node 6 — Montreux-Glion | 46.436, 6.910 | E 2'560'500, N 1'143'500 | Not started |

---

## Key decisions made

1. **Free pipeline over paid tools.** swisstopo OGD is sufficient for LOD 100-200 site models. No need for RhinoTerrain or other paid plugins.

2. **swissBUILDINGS3D over point cloud extrusion.** The LOD2 DXFs give real roof geometry and import directly into Rhino. Much simpler than processing swissSURFACE3D point clouds for building volumes.

3. **2m terrain resolution.** Adequate for architectural site models. 0.5m is available if needed (URLs saved).

4. **Two-tier approach.** Fast path (GeoTIFF + DXF) for all sites first, then upgrade select sites with full point cloud if more detail is needed.

5. **No PDAL/CloudCompare needed** for the current pipeline. Those are only needed if you want the full point cloud path (vegetation, precise roofs beyond LOD2).

---

## Asking Claude to continue this work

When you open a session to do the Rhino modeling:

1. Open Rhino with the MCP addon running
2. Tell Claude: "I'm continuing the site modeling pipeline from the handoff at `output/city101_hub/site_modeling/HANDOFF.md`. Let's import [site name] into Rhino."
3. Claude can read the XYZ CSV, create terrain mesh, set up layers, and guide you through the DXF import — all via MCP.

For downloading data for the remaining 4 sites, Claude can run the STAC API queries and GeoTIFF conversion automatically — same process used for the first 3.

---

## Files in this folder

| File | What |
|------|------|
| `HANDOFF.md` | This document |
| (future) | Rhino import scripts, Grasshopper definitions, per-site notes |
