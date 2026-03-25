# TEAM HANDOFF — Andrea + Henna
**Date**: 2026-03-01 (night)
**From**: Andrea (via Cairn)
**To**: Henna
**Context**: A02 desk crit: **Monday March 2nd, 1pm** (submission deadline March 3rd). Team presentation.

---

## THE SITUATION

We have ~14 hours until the crit. The data foundation is strong — arguably the deepest in the studio. The question is curation: what do we print, what do we show live, and what's the argument we walk them through in 30 minutes?

Our shared narrative: **"the rail line as 24-hour living infrastructure"** — workspace by day (Train Desk), lifeline by night (Gap Hours). The prototypology: an adaptive rail-mounted module that transforms through the 24h cycle. One system, following demand along the line.

The A02 brief asks for 5 things:
1. A clear narrative for your flows ✅ strong
2. Updated maps according to your narrative/index ✅ exist in QGIS, need export + curation
3. Your formula for an urban potential index ✅ WCI computed
4. Comparison metrics to Zurich 🟡 structural argument clear, data thin
5. Point-Cloud Sections for high-potential sites 🔴 week 2, but need sites identified now

---

## WHAT ANDREA HAS BUILT SINCE FEB 24 — Session by Session

### 28-02 (late night): Transport Data Acquisition
Two major datasets via transport.opendata.ch API:
- **Service frequency v2** (49 stations): trains/hr during workday morning. Revealed **42x frequency variation** — Lausanne 28.5 tr/hr (2-min wait) vs Bossière 2.0 (37-min wait) vs St-Saphorin 0.0. This is THE spatial argument for working continuity.
- **SBB Ridership** (174 stations): daily passengers + Commuter Index (workday/nonworkday ratio). CI classifies station character: Lancy-Pont-Rouge CI=4.04 (pure commuter), Montreux CI=1.02 (balanced), Épesses CI=0.47 (wine tourism).
- Bug discovery: API limit=30 had silently flattened all stations to identical values. Fixed in v2.

### 01-03 S1 (morning): Narrative Gap + 4-Point Framework
Felt "something is missing." Brainstormed directions → defined 4 investigations to shift WCI from spatial scores to journey narrative:
- Point 1: Break Point Map (where continuity ruptures)
- Point 2: Temporal Corridor (same 101km at different hours)
- Point 3: GA Hypothesis (who experiences it as one city)
- Point 4: Station Reviews (dark data — felt quality)
Full breakdown in `TODO_4_POINTS.md`.

### 01-03 S2 (desktop MCP): The Dark Data Trawl + QGIS Setup
Major opendata.swiss investigation → `opendata_trawl_categorized.md` scoring 50+ federal datasets.
Actually fetched and loaded:
- **14 WMS layers** from geo.admin.ch: rail noise day/night, road noise day/night, EV 2035 projections (3 scenarios), home charging 2035 (3 scenarios), EV fleet 2035, electricity demand. **KEY: noise WMS covers all of Switzerland including Zurich — free comparison data already loaded.**
- **Shared mobility** (2,062 stations from sharedmobility.ch): 8 providers. Geneva-heavy: donkey_ge + 2em_cars = 78%. Lausanne has PubliBike (67). Vevey-Montreux barely exists.
- **Swiss charging key figures** (63 months national stats 2020-2026)
- Created **CITY101_WORKING.qgz** (now 50+ layers). Old project preserved in Downloads.
- Identified **viageo.ch** for commune-level Romandie data (parking meters, benches, cycling infra) — not yet fetched.

### 01-03 S3 (browser + MCP): WCI Computation + A02 Map Layouts
Claude Code monolithic script produced:
- `city101_remote_work_CROSSREF.csv` (68 workspaces × 31 columns): each workspace cross-referenced against all infrastructure.
- `city101_corridor_segments_WCI.csv` (49 segments): **Working Continuity Index**. Formula: WCI = 0.30×transit + 0.25×workspace + 0.20×temporal + 0.15×connectivity + 0.10×mobility. Range: 0.0003 (St-Saphorin) to 0.6431 (Genève).
- 7 print layouts created in QGIS (A1 landscape): WCI hero, Remote Work Infrastructure, Lavaux Fracture zoom, Geneva Pole, Lausanne Pole, Transit Backbone, Data Synchronicity (all layers). **Not yet exported/reviewed.**

