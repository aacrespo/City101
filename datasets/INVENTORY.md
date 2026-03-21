# Dataset Inventory

All verified production datasets. Updated when data changes.

---

## Corridor Analysis (the core)

| Dataset | File | Rows | Key columns |
|---------|------|------|-------------|
| WCI segments | `corridor_analysis/city101_corridor_segments_WCI.csv` | 49 | station, WCI score, 5 dimensions |
| Break points | `corridor_analysis/city101_break_points.csv` | 49 | 5 break dimensions, severity |
| Journey workability | `corridor_analysis/city101_journey_workability.csv` | 618 | per-connection workability rating |
| Journey summary | `corridor_analysis/city101_journey_workability_summary.csv` | 35 | OD pair aggregates |
| Train workability | `corridor_analysis/city101_train_workability.csv` | 49 | IC/IR vs R/S ratio |
| Classmate crossref | `corridor_analysis/city101_station_crossref_classmates.csv` | 49×46 | 2,093 points from 33 datasets, Shannon diversity |
| GA cost OD pairs | `corridor_analysis/city101_ga_cost_od_pairs.csv` | 35 | full/halbtax/GA prices |
| GA cost corridor | `corridor_analysis/city101_ga_cost_corridor.csv` | 49 | cumulative cost from Geneva |
| Temporal frequency | `corridor_analysis/city101_temporal_frequency.csv` | 49×28 | 7 time slots, trains/hr + IC + deps |
| Temporal WCI | `corridor_analysis/city101_temporal_WCI.csv` | 49×~50 | TWCI per station × 7 slots + first/last |
| Temporal summary | `corridor_analysis/city101_temporal_summary.csv` | 7 | per-slot aggregates |
| First/last trains | `corridor_analysis/city101_first_last_trains.csv` | 49 | service windows |
| Modal diversity | `corridor_analysis/city101_modal_diversity.csv` | 49 | 11 transport modes, modal Shannon |

## Zurich Comparison

| Dataset | File | Rows | Key columns |
|---------|------|------|-------------|
| S8 lakeside | `zurich_comparison/zurich_sbahn_comparison.csv` | 12 | S8 stations with City101 analogs |
| Metrics | `zurich_comparison/zurich_comparison_metrics.csv` | 15 | structural comparison metrics |

## EV Charging (supporting evidence)

| Dataset | File | Rows | Key columns |
|---------|------|------|-------------|
| Enriched v3 | `ev_charging/city101_ev_charging_ENRICHED_v3.csv` | 194 | 53 cols, DIEMO + distances + context |
| Reviews | `ev_charging/city101_ev_charging_REVIEWS.csv` | 109 | sentiment-tagged |
| National stats | `ev_charging/swiss_charging_keyfigures_monthly.csv` | 63mo | monthly 2020–2026 |

## Remote Work / Connectivity

| Dataset | File | Rows | Key columns |
|---------|------|------|-------------|
| Places | `remote_work/city101_remote_work_places.csv` | 68 | Google-sourced with place_ids |
| Hours | `remote_work/city101_remote_work_HOURS.csv` | 63 | 14 are 24h, 18 weekdays-only |
| Reviews | `remote_work/city101_remote_work_REVIEWS.csv` | 109 | work-relevance tagged |
| Crossref | `remote_work/city101_remote_work_CROSSREF.csv` | 68 | 31 cols: train, frequency, WiFi, acoustics |
| WiFi | `remote_work/city101_wifi_MERGEDv3.csv` | 81 | quality scores, categories, clusters |
| Cell towers | `remote_work/city101_cell_towers.csv` | 3,218 | 3G/4G/5G BAKOM |
| International anchors | `remote_work/city101_international_anchors.csv` | 15 | CERN, UN, IOC, etc. |

## Transit

| Dataset | File | Rows | Key columns |
|---------|------|------|-------------|
| Frequency v2 | `transit/city101_service_frequency_v2.csv` | 49 | trains/hr, IC vs regional |
| Ridership | `transit/city101_ridership_sbb.csv` | 174 | daily pax, commuter index |
| Shared mobility | `transit/city101_shared_mobility.csv` | 2,062 | 8 providers |

## Station Quality

| Dataset | File | Rows | Key columns |
|---------|------|------|-------------|
| Ratings | `stations/city101_station_ratings.csv` | 37 | Google ratings for M2, M1, Léman Express, CGN |
| Reviews | `stations/city101_station_REVIEWS.csv` | 71 | tagged by theme |

## Late-Night Venues

| Dataset | File | Rows | Key columns |
|---------|------|------|-------------|
| Late night v3 | `24h_venues/city101_late_night_venues_v3.csv` | — | 24h and late-closing venues |

## Healthcare ⚠️ UNVERIFIED

| Dataset | File | Rows | Key columns |
|---------|------|------|-------------|
| Hospitals corridor | `healthcare/city101_hospitals_corridor_research.csv` | 32 | id, name, city_commune, type, address, lat_wgs84, lon_wgs84, canton, beds, notes, source, in_riegert_data |

---

## Not yet integrated (available in `source/00-datasets 2/`)

See CLAUDE.md Tier 2 inventory for full list of classmate datasets awaiting integration.
