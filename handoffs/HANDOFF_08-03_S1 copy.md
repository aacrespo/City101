# HANDOFF — 08-03 Session 1
**Account**: Meridian (school)

## Last action
Identified and documented **24 candidate sites** for horizontal elevators along the City101 corridor, cross-referencing all 15 project datasets. Built an interactive React artifact cataloguing each site with data evidence. Sites are tiered by urgency (critical / high / moderate) and typed by disconnection pattern (daytime commuter gap / nocturnal dead zone).

## Current state
- **Artifact**: `city101_horizontal_elevator_24_sites.jsx` — interactive card-based explorer with corridor position map, filtering (day/night), sorting (position/urgency), and expandable detail cards per site
- **Earlier versions also saved**: `city101_horizontal_elevator_sites.jsx` (6 sites), `city101_horizontal_elevator_12_sites.jsx` (12 sites), `city101_horizontal_elevator_18_sites.jsx` (18 sites) — superseded by the 24-site version
- **No QGIS layers created this session** — all analysis was done in Python against the CSV files
- **No handoff file was found at session start** — last known handoff was HANDOFF_23-02_S2 (from Cadence account), which established the narrative: "the rail line as 24-hour living infrastructure"

## The 24 Sites — Summary

### Tier 1: Critical (5 sites)
| # | Name | Type | Key Signal |
|---|------|------|------------|
| 1 | Ecublens ↔ Lausanne West | Day | Day/night ratio 2.48× (highest). 30k EPFL/UNIL + 800 stranded night workers |
| 2 | Geneva North Industrial Belt | Night | 4,600 night workers, 3 venues, 12k frontaliers |
| 7 | Lancy–Pont-Rouge ↔ Onex/ZIPLO | Day | Commuter index 4.04. 19k Onex = biggest remote work desert |
| 10 | Lausanne Perpendicular | Day | 5.8km / 250m altitude split. 127k people. Architectural test: what is a "horizontal" elevator on a slope? |
| 18 | Crissier–Bussigny Night Belt | Night | 1,680 supply-chain night workers (pharma, food, logistics). Zero nocturnal transport |

### Tier 2: High (9 sites)
| # | Name | Type | Key Signal |
|---|------|------|------------|
| 3 | Pully–Lutry → Lausanne | Day | Jobs/pop 0.04 (lowest). 7% work buildings. Perpendicular disconnect |
| 4 | Morges–Rolle Gap | Night | 300+250 night workers stranded. Longest gap GE–LS. 58% car |
| 5 | Montreux–Rennaz Hospital | Night | 400 night staff, hospital off-rail. 2.6★ Google rating (lowest) |
| 8 | Genève-Sécheron International | Day | Commuter 4.53 (highest). UN/WHO ghost zone weekends. 50-62% foreign |
| 9 | Gland–Rolle La Côte Gap | Day | 6.3km station gap. Villages with 1.8× day/night ratios. 62% car |
| 12 | Founex–Nyon Gap | Day | 6.6km (longest gap). 28k between. Shared mobility desert |
| 13 | Bernex — Stranded Southwest | Night | 10.6k pop. 0 venues in 3km. 5.7km to coworking. Darkest pocket |
| 19 | Nyon Industrial + Hospital | Night | 730 night workers: hospital (200), industrial (300), hilltop clinic (150) |
| 20 | Lausanne Flon Nightlife | Night | 300 bar staff Mon–Thu. Noctambus = Fri/Sat ONLY. Weeknight dead window |

### Tier 3: Moderate (10 sites)
| # | Name | Type | Key Signal |
|---|------|------|------------|
| 6 | Versoix–Geneva International | Day | 6km to employer. Most disconnected residential cluster |
| 11 | Burier–La Tour Spine | Day | Commuter 3.49. Invisible station carrying hillside villages |
| 14 | Thônex-Moillesulaz Border | Day | 27k at eastern dead end. Border wall. 4.2km to station |
| 15 | Allaman Hub | Day | 5,200 daily pax / 646 residents = 8× anomaly. Car funnel |
| 16 | Lavaux Vineyard Corridor | Day | 1.89× ratio (highest). UNESCO = can't widen roads |
| 17 | Epalinges Medical Hill | Day | 3.4km from rail. Medical satellite. 38 mobility stations → dead end |
| 21 | Satigny Agricultural Island | Day | 15% primary sector. Zero mobility. Wine country → CERN |
| 22 | Puidoux-Chexbres Hillside | Day | 68% car (highest). 2 tr/hr. Hillside above Lavaux |
| 23 | Genthod-Bellevue Lakeside | Night | Wealthy, 40% foreign. Zero nocturnal. Zero venues |
| 24 | Saint-Prex Isolated Village | Night | 64% car. 4 tr/hr. Forgotten middle between Morges and Allaman |

