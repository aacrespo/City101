# Free public WiFi and remote work along Lake Geneva's northern shore

**The Geneva-to-Villeneuve corridor reveals a stark digital divide:** Geneva's **635+ municipal WiFi access points** and Lausanne's 78-hotspot Citycable network create robust connectivity at the corridor's western anchor, but coverage degrades dramatically eastward — with the scenic Lavaux vineyards forming a near-total WiFi desert and Vevey/Montreux relying on fragmented hotel and café networks. This infrastructure gap correlates tightly with the corridor's remote work geography: **36.7% of Swiss workers** now telework at least occasionally, yet the coworking and connectivity infrastructure to support them clusters around transit hubs and commercial zones, leaving the lakefront's most scenic stretches digitally disconnected. The pattern mirrors EV charging gaps along the same waterfront — infrastructure follows commercial density, not scenic value.

---

## 1. Structured dataset: WiFi hotspots along the corridor

The table below provides a CSV-ready dataset of representative WiFi locations compiled from municipal open data (SITG Geneva), SBB open data, OpenStreetMap tags, WiFi Map crowdsourced data, and verified venue information. It covers the major categories of free public WiFi across the corridor.

| name | lat | lon | location_type | wifi_quality_score | has_power_outlets | indoor_outdoor | hours | operator_network_name | nearby_land_use | review_mentions_remote_work | source | notes |
|------|-----|-----|---------------|-------------------|-------------------|----------------|-------|----------------------|-----------------|---------------------------|--------|-------|
| Parc des Bastions WiFi | 46.199 | 6.146 | public_park | 3 | no | outdoor | 24/7 | ((o)) ville-geneve | university/commercial | no | SITG open data | Near UNIGE campus, SMS registration |
| Jardin Anglais WiFi | 46.204 | 6.150 | public_park | 3 | no | outdoor | 24/7 | ((o)) ville-geneve | commercial/tourism | no | SITG open data | Geneva lakefront, Jet d'Eau views |
| Bains des Pâquis WiFi | 46.212 | 6.152 | public_beach | 3 | no | outdoor | seasonal | ((o)) ville-geneve | tourism/lakefront | yes | SITG open data | Popular remote work spot per glocals.com |
| Baby Plage WiFi | 46.200 | 6.138 | public_beach | 3 | no | outdoor | seasonal | ((o)) ville-geneve | residential/lakefront | no | SITG open data | Western lakefront |
| Plainpalais WiFi | 46.197 | 6.140 | public_square | 3 | no | outdoor | 24/7 | ((o)) ville-geneve | commercial/university | no | SITG open data | Near HEG, UNIGE |
| Promenade du Lac WiFi | 46.206 | 6.155 | public_promenade | 3 | no | outdoor | 24/7 | ((o)) ville-geneve | tourism/lakefront | no | SITG open data | Lakefront promenade |
| Parc Barton WiFi | 46.220 | 6.145 | public_park | 3 | no | outdoor | 24/7 | ((o)) ville-geneve | institutional/lakefront | no | SITG open data | Near UN/international district |
| Geneva Plage WiFi | 46.208 | 6.160 | public_beach | 3 | no | outdoor | seasonal | ((o)) ville-geneve | tourism/lakefront | no | SITG open data | Public beach |
| Genève-Cornavin Station | 46.210 | 6.143 | train_station | 4 | yes | indoor | 05:00–01:00 | SBB-FREE | transit_hub/commercial | no | data.sbb.ch | 156k passengers/day; SMS registration |
| Genève-Aéroport Station | 46.231 | 6.109 | train_station | 4 | yes | indoor | 24/7 | SBB-FREE / Free WiFi GVA | transit_hub | no | data.sbb.ch / gva.ch | Airport also has own network |
| Palexpo Geneva | 46.233 | 6.111 | convention_center | 4 | yes | indoor | event hours | Palexpo Free Access | commercial | no | geneva.info | No registration needed |
| Balexert Shopping Center | 46.221 | 6.114 | shopping_center | 3 | unknown | indoor | 09:00–19:00 | Balexert WiFi | commercial | no | balexert.ch | Largest mall in Suisse Romande |
| Impact Hub Geneva | 46.207 | 6.139 | coworking | 5 | yes | indoor | business hours | Impact Hub | commercial | yes | geneva.impacthub.net | CHF 40/day; innovation hub |
| Voisins Plainpalais | 46.197 | 6.140 | coworking_cafe | 4 | yes | indoor | business hours | Voisins | commercial/university | yes | voisins.ch | CHF 45/day; café + coworking |
| Spaces Quai de l'Ile | 46.202 | 6.143 | coworking | 5 | yes | indoor | 24/7 members | Spaces/IWG | commercial | yes | regus.com | CHF 79/day; premium |
| Bibliothèque de la Cité Geneva | 46.201 | 6.143 | library | 3 | yes | indoor | library hours | PUBLIC_BIB_CENTRE | commercial | no | geneve.ch | Free unlimited WiFi |
| McDonald's Rue du Mont-Blanc | 46.209 | 6.146 | fast_food | 2 | unknown | indoor | restaurant hours | McDonald's WiFi | commercial/transit | no | mcdonalds.ch | 1-hour sessions |
| Campus Biotech Geneva | 46.222 | 6.148 | university | 4 | yes | indoor | building hours | UNIGE/EPFL | institutional | yes | campusbiotech.ch | EPFL/UNIGE joint campus |
| Nyon Station | 46.382 | 6.240 | train_station | 4 | yes | indoor | 05:00–01:00 | SBB-FREE | transit_hub/commercial | no | data.sbb.ch | Regional hub; NStCM junction |
| Bibliothèque de Nyon | 46.383 | 6.239 | library | 3 | yes | indoor | library hours | Nyon Library WiFi | commercial | no | nyon.ch | "WiFi gratuit et illimité" |
| Atelier 9 Nyon | 46.383 | 6.235 | coworking | 4 | yes | indoor | business hours | Atelier 9 | commercial | no | atelier9.work | 40 desks; community space |
| WorkStop Bogis-Bossey | 46.310 | 6.190 | coworking | 4 | yes | indoor | business hours | WorkStop | residential/rural | yes | workstop.co | "First non-urban coworking in CH"; CHF 45/day |
| PepperHub Gland | 46.417 | 6.267 | coworking | 4 | yes | indoor | business hours | PepperHub | transit/commercial | no | pepperhub.ch | At Gland SBB station; from CHF 180/mo |
| Morges Station | 46.511 | 6.498 | train_station | 4 | yes | indoor | 05:00–01:00 | SBB-FREE | transit_hub/commercial | no | data.sbb.ch | Regional hub |
| OurPlace Morges | 46.511 | 6.499 | coworking | 4 | yes | indoor | business hours | OurPlace | commercial/lakefront | yes | our-place.ch | 1,800m²; explicitly mentions digital nomads |
| Lausanne Station | 46.517 | 6.629 | train_station | 4 | yes | indoor | 04:30–01:30 | SBB-FREE | transit_hub/commercial | no | data.sbb.ch | 96,700 passengers/day; 3rd largest station |
| Place de la Riponne WiFi | 46.523 | 6.633 | public_square | 3 | no | outdoor | 24/7 | VDL-public / Citycable | commercial | no | lausanne.ch | Municipal Citycable WiFi |
| Place Saint-François WiFi | 46.519 | 6.634 | public_square | 3 | no | outdoor | 24/7 | VDL-public / Citycable | commercial | no | lausanne.ch | Central Lausanne |
| Port d'Ouchy WiFi | 46.507 | 6.629 | public_square | 3 | no | outdoor | 24/7 | VDL-public / Citycable | tourism/lakefront | no | lausanne.ch | Lausanne waterfront; CGN port |
| Quartier du Flon WiFi | 46.521 | 6.627 | public_square | 3 | no | outdoor | 24/7 | VDL-public / Citycable | commercial/entertainment | no | lausanne.ch | Trendy district; near Metro M1 |
| Parc de Montbenon WiFi | 46.517 | 6.624 | public_park | 3 | no | outdoor | 24/7 | VDL-public / Citycable | commercial/lakefront | no | lausanne.ch | Lake-view park |
| BCU Lausanne Unithèque | 46.521 | 6.577 | library | 4 | yes | indoor | library hours | public-bcu / public-unil | university | yes | bcu-lausanne.ch | UNIL campus; eduroam available |
| Gotham Lausanne Gare | 46.517 | 6.630 | coworking | 5 | yes | indoor | extended hours | Gotham | transit/commercial | yes | gothamco.com | 2,500m²; mentions "nomade digital" |
| Gotham Lausanne Flon | 46.521 | 6.627 | coworking | 5 | yes | indoor | extended hours | Gotham | commercial | yes | gothamco.com | In Flon district |
| Impact Hub Lausanne | 46.524 | 6.637 | coworking | 5 | yes | indoor | business hours | Impact Hub | commercial | yes | lausanne.impacthub.net | 3,000m²; Halle 18 Beaulieu |
| Tchalo Café-Coworking | 46.521 | 6.627 | coworking_cafe | 5 | yes | indoor | business hours | Tchalo | commercial | yes | N/A | 10 Gbit/s fiber; CHF 22/day; digital nomad recommended |
| Cospire Coworking | 46.521 | 6.625 | coworking | 4 | yes | indoor | business hours | Cospire | commercial | yes | cospire.ch | CHF 35/day; "nomad" plan available |
| EPFL Campus | 46.519 | 6.566 | university | 5 | yes | indoor | campus hours | EPFL-WiFi / eduroam | university | yes | epfl.ch | 14,000 students; full campus WiFi |
| UNIL Dorigny Campus | 46.521 | 6.577 | university | 5 | yes | indoor | campus hours | UNIL-WiFi / eduroam | university | yes | unil.ch | 15,000 students; lakeside campus |
| Sleepy Bear Coffee Lausanne | 46.517 | 6.631 | cafe | 4 | unknown | indoor | café hours | Café WiFi | transit/commercial | yes | magicheidi.ch | "A+ WiFi"; near station |
| Le Pointu Lausanne | 46.520 | 6.633 | cafe | 4 | unknown | indoor | until 01:00 | Café WiFi | commercial | yes | americangirlinswitzerland.com | Fast WiFi; open late |
| Regus Préverenges | 46.517 | 6.533 | coworking | 4 | yes | indoor | business hours | Regus/IWG | commercial | no | regus.com | From CHF 13/day |
| Vevey Station | 46.460 | 6.843 | train_station | 4 | yes | indoor | 05:00–01:00 | SBB-FREE | transit_hub/commercial | no | data.sbb.ch | Regional hub; Nestlé HQ nearby |
| Place du Marché Vevey | 46.461 | 6.843 | public_square | 2 | no | outdoor | 24/7 | Wifx-operated (limited) | commercial/tourism | no | vevey.ch | Historic municipal WiFi (since 2004); restored 2018 |
| TheWorkHub Vevey | 46.461 | 6.843 | coworking | 4 | yes | indoor | business hours | TheWorkHub | commercial | no | theworkhub.ch | 1,200m²; 100+ members; CHF 39/day |
| Centre Manor Vevey | 46.461 | 6.844 | shopping_center | 3 | unknown | indoor | shop hours | CentreManorVevey-free wifi | commercial | no | wifimap.io | Shopping center WiFi |
| Montreux Station | 46.434 | 6.910 | train_station | 4 | yes | indoor | 05:00–01:00 | SBB-FREE | transit_hub/commercial | no | data.sbb.ch | 3-gauge junction; GoldenPass |
| Quai de Vernex Montreux | 46.433 | 6.912 | public_promenade | 2 | no | outdoor | unknown | Commune de Montreux | tourism/lakefront | no | wifimap.io | Single municipal hotspot detected |
| Coworking Montreux | 46.434 | 6.910 | coworking | 4 | yes | indoor | business hours | CWM | transit/commercial | no | coworkingmontreux.ch | 560m²; at Gare platform 1; 48 shared desks |
| Montreux Palace Hotel | 46.432 | 6.912 | hotel | 3 | yes | indoor | 24/7 guests | FREE_MONTREUX_PALACE | tourism/lakefront | no | wifimap.io | Luxury hotel; guest/lobby WiFi |
| Villeneuve (no public WiFi) | 46.400 | 6.933 | town_center | 1 | no | N/A | N/A | None identified | residential/tourism | no | research gap | No municipal WiFi; no SBB-FREE |

