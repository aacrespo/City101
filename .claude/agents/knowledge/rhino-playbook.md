# Rhino Modeling Playbook

How to model architecture in Rhino via MCP. Read this before any modeling session. This is your complete knowledge base — everything you need to build well is here. Update after every build.

Two halves: HOW to think about modeling (assemblies, connections, materials) and HOW to drive the tool (rhinoscriptsyntax, MCP).

## Team Builds

When modeling with agent teams (TeamCreate), follow `workflows/agent-team-modeling-v2.md` for coordination. Complete Phase 0 (site data card, bill of objects, interface registry, layer tree) before spawning any agents. This playbook covers HOW to model; the workflow covers HOW to coordinate the team.

---

## The Core Rule

**Everything has a thickness. Nothing is just a surface.**

A wall is not a box — it's a sequence of layers. A roof panel is not a surface — it's battens, counter-battens, sheathing, tiles. Terrain is not a plane — it's compacted ground. If you model anything as a zero-thickness surface, you've failed the section test.

**Model assemblies, not surfaces.**

Put a clipping plane through your model: can you read a credible section? If you see a single rectangle or a zero-thickness line, you failed. If you see layers with metadata, you succeeded.

```python
# WRONG: concept model
wall = rs.AddBox(corner, 6.0, 0.2, 3.0)

# RIGHT: assembly model
layers = [
    {"name": "exterior_render", "t": 2, "mat": "lime_render"},
    {"name": "structure", "t": 36, "mat": "molasse_sandstone"},
    {"name": "interior_plaster", "t": 2, "mat": "lime_plaster"},
]
offset = 0
for layer in layers:
    geom = make_layer(origin, length, layer["t"], height, offset)
    rs.ObjectLayer(geom, "Wall_Assembly::{}".format(layer["name"]))
    rs.SetUserText(geom, "material", layer["mat"])
    offset += layer["t"]
```

## Étanchéité — The Thermal Envelope

**The building must be tight.** Trace a continuous line around the building section — this is the thermal envelope. Any break = fail. Every agent must know WHERE their system meets the envelope and ensure continuity.

Key envelope principles:
- **Walls**: continuous insulation or mass from foundation to roof
- **Roof-wall junction**: block the gap between rafters at the wall plate (solid blocking or insulation)
- **Material transitions**: sealed — capillary breaks + thermal seals at every change of material
- **Openings**: reveals, frames, and seals must close every penetration
- **Floor-wall junction**: no air path from exterior to interior at slab edge
- **Corners**: wind barrier wraps, insulation stops at corner post — never exposed insulation at corners
- **Penetrations** (chimney, pipes): fire-rated non-combustible collars at every assembly layer crossing

---

## Known Assemblies

These are proven assemblies from archibase and from builds. Use these directly — don't reinvent.

### Rammed Earth Wall (from archibase: `wall_rammed_earth_ext`, 500mm total)
```
exterior: earth/lime render         20mm
structure: rammed earth, compacted  400mm
insulation: wood fibre (optional)   60mm
interior: earth plaster             20mm
```
- Courses are monolithic rings — NEVER 4 boxes meeting at corners
- Course height: 10-15cm (compaction layer)
- Openings: max 1/3 of wall length between structural elements
- Lintels: timber or stone ONLY (never steel in contact with earth)
- Foundation must be below frost depth (80cm in Swiss lowland)
- Overhang: minimum 60cm on all sides — rammed earth is vulnerable to rain erosion

### Stone Masonry Wall (NOT in archibase DB — constructed from knowledge)
```
exterior: lime render               20mm
structure: molasse sandstone         360mm
interior: lime plaster              20mm
total:                              400mm
```
- Course height: 20cm works well for modeling (13 courses = 260cm)
- Lime mortar joints between courses
- Corners: dressed quoins (pierre de taille) or overlap convention (S/N full length, E/W between)
- Thermal performance: poor (U ~2.0 W/m²K) — acceptable for vernacular
- Lintels: stone or timber, never steel. Bearing ≥20cm each side.
- The key requirement is envelope CONTINUITY, not thermal performance
- Generates many objects (222 for cabin v3) — this is fine, each has clear naming

