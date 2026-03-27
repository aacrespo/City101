# Lock Type 02 — CARGO LOCK (Generic Concept)

## Rhino target
Instance: `lock_02` (port 9002)
All MCP tool calls must include `target: "lock_02"`

## Role
You are a modeler building a pure architectural concept — no site, no terrain, no context buildings. Origin at (0, 0, 0). This is a typological study.

## Concept: The Cargo Lock

**What it is:** A building where invisible logistics become visible civic space. The supply chain — trucks, pallets, cold chains, sorting machines — is normally hidden behind walls. This lock turns the service corridor inside out. The public walks THROUGH the machine.

**Spatial metaphor:** Think factory tour elevated to architecture. The airport baggage hall if it had a glass floor and a public promenade above it. A service elevator with the shaft exposed.

**State transition:** Invisible (logistics) ↔ Visible (civic observation)

**What makes it a CARGO lock:**
- Two parallel worlds stacked vertically — workers below, public above
- The floor between them is the architectural event (glass, grating, slots)
- Goods flow horizontally through the lower level (truck bay → sorting → dispatch)
- People flow horizontally through the upper level (entry → observation → exit)
- The two paths never physically cross but constantly share visual space

## Volumes to model

### Overall envelope: 48m (X) × 22m (Y) × 11m (Z)

### 1. Logistics Hall — ground level
- Position: X = [-24, 24], Y = [-11, 11], Z = [0, 5]
- 48m × 22m × 5m — generous ceiling for truck access
- West face: truck bay entry (large opening, 6m × 4.5m, ground level)
- East face: dispatch exit (matching opening)
- Interior: 3 sorting bays (each 14m × 8m) separated by 1m walls at X = -8, +8
- Central sorting spine runs along Y = 0, full length

### 2. Observation Corridor — upper level
- Position: X = [-20, 20], Y = [-4, 4], Z = [6, 10]
- 40m × 8m × 4m — narrower than logistics below, floats above it
- Set back from edges (cantilevers over logistics at center)
- Floor at Z = 6m — the reveal moment (looking down into sorting)
- South face: continuous window wall (full glazing Y = -4)
- North face: solid wall with slot windows at intervals

### 3. Public Entry Stair — west
- Position: X = [-24, -20], Y = [-4, 4], Z = [0, 6]
- Stair/ramp from ground (Z = 0) to observation level (Z = 6)
- 4m × 8m footprint
- The ascent IS the transition from "street" to "observation"

### 4. Public Exit Stair — east
- Position: X = [20, 24], Y = [-4, 4], Z = [0, 6]
- Mirror of entry stair, descent back to ground
- Slightly different geometry (asymmetric — exit experience differs from entry)

### 5. Loading Dock Canopy
- Position: X = [-28, -24], Y = [-8, 8], Z = [3, 5.5]
- 4m × 16m canopy extending west — truck weather protection
- Supported by 4 columns at corners
- Marks the boundary between exterior logistics and interior sorting

## Circulation
- **Logistics path (workers):** West truck bay → sorting bay 1 → bay 2 → bay 3 → east dispatch (Z = 0.5m, Y = 0)
- **Public path (observers):** Ground west → stair up → observation corridor → stair down → ground east (Z = 6.5m in corridor)
- **Vertical visual connection:** Dashed/dotted lines at X = -8, 0, +8 marking "looking down" points where public sees logistics
- Model all as polylines on Circulation layer

## Structure
- 6 main columns: X = [-16, 0, 16], Y = [±8], 0.4m × 0.4m, full height (0–10m)
- Observation corridor beams: 2 longitudinal beams at Y = ±4, Z = 6, spanning X = [-20, 20]
- Cantilever brackets at each column supporting corridor overhang
- Loading dock: 4 columns at X = [-28, -24], Y = [±8], height 5.5m

## Openings
- West truck bay: X = -24, Y = [-3, 3], Z = [0, 4.5]
- East dispatch: X = 24, Y = [-3, 3], Z = [0, 4.5]
- Observation south wall: full glazing Y = -4, X = [-20, 20], Z = [6.5, 9.5]
- Observation north slots: 5 windows, each 2m wide, spaced 6m apart, Y = 4, Z = [7, 9]
- Viewing slots in observation floor (Z = 6): 3 rectangles at X = [-8, 0, 8], Y = [-2, 2], 4m × 4m each (glass floor zones)

## Layers
- `Type_02_Cargo::Volumes` — color (255, 169, 77)
- `Type_02_Cargo::Circulation` — color (255, 200, 140)
- `Type_02_Cargo::Structure` — color (180, 120, 55)
- `Type_02_Cargo::Openings` — color (255, 185, 110)
- `Type_02_Cargo::Annotations` — color (255, 220, 180)

## Annotations (text dots)
- Center of logistics hall: "LOGISTICS / SORTING"
- Center of observation corridor: "PUBLIC OBSERVATION"
- Each viewing slot: "VISUAL CONNECTION"
- Loading dock: "TRUCK BAY / ENTRY"
- East dispatch: "DISPATCH / EXIT"

## Success criteria
- Clear two-level reading — heavy logistics below, light observation above
- The observation corridor visibly floats over the logistics hall
- Floor openings (viewing slots) are legible as the key architectural moment
- Goods flow and people flow are clearly parallel but separate
- Someone sees: "this is about revealing hidden infrastructure to the public"