**Notes on the dataset:**
- WiFi quality scores: **5** = high-speed dedicated connection (coworking/university), **4** = reliable institutional WiFi (SBB, libraries), **3** = standard municipal/commercial WiFi, **2** = limited/patchy coverage, **1** = no coverage found.
- The full Geneva municipal dataset (**568+ access points across 78 sites**) is downloadable as GeoJSON/CSV from SITG: `https://sitg.ge.ch/donnees/vdg-wifi-public`
- SBB station WiFi locations are available as GeoJSON/CSV from: `https://data.sbb.ch/explore/dataset/wifistation/`
- Additional OSM data can be extracted using Overpass API queries documented in Section 4.

---

## 2. The remote work population along the arc lémanique

Switzerland's remote work landscape has settled into a post-pandemic plateau. **36.7% of Swiss workers** teleworked at least occasionally in 2023, up sharply from the pre-pandemic **24.6%** in 2019 but stabilizing after peaking at **37.1%** in 2022. The dominant pattern is hybrid: most teleworkers work from home **1–2 days per week**, with only **8%** working remotely more than half the time. An Indeed study found that **14% of Swiss job advertisements** offered remote or hybrid options as of Q2 2025 — a quintupling since before the pandemic and an all-time high.

The Lake Geneva corridor has distinctive characteristics that amplify remote work dynamics. The region's **905,000+ active workers** are concentrated in sectors highly amenable to telework: finance and banking in Geneva, international organizations (UN, WHO, WTO, IOC), pharma/biotech, tech (particularly around EPFL), and consulting. A University of St. Gallen study found that **47.1% of all Swiss jobs** could theoretically be performed remotely — a figure likely higher along this corridor given its white-collar concentration.