### Timber Frame Wall (from archibase: `wall_timber_frame_ext`, 340mm total)
```
exterior: timber cladding on battens   22mm   (rainscreen, ventilated)
         ventilated air gap            30mm   (pressure equalization)
         wood fibre board              60mm   (wind barrier)
structure: studs 60x160 @ 625cc       160mm  (+ mineral wool between)
         OSB vapour barrier            15mm   (CRITICAL airtightness layer)
interior: service cavity               40mm   (electrical/plumbing)
         gypsum plasterboard           12.5mm (fire protection)
total:                                 339.5mm ≈ 340mm
```
- Build exterior-to-interior: the order matters for construction logic
- Window voids must cut through ALL 7 layers, not just the studs
- OSB vapour barrier is the most important layer for airtightness — must be continuous
- Service cavity exists so you NEVER penetrate the OSB for wiring

### Timber Floor (from archibase: `floor_timber`, 350mm total)
```
finish: wood flooring                  15mm
       dry screed / impact sound       60mm
       impact sound insulation         30mm
structure: OSB structural deck         22mm
          timber joists 80x200 @ 400cc 200mm
ceiling: 2x gypsum board              25mm   (fire + acoustic)
total:                                 352mm ≈ 350mm
```
- Joists typically span the SHORT direction (N-S in an E-W long building)
- Fire stops (mineral wool blocking) between ALL joists at perimeter — prevents fire traveling through joist cavity
- Rim boards (OSB 22mm) at E/W walls where joists run parallel — closes the floor cavity

### Pitched Timber Roof (from archibase: `roof_timber_pitched`, 400mm total)
```
exterior: roof tiles on battens        20mm
         counter-battens + air gap     40mm   (ventilated)
         wood fibre sarking board      60mm   (wind barrier, continuous)
structure: rafters 80x240             240mm  (+ mineral wool between)
         PE vapour barrier             ~0mm   (warm side, continuous)
interior: gypsum board finish          12.5mm
total:                                 372.5mm ≈ 400mm
```
- Ridge runs along the LONG axis. Rafters slope perpendicular to ridge.
- Pitch: ~35° for Swiss Alpine (snow shedding)
- Overhang: 60cm minimum on ALL sides (eaves and gables)
- Inter-rafter blocking at wall plate: solid blocking between every rafter pair — seals the roof-wall thermal junction
- Sarking board must be continuous — no gaps at ridge, eaves, or gables
- Vapour barrier on the WARM side (interior) — continuous

---

## Connections: Where Architecture Happens

Model the CONNECTION, not just the elements on either side.

### Foundation → Wall
- Foundation wider than wall (typically +20cm total)
- DPC (damp-proof course) at interface: bitumen membrane, 0.5cm
- Wall sits ON the DPC, not directly on foundation

### Wall Base → Grade
- Capillary break between any material and the ground
- Splash apron: gravel drainage (not concrete) around perimeter
- Foundation below frost depth: 80cm in Swiss lowland, deeper in Alps

### Stone-Timber Transition (designed in cabin v3 — NOT in archibase)
Three problems solved simultaneously:
```
1. Capillary break: 3mm bitumen membrane on sablière top
   (timber must NEVER touch stone directly — moisture wicks)
2. Thermal seal: 20mm compriband expanding foam tape
   (fills irregularities, seals the junction)
3. Width reconciliation: timber frame inset 3cm from stone face
   (stone projects → sheds water away from timber)
4. Perimeter flashing: zinc drip strip at the stone ledge
   (closes the gap between cladding line and transition seal)
5. Corner patches: separate capillary + thermal pieces at each corner
   (wall-face elements don't meet at corners — patch the gap)
```

### Wall Corners (timber frame)
- **Corner post** (16x16cm minimum) at every wall intersection
- **Wind barrier return**: wood fibre board wraps around from one wall face to the perpendicular — insulation must NEVER be exposed at a corner
- **S/N walls continuous** (full length), E/W walls butt in between
- Think of it like rammed earth rings — the envelope must be continuous at corners

### Lintel → Wall
- Bearing surface ≥20cm each side into wall
- Stone or timber for masonry/earth walls (NEVER steel)
- Doubled studs + timber header for timber frame walls
- Courses above lintel sit ON the lintel at the opening span
- Lintel height vs course height: if lintel protrudes into the next course, that course needs a void too

### Sill Plate / Wall Plate
- Oak timber plate (10×15cm typical) at wall top, centered on structural material
- Bedded in lime mortar (masonry) or bolted (timber frame)
- Receives rafters or upper floor structure
- S/N plates full length, E/W between them (same corner convention as walls)

### Roof-Wall Junction
- Rafters sit on wall plate
- Gap between rafters at wall plate → solid blocking (mineral wool or timber)
- Fascia board at rafter tail ends (vertical, closes eave edge)
- Soffit (horizontal board closing eave underside)
- Wind barrier (sarking) must connect to wall wind barrier

