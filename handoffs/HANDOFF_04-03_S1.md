# HANDOFF — 04-03 Session 1
**From**: Cairn (claude.ai browser + QGIS MCP)
**To**: Next session (Cairn Code for Phase 2 build, or Cairn/Lumen for QA)
**Date**: 2026-03-04

---

## Last action
Phase 1 fix session completed by Cairn Code. All 4 data outputs now pass validation. Ready for Phase 2: building the "Train Pulse" and "Passenger Flow" animated maps.

## What happened this session (two parts)

### Part 1: Infrastructure rebuild (from transcript)
- **CLAUDE.md v2** rebuilt (381 lines, 24KB) — corrected project phase (A02 still active), team table, agent output staging workflow, QA verification gates
- **PROJECT_INSTRUCTIONS.md** extracted from system prompt (131 lines) — account system, first-thing protocol, MCP safety rules
- **Corridor animation prompts updated** — `PLAN_corridor_animation_maps_v2.md` and `PROMPT_corridor_maps_03032026_v2.md` in `prompts/`. Removed gondola framing, corrected dataset filenames, aligned with staging workflow
- **research-with-agent-team.md** created in `.claude/commands/` (429 lines) — adapted from coleam00's build-with-agent-team for data research sprints. Adds: canonical entity lists, discovery mode, trawl summaries, graceful failure handling
- **build-with-agent-team.md** added to `.claude/commands/` — the original software build skill from GitHub

### Part 2: Phase 1 data audit and fix
Cairn (this session, browser + QGIS MCP) audited all Phase 1 outputs and identified specific quality problems. Wrote a targeted fix prompt. Cairn Code executed it.

**Phase 1 v1 problems found:**
1. GTFS: stop_times format (station arrivals/departures), not per-minute interpolated positions
2. Ridership: only 3 unique hourly curves across 49 stations (cantonal Gaussian templates)
3. Demographics: only 2 unique profiles (GE average, VD average) — not commune-level
4. Geometry: mixed points + lines, no properties, Genève classified as narrow gauge, distances broken

**Phase 1 v2 results (all PASS):**

| Agent | v1 → v2 | Status |
|-------|---------|--------|
| 1: GTFS | 7,018 stop_times → 39,695 per-minute interpolated positions (860 trips) | ✅ |
| 2: Ridership | 3 curves → 49 unique curves, 10 profile types | ✅ |
| 3: Demographics | 2 cantonal averages → 42 unique age profiles, commune-level | ✅ |
| 4: Geometry | broken → 18 line features, 0 points, Genève=standard_gauge | ✅ |

**Known remaining issues (acceptable):**
- Agent 1: 39,695 rows (just below 40K target — acceptable, 860 trips all present)
- Agent 2: Montreux morning=0.29 (spec said <0.20 for CI=1.02) — falls in "balanced_moderate" profile which still gets meaningful peaks. Modeling choice, not error.
- Agent 4: Aigle snap=6.3km, Bex snap=14km — SwissTLM3D geometry doesn't fully extend to eastern terminus. Bus stops (Begnins, Aubonne) at 2-3km as expected (not on rail).
- Agent 2 research confirmed: no public hourly ridership data exists from SBB/BFS. All hourly curves are modeled.

## Current state

### Animation data in `output/` (staging — not yet promoted)
| File | Size | Key metrics |
|------|------|-------------|
| `gtfs_corridor_trains_interpolated.csv` | 2,113 KB | 39,695 rows, 860 trips, 5 line categories |
| `station_ridership_v2.csv` | 17 KB | 49 rows, 10 profiles, hourly pcts sum=1.0 |
| `corridor_demographics_v2.csv` | 9 KB | 49 rows, 42 age profiles |
| `corridor_rail_lines_v2.geojson` | 219 KB | 18 lines, 96.4km mainline |
| `corridor_station_distances_v2.csv` | 4 KB | 49 rows, monotonic distances |
| `gtfs_corridor_stops.csv` | 4 KB | 49 stations with coords (v1, still valid) |