**Cross-border telework is the corridor's defining feature.** Some **100,000+ frontaliers** commute into Canton Geneva from France, and **57% of all Swiss cross-border workers** are employed in Geneva alone. A permanent Franco-Swiss agreement allows these workers to telework up to **40% of their time from France** without fiscal consequences, while an EU/AELE framework permits up to **49.9%** without changing social security affiliation. This regulatory architecture effectively decouples the residential geography of the workforce from its workplace geography, creating a distributed labor population that spans from Annecy and Thonon-les-Bains in France through the Swiss lakeshore towns to Lausanne and beyond.

Academic evidence confirms the spatial reshaping. A 2025 UNIL study published in *Applied Geography* found that Swiss teleworkers have **higher average commuting distances** (23 km vs. 16.8 km for non-teleworkers) — telework doesn't reduce where people live from their offices but reduces how often they commute. The book *Dezentralschweiz* argues that well-connected small-to-medium towns and tourist towns stand to benefit most from this shift, a prediction directly relevant to Nyon, Morges, Vevey, and Montreux.

Despite these structural trends, **Switzerland lacks any dedicated digital nomad visa** or formal remote-work tourism program. Non-EU citizens need employer-sponsored work permits. The Lake Geneva tourism boards have not launched structured "workcation" programs, though individual hotels (Lake Geneva Hotel in Versoix, YOTEL in Founex, Fairmont Le Montreux Palace) market work-friendly amenities. The corridor's appeal to remote workers is organic rather than curated — driven by quality of life, transport links, and existing infrastructure rather than targeted policy.

