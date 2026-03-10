# Point 2: The Temporal Corridor — Execution Prompt
**For**: Cairn (desktop with MCP) or Claude Code
**Priority**: HIGH — highest narrative impact for A02 and beyond
**Prerequisites**: First/last train data (Henna's task). If not available, can still do partial.

---

## Goal

Map the same 101km corridor at **different times of day**. The corridor pulses — compute a temporal WCI showing when and where working continuity exists vs collapses.

## The argument

"The linear city doesn't just break in SPACE — it breaks in TIME. At 7am, 35 of 49 stations are workable. By 11pm, only 3 remain."

## Data we have

1. **Service frequency v2** (`datasets/transit/city101_service_frequency_v2.csv`) — 49 stations, trains/hr during 7-9am peak. BUT this is only one time window.
2. **Remote work HOURS** (`datasets/remote_work/city101_remote_work_HOURS.csv`) — 63 places with Mon-Sun opening hours, early/late/weekend flags.
3. **WCI corridor segments** (`datasets/corridor_analysis/city101_corridor_segments_WCI.csv`) — current spatial WCI (time-agnostic).
4. **Break points** (`datasets/corridor_analysis/city101_break_points.csv`) — 49 stations, 5 break dimensions.

## What we need to fetch

### A. Multi-slot train frequency (CRITICAL)
Query transport.opendata.ch stationboard for each of 49 stations at 7 time windows:

| Slot | Window | Why |
|------|--------|-----|
| early_morning | 05:00-07:00 | First trains, shift workers |
| am_peak | 07:00-09:00 | Already have this data |
| midday | 11:00-13:00 | Lunch break, off-peak |
| pm_peak | 16:00-18:00 | Return commute |
| evening | 19:00-21:00 | Late workers, culture |
| late_night | 21:00-23:00 | Last trains |
| weekend_mid | Sat 11:00-13:00 | Non-commuter corridor |

**API call per station per slot:**
```
GET https://transport.opendata.ch/v1/stationboard?station={name}&datetime={date}T{time}&limit=200&type=departure
```

Use a Monday for weekday slots, a Saturday for weekend. Date: 2026-03-02 (Monday) and 2026-03-07 (Saturday).

**CRITICAL**: Do NOT set limit=30 (it caps the data). Use limit=200 and count departures within the 2hr window yourself. Previous session learned this the hard way — see LEARNINGS.md.

**Script pattern**: Monolithic. Loop stations × slots, sleep 0.3s between calls, write one CSV. ~350 API calls total = ~2 min.

### B. First/last train per station
If Henna hasn't done this yet:
- Query stationboard at 04:00 (first) and 23:59 (last) for each station
- Extract earliest departure and latest departure
- This gives the "temporal corridor width" — how many hours each station is accessible

### C. Temporal WCI computation
For each station × time slot, compute:
1. **Transit score**: frequency in that slot (normalized to max)
2. **Workspace score**: number of workspaces open during that slot (from HOURS data, cross-reference opening times)
3. **Connectivity score**: cell towers don't change by time → constant
4. **Temporal score**: 1 if any workspace is open AND any train runs, 0 if either is zero

**Temporal WCI** = same formula as spatial WCI but recomputed per slot.

## Output files

1. `city101_temporal_frequency.csv` — 49 stations × 7 slots, trains/hr per slot
2. `city101_temporal_WCI.csv` — 49 stations × 7 slots, WCI per slot
3. `city101_temporal_summary.csv` — per-slot aggregates (how many stations workable, average WCI, etc.)
4. `TEMPORAL_CORRIDOR_FINDINGS.md` — key numbers, the pulsing narrative

## Key numbers to extract

- How many stations are "workable" (WCI > 0.2) at each time slot?
- When does the Lavaux Fracture open (first train) and close (last train)?
- What's the latest you can work continuously Geneva→Villeneuve?
- Weekend vs weekday: does the corridor shrink or grow?
- The "11pm corridor" — which 3-5 stations still function as a city?

## Visualization

In QGIS: create a temporal map series (7 maps, same extent, different WCI colors per slot). Or a single map with pie charts showing temporal coverage per station.

## Time budget

- API fetching: 30 min (350 calls)
- Processing + WCI: 20 min
- Findings: 10 min
Total: ~60 min

## Network note

`transport.opendata.ch` is in the allowed domains list. Rate limit: 0.3s between calls minimum.
