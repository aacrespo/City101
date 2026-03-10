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

## Git workflow

### Commit as you go
- Commit after each logical piece of work (finished a script, added a dataset, updated a viz).
- Use the correct prefix from the table above.
- `/session-end` catches anything still uncommitted — but don't rely on it as the only commit.

### Branch naming
- `andrea/[topic]` — Andrea's work-in-progress branches
- `henna/[topic]` — Henna's work-in-progress branches
- `test/[topic]` — throwaway test branches
- Use branches for: WIP code, big changes needing review, anything you want the other person to look at before merging.
- Push directly to main for: doc updates, lockboard, context, small verified changes.

### Visual work (gitignored files)
PNG, PDF, PPTX, QGZ, and other large binaries live on Google Drive, not in git.
For each visual deliverable, create a placeholder markdown in the same directory:
```
deliverables/A03/map_relay_lock.md    ← placeholder (tracked in git)
deliverables/A03/map_relay_lock.png   ← actual file (on Drive, gitignored)
```
The placeholder should contain: description, Drive location, last updated date, who made it.
This way the git log tracks when visuals were created/updated, and anyone can find them.

### output/ directory
Keep pushed to remote. Serves as a shared staging area — either person can review and promote files from output/ to their proper location.
