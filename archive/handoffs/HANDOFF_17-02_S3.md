# HANDOFF — 17-02 Session 3

## Last action
Cross-session checkpoint. Verified QGIS project state against work done on other account. Confirmed CSV is still the original 16-column version — enrichment from other session was planned but not yet executed.

## Current state
- **QGIS project**: `CITY101_TESTS_Charging stations_dots and colors.qgz` (EPSG:2056)
- **CSV loaded**: `city101_ev_charging_MERGED.csv` — 194 rows, 16 columns (ORIGINAL, not enriched)
- **QGIS styling**: Rule-based renderer already applied with 6 categories:
  - Micro-mobility (e-bike/scooter connectors)
  - Car-sharing Fleet (operator = 'mobility') — 24 stations
  - Fast / Transit (CCS, CHAdeMO, Tesla, high-power connectors)
  - Slow / Destination (Type2, Type1, CEE, plus known AC operators)
  - Mixed Network (Shell Recharge, MOVE, Migrol with null connectors)
  - Unknown (catch-all)
- **Data gaps in current CSV**:
  - operator: 44 nulls / 194
  - network: 110 nulls / 194
  - connectors: 116 nulls / 194
  - capacity: 95 nulls / 194
  - address: 104 nulls / 194

## Work completed on other account (not yet in files)
1. **EV Charging Experience Audit** (saved as `EV_charging_experience_audit.md`)
   - Deep qualitative research on user experience along City101 corridor
   - 9 recurring pain points identified (payment fragmentation, phantom stations, underground parking disorientation, Lausanne macaron trap, missing cables, broken chargers, vampire cars, ICEing, spatial disconnect from lake)
   - Dwell behavior analysis (productive wait vs. dead time)
   - Academic frameworks: sentient city (Shepard), third place paradigm, multifunctional mobility hubs
   - Key insight: "infrastructure that knows about kilowatts but nothing about people"

2. **Proposed Enriched Schema** (saved as `proposed_schema.md`)
   - Expands from 16 → 36 columns across 4 layers:
     - Layer 1: Existing (fill gaps from DIEMO)
     - Layer 2: Technical — power_kw, charge_level, is_24h, auth_method, pricing_chf_kwh, diemo_station_id
     - Layer 3a: Location Context — location_type, floor_level, sheltered, mobile_signal, parking_fee, parking_max_hours
     - Layer 3b: Human Experience — google_rating, chargemap_rating, review counts, dwell_context, nearby_amenities, distance_to_lake_m, distance_to_transit_m, sentiment_tags

3. **Two-CSV architecture decision**
   - File 1: `city101_ev_charging_ENRICHED.csv` — one row per station, ~36 columns
   - File 2: `city101_ev_charging_REVIEWS.csv` — one row per review, linked by station_id
   - Reviews schema: station_id, platform, date, rating, language, review_text, dwell_mentions, pain_point_tags, sentiment

4. **DIEMO data fetch initiated** — found the direct download URL (`data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/...`) but session ended before enrichment could be applied

## Open threads — PRIORITY ORDER
1. **Fetch DIEMO data and enrich the CSV** — this is the immediate next step. Fill gaps in operator, network, connectors, capacity, address + add new technical columns (power_kw, charge_level, is_24h, etc.)
2. **Dwell context classification** — manual/semi-manual tagging of 194 stations by what people do while charging (shopping, dining, transit, work, recreation, residential, highway, none)
3. **Second dataset for A.01** (due 23.02) — need one "straightforward" + one "creative" dataset per person. EV stations = creative. Still need the straightforward one.
4. **Reviews CSV** — scraping/collecting reviews from Google, Chargemap, PlugShare — significant effort, may be lower priority for A.01
5. **QGIS distance calculations** — distance_to_lake_m and distance_to_transit_m can be computed once enriched CSV is loaded
6. **Sentient city narrative** — the audit gives rich material but needs to be articulated as a design argument

## Key decisions made (cumulative)
- Framing: "flow of people" not energy (energy = Siméon's territory)
- EV charging analyzed through human experience lens
- LV95 / EPSG:2056 as working coordinate system
- LOG/LOI/LOD framework adopted (see 00_Workflow_v02.md)
- LOI principle: "Work rich, export lean" — collect all attributes, filter for output
- Two-CSV architecture for stations + reviews
- DIEMO (Swiss federal registry) as primary enrichment source for technical data
- Proposed 36-column schema for enriched stations file
- Rule-based QGIS styling by charging typology (already implemented)

## Technical notes
- QGIS project file: `~/Documents/EPFL cours/Archi/3ème/BA6/PROJECT/Assignement 1/CITY101_TESTS_Charging stations_dots and colors.qgz`
- CSV source path: same directory, `city101_ev_charging_MERGED.csv`
- DIEMO download URL: `https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/oicp/ch.bfe.ladestellen-elektromobilitaet.json` (to verify)
- 00_Workflow_v02.md: `/mnt/project/00_Workflow_v02.md`
- Top operators by count: Shell Recharge (30), Mobility (24), MOVE (20), evpass (18), Migrol (6), eCarUp (5), GreenMotion (5)
- Some operator name inconsistencies: "Energie 360°" vs "Energie360°", "GreenMotion" vs "Greenmotion", "MOVE" vs "Move", "Lausanne SiL" vs "SiL"

## Data sources (this session)
- EV_charging_experience_audit.md: compiled from Google reviews, Chargemap, Asphalte.ch, RTS A Bon Entendeur, TCS studies, academic papers, François Cuneo blog, Reddit, TMC forums (17.02.26)
- proposed_schema.md: designed based on audit findings + DIEMO field analysis (17.02.26)
