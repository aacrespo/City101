# Point Cloud to Rhino 3D Site Model — Pipeline Research

> Research for City101 Prototypology pipeline: raw LiDAR to architectural site models
> Generated: 2026-03-17 | Analyst role

---

## 1. Pipeline Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    POINT CLOUD → SITE MODEL PIPELINE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  STEP 1: ACQUIRE          STEP 2: PREPROCESS       STEP 3: CLASSIFY         │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐         │
│  │ swissSURFACE │         │ Crop to site │         │ Filter by    │         │
│  │ 3D (STAC API)│────────▶│ (500m radius)│────────▶│ ASPRS class  │         │
│  │              │         │              │         │              │         │
│  │ Format: COPC │         │ Tool: PDAL   │         │ Tool: PDAL   │         │
│  │ (LAZ 1.4)    │         │ or CloudComp │         │ or CloudComp │         │
│  └──────────────┘         └──────────────┘         └──────────────┘         │
│        │                                                  │                 │
│        │ ~200 MB/tile                                     │                 │
│        │ (1 km²)                                          ▼                 │
│                                                                             │
│  STEP 4: MESH             STEP 5: IMPORT           STEP 6: MODEL           │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐         │
│  │ Ground → DTM │         │ Import mesh  │         │ Architectural│         │
│  │ Bldg → hulls │────────▶│ to Rhino     │────────▶│ site model   │         │
│  │              │         │              │         │              │         │
│  │ Tool: PDAL / │         │ Format: OBJ/ │         │ Tool: Rhino  │         │
│  │ CloudCompare │         │ PLY/3DM      │         │ + Grasshoppr │         │
│  └──────────────┘         └──────────────┘         └──────────────┘         │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  FILES AT EACH STAGE:                                                       │
│  ① .copc.laz  ② .laz (cropped)  ③ .laz (filtered)  ④ .obj/.ply  ⑤ .3dm   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Simplified decision tree

```
Do you need terrain only?
  YES → swissALTI3D (2m GeoTIFF) → Grasshopper heightfield → done
  NO  → continue below

Do you need buildings + terrain + vegetation?
  YES → swissSURFACE3D → PDAL crop+filter → CloudCompare mesh → Rhino import

Do you need just building footprints extruded?
  YES → swissTLM3D (vector) → Rhino import → extrude to height → done
```

---

## 2. Data Source Assessment

### 2.1 swissSURFACE3D (Primary Source)

| Property | Value |
|----------|-------|
| **What** | Classified airborne LiDAR point cloud of all Switzerland |
| **Density** | Several million points per km² (~15–20+ pts/m²) |
| **Accuracy** | Sub-decimeter XYZ |
| **CRS** | CH1903+ / LV95 (EPSG:2056), heights in LHN95 (EPSG:5728) |
| **Tile size** | 1 km² |
| **Format (new, 2024+)** | Cloud Optimized Point Cloud LAZ 1.4 (COPC), ~200 MB/tile |
| **Format (legacy, pre-2024)** | LAS 1.2, ~610 MB/tile |
| **License** | Free, open data (OGD) |
| **Coverage** | All of Switzerland (first complete coverage achieved, ongoing updates) |
| **Update cycle** | Rolling updates by region |

#### Classification codes in swissSURFACE3D

| Code | Class | Available | Notes |
|------|-------|-----------|-------|
| 1 | Unclassified | Yes | Points not fitting other classes |
| 2 | Ground | Yes | Terrain surface |
| 3 | Vegetation | Yes | Low/medium/high combined |
| 6 | Building (roofs) | Yes | Building roof surfaces |
| 9 | Water | Yes | Lake and river surfaces |
| 17 | Bridge deck | Yes | Bridges, footbridges, viaducts |
| — | Building facades | Newer tiles | Added in recent generation |
| — | Power lines/poles | Newer tiles | Added in recent generation |
| — | Bridge piers | Newer tiles | Added in recent generation |

**Key finding**: swissSURFACE3D already comes pre-classified. For the City101 use case (terrain + buildings + infrastructure context), the existing classification is sufficient. No custom ML classification needed.

#### Tile naming convention

```
swisssurface3d_YEAR_{E}-{N}_2056_5728.laz
```