### 01-03 S4 (browser): Rail History Research
Feeding the "horizontal elevator" concept (Huang loves this):
- Comprehensive timeline 1855-2025 of every rail line in corridor
- **6 ghost stations** killed by Rail 2000 in 2004 (Bursins, Perroy, Lonay-Préverenges, etc.)
- **Clarens-Chailly-Blonay tramway** (1911-1955, demolished, 5.6km) — tracks gone
- **Blonay-Chamby heritage railway** — tracks still exist, museum operates weekends
- Peak rail density was ~1911. Everything since is contraction. More connectivity 115 years ago.

### 01-03 S5 (browser): Rail History Visualization
Built `rail_history_v3.html` — interactive Leaflet.js timeline, dark basemap, 170 years of rail evolution. 18 corridor lines, 16 Swiss context lines, 6 ghost stations, 35 timeline events, play/pause/speed. Research tool AND potential presentation element.

### 01-03 S6 (current, desktop MCP): Break Points + Journey Workability + Lumen Dispatch

**Break Point Analysis** (`city101_break_points.csv`, 49 stations):
Five break dimensions: transit gap, workspace desert, connectivity gap, amenity void, mobility isolation. Severity classification per station.
- **Only 11 of 49 stations (22%) maintain full continuity.** The "linear city" is an archipelago.
- The archipelago: Genève → (19.3km) → Nyon → Gland → (20km) → Morges → Lausanne/Flon → (17.5km) → Vevey → La Tour-de-Peilz → Montreux → Villeneuve
- **Frequency-amenity paradox**: Bussigny (9 tr/hr), Lancy-Bachet (12.5 tr/hr), Aigle (16.5 tr/hr) = great transit, ZERO workspaces. Train delivers you to a void. One coworking space flips these from MAJOR break to CONTINUOUS. → **Intervention sites for the adaptive module.**

**Lumen dispatched** for station reviews. Result:
- 37 new stations (M2, M1, Léman Express, CGN boats) with Google ratings
- 71 reviews tagged by theme. **Zero mention "work" at stations.** Beauty #1 (26), amenities #2 (22). Nobody thinks of stations as workplaces — this is dark data.

**Journey-level on-train workability** (via Claude Code, 618 connections):
Shifted unit from per-hop to per-JOURNEY. Used connections API.
- 15% PRIME_WORK, 12% WORKABLE, 39% MARGINAL, 32% NOT_WORKABLE, 2% BROKEN
- **Two corridors on same tracks**: IC (Genève↔Lausanne 46min, WiFi, tables, quiet car) = office extension. S-Bahn (everything between) = doors every 90sec, no WiFi, can't work.
- Workability barely changes by time of day. The temporal pulse is about FREQUENCY (how long you wait), not QUALITY (what the ride is like).

---

## KEY DISCOVERIES (for the crit argument)

**The Archipelago**: The linear city doesn't exist as continuous infrastructure. It's 11 functional islands in a sea of breaks. The 20km Gland→Morges gap and the 17.5km Lavaux Fracture are structural wounds.

**Two Corridors on Same Tracks**: IC passengers experience a workable linear city. S-Bahn passengers experience fragmented villages. Same infrastructure, completely different city depending on which train you board.

**The Frequency-Amenity Paradox**: Some stations have excellent transit but zero amenities — the train delivers you to a void. These are the highest-impact intervention sites.

**Nobody Reviews Stations for Work**: Zero "work_friendly" in 71 reviews. The idea of the station as workplace is invisible to users. Our prototypology introduces a use that doesn't yet exist in anyone's mental model.

**42x Frequency Variation**: 2-min wait at Lausanne, 37-min at Bossière. The wait duration IS the design problem — it creates demand for spatial program at low-frequency stations.

**Peak Rail Was 1911**: The corridor had more connectivity 115 years ago. Ghost stations and demolished tramways show a network that contracted, not one that was never built.

---


---

## THE GA HYPOTHESIS — Who Lives the Linear City?

The WCI tells us WHERE the corridor breaks. The GA hypothesis tells us FOR WHOM. The same corridor is a different city depending on your ticket type. This is Comtesse's formula made concrete: diversity × **accessibility** × time. The GA changes the accessibility variable to maximum.

