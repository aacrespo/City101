# Lock Type 09 — BRIDGE LOCK (Generic Concept)

## Rhino target
Instance: `lock_09` (port 9009)
All MCP tool calls must include `target: "lock_09"`

## Role
You are a modeler building a pure architectural concept — no site, no terrain, no context buildings. Origin at (0, 0, 0). This is a typological study.

## Concept: The Bridge Lock

**What it is:** A horizontal span connecting two disconnected points. The building IS the infrastructure — not a building ON infrastructure, but a building that IS the connection. A skybridge at urban scale. Architecture as last-mile corrective.

**Spatial metaphor:** A covered bridge — like Bern's Marzili lift bridge, but 2km long and inhabited. A moving sidewalk enclosure. An airport jetway stretched to building scale. The building doesn't sit somewhere — it SPANS somewhere.

**State transition:** Connected node (station) ↔ Disconnected destination (hospital/campus)

**What makes it a BRIDGE lock:**
- EXTREMELY LINEAR — length dominates all other dimensions (10:1 ratio or more)
- Three zones: origin node + span + destination node
- The span NARROWS in the middle (structural and experiential — compression at midpoint)
- Bidirectional — traffic flows both ways simultaneously (lane divider)
- The bridge is elevated — it crosses OVER the terrain gap, not through it
- V-columns or pylons support the span — the structure IS the expression

## Volumes to model

### Overall envelope: 100m (X, span axis) × 12m (Y, cross-section at widest) × 9m (Z)

### 1. Origin Node — Station End (west)
- Position: X = [-50, -35], Y = [-6, 6], Z = [4, 9]
- 15m × 12m — widest section, entry hall
- Floor at Z = 4m (elevated — the bridge deck level)
- Roof at Z = 9m (5m internal height)
- West face (X = -50): large entry opening, Y = [-4, 4], Z = [4.5, 8]
- This is the "gathering" space — where people start the crossing
- 2 stair/ramp elements descend from deck (Z = 4) to ground (Z = 0):
  - North ramp: X = [-50, -44], Y = [6, 10], Z = [0, 4] (6m run, accessible)
  - South stair: X = [-50, -46], Y = [-10, -6], Z = [0, 4] (compact)

### 2. Bridge Span — the crossing
- Position: X = [-35, 35], Y = [-4, 4], Z = [4, 8.5]
- 70m × 8m × 4.5m — NARROWER than either end node
- Floor at Z = 4m (continuous deck)
- Roof at Z = 8.5m (4.5m internal height — slightly lower than nodes)
- The span narrows further at midpoint:
  - X = [-10, 10]: width reduces to Y = [-3, 3] (6m) — the compression point
  - Then widens again toward destination
- Side walls: lower portion solid (Z = 4–5.5, parapet), upper portion open (Z = 5.5–8, glazed or lattice)
- Every 10m: a bay frame (structural rhythm visible from outside)

### 3. Destination Node — Hospital/Campus End (east)
- Position: X = [35, 50], Y = [-6, 6], Z = [0, 9]
- 15m × 12m — same width as origin, but DESCENDS to ground level
- Floor ramps down from deck (Z = 4) to ground (Z = 0) over the 15m length
- The ramp IS the building — the floor slopes continuously
- East face (X = 50): ground-level exit, Y = [-4, 4], Z = [0.5, 4.5]
- Roof stays at Z = 9m — so interior height GROWS as floor descends (from 5m to 9m)
- This expanding height = arrival, release, decompression

### 4. V-Columns — bridge support structure
Along the span, every 14m:
- Positions: X = [-28, -14, 0, 14, 28]
- Each V-column pair: two legs spreading from a single base point at ground (Z = 0) to deck edges (Z = 4, Y = ±3.5)
  - Base: (X, 0, 0) — single point
  - Top left: (X, -3.5, 4)
  - Top right: (X, 3.5, 4)
- Column section: 0.25m × 0.25m (slender steel)
- 5 V-column pairs total — the structural rhythm of the bridge

### 5. Bay Frames — span rhythm
Every 10m along span: X = [-30, -20, -10, 0, 10, 20, 30]
- Each bay frame: two vertical posts (Y = ±4, Z = [4, 8.5]) + one horizontal beam (Y = [-4, 4], Z = 8.5)
- Post section: 0.2m × 0.15m
- Beam section: 0.3m × 0.15m
- 7 bay frames — visible from outside as the bridge's rhythm

### 6. Ground Plane
- Thin surface: X = [-55, 55], Y = [-15, 15], Z = [-0.1, 0]
- Shows that the bridge is ELEVATED above grade
- The gap between ground and deck (Z = 0 to Z = 4) is the void the bridge spans

## Circulation
- **Westbound lane:** Center line + north: from origin (X = -50, Y = 2, Z = 4.5) → span → destination (X = 50, Y = 2, Z = 0.5)
- **Eastbound lane:** Center line + south: reverse direction, Y = -2
- **Lane divider:** Continuous line at Y = 0, Z = 4.1, from X = -35 to X = 35 (0.1m tall strip)
- **Tactile strips:** Every 10m along span, perpendicular to direction: Y = [-3.5, 3.5], 0.2m wide, Z = 4.05
- Model both lanes as polylines. Mark midpoint compression (X = 0) with a cross or circle.

## Structure
- V-columns: 5 pairs (described above)
- Bay frames: 7 frames (described above)
- Origin node: 4 columns at corners (±6, ±6, Z = 0 to 9), 0.3m × 0.3m
- Destination node: 4 columns at corners, same
- Deck edge beams: 2 continuous beams, Y = ±4, Z = 4, from X = -50 to X = 50, section 0.2m × 0.3m
- Roof beam: continuous, Y = 0, Z = 8.5 (span) / 9 (nodes)

## Openings
- Origin west entry: X = -50, Y = [-4, 4], Z = [4.5, 8]
- Destination east exit: X = 50, Y = [-4, 4], Z = [0.5, 4.5]
- Span side openings: continuous glazing above parapet, both sides, Z = [5.5, 8]
- Bay window rhythm: each 10m bay has a 6m × 2.5m opening framed by the bay posts
- Midpoint compression: narrowest windows (Y = ±3, Z = [5.5, 7.5]) — the tightest point

## Layers
- `Type_09_Bridge::Volumes` — color (32, 201, 151)
- `Type_09_Bridge::Circulation` — color (100, 220, 185)
- `Type_09_Bridge::Structure` — color (22, 142, 107)
- `Type_09_Bridge::Openings` — color (70, 210, 170)
- `Type_09_Bridge::Annotations` — color (160, 230, 205)

## Annotations (text dots)
- Origin node center: "ORIGIN / STATION"
- Span midpoint: "COMPRESSION / MIDSPAN"
- Destination node center: "DESTINATION / CAMPUS"
- Under span (ground level): "THE GAP"
- V-column base: "V-SUPPORT"

## Key design principle
The bridge IS the building. Not a building with a bridge, but a bridge that IS architecture. The 10:1 length-to-width ratio is extreme and intentional. The midpoint compression creates a visceral experience of crossing — you feel the narrowing. The destination ramp that descends means the interior volume EXPANDS as you arrive — decompression.

## Success criteria
- Extreme linearity — immediately reads as a BRIDGE, not a building
- Clear three-part rhythm: wide (origin) → narrow (span) → wide (destination)
- Midpoint compression is visible (the span visibly pinches at X = 0)
- V-columns are the dominant structural expression (5 pairs visible beneath deck)
- Bay frames create rhythm along the span
- Destination ramp descending to ground is legible (floor slopes down, ceiling stays)
- Someone sees: "this is a bridge connecting two disconnected places"