### Chimney / Penetrations Through Assemblies
- **10cm clearance** to all combustible materials (Swiss VKF)
- **Calcium silicate board** collars at EVERY assembly layer the penetration crosses
- **Lead flashing** at the roof tile surface — sheds water around penetration
- **Vapour barrier**: PE membrane cannot touch hot flue — calcium silicate substitutes at penetration
- Chimney top: minimum 50cm above ridge for draft

### Floor-Wall Junction
- Fire stops between joists at wall perimeter
- Rim boards where joists run parallel to wall
- Floor corner blocking at all 4 corners (zone between wall face and first joist)
- At stair openings: closure panel + mineral wool blocking + vapour barrier bridge to seal the envelope breach

---

## Openings: More Than Voids

Openings are not just holes in walls. A complete opening includes:

### In Stone/Earth Walls
- **Lintel**: stone or timber beam with ≥20cm bearing each side
- **Courses above**: sit ON the lintel — courses must be split around voids, not modeled as full rings
- **Door leaf**: frame (oak, 7-8cm section) + timber panel (4cm thick)
- **Window**: frame (oak, 7cm section) + glass pane
- **Reveals**: 2cm lime render return on all cut faces (jambs + soffit)
- **Threshold**: stone at door base, projecting 2cm for weather shed
- **Sill**: stone, projecting 2cm, with 5cm overhang each side of window
- **Hardware**: lever handle interior, pull ring exterior (door); espagnolette handle interior (windows)
- Clear width: rough opening minus 2x frame jamb thickness. For 80cm clear, need ~96cm rough opening.

### In Timber Frame Walls
- **Header**: doubled studs + timber header beam in the stud zone
- **Window voids**: cut through ALL 7 wall layers, not just the studs
- **Frame**: set at the wind barrier face to maintain continuous envelope
- **Reveal insulation**: mineral wool (3cm) fills the gap between window frame and interior layers on all 4 edges
- **Vapour barrier**: window frame connects to OSB vapour layer — no air path
- **Hardware**: espagnolette handle interior

### Opening Void Modeling Technique
For courses/layers with openings: split each segment into pieces around the void. Example for a wall with window at y=200-300:
- Left segment: y=36 to y=200
- Right segment: y=300 to y=564
- Apply to EVERY layer (render, structure, plaster) — finish layers need the same voids as structure

---

## Circulation

### Stairs (Swiss residential, SIA)
- **Rise**: maximum 180mm per step
- **Going**: minimum 270mm per step
- **Blondel formula**: 2R + G = 600-640mm (ideal: 620mm)
- **Clear width**: minimum 900mm between stringers
- **Headroom**: minimum 2000mm from tread nosing to soffit above
- **Landings**: 900mm clear zone at top and bottom of stair
- **Railing**: both sides, 1000mm height, posts every 3rd tread

### Floor Opening for Stairs
- Frame with doubled trimmer joists on long sides
- Header joists on short sides
- Cut joists become stubs bearing on headers
- **Envelope seal**: where opening abuts exterior wall, add closure panel + mineral wool blocking + vapour barrier bridge

### Door Widths
- 80cm minimum clear passage (accessibility)
- In thick walls (40cm stone), the reveal is a 40cm tunnel — factor frame jamb thickness into clear width calculation

---

## Rhinoscriptsyntax Techniques

### Boxes
- `rs.AddBox(pts)` — 8 corner points: [0-3] bottom face, [4-7] top face, counter-clockwise from above
- Helper for axis-aligned boxes:
  ```python
  def box(x, y, z, L, W, H):
      pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
             (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
      return rs.AddBox(pts)
  ```