### Behavioral segmentation
- **GA citizen**: Treats entire corridor as one city. Goes to Geneva for work, Montreux for dinner, Nyon for weekend. Cost = ~CHF 10.50/day (amortized annual). The corridor IS their city.
- **Demi-tarif commuter**: Uses corridor daily but only between home and work. Two points, one line. City = home station catchment + work station catchment. Geneva→Lausanne = ~CHF 13 one-way.
- **Point-to-point occasional**: Corridor is expensive (~CHF 26 Geneva→Lausanne). Takes car instead. The linear city doesn't exist for them.
- **Frontalier**: Enters corridor from France via Léman Express (~100k in Geneva canton alone). Uses it intensively during work hours, invisible after 19h. Can't buy GA (French resident). The "ghost citizen."
- **Gig worker / precariat**: Platform workers, irregular hours, no corporate GA. Pay per trip. Experience the worst version: expensive, infrequent, no workspace.

### What we can compute tonight
- **Cost map**: SBB prices for all 35 OD pairs we already have journey data for. Plot "cost to traverse each segment" by ticket type. The corridor is literally a different length depending on your wallet.
- **Frontalier overlay**: Léman Express stations (Annemasse, Chêne-Bourg) as entry points. Cross-border commuter flows visible in ridership data (high CI = commuter-heavy).

### Why this matters for the crit
The archipelago finding (only 11/49 stations maintain continuity) hits differently when you add: "...and if you don't have a GA, it's even worse because each hop costs CHF 5-26." The break points aren't just spatial — they're economic. The Lavaux Fracture is beautiful and free to cross by car, but costs CHF 8.80 by train (Vevey→Lausanne demi-tarif). The corridor selects for car owners in the gaps.

---

## CLASSMATE DATA CROSS-REFERENCE — Patterns to Map

All classmate datasets are locally available in `source/00-datasets 2/`. These aren't decorative overlays — each tests a specific hypothesis about who uses the corridor and how infrastructure creates (or prevents) their mobility.

### Priority cross-references for the crit:

**Charlene Dejean — Gig work (50 locations)**
`source/00-datasets 2/charlenedejean/dejeancharlene-gigwork.csv`
Columns: id, municipality, place_name, work_type, platform, workers_est, season, permit_status, latitude, longitude, dist_lake...
**Hypothesis**: Do gig workers cluster at break points or avoid them? If the precariat concentrates where infrastructure is worst, that's a structural inequity finding. Overlay with WCI + break severity.

**Thomas Riegert — Hospitals + healthcare (4 datasets, ~240 locations)**
`source/00-datasets 2/thomasriegert/thomasriegert-publichospitals.csv` (public hospitals)
`thomasriegert-privateclinics.csv` + `generalpractitioners.csv` + `specialists.csv`
**Hypothesis**: Healthcare = shift workers. A CHUV nurse ending at 23:00 needs to get to Montreux. Cross with first/last train data → which hospital workers are stranded by the dead window? Also: hospitals as 24h anchor points that generate nighttime corridor demand.

**Thomas Riegert — Religious diversity (12 datasets, ~42+ communities)**
All denominations mapped: Buddhist, Christian, Evangelical, Hindu, Jewish, Muslim, Orthodox, Protestant, Esoteric.
**Hypothesis**: Comtesse says diversity = vitality. If religiously diverse segments also score highest WCI, the theory holds. If they diverge, the corridor has diversity without accessibility — potential without connection.

**Siméon Pavicevic — Industrial zones + sectors (25 zones, 195 companies)**
`simeonpavicevic-industrialzones.csv` + `simeonpavicevic-industrialsectors.csv`
Includes NOGA codes, employee counts (ETP), energy intensity.
**Hypothesis**: Do industrial zones align with the frequency-amenity paradox stations? Bussigny (9 tr/hr, zero amenities) — are there industrial zones nearby generating shift workers who arrive at this void?

**Marek Waeber — Schools (199 across corridor)**
`source/00-datasets 2/marekwaeber/CSV/` — Aldi, Coop, Denner, Lidl, Migros (121 stores)
Plus: `All_ecoles_public_arc_lemanique.csv` (199 schools)
**Hypothesis**: Are schools clustered at the 11 continuous nodes or distributed? If families in the gaps have no school within walking distance of a station, the corridor selects for car-owners. School locations = family infrastructure.

**Vladislav Belov — Acoustic ecology (50 points)**
Already partially integrated (noise levels near EV chargers). But cross with station break points: are the worst break points also the loudest? Or is the Lavaux Fracture actually the corridor's quietest segment — making it simultaneously the worst for work and the best for rest?

