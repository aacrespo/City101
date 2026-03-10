# opendata.swiss Trawl — Categorized Analysis

*Reviewed by Cairn, 01-03-2026. Based on top 50 from phase 2+3 trawl.*

Your narrative: **"working continuity as a flow"** — how infrastructure along the Geneva–Villeneuve corridor supports (or fails to support) continuous work, charging, connectivity, and movement.

---

## 🔥 TIER 1 — Direct hits (download these)

### EV Charging & Electric Mobility
These directly enrich or extend your existing 194-station dataset:

| # | Dataset | Why it matters | Format |
|---|---------|---------------|--------|
| **7** | [Bornes de recharge véhicules électriques (CFF)](https://opendata.swiss/en/dataset/ladestationen) | Real-time availability of charging stations — adds temporal dimension to your static dataset | JSON |
| **27** | [Chiffres-clés infrastructure de recharge](https://opendata.swiss/en/dataset/kennzahlen-offentliche-ladeinfrastruktur-elektromobilitat) | National charging infrastructure statistics — benchmark corridor vs national | CSV, JSON |
| **35-37** | Charging point projections 2035 (3 scenarios: Planned/Flexible/Comfortable) | Future infrastructure demand per commune — where will gaps persist? | CSV, GPKG, WMS |
| **41-43** | Home charging availability 2035 (3 scenarios) | % of EV owners WITHOUT home charging — who depends on public infra? | CSV, GPKG, WMS |
| **44** | [Besoin de recharge: parc véhicules 2035](https://opendata.swiss/en/dataset/ladebedarf-bestand-an-steckerfahrzeugen-fur-das-jahr-2035) | EV fleet size projections per commune — demand side | CSV, GPKG, WMS |

**Why these matter together**: Your current dataset shows where charging IS. These show where it WILL NEED TO BE and who won't have home charging. The gap between current reality and 2035 projections = your index of infrastructure readiness per commune. Very strong for the A02 narrative.

### Mobility & Dwell Infrastructure
| # | Dataset | Why it matters | Format |
|---|---------|---------------|--------|
| **28** | [Géolocalisation mobilité partagée (temps réel)](https://opendata.swiss/en/dataset/standorte-und-verfugbarkeit-von-shared-mobility-angeboten) | E-bikes, scooters, carshare — what you do AFTER you park/charge | JSON, API |
| **25** | [Mobilité douce — La Suisse à vélo](https://opendata.swiss/en/dataset/langsamverkehr-veloland-schweiz) | Cycling infrastructure — soft mobility alternative to car | WMS |
| **5** | [Mobilier urbain Lausanne](https://opendata.swiss/en/dataset/mobilier-urbain) | Public benches = dwell quality at stops. Can you sit while you charge? | CSV, SHP |
| **19** | [RefPU Passage Mobilité Douce (Geneva)](https://opendata.swiss/en/dataset/refpu-passage-mobilite-douce-ligne) | Soft mobility paths in Geneva — pedestrian/bike infrastructure | WFS |

### Noise & Environmental Context
| # | Dataset | Why it matters | Format |
|---|---------|---------------|--------|
| **11** | [Bruit trafic ferroviaire (jour)](https://opendata.swiss/en/dataset/larmbelastung-durch-eisenbahnverkehr-lr_tag) | Rail noise exposure — acoustic quality at stations/charging points. Also covers Zurich! | WMS |
| **38** | [Bruit trafic ferroviaire (nuit)](https://opendata.swiss/en/dataset/larmbelastung-durch-eisenbahnverkehr-lr_nacht) | Same but nighttime. Also covers Zurich! | WMS |

---

## ⚡ TIER 2 — Good for cross-referencing or context

### Parking & Road Infrastructure (supports "program of stopping")
| # | Dataset | Why it matters | Format |
|---|---------|---------------|--------|
| **1** | [Signalisation et stationnement Morges](https://opendata.swiss/en/dataset/signalisation-et-stationnement) | Parking infrastructure — where stopping is designed vs improvised | GPKG |
| **2** | [Stationnement Lausanne](https://opendata.swiss/en/dataset/stationnement) | Public parking data — complements EV charging | CSV, SHP |
| **4** | [Horodateur Lausanne](https://opendata.swiss/en/dataset/horodateur) | Parking meters = temporal pricing of stopping. How long CAN you stop? | CSV, SHP |
| **6** | [Hiérarchie routière Lausanne](https://opendata.swiss/en/dataset/hierarchie-routiere) | Road classification — VERKEHRSBEDEUTUNG equivalent for Lausanne | CSV, GPKG |
| **9-10, 17-18** | Geneva RefPU parking (multiple) | Geneva parking infrastructure — pick ONE format (WFS) | WFS |

### Statistics & Demographics
| # | Dataset | Why it matters | Format |
|---|---------|---------------|--------|
| **26** | [Statistique villes suisses 2020](https://opendata.swiss/en/dataset/statistics-on-swiss-cities-and-towns-2020) | Population, economy, transport per city — context for corridor communes | CSV, XLS |
| **32** | [Statistique villes suisses 2021](https://opendata.swiss/en/dataset/statistik-der-schweizer-staedte-2021) | Updated version of above | CSV, ODS |

### Heritage & Historical
| # | Dataset | Why it matters | Format |
|---|---------|---------------|--------|
| **22** | [Architecture à Genève 1919-1975](https://opendata.swiss/en/dataset/larchitecture-a-geneve-1919-19751) | Where heritage constraints may limit infrastructure placement | WFS |

---

## ❌ TIER 3 — Not useful for your narrative (skip)

| # | Why skip |
|---|---------|
| **3** | Environmental wardens — enforcement, not infrastructure |
| **8** | Max van Berchem photos — historical orientalist photography, false positive |
| **13** | Amphibian migration — false positive from "transport" theme |
| **14** | International comparison indicators — too broad, no spatial granularity |
| **15** | Lake thermal potential — energy/Siméon's territory |
| **16** | Pipeline installations — industrial safety, not mobility |
| **20** | High-voltage installations — energy grid, Siméon's territory |
| **21** | De Hondt 1630 map — historical cartography curiosity |
| **23** | Tapinoma ant zones — invasive species, false positive |
| **24** | Water extraction permits — hydrology |
| **29** | Polluted sites (transport) — environmental remediation |
| **30** | Crop rotation surfaces — agriculture |
| **31** | Bern heritage — wrong canton entirely |
| **33-34** | Federal voting data — political, not spatial infrastructure |
| **39-40** | Polluted sites (aerodromes) — tangential |
| **45** | Electricity demand for EVs — energy side (Siméon) |
| **46-47, 49-50** | Geneva RefPU environment reservations — urban planning zoning, not flow |
| **48** | Aerodrome noise — aviation noise, tangential |

---

## Scoring issues to flag

The scoring has some quirks worth noting:
- **"coworking" appears as a matched theme on many datasets that have nothing to do with coworking** (#9, 16, 29, 30, 33...). The thematic matching probably triggered on a common French word fragment. This inflates scores for irrelevant datasets.
- **Geneva RefPU datasets are heavily duplicated** — same underlying data in point/surface/adopted variants. Pick one per topic.
- **National datasets score lower than they should** — #35-44 (OFEN charging projections) all score 49.0 because spatial is "Schweiz" (medium), but these are actually the most valuable for your narrative since they have commune-level granularity.

## Recommended action plan

1. **Immediate**: Download #7 (CFF real-time charging), #27 (charging key figures), #28 (shared mobility) — these are CSV/JSON, easy to integrate
2. **WMS layers for QGIS**: Add #11 + #38 (rail noise day/night) + #35-37 (2035 charging projections) as WMS layers — instant, no processing needed
3. **Cross-reference**: Use #41-43 (home charging availability) to identify communes where public charging dependency is highest → overlay with your 194 stations → find the gap
4. **Zurich comparison**: #11 and #38 already cover Zurich — rail noise is your easiest apples-to-apples comparison layer
5. **Later**: Lausanne street furniture (#5) + parking meters (#4) for a deep-dive on one municipality's "dwell infrastructure"
