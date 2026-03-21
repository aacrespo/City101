# Workflow: Agent Team Architectural Modeling

Build architecture models with coordinated agent teams in Rhino via MCP.
Synthesized from the Lock 05 CHUV roundtable — 7 agents, 709 objects, 4 build rounds.

## When to use
- LOG 300+ models with multiple building systems (structure, envelope, MEP, circulation)
- Locks or prototypology sites where systems must coordinate dimensionally
- Any model where > 3 agents would work on the same geometry file

## Phase 0: Spec Preparation (lead, before team)

### Site Data Card
```
SITE CONDITIONS:
- Location: [city, campus, terrain feature]
- Elevation: [finish floor = X.Xm ASL]
- Rainfall: [mm/yr]
- Frost depth: [mm]
- Slope: [%] [direction]
- Orientation: [which face is primary]
```

### Level 0 Definition (MANDATORY — blocks everything)
- **Origin point**: SITE_ORIGIN = (x, y, z)
- **Finish floor elevation**: z = 0.00 relative
- **Structural grid**: column line positions (X and Y), with named lines if complex
- **Level datums**: z-heights for every floor, including slab thickness

### Bill of Objects
Every physical element listed with owner and status:

| Element | Owner agent | Status | Notes |
|---------|------------|--------|-------|
| Ground slab | structure | CREATE | |
| L0 columns | structure | CREATE | 5m grid |
| L0 walls | shell | CREATE | 0.3m thick |
| L0 glazing | windows | CREATE | after shell |
| ... | ... | ... | ... |

Status values: `CREATE`, `EXISTS (verify)`, `DEFER TO [agent]`
No ambiguous language ("keep", "carry forward"). If it must exist, someone owns it.

### Interface Registry
Where two agents' geometry meets:

| Interface | Owner | Reference agent | Rule |
|-----------|-------|----------------|------|
| Wall base → slab edge | shell | structure | Flush interior face, shell builds to slab edge |
| Parapet → wall top | roof | shell | Same plane, roof starts at shell's top Z |
| Window → wall opening | windows | shell | Glass at wall_face - 0.08m recess |
| Footing → column | ground | structure | Centered on column, 3× column width |
| Railing → wall | circulation | shell | Wall-mounted at wall inner face |

### Code Compliance Reference
Hard minimums — any deviation needs `[CODE OVERRIDE: reason]`:

| Element | Minimum | Standard |
|---------|---------|----------|
| Parapet / guardrail height | 1070mm | SIA 358 |
| Handrail diameter | 40-45mm round | SIA 500 |
| Ramp gradient (accessible) | max 6% | SIA 500 |
| Landing turning radius | 1500mm | SIA 500 |
| Handrail extensions | 300mm beyond ramp | SIA 500 |
| Railings required | both sides, all edges > 1000mm drop | SIA 358 |
| Safety glass markings | bands at 1.0m + 1.5m on full-height glazing | Swiss building code |
| Floor-to-floor clearance | 2700mm habitable | SIA 180 |

### Thicknesses & Dimensions
```
WALL_T = 0.3       FRAME_D = 0.15     SLAB_T = 0.3
COL_W = 0.4        BEAM_W = 0.3       PARAPET_H = 1.07
FOUND_DEPTH = 0.4  FOUND_W = 0.5
MULLION_W = 0.05   GLASS_T = 0.02     GLASS_RECESS = 0.08
RAIL_DIA = 0.044   RAIL_H = 1.1       KICK_H = 0.10
```

### Layer Tree (pre-built before agents start)
```
Lock_[ID]::
  Structure::Columns
  Structure::Beams
  Structure::Slabs
  Shell::Walls::[Level]
  Shell::Facade
  Windows
  Circulation
  Elevator
  Roof
  Ground::Foundation
  Ground::Site
  Terrain
```
Agents place objects on existing layers. Never create ad-hoc layers.

## Phase 1: Rough-In (sequential start, then parallel)

### Step 1 — Structure agent (STARTS FIRST)
Builds: column grid, primary beams, floor slabs, core walls.
Publishes: `coordination_geometry` — column positions, slab edges, beam depths.
**This is the contract. All other agents build to it.**