Where `{E}` and `{N}` are the LV95 km coordinates of the tile's southwest corner.

#### Download methods

1. **STAC API** (recommended for automation):
   - Endpoint: `https://data.geo.admin.ch/api/stac/v0.9/collections/ch.swisstopo.swisssurface3d`
   - Query by bounding box to find tiles covering a site
   - Returns direct download URLs for each tile

2. **swisstopo map viewer** (manual):
   - Go to map.geo.admin.ch, enable swissSURFACE3D layer
   - Click tile to get download link

3. **opendata.swiss** (catalog):
   - Dataset page with metadata and links to STAC

#### Tiles needed for the Geneva–Villeneuve corridor

The corridor spans ~70 km east-west (E ~2'500 to ~2'560 in LV95) and ~25 km north-south (N ~1'130 to ~1'155). That is roughly **70 × 25 = 1,750 tiles** for full corridor coverage.

For the 7 lock sites (500m radius each = ~1 km² per site), you need **1–4 tiles per site**, roughly **7–28 tiles total** depending on site boundaries.

| Site | Approx LV95 E | Approx LV95 N | Tiles needed |
|------|---------------|---------------|--------------|
| 1. Geneva North | 2'496–2'498 | 1'122–1'124 | 2–4 |
| 2. Nyon | 2'507–2'509 | 1'139–1'141 | 2–4 |
| 3. Morges | 2'527–2'529 | 1'151–1'153 | 2–4 |
| 4. Crissier-Bussigny | 2'533–2'535 | 1'153–1'155 | 2–4 |
| 5. Lausanne CHUV | 2'538–2'540 | 1'152–1'154 | 2–4 |
| 6. Montreux-Glion | 2'560–2'562 | 1'143–1'145 | 2–4 |
| 7. Rennaz | 2'563–2'565 | 1'137–1'139 | 2–4 |

**Total download: ~28 tiles × 200 MB = ~5.6 GB** (COPC format). Manageable.

### 2.2 Complementary Sources

| Source | What | Format | When to use |
|--------|------|--------|-------------|
| **swissALTI3D** | Digital terrain model (bare earth) | GeoTIFF, 2m grid | Quick terrain mesh without point cloud processing |
| **swissTLM3D** | Topographic landscape model | GeoPackage (vector) | Building footprints with heights, roads, rail, water |
| **swissBUILDINGS3D 2.0** | 3D building models | CityGML / DXF | Detailed building geometry (LOD2) |
| **Swiss STAC catalog** | All geo products | Various | Discover other relevant layers |

**Recommendation**: For a BA6 studio project, start with swissALTI3D (terrain) + swissTLM3D (buildings, roads). Use swissSURFACE3D only for the final detailed site models where you need vegetation or precise roof geometry.

---

## 3. Tool Recommendations

### 3.1 Ranked by practicality for this project

| Rank | Tool | Role in pipeline | Install complexity | Learning curve |
|------|------|-----------------|-------------------|---------------|
| 1 | **PDAL** (+ pdal-wrench) | Crop, filter, classify, convert LAS/LAZ | `conda install pdal` | Low — JSON pipelines |
| 2 | **CloudCompare** | Visualize, subsample, mesh, export | Desktop app (free) | Medium — GUI based |
| 3 | **Rhino 8** (native) | Import E57/LAS/PLY, model, render | Already installed | Low (you know Rhino) |
| 4 | **Grasshopper** (Delaunay) | Point grid → terrain mesh, parametric | Built into Rhino | Low-medium |
| 5 | **Cockroach** (GH plugin) | Point cloud processing in Grasshopper | food4rhino install | Medium |
| 6 | **QGIS 3.40+** | Visualize point clouds, basic processing | Desktop app (free) | Medium |
| 7 | **Volvox** (GH plugin) | E57 import, point cloud manipulation | food4rhino install | Medium |
| 8 | **Open3D** (Python) | Custom classification, advanced processing | `pip install open3d` | High |

### 3.2 Tool details

#### PDAL — Point Data Abstraction Library

The most practical tool for batch processing. Runs from command line with JSON pipeline definitions.

