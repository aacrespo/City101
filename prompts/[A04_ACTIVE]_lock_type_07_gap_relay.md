# Lock Type 07 — GAP RELAY (Generic Concept)

## Rhino target
Instance: `lock_07` (port 9007)
All MCP tool calls must include `target: "lock_07"`

## Role
You are a modeler building a pure architectural concept — no site, no terrain, no context buildings. Origin at (0, 0, 0). This is a typological study.

## Concept: The Gap Relay

**What it is:** An intermediate waypoint that sustains a chain. NOT a destination, NOT an origin — a PASSING POINT. The minimum architecture needed to keep a network alive across a gap too long to cross in one jump. It stores just enough, holds just long enough, and passes flows onward.

**Spatial metaphor:** A Panama Canal water-saving basin — an intermediate chamber that stores water level while allowing continuous flow. A caravanserai — a rest stop spaced at one day's travel (~11km). A pit stop — fast in, fast out, critical servicing.

**State transition:** Gap (broken chain) ↔ Continuity (chain sustained)

**What makes it a GAP RELAY (not a full station):**
- MINIMAL footprint — the smallest of all 9 lock types
- MAXIMUM connectivity — arms reaching in multiple directions
- Through-flow dominates — people/goods PASS THROUGH, not STAY
- Dwell time is SHORT (minutes, not hours like Temporal Lock)
- The building is a HUB or JUNCTION, not a chamber
- It branches: flows arrive from one direction, split to 2-3 departure directions

## Volumes to model

### Overall envelope: 24m (X) × 24m (Y) × 7m (Z)

### 1. Central Hub — the relay core
- Position: X = [-5, 5], Y = [-5, 5], Z = [0, 7]
- 10m × 10m × 7m — compact, double-height
- Hexagonal or octagonal plan (chamfer the corners of the square at 45°)
- This is where all arms converge — coordination, brief rest, redirection
- Open interior — single volume, no partitions
- Roof has skylight or open oculus (Z = 6–7, 4m × 4m opening)

### 2. Arm A — Rail Direction (south, primary corridor)
- Position: X = [-3, 3], Y = [-18, -5], Z = [0, 4]
- 6m × 13m × 4m — elongated, lower ceiling than hub
- South face: open (connection to rail/primary transport)
- The main flow direction — most traffic passes through this arm

### 3. Arm B — Lateral Direction (west, secondary connection)
- Position: X = [-18, -5], Y = [-3, 3], Z = [0, 4]
- 13m × 6m × 4m — perpendicular to Arm A
- West face: open (connection to lateral transport — bus, boat, funicular)
- Lower volume than rail arm

### 4. Arm C — Uphill Direction (northeast, tertiary connection)
- Position: X = [5, 16], Y = [5, 16], Z = [0, 5]
- 11m × 11m × 5m — angled at 45°, reaching toward higher ground
- Northeast face: open (connection to hillside — funicular, path)
- Slightly taller than other arms (ascends)
- Floor ramps up from Z = 0 at hub to Z = 1.5 at far end (gentle slope)

### 5. Canopy Extensions — lightweight shelters at arm tips
- 3 canopies, one at each arm terminus:
  - Arm A tip: X = [-4, 4], Y = [-20, -18], Z = [3, 4.5] (8m × 2m)
  - Arm B tip: X = [-20, -18], Y = [-4, 4], Z = [3, 4.5] (2m × 8m)
  - Arm C tip: X = [14, 18], Y = [14, 18], Z = [4, 5.5] (4m × 4m)
- Steel frame, open sides — weathering protection at transitions

## Circulation
- **Primary through-flow:** Arm A south entry → Hub → Arm A north (or reverse). Straight line Y-axis.
- **Transfer flow A→B:** Arm A → Hub → turn 90° → Arm B. L-shaped path.
- **Transfer flow A→C:** Arm A → Hub → turn 45° → Arm C. Diagonal path.
- **Transfer flow B→C:** Arm B → Hub → turn 135° → Arm C.
- Model all 4 paths as polylines converging at hub center (0, 0, 1.0)
- Mark hub center with a circle (radius 2m) at Z = 0.1 — the "turntable"

## Structure
- Hub: 8 columns at octagon vertices (or 4 at square corners + 4 at chamfer points)
  - Radius ~5m from center, 0.3m × 0.3m, full height to 7m
- Arms: 2 columns per arm at midpoint (lightweight, 0.25m × 0.25m)
- Canopies: 4 thin steel columns each (0.15m × 0.15m)
- Hub roof beams: star pattern — beams from center to each column (8 beams)
- Skylight frame: 4m × 4m steel frame at Z = 6.5

## Openings
- Hub: open on all faces where arms connect (3 large openings, each 6m wide, full height)
- Hub face without arm (southeast): solid wall with single window, X = [3, 5], Y = [-5, -3], Z = [2, 5]
- Arm A south: fully open end, X = [-3, 3], Z = [0, 3.5]
- Arm B west: fully open end, Y = [-3, 3], Z = [0, 3.5]
- Arm C northeast: fully open end, diagonal face, Z = [0, 4]
- Skylight: 4m × 4m opening in hub roof

## Layers
- `Type_07_GapRelay::Volumes` — color (240, 101, 149)
- `Type_07_GapRelay::Circulation` — color (245, 170, 190)
- `Type_07_GapRelay::Structure` — color (170, 72, 105)
- `Type_07_GapRelay::Openings` — color (242, 140, 170)
- `Type_07_GapRelay::Annotations` — color (248, 200, 215)

## Annotations (text dots)
- Hub center: "RELAY HUB / JUNCTION"
- Arm A: "RAIL CORRIDOR →"
- Arm B: "LATERAL CONNECTION →"
- Arm C: "UPHILL / FUNICULAR →"
- Skylight: "OPEN TO SKY"

## Key design principle
This is the SMALLEST and most OPEN of all 9 types. It should feel like a junction, not a building. Arms reach out, the center is porous, dwell time is minimal. The architecture is about CONNECTIVITY, not enclosure.

## Success criteria
- Compact hub with 3+ arms radiating outward — reads as a junction
- Hub is taller than arms — marks the convergence point
- Arms clearly point in different directions (not symmetric)
- Open, porous — more openings than walls
- Skylight/oculus signals "brief stop, keep moving"
- Someone sees: "this is a transfer point where paths cross and flows get redirected"
