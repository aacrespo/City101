# Master Plan — Rennaz Lock 07: Construction-Ready Bridge Lock

**Project ID**: `rennaz-lock07`
**Owner**: Andrea
**Created**: 2026-03-27
**Target**: LOG 400 / LOI 400 / LOD 400 — first lock with full archibase knowledge
**Material system**: Timber (glulam GL24h structure, CLT slabs, timber platform frame walls)

---

## Why this lock

Rennaz is the most acute transit desert on the corridor. HRC hospital (1,965 employees, 200-300 night staff) has a 5h 52m dead window with zero public transit, no rail station, no shuttle, and a 2.1km hostile highway walk to Villeneuve station. The bridge lock connects rail to hospital — a literal bridge across the infrastructure gap.

## What's different from v0-v3

| Aspect | v0-v3 (before archibase) | This build (with archibase) |
|--------|--------------------------|----------------------------|
| LOG | 200-300 (massing/defined) | 400 (full assembly detail) |
| LOD | 200 (direction set) | 400 (build from this) |
| Walls | Single solid box | 7-layer timber frame assembly (276mm) |
| Deck | 250mm slab | CLT + waterproofing + decking (217mm) |
| Roof | 150-200mm slab | Flat warm deck timber (336mm) |
| Ramp | 26.7% grade (violates SIA 500) | 6% switchback + elevator (SIA 500 compliant) |
| Columns | 250mm generic | GL24h 200×200mm with steel shoes on pad footings |
| Openings | Void boxes | Frame + reveals + sill + lintel + glazing pane |
| Metadata | None | Every object tagged: material, thickness_mm, SIA ref |
| Foundation | None | Concrete pad footings, 800mm depth, steel shoes |
| Knowledge | None (agent guessing) | Every assembly from Deplazes/Vittone/SIA via archibase |

---

## Phases

### Phase 0: Spec Preparation — DONE IN THIS SESSION
- Lock all design decisions
- Query archibase for every assembly
- Write bill of objects, interface registry, code compliance
- Write overnight execution prompt
- **Deliverable**: Self-contained prompt file at `state/pm/rennaz-lock07/prompts/phase1_overnight_build.md`

### Phase 1-4: Overnight Build (autonomous, ~6-8 hours)
Runs as a single session with internal phase gates:

| Internal Phase | Agents | Duration | What |
|---------------|--------|----------|------|
| 1: Site + Rough-In | Site, Structure | ~1.5hr | Terrain, foundations, column grid, primary beams, slabs |
| 2: Envelope + Detail | Envelope, Circulation | ~2.5hr | Walls (7 layers), openings, ramp, stairs, railings |
| 3: Review | All + Lead | ~1hr | Mode A constraints + Mode B visual + Mode C load path |
| 4: Output | Lead | ~0.5hr | Spec sheet, baked script, viewport captures |

**Health-check pings** between each internal phase. If geometry count < 50% expected, agent retries before proceeding.

---

## Team Topology

**Type**: Hierarchical (lead resolves all — no human available overnight)
**Context**: Narrow (each agent sees only their domain + shared spec)
**Execution**: Sequential start (site → structure → parallel envelope/circulation)

