# Wave 1 Research Review — Reconsidering the Pipeline

**Branch:** `andrea/prototypology-v2`
**Context:** Wave 1 research is complete but uncommitted. Review before committing.

---

## Background

Wave 1 produced:
- 3 DXF site extracts (buildings 2D, rail, roads) in `output/city101_hub/terrain/`
- 3 swissALTI3D GeoTIFF tiles downloaded
- 3 metadata JSONs in `output/city101_hub/context/`
- Pipeline research: `output/city101_hub/point_cloud_pipeline_research.md`

Key finding: **No building heights** in any GeoPackage — all footprints are 2D only. The research recommended either swissBUILDINGS3D 2.0 (free, CityGML LOD2) or point cloud extrusion from swissSURFACE3D.

## New context from yesterday's crit

The studio (Huang) offered to help with tools if needed. This means **spending some money on paid tools/services might be on the table** — the original research assumed CHF 0 budget.

## What to discuss

1. **Read the pipeline research** at `output/city101_hub/point_cloud_pipeline_research.md` — understand the free vs paid options
2. **Reconsider the pipeline** now that budget is possible:
   - Are there paid tools/plugins that dramatically simplify the LiDAR → Rhino workflow?
   - Would a paid Grasshopper plugin (e.g., Elk, Heron, Urbano) skip days of manual work?
   - Cloud processing services for point clouds?
   - Any paid swisstopo products worth it, or is OGD sufficient?
3. **Compare**: free pipeline (STAC → PDAL → CloudCompare → Rhino) vs paid alternatives — time, quality, reliability
4. **Recommend** which route to take given that some budget exists but this is still a student project

## After discussion

- Update the research doc with any new findings or revised recommendations
- Commit all Wave 1 outputs (they've been sitting uncommitted)
- Commit prefix: `[DATA] Terrain + point cloud research for 3 lock sites`