**Henna Rafik — UHI + thermal comfort (203 zones + 33 comfort points)**
`hennarafik-UHIhighpeakheatislands.csv` (40), `UHImediumtransitionzones.csv` (54), `UHIlowcoolzones.csv` (109)
`hennarafik-thermalcomfort.csv` (33 points)
**Hypothesis**: Environmental quality as hidden WCI dimension. A station with good frequency but 40°C heat island = uncomfortable wait = break point even if the data says it's continuous. Add thermal comfort to station quality assessment.

### Quick wins (tonight, scriptable):
1. **Count classmate features within 500m of each station** — for each of the 49 stations: how many gig work locations, hospitals, schools, religious buildings, industrial companies within 500m? Produces a "station richness" score from classmate data alone.
2. **Religious diversity index per segment** — Shannon diversity of denominations along corridor segments. Tests Comtesse directly.
3. **Hospital proximity to last-train stations** — which hospitals are >1km from a station that still runs past 23:00?


## WHAT'S MISSING — Honest Assessment

### Critical for crit (must do tonight/tomorrow morning):

**1. First/last train per station** — HIGHEST PRIORITY.
This unlocks the temporal narrative: "at 7am, 40 stations active. At midnight, 8. At 2am, zero." Without this, the 24h story is conceptual not evidenced. Also produces the "dead window" per station — duration of zero service. **This is Henna's key contribution.**

**2. Curated map export** — Andrea has 7 layouts in QGIS but hasn't reviewed or exported any. Need to select the strongest 3-5 and export as print-ready PDFs.

**3. Narrative text** — 1-page max. Why this index, what it reveals, what the prototypology responds to. Written together.

### Important but achievable:

