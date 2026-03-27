# Lock Type 03 — ALTITUDE LOCK (Generic Concept)

## Rhino target
Instance: `lock_03` (port 9003)
All MCP tool calls must include `target: "lock_03"`

## Role
You are a modeler building a pure architectural concept — no site, no terrain, no context buildings. Origin at (0, 0, 0). This is a typological study.

## Concept: The Altitude Lock

**What it is:** A vertical connector between two settlements at different elevations. Two communities live at different heights — one in the valley, one on the hilltop — and this lock bridges the altitude gap. The building IS the gradient.

**Spatial metaphor:** A funicular station — but as inhabitable architecture, not just a platform. Two counterbalanced cars on a single cable: one goes up as the other comes down. The movement creates twin settlements.

**State transition:** Valley (low) ↔ Hilltop (high)

**What makes it an ALTITUDE lock:**
- The building follows a slope — it is NOT level
- Base and top are architecturally different (valley = arrival, hilltop = destination)
- The inclined connection IS the main architectural space, not just a corridor
- Movement is diagonal — neither purely horizontal nor purely vertical
- Counterbalance logic: what goes up enables what comes down

## Volumes to model

### Overall envelope: 16m (X) × 40m (Y, slope axis) × 24m (Z, total rise)
The Y-axis represents the slope. Z rises as Y increases.

### 1. Valley Station — base
- Position: X = [-8, 8], Y = [-5, 5], Z = [0, 6]
- 16m × 10m × 6m — horizontal volume, grounded
- Wide and welcoming — arrival/departure hall
- Large opening on south face (Y = -5) — approach from valley
- Floor at Z = 0

### 2. Inclined Track / Inhabited Slope
- Position: X = [-3, 3], Y = [5, 35], Z = [6, 22]
- 6m wide tube rising from Z = 6 to Z = 22 over 30m horizontal (Y)
- Grade: 53% (16m rise / 30m run) — expressed as architectural form, not accessible ramp
- This is the funicular/inclined elevator shaft — but wide enough to inhabit
- Two parallel tracks within: ascending car + descending car (counterbalanced)
- Intermediate landing at Y = 20, Z = 14 (midpoint rest)
- Structure visible: exposed rail or cable guides along walls

### 3. Hilltop Station — summit
- Position: X = [-8, 8], Y = [35, 45], Z = [22, 28]
- 16m × 10m × 6m — horizontal volume at top
- Opening on north face (Y = 45) — exit to hilltop settlement
- Floor at Z = 22
- Mirror of valley station but ELEVATED — same footprint, different world

### 4. Vertical Tower / Marker
- Position: X = [-3, 3], Y = [35, 41], Z = [22, 32]
- 6m × 6m × 10m tower rising above hilltop station
- Mechanical room (cable machinery) + observation
- Landmark visible from valley — marks the vertical connection
- Open top or lattice structure at crown

### 5. Terrain Proxy (abstract slope)
- A tilted surface from (Y = -5, Z = -1) to (Y = 45, Z = 21)
- Represents the hillside — NOT actual terrain, just a slope reference plane
- Thin surface (not solid), transparent or wireframe
- Shows that the building follows the natural grade

## Circulation
- **Ascending path:** Valley entry (Y = -5, Z = 0) → valley hall → inclined track → midpoint landing → inclined track → hilltop hall → hilltop exit (Y = 45, Z = 22)
- **Descending path:** Same route in reverse (counterbalanced — simultaneous movement)
- **Vertical emergency:** Stair in tower from Z = 22 to Z = 32
- Model ascending path as polyline on Circulation layer (diagonal line from base to top)
- Model midpoint landing as a small horizontal platform

## Structure
- Valley station: 4 corner columns, 0.35m × 0.35m
- Hilltop station: 4 corner columns, 0.35m × 0.35m
- Inclined track: 2 longitudinal beams along X = ±3, following slope (Z = 6 to 22)
- Track supports: every 5m along slope (6 support frames, each an inverted U)
- Tower: 4 vertical columns at corners, bracing at Z = 25, 28

## Openings
- Valley south entry: Y = -5, X = [-4, 4], Z = [0.5, 4.5]
- Hilltop north exit: Y = 45, X = [-4, 4], Z = [22.5, 26.5]
- Inclined track sides: continuous slot windows, X = ±3, Z varies with slope, 1.5m tall — view out during ascent
- Tower top: open on all 4 faces, Z = [28, 32], X = [-2, 2], Y = [36, 40]
- Midpoint landing window: X = [-3, 3], Y = 20, Z = [14.5, 16.5]

## Layers
- `Type_03_Altitude::Volumes` — color (255, 212, 59)
- `Type_03_Altitude::Circulation` — color (255, 230, 140)
- `Type_03_Altitude::Structure` — color (180, 150, 40)
- `Type_03_Altitude::Openings` — color (255, 225, 100)
- `Type_03_Altitude::Annotations` — color (255, 240, 180)
- `Type_03_Altitude::TerrainProxy` — color (120, 110, 80)

## Annotations (text dots)
- Center of valley station: "VALLEY / DEPARTURE"
- Midpoint landing: "MIDPOINT / REST"
- Center of hilltop station: "HILLTOP / ARRIVAL"
- Tower top: "MECHANICAL + OBSERVATION"
- Along inclined track: "INHABITED SLOPE"

## Success criteria
- The building clearly FOLLOWS A SLOPE — it is not a flat building with a tall part
- Valley and hilltop stations read as siblings (same footprint, different elevation)
- The inclined track is the dominant spatial element — the diagonal IS the architecture
- The tower marks the top from afar — visible landmark
- Someone sees: "this connects two levels of a hillside"
