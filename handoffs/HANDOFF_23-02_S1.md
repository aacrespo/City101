# HANDOFF — 23-02 Session 1 (Lumen)

## Last action
Created a new dataset layer: **remote-work-friendly places** along the City101 corridor. Used Google Places to collect 68 venues (coworking, cafés, libraries), then mined 109 review snippets for remote work sentiment. Two CSVs produced. This is a third dataset for A.01, complementing EV charging and WiFi/invisible flows.

---

## Current state

### Dataset 1 — Electric Charging ✓ COMPLETE (from previous sessions)
- `city101_ev_charging_ENRICHED_v3.csv` — 194 rows, 53 columns
- Sources: Google Places + OSM + DIEMO + OpenChargeMap
- 7 OCM reviews in `city101_ev_charging_REVIEWS.csv`

### Dataset 2 — Invisible Data Flows ✓ LAYERS BUILT (from 22-02 S3)
- `city101_wifi_MERGEDv3.csv` — 81 WiFi points
- `city101_cell_towers.csv` — 3,218 BAKOM towers
- `city101_international_anchors.csv` — 15 anchors
- QGIS: 10 layers loaded and styled, print layouts NOT yet built

### Dataset 3 — Remote Work Places ✓ NEW THIS SESSION
- **`city101_remote_work_places.csv`** — 68 rows, 9 columns
  - 35 coworking spaces, 25 cafés, 8 libraries
  - Columns: name, latitude_wgs84, longitude_wgs84, place_type, google_rating, google_review_count, address, municipality, google_place_id
  - Sorted west→east by longitude
  - Coordinates: WGS84 (needs LV95 conversion for QGIS)
  - Source: Google Places searches across 11 corridor zones

- **`city101_remote_work_REVIEWS.csv`** — 109 rows, 8 columns
  - Columns: place_name, municipality, place_type, google_place_id, review_text, tags, is_work_relevant, sentiment
  - 87 of 109 reviews tagged as work-relevant (80%)
  - Tags include: work_relevant, mentions_transit, mentions_wifi, mentions_noise, mentions_lake_nature, mentions_community, mentions_study, mentions_power, mentions_devices, pain_point
  - Linkable to places CSV via google_place_id

---

## KEY FINDINGS — Remote Work Review Mining

### 1. Distribution confirms the two-speed corridor
| Municipality | Places | Reviews |
|---|---|---|
| Genève | 18 | 42 |
| Lausanne | 17 | 31 |
| Vevey | 8 | 7 |
| Montreux | 6 | 6 |
| Nyon | 4 | 5 |
| Morges | 4 | 5 |
| Versoix | 2 | 2 |
| Rolle | 2 | 2 |
| Collex-Bossy | 1 | 2 |
| Préverenges | 1 | 2 |
| Pully | 1 | 1 |
| Lutry | 2 | 2 |
| Gland | 1 | 1 |
| Villeneuve | 1 | 1 |

Geneva + Lausanne = 35 of 68 places (51%), 73 of 109 reviews (67%). Villeneuve has 1 venue — a lakefront restaurant, not a workspace.

### 2. The lake-work paradox is confirmed by user voice
12 reviews explicitly mention BOTH working AND lake/nature proximity. They cluster almost entirely in Geneva's western corridor:
- **Spaces Nations** (Geneva, 4 mentions): "Location near the lake is a huge plus if you want to go on walks during breaks"
- **Society Coworking** (Morges): "1 min walk to the lake, friendly atmosphere, free food, bikes, paddle surf"
- **Coworking Montreux**: "literally on the platform of Montreux train station and a 2-minute walk from the lake"
- **TheWorkHub Vevey**: "A truly international community... nice view towards the mountains"

East of Morges, the work+lake overlap nearly disappears. People *want* to work near the lake — the infrastructure only delivers it in Geneva and a few western nodes.

### 3. Transit proximity dominates how places market themselves
32 of 109 reviews mention transit (train station, metro, transport). Coworking spaces are measured by walking distance to the station:
- Coworking Montreux: "literally on the platform"
- PepperHub Gland: "just steps from the station"
- Gotham Lausanne: "2 minutes walk from the Lausanne train station"
- Impact Hub Geneva: "near Cornavin station"

**Implication for invisible flows argument:** The rail line is the coworking backbone. Workspaces cluster at station nodes. Between stations = desert. The linear corridor forces this — there's no grid of alternatives.

### 4. WiFi is mentioned casually in west, desperately in east
14 reviews mention WiFi/internet:
- **Geneva/Lausanne pattern** (casual): "Free Wi-Fi, password on the counter" (Boréal), "fast Wi-Fi" (Open Space, Tchalo)
- **Vevey pattern** (urgent): "Walked in and asked for wifi and the owner gave me, even before I ordered" (Café La Belle Epoque)
- **Pain point**: "WiFi barely works, so had to hot spot off my phone for the day" (Voisins Saint-Gervais, Geneva — even Geneva has gaps)
- **Infrastructure failure**: "GSM connection is virtually non-existent in the building" (Gotham Flon, Lausanne — cellular dead zone inside a coworking space)