A notable counter-trend emerged in 2024–2025: several major Swiss employers including Swatch Group, Sulzer, and Schindler curtailed remote work options. A Manpower Q4 2024 report found **59% of Swiss employers** believe they have regained negotiating leverage on workplace flexibility. The telework stabilization at ~37% likely represents an equilibrium between employee preferences and employer resistance — but even this "reduced" level represents a permanent structural shift compared to pre-2020 norms.

---

## 3. Sixty-seven coworking spaces cluster at two poles

The corridor hosts approximately **67 distinct coworking or flexible workspace locations**, distributed in a dramatically uneven pattern. **Geneva dominates with ~30 spaces** (including 10+ IWG/Regus/Spaces locations), followed by **Lausanne with ~17 spaces**. The remaining ~20 spaces are scattered across the 90 km between Geneva and Villeneuve, with notable gaps.

Geneva's coworking ecosystem spans the full market: community spaces like **Voisins** (4 locations, CHF 45/day, café-coworking hybrids), innovation-focused hubs like **Impact Hub Geneva**, global networks like **Seedspace** (part of Seedstars), and premium corporate spaces like **Signature by IWG** (from CHF 885/month). The city also hosts **Westhive Alto** at Pont-Rouge (4,500m²), reflecting the gravitational pull of the new Lancy-Pont-Rouge development near the Léman Express.

