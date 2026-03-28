# Lock Type 08 — ALTITUDE LOCK South Variant (Generic Concept)

## Rhino target
Instance: `lock_08` (port 9008)
All MCP tool calls must include `target: "lock_08"`

## Role
You are a modeler building a pure architectural concept — no site, no terrain, no context buildings. Origin at (0, 0, 0). This is a typological study.

## Concept: The Altitude Lock — Asymmetric Variant

**What it is:** Same spatial type as Type 03 (vertical connector between valley and hilltop), but with ASYMMETRIC ENDS reflecting different temporalities. The bottom station handles emergency (fast, urgent, compact). The top station handles rehabilitation (slow, expansive, peaceful). The cable connects two opposite speeds.

**Spatial metaphor:** Same funicular as Type 03, but the two terminal buildings are dramatically different. One is an emergency room entrance — compressed, efficient, urgent. The other is a rehabilitation garden — open, slow, generous. The mechanical connection between them is the same, but what happens at each end is opposite.

**State transition:** Acute care (fast, below) ↔ Rehabilitation (slow, above)

**What makes it different from Type 03:**
- Type 03: both ends are similar (valley station ≈ hilltop station, symmetric twins)
- Type 08: bottom is COMPACT and URGENT, top is EXPANSIVE and SLOW
- The inclined connection is the same, but the endpoints express opposite programs
- This is about connecting two TEMPORALITIES through altitude, not just two locations

## Volumes to model

### Overall envelope: 20m (X) × 40m (Y, slope axis) × 24m (Z total rise)

### 1. Valley Station — Emergency Interface (compact, urgent)
- Position: X = [-5, 5], Y = [-5, 5], Z = [0, 5]
- 10m × 10m × 5m — SMALLER than Type 03's valley station
- Dense, efficient — emergency intake logic
- South face (Y = -5): narrow entry with canopy (ambulance pull-up)
  - Entry opening: X = [-2, 2], Z = [0, 3.5] (4m wide only)
- Thick walls (0.4m) — protective, institutional
- Minimal windows — 2 slot windows on east and west faces, Z = [2, 4], 1m wide
- Low ceiling relative to footprint — compressed, pressurized feeling

### 2. Inclined Track / Inhabited Slope (shared with Type 03)
- Position: X = [-3, 3], Y = [5, 35], Z = [5, 21]
- 6m wide tube rising from Z = 5 to Z = 21 over 30m (Y)
- Same grade as Type 03 (53%)
- Two tracks: ascending + descending (counterbalanced)
- Midpoint landing at Y = 20, Z = 13
- But here: the windows along the track get LARGER as you ascend
  - Bottom third: 0.8m × 1m slots
  - Middle third: 1.2m × 1.5m windows
  - Top third: 2m × 2m openings approaching the top
- The ascent gradually reveals the landscape — transition from urgency to calm

### 3. Hilltop Station — Rehabilitation Pavilion (expansive, slow)
- Position: X = [-10, 10], Y = [35, 50], Z = [21, 27]
- 20m × 15m × 6m — BIGGER than valley station (double the footprint)
- Open, generous — rehabilitation, family visits, slow time
- North face (Y = 50): full-width glazing, X = [-8, 8], Z = [22, 26] — panoramic view
- East and west faces: floor-to-ceiling windows with deep reveals (0.5m)
- Terrace/veranda wrapping north and east: extends 3m beyond envelope
  - X = [-10, 13], Y = [48, 53], Z = [21, 21.1] (outdoor platform)
- High ceiling — airy, decompressed
- Thin walls (0.2m) — light, permeable

### 4. Vertical Core (same as Type 03 but shorter)
- Position: X = [-3, 3], Y = [42, 48], Z = [21, 28]
- 6m × 6m × 7m — mechanical room + stair
- Less prominent than Type 03's tower — the hilltop pavilion is the landmark, not the tower
- Enclosed, functional

### 5. Terrain Proxy (abstract slope)
- Tilted surface from (Y = -5, Z = -1) to (Y = 50, Z = 20)
- Thin, wireframe

### 6. Garden Platform (at hilltop)
- Position: X = [-14, 14], Y = [45, 55], Z = [20.5, 21]
- 28m × 10m platform extending beyond building — rehabilitation garden ground plane
- Thin slab (0.5m), slightly below hilltop floor
- Marks the expansive territory of the slow end

## Circulation
- **Emergency arrival:** South entry (Y = -5, Z = 0.5) → valley hall → inclined track UP
- **Rehabilitation arrival:** Track TOP → hilltop pavilion → terrace → garden
- **Visitor path:** Same as emergency arrival but slower (family coming to visit rehab patients)
- **Descent (discharge):** Hilltop → track DOWN → valley → exit south
- Model ascending and descending as two parallel diagonal polylines (offset 1m in X)
- Model terrace stroll as a loop on the garden platform

## Structure
- Valley station: 4 columns at corners, 0.4m × 0.4m (heavy)
- Hilltop pavilion: 6 columns, 0.2m × 0.2m (light, slender) — at X = [±8, 0], Y = [38, 47]
- Terrace: 4 thin columns supporting overhang, 0.15m × 0.15m
- Inclined track: same as Type 03 (longitudinal beams + support frames every 5m)
- Core: 4 columns, 0.3m × 0.3m

## Openings
- Valley south entry: Y = -5, X = [-2, 2], Z = [0.5, 3.5] (small, controlled)
- Valley slots: X = ±5, Y = [-2, 2], Z = [2, 4] (minimal)
- Track windows: progressive sizing (described above)
- Hilltop north: full glazing, Y = 50, X = [-8, 8], Z = [22, 26]
- Hilltop east/west: large windows, Z = [21.5, 26], 4m wide each
- Terrace: open (no walls, just roof/canopy above)

## Layers
- `Type_08_AltitudeS::Volumes` — color (252, 196, 25)
- `Type_08_AltitudeS::Circulation` — color (253, 220, 120)
- `Type_08_AltitudeS::Structure` — color (178, 140, 18)
- `Type_08_AltitudeS::Openings` — color (252, 210, 80)
- `Type_08_AltitudeS::Annotations` — color (253, 235, 170)
- `Type_08_AltitudeS::TerrainProxy` — color (140, 120, 50)

## Annotations (text dots)
- Valley station: "EMERGENCY / FAST / COMPACT"
- Midpoint: "TRANSITION / WINDOWS GROW"
- Hilltop pavilion: "REHABILITATION / SLOW / EXPANSIVE"
- Terrace: "GARDEN / RECOVERY"
- Track: "ASCENDING = DECELERATING"

## Key design principle
The two ends must feel OPPOSITE. Valley = small, thick walls, few openings, urgent. Hilltop = large, thin walls, panoramic views, peaceful. The track between them is the gradient — not just of altitude but of SPEED. You physically slow down as you rise.

Type 03 vs Type 08 comparison:
- Type 03: symmetric twins (valley ≈ hilltop, same program)
- Type 08: asymmetric opposites (emergency ≠ rehabilitation)

## Success criteria
- Valley station is visibly SMALLER and more ENCLOSED than hilltop
- Hilltop pavilion is visibly LARGER and more OPEN
- Track windows grow larger as they ascend — visible gradient of transparency
- The terrace/garden platform reads as generous outdoor space
- When compared side-by-side with Type 03, the asymmetry is immediately visible
- Someone sees: "this connects urgency below with calm above"
