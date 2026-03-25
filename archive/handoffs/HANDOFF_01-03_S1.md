# HANDOFF — 01-03 Session 1 (Cairn, browser)

## Last action
Produced and validated two new transport datasets via Claude Code. Reviewed data plan status and confirmed next priorities.

## What happened this session

### Two new datasets landed
Both scripts were written in the previous session (28-02 late) but couldn't be downloaded due to context compaction. Recreated and downloaded this session, Claude Code ran them locally.

**1. Service frequency v2** — `city101_service_frequency_v2.csv` (49 stations)
- Source: transport.opendata.ch/v1/stationboard
- Measures: trains/hour during workday morning (7-9am, next Monday)
- Columns: name, station_id, lat/lon, departures_7to9, trains_per_hour, avg_wait_minutes, ic_ir/regional/metro_tram/other departures, category_breakdown, operators, sample_destinations, query_date
- v1 had a critical bug: limit=30 capped all stations at ~30 trains/hr, making Lausanne look the same as Épesses. v2 fixed this — real variation now visible.
- **Key numbers**: Lausanne 28.5 tr/hr (2 min wait), Renens 26.5, Genève 25.0, Vevey 20.0 → Cully 9.0, Grandvaux 4.5, Rivaz 3.5, Épesses 3.0, Bossière 2.0, St-Saphorin 0.0. **42x frequency ratio** across the corridor.
- Vernier at 84 is tram/metro (73 metro departures) — flag separately from rail.
- Capacity/occupancy data (capacity1st/2nd) was NOT available from the stationboard endpoint. The v1 script had columns for it but they were all empty. v2 dropped them. Capacity would require the /v1/connections endpoint (point-to-point journeys), a different and more complex query.

**2. Ridership (SBB Passagierfrequenz)** — `city101_ridership_sbb.csv` (174 stations)
- Source: data.sbb.ch passagierfrequenz dataset
- Columns: code, uic, name, canton, infrastructure_manager, year, daily_avg, workday_avg, nonworkday_avg, commuter_index, transport_companies, lat/lon, remarks
- Commuter index = workday_avg / nonworkday_avg. High = commuter-dominated, low = leisure/tourism.
- **Key findings**: Lausanne 102,800 daily, Genève 80,600. Lancy-Pont-Rouge CI=4.04 (pure commuter), Genève-Sécheron CI=4.53, Montreux CI=1.02 (balanced), Genève-Aéroport CI=0.90 (leisure-dominated), Épesses CI=0.47 (wine tourism), Jaman CI=0.40.
- 174 stations is far more than Henna's 22 — this covers the full corridor including tiny stops.

### Narrative clarification
EV charging confirmed as **supporting evidence, not primary dataset** for A02. The working continuity narrative is about the universal commuter/knowledge worker, not the EV driver subset. EV data's best contribution: confirming the Lavaux gap from a third angle and the "dwell time as design opportunity" concept. But train frequency now demonstrates both of those things better and more universally. This was already decided at 24-02 ("narrative pivot: from separate EV + wifi → unified working continuity") — this session just made it explicit.

### Data plan status check
Reviewed the comprehensive data plan (5 layers + Zurich). Current state:

| Layer | Status | What's done | What's missing |
|-------|--------|------------|----------------|
| 1. Digital Backbone | 🟡 | Cell towers (3,218), WiFi (81) | Train WiFi quality, signal dead zones |
| 2. Workspace Availability | 🟡 | Remote work places (68), reviews (109) | Station amenities |
| 3. Temporal Access | 🟡 | **Train frequency (49 stations) — NEW** | **Opening hours (68 places) — #1 PRIORITY**, first/last train, weekend patterns |
| 4. Transit Continuity | 🟢 | **Ridership (174 stations) — NEW**, transit stations, bus stops | Intermodal connections, bike-share |
| 5. Comfort | 🟢 | Acoustic cross-ref, grocery cross-ref, ratings | — |
| 6. Zurich Comparison | 🔴 | Nothing | Everything |

## Files created/modified this session
- `~/CLAUDE/City101_ClaudeCode/source/city101_service_frequency_v2.csv` (49 rows, by Claude Code)
- `~/CLAUDE/City101_ClaudeCode/source/city101_ridership_sbb.csv` (174 rows, by Claude Code)
- `~/CLAUDE/City101_ClaudeCode/source/fetch_transport_frequency_v2.py` (v2 script, by Claude Code)
- `~/CLAUDE/City101_ClaudeCode/source/fetch_ridership.py` (ridership script, by Claude Code)
- v1 files also in source/ (city101_service_frequency.csv, fetch_transport_frequency.py) — kept for reference

## What to do next (priority order)

1. **Opening hours for 68 remote work places** — Cairn has Google Places API access + all place_ids are in city101_remote_work_places.csv. This is the #1 gap. Without temporal data, "working continuity" is spatial only. Assign to Cairn next session.
2. **Load new datasets into QGIS** — frequency + ridership as point layers, EPSG:2056. Cross-reference with existing layers.
3. **First/last train per station** — derivable from the same transport.opendata.ch API, query earliest/latest departures instead of 7-9am window.
4. **Segment framework** — divide corridor into ~50 segments for spatial aggregation. Claude Code task.
5. **Zurich comparison** — if time before 03.03 deadline.

## Key decisions made (cumulative)
- Two-color map logic: MAP1 (teal/amber), MAP3 (coral/teal-green) — from S6 17-02
- Backbone principle: each map has one infrastructure spine — from S5 17-02
- Monolithic script pattern for large data ops — established early
- **Narrative pivot**: from separate EV + wifi → unified "working continuity as a flow" — 24-02, teacher-endorsed
- **EV charging = supporting evidence only** for A02, not primary dataset — confirmed 01-03
- **Train frequency limit bug**: API limit=30 makes all stations look identical. Must use high limit or no limit. — 01-03

## Technical notes
- transport.opendata.ch API: x=latitude, y=longitude (reversed from typical). Unofficial API, rate limit 0.5s between calls.
- SBB passagierfrequenz: semicolon-delimited CSV, geopos field is "lat, lon" string
- Stationboard endpoint does NOT return capacity1st/capacity2nd — connections endpoint might, but untested
- data.sbb.ch and transport.opendata.ch both blocked from claude.ai container — scripts must run locally via Claude Code or desktop MCP
