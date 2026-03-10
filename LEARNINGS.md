# LEARNINGS — Accumulated Insights
**Things discovered across all sessions. Don't re-learn these.**

---

## Spatial findings

### The lakeside disconnect
EV charging stations along a "lakefront" corridor average 1.9km from the actual lake. The infrastructure serves the highway, not the waterfront. The corridor's identity as "lakeside" is a label, not a spatial reality for drivers.

### The Lavaux gap
Between Lausanne and Montreux, EV charging infrastructure nearly vanishes. This isn't neglect — it's deliberate. UNESCO-protected Lavaux vineyards actively resist infrastructure. WiFi coverage also drops. This creates an intentional digital and energy desert in the middle of the corridor. On maps, this gap is visually absolute and architecturally significant.

### Geneva-Lausanne concentration
Infrastructure clusters at the corridor endpoints. The middle sections (La Côte, Riviera) are underserved relative to population. The corridor is really two poles with a thin connective tissue.

### The permanently transient international
The corridor hosts CERN, UN, WHO, WTO, ICRC, ITU, IOC, EPFL, Nestlé HQ. These institutions create a population of globally-connected professionals who depend on public connectivity infrastructure while their employers have private fiber networks. The public WiFi gaps affect these people disproportionately — they need to work everywhere, but the corridor only lets them work in specific nodes.

## Architectural insights

### Charge speed = urban program
This is the core architectural argument. The duration of energy transfer creates mandatory dwell time, and that dwell time requires spatial program:
- Fast charge (20-30 min) → espresso, phone scroll, nothing designed for it
- Medium charge (1-2h) → restaurant, walk, coworking needed
- Slow/overnight → becomes part of domestic or hotel life

Nobody else in the class is mapping infrastructure where transfer duration determines spatial program. This is an architectural argument, not just a data one.

### Infrastructure creates behavior
Charge speeds mandate specific dwell times requiring particular spatial programs. WiFi coverage gaps create deliberate disconnection zones. Train frequency controls when you can move. Opening hours create temporal barriers. The corridor's "program" isn't designed by architects — it's an emergent consequence of infrastructure decisions made by different agencies who don't coordinate.

### The threshold concept (via Olson Kundig)
A charging station is a threshold between commute-mode and work-mode. Can waiting infrastructure *respond* to the commuter? Architecture that treats the transition between states as the main event.

## Theoretical frameworks

### Deleuze's surface (via Comtesse)
Meaning is produced at surfaces/interfaces, not hidden in depths. The data flows we map (charging, wifi, dwell times, reviews) ARE the urban reality, not evidence of something underneath. This validates reading urban patterns through visible flows.

### The fractal principle (via Comtesse)
"Every single part is the expression of the whole." One charging station's relationship to its context (noise, transit, groceries, acoustic comfort) is a microcosm of how the corridor organizes speed, pause, and exchange at every scale.

### Diversity formula (via Comtesse)
diversity × accessibility × time = urban vitality. Speed determines which diversity you can access (car = full line, train = node-to-node, bike = local texture). More diverse → more exchange. Homogeneity = stasis.

## Workflow lessons

### Monolithic scripts for large data
For large data operations (API fetches, processing big files): write a single self-contained script that runs end-to-end and prints only a summary. Never explore raw data interactively — it fills the context window and causes the conversation to hit its limit before the work is done. Pattern: fetch → filter → process → match → write output → print summary.

### LOI before LOG
Maximize information richness (LOI) early while keeping geometric detail (LOG) simple until design decisions become certain. "Work rich, export lean." Prevents wasted effort on detailed geometry that might change.

### The thinking is for you; the map is for them
Narrative and analysis live in handoffs and CONTEXT.md. Maps must communicate spatially without explanation. Don't put the argument in text overlays — put it in spatial relationships.

### Cross-referencing as discovery
The most valuable insights came from spatially joining datasets that weren't designed to go together: EV stations + train ridership + noise levels + grocery stores revealed which stations offer "good waits" vs "isolated pauses." This cross-reference methodology is the core analytical approach.

### Account capabilities follow the platform, not the account
As of 28-02, both accounts have Google Places search (reviews, ratings, opening hours). Cairn (Max plan) has higher limits; Lumen (school) hits Opus 4.6 cap quickly. Run both in parallel for 2x throughput.