| Agent | Role | Layers | Objects (est.) |
|-------|------|--------|---------------|
| **Lead** | Coordinator | — (doesn't build) | — |
| **Site** | Terrain + context | Lock_07::Terrain, Lock_07::Ground::Site | ~20 |
| **Structure** | Foundations + columns + beams + slabs | Lock_07::Structure::*, Lock_07::Ground::Foundation | ~80 |
| **Envelope** | Walls + windows + doors + roof + cladding | Lock_07::Shell::*, Lock_07::Windows, Lock_07::Roof | ~200 |
| **Circulation** | Bridge deck + ramp + stairs + elevator + railings | Lock_07::Circulation, Lock_07::Elevator | ~150 |

**Total estimated objects: ~450**

---

## Design Decisions (locked)

### Site
- **SITE_ORIGIN**: (200, 300, 374.0) — local coords, offset from LV95 by E-2560000, N-1137500
- **Terrain**: flat at ~374m ASL, 1km×1km tile extracted
- **Orientation**: Y-axis = South→North (station→hospital), X-axis = East→West

### Structure — Timber
- **Material**: Glulam GL24h (f_m,k = 24 MPa, f_c,0,k = 21 MPa)
- **Columns**: 200×200mm GL24h, 4.0m clear height
- **Primary beams (deck)**: 140×320mm GL24h, 6m span
- **Secondary beams (roof)**: 140×280mm GL24h, 6m span
- **Bridge deck slab**: CLT 160mm (5-layer) between beams
- **Chamber floor slab**: CLT 200mm (5-layer) — longer spans in station hall
- **Bay spacing**: 6m along Y-axis (bridge), 4m in chambers
- **Lateral bracing**: Steel tension rods Ø16mm in X-pattern between column pairs

### Bridge Span
- **Length**: 60m (Y=-30 to Y=30)
- **Width**: 6m clear (X=-3 to X=3)
- **Two lanes**: fast (east, X=0 to 3) + slow (west, X=-3 to 0)
- **Deck elevation**: +4.0m above ground
- **Bay frame**: paired columns + deck beam + roof beam + 2 posts per bay
- **11 bays at 6m spacing** (Y=-30, -24, -18, -12, -6, 0, 6, 12, 18, 24, 30)

### Station Chamber (south)
- **Footprint**: 12m × 15m (X=-6 to 6, Y=-45 to -30)
- **Program**: Waiting hall (96m²) + reception desk (12m²) + 2× accessible WC (5m² each) + storage (9m²)
- **Floor level**: +4.0m (same as bridge deck — seamless transition)
- **Ceiling height**: 3.5m (floor-to-ceiling), total Z: 4.0 to 7.5m
- **Roof**: flat at Z=+8.0m (with 336mm assembly above structure)

### Hospital Chamber (north) — with switchback ramp
- **Ramp footprint**: 18m × 10m (Y=30 to 48, X=-5 to 5)
- **Descent**: 4.0m at 6% grade (SIA 500 compliant)
- **4 straight runs** of 16.7m each, 180° turn landings (1.5m × 3m each)
  - Run 1: Y=30→46.7, Z=4.0→3.0 (east side, X=1 to 4)
  - Landing A: Y=46.7→48.2, Z=3.0 (turning, south→north becomes north→south)
  - Run 2: Y=48.2→31.5, Z=3.0→2.0 (west side, X=-4 to -1)
  - Landing B: Y=31.5→30.0, Z=2.0 (turning)
  - Run 3: Y=30→46.7, Z=2.0→1.0 (east side again, shifted)
  - Landing C: Y=46.7→48.2, Z=1.0
  - Run 4: Y=48.2→31.5, Z=1.0→0.0 (arrives at grade)
- **Elevator shaft**: 2.5m × 2.5m at X=-6 to -3.5, Y=30 to 32.5
  - Hospital-grade (stretcher capable): cabin 1100×2100mm, door 900mm
  - Serves: +4.0m (bridge level) and 0.0m (ground level)
- **Arrival hall** at ground level: 6m × 4m, Z=0 to 3.5m (at base of ramp/elevator)

### Wall Assembly — Timber Platform Frame (Deplazes p.428, LOG 400)
**Total: 276mm** (outside → inside)
| Layer | Material | Thickness |
|-------|----------|-----------|
| 1 | Horizontal larch boards | 24mm |
| 2 | Ventilated cavity (vertical battens 40×40) | 40mm |
| 3 | Wind barrier (bitumen-impregnated softboard) | 18mm |
| 4 | Timber studs 60×120 + Isofloc insulation | 120mm |
| 5 | Vapour barrier (plywood) | 12mm |
| 6 | Service cavity (vertical battens 50×30) | 50mm |
| 7 | Interior finish (wood-cement particleboard) | 12mm |

### Bridge Deck Assembly (LOG 400)
**Total: 217mm** (top → bottom)
| Layer | Material | Thickness |
|-------|----------|-----------|
| 1 | Anti-slip timber decking (larch) | 40mm |
| 2 | Waterproof membrane (bitumen) | 2mm |
| 3 | Plywood substrate | 15mm |
| 4 | CLT structural slab (5-layer) | 160mm |

### Flat Roof Assembly (Deplazes p.475, LOG 400)
**Total: 336mm** (top → bottom)
| Layer | Material | Thickness |
|-------|----------|-----------|
| 1 | Granule-surfaced bitumen felt (2 layers) | 7mm |
| 2 | Plywood deck | 21mm |
| 3 | Timber joists 40×300 + 120mm insulation | 300mm |
| 4 | Plywood (airtight membrane) | 15mm |
| 5 | (Soffit exposed — structural timber visible from below) | — |

Roof falls: 1.5% minimum toward drainage. Total assembly Z = 8.0 to 8.336.

### Foundation Assembly
- **Pad footings**: 600×600×400mm concrete under each column
- **Strip footings**: 400mm wide × 400mm deep under chamber walls
- **Depth**: 800mm below ground (frost protection, Swiss Plateau)
- **Steel shoes**: Rothoblaas-type timber column connectors
- **Capillary break**: timber base ≥30mm above concrete
- **Ground slab** (chambers only): 200mm reinforced concrete + 50mm lean concrete + insulation 120mm

### Opening Assembly (LOG 400)
**Windows:**
- Frame: timber, 80×80mm profile
- Glass recess: 80mm from exterior wall face
- Glazing: double-pane insulated, 24mm unit (4mm + 16mm gap + 4mm)
- Sill: projecting 40mm beyond wall face, 30mm thick timber
- Lintel: GL24h 140×200mm spanning opening + 150mm bearing each side
- Reveals: 12mm timber lining, returned into wall cavity

**Doors:**
- Frame: timber, 100×60mm
- Leaf: 44mm solid timber (30mm core + 7mm face each side)
- Clear width: 900mm (main entrance), 800mm (internal)
- Threshold: 25mm max height difference (SIA 500)

### Guardrails & Handrails
- **Bridge guardrails**: 1100mm height (SIA 358), timber posts 80×80mm at 1200mm centers, horizontal timber rails 40×60mm at 100mm spacing, timber cap rail Ø50mm
- **Ramp handrails**: both sides, continuous, 850-900mm height, Ø44mm timber, extend 300mm beyond top/bottom
- **Ramp guardrails**: 1100mm height, same detail as bridge

### Fire Code (VKF/AEAI)
- **Building class**: Low-rise (<11m) → timber structure permitted
- **REI requirement**: REI 60 for structure
- **Charring design**: add 39mm sacrificial timber to each exposed face of structural members
  - Columns: 200+39+39 = 278mm nominal → model at 200mm structural + note metadata
- **Escape distance**: max 35m to exit (single direction)
- **Stair width**: ≥1200mm (residential), ≥1500mm (public) → use 1500mm
- **Combustible cladding**: allowed <11m with fire breaks

### Accessibility (SIA 500)
- **Ramp**: 6% max, 1200mm min width, landings every 6m, handrails both sides
- **Doors**: 900mm clear (main), 800mm clear (internal)
- **WC**: 1800×2000mm minimum, grab bars, turning circle
- **Corridor**: 1400mm min for wheelchair passing
- **Elevator**: stretcher-capable 1100×2100mm, door 900mm
- **Tactile strips**: along bridge slow lane, at ramp landings, at elevator doors

---

## Code Compliance Checklist

| Element | Minimum | Standard | Modeled |
|---------|---------|----------|---------|
| Guardrail height | 1070mm | SIA 358 | 1100mm |
| Handrail diameter | 40-45mm | SIA 500 | Ø44mm |
| Ramp gradient | max 6% | SIA 500 | 6% (66.7m for 4m rise) |
| Ramp width | 1200mm | SIA 500 | 1500mm |
| Landing depth | 1400mm | SIA 500 | 1500mm |
| Handrail extensions | 300mm | SIA 500 | 300mm |
| Door clear width (main) | 900mm | SIA 500 | 900mm |
| Door clear width (internal) | 800mm | SIA 500 | 800mm |
| WC turning circle | 1400×1700mm | SIA 500 | 1800×2000mm |
| Escape distance | 35m | VKF | <30m (both chambers) |
| Fire resistance (structure) | REI 60 | VKF low-rise | REI 60 (charring design) |
| Floor-to-ceiling | 2700mm | SIA 180 | 3500mm (chambers) |
| Stair width (public) | 1500mm | VKF | 1500mm |
| Timber above concrete | ≥30mm | Capillary break | 30mm (steel shoe) |

---

## Layer Tree

```
Lock_07::
  Terrain
  Ground::Site          (roads, context buildings)
  Ground::Foundation    (pad footings, strip footings, ground slab)
  Structure::Columns    (GL24h columns)
  Structure::Beams      (GL24h beams — deck and roof level)
  Structure::Slabs      (CLT deck + floor slabs)
  Structure::Bracing    (steel tension rods)
  Shell::Walls::Station       (7-layer timber frame — station chamber)
  Shell::Walls::Hospital      (7-layer timber frame — hospital chamber)
  Shell::Walls::Bridge        (bridge enclosure panels — partial)
  Shell::Facade::Cladding     (larch boards)
  Shell::Facade::WindBarrier  (softboard layer)
  Shell::Facade::Insulation   (Isofloc between studs)
  Shell::Facade::VapourBarrier (plywood)
  Shell::Facade::ServiceCavity (battens + finish)
  Windows                     (frames, glass, sills, lintels, reveals)
  Doors                       (frames, leaves, thresholds)
  Roof::Structure             (timber joists)
  Roof::Insulation            (120mm between joists)
  Roof::Membrane              (bitumen + plywood)
  Roof::Parapet               (copings, flashings)
  Circulation::BridgeDeck     (decking + membrane + plywood + CLT)
  Circulation::Ramp           (switchback runs + landings)
  Circulation::Stairs         (emergency stair alongside elevator)
  Circulation::Elevator       (shaft, doors, cab outline)
  Circulation::Guardrails     (bridge + ramp)
  Circulation::Handrails      (ramp + stairs)
  Circulation::TactileStrips  (guidance + warning strips)
```

---

## Interface Registry

| Interface | Owner | Reference | Rule |
|-----------|-------|-----------|------|
| Wall base → ground slab | Shell | Structure | Wall sits ON slab edge, flush interior |
| Wall top → roof joists | Shell | Roof | Joists bear on wall plate, shell defines top Z |
| Column → beam | Structure | Structure | Beam sits on column top, centered |
| Column → footing | Structure | Ground | Footing centered on column, 3× column width |
| Window → wall void | Windows | Shell | Glass at wall_face - 80mm recess |
| Door → wall void | Doors | Shell | Frame flush with interior face |
| Ramp → bridge deck | Circulation | Structure | Starts at deck Z=4.0, east side |
| Elevator → structure | Elevator | Structure | Shaft walls clear of columns, slab openings at +4.0 and 0.0 |
| Guardrail → deck edge | Circulation | Structure | Posts fixed to deck slab, outer face flush with deck edge |
| Cladding → wind barrier | Shell::Cladding | Shell::WindBarrier | 40mm ventilated gap between |
| Terrain → foundations | Ground::Site | Ground::Foundation | Foundations extend 800mm below terrain |
| Roof membrane → parapet | Roof | Shell | Membrane turns up behind parapet coping |

---

## Risk Assessment (overnight)

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Rhino MCP disconnect | Medium | Total stop | Nothing — restart in morning |
| Agent context overflow | Low | Quality drop | Narrow context per agent, embed data in prompt |
| Switchback ramp geometry error | Medium | Bad geometry | Explicit coordinates for all 4 runs + landings |
| Assembly layers misaligned | Low | Review catch | Z-heights pre-calculated, embedded in prompt |
| Silent script failure | Medium | Empty layers | Health-check pings mandatory between phases |
| Duplicate geometry | Low | Cleanup needed | Unique naming, object count verification |

---

## Success Criteria

The build is successful if:
1. **Object count ≥ 400** (450 target)
2. **Every wall has 7 modeled layers** with correct thicknesses
3. **Ramp is SIA 500 compliant** (6% grade, landings, handrails)
4. **Thermal envelope is continuous** (foundation → walls → roof, no gaps)
5. **Every object has metadata** (material, thickness_mm, SIA reference)
6. **Section test passes** — clipping plane reads bottom-to-top correctly
7. **No zero-thickness or overlapping geometry**
8. **Coordination log documents all decisions**
