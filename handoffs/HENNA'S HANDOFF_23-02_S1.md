# HENNA'S HANDOFF — 23-02 Session 1

## Last action
Brainstormed and selected narrative direction for Assignment 2: **"The Night City"** — mapping where urban life persists after dark along City101, and where it vanishes. This flips the studio's daytime-commuter framing of the linear city and tests whether City101 is a real city or just infrastructure with bedrooms.

## Current state
- **Narrative chosen**: The Night City
- **Core question**: Where along City101 does urban life persist after dark, and where does it vanish?
- **No datasets built yet** — brainstorming phase only
- **All classmate datasets inventoried** (see below)
- **Own A.01 datasets exist**: UHI zones, cold air drainage, thermal comfort, psycho-comfort, local traditions, rotating cultural circuits, station ridership, flow of meaning + transit stops

## The Night City — Planned Layers

1. **Alive/dead map** — Google Places opening hours: everything open past 10pm, midnight, 2am. Heat map of nocturnal activity per segment.
2. **Night transport skeleton** — Noctambus routes, last trains, night taxi stands, bike-share at night. Where does connectivity die after trains stop?
3. **Lit and dark** — Public lighting data or satellite nighttime imagery. Physical illumination along corridor.
4. **Night workers** — Hospitals (Thomas), industrial shift work (Siméon), gig hubs (Charlene), 24h logistics (Alexei). People the line wasn't designed for.
5. **Night ecology** — Cold air drainage (own data) happens at night. Bats/nocturnal insects. Light pollution disruption. Biological city breathes at night.

## Index Formula (draft)
**Nocturnal Vitality Score** per segment = density of late-night venues × night transport accessibility × public lighting coverage × night worker presence. High = real city. Zero = dormitory.

## Zurich Comparison Angle
Zurich has genuine 24h urban core (Langstrasse, Niederdorf). City101 likely shows nightlife concentrated in a few nodes (Lausanne Flon, Montreux) with dead zones between. Linear city = daytime phenomenon? The line itself is dead after dark.

## Prototypology Direction
"Night node" — architecture for the hours when everything shuts down. Serves shift workers, teenagers, delivery riders, nocturnal ecology. Not a nightclub but infrastructure that acknowledges the city doesn't stop at sunset.

## Open threads
- [ ] Build Layer 1: late-night venues dataset (Google Places hours along City101)
- [ ] Build Layer 2: night transport (SBB last departures, Noctambus routes)
- [ ] Build Layer 3: lighting/satellite night imagery source needed
- [ ] Build Layer 4: cross-reference classmates' data for night workers
- [ ] Build Layer 5: integrate own cold air drainage as night ecology layer
- [ ] Define corridor segments for scoring
- [ ] Zurich equivalent datasets needed
- [ ] Point Cloud Sections for high-potential sites (A.02 requirement)
- [ ] Determine how "night" connects back to Huang's 4 axes (pedestrian returns, lake relationship, diversity/demography, heterogeneity)

## Key decisions made (cumulative)
1. **Flow of life abandoned** as primary framing — too narrow for A.02
2. **Night City chosen** as narrative — specific, original, expandable
3. **Cross-dataset approach** — will pull from collective pool, not just own data
4. **Index-based method** — nocturnal vitality score to rank segments and compare to Zurich
5. **Cold air drainage** reframed as night ecology data (connects old work to new narrative)

## Huang's Framework (from crit notes)
Four axes he wants investigated across the studio:
1. Pedestrian returns (accessibility, walkability)
2. Relationship to lake (key to city)
3. Diversity and demography (homogeneity to map)
4. Strength of heterogeneity

Method: Build a **city index** (like happiest cities rankings), define criteria, id sites for intervention or compare to Zurich. Narrative feeds into **prototypology**.

Also noted: "Specificity is better. Uniqueness." and "CVS as official data — modify that CVS based on indexing personally defined."

## Technical notes
- CRS: Swiss LV95 / EPSG:2056
- Tools: QGIS, Claude Desktop with OSM + Rhino + QGIS MCP
- Classmate datasets in shared Google Drive folder (00-datasets)
- Own datasets uploaded to shared folder as hennarafik-*.csv/gpkg/pdf

## Collective Dataset Inventory

| Student | Datasets | Flow |
|---------|----------|------|
| **Henna (own)** | Cold air drainage, thermal comfort, UHI (high/med/low), psycho-comfort, local traditions + heritage, rotating cultural circuits, station ridership, flow of meaning + transit stops | Life / Meaning |
| **Andrea Crespo** | EV charging + reviews, cell towers, international anchors, public WiFi, remote work places + reviews | People / Forces |
| **Alexei Potapushin** | E-commerce, Migros/Coop, delivery routes (fullroutes), tier A/B/C | Goods |
| **Aimeric Marin** | Cultural spaces, libraries, museums, theaters, sailboats, sailboat paths/ports | Meaning |
| **Julie Favre** | Apple farms, commercial hubs, farm-to-market flows, pollinator hubs | Goods / Life |
| **Lhiam Rossier** | Water quality (CIPEL), lake degradation, microbial corridors, marshes, soil aptitude, alluvial zones, amphibian reproduction, STEP performance, river morphology | Well-being / Forces |
| **Cristina Martinez** | Social segregation, intergenerational exchange | People |
| **Charlene Dejean** | Gig work, rooftops | Labor / Space |
| **Thomas Riegert** | All religious communities + buildings (Buddhist, Christian, Evangelical, Hindu, Jewish, Muslim, Orthodox, Other), esotericism, GPs, specialists, private clinics, public hospitals | Well-being / Forces |
| **Dimitri Roulet** | Hazardous waste, incineration, industrial composting, inert landfill, waste collection, waste sorting, wastewater | Residue |
| **Siméon Pavicevic** | Energy consumption/production/flows, industrial sectors, industrial zones | Labor / Forces |
| **Stella Guicciardi** | Birdhouses (+ Geneva), Lausanne birds, temporary structures | Life / Space |
| **Vladislav Belov** | Acoustic ecology, local materials, traffic noise raster | Life / Space |

## Data sources (this session)
- Classmate datasets: Google Drive shared folder (22-23.02.2026)
- Topic spreadsheet: A_01_-_TOPIC_SPREADSHEET.xlsx
- Brainstorming transcripts: voice-to-text PDFs from group session + crit conclusion (23.02.2026)
- Handwritten crit notes: 3 notebook pages photographed

## Crit notes (from A.01 conclusion + group brainstorm)
- Benchmark City101 vs Zurich is essential
- Diversity = cross-fertilization = creativity (strongest critic theme)
- Dark data: nobody has studied City101 as one city
- Data-driven ≠ argument: let stories emerge from data
- Fractal: small part should express the whole
- Zoning = authority-built city; linear city was originally socialist/utopian
- Speed to diversity: family names as indicator
- The line = no cars; diversity by accessibility by time
- La dérive: you go where you love ≠ methodology