### 5. Only 3 reviews mention power outlets
- Boréal (Geneva): "Lots of plugs for laptops/phones"
- Sleepy Bear (Lausanne): "You have plugs if you want to stay in and work"
- Spaces (Geneva, billing context, not plugs)

Power outlets are barely visible in the review discourse. Either they're assumed (coworking) or absent (cafés). This connects directly to the EV charging insight: energy access infrastructure is invisible until it fails.

### 6. The Lavaux gap is absolute
Zero places found. Zero reviews. Between Lutry (lon 6.69) and Vevey (lon 6.84) — a 15km stretch — there is not a single coworking space, work-friendly café, or library. The UNESCO vineyard terraces are a complete remote work void, confirmed now from three data angles:
- WiFi coverage: zero (from dataset 2)
- Remote work venues: zero (from dataset 3)
- User voice: silence (from review mining)

### 7. Pain points cluster around two themes
13 reviews flagged as pain points:
- **Connectivity failures**: WiFi not working, GSM dead, no signal
- **Privacy/noise**: "no ability to make a call without the whole room hearing it" (Regus Flon), "not the best silent place to work" (Impact Hub Geneva)

These mirror the EV charging experience audit findings — infrastructure designed for a function (desks, power) but not for the human reality of how work happens (calls, focus, connectivity).

### 8. Sentiment is overwhelmingly positive (selection bias)
96 positive, 3 negative, 2 mixed. This reflects Google Reviews self-selection — people review places they like. The negative reviews are more analytically interesting because they reveal structural gaps rather than service complaints.

### 9. The "international" signal
Several reviews explicitly reference international/mobile workers:
- "A truly international community" (TheWorkHub Vevey)
- "Having moved from London to Nyon and needing a professional, comfortable and clean environment" (Atelier 9)
- "People from all over" (Regus Versoix)
- "I can work from home from many different cities and countries" (Regus Lausanne)

This is the permanently transient international from the invisible flows narrative — showing up unprompted in the review data.

---

## HOW THIS CONNECTS TO THE PIN-UP NARRATIVE

### For Electric Charging maps
No direct connection this session, but the "architecture of waiting" framing (charge time = dwell time = urban program) is reinforced by remote work patterns. Some EV charging stations are near coworking/cafés = designed dwell. Most are not = dead time.

### For Invisible Data Flows maps
This dataset is the human evidence layer for the WiFi desert argument:
- **Quantitative**: 68 places, distributed 51% in two cities
- **Qualitative**: review text shows people seeking connectivity, measuring venues by WiFi quality, walking distance to stations
- **The Lavaux paradox**: not just a WiFi desert but a remote work desert, confirmed by total absence of venues — on the daily route of some of the world's most connected people

### Potential map addition
If time permits, overlaying remote work venues on the WiFi/cell tower map would show the correlation between connectivity infrastructure and where people can actually work. The gap in Lavaux would be visually absolute — no dots of any kind.

---

## Files produced this session
| File | Location | Rows | Columns |
|---|---|---|---|
| city101_remote_work_places.csv | outputs/ | 68 | 9 |
| city101_remote_work_REVIEWS.csv | outputs/ | 109 | 8 |

Both files need LV95 coordinate conversion before QGIS loading.

---

## Open threads — PRIORITY ORDER

### For pin-up (TODAY)
1. **QGIS print layouts** — still not built (from 22-02 S3). This is the critical path item.
2. **Load remote work places in QGIS** — optional bonus layer, needs LV95 conversion
3. **Print at FAR studio**

### After pin-up
4. **Google Places reviews batch fetch** — the 109 reviews here are snippets from search results. Full review text harvest (hundreds more) possible via Places API on this account
5. **LV95 conversion script** — for remote work places CSV
6. **Cross-analysis** — overlay EV charging dwell contexts with remote work venue proximity (which charging stations are near workable places?)
7. **Review text NLP** — deeper sentiment analysis, topic modeling across all three review corpora (EV, WiFi, remote work)

---

## Key decisions made (cumulative)
- Framing: "flow of people" (EV) + "invisible data flows" (WiFi/infrastructure)
- EV charging → architectural lens: charge duration creates spatial program
- Invisible flows → the permanently transient international on a linear corridor
- Lavaux desert = deliberate policy choice, not technical failure
- Remote work places = human evidence layer for WiFi/connectivity argument
- Review mining confirms: lake-work paradox, transit-as-backbone, east-west digital divide
- The thinking is for you; the map is for them
- LV95 / EPSG:2056 working CRS throughout
- Monolithic scripts for large data operations
- Original CSVs preserved as raw sources of truth

## Technical notes
- Remote work places: collected via Google Places search tool across 11 corridor zones × 4 search queries each
- Review mining: keyword-based tagging (work_relevant, mentions_wifi, mentions_transit, etc.) + simple sentiment classification
- No API keys needed — Google Places integration is account-bound on Lumen
- Deduplication by google_place_id
- Coordinates are WGS84 — need pyproj or QGIS reproject for LV95

## Data sources (this session)
- Google Places search results: 68 venues across City101 corridor (23.02.26)
- Google Places review snippets: 109 reviews extracted from search results (23.02.26)
