# Lock Type 06 — GRADIENT DISPATCHER (Generic Concept)

## Rhino target
Instance: `lock_06` (port 9006)
All MCP tool calls must include `target: "lock_06"`

## Role
You are a modeler building a pure architectural concept — no site, no terrain, no context buildings. Origin at (0, 0, 0). This is a typological study.

## Concept: The Gradient Dispatcher

**What it is:** A building that sorts multiple flows across a slope. Not one path going up, but MANY paths branching to different levels. The architecture is a sorting machine — flows are identified and dispatched to the correct elevation before they enter the building.

**Spatial metaphor:** An elevator bank where you choose your floor BEFORE entering the car (Schindler PORT destination dispatch). A terraced hillside where each terrace serves a different function. A sky lobby that redistributes flows from one transport mode to many.

**State transition:** Horizontal flow (arriving) ↔ Gradient flow (dispatched to correct level)

**What makes it a GRADIENT dispatcher (not just a stepped building):**
- The LOBBY at the base does the sorting — intelligence is at entry, not distributed
- Multiple parallel levels step up a slope, each serving a different flow type
- Flows are separated by TYPE (staff, patients, cargo, emergency), not just elevation
- The vertical core connects all levels but is NOT the primary circulation — the dispatcher IS
- The gradient is expressed architecturally — the building steps uphill visibly

## Volumes to model

### Overall envelope: 24m (X) × 40m (Y, slope axis) × 18m (Z total rise)
Y-axis is the slope. Building steps up as Y increases.

### 1. Dispatcher Lobby — ground level, base of slope
- Position: X = [-12, 12], Y = [-5, 5], Z = [0, 5]
- 24m × 10m × 5m — widest volume, full width of building
- THE key space — where all flows arrive and get sorted
- South face (Y = -5): large opening, public entry, full width
- Interior: 4 dispatch lanes (each 5m wide, separated by 0.5m walls)
  - Lane 1 (X = [-12, -7]): staff circulation → routes to L1
  - Lane 2 (X = [-6, -1]): patient circulation → routes to L2
  - Lane 3 (X = [1, 6]): cargo circulation → routes to L3
  - Lane 4 (X = [7, 12]): emergency → routes directly up via core

### 2. Level 1 — Staff (first terrace)
- Position: X = [-12, 0], Y = [5, 15], Z = [4, 8]
- 12m × 10m × 4m — floor at Z = 4
- West half of the building only — steps up and narrows
- Connected to lobby via ramp from Lane 1

### 3. Level 2 — Patients (second terrace)
- Position: X = [-12, 0], Y = [15, 25], Z = [8, 12]
- 12m × 10m × 4m — floor at Z = 8
- Same width as L1, further up the slope
- Connected to lobby via ramp from Lane 2 (longer run)

### 4. Level 3 — Cargo (third terrace)
- Position: X = [-12, -4], Y = [25, 35], Z = [12, 16]
- 8m × 10m × 4m — narrower, highest working level
- Cargo handling — large openings for vehicle access on north face
- Connected to lobby via ramp from Lane 3

### 5. Vertical Core / Emergency Shaft
- Position: X = [8, 12], Y = [5, 9], Z = [0, 18]
- 4m × 4m × 18m — full height tower on east side
- Contains emergency stair + lift shaft
- Connected to all levels via landings
- Rises above the building — visible marker
- Open lattice at top (Z = 16–18) — mechanical/observation

### 6. Ramp System (connecting lobby to levels)
Each ramp is SIA 500 compliant (max 6% grade):
- **Ramp to L1:** from lobby (Z = 0) to L1 (Z = 4), run = 67m minimum
  - Switchback within X = [-12, -7], Y = [2, 15]
  - 3 runs of ~22m with landings
- **Ramp to L2:** from lobby (Z = 0) to L2 (Z = 8), run = 134m
  - Runs along east side, X = [1, 6], Y = [2, 25]
  - External switchback, 6 runs with landings
- **Ramp to L3:** from lobby (Z = 0) to L3 (Z = 12)
  - Service ramp (cargo, steeper grade allowed: 10% = 120m run)
  - Runs along west exterior, X = [-14, -12], Y = [5, 35]

For the concept model, represent each ramp as an inclined surface (simplified):
- Ramp to L1: single inclined plane, X = [-10, -7], Y = [3, 13], Z = [0.5, 4]
- Ramp to L2: single inclined plane, X = [1, 4], Y = [3, 23], Z = [0.5, 8]
- Ramp to L3: single inclined plane, X = [-13, -12], Y = [5, 33], Z = [0.5, 12]

### 7. Terrain Proxy (abstract slope)
- Tilted surface from (Y = -5, Z = -1) to (Y = 35, Z = 14)
- Shows the building follows a hillside
- Thin surface, wireframe

## Circulation
- **Staff path:** Lobby Lane 1 → Ramp → L1 (polyline, color-coded)
- **Patient path:** Lobby Lane 2 → Ramp → L2
- **Cargo path:** Lobby Lane 3 → Ramp → L3
- **Emergency path:** Lobby Lane 4 → Vertical Core → any level (vertical line)
- Model 4 polylines, each from lobby (Z = 0.5) to destination level
- Also model a single line from core base (X = 10, Y = 7, Z = 0) straight up to Z = 18

## Structure
- Lobby: 6 columns at X = [-7, -1, 5], Y = [±2], 0.35m × 0.35m
- Each terrace level: 4 perimeter columns
- Core: 4 corner columns, continuous full height, 0.35m × 0.35m
- Terrace edge beams: along Y = [5, 15, 25, 35] at respective Z levels
- Floor slabs: 0.3m thick at each level

## Openings
- Lobby south face: full width entry, Y = -5, X = [-10, 10], Z = [0.5, 4]
- L1 west window: X = -12, Y = [7, 13], Z = [5, 7.5]
- L2 west window: X = -12, Y = [17, 23], Z = [9, 11.5]
- L3 north cargo door: Y = 35, X = [-10, -6], Z = [12.5, 15.5]
- Core top: open on all faces, Z = [16, 18]

## Layers
- `Type_06_Gradient::Volumes` — color (151, 117, 250)
- `Type_06_Gradient::Circulation` — color (190, 170, 252)
- `Type_06_Gradient::Structure` — color (110, 85, 180)
- `Type_06_Gradient::Openings` — color (170, 145, 250)
- `Type_06_Gradient::Annotations` — color (210, 200, 252)
- `Type_06_Gradient::TerrainProxy` — color (120, 100, 160)

## Annotations (text dots)
- Lobby center: "DISPATCHER LOBBY / SORTING"
- Lane 1 start: "STAFF →"
- Lane 2 start: "PATIENTS →"
- Lane 3 start: "CARGO →"
- Lane 4 start: "EMERGENCY ↑"
- L1 center: "LEVEL 1 / STAFF"
- L2 center: "LEVEL 2 / PATIENTS"
- L3 center: "LEVEL 3 / CARGO"
- Core top: "EMERGENCY CORE"

## Success criteria
- Building clearly steps up a slope — 4 visible terraces (lobby + 3 levels)
- Lobby reads as a wide sorting space with multiple lanes
- Each level is a distinct platform at increasing elevation
- The vertical core is an independent tower element (emergency override)
- Ramps are visible as separate paths from lobby to each level
- Someone sees: "this sorts multiple flows to different elevations on a hillside"
