# HANDOFF — 04-03 Session 2
**From**: Cairn (claude.ai browser + QGIS MCP)
**To**: Cairn Code (Phase 2 build)
**Date**: 2026-03-04

---

## Last action
QA-verified all Phase 1 v2 outputs via QGIS MCP (read actual CSVs, not just Cairn Code's summary). Found Agent 4 geometry had 3 problems: distances capped at 69.5km (should be ~105), 7 stations snap >500m, Léman Express misclassified as narrow_gauge. Wrote self-contained fix prompt. Cairn Code produced v3 geometry — all 3 issues resolved. Phase 1 data now fully validated and ready for Phase 2 build.

## What happened today (3 parts)

### Part 1: Infrastructure rebuild (Cairn Code, from transcript)
- **CLAUDE.md v2** rebuilt (381 lines, 24KB) — corrected project phase, team table, agent output staging workflow, QA verification gates
- **PROJECT_INSTRUCTIONS.md** extracted from system prompt (131 lines)
- **Corridor animation prompts** updated in `prompts/` — `PLAN_corridor_animation_maps_v2.md` + `PROMPT_corridor_maps_03032026_v2.md`
- **research-with-agent-team.md** created in `.claude/commands/` (429 lines) — adapted for data research
- **build-with-agent-team.md** added to `.claude/commands/` — original software build skill

### Part 2: Phase 1 v2 fix (Cairn Code)
Agents 1-4 rewritten. Cairn Code ran all 4 scripts sequentially (background agents failed on permissions — lesson learned).

### Part 3: QA + v3 geometry fix (this session, Cairn browser + QGIS MCP)
- Read every v2 output file directly via QGIS Python (not trusting summaries)
- Agents 1-3: genuine pass on all validation checks
- Agent 4: identified 3 problems, wrote `FIX_AGENT4_GEOMETRY.md` prompt
- Cairn Code produced v3: distances 0–105km, snap classifications, CEVA reclassified
- Root cause on distances: v2 calibrated against GA cost estimates that diverge from SBB km-posts east of Lausanne

## Phase 1 Final Status — ALL PASS

| File | Rows | Key Validation | Version |
|------|------|----------------|---------|
| `gtfs_corridor_trains_interpolated.csv` | 39,695 | 860 trips, 0 minute gaps, coords valid, 5 line categories | v2 |
| `station_ridership_v2.csv` | 49 | 49 unique curves, 10 profiles, all sums=1.0 | v2 |
| `corridor_demographics_v2.csv` | 49 | 42 unique age profiles, all commune-level, no placeholders | v2 |
| `corridor_rail_lines_v3.geojson` | 19 features | 0 points, CEVA feature (32.1km), Genève=standard_gauge | v3 |
| `corridor_station_distances_v3.csv` | 49 | 0–105km, Aigle≠Bex, monotonic, snap quality classified | v3 |
| `gtfs_corridor_stops.csv` | 49 | Station coords (unchanged from v1) | v1 |

### Known acceptable limitations
- Ridership hourly curves are **modeled** (Gaussian mixtures using commuter_index), not measured. No public hourly SBB data exists.
- Demographics: BFS STATPOP commune-level is real. Commute mode may still be Strukturerhebung estimates.
- Geometry: Bex snap=14km, Aigle snap=6.3km — SwissTLM3D literally doesn't have rail geometry there. Flagged as `original_coords_used`.
- Montreux morning peak=0.29 (spec said <0.20 for CI=1.02) — modeling choice, not error.

## Current file state

### Phase 1 outputs in `output/` (staging — NOT yet promoted)
```
output/
├── gtfs_corridor_trains_interpolated.csv  (2,113 KB)
├── gtfs_corridor_stops.csv                (4 KB)
├── station_ridership_v2.csv               (17 KB)
├── corridor_demographics_v2.csv           (9 KB)
├── corridor_rail_lines_v3.geojson         (219 KB)
├── corridor_station_distances_v3.csv      (4 KB)
├── agent1_interpolation.py
├── agent2_ridership_v2.py
├── agent3_demographics_v2.py
├── agent4_geometry_v2.py
├── agent4_geometry_v3.py
└── [v1 files kept for reference]
```

### `source/animation/` DOES NOT EXIST YET
Data must be promoted before Phase 2. See promotion commands below.

### Existing visualizations in `visualizations/`
viz_01 through viz_08 + clock/marey/spacetime diagrams — all intact from 01-03/02-03 sessions.

### "Still on the Line" scrollytelling site
`index_v2.html` with 7 interactive Leaflet maps — complete as of HANDOFF_02-03_S1.

### QGIS project
`CITY101_WORKING.qgz` — 60 layers, EPSG:2056

## Before Phase 2: Promote data

```bash
cd ~/CLAUDE/City101_ClaudeCode
mkdir -p source/animation
cp output/gtfs_corridor_trains_interpolated.csv source/animation/
cp output/gtfs_corridor_stops.csv source/animation/
cp output/station_ridership_v2.csv source/animation/
cp output/corridor_demographics_v2.csv source/animation/
cp output/corridor_rail_lines_v3.geojson source/animation/
cp output/corridor_station_distances_v3.csv source/animation/
```

## CONTEXT.md + LEARNINGS.md need update
This session was browser-based (no direct filesystem write to those files). Next desktop session should update:
- **CONTEXT.md**: Phase 1 data complete, v2/v3 outputs in staging, agent team commands available, 8 existing visualizations
- **LEARNINGS.md**: Add — "no public hourly SBB ridership data exists", "SwissTLM3D doesn't extend to Bex/Aigle", "background agents fail on Write/Bash permissions", "v2 GA cost calibration diverges from SBB km-posts east of Lausanne"

## Key decisions made (cumulative)
- Narrative: "Infrastructure for working continuity as a flow" (teacher-endorsed 24-02)
- Corridor is an archipelago (11/49 stations maintain continuity)
- Two corridors on same tracks (IC vs S-Bahn experience)
- Diversity creates unity (quadruple-validated, Shannon phase transition at ~1.0)
- 160,000 ghost citizens (frontaliers exceed Lausanne population)
- Agent team skill adapted for data research (not just software builds)
- Phase 1 fix ran sequential due to permission issues — pragmatic choice
- All animation outputs route through `output/` staging before promotion
- Hourly ridership = modeled, documented and accepted
- Geometry v3 uses SBB km-post benchmarks instead of GA cost calibration for eastern corridor

## Technical notes
- Agent team commands: `/research-with-agent-team` and `/build-with-agent-team` in `.claude/commands/`
- Phase 2 maps: single self-contained HTML files, Leaflet.js + Canvas overlay, sky color = background
- PROMPT file: `prompts/PROMPT_corridor_maps_03032026_v2.md` — has full Phase 2+3 spec with CSS variables, sky timeline, UI elements
- Corridor bounding box: lat [46.15, 46.55], lon [6.05, 7.10]
- 49 canonical station names are the join key across ALL datasets
- Coordinate system: WGS84 for web maps, LV95 columns kept in CSVs for QGIS

## Data sources (this session)
- GTFS interpolated: geOps GTFS → 860 trips → 39,695 per-minute positions (verified)
- Ridership v2: SBB 2024 daily totals + modeled hourly curves (verified, 49 unique)
- Demographics v2: BFS STATPOP 2023 commune-level (verified, 42 unique profiles)
- Geometry v3: SwissTLM3D + SBB km-post calibration (verified, 0–105km)
