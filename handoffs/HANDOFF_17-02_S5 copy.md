# HANDOFF — 17-02 Session 5

## Last action
Ran Script 2 (distances + context classification) on the 27-column enriched CSV. Output: 34-column `city101_ev_charging_ENRICHED_v2.csv`. Attempted to test new network domains for reviews collection — none active yet.

## Current state
- **ENRICHED_v2.csv** — 194 rows, 34 columns (27 from DIEMO enrichment + 7 new)
- **Script saved**: `enrich_distances_context.py` — re-runnable, pure Python, no dependencies
- **Network domains**: `api.openchargemap.io`, `chargemap.com`, `plugshare.com`, `maps.googleapis.com` — Andrea added them but they're not yet active (all returning `host_not_allowed`). Need to verify settings or start new conversation for them to apply.

### New columns added this session (Script 2)
| Column | Coverage | Notes |
|--------|----------|-------|
| distance_to_lake_m | 194/194 | Min: 11m, Max: 9098m, Avg: 1905m |
| distance_to_transit_m | 194/194 | Min: 27m, Max: 9127m, Avg: 1497m |
| nearest_transit_name | 194/194 | Name of closest train/metro station |
| distance_to_nearest_station_m | 194/194 | Min: 2m, Max: 4657m, Avg: 512m |
| location_type | 194/194 | 59 unknown, 43 street, 43 surface_lot, 22 car_sharing_hub, 11 underground_parking, 5 highway_rest, 4 commercial_retail, 4 institutional, 2 hotel, 1 car_dealer |
| sheltered | 194/194 | 22 TRUE, 91 FALSE, 81 uncertain (derived from location_type) |
| dwell_context | 194/194 | 71 transit, 39 errands_mixed, 39 unknown, 23 residential_substitute, 8 recreation, 4 shopping, 4 highway_stop, 3 work, 1 dining, 1 overnight, 1 car_service |

### Key findings
- **Lakeside disconnect quantified**: average station is 1.9km from the lake. Closest: Plenitude On The Road in La Tour-de-Peilz (11m). Farthest: evpass Begnins (9.1km)
- **Most isolated station**: evpass Begnins (4.7km from any other station)
- **Sheltered logic confirmed**: underground_parking / commercial_retail / hotel / institutional / car_dealer → sheltered=TRUE. Street / surface_lot / highway → FALSE. No need for "manual" tagging.
- **Classification accuracy**: ~60-70% estimated. 59 unknown location_types and 39 unknown dwell_contexts need review

### What's NOT yet in the CSV (per proposed_schema.md)
**Needs API access (domains not yet working):**
- google_rating, google_review_count → needs `maps.googleapis.com`
- chargemap_rating, chargemap_review_count → needs `chargemap.com`
- Open Charge Map cross-reference → needs `api.openchargemap.io`

**Separate file — Reviews CSV (not yet started):**
- `city101_ev_charging_REVIEWS.csv` — one row per review
- Schema: station_id, platform, date, rating, language, review_text, dwell_mentions, pain_point_tags, sentiment
- Key insight from Andrea: reviews don't have to be station-specific — regional reviews, operator-level reviews, and general corridor commentary all count as human experience data
- The audit document (EV_charging_experience_audit.md) has rich qualitative analysis but didn't capture the raw review data — next scripts should capture both

**Still missing:**
- mobile_signal (no data source)
- floor_level (no data source — truly manual)
- parking_fee, parking_max_hours (partial from reviews)
- nearby_amenities (OSM POI queries possible via OSM MCP)
- sentiment_tags (derivable once reviews are collected)

## Open threads — PRIORITY ORDER
1. **Fix network domains** — verify `api.openchargemap.io`, `chargemap.com`, `plugshare.com`, `maps.googleapis.com` are in allowed list. May need new conversation to take effect.
2. **Reviews collection script** — once domains work, build monolithic script to fetch reviews from Open Charge Map + Chargemap. Capture raw data this time (the audit went to analysis without preserving source data).
3. **Google ratings enrichment** — once `maps.googleapis.com` works (needs API key from Andrea)
4. **OSM nearby amenities** — can do now via OSM MCP tools, no new domains needed
5. **Spot-check classifications** — 59 unknown location_types, 39 unknown dwell_contexts need human review
6. **Second dataset for A.01** (due 23.02) — still need the "straightforward" dataset
7. **Pin-up map outputs** — need actual QGIS map compositions for Monday
8. **Load ENRICHED_v2 in QGIS** — replace old layer, restyle with new fields

## Key decisions made (cumulative)
- Framing: "flow of people" not energy (energy = Siméon's territory)
- EV charging analyzed through human experience lens
- LV95 / EPSG:2056 as working coordinate system
- LOG/LOI/LOD framework adopted (see 00_Workflow_v02.md)
- LOI principle: "Work rich, export lean"
- Two-CSV architecture: stations + reviews (reviews not yet created)
- DIEMO as primary enrichment source for technical data ✓ DONE
- Script 2 pattern: distances computed from hardcoded polylines + station lists (no API needed)
- Sheltered = derived from location_type, not manual
- Reviews are the human voice — most important remaining dataset
- Reviews can be regional/operator-level, not only station-specific
- Monolithic script pattern: fetch → process → write → summary only

## Technical notes
- Script 2 path: `/home/claude/enrich_distances_context.py` (also in outputs)
- Lake shore: 48-point polyline from Geneva to Villeneuve, traced along northern coast
- Transit stations: 38 entries (CFF main line + Lausanne M1/M2 + Geneva tram/CEVA)
- Distance to lake uses point-to-segment projection (not just point-to-point)
- All distance calculations in WGS84 with haversine + local flat-earth projection for segments
- Some municipality labels may be off (e.g., stations near Founex showing "Genève") — inherited from original CSV

## Data sources (this session)
- Lake shoreline polyline: manually traced from map, 48 points Geneva→Villeneuve (17.02.26)
- Transit stations: CFF timetable + Lausanne Metro + Geneva CEVA, 38 stations (17.02.26)
- Classification heuristics: keyword matching on name, address, operator, accessibility_type fields