Critical: MCP access (filesystem, QGIS, Rhino) comes from the desktop app, not the account. Whichever account is on the desktop app can read/write CONTEXT.md and control spatial tools. The account running in the browser only has project knowledge files. Don't assume "Cairn = MCP" — it's "desktop app = MCP." In practice Cairn is usually on desktop, but it's the platform that matters.

### MCP = full machine access
QGIS and Rhino MCP execute Python directly on Andrea's Mac with full user-level privileges. No sandbox. This means any Claude instance with MCP connected can do everything Claude Code can do (and more, since it's already inside the spatial tools). Safety rules are in the project instructions.

### Persistent context > handoffs
Rather than hunting through dated handoff files, maintain living state files (CONTEXT.md, LEARNINGS.md) in the CLAUDE folder. Any instance reads these at session start. Handoffs still exist for traceability but the living files are the primary context source.


### The 42x frequency variation
Train service frequency varies 42-fold across the corridor (Lausanne 28.5 trains/hr vs Bossière 2.0). This is *the* spatial argument for working continuity: a 2-minute wait at Lausanne vs 37 minutes at Bossière. The 35-minute difference creates demand for spatial program at low-frequency stations — you need somewhere to sit, WiFi, coffee. High-frequency nodes let you barely break stride.

### Commuter index reveals station character
SBB Passagierfrequenz workday/nonworkday ratio instantly classifies stations: Lancy-Pont-Rouge CI=4.04 (pure commuter, dead on weekends), Montreux CI=1.02 (balanced year-round), Épesses CI=0.47 (wine tourism, busier on weekends). Cross-referencing CI with frequency tells you who's waiting and how long — the two inputs to any design intervention.

### API limit parameters can silently flatten data
The transport.opendata.ch stationboard with limit=30 made every station look identical (~30 trains/hr). Only after removing the cap did the real 42x variation appear. Lesson: always check whether API pagination or limits are masking the actual distribution. If your data has suspiciously uniform values, the API might be the ceiling, not the reality.

### Stationboard ≠ connections for capacity
The transport.opendata.ch stationboard endpoint does NOT return capacity1st/capacity2nd occupancy data. That data (if available) would come from the /v1/connections endpoint (point-to-point journey queries). Different API call, different data model. Don't assume all endpoints return the same fields.

### EV charging: supporting evidence, not primary
The working continuity narrative is about the universal commuter, not the EV driver subset. EV charging data's best contributions: confirming the Lavaux gap from a third angle, demonstrating dwell-time-as-design-opportunity. But train frequency does both better and applies to everyone. Keep EV as background context, don't build A02 maps around it.


### The archipelago is structural, not temporal
The temporal corridor analysis (7 time slots × 49 stations) reveals that the number of workable stations barely changes across the day: 14 at peak, 13 at 11pm. The three structural gaps (Nyon→Gland, Gland→Morges, Lavaux Fracture) persist at all hours. This means architectural interventions at break points can't rely on "it works during rush hour" — the deficit is permanent. The corridor is always an archipelago.

### First/last train API: filter by calendar date
When querying transport.opendata.ch for "last train," requesting from 23:00 with limit=50 returns departures that wrap into the next morning for busy stations. Fix: query from 20:00 with limit=200 and filter results to the target calendar date (allowing past-midnight up to ~01:30). Same principle as the limit=30 lesson — the API returns what you ask for, not what you mean.

### IC trains as temporal indicator
IC departures are the clearest signal of corridor quality over time. They drop from 128 at peak (07-09 and 16-18) to 72 at late night (21-23) — the "workable corridor" (IC with WiFi, tables, quiet car) contracts by 44% while regional services barely change. The two-corridors finding has a temporal dimension: the good corridor shrinks faster than the bad one.

### Weekend = 10% less workable
Weekend midday TWCI is 0.90× weekday. Driven by workspace closures (coworking, libraries) more than frequency drops. The knowledge worker's corridor is primarily a weekday phenomenon. Weekend use is leisure/tourism — different spatial program, different break points.

## Data source notes

