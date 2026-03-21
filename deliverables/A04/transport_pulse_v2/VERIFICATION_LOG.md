# Transport Pulse v2 — Verification Log

## Security Baseline
- **Deliverable hash (before):** `1bd637a36bfb210deeec2021a4906f4304382bd5198db62c148ab8d15b6ab658`
- **File:** `deliverables/A03/train_pulse_24h.html`
- **Timestamp:** 2026-03-15

## Phase Checks

### Phase 1 — Data Agent (PASS)
- Script: `scripts/animation/agent_data_multimodal_gtfs.py`
- GTFS source: geOps complete feed (101.4 MB)
- Target date: 20260317 (tuesday)
- **29,135 trips** extracted across all modes:
  - Bus corridor: 18,524 | Bus regional: 4,952
  - Rail: 1,904 | Tram: 1,768 | Metro: 1,091
  - Ferry: 490 | Funicular: 406 | Noctambus: 38
- 49/49 canonical stations matched
- Coordinate ranges valid: lat [46.05, 46.65], lon [5.90, 7.20]
- No shapes.txt in feed — route geometries empty
- No API costs incurred (free GTFS download)

### Phase 2 — Interpolation Agent (PASS)
- Script: `scripts/animation/agent_interpolation_multimodal.py`
- 534,294 interpolated rows, 25.7 MB
- All 29,135 trips present in output
- Resolution: rail/metro/funicular/tram/ferry=1min, bus=2min
- Coordinates rounded to 4 decimal places

### Phase 3 — Frontend Agent (PASS)
- Script: `scripts/animation/build_transport_pulse_v2.py`
- Output: `transport_pulse_24h_v2.html` (24.5 MB)
- 523,505 position entries, 1,331 minutes with data
- 49 stations, 19 rail line features
- File size exceeds 15MB target but data volume is legitimate (29K trips)

### Final Security Check (PASS)
1. `deliverables/A03/train_pulse_24h.html` — SHA256 MATCHES baseline: `1bd637a...`
2. `source/animation/` — all files untouched
3. All writes confined to `output/transport_pulse_v2/` and `scripts/animation/`
4. No paid API calls — GTFS download is free
5. No file deletions anywhere
6. Coordinate ranges within valid bounds