## Open threads
- **Group hasn't chosen sites yet** — 24 options to narrow down. Need group discussion to pick 2-3 for design development
- **No prototypology defined yet** — last handoff mentioned "rail-mounted module that transforms through 24h cycle" but no design work started
- **No QGIS visualization of these sites** — could map them as a layer with the data signals as attributes
- **The Lausanne perpendicular (Site 10) raises a conceptual question**: what does a "horizontal elevator" become on a 250m altitude gradient? This could be the most architecturally interesting site
- **Station reviews contain user experience evidence** — "arrived at 12:38am to a ghost station" (Lausanne), "too dangerous" (Vigie), "elevators always broken" (Vigie). Could feed into design brief
- **Datasets exhausted** — remaining uncovered communes are <2,000 pop or well-served. The 15 CSVs have been fully cross-referenced

## Key decisions made (cumulative)
- Narrative: the rail line as 24-hour living infrastructure (decided Session 2, 23-02, Cadence)
- Two halves: Train Desk (day) + Gap Hours (night) (decided 23-02)
- Group work confirmed — working as a team (decided 23-02)
- Prototypology direction: adaptive module, work pod by day, rest/transport pod by night (proposed 23-02, not yet developed)
- 24 candidate sites identified and tiered (this session, 08-03, Meridian)

## Technical notes
- **All analysis run in Python** against project CSVs in `/mnt/project/`
- **CRS**: Data is in WGS84 (lat/lon) in the CSVs. QGIS project uses LV95/EPSG:2056 — conversion needed if mapping
- **Haversine distances used** — approximate, sufficient for site identification. Road/rail distances would differ
- **Buildings dataset**: 218,437 records in `city101_buildings_classified.csv` — used for building use category ratios per commune
- **Ridership hourly curves**: `station_ridership_v2.csv` has pct_h00 through pct_h23 — could generate 24h ridership profiles per station
- **Station reviews**: `city101_station_REVIEWS.csv` — 71 reviews with sentiment, accessibility, safety flags. Vigie (2.9★) and Bourdonnette (3.6★, "too dangerous") are notable
- **Output files on Claude container** (will need re-export if needed in future session):
  - `/mnt/user-data/outputs/city101_horizontal_elevator_24_sites.jsx`
  - Earlier versions: `_sites.jsx`, `_12_sites.jsx`, `_18_sites.jsx`
  - Python analysis scripts: `/home/claude/site_analysis.py`, `deep_sites.py`, `deeper_sites.py`, `round3.py`, `round3b.py`, `round4.py`, `round4_deep.py`

## Data sources (this session)
- Site identification: cross-reference of all 15 project CSVs, 08.03.26
- Datasets used (all pre-existing in project):
  - `city101_population_distribution_24h.csv` — day/night population swings per commune
  - `city101_work_locations.csv` — 73 employment nodes with employee estimates
  - `city101_night_workers.csv` — 51 night worker locations with shift times
  - `city101_residencies_professions_neighbourhoods.csv` — 147 residential areas with professions, income, foreign %
  - `city101_nocturnal_transport_stops.csv` — 146 stops, 95 with no nocturnal service
  - `city101_late_night_venues_v3.csv` — 133 venues with closing times
  - `city101_ridership_sbb.csv` — daily/workday/weekend ridership + commuter index
  - `station_ridership_v2.csv` — hourly ridership curves (pct per hour)
  - `city101_service_frequency_v2.csv` — trains per hour, wait times
  - `city101_shared_mobility.csv` — 2,062 shared mobility stations
  - `city101_remote_work_places.csv` — 68 coworking/café locations
  - `corridor_demographics_v2.csv` — commute mode split, frontalier estimates
  - `corridor_station_distances_v3.csv` — station-to-station gaps along corridor
  - `thomasriegertpublichospitals.csv` — 23 hospitals with rail distances
  - `city101_buildings_classified.csv` — 218,437 buildings with use categories
  - `city101_station_REVIEWS.csv` — 71 Google reviews with sentiment analysis
  - `city101_station_ratings.csv` — 37 stations with Google ratings