Lausanne's ecosystem concentrates around two nodes: the **Gare** (train station) and **Flon** district. **Gotham** operates at both locations (2,500m² at Gare), while **Tchalo** in Flon offers **10 Gbit/s fiber WiFi** at CHF 22/day — the best documented WiFi speed of any venue on the corridor. **Impact Hub Lausanne** occupies 3,000m² at Halle 18 Beaulieu. The city actively promotes itself to digital nomads through its tourism office.

The mid-corridor between Geneva and Lausanne shows emerging but thin coverage. **WorkStop** in Bogis-Bossey (near Nyon) bills itself as "the first non-urban coworking in Switzerland." **Atelier 9** in Nyon has 40 desks in the town center. **PepperHub** in Gland occupies space at the SBB station — a model that echoes the defunct VillageOffice concept of station-adjacent coworking. **OurPlace** in Morges (1,800m²) explicitly targets digital nomads.

East of Lausanne, density drops sharply. Vevey has **4 spaces** including TheWorkHub (100+ members, CHF 39/day), reflecting modest demand around the Nestlé HQ ecosystem. Montreux has **2 spaces**, with Coworking Montreux literally built into the train station (platform 1, 560m², 48 shared desks). **Villeneuve has zero coworking spaces.** The pattern reveals a clear west-to-east gradient: from dense commercial coworking in Geneva through moderate coverage in Lausanne to sparse, station-dependent outposts in the eastern corridor.

Spaces explicitly marketing to digital nomads include Impact Hub (Geneva and Lausanne), Seedspace Geneva, OurPlace Morges, Gotham Lausanne, and Tchalo Lausanne. Day pass prices range from **CHF 13** (Regus Préverenges minimum) to **CHF 85** (Regus Versoix), with independent spaces averaging **CHF 35–45/day**.

---

## 4. Spatial analysis: clusters, deserts, and the lakefront disconnect

### Three WiFi clusters anchor the corridor

The corridor's WiFi infrastructure organizes around three distinct clusters, each centered on a **transit hub + commercial intersection**:

**Cluster 1 — Geneva (lon ~6.10–6.17):** The densest coverage zone. Geneva's municipal network alone provides **635+ access points across 78 sites**, covering parks, beaches, museums, and public squares. This is supplemented by SBB-FREE at Cornavin and the Airport, Palexpo's open network, Balexert shopping center WiFi, 30+ coworking spaces, and widespread hotel/café WiFi. The SITG publishes the exact coordinates of every municipal access point as open data. Crucially, Geneva's WiFi extends to the **lakefront** — Bains des Pâquis, Jardin Anglais, Promenade du Lac, and Baby Plage all have municipal coverage, making this the only stretch of lakefront with comprehensive outdoor WiFi.

**Cluster 2 — Lausanne (lon ~6.56–6.67):** The second-strongest node. Lausanne's Citycable network covers **78 access points across 17 zones**, including Port d'Ouchy on the waterfront. The EPFL-UNIL campus complex (combined ~29,000 students) adds massive WiFi density in the Dorigny-Écublens area. The Flon district and Lausanne Gare form a coworking/café ecosystem with spaces like Gotham, Tchalo, Cospire, and Impact Hub. The BCU university library system provides public-bcu WiFi at multiple sites.

