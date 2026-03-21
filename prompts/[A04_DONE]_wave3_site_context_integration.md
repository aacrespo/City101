# Wave 3: Site Context Integration — Locks onto Real Terrain

**Branch:** `andrea/prototypology-v2`
**Rhino needed:** YES — open Rhino with MCP addon before starting
**Duration:** ~1 session
**Depends on:** Wave 1 (terrain data) + Wave 2 (tested scripts)
**Commit prefix:** `[MODEL]`

---

## Goal

Place the 3 tested lock scripts onto their real site terrain with surrounding building context. This is the soft launch of the prototypology workflow: can we go from data → site model → architectural intervention in one session?

The scripts currently generate geometry at origin. This wave:
1. Imports real terrain (swissALTI3D)
2. Imports real buildings (swissBUILDINGS3D LOD2)
3. Imports 2D context (roads, rail)
4. Places each lock at its actual position on the terrain
5. Validates the workflow end-to-end

---

## Pre-flight

1. Confirm Rhino is open and MCP is connected (`get_document_summary`)
2. Confirm units are **Meters** (not Millimeters)
3. Read:
   - Lock concepts: `output/city101_hub/prototypology_content.json` (node coords, lock types)
   - Script test log: `output/city101_hub/script_test_log.md` (known issues)
   - Site modeling handoff: `output/city101_hub/site_modeling/HANDOFF.md` (data inventory)

---

## Site data inventory

Everything is in `output/city101_hub/`. Verify these files exist before starting:

### Terrain (in `terrain/`)
| Site | XYZ grid | Summary |
|------|----------|---------|
| Morges | `city101_node3_morges_swissalti3d_2021_2527-1151_2_2056_5728_xyz.csv` | 250k pts, 365–413m |
| CHUV | `city101_node5_chuv_swissalti3d_2021_2538-1152_2_2056_5728_xyz.csv` | 250k pts, 445–577m |
| Rennaz | `city101_node7_rennaz_swissalti3d_2019_2560-1137_2_2056_5728_xyz.csv` | 250k pts, 372–381m |

### Buildings 3D (in `context/`)
| Site | File | Notes |
|------|------|-------|
| Morges | `city101_node3_morges_swissbuildings3d.dxf.zip` | Unzip first → DXF, LOD2 |
| CHUV | `city101_node5_chuv_swissbuildings3d.dxf.zip` | Unzip first → DXF, LOD2. Large (199MB extracted) |
| Rennaz | `city101_node7_rennaz_swissbuildings3d.dxf.zip` | Unzip first → DXF, LOD2 |

### 2D context (in `terrain/`)
| Site | DXF file |
|------|----------|
| Morges | `city101_node3_morges_context.dxf` |
| CHUV | `city101_node5_chuv_context.dxf` |
| Rennaz | `city101_node7_rennaz_context.dxf` |

---

## Workflow — do one site first (CHUV recommended)

CHUV is the most complex (steep terrain, dense buildings, 132m elevation change in the tile). If the workflow works here, it works everywhere.

### Step 1: Create layer hierarchy

```
CHUV_Site/
  TERRAIN/           [160, 150, 130]  earth brown
  BUILDINGS_3D/      [180, 180, 175]  warm grey
  ROADS/             [120, 120, 120]  mid grey
  RAIL/              [80, 80, 80]     dark grey
  CONTEXT_2D/        [200, 200, 195]  light grey
Lock_05/
  (existing sublayers from script — Volumes, Structure, etc.)
```

### Step 2: Import terrain

Read `city101_node5_chuv_swissalti3d_2021_2538-1152_2_2056_5728_xyz.csv` and create a terrain mesh on the TERRAIN layer.

The CSV has columns: X, Y, Z (LV95 coordinates, meters).
- Full tile is 1km x 1km (500x500 grid at 2m spacing)
- For Rhino performance: consider subsampling to every 4th point (125x125 = ~15k pts) for initial test
- Create mesh via Delaunay triangulation or patch surface