- Define this helper at the TOP of every script (state doesn't persist between calls)
- For angled elements (rafters): compute all 8 corners from slope geometry

### Hollow Rings (monolithic wall courses, foundation strips)
- **Best**: outer + inner closed polylines → `rs.AddPlanarSrf([outer, inner])` → `rs.ExtrudeSurface(srf, path, cap=True)`
- Creates a TRUE monolithic ring — no corner joints
- Always check return value — `AddPlanarSrf` can fail silently
- **With openings**: DON'T use boolean subtraction. Split into multiple boxes around the void instead.

### Boolean Operations
- `rs.BooleanUnion()` — additive, combining boxes. Generally reliable.
- `rs.BooleanDifference()` — subtractive, cutting holes. UNRELIABLE for complex geometry.
- After any boolean: scan for unnamed orphan objects and delete them
- `BooleanUnion` can return multiple objects — pick by largest bounding box volume, not by index
- Name objects AFTER boolean, not before (inputs may be consumed or orphaned)

### Volume Verification
- `rs.SurfaceVolume(obj)` — compare actual vs expected to verify voids exist
- Bounding boxes are MISLEADING for hollow geometry — a course with a void has the same bbox as one without
- `rs.IsPointInSurface(brep, point)` — definitive test: True = solid, False = void

### Metadata
- `rs.SetUserText(obj, key, value)` — always strings
- Minimum keys: `material`
- `rs.ObjectName(obj, name)` — name EVERY object: `{Element}_{Level}_{Location}_{SubElement}`
- Naming convention: sortable (level first), parseable (underscores), traceable (maps to spec)

### Layers
- `rs.CurrentLayer("Parent::Child")` before creating objects
- Agents use EXISTING layers. Don't create ad-hoc ones.
- DON'T use `rhino_create_layer` for `Parent::Child` paths — it creates orphan top-level layers with literal `::` in the name. Use `rs.AddLayer("Parent::Child")` in Python instead.
- Assign distinct colors per layer for section legibility

### Script Execution
- Break large builds into 3-5 separate `rhino_execute_python_code` calls
- Always `import rhinoscriptsyntax as rs` at top of each script
- Print summary at end (object count, key dimensions)

---

## Common Failures

| Problem | Cause | Fix |
|---------|-------|-----|
| `AddPlanarSrf` returns None | Curves not coplanar or not closed | Verify z-values match, verify closure |
| Boolean difference fails | Complex geometry | Build constructively with multiple boxes |
| `BooleanUnion` returns wrong object | Multiple results, picked index 0 | Pick by largest bounding box volume |
| Orphan objects after boolean | Inputs not consumed | Scan for unnamed objects, delete orphans |
| Script timeout | Too much geometry in one call | Split into multiple scripts |
| Objects on wrong layer | Forgot `rs.CurrentLayer()` | Set layer before EVERY creation block |
| Render/plaster covers openings | Finish layers not split at voids | Every finish layer needs same void pattern as structure |
| Course above lintel floats | No void in course at lintel z-range | If lintel protrudes into next course, void that course too |
| Gable infill missing | Triangular area between wall top and roof forgotten | Walls agent responsibility, not roof |
| Corner insulation exposed | Wind barrier doesn't wrap | Add return piece at every corner |
| Transition gap at corners | Wall-face elements don't meet at 90° | Add separate corner patch pieces |

---

## Review Checklist

### Mode A — Constraint Check
- [ ] Section test: clipping plane, readable bottom-to-top, every layer present with credible thickness
- [ ] Thermal envelope: continuous line from foundation → walls → transition → roof. Any break = FAIL
- [ ] Interface alignment: z-heights match across systems
- [ ] Object count per layer — track across rounds
- [ ] All objects named and have material metadata
- [ ] DPC/capillary breaks at every material transition
- [ ] Fire stops at floor perimeter, between rafters at wall plate
- [ ] Corner posts + wind barrier returns at all wall intersections

### Mode B — Visual Coherence
- [ ] Viewport captures from 4 cardinals + aerial
- [ ] Does it look like the intended building type? (not just a generic box)
- [ ] Proportions: heights, widths, overhangs feel right
- [ ] Roof: protective overhang, correct pitch, fascia/soffit closing edges
- [ ] Openings: placed with intention, rhythmic, proportional to wall area
- [ ] Silhouette: ridge orientation, gable closure, no awkward geometry
- [ ] Compare against a mental reference of the building type — not just numbers

---

## Archibase Query Reference

```python
# Query the construction database
from tools.data.knowledge_bridge import ConstructionDB
import json

db = ConstructionDB()

# Get an assembly (returns None if not found)
a = db.get_assembly('wall_timber_frame_ext')
layers = json.loads(a['layers_json'])

# Get a material
m = db.get_material('stone_sandstone')

# List assemblies
results = db.query('SELECT id, type, total_thickness_mm FROM assemblies')

# Available assemblies:
# wall_rammed_earth_ext, wall_timber_frame_ext, wall_concrete_ext
# floor_timber, floor_concrete
# roof_timber_pitched
# NOTE: stone masonry wall is NOT in the DB — use the assembly above
```

If an assembly doesn't exist in archibase, read the knowledge markdown at `~/CLAUDE/archibase/source/knowledge/materials/` and construct the assembly from material properties + design rules.

---

*Updated: 2026-03-22 — distilled from cabin v1, v2, v3 builds (rammed earth, stone masonry, timber frame, mixed construction). Source learnings: 16 wall, 12 roof, 11 openings, 12 foundation, 7 stone, 9 timber-frame, 10 review, 9 circulation.*
