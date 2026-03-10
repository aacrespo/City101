# HANDOFF — 22-02 Session 1

## Last action
Confirmed second dataset topic: **Invisible Data Flows** (Flow of Forces) — WiFi/public connectivity infrastructure along Geneva–Villeneuve corridor. Topic is unoccupied in class spreadsheet. Decided on 4-layer approach executed one at a time.

## Current state

### Dataset 1 — Electric Charging ✓ COMPLETE
- `city101_ev_charging_ENRICHED_v3.csv` — 194 rows, 53 columns
- Sources: Google Places + OSM + DIEMO + OpenChargeMap
- QGIS: needs reload with ENRICHED_v3 (still has old 16-col version loaded)
- 7 OCM reviews in `city101_ev_charging_REVIEWS.csv`
- Google ratings still missing (needs Google Places API — see account strategy below)

### Dataset 2 — Invisible Data Flows (IN PROGRESS)
4-layer plan, priority order:
1. **WiFi hotspots** ← CURRENT LAYER (start here)
2. **Data centers**
3. **Fiber backbone routes**
4. **4G/5G cell towers**

#### WiFi research already done (from previous session):
- ~50 locations compiled in research doc (see project file: `Free_Public_WiFi...md`)
- Covers: Geneva municipal (635+ hotspots), Lausanne Citycable (78 hotspots), SBB-FREE (7 stations), coworking spaces, libraries, cafés
- Qualitative analysis done: 3 clusters (Geneva, Lausanne, Vevey-Montreux), 4 deserts (Lavaux = most dramatic)
- Municipality readiness rankings: Geneva ★★★★★ → Villeneuve ★☆☆☆☆
- Key insight: inverse correlation between scenic value and WiFi coverage

#### What's NOT yet done for WiFi layer:
- No proper CSV with LV95 coordinates (research doc has WGS84 lat/lon only)
- No Google Places reviews / ratings for individual WiFi locations
- OSM Overpass query not yet run (queries are documented in research doc, ready to execute)
- Geneva SITG official dataset not yet fetched (568+ access points as GeoJSON)
- SBB official WiFi dataset not yet fetched (data.sbb.ch)
- Lausanne Citycable exact hotspot coordinates not yet fetched

## Open threads — PRIORITY ORDER

### Immediate (tonight, before pin-up)
1. **WiFi CSV** — run OSM Overpass query + fetch SITG Geneva + SBB data → merge into `city101_wifi_MERGED.csv`
2. **WiFi reviews** — use Google Places API (THIS account only — see below) to get ratings for coworking spaces and named venues
3. **LV95 conversion** — all coordinates → EPSG:2056 for QGIS
4. **QGIS styling** — load WiFi layer + reload ENRICHED_v3 for EV charging, compose pin-up maps
5. **Data centers** — second layer, can be added as separate simple CSV tonight if time allows

### Soon after pin-up
6. **Fiber routes** — harder to get, may need Swisstopo or manual tracing
7. **Cell tower layer** — BAKOM data (Swiss federal telecom authority) may have this
8. **EV charging Google ratings** — batch fetch via Google Places API (this account)

## TWO-ACCOUNT WORKFLOW STRATEGY

### Account capabilities
| Feature | This account (personal) | Other account (school) |
|---------|------------------------|----------------------|
| Google Places API | ✅ Working | ❌ Not available |
| Usage limit | Lower | Higher |
| Model | Sonnet | Opus 4.6 available |
| Project files | ✅ This project | Needs handoff sync |

### Recommended parallel workflow
**This account handles:**
- All Google Places API calls (reviews, ratings, coordinates)
- Final CSV outputs that need Places data
- Anything requiring the enriched datasets already here

**Other account handles:**
- Heavy analysis, long scripts, iterative coding (higher limit + Opus)
- QGIS MCP operations (styling, rendering maps)
- Rhino work
- Research tasks that don't need Places API

### Handoff sync between accounts
- Copy the latest HANDOFF file into the other account's project files
- The other account can pick up any task that doesn't need Google Places
- For Places-dependent tasks: run script HERE, copy output CSV to other account via shared file or paste

### I cannot share API keys
Claude doesn't have API keys — the Google Places integration works because it's built into this Claude.ai account's tools. There's no key to copy. The capability is account-bound.

## Key decisions made (cumulative)
- Framing: "flow of people" (EV) + "invisible data flows" (WiFi/infrastructure)
- EV charging analyzed through human experience lens
- LV95 / EPSG:2056 as working coordinate system
- LOG/LOI/LOD framework adopted (see 00_Workflow_v02.md)
- LOI principle: "Work rich, export lean"
- 4-layer invisible infrastructure plan: WiFi → data centers → fiber → cell towers
- WiFi desktop = important for equity argument (unlimited cellular plans don't eliminate need)
- Scenic WiFi desert (Lavaux) is key analytical finding — quantify and visualize

## Technical notes
- WiFi research doc: `/mnt/project/Free_Public_WiFi...md` — has 50+ locations, Overpass queries, open data URLs
- SITG Geneva WiFi WFS: `https://app2.ge.ch/tergeoservices/rest/services/Hosted/VDG_WIFI_PUBLIC/FeatureServer`
- SBB WiFi: `https://data.sbb.ch/explore/dataset/wifistation/`
- OSM Overpass: bbox `46.10,6.05,46.55,6.95` — queries documented in research doc
- EV scripts: `enrich_v2.py` (DIEMO), `enrich_distances_context.py` (distances), `enrich_ocm.py` (OCM)
- OCM API key: `23617e07-95e4-4666-b1f6-f4dfcd6a8e64`

## Data sources (this session)
- City101 class spreadsheet photo: confirmed topic availability (22.02.26)
- Previous session WiFi research doc: compiled from SITG, SBB, OSM, direct venue research