**Coordinate decision — IMPORTANT:**
The XYZ data is in full LV95 (E ~2,538,000, N ~1,152,000). Working at these coordinates in Rhino causes floating-point precision issues far from origin.

Two options:
- **A. Offset to local origin** — subtract site center (E 2538500, N 1152500) so terrain centers at (0,0). Simpler for modeling. Document the offset.
- **B. Keep LV95** — all data aligns automatically but Rhino viewport may have precision artifacts.

**Recommend Option A.** Store the offset in the file as metadata/text dot.

### Step 3: Import buildings

The swissBUILDINGS3D DXF must be unzipped first (if not already). Then import into Rhino on the BUILDINGS_3D layer.

If using Option A (local origin): the DXF also comes in LV95, so apply the same offset after import — select all imported objects and `Move` by (-2538500, -1152500, 0).

### Step 4: Import 2D context

Import `city101_node5_chuv_context.dxf` — contains roads, rail, building outlines as 2D polylines. Place on CONTEXT_2D layer. Apply same offset if using Option A.

### Step 5: Crop to 500m radius

The terrain tile is 1km x 1km but the site radius is 500m. After import:
1. Create a circle at (0, 0) radius 500m (if using local origin)
2. Use it as a visual boundary
3. Optionally trim/delete geometry outside the circle for performance

### Step 6: Place the lock

The lock scripts currently generate geometry at origin. Two approaches:

**A. Run script then move:**
1. Run `lock_05_chuv_gradient_v2.py` (the fixed version from Wave 2)
2. Select all Lock_05 objects
3. Move to the correct position on the terrain
4. The lock should sit at the CHUV campus location

**B. Modify script to accept site coordinates:**
1. Add a `SITE_ORIGIN` parameter to the script header
2. Offset all geometry by `SITE_ORIGIN` during creation
3. This is the template pattern we want for the prototypology app

**Recommend approach B** — it's more work now but establishes the reusable pattern.

### Step 7: Validate

- [ ] Terrain mesh looks correct (no holes, reasonable elevation)
- [ ] Buildings sit on terrain (not floating, not buried)
- [ ] Lock geometry sits at a reasonable position on the site
- [ ] Scale feels right (lock footprint vs surrounding buildings)
- [ ] Roads/rail align with terrain and buildings
- [ ] Layer organization is clean

Capture viewports:
1. **Top** — plan view showing lock in site context (zoom to fit)
2. **Perspective** — 3/4 view showing terrain, buildings, and lock together
3. **Side/section** — showing how lock meets terrain slope (especially important for CHUV's gradient)

---

## After CHUV: repeat for Morges and Rennaz

Apply the same workflow. Each site will surface different issues:
- **Morges** — flat terrain, simpler. Good sanity check.
- **Rennaz** — nearly flat (372-381m), isolated hospital. Tests the "bridge" concept on real ground.

---

## What to document

Write to `output/city101_hub/site_modeling/wave3_integration_log.md`:

For each site:
- Steps taken, any errors
- Coordinate offset used
- Screenshot descriptions (3 views minimum)
- What worked, what didn't
- Performance notes (how heavy is the model?)

Cross-site:
- Is the workflow repeatable? How long per site?
- What should be automated for the remaining 4 sites?
- Does the lock geometry make sense at real scale on real terrain?
- Any script modifications needed?

---

## Deliverables

1. `output/city101_hub/site_modeling/wave3_integration_log.md` — process log
2. Updated lock scripts (if modified for site placement) → `rhino_scripts/lock_*_v3.py`
3. Commit: `[MODEL] Wave 3 — 3 locks placed on real site terrain`

---

## Reference files
- Modeling workflow: `workflows/rhino-modeling.md`
- LOG levels: `00_Workflow_v04.md` Section 3.2
- Lock concepts: `output/city101_hub/prototypology_content.json`
- Script test log: `output/city101_hub/script_test_log.md`
- Site modeling handoff: `output/city101_hub/site_modeling/HANDOFF.md`
- Pipeline research: `output/city101_hub/point_cloud_pipeline_research.md`
