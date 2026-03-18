# HANDOFF — 22-02 Session 2

## Last action
Fetched BAKOM national cell tower dataset (22,138 towers → 3,218 filtered to corridor), created `city101_cell_towers.csv`. Loaded 3 layers into QGIS: Cell Towers, WiFi v3, EV Charging v3 (swapped out old 16-col version). Project saved. Began thinking about pin-up representation strategy — session ended before going into that or researching Xavier Comtesse.

## Current state

### QGIS layers (all live, project saved)
| Layer | Features | File |
|---|---|---|
| City101_CellTowers | 3,218 | `city101_cell_towers.csv` |
| City101_WiFi | 81 | `city101_wifi_MERGEDv3.csv` |
| City101_EV_Charging_v3 | 194 | `city101_ev_charging_ENRICHED_v3.csv` |
| + all Swisstopo base layers | — | unchanged |

All layers loaded as EPSG:4326 memory layers (QGIS reprojects to LV95 on the fly). **No styling applied yet to new layers** — default single symbol.

### Datasets complete (LOI status)
**EV Charging** — `city101_ev_charging_ENRICHED_v3.csv`, 194 rows, 53 cols
- Sources: Google Places + OSM + DIEMO + OpenChargeMap
- Key fields: dwell_context, location_type, sheltered, distance_to_lake_m, distance_to_transit_m, charge_level, power_kw
- Missing: Google ratings (blocked), OCM reviews sparse (7 total)

**WiFi** — `city101_wifi_MERGEDv3.csv`, 81 rows, 23 cols
- Sources: SITG Geneva (6pts), SBB (7pts), Lausanne (5pts), Google Places (24pts), research (rest)
- Key fields: wifi_category, wifi_quality_score, connectivity_cluster, wifi_desert, day_pass_chf
- Key insight: Lavaux = most dramatic WiFi desert. Geneva ★★★★★ → Villeneuve ★☆☆☆☆
- Missing: OSM Overpass (blocked), SITG full 568-pt dataset (blocked), Lausanne Citycable full list
- Note: 81 pts is under-populated — desert zones partly reflect missing data, not just absence

**Cell Towers** — `city101_cell_towers.csv`, 3,218 rows, 14 cols
- Source: BAKOM/geo.admin.ch federal dataset (already in LV95 coords)
- Key fields: operator, technology (3G/4G/5G), power_class, has_5g, has_4g
- Operators: Swisscom 1,441 | Salt 1,076 | Sunrise 590 | SBB 111
- 5G-capable: 2,012 towers (63%) — 5G rollout frontier is mappable along corridor
- This is a new analytical layer not originally planned — richer than WiFi hotspots

### Two conceptual categories for pin-up
1. **Invisible Data Flows** — WiFi (81pts) + Cell Towers (3,218pts)
2. **Electric Charging / Flow of People** — EV Charging (194pts)

## Open threads — PRIORITY ORDER

### TONIGHT (before pin-up)
1. **Research Xavier Comtesse** — originator of City101 concept; tailor presentation to his framing
2. **Decide pin-up maps** — which views, which representations, what each map argues
3. **Style all 3 layers in QGIS** — heatmap / categorized / graduated TBD
4. **Export A2+ prints** — render from QGIS, print at FAR studio printer

### Styling options discussed (not yet chosen)
- Cell towers: heatmap (density), or rule-based by technology gen (grey=4G, cyan=5G)
- WiFi: categorized by wifi_category (shape=type, size=quality_score), or heatmap showing desert
- EV: categorized by dwell_context (color), graduated by distance_to_lake_m

### Soon after pin-up
- OSM/SITG data gaps — if network access restored, re-run wifi fetch to ~200+ points
- Add data centers as 4th invisible flows layer
- EV Google ratings batch fetch (this account has Places API)

## Key decisions made (cumulative)
- Framing: "flow of people" (EV charging) + "invisible data flows" (WiFi + cell towers)
- EV charging → human experience lens (dwell_context, not kW specs)
- LV95 / EPSG:2056 working CRS
- LOG/LOI/LOD framework: "work rich, export lean"
- Monolithic scripts for large data ops (no interactive exploration)
- Cell towers = valid invisible infrastructure layer (added this session)
- WiFi 81-pt dataset is analytically valid but should note data gap caveat in presentation

## Technical notes
- QGIS project: `/Users/andreacrespo/Documents/EPFL cours/Archi/3ème/BA6/PROJECT/Assignement 1/CITY101_TESTS_Charging stations_dots and colors.qgz`
- Cell towers file: `/Users/andreacrespo/Documents/EPFL cours/Archi/3ème/BA6/PROJECT/Assignement 1/invisible flows/city101_cell_towers.csv`
- WiFi file: same folder, `city101_wifi_MERGEDv3.csv`
- EV file: `/Users/andreacrespo/Documents/EPFL cours/Archi/3ème/BA6/PROJECT/Assignement 1/Charging station csv/city101_ev_charging_ENRICHED_v3.csv`
- Script: `enrich_wifi_v3.py` in invisible flows folder
- BAKOM cell tower source: `https://data.geo.admin.ch/ch.bakom.standorte-mobilfunkanlagen/...`
- OCM API key: `23617e07-95e4-4666-b1f6-f4dfcd6a8e64`

## Data sources (this session)
- Cell towers: BAKOM via geo.admin.ch STAC API (22.02.26)
- WiFi v3: minor schema update only (google_place_id column added), no new points
- EV v3: loaded into QGIS, no new data

## Next session should start with
→ Research Xavier Comtesse + City101 concept origins
→ Then decide pin-up map set and style in QGIS