**Key operations for City101:**
```bash
# Inspect a tile
pdal info tile.copc.laz --summary

# Crop to 500m radius around a site center
pdal translate input.copc.laz output_cropped.laz \
  --filter filters.crop --filters.crop.point="EPSG:2056 2538000 1153000" \
  --filters.crop.distance=500

# Filter ground points only (for terrain mesh)
pdal translate input.laz ground.laz \
  --filter filters.range --filters.range.limits="Classification[2:2]"

# Filter building points only
pdal translate input.laz buildings.laz \
  --filter filters.range --filters.range.limits="Classification[6:6]"

# Convert to CSV for Grasshopper import
pdal translate ground.laz ground.csv --writers.text.order="X,Y,Z"
```

**Install**: `conda install -c conda-forge pdal python-pdal` or `brew install pdal`

#### CloudCompare

Free, open-source 3D point cloud and mesh processing software. The standard tool in architecture/surveying for point cloud visualization and manipulation.

**Key operations:**
- Load LAS/LAZ directly
- Subsample (reduce point density for performance)
- Segment by classification code
- Compute normals
- Poisson surface reconstruction (point cloud → mesh)
- Export to OBJ, PLY, E57 for Rhino import

**MCP server**: A demo CloudCompare MCP exists at `github.com/truebelief/CloudCompareMCP`. It wraps CloudCompare's Python scripting interface. Status: experimental/demo — requires customization. Not production-ready but proves the concept is viable.

#### Rhino 8 — Native point cloud support

Rhino 8 natively imports:
- **E57** — full support with the E57 import plugin
- **LAS/LAZ** — supported
- **PTS, XYZ, CSV** — supported

**Limitations:**
- Large point clouds (>50M points) cause viewport performance issues
- Subsample before import — aim for <5M points per site
- Point clouds near origin display correctly; far from origin can have precision issues (move to 0,0,0 if needed, but this means losing LV95 coordinates — document the offset)

#### Cockroach (Grasshopper plugin)

Developed at IBOIS (EPFL Wood Construction Lab — same campus). Wraps Open3D, CGAL, and Cilantro libraries for Grasshopper.

**Capabilities:**
- Point cloud post-processing (normals, downsampling, outlier removal)
- Meshing (Poisson, Ball Pivoting, Alpha Shapes)
- Segmentation (RANSAC plane detection)
- Compatible with Rhino 6 and 7 (check Rhino 8 compatibility)

**Note**: Developed at EPFL — potential for direct support/advice from the lab.

#### Volvox (Grasshopper plugin)

Focused on E57 format and BIM/heritage workflows.

**Capabilities:**
- Full E57 import/export
- PLY support
- Scanner position extraction
- Color-based segmentation
- Multithread processing (~1M points/second for segmentation)

**Best for**: When working with E57 files from terrestrial laser scanners. Less relevant for airborne LiDAR (which comes in LAS/LAZ).

#### QGIS 3.40+ with point cloud tools

QGIS now has native point cloud rendering and processing via PDAL integration.

**Capabilities:**
- Direct LAZ/LAS viewing in 2D and 3D
- Classification-based rendering
- Point cloud processing algorithms (clip, thin, convert)
- Integration with broader GIS workflow (overlay with vector data)

**MCP server**: `github.com/jjsantos01/qgis_mcp` — active project, allows Claude to control QGIS via socket connection. Can execute processing algorithms, load layers, run Python code in QGIS. Tested with QGIS 3.22+.

#### Open3D (Python library)

Advanced point cloud processing with ML capabilities.

**Capabilities:**
- Point cloud I/O (PCD, PLY, XYZ, but NOT native LAS — needs conversion)
- RANSAC plane segmentation
- DBSCAN clustering
- Normal estimation
- Poisson surface reconstruction
- PointNet/PointNet++ semantic segmentation (via Open3D-ML)

**Verdict for City101**: Overkill. swissSURFACE3D is already classified. Use Open3D only if you need custom classification beyond what swisstopo provides.

### 3.3 Semantic segmentation — do you need it?

**Short answer: No.** swissSURFACE3D already provides classified points (ground, building, vegetation, water, bridges). The existing classification is sufficient for:
- Extracting terrain meshes (class 2)
- Extracting building volumes (class 6)
- Mapping vegetation coverage (class 3)
- Identifying water bodies (class 9)
- Locating bridges and infrastructure (class 17)

