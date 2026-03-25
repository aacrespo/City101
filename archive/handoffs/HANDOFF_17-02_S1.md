# HANDOFF — 17-02 Session 1

## Last action
Set up handoff workflow system across two Claude accounts. No analytical work done this session — focused on workflow optimization.

## Current state
- 194 EV charging points compiled along City101 corridor (merged from Google Places + OSM)
- Data deduplicated using haversine distance calculations
- Dataset loaded in QGIS with Swiss LV95 (EPSG:2056) coordinates
- Working on classifying stations by "dwell context" (user behavior patterns at charging locations)

## Open threads
- Dwell context classification system not yet finalized — how to categorize charging stations by what people do while waiting (shopping, working, eating, etc.)
- Need a second dataset for A.01 (due 23.02) — one "straightforward" and one "creative"
- Need to think about datasets as *flows/movements*, not just static points
- Connection to sentient city narrative still needs articulation

## Key decisions made (cumulative)
- Framing is "flow of people" not energy infrastructure (energy = Siméon's territory)
- EV charging stations analyzed through human experience lens, not technical specs
- Using both Google Places + OSM sources, cross-referenced and deduplicated
- LV95 / EPSG:2056 as working coordinate system

## Technical notes
- QGIS project uses Swisstopo geodata (TLM3D, Boundaries, SWISSBUILDINGS)
- OSM MCP server needed SSL certificate fix on macOS to work
- pyproj used for coordinate transformations
- Haversine with ~50m threshold for deduplication (verify this number)