### Step 2 — Envelope agents (parallel, after structure publishes grid)
- **Shell**: walls split at openings, facade frames. References structure grid.
- **Roof**: parapets, canopies, copings. References wall tops from shell.
- **Ground**: foundations, footings at structure's column positions, terrain.

### Step 3 — Coordination freeze
Lead verifies: walls align with slabs, columns don't intersect walls, roof meets wall tops. No geometry changes after freeze without change propagation.

## Phase 2: Detail (parallel, after freeze)

All detail agents start simultaneously, building against frozen Phase 1 geometry:
- **Windows**: mullion grids, glass, perimeter frames, door systems
- **Circulation**: ramps/stairs, railings (both sides), landings, anti-slip
- **Elevator**: shaft, cab, guide rails, landing doors, machine room
- **MEP** (if applicable): ducts, risers, equipment

### Concept system rule
Concept systems (elevator, MEP) must receive **interface inputs** before building:
- Landing approach directions (from circulation)
- Shaft opening dimensions (from structure)
- Floor elevations (from structure)

Don't let concept agents guess — route the queries explicitly.

## Phase 3: Review (3 gates)

### Gate 1 — Self-review (each agent, mandatory before "done")
Each agent audits their own layer:
- Object count matches expectations
- All objects on correct layer with systematic names
- Z heights match spec datums
- No zero-thickness or overlapping geometry
- Code compliance checklist passed (circulation: railing coverage map)

### Gate 2 — Bilateral review (parallel, between dependent agents)
Focused checks between agents sharing a boundary:
- Structure ↔ Shell: walls on slabs? columns clear of walls?
- Shell ↔ Windows: frames align to wall faces? openings match?
- Shell ↔ Roof: parapet-wall continuity?
- Structure ↔ Ground: footings under every column?
- Circulation ↔ Shell: railings clear of walls? ramp openings framed?

### Gate 3 — Full model review (lead)
- Viewport capture from 4 cardinals + aerial
- Object count per layer
- Void/core zones clear
- Visual coherence check

## Phase 4: Free Improvement (optional, parallel)

Prompt for agents:
> "Your system is built. Add ONE element that either: (a) completes a functional gap (something missing in a real building), or (b) resolves an interface problem with an adjacent system. State what you're adding and why it matters for the building's function — not for visual completeness."

Emphasis on function over appearance. No structural changes. One improvement per agent.

## Agent Prompt Template

Each agent receives:
1. **Role**: what systems they own, what layers they write to
2. **Shared spec**: site data card, level 0 definition, thicknesses
3. **Coordination geometry**: structure grid (column positions, slab edges) — after Phase 1
4. **Interface rules**: how their geometry meets adjacent systems
5. **Code checklist**: relevant standards for their system
6. **Helper functions**: `box()`, `named_box()`, `box_pts()` with SITE_ORIGIN offset
7. **Task assignment**: specific objects to build, with names and coordinates

## Geometry Type Guide

| Element | Geometry method | Why |
|---------|----------------|-----|
| Walls, slabs, beams, columns | BOX (rs.AddBox) | Predictable, fast, clean booleans |
| Handrails, grab bars | PIPE (rs.AddPipe) | Must read as round for grip |
| Anti-slip strips, trim | Thin BOX | Too small for pipe, reads as surface |
| Ramps | WEDGE (box_pts with 8 explicit corners) | Sloped surfaces need explicit Z control |
| Glass panes | Thin BOX | Planar, uniform thickness |
| Mullions | BOX | Rectangular profile standard for aluminum |
| Terrain | WEDGE or SURFACE | Follows natural grade |
| Copings, flashings | Thin BOX with overhang | Detail at LOG 400 |

## Naming Convention

```
{Element}_{Level}_{Location}_{SubElement}
```

Examples:
- `Wall_L0_North_WestPier`
- `Col_L1_-5_13`
- `Glass_L2_NWest_pane_TL`
- `Beam_L1_Transfer_Entrance`
- `Post_L0L1_Inner_3`

Principles:
- Sortable (level first after element type)
- Parseable (underscores, no spaces)
- Traceable (maps to spec opening/element ID)

## History
| Date | Change | Result |
|------|--------|--------|
| 2026-03-19 | Created from Lock 05 CHUV roundtable | 7 agents, 709 objects, 4 rounds |
