# PLAN: Corridor Animation Maps

## Overview
Two interactive animated maps for the Geneva-Villeneuve corridor (City101 project).
These maps support the design argument for aerial gondola / horizontal elevator placement
by showing WHERE trains run, WHEN they're busiest, and WHO is on them.

Architecture studio context: EPFL BA6, Studio Huang "Sentient Cities."
Final project: aerial gondola or horizontal elevator system for the corridor.

---

## MAP 1: Train Pulse — 24h Frequency Animation

### Concept
An animated map showing every train on the corridor over 24 hours.
Trains appear as moving dots along their routes. Where tracks are heavily used,
overlapping trails create a "long exposure" glow effect — busier segments burn brighter.

The background map transitions through sky colors matching time of day:
- Night (00:00-05:30): dark navy/deep blue, minimal ambient light
- Pre-dawn (05:30-06:30): deep blue → violet → first hint of warm light on horizon
- Sunrise (06:30-07:30): pink/coral/amber gradient, warm pastels
- Morning (07:30-10:00): brightening to clean daylight blues
- Midday (10:00-14:00): full bright, slight warm white/pale blue
- Afternoon (14:00-17:00): warm golden light starts creeping in
- Golden hour (17:00-18:30): amber/gold, warm tones
- Sunset (18:30-19:30): orange → pink → violet
- Dusk (19:30-20:30): violet → deep blue
- Night (20:30-24:00): back to dark navy

### Data needed

**CRITICAL — GTFS timetable data:**
- Source: opentransportdata.swiss (Swiss GTFS feed) or transport.opendata.ch
- What we need: stop_times.txt, trips.txt, routes.txt, stops.txt, calendar.txt
- This gives us: every train's departure/arrival at every station, route geometry
- Filter to: corridor stations only (Geneva to Villeneuve, 49 stations)
- Filter to: rail only (route_type = 2 in GTFS), exclude buses/trams/metros

**Route geometry:**
- GTFS shapes.txt (if available) gives exact track geometry
- Fallback: interpolate straight lines between station coordinates
- Better fallback: OSM railway lines for the corridor (already partially in QGIS project)

**What to compute from GTFS:**
- For each minute of a 24h period, which trains are in motion and where
- Position = linear interpolation between last station and next station based on time
- Accumulate all positions over time → frequency heatmap per track segment
- Peak detection: identify the morning rush, evening rush, midday lull, late night

### Visualization approach
- Leaflet.js or Mapbox GL for the base map
- Canvas overlay for the train dots and trails (better performance than SVG for animation)
- Trail persistence: each train leaves a fading trail behind it
- Segment brightness = cumulative trail density (more trains = brighter glow)
- Color scheme for trains: white/gold dots, trails fade from gold → transparent
- Time scrubber: user can drag to any time, or press play for animation
- Speed control: 1 min = ~0.5s real time (so 24h plays in ~12 minutes at 1x)
- Counter overlay: show current time, number of active trains, trains/hour

### Separate layers (toggleable)
- Trains (rail): primary, always visible
- S-Bahn/RER: regional trains, slightly different color
- Metros (Lausanne M1/M2): different color, optional
- Trams (Geneva): different color, optional
- Buses: probably too many, maybe exclude or show as very faint

---

## MAP 2: Passenger Flow — Who's On The Trains

### Concept
Show actual (estimated) passenger volume on trains throughout the day.
Instead of every train being the same dot, the dot size or brightness represents
how many people are aboard. Stations pulse when passengers board/alight.

Like the Manhattan Population Explorer but for a linear corridor:
watch the population shift from residential areas to work hubs in the morning,
then reverse in the evening.

### Data needed

**Station-level passenger counts:**
- Source: SBB Passagierfrequenz (already partially in our data as city101_transport_frequency.csv)
- What it gives: daily average passengers per station, possibly with time-of-day breakdown
- URL: data.sbb.ch or opentransportdata.swiss
- This is the foundation — how many people use each station per day

**Ridership estimation approach (reverse engineering):**
Since per-train occupancy isn't published, estimate it:
1. Take daily passenger count per station (SBB data)
2. Distribute across departures using time-of-day weight curve:
   - Morning peak (07:00-09:00): ~25% of daily passengers
   - Midday (09:00-16:00): ~30% spread across 7 hours
   - Evening peak (16:00-19:00): ~25% of daily passengers  
   - Off-peak (19:00-07:00): ~20% spread across 12 hours