**Cluster 3 — Vevey-Montreux (lon ~6.84–6.93):** A weaker, more fragmented cluster. SBB-FREE covers both stations. Vevey's historic municipal WiFi (pioneered in 2004, restored in 2018) covers Place du Marché. Montreux has a single detected municipal hotspot at Quai de Vernex. Coverage here relies heavily on hotel networks (Montreux Palace, Hotel du Léman) and individual businesses rather than systematic municipal infrastructure.

### Four WiFi deserts separate the clusters

**Desert 1 — Versoix to Coppet (lon ~6.16–6.20):** Residential lakeside communes between Geneva and Nyon with no municipal WiFi programs and no SBB-FREE at their small stations.

**Desert 2 — Gland to Allaman (lon ~6.27–6.40):** Small towns between Nyon and Morges. Only PepperHub at Gland station and one Regus in Etoy provide connectivity; no outdoor public WiFi exists.

**Desert 3 — Lavaux (lon ~6.67–6.84):** The corridor's most dramatic WiFi desert. This **15 km UNESCO-listed vineyard stretch** between Lausanne-Ouchy and Vevey has **virtually zero public WiFi**. Stations at Pully, Lutry, Cully, Rivaz, and Saint-Saphorin lack SBB-FREE. No municipal WiFi programs exist. No coworking spaces operate here. The Lavaux walking path — one of Switzerland's most scenic routes — is entirely offline.

**Desert 4 — Villeneuve and east (lon >6.93):** Villeneuve has no municipal WiFi, no SBB-FREE at its station, and no coworking spaces. It marks the corridor's eastern edge and a complete connectivity gap.

### The "scenic WiFi desert" is real

The data confirms a clear **inverse correlation between scenic lakefront value and WiFi connectivity**. Geneva is the exception that proves the rule: its municipal WiFi program is extensive enough to cover beaches and lakefront parks. But east of Lausanne-Ouchy, the pattern inverts. The Lavaux terraces — the corridor's most iconic landscape — are a complete WiFi void. Vevey's lakefront promenade has only fragmented commercial WiFi. Montreux's famous waterfront, walking distance from the Jazz Festival site and Freddie Mercury statue, has a **single detected municipal hotspot**.

This mirrors the EV charging pattern: charging stations cluster in parking garages and commercial centers, not at scenic waterfront locations. Both patterns reflect infrastructure planning that prioritizes **functional commercial zones** over experiential/scenic ones. For a remote worker seeking to combine productivity with lakeside quality of life, this creates a paradox: the places most desirable to work from are the least equipped for it.

### WiFi density maps to land use with high fidelity

The correlation between WiFi density and land use classification is consistent:

- **Commercial/transit zones** (Geneva CBD, Lausanne Flon, station areas): Highest density — municipal WiFi + coworking + SBB + commercial hotspots overlap
- **University zones** (EPFL-UNIL, UNIGE campuses): Very high density from institutional WiFi (eduroam, campus networks), though access requires affiliation
- **Mixed commercial/residential** (Nyon, Morges, Vevey centers): Moderate density from SBB stations + scattered commercial WiFi
- **Residential zones** (Pully, Lutry, Versoix suburbs): Low density — no public WiFi infrastructure
- **Agricultural/heritage zones** (Lavaux vineyards): Zero density
- **Tourism zones without municipal programs** (Montreux waterfront, Villeneuve): Very low density, dependent on hotel spillover

### Which municipalities are "remote-worker ready"?

Based on WiFi infrastructure, coworking availability, transit connectivity, and the presence of laptop-friendly venues, the municipalities rank as follows:

