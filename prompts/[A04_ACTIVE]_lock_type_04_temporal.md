# Lock Type 04 — TEMPORAL LOCK (Generic Concept)

## Rhino target
Instance: `lock_04` (port 9004)
All MCP tool calls must include `target: "lock_04"`

## Role
You are a modeler building a pure architectural concept — no site, no terrain, no context buildings. Origin at (0, 0, 0). This is a typological study.

## Concept: The Temporal Lock

**What it is:** A chamber that holds people during a time gap. The occupant is stationary — the CITY transitions around them. You enter in one temporal state (last service, night) and exit in another (first service, dawn). The dwell time IS the architecture.

**Spatial metaphor:** A canal lock — the vessel (person) enters, gates close, water level (time) changes, gates open on the other side. Also: the capsule hotel (Nine Hours Tokyo), where architecture is designed precisely for waiting. The airlock where pressure equalizes.

**State transition:** Night (01:30, last service) ↔ Dawn (05:00, first service)

**What makes it a TEMPORAL lock:**
- TWO CHAMBERS sharing ONE GATE — not a single room, but a sequence
- Night side is for rest, retreat, shelter (introverted)
- Dawn side is for preparation, re-entry, activation (extroverted)
- The Gate between them is the temporal threshold — architecturally the tallest, narrowest element
- Linear sequence: enter night → pass gate → exit dawn. No shortcuts.
- The 5-stage canal lock sequence: entry → sealing → equalization → level-matching → exit

## Volumes to model

### Overall envelope: 36m (X) × 12m (Y) × 9m (Z)

### 1. Night Chamber — rest/shelter
- Position: X = [-18, -3], Y = [-6, 6], Z = [0, 6]
- 15m × 12m × 6m
- Enclosed, introverted — few openings, protective
- West face: entry door, modest (Y = [-1.5, 1.5], Z = [0, 3.5])
- North face: 3 small high windows (Z = 3.5–5.5, each 1.5m wide, spaced 4m)
- Interior logic: rest capsules, soft lighting, horizontal surfaces
- Ceiling relatively low — intimate, compressive

### 2. Gate — the temporal threshold
- Position: X = [-3, 3], Y = [-4, 4], Z = [0, 9]
- 6m × 8m × 9m — TALLEST volume, narrower than both chambers
- Double height void — marks the passage of time
- Thin in X (6m) but tall — a vertical slot between two worlds
- Canopy overhang extends 1.5m on both sides (X = [-4.5, 4.5] at Z = 8)
- Opening on both sides (night face and dawn face) — but not simultaneously visible (offset or angled)

### 3. Dawn Chamber — preparation/re-entry
- Position: X = [3, 18], Y = [-6, 6], Z = [0, 7]
- 15m × 12m × 7m — slightly taller than Night (you're waking up, expanding)
- Extroverted — larger openings, more light
- East face: large window/opening (Y = [-3, 3], Z = [1, 6]) — morning light
- South face: 3 wider windows (Z = [0.8, 5.5], each 2.4m wide)
- Interior logic: showers, food, preparation for departure
- Ceiling higher — expansive, activating

### 4. Ground Plane
- A thin slab: X = [-20, 20], Y = [-8, 8], Z = [-0.15, 0]
- Extends slightly beyond building footprint — situates it on ground
- Subtle level change: Night side at Z = 0, Dawn side at Z = 0.3 (30cm step up — you've been "raised" by the passage of time)

## Circulation
- **Primary sequence:** West entry → Night Chamber (rest) → Gate (threshold crossing) → Dawn Chamber (preparation) → East exit
- Model as polyline: (-18, 0, 0.5) → (-3, 0, 0.5) → (0, 0, 0.5) → (3, 0, 0.5) → (18, 0, 0.5)
- **Internal Night stair:** Ramp or stair from Z = 0 to Z = 3 within Night Chamber, for mezzanine sleeping level
  - X = [-15, -12], Y = [-3, 3], Z = [0, 3], 10 treads
- **Internal Dawn stair:** Similar, Z = 0.3 to Z = 3.3 within Dawn Chamber
  - X = [12, 15], Y = [-3, 3], Z = [0.3, 3.3]

## Structure
- Gate: 4 columns at (±3, ±4), 0.3m × 0.3m, full height to 9m
- Gate canopy beam: X = [-4.5, 4.5], Y = 0, Z = 8, section 0.3m × 0.3m
- Night Chamber: 2 interior columns at X = -10, Y = ±3
- Dawn Chamber: 2 interior columns at X = 10, Y = ±3
- Wall thickness: 0.3m throughout

## Layers
- `Type_04_Temporal::Volumes` — color (105, 219, 124)
- `Type_04_Temporal::Circulation` — color (160, 235, 175)
- `Type_04_Temporal::Structure` — color (75, 155, 90)
- `Type_04_Temporal::Openings` — color (130, 225, 150)
- `Type_04_Temporal::Annotations` — color (200, 245, 210)

## Annotations (text dots)
- Center of Night Chamber: "NIGHT / REST / 01:30"
- Center of Gate: "THRESHOLD / TIME PASSES"
- Center of Dawn Chamber: "DAWN / PREPARATION / 05:00"
- West entry: "ENTRY (LAST SERVICE)"
- East exit: "EXIT (FIRST SERVICE)"

## Key design principle
The Night side and Dawn side must feel DIFFERENT — not mirror images. Night is compressed, dark, protective. Dawn is open, bright, activating. The Gate is the hinge between them — tallest, thinnest, most monumental.

## Success criteria
- Three-part reading: night — gate — dawn
- Gate is clearly the tallest element (9m vs 6-7m chambers)
- Night Chamber feels enclosed (fewer, smaller openings)
- Dawn Chamber feels open (larger openings, taller ceiling)
- The Z = 0.3m level change on the dawn side is subtle but present
- Someone sees: "this is about waiting through a time gap — you enter at night and exit at dawn"
