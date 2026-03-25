# HANDOFF — 01-03 Session 2 (Cairn, desktop MCP)

## Last action
Loaded all datasets into new QGIS project (`CITY101_WORKING.qgz`, 48 layers). Executed the dark data trawl from `opendata_trawl_categorized.md` — added 14 WMS layers (noise, EV 2035 projections, home charging), fetched shared mobility API (2,062 corridor stations), downloaded national charging key figures (63 months). CONTEXT.md updated.

## What happened this session
1. Bridged opening hours CSV from container to Mac filesystem (base64 via QGIS Python)
2. Duplicated `~/Downloads/CITY101_TESTS.qgz` → `~/CLAUDE/City101_ClaudeCode/CITY101_WORKING.qgz`
3. Loaded 7 data CSV layers (EV, WiFi, remote work, transport frequency, ridership, cell towers, intl anchors)
4. Removed broken EV_Charging_Stations layer (0 features)
5. Added 14 WMS layers from geo.admin.ch (noise day/night for rail+road, rail immission, EV 2035 x3, home charging x3, fleet, electricity demand)
6. Fetched sharedmobility.ch API → `city101_shared_mobility.csv` (2,062 corridor stations, 8 providers)
7. Downloaded `swiss_charging_keyfigures_monthly.csv` (national stats 2020-2026)
8. Lausanne datasets (horodateur, mobilier urbain, stationnement) need manual download from viageo.ch

## Current state

### QGIS project: `~/CLAUDE/City101_ClaudeCode/CITY101_WORKING.qgz`
- 48 layers total (26 base map geopackages + 8 data CSVs + 14 WMS)
- CRS: EPSG:2056
- Rail_Noise_Day visible for verification, most WMS layers off

### Files created this session
- `~/CLAUDE/City101_ClaudeCode/source/city101_remote_work_HOURS.csv` (68 places, opening hours)
- `~/CLAUDE/City101_ClaudeCode/source/city101_shared_mobility.csv` (2,062 stations)
- `~/CLAUDE/City101_ClaudeCode/source/swiss_charging_keyfigures_monthly.csv` (63 months)
- `~/CLAUDE/City101_ClaudeCode/CITY101_WORKING.qgz` (new working QGIS project)

### Manual downloads needed (Andrea)
Save to `~/CLAUDE/City101_ClaudeCode/source/lausanne/`:
1. Horodateur (parking meters) — https://viageo.ch/md/ec4ea2eb-1c77-1964-6578-c9be0c3a24de
2. Mobilier urbain (benches) — https://viageo.ch/md/91e1a4d7-ec94-3e54-993d-912663f236b7
3. Stationnement (parking) — https://opendata.swiss/en/dataset/stationnement

## Tasks for next session

### PRIORITY 1: Cross-reference everything (monolithic script)
For each of the 68 remote work places, calculate:
- Distance to nearest train station + that station's trains/hr + commuter index
- Distance to nearest EV charger + charge level
- Distance to nearest shared mobility station + provider type
- Noise level at location (from WMS — query pixel value at point)
- Opening hours score (from HOURS csv — 24h=1.0, weekdays-only=0.5, etc.)
- WiFi quality from nearest WiFi hotspot

Output: `city101_remote_work_CROSSREF.csv` — one row per workspace, all infrastructure proximity + quality metrics.

### PRIORITY 2: Viageo.ch trawl
Crawl viageo.ch catalogue for all commune-level geodata along corridor. Their API exists at `/api/doc`. Pattern: search by bounding box or commune name, filter for open data, score by dark data potential. Target: find parking meters, street furniture, cycling infra for communes BEYOND Lausanne.

### PRIORITY 3: Segment framework + Working Continuity Index
- Divide corridor into ~50 segments (station-to-station or 2km intervals)
- Aggregate all metrics per segment
- Compute WCI = f(transit_freq, workspace_density, temporal_coverage, noise_quality, connectivity)
- This is the core A02 deliverable

### PRIORITY 4: Zurich comparison
Noise WMS already covers Zurich. Need to replicate the workspace + transit analysis for Zurich S-Bahn corridor to have a comparison dataset.

## Key decisions made (cumulative)
- Two-color map logic: MAP1 (teal/amber), MAP3 (coral/teal-green)
- Backbone principle: each map has one infrastructure spine
- Monolithic script pattern for large data ops
- Narrative pivot: unified "working continuity as a flow" — teacher-endorsed
- EV charging = supporting evidence only for A02
- Train frequency limit bug: API limit=30 makes all stations identical
- **QGIS project is now `CITY101_WORKING.qgz`** — do not use the old one in Downloads
- **Noise WMS = free Zurich comparison** — covers both corridors
- **Shared mobility is Geneva-heavy** — donkey_ge + 2em_cars = 1608/2062 stations

## Technical notes
- WMS layer IDs for geo.admin.ch: use `ch.bafu.laerm-bahnlaerm_tag` NOT `ch.bafu.laerm-eisenbahn_tag`
- sharedmobility.ch API: station_information.json + free_bike_status.json, no auth needed
- Lausanne data through viageo.ch requires interactive download (no direct API for file download found)
- DIEMO real-time JSON is gzip-compressed, 24MB uncompressed, 17,721 EVSE nationally, 1,886 in corridor
