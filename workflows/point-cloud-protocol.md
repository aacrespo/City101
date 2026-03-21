# Point Cloud Protocol

Conventions for handling LiDAR and point cloud data in the City101 project.

## File Formats

| Format | Extension | Use |
|--------|-----------|-----|
| LAS | .las | Raw point cloud (uncompressed) |
| LAZ | .laz | Raw point cloud (compressed) — preferred for storage |
| E57 | .e57 | Exchange format, some Rhino importers prefer this |
| PLY | .ply | Mesh/point cloud, good for CloudCompare ↔ Rhino |

## CRS

All point cloud data must be in **Swiss LV95 / EPSG:2056**. If source data is in a different CRS, convert before any processing.

## Classification Codes (ASPRS LAS Standard)

| Code | Class | Relevant? |
|------|-------|-----------|
| 2 | Ground | Yes — terrain mesh |
| 3 | Low vegetation | Maybe — landscape context |
| 4 | Medium vegetation | Maybe — tree canopy |
| 5 | High vegetation | Maybe — tree canopy |
| 6 | Building | Yes — building extraction |
| 9 | Water | Yes — lake/river context |
| 10 | Rail | Yes — rail corridor |
| 11 | Road surface | Yes — road context |
| 17 | Bridge deck | Yes — infrastructure |

## Storage

```
output/city101_hub/point_cloud/
├── raw/          ← downloaded LAS/LAZ (never modify)
├── filtered/     ← classified/cropped subsets
├── meshed/       ← terrain meshes, building meshes
└── metadata/     ← processing logs, source info
```

## Rules

1. **Never modify raw point cloud files.** Work on copies in `filtered/`.
2. **Document provenance**: source, download date, tile ID, CRS, point count.
3. **Crop before processing**: extract only the 500m radius around each site.
4. **Classify before meshing**: ground points → terrain mesh, building points → building mesh.
5. **Validate coordinate ranges** after any transform:
   - LV95 E: 2'496'000–2'565'000
   - LV95 N: 1'130'000–1'155'000

## Data Sources

| Source | What | Format | Resolution |
|--------|------|--------|------------|
| swissSURFACE3D | Classified LiDAR | LAZ | ~20 pts/m² |
| swissALTI3D | Digital terrain model | GeoTIFF | 2m grid |
| TLM3D | Topographic landscape model | GPKG | Vector + heights |

## Pipeline (reference)

```
Raw LAZ → crop to site → classify → filter by class → mesh → export to Rhino
```

Each step should be a separate tool or script. Document which tool was used and with what parameters.
