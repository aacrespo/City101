# Lock Type 05 — VISIBILITY LOCK (Generic Concept)

## Rhino target
Instance: `lock_05` (port 9005)
All MCP tool calls must include `target: "lock_05"`

## Role
You are a modeler building a pure architectural concept — no site, no terrain, no context buildings. Origin at (0, 0, 0). This is a typological study.

## Concept: The Visibility Lock

**What it is:** Infrastructure made legible. Unlike the Cargo Lock (which stacks public ABOVE logistics), the Visibility Lock wraps a viewing path AROUND a working core. The machine is in the center; you orbit it. The building is a lens that makes a system readable.

**Spatial metaphor:** An observatory — you look INTO a process from a surrounding ring. Airport control tower looking down at the apron. A panopticon inverted — the public watches the machine, not the other way around.

**State transition:** Opaque (hidden system) ↔ Transparent (legible system)

**Distinction from Cargo Lock (Type 02):**
- Cargo Lock = two parallel horizontal paths (above/below), linear flow
- Visibility Lock = central working core SURROUNDED by a viewing ring, orbital flow
- Cargo is about goods passing through; Visibility is about understanding a system

## Volumes to model

### Overall envelope: 30m (X) × 30m (Y) × 14m (Z)

### 1. Working Core — the machine
- Position: centered, circular or square, radius ~8m
- X = [-8, 8], Y = [-8, 8], Z = [0, 8]
- 16m × 16m × 8m — the opaque heart
- Mostly solid walls at ground level (the system operates privately)
- Upper portion (Z = 5–8) has slot windows — partial reveal from inside out
- This is where sorting, processing, coordination happens
- Interior not detailed — it's a black box made SELECTIVELY transparent

### 2. Viewing Ring — public orbit
- Wraps around the core at elevated level
- Z = [5, 9] — floor at 5m, ceiling at 9m (4m tall)
- Ring width: 4m, outer edge at ~12m from center
- Outer boundary: X = [-12, 12], Y = [-12, 12] (with corners chamfered or rounded)
- Continuous glass on inner face (looking INTO the core)
- Solid or perforated on outer face (filtered view OUT to context)
- The ring is the architectural event — the orbit around the machine

### 3. Access Ramp — the ascent
- Spirals or switchbacks from ground (Z = 0) to ring level (Z = 5)
- Position: southeast quadrant, X = [6, 14], Y = [-14, -2]
- 8m × 12m footprint
- Grade: max 6% (SIA 500 accessible ramp: 5m rise / 83m run, switchback with landings)
- 3 switchback runs:
  - Run 1: Y = [-14, -8], X = [6, 14], Z = [0, 1.7]
  - Landing: Y = [-8, -7], full width, Z = 1.7
  - Run 2: Y = [-7, -1], X = [6, 14], Z = [1.7, 3.4]
  - Landing: Y = [-1, 0], full width, Z = 3.4
  - Run 3: short connector to ring level, Z = [3.4, 5]
- The ramp is exposed — you see the core growing as you ascend

### 4. Exit Stair — quick descent
- Northwest quadrant: X = [-14, -10], Y = [8, 12]
- 4m × 4m footprint
- Stair from Z = 5 to Z = 0 (compact, not ceremonial)

### 5. Roof / Canopy over Core
- X = [-10, 10], Y = [-10, 10], Z = [10, 11]
- Overhangs the core, shelters the top of the viewing ring
- Flat or slightly pitched (single slope draining north)
- Supported by core walls + 4 outrigger columns at ring corners

## Circulation
- **Public path:** Ground entry (SE) → ramp up → ring orbit (360° or 270°) → exit stair (NW) → ground
- Model as polyline: spiral/switchback ramp + ring circuit + stair descent
- **Worker path:** Ground level direct entry into core (north face, Y = 8), Z = 0 — separate from public
- Mark "looking in" moments at 4 points around the ring (N, E, S, W)

## Structure
- Core walls: 0.3m thick, 4 faces
- Ring floor: supported by core walls (cantilever inward) + 8 outrigger columns at 3m beyond core
- Outrigger columns: 0.3m × 0.3m, at 45° intervals around ring (8 total)
- Ramp: supported by 2 columns per landing (6 columns total, 0.25m × 0.25m)
- Roof: 4 outrigger beams from core to ring edge

## Openings
- Core inner windows (visible from ring): 4 large glazed panels, one per face, X or Y = ±8, Z = [5.5, 7.5], 6m wide
- Ring outer windows: continuous slot, Z = [6, 8.5], all 4 outer faces
- Ring inner face: full glazing (looking into core), Z = [5.5, 8.5]
- Core ground entry (workers): Y = 8, X = [-2, 2], Z = [0, 3.5]
- Public ground entry (ramp start): X = 10, Y = -10, Z = [0, 3]

## Layers
- `Type_05_Visibility::Volumes` — color (77, 171, 247)
- `Type_05_Visibility::Circulation` — color (140, 200, 250)
- `Type_05_Visibility::Structure` — color (55, 120, 175)
- `Type_05_Visibility::Openings` — color (110, 185, 245)
- `Type_05_Visibility::Annotations` — color (180, 220, 250)

## Annotations (text dots)
- Center of core: "WORKING CORE / OPAQUE"
- Ring north: "VIEWING RING / ORBIT"
- Ring east: "LOOKING IN"
- Ramp base: "ASCENT / REVEAL"
- Core ground entry: "WORKER ACCESS"

## Success criteria
- Central mass clearly reads as a solid/opaque core
- Ring floats around it at a higher level — orbital, not linear
- Ramp ascent is legible as a journey of gradual revelation
- Inner face of ring is transparent (glass), outer face is more solid
- Someone sees: "this is about orbiting a system to understand it"