3. For each train departure, estimate boarding = station_daily_pax × time_weight / departures_in_window
4. Accumulate passengers along the route (board at each station, subtract estimated alighting)

**Demographic overlay data (for gondola placement argument):**
- BFS/OFS commune-level census data: population, age distribution, profession categories
- Frontalier (cross-border commuter) counts by commune: OFAS data
- Commune-level commute mode split: % car, % train, % bus, % bike, % walk
- Employment by sector per commune: primary/secondary/tertiary
- Sources: bfs.admin.ch, STATPOP, structural survey

**Additional useful data:**
- SBB load factor reports (if published): actual vs. capacity
- Google Popular Times for major stations (proxy for hourly flow patterns)
- Pendlermobilität (commuter mobility) from BFS — origin-destination matrices

### Visualization approach
- Same base map as Map 1 (same sky color transitions)
- Train dots sized by estimated passenger count
- Station circles pulse on boarding/alighting events
- Station "reservoir" visualization: show waiting passengers accumulating
- Corridor cross-section view (optional): like a bar chart along the line showing volume
- Demographic layer: choropleth of communes colored by dominant commute mode or age
- Time scrubber + play controls (same as Map 1)

---

## DATA RESEARCH TASKS (for agent teams)

### Task 1: GTFS Data Acquisition
- Download Swiss GTFS feed from opentransportdata.swiss
- Filter to corridor extent (Geneva → Villeneuve bounding box)
- Extract: stops, stop_times, trips, routes, shapes, calendar
- Filter route_type: trains only (type 2), then separately metros/trams/buses
- Compute: for a typical weekday, how many unique train trips traverse the corridor?
- Output: cleaned CSV with columns: trip_id, route_name, stop_sequence, stop_name, arrival_time, departure_time, lat, lon

### Task 2: Passenger Count Data
- Search data.sbb.ch for Passagierfrequenz dataset
- Search opentransportdata.swiss for ridership data
- Search BFS for public transport statistics (T-Bahnen, Pendlerstatistik)
- Check if SBB publishes hourly passenger distribution curves
- Check if SBB publishes seat occupancy / load factors per line
- Cross-reference with our existing city101_transport_frequency.csv
- Output: station-level daily passenger counts + hourly distribution weights

### Task 3: Demographic Data
- BFS STATPOP: population per commune along corridor
- BFS structural survey: age distribution, profession, commute mode per commune
- OFAS frontalier statistics: cross-border commuters by commune/canton
- Search for pendlermobilität (commuter mobility) origin-destination data
- GeoJSON of commune boundaries along corridor (already partially in QGIS)
- Output: commune-level CSV with pop, age_brackets, profession_categories, commute_mode_split

### Task 4: Route Geometry
- Extract rail lines from existing QGIS project or OSM
- Match GTFS route_ids to physical track geometry
- Create simplified GeoJSON linestrings for each rail line in the corridor
- Include: Geneva CEVA line, main SBB line, MOB narrow gauge, MVR, NStCM, etc.
- Output: GeoJSON with route geometries + metadata

---

## BUILD SEQUENCE

### Phase 1: Data (agent teams — parallel)
Run tasks 1-4 in parallel. Each agent works independently.
All outputs go to ~/CLAUDE/City101_ClaudeCode/source/animation/

### Phase 2: Map 1 prototype
Build the train frequency animation first — it depends only on GTFS data.
Start with a static frame (all trains at 08:00), then add time animation.
Then add the sky color transitions.

### Phase 3: Map 2 prototype
Layer passenger estimates on top of the same framework.
Start with station-level bubbles sized by daily volume.
Then add time-based distribution.

### Phase 4: Combine + demographic overlay
Merge both maps or create a toggle between them.
Add commune-level demographic choropleth as a toggleable base layer.

### Phase 5: Polish
- Design language: Archipelago (dark theme, gold accents, Instrument Serif / DM Sans)
- Smooth animations, responsive controls
- Export options for presentation (video capture, high-res screenshots)

---

## NOTES
- Coordinate system: WGS84 for web maps (Leaflet/Mapbox use WGS84 natively)
- Keep LV95 versions of all data for QGIS integration
- All intermediate data saved to ~/CLAUDE/City101_ClaudeCode/source/animation/
- Final HTML outputs to ~/CLAUDE/City101_ClaudeCode/output/
- This plan is for the DATA RESEARCH phase — the visualization build comes after