**When you would need custom classification:**
- If working with unclassified point clouds (e.g., drone surveys)
- If you need finer-grained classes (e.g., deciduous vs. coniferous trees)
- If swisstopo's classification has errors at your specific sites

**ML approaches (PointNet, etc.) — verdict**: Not feasible for a BA6 project timeline. Training requires labeled datasets, GPU resources, and significant debugging time. The pre-classified swissSURFACE3D data eliminates this need entirely.

---

## 4. Preprocessing Pipeline — Step by Step

### Step 1: Download tiles (automated)

**Tool**: Python script using STAC API
**Input**: Site center coordinates (from prototypology_content.json)
**Output**: Raw COPC/LAZ files in `output/city101_hub/point_cloud/raw/`

```python
# Pseudocode for download script
import requests

STAC_URL = "https://data.geo.admin.ch/api/stac/v0.9/collections/ch.swisstopo.swisssurface3d/items"

def download_tiles_for_site(site_name, center_e, center_n, radius_m=500):
    """Query STAC API for tiles covering site, download each."""
    bbox = [center_e - radius_m, center_n - radius_m,
            center_e + radius_m, center_n + radius_m]
    response = requests.get(STAC_URL, params={"bbox": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"})
    for item in response.json()["features"]:
        download_url = item["assets"]["data"]["href"]
        # download to output/city101_hub/point_cloud/raw/{site_name}/
```

**Effort**: 2–3 hours to build and test
**Automation potential**: High — perfect Claude Code tool

### Step 2: Crop to site extent

**Tool**: PDAL (crop filter)
**Input**: Raw LAZ tiles
**Output**: Single cropped LAZ per site in `output/city101_hub/point_cloud/filtered/`

```json
{
    "pipeline": [
        "raw/site_tile_1.copc.laz",
        "raw/site_tile_2.copc.laz",
        {
            "type": "filters.merge"
        },
        {
            "type": "filters.crop",
            "point": "EPSG:2056 2538000 1153000",
            "distance": 500
        },
        "filtered/site_chuv_500m.laz"
    ]
}
```

**Effort**: 1 hour per site (mostly waiting for processing)
**Automation potential**: High — PDAL pipeline JSON can be generated per site

### Step 3: Filter by classification

**Tool**: PDAL (range filter)
**Input**: Cropped LAZ
**Output**: Separate LAZ files per class (ground, buildings, vegetation)

```bash
# Ground only (terrain mesh input)
pdal translate site.laz site_ground.laz \
  --json '{"pipeline":[{"type":"filters.range","limits":"Classification[2:2]"}]}'

# Buildings only
pdal translate site.laz site_buildings.laz \
  --json '{"pipeline":[{"type":"filters.range","limits":"Classification[6:6]"}]}'

# Vegetation (classes 3, 4, 5)
pdal translate site.laz site_vegetation.laz \
  --json '{"pipeline":[{"type":"filters.range","limits":"Classification[3:5]"}]}'
```

**Effort**: 30 min per site
**Automation potential**: High — identical commands per site

### Step 4: Generate meshes

**Tool**: CloudCompare or PDAL → Grasshopper
**Input**: Filtered LAZ per class
**Output**: Mesh files (OBJ or PLY)

Two approaches:

**A. CloudCompare (recommended for quality)**
1. Load ground LAZ → compute normals → Poisson reconstruction → trim → export OBJ
2. Load building LAZ → compute normals → Poisson reconstruction → export OBJ
3. Each mesh is clean, watertight, and ready for Rhino

**B. Grasshopper Delaunay (faster, terrain only)**
1. Export ground points to CSV
2. Import as point grid in Grasshopper
3. Delaunay Mesh component → terrain mesh
4. Bake to Rhino layer

**Effort**: 1–2 hours per site
**Automation potential**: Medium — CloudCompare is manual; Grasshopper can be scripted

### Step 5: Import to Rhino

**Tool**: Rhino 8
**Input**: OBJ/PLY meshes
**Output**: Layered 3DM file