### Swiss DIEMO registry
25MB JSON, comprehensive EV charging database. Matched to our 194 stations, added 37 columns including power ratings, connector types, operator details. Access via geo.admin.ch.

### BAKOM cell towers
Federal telecom authority data. 3,218 towers along corridor with technology types (3G/4G/5G), power class, indoor/outdoor.

### opendata.swiss (CKAN API)
Federal open data portal. 10,000+ datasets. Triple-filter trawl script ready: 120+ keywords × 11,875 place names × bounding box overlap. Catches unexpected datasets beyond obvious searches.

### transport.opendata.ch
SBB open data API. Train schedules, station data. Not yet queried — priority for temporal layer.

### Google Places API
Account-bound on Cairn. Used for: remote work places (68), reviews (109 EV + 109 remote work), ratings. Still needed for: opening hours (68 places with place_ids ready).

### No public hourly SBB ridership data exists
SBB Passagierfrequenz provides daily totals only. Hourly curves must be modeled (Gaussian mixtures using commuter_index). Documented and accepted — no workaround exists.

### SwissTLM3D doesn't extend to Bex/Aigle
Rail geometry from SwissTLM3D literally doesn't cover the eastern terminus of the corridor. Bex snap=14km, Aigle snap=6.3km. Use `original_coords_used` flag and accept the limitation.

### Background agents fail on Write/Bash permissions
Agent team subagents in parallel mode can't execute Write or Bash tools due to permission restrictions. Pragmatic fix: run agent scripts sequentially from the main session, not as parallel background agents.

### GA cost calibration diverges east of Lausanne
v2 geometry used GA cost estimates to calibrate station distances, but these diverge from SBB km-post benchmarks east of Lausanne. v3 switched to SBB km-post calibration (r=0.9987).

### Night worker counts are the load-bearing claim
The 7-site healthcare supply chain argument rests on specific night worker numbers (4,600 / 1,680 / 1,500 / 400 / 300 / 730) that are NOT in any dataset. These were likely estimated externally. Field visits and OFS employment data are the verification path.

### "Zero nocturnal transport" is overstated
The real dead window is **01:00–05:00**, not "all night." Late-night frequencies: Bussigny 9.0 tr/hr, Nyon 7.0, Montreux 10.5, Lausanne 22.0. The argument holds but the framing must be precise — "4-hour gap" not "no night transport."

### Inline GeoJSON for file:// compatibility
Leaflet maps opened via `file://` can't use `fetch()` for local GeoJSON (CORS). Fix: inline all geodata as JS global variables in a separate `city101_geodata.js` file, loaded via `<script>` tag before the map module. The map module checks for globals first, falls back to `fetch()` for server deployments.

## A03/A04 insights

### The relay-lock prototypology
Combined two concepts: **relay** (system-level chain of nodes, like postal relay stations) and **lock** (building-level threshold management, like a canal lock). Each site has a different lock condition (cargo↔city, valley↔hilltop, last↔first train, etc.) but the same DNA: a chamber where the transition happens during the 01:00–05:00 dead window.

### Income-transport paradox at CHUV
CHUV nurses earning CHF 56k live in Renens/Prilly (worse night transport). Doctors earning CHF 95k live in Cour (walkable). The people who need the horizontal elevator most are the ones who can least afford the gap. ⚠️ [NEEDS: verification — are these really where CHUV staff live?]

### Three scales of the same problem
The 7-site network covers: infrastructure (nodes 1, 4 — how goods move), staff access (nodes 2, 3, 5, 7 — how workers get home), patient access (nodes 2, 5, 6 — how people reach care). Same system, different locks.

## Crit feedback patterns

- **Benchmark City101 vs Zurich** — always compare linear vs radial
- **Dark data**: nobody studies City101 as one city — this IS the dark data
- **Specificity > breadth** — reinforced by assistants and teachers
- **Data-driven**: let stories emerge from spatial patterns, don't impose narrative
- **"The line = no cars"** — diversity is expressed through accessibility modes
- **"Find the one person"** (Huang) — anchor the narrative in a single human experience
- **Horizontal elevator** — Huang loves this concept. On-demand rail, autonomous module, repurposed tracks.
- **Be very specific** (assistants) — not "night workers" but "one nurse, one shift, one 2am walk home"
