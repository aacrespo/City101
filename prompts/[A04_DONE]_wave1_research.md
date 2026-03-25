# Wave 1: Terrain + Point Cloud Research

**Branch:** `andrea/prototypology-v2` (confirm you're on it)
**Rhino needed:** No
**Duration:** ~1 session
**Commit when done:** `[DATA] Terrain + point cloud research for 3 lock sites`

---

## What to do

Run two research agents in parallel using `/team`. Both are Analyst role.

---

## Agent 1: Terrain + GIS Data Researcher

**Goal:** Find and extract site context data for 3 lock nodes.

**Sites:**
- Node 3 (Morges): lat 46.511, lon 6.494, LV95 ~2'527'500 / 1'151'500
- Node 5 (CHUV Lausanne): lat 46.525, lon 6.642, LV95 ~2'538'500 / 1'152'500
- Node 7 (Rennaz): lat 46.389, lon 6.912, LV95 ~2'560'000 / 1'137'500

**Tasks:**

1. Inspect `source/00-datasets 2/lhiamrossier/GPKG/190226_TLM3D_City101_v3_EN.gpkg`
   - List all layers and their attributes
   - Check for building height fields (HOEHE, HEIGHT, GEBAEUDE_HOEHE, etc.)
   - Extract buildings within 500m of each site

2. Inspect `source/WORK copy/` and `source/Documents copy/`
   - List all GIS-relevant files (shp, gpkg, geojson, tif, asc)
   - Note any elevation/height/terrain data

3. Research swissALTI3D on data.geo.admin.ch
   - Find download URLs for 2m DTM tiles covering each site
   - Document the tile naming system and format (GeoTIFF)
   - Download tiles if accessible via REST API (free, no cost)

4. For each site, extract 500m-radius context:
   - Buildings with heights (if available)
   - Rail lines
   - Roads
   - Export as DXF for Rhino import (layers: Buildings, Rail, Roads, Terrain)

**Output:**
- `output/city101_hub/terrain/` — one DXF per site + GeoTIFF tiles
- `output/city101_hub/context/` — metadata JSON per site (source, CRS, layer list, feature counts)
- Print full summary: what was found, what's missing, quality assessment

---

## Agent 2: Point Cloud Pipeline Researcher

**Goal:** Research the complete pipeline from raw LiDAR point clouds to Rhino 3D site models.

**Research questions (investigate all):**

1. **Data source: swissSURFACE3D (swisstopo)**
   - What is it? (density, classification, format, CRS)
   - How to download? (REST API, STAC, manual)
   - Tile system and coverage for Geneva–Villeneuve corridor
   - File sizes and processing requirements

2. **Import to Rhino**
   - Native Rhino point cloud support (formats, limits)
   - Cockroach plugin (capabilities, installation)
   - Volvox for Grasshopper
   - CloudCompare as preprocessing bridge
   - Which approach do architecture firms actually use?

3. **Semantic segmentation**
   - Classifying raw points into: buildings, terrain, vegetation, infrastructure, water
   - LAS classification codes (what's already classified in swissSURFACE3D?)
   - Open3D Python for custom classification
   - QGIS point cloud tools (3.32+)
   - Machine learning approaches (PointNet, etc.) — feasible or overkill?

4. **Preprocessing pipeline**
   - Raw LAS → filtered → classified → meshed → Rhino
   - Which steps need which tools?
   - CloudCompare MCP — does it exist?
   - QGIS MCP — does it exist?
   - What can be scripted vs manual?

5. **Professional practice**
   - How do architecture firms go from site survey to digital site model?
   - What's the typical pipeline (survey company → point cloud → model)?
   - What specialist roles review 3D models at LOG 400?
   - Time/cost benchmarks for point cloud → model workflows

6. **Tools & automation potential**
   - Which steps could become Claude Code tools/skills?
   - Which need human judgment?
   - Recommended agents, skills, and rules to build

**Output:** `output/city101_hub/point_cloud_pipeline_research.md`

Structure:
1. Pipeline diagram (ASCII: steps → tools → formats at each stage)
2. Data source assessment (swissSURFACE3D availability + alternatives)
3. Tool recommendations (ranked by practicality)
4. Agent/skill/rule specs (what to build, what each does)
5. Effort estimates per pipeline step
6. Recommended next steps (ordered by priority)

---

## After both agents finish

1. Review their outputs
2. Check: did Agent 1 find building heights in the GeoPackage? If not, note the gap.
3. Check: did Agent 1 successfully download swissALTI3D tiles? If not, note the URLs for manual download.
4. Commit: `[DATA] Terrain + point cloud research for 3 lock sites`
5. Push branch: `git push -u origin andrea/prototypology-v2`

---

## Reference files
- Lock concepts: `output/city101_hub/prototypology_content.json`
- Coordinate conventions: `.claude/rules/conventions.md`
- Data protocol: `.claude/rules/data-protocol.md`
- Point cloud conventions: `workflows/point-cloud-protocol.md`
