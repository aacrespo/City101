# Lock Type 01 — BORDER LOCK (Generic Concept)

## Rhino target
Instance: `lock_01` (port 9001)
All MCP tool calls must include `target: "lock_01"`

## Role
You are a modeler building a pure architectural concept — no site, no terrain, no context buildings. Origin at (0, 0, 0). This is a typological study.

## Concept: The Border Lock

**What it is:** A threshold between two incompatible systems. Two worlds that operate under different rules (legal, economic, temporal) meet at a controlled passage. The architecture mediates crossing.

**Spatial metaphor:** Think passport control — but as architecture, not furniture. The genkan (Japanese entrance) where you transition from outside to inside. An airlock where pressure equalizes before you can pass.

**State transition:** System A ↔ Control Zone ↔ System B

**What makes it a BORDER lock (not just a door):**
- The two sides are NOT equivalent — asymmetric volumes
- The control zone is architecturally prominent (not just a desk)
- There is a possible REJECTION path (you might not pass through)
- Dwell time in the middle is the architecture — equalization happens there

## Volumes to model

### Overall envelope: 32m (X) × 14m (Y) × 7m (Z)

### 1. Entry Hall — "System A" side
- Position: X = [-16, -4], Y = [-7, 7], Z = [0, 5]
- 12m × 14m × 5m
- Open, generous — arrival space, queuing, waiting
- One large opening on the west face (entry from System A)
- Ceiling lower than the gate — creates compression before threshold

### 2. Gate / Control Zone — the threshold
- Position: X = [-4, 4], Y = [-4, 4], Z = [0, 7]
- 8m × 8m × 7m — TALLEST volume, marks the threshold
- Narrow relative to the halls on either side
- Double-height void — monumental despite small footprint
- Two narrow passages through (one forward, one rejection/return)
- Overhead bridge or canopy element connecting the two halls at +5m

### 3. Exit Hall — "System B" side
- Position: X = [4, 16], Y = [-7, 7], Z = [0, 6]
- 12m × 14m × 6m
- Slightly taller than Entry (you've been "elevated" by passing through)
- Opening on east face (exit to System B)
- More structured interior — you've been processed, now dispatched

### 4. Rejection Loop
- A curved corridor or ramp from the Gate back to the Entry Hall
- Runs along the south face: Y = [-7, -5], X = [-4, 4], Z = [0, 3]
- Returns rejected flow to System A without crossing into System B

## Circulation
- **Primary path:** West entry → Entry Hall → Gate → Exit Hall → East exit (linear, one-directional)
- **Rejection path:** Gate → south corridor → back to Entry Hall (loop)
- Model both as polyline curves on the Circulation layer, at Z = 1.0m (walking height)
- Mark the threshold moment (center of Gate at X = 0) with a vertical line Z = [0, 7]

## Structure
- 4 columns at Gate corners: (±4, ±4), 0.35m × 0.35m, full height
- Overhead bridge beam: Y = 0, X = [-4, 4], Z = 5.0, section 0.4m × 0.3m
- Entry Hall: 2 columns at X = -10, Y = ±3.5
- Exit Hall: 2 columns at X = 10, Y = ±3.5

## Openings
- West face entry: X = -16, Y = [-3, 3], Z = [0, 4] (generous 6m wide)
- East face exit: X = 16, Y = [-2, 2], Z = [0, 4.5] (narrower 4m, taller)
- Gate north window: Y = 4, X = [-2, 2], Z = [3, 6] (high slot, light from above)
- Gate south window: Y = -4, X = [-2, 2], Z = [3, 6] (matching)

## Layers
- `Type_01_Border::Volumes` — color (255, 107, 107)
- `Type_01_Border::Circulation` — color (255, 180, 180)
- `Type_01_Border::Structure` — color (180, 80, 80)
- `Type_01_Border::Openings` — color (255, 140, 140)
- `Type_01_Border::Annotations` — color (255, 220, 220)

## Annotations (text dots)
Place text dots at:
- Center of Entry Hall: "SYSTEM A / ARRIVAL"
- Center of Gate: "THRESHOLD / EQUALIZATION"
- Center of Exit Hall: "SYSTEM B / DISPATCH"
- Rejection corridor: "REJECTION LOOP"

## Success criteria
- Three distinct volumes with clear hierarchy (gate tallest)
- Visible asymmetry between entry and exit
- The rejection loop is legible as a separate path
- Someone unfamiliar with the project can see: "this is about controlled passage between two different states"