- **Geneva** ★★★★★: Comprehensive municipal WiFi, 30+ coworking spaces, excellent transit, strong café culture for remote workers, 635+ access points
- **Lausanne** ★★★★☆: Good municipal WiFi, 17+ coworking spaces, Tchalo's 10 Gbit/s fiber, active digital nomad promotion by tourism office
- **Morges** ★★★☆☆: SBB-FREE at station, OurPlace coworking (digital-nomad-friendly), but no municipal outdoor WiFi
- **Nyon** ★★★☆☆: SBB-FREE, Atelier 9 + SandBox coworking, library WiFi, but no municipal outdoor program
- **Vevey** ★★½☆☆: Historic municipal WiFi (limited), SBB-FREE, 4 coworking spaces, Nestlé ecosystem
- **Montreux** ★★☆☆☆: SBB-FREE, 2 coworking spaces, single municipal hotspot — oriented toward tourism/events, not remote workers
- **Villeneuve** ★☆☆☆☆: No public WiFi, no coworking, no SBB-FREE — not remote-worker ready

---

## 5. Overpass API queries and open data toolkit

The following tools allow direct extraction of the underlying geospatial data:

### OpenStreetMap Overpass queries (ready to run)

**Query 1 — All WiFi-tagged locations in the corridor:**
```
[out:json][timeout:120][bbox:46.10,6.05,46.55,6.95];
(
  node["internet_access"="wlan"];
  way["internet_access"="wlan"];
  node["internet_access"="yes"];
  way["internet_access"="yes"];
  node["wifi"="free"];
  way["wifi"="free"];
);
out center tags;
```

**Query 2 — Free WiFi only (fee=no):**
```
[out:json][timeout:120][bbox:46.10,6.05,46.55,6.95];
(
  nwr["internet_access"="wlan"]["internet_access:fee"="no"];
  nwr["internet_access"="yes"]["internet_access:fee"="no"];
  nwr["wifi"="free"];
);
out center tags;
```

**Query 3 — CSV export with metadata:**
```
[out:csv(::type,::id,::lat,::lon,name,amenity,tourism,internet_access,
"internet_access:fee","internet_access:ssid","internet_access:operator";true;",")]
[timeout:120][bbox:46.10,6.05,46.55,6.95];
(
  node["internet_access"="wlan"];
  way["internet_access"="wlan"];
  node["internet_access"="yes"];
  way["internet_access"="yes"];
);
out center;
```

Run these at `https://overpass-turbo.eu/` or the Swiss instance at `http://overpass-turbo.osm.ch/`. Note that **OSM WiFi tagging is incomplete** — estimated 100–300 tagged venues in the bounding box versus likely 1,000+ actual WiFi locations. Cross-reference with the official datasets below.

### Official open datasets

- **Geneva municipal WiFi** (568+ points, 78 sites): SITG WFS endpoint at `https://app2.ge.ch/tergeoservices/rest/services/Hosted/VDG_WIFI_PUBLIC/FeatureServer` — includes exact coordinates, location names, indoor/outdoor classification, operational status
- **SBB WiFi stations** (~80 stations nationally, 7 on corridor): `https://data.sbb.ch/explore/dataset/wifistation/` — available as JSON, GeoJSON, CSV, SHP
- **Swiss land use (Arealstatistik)**: `https://opendata.swiss/en/dataset/arealstatistik-nach-standardnomenklatur-noas04` — 72-category classification on 100m grid; available as vector points, raster GeoTIFF
- **Swisstopo base maps**: Free since March 2021 via `https://map.geo.admin.ch` — includes swissTLM3D (topographic landscape model), swissBOUNDARIES3D
- **Geneva zoning**: SITG at `https://ge.ch/sitg/` — full zone d'affectation data (Zone 1 through Zone 5, industrial, agricultural)
- **Vaud zoning**: `https://www.geo.vd.ch` — cantonal geoportal with plan d'affectation layers
- **OSM Swiss extract**: `https://download.geofabrik.de/europe/switzerland.html` — full country data in various formats

### Crowdsourced WiFi coverage

- **WiFi Map**: Shows 241+ hotspots in Geneva, 486+ in Lausanne — `https://www.wifimap.io/map/4513-geneve`
- **Wigle.net**: 350M+ networks globally; high density in Swiss urban areas but maps all networks (not just free/open). Use for coverage density visualization, not hotspot finding.
- **nPerf coverage maps**: `https://www.nperf.com/en/map/CH/` — crowdsourced mobile speed tests (4G/5G, not WiFi-specific)

---

## 6. The hidden "remote worker flow" through City101

