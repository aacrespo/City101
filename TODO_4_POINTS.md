# TODO — The 4 Points That Make It Click
**Created**: 2026-03-01
**Context**: The WCI exists (49 segments, spatial scores) but it describes conditions, not flows. These 4 points shift the project from "how good is this place?" to "what happens to your continuity as you move through?"

---

## POINT 1: THE BREAK POINT MAP
**Core idea**: Map where continuity RUPTURES, not where it exists. The negative space of the data. Comtesse's "dark data" = the infrastructure that doesn't exist.

### Data we already have
- [x] Stations with 0 workspaces within catchment (27/49 stations = 55%)
- [x] Stations with <2 trains/hr: Denges-Echandens, Bossière, Territet, St-Saphorin
- [x] WiFi hotspot locations (81 points) → gaps between them are the dead zones
- [x] Cell tower locations (3,218) → but need to identify actual signal gaps along rail line
- [x] Acoustic data (50 points from Vladislav) → 80% of chargers in loud environments

### Data we need to produce
- [ ] **WiFi dead zone mapping**: Buffer the 81 hotspots by their effective range (~100m indoor, ~300m outdoor), then identify stretches of the corridor NOT covered. Output: polyline/polygon of dead zones along rail spine.
- [ ] **Cell signal gaps along rail**: The ~3.2km Glion-Les Avants tunnel, the Lavaux tunnels between Cully-Vevey, urban canyons in Lausanne Gare area. Research actual tunnel locations from Swisstopo or OSM railway data. Cross-reference with cell tower coverage.
- [ ] **Workspace deserts**: Already have workspace_count=0 for 27 stations. But need to compute actual walking distances — "no workspace within 15-min walk (1.2km)" is more meaningful than "no workspace within catchment." Use actual road network distance if possible, or haversine as fallback.
- [ ] **Transit gaps by duration**: Convert trains_per_hour to average_wait_minutes. Map where average wait > 20 min, > 30 min, > 40 min. A 40-min wait breaks any work session.
- [ ] **Amenity voids around stations**: For each station, check: is there a café/restaurant within 300m? A grocery within 500m? A sheltered waiting area? Power outlets? Use Google Places or OSM for this.
- [ ] **The Lavaux Fracture in detail**: The zone between Cully and Vevey is where EVERYTHING breaks simultaneously — low frequency, no workspaces, no WiFi, high noise (rail), no amenities. Map this as a single "fracture zone" with all break types overlaid.

### Break severity classification
- **Minor break** (1): One dimension fails (e.g., no WiFi but workspace + transit OK)
- **Moderate break** (2): Two dimensions fail simultaneously
- **Major break** (3): Three or more dimensions fail
- **Total rupture** (4): All dimensions fail (St-Saphorin: 0 trains/hr, 0 workspaces, no WiFi, no amenities)

### Output
- Corridor spine polyline colored by break severity
- "Break point cards" for the worst ruptures (visual callouts)
- Break count per segment: how many times does continuity rupture on the Geneva→Villeneuve journey?

---

## POINT 2: THE TEMPORAL CORRIDOR
**Core idea**: The corridor isn't one city — it's a city that pulses. Map the same 101km at different hours. The WCI changes across the day.

### Data we already have
- [x] Service frequency (49 stations, trains/hr during 7-9am workday)
- [x] Opening hours for 68 remote workspaces (14 are 24h, 18 weekdays-only, hours_score computed)
- [x] Ridership with commuter index (CI: ratio of workday to average → high CI = pure commuter station)

### Data we need to produce
- [ ] **First train per station**: Query transport.opendata.ch for earliest departure from each corridor station. This is when the station "wakes up." Typically 5:00-6:30am but varies.
- [ ] **Last train per station**: Query for latest departure. This is when the station "dies." Typically 23:30-00:30 but varies dramatically — Épesses last train might be 22:00.
- [ ] **The dead window per station**: Duration between last train and first train. Lausanne might have 4.5 hours dead; Bossière might have 7+ hours.
- [ ] **Frequency by time slot**: Re-query transport API for multiple time windows, not just 7-9am:
  - Early morning: 5:00-7:00 (who can even get on the corridor?)
  - Peak commute: 7:00-9:00 (already have this)
  - Midday: 11:00-13:00 (tourist/leisure/flexible workers)
  - Afternoon: 14:00-16:00 
  - Evening peak: 17:00-19:00
  - Late evening: 20:00-22:00
  - Night: 22:00-00:00