Layer structure:
```
Site_Name/
├── TERRAIN/          ← ground mesh (class 2)
├── BUILDINGS/        ← building meshes (class 6)
├── VEGETATION/       ← vegetation point cloud or simplified geometry
├── WATER/            ← water surface (class 9)
├── INFRASTRUCTURE/   ← bridges, roads (class 17)
└── CONTEXT/          ← surrounding area at lower detail
```

**Effort**: 30 min per site
**Automation potential**: High via Rhino MCP — can script layer creation and import

### Step 6: Architectural modeling

**Tool**: Rhino + Grasshopper
**Input**: Site model with terrain + buildings + context
**Output**: Intervention design within existing site

This step is human-driven architectural design. Claude Code assists with:
- Generating Rhino scripts for repetitive operations
- Running Grasshopper definitions for parametric variations
- Managing layers and organization

---

## 5. Professional Practice Context

### How architecture firms typically go from site to model

| Phase | Who | Tool | Time | LOD |
|-------|-----|------|------|-----|
| Commission survey | Architect | — | 1 day | — |
| Terrestrial + drone scan | Survey company | Leica/FARO scanner | 1–3 days | Raw |
| Point cloud registration | Surveyor | Cyclone / RealityCapture | 1–2 days | — |
| Cleaning + classification | Surveyor or BIM team | CloudCompare / ReCap | 1–3 days | LOD 100 |
| Mesh generation | BIM modeler | CloudCompare / Rhino | 1–2 days | LOD 200 |
| BIM modeling | BIM team | Revit / Rhino | 1–2 weeks | LOD 300 |
| QA review | Project architect | All | 1–2 days | LOD 300–400 |

