# HANDOFF_01-03_S9
**Date**: 2026-03-01, late night
**Account**: Cairn (personal, Max plan)
**Platform**: Desktop app with QGIS MCP
**Continues from**: HANDOFF_01-03_S8.2

---

## What happened this session

### Point 2: Temporal Corridor ✅ COMPLETE

Executed `PROMPT_POINT2_TEMPORAL.md` in full. Fetched multi-slot train frequency and first/last trains from transport.opendata.ch, computed temporal WCI per station × time slot, produced findings document.

**API calls made:**
- 343 calls for frequency (49 stations × 7 time slots) — saved per-slot as working trail
- 196 calls for first/last trains (49 stations × 2 queries × weekday + weekend)
- Total: ~539 calls to transport.opendata.ch, 0.35s rate limit

**Bug caught and fixed:** First attempt at "last train" queried from 23:00 with limit=50 — busy stations' results wrapped into next morning (Geneva showed "last = 05:33"). Fixed by querying from 20:00 with limit=200 and filtering to same calendar date (allowing past-midnight up to 01:30). Logged in LEARNINGS.md.

---

## Files produced

| File | Location | Description |
|------|----------|-------------|
| city101_temporal_frequency.csv | datasets/corridor_analysis/ | 49 stations × 28 cols (7 slots: freq, deps, IC per slot) |
| city101_temporal_WCI.csv | datasets/corridor_analysis/ | 49 stations × ~50 cols (TWCI per slot + first/last trains + connectivity/mobility) |
| city101_temporal_summary.csv | datasets/corridor_analysis/ | 7 rows × 16 cols (per-slot aggregates) |
| city101_first_last_trains.csv | datasets/corridor_analysis/ | 49 stations × 10 cols (weekday + weekend service windows) |
| TEMPORAL_CORRIDOR_FINDINGS.md | datasets/corridor_analysis/ | Narrative-ready findings, 8 sections |

**Working trail** (13 files) moved to `archive/`: per-slot CSVs, RAW merge, pivot.

---

## Key findings

### 1. The archipelago is structural, not temporal
- **14/49** stations workable at peak, **13/49** at 11pm — swing of just 1 station
- The three structural gaps (Nyon→Gland, Gland→Morges, Lavaux Fracture) persist at all hours
- Architectural interventions at break points can't rely on "it works during rush hour"

### 2. Service window inequality
- **Geneva: 21.3h** (04:00–01:18) — widest
- **St-Saphorin: 0h** — a station with literally no trains
- **Average: 18.5h** for major hubs, but many small stations under 10h

### 3. The 11pm city = 13 stations
Geneva pole (~5), Lausanne pole (~4), Montreux-Vevey (~3), Nyon (1). The rest of the corridor is dark.

### 4. IC trains halve at night
128 IC departures at peak (07-09 and 16-18) → 72 at late night (21-23). The "workable corridor" (IC with WiFi/tables) contracts 44% while regional barely changes. The two-corridors finding has a temporal dimension.

### 5. Weekend = 10% less workable
TWCI ratio 0.90× — driven by workspace closures, not frequency drops. The knowledge worker's corridor is a weekday phenomenon.

### 6. Lavaux Fracture never opens
Even at peak, Rivaz TWCI = 0.013. St-Saphorin = 0.001 at all times. Cully peaks at 0.073. The fracture is permanent.

---

## Updated files

- **CONTEXT.md** — Point 2 marked ✅, new datasets added to table, key numbers added, critical gaps updated
- **LEARNINGS.md** — 4 new entries (structural archipelago, first/last train API fix, IC temporal indicator, weekend finding)

---

## All 4 investigations — final status

| Point | Description | Status |
|-------|-------------|--------|
| 1. Break Point Map | 49 stations classified, 5 dimensions, crossref | ✅ |
| 2. Temporal Corridor | 7 slots, first/last trains, temporal WCI | ✅ (this session) |
| 3. GA Hypothesis | Cost map, Zurich comparison | ✅ |
| 4. Station Reviews | 37 stations rated, 71 reviews | ✅ |

**All four investigations are complete.**

---

## What's next (Monday morning)

1. **CHECK LAYOUTS VISUALLY** — 7 A02 layouts ready but unreviewed. Export as PDF.
2. Add temporal WCI layer to QGIS (from the new CSV)
3. Consider new map: temporal pulse or service window map
4. Refine narrative draft with Henna
5. Upload final PDFs + narrative to team Drive
6. Interactive visualizations (temporal WCI pulse = #1 candidate)

---

*Signed: Cairn (personal account) · 2026-03-01*