- [ ] **Workspace temporal profile**: From opening hours data, compute how many workspaces are available at each time slot per segment. At 7am: probably 5 in Geneva, 0 in Lavaux. At 2pm: 13 in Geneva, 3 in Vevey. At 11pm: 2 in Geneva (24h places), 0 everywhere else.
- [ ] **Temporal WCI**: Recompute the WCI for each time slot. The formula stays the same but the inputs change:
  - transit_score changes with frequency by hour
  - workspace_density changes with opening hours
  - temporal_coverage becomes binary (is the workspace even open?)
  - connectivity stays constant (WiFi/cell doesn't change by hour)
  - mobility_score may change (some shared mobility is 24h, some isn't)
- [ ] **"Corridor alive" visualization**: For each hour 0-23, compute how many segments have WCI > threshold (e.g., 0.10). Plot as a timeline: the corridor breathes — wide at 8am, narrow at 2pm, almost gone at midnight.

### Output
- 3-4 maps showing the SAME corridor at different hours (7am / 2pm / 11pm minimum)
- Temporal WCI heatmap: x-axis = distance along corridor (Geneva→Villeneuve), y-axis = hour of day, color = WCI. This is the "pulse" visualization.
- "When does the city end?" — the hour at which each segment drops below minimum WCI

### Connection to Henna
Henna's Night City narrative maps where urban life persists after dark. The Temporal Corridor maps where WORKING life persists across the day. They're complementary — hers is about vitality, yours is about productivity.

---

## POINT 3: THE GA HYPOTHESIS
**Core idea**: The GA travelcard collapses the cost barrier, making the full corridor's diversity accessible. GA holders are the corridor's true citizens. Non-GA holders experience fragmented cities. Comtesse's formula: diversity × accessibility × time = urban vitality.

### Data we need to research/find
- [ ] **GA penetration data**: SBB doesn't publish per-commune. But: OFS MRMT 2021 has modal split + travelcard ownership by commune type; SBB annual reports have aggregate counts; Alliance SwissPass statistics
- [ ] **Cost of the corridor**: Actual ticket prices Geneva→Villeneuve per ticket type (point-to-point, demi-tarif, GA amortized, Léman Pass, zone Abo)
- [ ] **Frontalier commuting data**: OFS cross-border worker statistics. ~100k in Geneva canton. Where do they board/exit?
- [ ] **Modal split by commune**: MRMT data, % train vs car vs bike for commuting
- [ ] **Journey probability model**: Given ticket type and origin, what's the probability of an inter-city trip?

### The behavioral segmentation
- **GA citizen**: Treats entire corridor as one city. Cost = zero per trip.
- **Demi-tarif commuter**: Two points, one line. City = home catchment + work catchment.
- **Point-to-point occasional**: Corridor is expensive, fragmented. Takes car instead. Linear city doesn't exist for them.
- **Frontalier**: Enters from France, uses corridor during work hours, invisible in evening. The "ghost citizen."

### Output
- Cost map: what does it cost to traverse each segment by ticket type?
- "Who lives the linear city?" — commune-level indicators of corridor citizenship
- The GA as urban equalizer

---

## POINT 4: GOOGLE STATION REVIEWS (DARK DATA)
**Core idea**: Station ratings capture felt quality no official dataset measures. Cleanliness, safety, wayfinding, shelter, the emotional break point.

### Station inventory to expand
Current list: 49 train stations. Need to add:
- [ ] **Missing train stations**: Lutry, Chexbres-Village, Puidoux-Chexbres
- [ ] **M2 metro stations** (Lausanne): ~14 stations
- [ ] **Key Léman Express stations**: Chêne-Bourg, Annemasse, Bernex, Bachet-de-Pesay
- [ ] **CGN boat landings**: ~15 along corridor
- [ ] **Key bus/tram interchange hubs**

**Target: ~80-100 stations total**

### Fetch pipeline
- [ ] Google Places search for each station → Place ID
- [ ] Fetch ratings (aggregate + review count)
- [ ] Fetch review text, tag for: shelter, cleanliness, safety, wayfinding, amenities, accessibility, crowding, beauty, work_friendly
- [ ] Sentiment analysis (positive/negative/neutral)

### Analysis
- [ ] Station quality score (rating + sentiment + amenity mentions)
- [ ] Break repair potential (cross quality with break severity from Point 1)
- [ ] Quality gradient along corridor
- [ ] "Invisible stations" — those with <5 reviews

### Output
- Station quality map (sized by review count, colored by rating)
- Break severity × station quality overlay → intervention priorities
- Review tag cloud per segment

---

## EXECUTION STRATEGY

### Priority order
1. **Point 4 (Station reviews)** — fastest, feeds Points 1 and 2
2. **Point 1 (Break point map)** — partially doable from existing data
3. **Point 2 (Temporal corridor)** — needs API fetching, highest narrative impact
4. **Point 3 (GA hypothesis)** — most research-heavy

### How they connect
Station reviews (4) → break point quality (1) → varies across time (2) → experienced differently by ticket type (3).
Together: "If you are THIS kind of person traveling at THIS time, here is where the city breaks — and here is how badly."