**For City101**: We skip the survey step (using swisstopo's existing airborne LiDAR) and go directly to classification → mesh → model. This saves weeks and thousands of CHF.

### LOD/LOG/LOD reference (from 00_Workflow_v04.md)

For the Prototypology project, site models should target:
- **Terrain**: LOD 200 (accurate mesh, 2m resolution sufficient)
- **Buildings**: LOD 100–200 (massing/footprint, not detailed facades)
- **Infrastructure**: LOD 100 (position and basic geometry)
- **Vegetation**: LOD 100 (canopy volumes, not individual trees)

This is achievable entirely from swissSURFACE3D + swissALTI3D without custom surveying.

### Time/cost benchmarks

| Task | Professional firm | City101 (with tools) |
|------|-------------------|---------------------|
| Site survey | CHF 5,000–15,000 | Free (swisstopo open data) |
| Point cloud → classified | 2–5 days | 1–2 hours (already classified) |
| Classified → terrain mesh | 1–2 days | 2–4 hours (PDAL + CloudCompare) |
| Terrain mesh → Rhino site model | 3–5 days | 4–8 hours (with scripts) |
| **Total per site** | **2–3 weeks, CHF 10k–30k** | **1–2 days, CHF 0** |

---

## 6. Agent/Skill/Rule Specifications

### 6.1 Proposed tools (for `tools/`)

#### `tools/pointcloud/download_tiles.py`
- **Input**: Site name, center E/N coordinates, radius
- **Output**: Downloaded COPC/LAZ files to `output/city101_hub/point_cloud/raw/{site}/`
- **Method**: STAC API query → download matching tiles
- **Dependencies**: `requests`

#### `tools/pointcloud/crop_site.py`
- **Input**: Raw tile paths, center coordinates, radius
- **Output**: Single cropped LAZ in `filtered/`
- **Method**: PDAL pipeline (merge + crop)
- **Dependencies**: `pdal` (conda)

#### `tools/pointcloud/filter_by_class.py`
- **Input**: Cropped LAZ path, list of classification codes
- **Output**: Separate LAZ per class in `filtered/`
- **Method**: PDAL range filter
- **Dependencies**: `pdal`

#### `tools/pointcloud/generate_terrain_mesh.py`
- **Input**: Ground-only LAZ path
- **Output**: OBJ mesh in `meshed/`
- **Method**: PDAL → points → Delaunay triangulation (via scipy or PDAL's delaunay writer)
- **Dependencies**: `pdal`, `scipy`, `numpy`

### 6.2 Proposed Rhino skills (via Rhino MCP)

#### Skill: `import-site-model`
- Reads mesh files from `output/city101_hub/point_cloud/meshed/{site}/`
- Creates layer hierarchy (TERRAIN, BUILDINGS, VEGETATION, etc.)
- Imports each mesh to its layer
- Sets display colors per layer

#### Skill: `terrain-from-alti3d`
- Simpler alternative: reads swissALTI3D GeoTIFF
- Creates Grasshopper heightfield mesh
- Imports to TERRAIN layer

### 6.3 Proposed workflow

#### `workflows/point-cloud-to-site-model.md`
```
# Point Cloud to Site Model

## Prerequisites
- PDAL installed (`conda install -c conda-forge pdal`)
- CloudCompare installed
- Site coordinates from prototypology_content.json

## Steps
1. Run `tools/pointcloud/download_tiles.py --site "CHUV" --radius 500`
2. Run `tools/pointcloud/crop_site.py --site "CHUV"`
3. Run `tools/pointcloud/filter_by_class.py --site "CHUV" --classes 2 6 9 17`
4. Open ground.laz in CloudCompare → Poisson reconstruction → export OBJ
   (OR run `tools/pointcloud/generate_terrain_mesh.py --site "CHUV"`)
5. Use Rhino MCP `import-site-model` skill to load meshes
6. Verify against map.geo.admin.ch aerial imagery
```

### 6.4 Proposed rules addition

Add to `.claude/rules/`:

```markdown
## Point cloud data
- All point cloud data stays in EPSG:2056 (LV95) + LHN95 heights
- Raw downloads go to output/city101_hub/point_cloud/raw/ (never modify)
- Processed files go to output/city101_hub/point_cloud/filtered/
- Meshes go to output/city101_hub/point_cloud/meshed/
- Always document: source tile IDs, point counts, processing parameters
- Subsample to <5M points before Rhino import
- swissSURFACE3D classification is authoritative — do not reclassify
```

---

## 7. Effort Estimates

| Task | Effort | Blocks on |
|------|--------|-----------|
| Install PDAL (`conda install`) | 15 min | Nothing |
| Install CloudCompare | 15 min | Nothing |
| Build `download_tiles.py` tool | 2–3 hours | STAC API testing |
| Build `crop_site.py` tool | 1–2 hours | PDAL install |
| Build `filter_by_class.py` tool | 1 hour | PDAL install |
| Build `generate_terrain_mesh.py` tool | 2–3 hours | PDAL install |
| Download tiles for all 7 sites | 1–2 hours (network) | download tool |
| Process all 7 sites (crop + filter + mesh) | 4–6 hours | processing tools |
| Import all 7 site models to Rhino | 2–3 hours | Rhino MCP |
| **Total pipeline build** | **~15–20 hours** | — |
| **Total per-site processing (after tools built)** | **~2–3 hours** | — |

---

## 8. MCP Server Availability

| MCP Server | Exists? | Maturity | Useful for City101? |
|------------|---------|----------|-------------------|
| **Rhino MCP** | Yes (configured in project) | Production | Yes — import meshes, create layers, run scripts |
| **QGIS MCP** | Yes (`jjsantos01/qgis_mcp`) | Functional | Maybe — visualize point clouds with GIS context |
| **CloudCompare MCP** | Demo (`truebelief/CloudCompareMCP`) | Experimental | Not yet — requires heavy customization |
| **PDAL MCP** | No | — | Would be valuable but PDAL CLI is sufficient |

**Recommendation**: Use Rhino MCP (already set up) for the import/modeling steps. Use PDAL via command line for preprocessing. CloudCompare stays manual for now. Consider QGIS MCP only if you need GIS overlay visualization.

---

## 9. Recommended Next Steps (Priority Order)

### Immediate (this week)

1. **Install PDAL** — `conda install -c conda-forge pdal python-pdal` or `brew install pdal`
2. **Test STAC API** — manually download one tile for one site (e.g., CHUV at E 2539, N 1153) to verify the download pipeline works
3. **Open test tile in CloudCompare** — verify classification codes match expectations, visualize the data

### Short-term (next 1–2 weeks)

4. **Build `download_tiles.py`** — automate STAC API downloads for all 7 sites
5. **Build `crop_site.py` + `filter_by_class.py`** — automate preprocessing
6. **Process one pilot site** (suggest CHUV — densest, most complex) end-to-end through the full pipeline
7. **Import pilot site to Rhino** via MCP and validate

### Medium-term (2–4 weeks)

8. **Process remaining 6 sites** — batch run all tools
9. **Build Rhino import skill** — automate layer creation and mesh import
10. **Create `workflows/point-cloud-to-site-model.md`** — document the proven workflow

### Consider but deprioritize

11. **QGIS MCP setup** — only if GIS overlay adds value beyond what map.geo.admin.ch provides
12. **CloudCompare MCP** — only if CloudCompare becomes a bottleneck (manual meshing for 7 sites is manageable)
13. **swissALTI3D alternative** — simpler terrain-only path if full point cloud is overkill for some sites
14. **Custom classification / ML** — not needed unless swisstopo's classification proves insufficient at specific sites

---

## 10. Alternative Quick Path: swissALTI3D + swissTLM3D

If full point cloud processing proves too time-consuming for the studio timeline, there is a faster alternative:

```
swissALTI3D (2m GeoTIFF) → Grasshopper heightfield → terrain mesh
swissTLM3D (GeoPackage)  → QGIS export → footprints + heights → Rhino extrude
```

This gives you terrain + building massing without any point cloud processing. Resolution is lower but adequate for LOD 100–200 site models. Can be done in a single afternoon per site.

**The point cloud pipeline is better** because it gives you:
- Precise roof geometry (not just extruded footprints)
- Vegetation canopy
- Infrastructure details (bridges, retaining walls)
- Higher accuracy terrain under buildings

But the quick path exists as a fallback.

---

## Sources

- [swissSURFACE3D — swisstopo](https://www.swisstopo.admin.ch/en/height-model-swisssurface3d)
- [swissSURFACE3D milestone and future plans](https://www.swisstopo.admin.ch/en/swisssurface3d-milestone-achieved-and-course-set-for-the-future)
- [swissSURFACE3D on opendata.swiss](https://opendata.swiss/en/dataset/swisssurface3d-die-klassifizierte-punktwolke-der-schweiz)
- [STAC API — data.geo.admin.ch](https://data.geo.admin.ch/api/stac/v0.9/collections/ch.swisstopo.swisssurface3d)
- [STAC API documentation — geo.admin.ch](https://www.geo.admin.ch/en/rest-interface-stac-api/)
- [Cockroach plugin — food4rhino](https://www.food4rhino.com/en/app/cockroach)
- [Cockroach documentation — IBOIS EPFL](https://ibois-epfl.github.io/Cockroach-documentation/)
- [Cockroach GitHub](https://github.com/9and3/Cockroach)
- [Volvox — food4rhino](https://www.food4rhino.com/en/app/volvox)
- [Rhino 8 E57 import documentation](https://docs.mcneel.com/rhino/8/help/en-us/fileio/e57_import.htm)
- [Point Clouds and Rhino — NExT Lab Melbourne](https://ms-kb.msd.unimelb.edu.au/next-lab/3d-scanning/guides/working-with-3d-scan-data/point-clouds-and-rhino)
- [CloudCompare MCP demo — GitHub](https://github.com/truebelief/CloudCompareMCP)
- [QGIS MCP — GitHub](https://github.com/jjsantos01/qgis_mcp)
- [Native Point Cloud Processing in QGIS — Lutra Consulting](https://www.lutraconsulting.co.uk/blogs/native-point-cloud-processing-in-qgis)
- [PDAL — Point Data Abstraction Library](https://pdal.io/)
- [PDAL wrench — GitHub](https://github.com/PDAL/wrench)
- [Colorize swissSURFACE3D tutorial — GitHub](https://github.com/CharlesGaydon/Colorize-SwissSURFACE3D-Lidar)
- [Terrain Modeling in Grasshopper — Brendan Harmon](https://baharmon.github.io/terrain-modeling-in-grasshopper)
- [ASPRS LAS classification codes](https://lidarvisor.com/lidar-classification-codes/)
- [LAS 1.4 Specification — ASPRS](https://www.asprs.org/a/society/committees/lidar/LAS_1-4_R6.pdf)
- [Open3D point cloud segmentation](https://www.open3d.org/2019/01/16/on-point-clouds-semantic-segmentation/)
