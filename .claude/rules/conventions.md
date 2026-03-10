# Conventions

## Coordinate system
- **Always Swiss LV95 / EPSG:2056** for spatial work and QGIS.
- Convert WGS84 ↔ LV95 using pyproj (or `tools/data/convert_coordinates.py`).
- QGIS project CRS: EPSG:2056.
- Web maps (Leaflet): WGS84 / EPSG:4326.

## Commit prefixes
| Prefix | Used by | Meaning |
|--------|---------|---------|
| `[DATA]` | Analyst | New or updated dataset |
| `[FIND]` | Analyst | Discovery worth noting |
| `[DEAD]` | Analyst | Dead end documented |
| `[MAP]` | Cartographer | Map or spatial output |
| `[VIZ]` | Visualizer | Visualization or chart |
| `[MODEL]` | Modeler | 3D model or geometry |
| `[BUILD]` | Builder | Deployment or packaging |
| `[SYNC]` | session-end | Context/lockboard update |

## File safety — CRITICAL
- **NEVER modify or overwrite original files.** Always write to a new path.
- **NEVER delete any file or directory.**
- **Ask before ANY filesystem write** — state the exact path and what will be written.
- Prefix all new data files with `city101_`.
- Version suffixes (`_v2`, `_v3`) when iterating on existing files.

## File naming
- Data files: `city101_[topic]_[detail].csv`
- GeoJSON: `city101_[topic].geojson`
- Visualizations: `viz_[NN]_[name].html`
- Scripts: descriptive, snake_case