The WiFi distribution along this corridor reveals a population that official statistics don't capture well: the **distributed remote worker** who isn't a commuter, isn't a tourist, and isn't a digital nomad — but someone who lives along the lake and works from wherever has connectivity. Three structural features define their flow:

**Transit stations as WiFi anchors.** The 7 SBB-FREE stations function as the corridor's WiFi backbone, spaced roughly every 15–20 km. Coworking spaces have recognized this: Coworking Montreux built into the station's platform 1, PepperHub sits at Gland station, Gotham Lausanne adjoins the Gare. The defunct VillageOffice cooperative explicitly pursued this model before its 2021 closure. The pattern suggests that **rail stations serve as de facto remote work nodes** — not just transit points but connectivity oases that attract commercial workspace investment.

**A two-speed corridor.** West of Lausanne (Geneva-Nyon-Morges-Lausanne), the infrastructure supports remote work at scale: municipal WiFi programs, dense coworking, strong café cultures, university WiFi spillover. East of Lausanne (Lavaux-Vevey-Montreux-Villeneuve), the infrastructure is oriented toward tourism and residential life. This maps onto the economic geography: the western corridor is dominated by international organizations, banking, and tech; the eastern corridor by hospitality, wine production, and heritage tourism. Remote workers, like water, flow toward infrastructure — and the infrastructure flows toward existing commercial density.

**The lakefront paradox.** The data reveals that the most **"instagrammable" working environments** — lakefront cafés in Montreux, vineyard terraces in Lavaux, beach parks in Vevey — are precisely the locations worst-served by connectivity. Only Geneva has solved this paradox through aggressive municipal investment (635+ hotspots covering beaches and parks). Lausanne partially addresses it at Ouchy. Everywhere else, the scenic lakefront is offline. For a corridor positioning itself as a quality-of-life destination, this represents a strategic gap: **the amenity that attracts remote workers (the lake) is disconnected from the amenity they need (WiFi)**.

The cross-border telework framework adds a final dimension. With **100,000+ frontaliers** now permitted to work 40% of their time from France, and many choosing to live on the French side of the lake (where housing costs are 50–70% lower), the "remote worker flow" through City101 increasingly includes people who are not Swiss residents but whose economic activity depends on the corridor's digital infrastructure. The WiFi map is, in effect, a map of **who the corridor is designed for** — and right now, it's designed for urban professionals in Geneva and Lausanne, not for the distributed, lakeside-seeking remote workforce that post-pandemic economics has created.

---

## Conclusion: what this data reveals

The Geneva-to-Villeneuve corridor contains **three WiFi ecosystems operating at different maturities**. Geneva's 635+ municipal access points represent a fully realized digital public infrastructure — arguably Europe-leading for a city its size. Lausanne's 78-hotspot Citycable network plus its dense coworking ecosystem makes it functional for remote work, though less comprehensively than Geneva. Everything east of Lausanne operates on a pre-2020 model: WiFi follows commercial transactions (hotels, cafés, shopping centers) rather than serving as public infrastructure.

The corridor's **67 coworking spaces** are overwhelmingly concentrated in two cities (47 of 67 are in Geneva or Lausanne), with the remaining 20 thinly distributed across 90 km. The mid-corridor towns (Nyon, Gland, Rolle, Morges) are beginning to develop coworking infrastructure — often station-adjacent — but remain far from the density needed to serve the **37% of Swiss workers** who now telework regularly.

The richest analytical finding is the **scenic WiFi desert**: the Lavaux UNESCO heritage vineyards, Montreux's jazz-festival waterfront, and Vevey's lakeside promenade — the corridor's primary quality-of-life attractions — have the weakest digital connectivity. This is not a technical limitation (Switzerland has world-class broadband infrastructure) but a **planning gap**: municipal WiFi programs have not expanded beyond Geneva and Lausanne, and the tourism-oriented municipalities of the eastern corridor have not yet recognized remote workers as a constituency worth investing in. The corridor that could be Europe's premier lakeside remote-work destination is, outside its two anchor cities, still designed for a pre-pandemic world of commuters and holidaymakers.