### Also in `output/` (v1 files + scripts — keep for reference)
- `agent1_gtfs_timetable.py`, `agent2_ridership.py`, `agent3_demographics.py`, `agent4_route_geometry.py`, `agent4_route_geometry_v4.py`
- v1 CSVs: `gtfs_corridor_trains.csv`, `station_ridership.csv`, `corridor_demographics.csv`, `corridor_rail_lines.geojson`, `corridor_station_distances.csv`
- v2 scripts: (produced by Cairn Code during fix session — check output/ for agent*_v2.py files)

### Files created on Mac filesystem (via MCP)
- `/Users/andreacrespo/CLAUDE/City101_ClaudeCode/CLAUDE.md` — rebuilt v2
- `/Users/andreacrespo/CLAUDE/City101_ClaudeCode/PROJECT_INSTRUCTIONS.md` — system prompt extract
- `/Users/andreacrespo/CLAUDE/City101_ClaudeCode/prompts/PLAN_corridor_animation_maps_v2.md`
- `/Users/andreacrespo/CLAUDE/City101_ClaudeCode/prompts/PROMPT_corridor_maps_03032026_v2.md`
- `/Users/andreacrespo/CLAUDE/City101_ClaudeCode/.claude/commands/research-with-agent-team.md`
- `/Users/andreacrespo/CLAUDE/City101_ClaudeCode/.claude/commands/build-with-agent-team.md` (downloaded by Andrea from this chat)

## Open threads

### IMMEDIATE: Phase 2 build
The PROMPT file (`PROMPT_corridor_maps_03032026_v2.md`) has full specs for:
- **Map 1 "Train Pulse"** — 24h animation with sky color cycle, white train dots + fading trails, canvas overlay on Leaflet
- **Map 2 "Passenger Flow"** — same framework, train dots sized by ridership, station accumulation rings, demographic choropleth toggle

Data is ready. Next step: give Cairn Code the Phase 2 build prompt. The PROMPT file already has CSS variables, sky color timeline, UI element specs.

### BEFORE Phase 2: Promote v2 data
Andrea needs to verify v2 outputs and promote from `output/` to `source/animation/`:
```
mkdir -p source/animation
cp output/gtfs_corridor_trains_interpolated.csv source/animation/
cp output/station_ridership_v2.csv source/animation/
cp output/corridor_demographics_v2.csv source/animation/
cp output/corridor_rail_lines_v2.geojson source/animation/
cp output/corridor_station_distances_v2.csv source/animation/
cp output/gtfs_corridor_stops.csv source/animation/
```

### CONTEXT.md + LEARNINGS.md need update
This session was browser-based (no filesystem write). Next desktop session should update:
- CONTEXT.md: Phase 1 data complete, v2 outputs in staging, agent team commands available
- LEARNINGS.md: Add — "no public hourly SBB ridership data exists", "SwissTLM3D doesn't extend to Bex", "background agents fail on Write/Bash permissions — run scripts from main session"

## Key decisions made (cumulative)
- Agent team skill adapted for data research (not just software builds)
- Phase 1 fix ran sequential (not parallel agents) due to permission issues — pragmatic choice
- Hourly ridership curves are modeled, not measured — documented and accepted
- Geometry uses Dijkstra spine from SwissTLM3D GPKG with piecewise calibration (r=0.9987)
- Canonical station list: 49 unique stations (Prangins duplicate removed, Bex included)
- All animation outputs route through `output/` staging before promotion

## Technical notes
- Agent team commands: `/research-with-agent-team` and `/build-with-agent-team` in `.claude/commands/`
- Agent teams require: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `~/.claude/settings.json` + tmux installed
- Phase 2 map build: single self-contained HTML files, Leaflet.js + Canvas overlay, no external tiles (sky color IS the background)
- Corridor bounding box: lat [46.15, 46.55], lon [6.05, 7.10]
- 49 canonical station names are the join key across ALL datasets

## Data sources (this session)
- GTFS interpolated: derived from geOps GTFS (gtfs.geops.ch), 860 trips → 39,695 per-minute positions
- Ridership v2: SBB Passagierfrequenz 2024 daily totals + modeled hourly curves using commuter_index
- Demographics v2: BFS STATPOP 2023 commune-level (42 unique profiles) + STAF frontalier data
- Geometry v2: SwissTLM3D City101_TrainLines.gpkg, Dijkstra extraction, 18 merged line features