**4. Zurich minimal comparison** — The key insight is structural: Zurich is radial (everything converges on HB, no point >15min from center), City101 is linear (you traverse, you don't converge, some points 40min from nearest functional node). Even 10 Zurich S-Bahn stations with frequency + workspace proximity gives a comparison. Plus noise WMS already covers Zurich.

**5. Night dimension** — 24h venue scan: what's open past midnight? Extends the workspace hours data into Henna's gap hours territory. Google Places hours filter.

### Would be powerful to have thought about (for discussion, not maps):

**6. Parking meter temporal data** (viageo.ch, Lausanne) — dwell time pricing reveals how long the city *expects* you to stop. 30-min meters = "pass through." 4-hour meters = "stay." The city's implicit program, written in coin slots.

**7. Public bench locations** (mobilier urbain, Lausanne) — the most basic workspace infrastructure. A bench near a station with WiFi = accidental coworking. How many stations have a bench within 100m?

**8. The loophole economy** — CFF land has different zoning. Coop Pronto in stations stays open when everything else closes. Legal geography creating the only night economy along the corridor.

**9. View quality per segment** — the lake is the corridor's identity but how many stations actually see it? Station with lake view + bench + WiFi = premium work node.

**10. Tunnel locations** — where cell signal dies on the train. Completes the on-train workability picture.

### Not for this crit:
- GA Hypothesis (research-heavy, parked)
- Point Cloud Sections (week 2 deliverable)
- Full Zurich WCI replication

---

## MAP STRATEGY — What to Print

The crit is a 30-min desk conversation. Print more maps than you'd show at a pin-up — they become reference material you pull from during discussion. Some maps are the ARGUMENT, others are EVIDENCE you point to when asked.

### The Argument Maps (print large, present first):

**MAP A — The Archipelago** (hero map)
Full corridor, WCI graduated color. The 11 continuous nodes named. The gaps dimensioned (19.3km, 20km, 17.5km). One glance = the linear city doesn't exist as continuous infrastructure.

**MAP B — The Two Corridors / Journey Workability**
Rail spine colored by journey workability: PRIME (IC routes) vs NOT_WORKABLE (S-Bahn). Same tracks, two different cities. Annotate with key journey times and comfort scores.

**MAP C — The Temporal Corridor** (IF first/last train data lands)
Same corridor at 3 timestamps: 8am / 8pm / 2am. Stations light up or go dark. The line dying at night = Henna's gap hours. Powerful visual.

### Evidence Maps (print smaller or have on screen, pull during discussion):

**MAP D — Lavaux Fracture zoom**
The wound up close. WCI near zero, frequency near zero, workspace desert, noise data showing the quiet. The "is this a failure or a refuge?" question lives here.

**MAP E — Break Point Classification**
All 49 stations colored by severity (CONTINUOUS / MINOR / MODERATE / MAJOR / TOTAL_RUPTURE). The frequency-amenity paradox stations labeled.

**MAP F — Transit Backbone**
Train frequency graduated along the spine. The 42x variation. Ridership bubbles sized by daily passengers.

**MAP G — Remote Work Infrastructure**
68 workspaces + WiFi hotspots + their hours (open now / closes at 18h / 24h). The workspace dimension of the WCI.

**MAP H — Zurich Comparison** (IF data lands)
Side-by-side: radial vs linear. Same color scheme, same metrics. Even approximate data makes the structural argument.

**MAP I — Shared Mobility Coverage**
Geneva-heavy, Lausanne minimal, Riviera absent. The last-mile problem visualized.

### On Computer (live exploration during crit):

- 50-layer QGIS project for live querying
- Rail history timeline (interactive HTML)
- Break points table / journey workability details
- Station reviews
- The opendata trawl document (shows research depth)

---

## TASK SPLIT — Tonight + Tomorrow Morning

### HENNA (Meridian or Lumen, browser):
**Priority 1 — First/last train per station** ⏰ TONIGHT
- Query transport.opendata.ch `/v1/stationboard` for all 49+ corridor stations
- Early morning window: departures after 04:00 → find first train
- Late night window: departures after 22:00 → find last train
- Output: CSV with station, first_departure, last_departure, dead_window_hours
- Pattern is in Andrea's `fetch_transport_frequency_v2.py` — same API, different time parameters
- This is the SINGLE MOST VALUABLE dataset for both narratives

**Priority 2 — 24h venue scan** 
- Google Places search along corridor for cafés/restaurants open past midnight
- Extends Andrea's workspace hours into night territory

**Priority 3 — Bring existing data**
- Thermal comfort / UHI / cold air drainage as environmental quality layer
- Her ridership data (already integrated but good to have for reference)

**Priority 4 — Night bus coverage**
- Noctambus routes: where do they run, how do they compare to rail spine?

### ANDREA (Cairn desktop MCP + Claude Code):
**Priority 1 — GA cost map + classmate cross-reference** ⏰ TONIGHT
- SBB pricing for 35 OD pairs by ticket type (GA / demi-tarif / full price)
- Classmate data cross-reference: count features within 500m of each station
  - Gig work (Charlene), hospitals (Thomas), schools (Marek), industrial zones (Siméon)
  - Religious diversity index per segment (Thomas's 12 denomination datasets)
- Output: enriched station CSV with "station richness" from classmate overlays

**Priority 2 — Map curation + export** ⏰ TOMORROW MORNING
- Review the 7 existing QGIS layouts
- Add new maps: GA cost gradient, classmate cross-reference, break points
- Export PDFs, check print quality
- Load all new layers (break points, journey workability, station ratings, GA, classmate data)

**Priority 3 — Zurich minimal comparison** ⏰ TONIGHT IF TIME
- 10 Zurich S-Bahn stations: frequency + nearest workspace + rough WCI
- Structural argument: radial (no point >15min from HB) vs linear (40-min gaps)
- Even approximate makes the point

**Priority 4 — Merge all new data into QGIS**
- Station ratings layer, journey workability, break points
- GA cost layer, classmate cross-reference layer
- Whatever Henna produces (first/last train, 24h venues)

### TOGETHER (tomorrow morning before 1pm):
- Write 1-page narrative text
- Decide final map selection
- Identify 3-5 intervention sites (for week 2 point cloud sections)
- Rehearse: what's the 2-minute opening pitch before they start asking questions?

---

## DATA INVENTORY — Everything Available

### Core Datasets
| Dataset | File | Rows | Key info |
|---------|------|------|----------|
| EV charging MERGED | city101_ev_charging_MERGED.csv | 194 | Base data |
| EV charging ENRICHED v3 | city101_ev_charging_ENRICHED_v3.csv | 194 | 53 cols, DIEMO+distances+context |
| EV charging REVIEWS | city101_ev_charging_REVIEWS.csv | 109 | Sentiment-tagged |
| EV charging CROSSREF | city101_ev_charging_CROSSREF.csv | 194 | +transit, noise, grocery proximity |
| WiFi MERGED v2 | city101_wifi_MERGEDv_2.csv | 81 | Quality scores, clusters |
| Remote work places | city101_remote_work_places.csv | 68 | Google-sourced with place_ids |
| Remote work REVIEWS | city101_remote_work_REVIEWS.csv | 109 | Work-relevance tagged |
| Remote work HOURS | city101_remote_work_HOURS.csv | 63 | Opening hours, 14 are 24h |
| Remote work CROSSREF | city101_remote_work_CROSSREF.csv | 68 | 31 cols, full infrastructure proximity |
| Service frequency v2 | city101_service_frequency_v2.csv | 49 | Trains/hr, IC/IR vs regional |
| SBB Ridership | city101_ridership_sbb.csv | 174 | Daily passengers, commuter index |
| Shared mobility | city101_shared_mobility.csv | 2,062 | E-bikes, scooters, carshare |
| WCI corridor segments | city101_corridor_segments_WCI.csv | 49 | Working Continuity Index |
| Break points | city101_break_points.csv | 49 | Break severity classification |
| Train workability (station) | city101_train_workability.csv | 49 | IC/IR vs R/S ratio per station |
| Journey workability | city101_journey_workability.csv | 618 | Journey-level, 35 OD pairs × 3 slots |
| Journey workability summary | city101_journey_workability_summary.csv | 35 | OD pair aggregates |
| Station ratings (Lumen) | city101_station_ratings.csv | 37 | M2, M1, CGN, LEx with ratings |
| Station reviews (Lumen) | city101_station_REVIEWS.csv | 71 | Tagged by theme |
| Swiss charging stats | swiss_charging_keyfigures_monthly.csv | 63mo | National benchmark |
| Cell towers | city101_cell_towers.csv | 3,218 | 3G/4G/5G |
| International anchors | city101_international_anchors.csv | 15 | CERN, UN, IOC, etc. |

### WMS Layers in QGIS (national coverage incl. Zurich)
Rail noise day/night, road noise day/night, EV 2035 projections (3 scenarios), home charging 2035 (3 scenarios), EV fleet 2035, electricity demand.

### Classmate Data Available
data_inventory_v.1.md 
(Henna's ridership (22 stations) + thermal comfort + UHI + cold air drainage, Vladislav's acoustic ecology (50 points), Marek's grocery stores (121), plus inventoried: Siméon's industrial zones, Charlene's gig work, Thomas's hospitals, Aimeric's cultural spaces.)

### Not Yet Fetched (identified)
- First/last train per station (HENNA TONIGHT)
- viageo.ch commune data (parking meters, benches)
- Tunnel locations from OSM
- Zurich S-Bahn frequency + workspaces (ANDREA TONIGHT)

---

## FILES TO SHARE ON DRIVE

Priority 1 (Henna needs for her tasks):
- `city101_break_points.csv`
- `city101_journey_workability.csv` + `_summary.csv`
- `city101_corridor_segments_WCI.csv`
- `city101_remote_work_HOURS.csv`
- `city101_service_frequency_v2.csv` (for the first/last train script pattern)

Priority 2 (context):
- `city101_station_ratings.csv` + `_REVIEWS.csv`
- `city101_train_workability.csv`
- `city101_remote_work_CROSSREF.csv`

Documentation:
- This handoff (`TEAM_HANDOFF_01-03.md`)
- `TODO_4_POINTS.md`
- `opendata_trawl_categorized.md`

---

## THE 2-MINUTE OPENING PITCH (draft)

"We're testing whether City101 functions as a linear city for knowledge workers. We built a Working Continuity Index — combining transit frequency, workspace availability, temporal access, connectivity, and mobility — and computed it for every train station on the corridor.

The answer: it doesn't. Only 11 of 49 stations maintain full working continuity. The corridor is an archipelago — 11 functional nodes separated by infrastructure deserts. The two worst gaps are 20km (Gland to Morges) and 17.5km (the Lavaux Fracture).

But the most surprising finding is that there are two different cities occupying the same tracks. On the IC express, Geneva to Lausanne is a 46-minute office — WiFi, tables, quiet car. On the S-Bahn, the same corridor is a sequence of 90-second interruptions where you can't open a laptop. 85% of connections are not workable.

Our prototypology responds to this: an adaptive module on existing rail infrastructure. Work pod by day at the frequency-amenity paradox stations (great transit, zero amenities). Rest/transport pod by night when the line dies. The data tells us where and when to deploy it. The design tells us how it transforms."

Then they ask questions and you pull up maps/data.
