# Agent Training Curriculum: Construction Detail Modeling in Rhino

*Version 1.0 — 2026-03-22*
*Built from: AR-327 course (law), rhino-playbook (doctrine), learnings files (jurisprudence), how-to-model-architecture study notes*

---

# Part 1: Exercise Curriculum

## Prerequisites

Agents completing these exercises must already have:
- AR-327 weeks 1-11 competency (Rhino fundamentals, Python, OOP, 2D/3D geometry, booleans)
- Access to archibase (`~/CLAUDE/archibase/`) for material specs and assembly lookups
- The `box()` helper function pattern from the playbook
- Understanding of the layer/metadata conventions (`rs.CurrentLayer`, `rs.SetUserText`, `rs.ObjectName`)

## Progression Logic

```
Phase 1: ELEMENTS         Phase 2: ASSEMBLIES        Phase 3: SYSTEMS         Phase 4: INTEGRATION
(single objects)          (multi-layer elements)      (complete assemblies)     (systems meeting)

Ex 1: Timber beam    -->  Ex 4: Wall corner      -->  Ex 7: Roof section  -->  Ex 9: Wall-roof junction
Ex 2: Mortise-tenon  -->  Ex 5: Window in wall   -->  Ex 8: Furniture lib -->  Ex 10: Room corner
Ex 3: Coursed wall   -->  Ex 6: Timber stair     -->
```

---

### Exercise 1: Timber Beam with Chamfers

**Skill focus:** Box creation, edge treatment, material metadata, the principle that everything has thickness

**LOG target:** LOG 300 (accurate dimensions, major features)

**Doctrine principle:** #1 — Everything has a thickness. #9 — Every object has identity.

**Specification:**
- Beam section: 120mm wide x 200mm tall
- Length: 2000mm
- Material: spruce (Fichte), C24 grade
- Chamfers: 5mm on all 4 long edges
- Layer: `Training::Ex01::Beam`
- UserText: `material=spruce_C24`, `section=120x200`, `length_mm=2000`

**Method:**
1. Create box from (0,0,0) to (2000,120,200) using `box()` helper
2. Create 4 chamfer cutter volumes (triangular prisms along each long edge)
3. Boolean difference to cut chamfers
4. Name object `Beam_01_Spruce_120x200`
5. Apply material metadata

**Success criteria:**
- Object count: 1 closed polysurface
- Face count: 12 (6 original faces + 4 chamfer faces, some original faces split)
- Volume: approximately 120x200x2000 minus 4 chamfer strips = ~47,900,000 mm3
- `rs.ObjectName()` returns correct name
- `rs.GetUserText(obj, "material")` returns `spruce_C24`
- Section test: clipping plane at x=1000 shows rectangular section with 4 cut corners

**Estimated complexity:** 1 script call, ~30 lines, 5-8 objects during construction, 1 final object

**Prerequisites:** None (first exercise)

---

### Exercise 2: Mortise-and-Tenon Joint

**Skill focus:** Boolean difference for joinery, precise dimensioning, mating parts with clearance, multi-object assembly

**LOG target:** LOG 400 (detailed assembly, joinery-level)

**Doctrine principle:** #5 — Connections are where architecture happens. #2 — Model assemblies, not surfaces.

**Specification:**
- Member A (horizontal): 120x200mm section, 800mm long, spruce C24
  - Tenon: centered on end face, 40mm wide x 80mm tall x 60mm deep
  - Tenon created by cutting away material around the projection
- Member B (vertical): 120x200mm section, 600mm tall, spruce C24
  - Mortise: rectangular void matching tenon + 2mm clearance all around
  - Mortise: 44mm wide x 84mm tall x 62mm deep, centered on face
- Joint clearance: 2mm on width, height, and depth
- Members meet at 90 degrees (T-junction, Member A's tenon into Member B's face)
- Layer: `Training::Ex02::Joint`
- Sublayers: `::MemberA`, `::MemberB`

**Method:**
1. Create Member A as full box
2. Create 4 cutter boxes around the tenon zone on end face (top, bottom, left, right)
3. Boolean difference: Member A minus cutters = beam with projecting tenon
4. Create Member B as full box
5. Create mortise cutter box (44x84x62mm) centered on Member B face
6. Boolean difference: Member B minus mortise cutter = beam with rectangular hole
7. Position members so tenon aligns with mortise (2mm gap all around)
8. Name, tag, assign layers

**Success criteria:**
- Object count: 2 closed polysurfaces (one per member)
- Tenon dimensions: 40x80x60mm (verify with bounding box of protruding geometry)
- Mortise dimensions: 44x84x62mm
- Gap between tenon surface and mortise surface: 2mm (verify with closest point)
- Section test: clipping plane through joint shows tenon inside mortise with visible gap
- Both objects have material metadata

**Estimated complexity:** 1-2 script calls, ~60 lines, 10-12 objects during construction, 2 final objects

**Prerequisites:** Exercise 1

---

### Exercise 3: Coursed Stone Wall (Stretcher Bond)

**Skill focus:** Systematic geometry generation, pattern logic, mortar joints, arraying with offset

**LOG target:** LOG 300 (accurate dimensions, recognizable construction pattern)

**Doctrine principle:** #6 — Corners are continuous, like rings. #1 — Everything has a thickness.

**Specification:**
- Wall face: 1000mm wide x 810mm tall (10 courses)
- Wall depth: 200mm (half-brick depth for simplicity)
- Stone/brick: 240x115x71mm (Swiss standard NF format)
- Mortar joints: 10mm on all sides
- Pattern: stretcher bond (each course offset by half brick + half mortar)
  - Course 1: starts with full brick (240mm)
  - Course 2: starts with half brick (115mm)
  - Repeat
- Layer: `Training::Ex03::Wall`
- Sublayers: `::Course_01` through `::Course_10`, `::Mortar` (optional)

**Method:**
1. Compute course height: 71 + 10 = 81mm per course
2. For each course (z = course_num * 81):
   - Determine offset: 0mm for odd courses, 125mm (half brick + mortar) for even
   - Calculate number of full bricks that fit, plus end conditions
   - Create brick boxes: each 240x200x71mm with 10mm gaps
   - Handle ends: half bricks (115mm) where needed
3. Name each brick: `Brick_C{course}_B{brick_num}`
4. Tag material: `molasse_sandstone` or `brick_NF`

**Success criteria:**
- Course count: 10
- Total brick count: approximately 40-42 full bricks + 5 half bricks
- Pattern verification: even courses offset by 125mm from odd courses
- No overlapping geometry (mortar gaps maintained)
- Wall face dimensions: approximately 1000x810mm
- Section test: clipping plane at y=100mm shows brick pattern with visible mortar gaps

**Estimated complexity:** 1-2 script calls, ~50 lines with loops, 45-50 objects

**Prerequisites:** Exercise 1

---

### Exercise 4: Multi-Layer Wall Corner

**Skill focus:** Multi-material wall assembly, corner resolution, layer wrapping, the envelope principle

**LOG target:** LOG 350 (connections to other elements shown, individual layers as separate solids)

**Doctrine principle:** #4 — The envelope must be continuous. #6 — Corners are continuous, like rings. #2 — Model assemblies, not surfaces.

**Specification:**
- L-shaped wall, 1500mm on each arm, 500mm tall
- Wall assembly (outside-in):
  - Exterior render: 20mm (lime render)
  - Insulation: 80mm (mineral wool)
  - Concrete block: 150mm (structure)
  - Interior plaster: 15mm (gypsum)
  - Total: 265mm
- Corner type: concrete block continuous on both arms (overlapping at corner)
- Insulation: wraps continuously at corner exterior — NO exposed insulation edge
- Render: wraps continuously over insulation
- Plaster: fills interior corner
- Layer: `Training::Ex04::WallCorner`
- Sublayers: `::Render`, `::Insulation`, `::Structure`, `::Plaster`

**Method:**
1. Plan corner resolution:
   - Arm A runs full length along X (including corner thickness)
   - Arm B butts into Arm A at interior face
   - Insulation wraps around the outer corner — Arm A insulation returns onto Arm B end face
   - Render covers all insulation (no exposed insulation)
2. Model each layer as boxes with correct overlaps
3. Verify envelope continuity: trace a line from exterior → insulation → structure → plaster around the entire L-shape

**Success criteria:**
- Object count: approximately 8-12 (2-3 pieces per layer, depending on wrapping)
- Envelope test: no exposed insulation at the corner — render covers all insulation surfaces
- Section test (horizontal clipping plane at z=250mm): shows all 4 layers, continuous insulation at corner
- Section test (vertical, cutting through corner): shows layer stacking
- All objects have material metadata
- Layer consistency: all objects within ONE LOG step (all LOG 350)

**Estimated complexity:** 2 script calls, ~80 lines, 8-12 final objects

**Prerequisites:** Exercise 1, Exercise 3 (pattern experience)

---

### Exercise 5: Window Frame in Wall

**Skill focus:** Openings as complete systems, reveals, frame profiles, glazing, envelope completion at penetrations

**LOG target:** LOG 400 (all layers + edge conditions, joinery-level for frame)

**Doctrine principle:** #7 — Openings are more than voids. #4 — Envelope must be continuous. #3 — Section test is the gold standard.

**Specification:**
- Wall: 300mm thick, 2000mm wide x 1500mm tall (simplified single-material for this exercise)
  - Wall material: concrete
- Opening: 900mm wide x 1200mm tall, centered horizontally, sill at 400mm above wall base
- Window frame: timber (oak), 60mm wide x 80mm deep
  - Frame sits 40mm from exterior wall face (creates exterior reveal of 40mm)
  - Interior reveal: 300 - 40 - 80 = 180mm
- Glazing: 6mm thick, inset in frame center (27mm from frame exterior face)
- Sill: stone, 960mm wide (30mm beyond opening each side), 50mm tall, 300mm deep
  - Projects 30mm beyond exterior wall face (drip detail)
  - 5-degree slope is optional (LOG 400 refinement)
- Reveals: lime render return, 15mm thick, on all 3 reveal faces (jambs + head)
- Layer: `Training::Ex05::Window`
- Sublayers: `::Wall`, `::Frame`, `::Glazing`, `::Sill`, `::Reveals`

**Method:**
1. Create wall as solid box
2. Create void cutter (900x300x1200mm) for the opening
3. Boolean difference to create wall with opening
4. Model frame as 4 pieces (head, sill piece, 2 jambs) — box frame profile
5. Model glazing as thin box within frame
6. Model sill with projection
7. Model 3 reveal returns (2 jambs + head soffit) as thin boxes
8. Verify envelope: render return + frame + glazing = sealed opening

**Success criteria:**
- Object count: 7-9 (wall, 4 frame pieces or 1 frame, glazing, sill, 3 reveals)
- Opening dimensions verify: 900x1200mm clear between frame inner edges
- Frame depth: 80mm, frame width: 60mm
- Sill projects 30mm beyond wall face
- Section test (horizontal at z=800): shows wall, reveals, frame, glazing, air gaps
- Section test (vertical at x=1000): shows head, sill, frame, glazing
- Reveal covers all exposed wall material at opening edge
- Point-in-surface test: point at opening center returns False (void exists)

**Estimated complexity:** 2-3 script calls, ~100 lines, 7-9 final objects

**Prerequisites:** Exercise 2 (booleans), Exercise 4 (multi-layer thinking)

**Jurisprudence reference:** learnings-openings.md #2 (sill projection), #9 (reveal as LOD question), #13 (frame position in deep reveals)

---

### Exercise 6: Timber Stair (4 Steps)

**Skill focus:** Angled geometry, repeated elements with computed offset, the Blondel rule, structural members

**LOG target:** LOG 350 (assembly-level — stringers, treads, nosing as separate objects)

**Doctrine principle:** #1 — Everything has a thickness. #8 — Structure before envelope before detail.

**Specification:**
- 4 risers, 3 treads + landing
- Rise: 180mm per step (2R+G = 630mm → G = 270mm)
- Going: 270mm per tread
- Width: 900mm clear between stringers
- Stringers: 50mm thick x 250mm deep, cut to stair profile
  - At LOG 350: model as notched beams (sawtooth cut on inner face)
  - Simplification: model as sloped boxes with notch cutouts
- Treads: 30mm thick, 270mm deep (going), 1000mm long (stringer outer to outer)
  - Nosing: 40mm projection beyond riser face on each tread
- Material: oak (treads), spruce (stringers)
- Layer: `Training::Ex06::Stair`
- Sublayers: `::Stringers`, `::Treads`
- No risers (open stair — Swiss residential common)
- No railing (separate exercise at LOG 400)

**Method:**
1. Compute stair geometry:
   - Total rise: 4 x 180 = 720mm
   - Total going: 3 x 270 = 810mm (3 treads, 4th step is landing)
   - Stringer slope angle: atan(720/810) ≈ 41.6 degrees
2. Model stringers:
   - Option A (LOG 350): sloped box, then cut notches for tread bearing
   - Option B (simpler): create stringer profile as polyline, extrude to 50mm
3. Model treads:
   - For each step n (0-2): box at x=0, y=n*270, z=(n+1)*180-30, size 1000x(270+40)x30
   - Nosing: tread extends 40mm past the riser line (y-40mm from tread back)
4. Position treads on stringer notches

**Success criteria:**
- Blondel check: 2*180 + 270 = 630mm (within 600-650 range)
- Object count: 2 stringers + 3 treads = 5 objects minimum
- Clear width between stringers: 900mm
- Tread nosing: 40mm projection visible in section
- Section test (vertical, cutting along stair center): shows stringer profile, tread positions, nosing projections
- All treads at consistent rise (180mm between each)
- All objects named and tagged with material

**Estimated complexity:** 2 script calls, ~80 lines, 5-7 final objects

**Prerequisites:** Exercise 2 (booleans for notches), Exercise 1 (beam basics)

**Jurisprudence reference:** learnings-circulation.md #1 (stringer thickness affects clear width)

---

### Exercise 7: Pitched Roof Section (500mm Strip)

**Skill focus:** Layered assembly at an angle, material thickness stacking, counter-batten/batten logic

**LOG target:** LOG 400 (full assembly detail, every layer modeled)

**Doctrine principle:** #2 — Model assemblies, not surfaces. #4 — Envelope must be continuous. #3 — Section test is the gold standard.

**Specification:**
Model a 500mm-wide strip of single-pitch roof at 30 degrees:

| Layer (bottom to top) | Thickness | Material | Spacing/notes |
|----------------------|-----------|----------|---------------|
| Gypsum ceiling | 12.5mm | plasterboard | continuous |
| Vapour barrier | 1mm | PE membrane | continuous |
| Rafters + insulation | 180mm | spruce C24 + mineral wool | rafters 60mm wide at 600mm c/c (model 1 rafter in 500mm strip) |
| Sarking board | 22mm | wood fibre | continuous |
| Counter-battens | 50mm tall x 25mm wide | spruce | on top of each rafter (1 in strip) |
| Battens | 38mm tall x 25mm wide | spruce | perpendicular to counter-battens, at 340mm gauge |
| Plain tiles | 10mm thick, 265mm x 165mm | clay | 75mm lap, so exposed = 265-75 = 190mm gauge |

- Strip width: 500mm (along ridge direction)
- Rafter span visible: 2000mm (from wall plate to near ridge)
- Roof pitch: 30 degrees
- Layer: `Training::Ex07::Roof`
- Sublayers: `::Gypsum`, `::VapourBarrier`, `::Rafters`, `::Insulation`, `::Sarking`, `::CounterBattens`, `::Battens`, `::Tiles`

**Method:**
1. Establish rafter slope: 30 degrees, running from (0,0,0) to (2000*cos30, 0, 2000*sin30)
2. Model rafter as sloped box (use 8-point approach — vertical offset per learnings-roof.md #1)
3. Model insulation as box filling between rafter sides (500-60=440mm of insulation)
4. Stack layers on top of rafter: sarking → counter-batten → battens → tiles
5. Stack layers below rafter: vapour barrier → gypsum
6. Each layer's z-coordinates computed from cumulative thickness along the slope normal
7. Tiles: array along the slope at 190mm gauge (exposed length)

**Success criteria:**
- Layer count: 8 distinct material zones
- Object count: approximately 15-25 (continuous layers + arrayed elements)
- Section test (cutting across slope): shows ALL 8 layers with correct thicknesses
- Ventilation gap: counter-batten creates 50mm gap between sarking and battens (visible in section)
- Tile overlap: each tile overlaps the one below by 75mm
- Rafter depth: 180mm visible in section
- All objects tagged with material and thickness metadata
- Envelope trace: vapour barrier is continuous below rafters (no penetrations)

**Estimated complexity:** 3-4 script calls, ~150 lines, 15-25 final objects

**Prerequisites:** Exercise 4 (multi-layer), Exercise 1 (beam basics)

**Jurisprudence reference:** learnings-roof.md #1 (vertical offset approach), #13 (layered z-offset tracking), #16 (assembly layer panels as continuous sloped boxes)

---

### Exercise 8: Door with Frame and Hardware

**Skill focus:** Small-scale precision, hardware geometry, threshold/weatherstrip details

**LOG target:** LOG 400 (detailed — hardware as simplified solids)

**Doctrine principle:** #7 — Openings are more than voids. #5 — Connections are where architecture happens.

**Specification:**
- Door leaf: 900mm wide x 2100mm tall x 44mm thick, timber (oak)
- Frame: timber (oak), 120mm wide x 80mm deep
  - Head + 2 jambs (no frame at threshold — separate element)
  - Frame sits in a 300mm wall (same as Exercise 5)
  - Frame position: 40mm from exterior face
- Hinges: 2 butt hinges at 300mm and 1500mm from bottom
  - Simplified geometry: 2 rectangular plates (70x30x3mm each) + cylinder pin (diameter 10mm, length 70mm)
  - Hinge knuckle: 5 interlocking cylinders (simplified as single cylinder)
- Handle: lever type, both sides
  - Backplate: 240x40x8mm rectangle
  - Lever: cylinder 20mm diameter, 120mm long, angled 15 degrees down
  - Height: 1050mm from floor (center of backplate)
- Threshold: stone, 960mm wide x 300mm deep x 15mm tall
  - Sits at z=0, projects 30mm beyond exterior wall face
- Weatherstrip groove: 3mm wide x 5mm deep, routed around frame inner perimeter
  - At LOG 400: model as boolean cut into frame
- Layer: `Training::Ex08::Door`
- Sublayers: `::Leaf`, `::Frame`, `::Hinges`, `::Handle`, `::Threshold`, `::Weatherstrip`

**Method:**
1. Model frame (3 pieces: head + 2 jambs)
2. Cut weatherstrip groove into frame (boolean difference with thin box along frame inner edge)
3. Model door leaf
4. Model hinges (plates + pin cylinders, positioned on leaf edge and frame jamb)
5. Model handles (backplates + lever cylinders, both sides of leaf)
6. Model threshold

**Success criteria:**
- Object count: 15-20 (frame pieces, leaf, hinge components, handle components, threshold)
- Door leaf thickness: 44mm
- Handle height: 1050mm ± 5mm
- Hinge positions: 300mm and 1500mm from bottom
- Weatherstrip groove: visible in section as 3x5mm notch in frame
- Threshold projects beyond wall face
- Section test: horizontal cut at z=1050 shows handle, leaf, frame, groove
- All objects named and tagged

**Estimated complexity:** 3-4 script calls, ~120 lines, 15-20 final objects

**Prerequisites:** Exercise 2 (booleans for groove), Exercise 5 (opening in wall context)

---

### Exercise 9: Wall-to-Roof Junction (Eaves Detail)

**Skill focus:** System interface — where wall assembly meets roof assembly, envelope continuity at transition

**LOG target:** LOG 400 (joints modeled, material transitions detailed)

**Doctrine principle:** #5 — Connections are where architecture happens. #4 — Envelope must be continuous. #8 — Structure before envelope before detail.

**Specification:**
Model the junction where a timber frame wall meets a pitched timber roof. This is a 500mm-wide strip showing:

**Wall assembly (from Exercise 4, simplified to timber frame):**
- Interior gypsum: 12.5mm
- Service cavity: 40mm
- OSB vapour barrier: 15mm
- Studs + insulation: 160mm (1 stud in 500mm strip)
- Wind barrier (wood fibre): 60mm
- Ventilated cavity: 30mm
- Timber cladding: 22mm
- Wall height: 600mm (just the top portion)

**Roof assembly (from Exercise 7, simplified):**
- Gypsum ceiling
- Vapour barrier
- Rafters + insulation (180mm)
- Sarking
- Counter-battens + battens + tiles

**Junction elements:**
- Wall plate: 150mm wide x 100mm tall, oak, centered on stud zone
- Rafter bearing: rafter sits on wall plate (birdsmouth cut at LOG 400, notch at LOG 350)
- Fascia board: 22mm thick, oak, covers rafter ends at eave
- Soffit: 12mm plywood, horizontal, closes underside of eave overhang
- Gutter bracket: simplified L-shape, 5mm steel, at fascia
- Inter-rafter blocking: mineral wool between rafters at wall plate zone
- Insulation continuity: wall insulation meets roof insulation at plate zone

**Eave overhang:** 600mm beyond wall face

- Layer: `Training::Ex09::Eaves`
- Sublayers: `::Wall`, `::Roof`, `::Junction`, `::Trim`

**Method:**
1. Build wall top portion (7 layers, 600mm tall)
2. Place wall plate on stud zone top
3. Build rafter from plate out to eave (angled, with birdsmouth notch)
4. Continue roof layers from rafter
5. Model fascia at rafter end
6. Model soffit from fascia back to wall face
7. Model inter-rafter blocking
8. Verify: insulation continuous from wall through plate zone into roof

**Success criteria:**
- Envelope continuity test: trace a line from wall interior gypsum up through wall vapour barrier, across the plate zone (blocking fills gap), into roof vapour barrier, along to ridge — NO breaks
- Thermal bridge check: insulation continuous from wall through junction into roof
- Fascia covers rafter end grain (weather protection)
- Soffit closes the eave cavity from below
- Section test: vertical cut shows all wall layers transitioning to roof layers
- Object count: approximately 25-35
- All objects named and tagged

**Estimated complexity:** 4-5 script calls, ~200 lines, 25-35 final objects

**Prerequisites:** Exercise 4 (wall assembly), Exercise 7 (roof assembly)

**Jurisprudence reference:** learnings-roof.md #14 (inter-rafter blocking for thermal envelope), learnings-timber-frame.md #5 (frame wall layer order)

---

### Exercise 10: Furnished Room Corner

**Skill focus:** Integration of all previous skills, system coherence at room scale, furniture as proper objects

**LOG target:** LOG 350-400 (walls at 350, furniture at 300-350, connections at 400)

**Doctrine principle:** All 10 doctrine principles applied. This is the capstone.

**Specification:**
Model a 2000mm x 2000mm corner of a room showing:

**Floor buildup (bottom to top):**
- CLT panel: 120mm (structure)
- Impact insulation: 30mm
- Cement screed: 60mm
- Parquet flooring: 15mm (oak)
- Total floor assembly: 225mm
- Finished floor level: z=0 (floor structure below, z=-225 to z=0)

**Wall (one wall with window, from Exercise 5):**
- Assembly: concrete 150mm + insulation 80mm + render 20mm (exterior) + plaster 15mm (interior)
- Height: 2800mm (floor to ceiling)
- Window: 900x1200mm, sill at 800mm, with frame + glazing + sill + reveals

**Wall-to-floor junction:**
- Skirting board: 15mm thick x 80mm tall, oak, applied to wall interior face
- Floor edge: screed and parquet stop 15mm from wall (skirting covers the gap)
- Detail: insulation folds under the screed at the wall base (impact insulation return)

**Furniture: timber shelf unit (freestanding):**
- Dimensions: 800mm wide x 300mm deep x 1200mm tall
- Material: oak, 18mm board thickness
- 4 shelves (including top and bottom) + 2 side panels
- Joints: housing joints (5mm deep dadoes in side panels)
- Back panel: 6mm plywood
- Position: 200mm from wall, 500mm from corner
- LOG 300-350: side panels, shelves, and back panel as separate objects with visible housing joint notches

**Layer: `Training::Ex10::RoomCorner`**
- Sublayers: `::Floor`, `::Wall`, `::Window`, `::Skirting`, `::Furniture`

**Method:**
1. Build floor assembly (4 layers, extending under both wall positions)
2. Build wall with window (reuse Exercise 5 approach, but with multi-layer wall from Exercise 4)
3. Model wall-floor junction: skirting, insulation fold
4. Build shelf unit with housing joints
5. Position furniture in room
6. Run section tests in both X and Y directions

**Success criteria:**
- Total object count: approximately 30-40
- Section test X: shows wall layers, window in wall, floor layers, skirting, shelf unit
- Section test Y: shows floor layers, wall return, skirting, shelf unit from the side
- Floor-wall junction: no gap visible — skirting covers screed edge
- Shelf unit: housing joints visible in section (5mm notches in side panels)
- LOG consistency: walls at 350, floor at 350, window at 400, furniture at 300-350 (all within one step)
- All objects named, layered, and tagged with material metadata
- Envelope: wall insulation continuous past floor junction

**Estimated complexity:** 5-6 script calls, ~250 lines, 30-40 final objects

**Prerequisites:** All previous exercises (this is the capstone)

---

# Part 2: Parametric Furniture Library Spec

## Design Principles

All furniture scripts follow these rules:
1. **Parametric:** accept dimensions as arguments, use sensible defaults
2. **LOG 300 minimum:** recognizable form with major sub-components, not bounding boxes
3. **Aesthetic:** Swiss Alpine vernacular — simple timber, visible joinery, honest proportions
4. **Metadata:** every object gets material, component name, and parent furniture ID
5. **Layered:** each piece on `Furniture::{Type}::{Component}` sublayers
6. **Composable:** each script returns a list of GUIDs for the furniture group

## Common Parameters (all scripts)

```python
# Every furniture script accepts these base parameters:
def create_[furniture](
    origin=(0,0,0),        # placement point (floor level, front-left corner)
    material="oak",        # timber species
    board_thickness=18,    # mm, for case goods
    log_level=300,         # 300 or 350
    layer_parent="Furniture"  # parent layer name
):
```

---

### F1: Dining Table

**Default dimensions:** 1800L x 900W x 750H mm
**Parameters:** `length, width, height, leg_section=80, top_thickness=30, stretcher=True`

**LOG 300 components:**
- Top slab: length x width x top_thickness
- 4 legs: leg_section x leg_section x (height - top_thickness), inset 60mm from edges
- 2 long stretchers (if stretcher=True): 40x60mm, connecting legs at 200mm above floor

**LOG 350 additions:**
- Edge profile on top (3mm chamfer on underside edge)
- Legs with tapered lower half (reduce to 0.7x section at foot)
- Stretcher tenon visible at leg junction (20x40mm projection)

**Defaults:** length=1800, width=900, height=750, leg_section=80, top_thickness=30

**Object count:** LOG 300: 5-7 | LOG 350: 7-11

---

### F2: Chair

**Default dimensions:** 450W x 500D x 850H mm (seat height 450mm)
**Parameters:** `width, depth, seat_height=450, back_height=850, leg_section=35, seat_thickness=20`

**LOG 300 components:**
- Seat: width x depth x seat_thickness at seat_height
- 4 legs: leg_section x leg_section, front legs straight, back legs angled (extend to back_height)
- Back: 2 vertical back legs + 2 horizontal rails (top rail at back_height - 30mm, mid rail at seat_height + 150mm)
- Back rails: 30x20mm section

**LOG 350 additions:**
- Seat with slight dish (1-2mm concavity — simplified as flat at LOG 350, noted in metadata)
- Legs with chamfered bottom edges (2mm)
- Back rail ends narrowed to tenon width

**Defaults:** width=450, depth=500, seat_height=450, back_height=850

**Object count:** LOG 300: 7-9 | LOG 350: 9-13

---

### F3: Bench

**Default dimensions:** 1200L x 350W x 450H mm
**Parameters:** `length, width=350, height=450, leg_section=60, top_thickness=40, leg_count=2`

**LOG 300 components:**
- Seat plank: length x width x top_thickness
- 2 (or 3 for >1500mm) slab legs: width x 30mm x (height - top_thickness)
  - Legs inset 100mm from ends
  - Optional: arch cutout at leg bottom (decorative, 100mm radius)

**LOG 350 additions:**
- Through-tenon visible on seat top (leg extends through seat, trimmed flush)
- Wedged tenon detail (small wedge slot at tenon top)

**Defaults:** length=1200, width=350, height=450, leg_count=2

**Object count:** LOG 300: 3-4 | LOG 350: 5-8

---

### F4: Bed

**Default dimensions:** Single 900mm / Double 1400mm wide, 2000mm long
**Parameters:** `mattress_width=900, mattress_length=2000, frame_height=300, headboard_height=900, footboard=True, footboard_height=500`

**LOG 300 components:**
- Frame: 4 rails (2 long sides + head + foot), 30mm thick x frame_height tall
  - Frame inner dimensions = mattress dimensions + 10mm clearance each side
- Mattress: box sitting inside frame, 200mm thick, top at frame_height + 200
  - Material: `mattress_fabric` (not timber)
- Headboard: full width x 30mm thick x headboard_height, attached to head rail
- 4 legs: 60x60mm posts at corners, from floor to frame rail top
- Optional footboard: same as headboard but at footboard_height

**LOG 350 additions:**
- Slat support: 5-7 slats (70mm wide x 18mm thick) spanning between long rails
- Leg-to-rail joint visible (mortise-tenon at each corner)
- Headboard planks (3-4 vertical boards instead of single slab)

**Defaults:** mattress_width=900, mattress_length=2000, frame_height=300, headboard_height=900

**Object count:** LOG 300: 6-8 | LOG 350: 15-22

---

### F5: Wardrobe / Armoire

**Default dimensions:** 1200W x 600D x 2000H mm
**Parameters:** `width=1200, depth=600, height=2000, door_count=2, shelf_count=3, has_drawer=False`

**LOG 300 components:**
- Carcase: 2 side panels + top + bottom + back (18mm boards, 6mm back)
- Doors: door_count panels (18mm), full height minus 100mm (top/bottom gaps)
- Internal shelves: shelf_count horizontal boards, evenly spaced
- Plinth: 80mm tall base, inset 30mm from front face

**LOG 350 additions:**
- Door hinges (simplified cylinders at 2 points per door)
- Door handles (simple cylindrical pulls, 20mm diameter x 100mm)
- Shelf housing joints (5mm dadoes in side panels)
- Crown moulding profile at top (20x30mm beveled strip)

**Defaults:** width=1200, depth=600, height=2000, door_count=2, shelf_count=3

**Object count:** LOG 300: 8-12 | LOG 350: 16-24

---

### F6: Desk

**Default dimensions:** 1400W x 700D x 750H mm
**Parameters:** `width=1400, depth=700, height=750, drawer_unit=False, drawer_count=3, leg_section=60`

**LOG 300 components:**
- Top: width x depth x 25mm
- 4 legs: leg_section x leg_section x (height - 25)
- Back rail: 60x30mm, connecting back legs at 400mm height (stiffening)
- Optional drawer unit: box (400W x depth x 400H) under one side of top
  - Drawer fronts: drawer_count rectangles with 5mm gaps

**LOG 350 additions:**
- Drawer fronts with recessed pulls (10mm deep x 30mm tall slot at top edge)
- Leg chamfers (3mm)
- Cable management hole in top (50mm diameter circle, boolean cut)

**Defaults:** width=1400, depth=700, height=750, drawer_unit=False

**Object count:** LOG 300: 5-9 | LOG 350: 10-18

---

### F7: Bookshelf

**Default dimensions:** 800W x 300D x 1800H mm
**Parameters:** `width=800, depth=300, height=1800, shelf_count=5, back_panel=True`

**LOG 300 components:**
- 2 side panels: depth x 18mm x height
- shelf_count shelves: (width - 36mm) x depth x 18mm, evenly spaced
- Top and bottom panels (included in shelf_count or separate)
- Back panel: width x height x 6mm (plywood)
- Plinth: 60mm tall, inset 20mm

**LOG 350 additions:**
- Housing joints: 5mm dadoes in side panels for each shelf
- Shelf front edge: 3mm chamfer or rounded nose
- Adjustable shelf pin holes (optional — row of 5mm cylinders as boolean cuts in side panels, 32mm system spacing)

**Defaults:** width=800, depth=300, height=1800, shelf_count=5

**Object count:** LOG 300: 8-10 | LOG 350: 10-15

---

### F8: Kitchen Counter

**Default dimensions:** 2400W x 600D x 900H mm
**Parameters:** `width=2400, depth=600, height=900, cabinet_count=3, countertop_thickness=30, countertop_material="stone_granite"`

**LOG 300 components:**
- Countertop: width x depth x countertop_thickness (material override: stone, not timber)
- Base cabinets: cabinet_count units, each (width/cabinet_count - 20mm gap) x (depth - 50mm) x (height - countertop_thickness - 80mm plinth)
  - Each cabinet: 2 sides + bottom + back + 1 door
- Plinth: continuous 80mm tall base, inset 50mm from front

**LOG 350 additions:**
- Cabinet doors with handle (cylindrical pull)
- Countertop overhang: 20mm front, 0mm back (against wall)
- One cabinet with drawer stack instead of door (3 drawers)
- Sink cutout in countertop (optional, boolean difference, 500x400mm)

**Defaults:** width=2400, depth=600, height=900, cabinet_count=3

**Object count:** LOG 300: 15-20 | LOG 350: 25-35

---

### F9: Wood-Burning Stove / Kachelofen

**Default dimensions:** 600W x 500D x 1200H mm (freestanding stove, not full Kachelofen)
**Parameters:** `width=600, depth=500, height=1200, type="stove"` (options: "stove", "kachelofen")

**Stove (LOG 300) components:**
- Main body: width x depth x height, with 3mm chamfer on vertical edges
- Firebox door: 300x400mm rectangle on front face, inset 5mm (separate object)
- Flue collar: cylinder, 150mm diameter x 100mm tall, centered on top
- 4 legs: 40x40mm x 100mm, at corners (body raised off floor)
- Material: `cast_iron` (not timber)

**Kachelofen (LOG 300) components:**
- Base plinth: width x depth x 200mm (masonry)
- Tile body: (width-40) x (depth-40) x (height-200-100), centered on plinth
- Crown moulding: width x depth x 100mm at top
- Firebox door: same as stove
- Flue: 150mm diameter, from top through ceiling
- Material: `ceramic_tile` (body), `masonry` (plinth)

**LOG 350 additions:**
- Tile pattern on Kachelofen faces (grid of 150x150mm tiles with 5mm grout, modeled as grid of boxes)
- Stove door handle (cylindrical pull)
- Ash drawer below firebox (30mm tall rectangle)

**Defaults:** width=600, depth=500, height=1200, type="stove"

**Object count:** LOG 300: 5-7 | LOG 350: 8-30 (Kachelofen tiles add many objects)

---

### F10: Simple Cabinet

**Default dimensions:** 600W x 400D x 800H mm
**Parameters:** `width=600, depth=400, height=800, door_count=1, shelf_count=1, drawer_on_top=False`

**LOG 300 components:**
- Carcase: 2 sides + top + bottom + back (18mm boards, 6mm back)
- door_count doors (18mm)
- shelf_count internal shelves
- Plinth: 60mm, inset 20mm

**LOG 350 additions:**
- Door hinges and handle
- Housing joints for shelves
- Optional top drawer (if drawer_on_top=True): 1 drawer with front and pull

**Defaults:** width=600, depth=400, height=800, door_count=1, shelf_count=1

**Object count:** LOG 300: 6-8 | LOG 350: 10-14

---

# Part 3: LOG Update for Workflow Document

## Proposed Addition to 00_Workflow_v04.md Section 2.4

*Insert after the current LOG spectrum table (line ~100), before the LOI spectrum table.*

---

### 2.4.1 LOG Per-Element Definitions

The generic LOG spectrum (100-500) applies differently depending on the element type. This table defines what each LOG level means for each building element category, providing clear targets for agents and reviewers.

#### Walls

| LOG | What to model | Example |
|-----|---------------|---------|
| 200 | Single solid box, correct footprint and height | `rs.AddBox(corners)` — one object per wall |
| 300 | 2-3 zones visible: structure, insulation, finish grouped as thick bands | 3 boxes per wall segment (render + structure + plaster) |
| 350 | Individual layers as separate solids with correct thicknesses | 7 boxes per timber frame wall segment, each layer with material metadata |
| 400 | All layers + edge conditions: corner wraps, reveals at openings, DPC at base, fire stops | Full assembly with wind barrier returns, thermal seal strips, blocking |

#### Floors

| LOG | What to model | Example |
|-----|---------------|---------|
| 200 | Single slab, correct extent and thickness | One box per floor zone |
| 300 | Structure + finish differentiated (2-3 layers) | CLT slab + screed/finish as separate objects |
| 350 | Full assembly layers visible: structure, insulation, screed, finish | 4-5 layers per floor zone, each with material metadata |
| 400 | + Edge conditions: rim boards, fire blocking at walls, resilient bars, acoustic details | Assembly with junction elements and construction sequence logic |

#### Roofs

| LOG | What to model | Example |
|-----|---------------|---------|
| 200 | Single sloped surface or box, correct pitch and extent | One box per roof slope |
| 300 | Rafters + panel/sheathing differentiated | Rafter boxes + continuous panel box |
| 350 | Full layer stack: rafters, sarking, counter-battens, battens, covering | 6-8 layer types as separate objects per slope |
| 400 | + Tiles as individual elements, ridge detail, eave fascia/soffit, inter-rafter blocking | Full assembly with all trim, blocking, and edge conditions |

#### Openings (Windows / Doors)

| LOG | What to model | Example |
|-----|---------------|---------|
| 200 | Void in wall (boolean cut or gap), no frame | Just the hole |
| 300 | Frame + leaf/glazing as simple boxes, correct dimensions | 3-4 objects: frame, glass, maybe sill |
| 350 | + Reveals (render returns), sill with drip projection, lintel visible | 7-9 objects including reveals and sill |
| 400 | + Hardware (hinges, handles), weatherstrip grooves, frame profiles, threshold | 15-20 objects with sub-centimeter hardware geometry |

#### Furniture

| LOG | What to model | Example |
|-----|---------------|---------|
| 200 | Bounding box only — correct footprint and height | Single box per furniture piece |
| 300 | Recognizable silhouette: table with top + legs, chair with seat + back + legs | 5-9 objects per piece, proportionally correct |
| 350 | Major sub-components separated, visible joinery (housing joints, tenons), edge profiles | 10-20 objects per piece with joint details |
| 400 | Joinery-level detail: drawer runners, edge profiles, hardware (pulls, hinges), back panels | Full construction detail, every board modeled |

#### Connections / Junctions

| LOG | What to model | Example |
|-----|---------------|---------|
| 200 | Not modeled — elements simply overlap or abut | Elements placed next to each other |
| 300 | Elements positioned correctly at interfaces, no gap or overlap | Wall sits on foundation at correct z |
| 350 | How layers meet at junctions: which wraps, which butts, continuity shown | Insulation wrapping at corner, sill bearing on wall |
| 400 | Joints modeled: notches, bolts, brackets, capillary breaks, thermal seals, blocking | Birdsmouth rafter cut, steel shoe at column base, transition membranes |

#### Hardware

| LOG | What to model | Example |
|-----|---------------|---------|
| 200 | Not modeled | — |
| 300 | Not modeled | — |
| 350 | Simplified presence: cylinder for hinge pin, box for handle backplate | 1-2 objects per hardware piece |
| 400 | Simplified solids: hinge plates + pin, lever handles, lock backplate, brackets, gutter | 3-5 objects per hardware piece, correct position and proportion |

#### Stairs

| LOG | What to model | Example |
|-----|---------------|---------|
| 200 | Sloped box or stepped profile, correct footprint | Single object showing overall stair volume |
| 300 | Treads + stringers as separate objects, correct rise/going | 2 stringers + n treads = n+2 objects |
| 350 | + Nosing detail, open/closed riser decision, notched stringers | Notch cuts in stringers, nosing projection on treads |
| 400 | + Railing with balusters, landing structure, stringer connections to floor/wall | Full stair assembly with all trim and safety elements |

#### Chimneys / Flues

| LOG | What to model | Example |
|-----|---------------|---------|
| 200 | Vertical box or cylinder, correct position | Single object |
| 300 | Flue liner + outer shell differentiated | 2 concentric boxes/cylinders |
| 350 | + Insulation between liner and shell, cap/cowl at top | 3-4 objects per chimney |
| 400 | + Flashing at roof penetration, fire-rated collar, clean-out door | Full chimney assembly with weather and fire details |

### 2.4.2 LOG Adjacency Consistency Rule

**Elements in the same section view must be within ONE LOG step of each other.**

Rationale: A section with LOG 400 walls next to LOG 200 furniture looks incoherent — the viewer can't tell if the furniture is unfinished or intentionally abstract. Keeping elements within one LOG step maintains visual coherence.

| If walls are at... | Minimum furniture LOG | Minimum connection LOG | Minimum opening LOG |
|--------------------|-----------------------|------------------------|---------------------|
| LOG 200 | 200 | 200 | 200 |
| LOG 300 | 200 | 200 | 300 |
| LOG 350 | 300 | 300 | 300 |
| LOG 400 | 300 | 350 | 350 |

**Exception:** LOG 350v (presentation visual) — visible elements at LOG 400, hidden elements at LOG 200 or omitted. This mode is explicitly for renders, not sections.

---

# Part 4: Training Session Prompt

The following prompt is designed to be pasted into a fresh Claude Code session. It loads the necessary context, runs exercises in order, and reports progress.

---

````markdown
# Agent Training Session: Construction Detail Modeling

You are entering a training session. Your goal is to complete a series of construction detail modeling exercises in Rhino, building progressively from simple elements to integrated assemblies.

## Context Loading

Before starting, read these files in order:

### 1. Doctrine (how we model)
Read: `~/CLAUDE/city101/.claude/agents/knowledge/rhino-playbook.md`
This is your modeling philosophy. Internalize the 10 principles before touching Rhino.

### 2. Jurisprudence (what we've learned)
Read ALL learnings files:
- `~/CLAUDE/city101/.claude/agents/knowledge/learnings-walls.md`
- `~/CLAUDE/city101/.claude/agents/knowledge/learnings-foundation.md`
- `~/CLAUDE/city101/.claude/agents/knowledge/learnings-stone.md`
- `~/CLAUDE/city101/.claude/agents/knowledge/learnings-timber-frame.md`
- `~/CLAUDE/city101/.claude/agents/knowledge/learnings-openings.md`
- `~/CLAUDE/city101/.claude/agents/knowledge/learnings-roof.md`
- `~/CLAUDE/city101/.claude/agents/knowledge/learnings-circulation.md`
- `~/CLAUDE/city101/.claude/agents/knowledge/learnings-review.md`

These are precedents from real builds. Use them to avoid repeating mistakes.

### 3. Study Notes (architectural knowledge)
Read: `~/CLAUDE/city101/claudes-corner/2026-03-21_how-to-model-architecture.md`
This tells you what walls, floors, roofs, and stairs actually are — assemblies, not surfaces.

### 4. Law (material specs and assembly definitions)
The archibase is at `~/CLAUDE/archibase/`. Query it when you need:
- Material properties (density, thermal conductivity, thickness ranges)
- Assembly definitions (wall types, floor types, roof types)
- Construction rules (SIA codes, fire requirements, acoustic requirements)
- The AR-327 course content: `~/CLAUDE/archibase/source/computational_design/AR327_complete_course_content.md`

### 5. Exercise Specifications
Read: `~/CLAUDE/city101/output/agent_training/exercise_curriculum.md`
Part 1 contains the 10 exercises with exact specifications. Follow them precisely.

## Rhino Setup

Before starting exercises:
1. Verify Rhino MCP connection is active
2. Set units to millimeters
3. Create top-level layer `Training` with sublayers per exercise (`Ex01` through `Ex10`)
4. Set tolerance to 0.01mm

## Exercise Execution Protocol

For EACH exercise:

### Before modeling
1. Read the exercise specification fully
2. Write a spatial plan as comments (see playbook section on "Plan Before You Model")
3. Identify which doctrine principles apply
4. Check jurisprudence for relevant learnings

### During modeling
1. Use the `box()` helper function (define at top of EVERY script — state doesn't persist):
```python
import rhinoscriptsyntax as rs

def box(x, y, z, L, W, H):
    pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
           (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
    return rs.AddBox(pts)
```
2. Set `rs.CurrentLayer()` before EVERY creation block
3. `rs.SetUserText(obj, "material", value)` on EVERY object
4. `rs.ObjectName(obj, name)` on EVERY object
5. Break complex builds into 3-5 separate script calls
6. Print summary at end of each script

### After modeling
1. **Section test:** Place clipping planes in both X and Y directions. Capture viewport for each.
2. **Verification:** Run the success criteria checks from the spec:
   - Object count matches expected range
   - Key dimensions verified (bounding boxes, distances)
   - Volume checks where specified
   - Material metadata present on all objects
3. **Write learnings:** If you discovered anything new (a technique that worked, a gotcha, a better approach), write it to a new file: `~/CLAUDE/city101/.claude/agents/knowledge/learnings-training-ex{NN}.md`

## Progress Reports

After completing exercises 1-3, 4-6, and 7-8:
- Capture a viewport showing all completed exercises
- Print a summary: exercise name, object count, pass/fail on each success criterion
- List any learnings discovered
- Note any specifications that need revision

This lets Andrea check progress without interrupting your flow.

## Exercises 8-10: Furniture Library Integration

Exercises 8-10 shift to building the parametric furniture library. For these:

### Exercise 8 pivot: Instead of the door exercise alone, ALSO build 3 furniture scripts:
- F1: Dining Table
- F2: Chair
- F3: Bench

### Exercise 9 pivot: Build 3 more furniture scripts:
- F4: Bed
- F7: Bookshelf
- F10: Simple Cabinet

### Exercise 10: Integration
- Build the Room Corner exercise from the curriculum
- Populate it with furniture from your library scripts (table + 2 chairs from Ex 8)
- Run full section tests
- This validates both the construction detail skills AND the furniture library

For each furniture script:
1. Write the script to `~/CLAUDE/city101/output/agent_training/furniture/` as `f{NN}_{name}.py`
2. Test it in Rhino at LOG 300
3. If LOG 300 passes, test at LOG 350
4. Capture viewport of both LOG levels

The furniture scripts should be self-contained — paste into any Rhino session and they work. Include the `box()` helper, parameter defaults, and layer setup in each script.

## Remaining Furniture

After completing exercises 1-10, if time permits, build the remaining furniture scripts:
- F5: Wardrobe
- F6: Desk
- F8: Kitchen Counter
- F9: Wood-Burning Stove / Kachelofen

## Completion

When all exercises and furniture scripts are complete:
1. Write a summary to `~/CLAUDE/city101/output/agent_training/TRAINING_REPORT.md`:
   - Each exercise: pass/fail, object count, key dimensions, learnings
   - Each furniture script: parameter list, LOG 300 object count, LOG 350 object count
   - Overall observations: what's hard, what's easy, where the specs need revision
2. Capture a final viewport with all training geometry visible
3. List all files created during the session

## Rules

- Do NOT modify any file outside `output/agent_training/` and `.claude/agents/knowledge/learnings-training-*.md`
- Do NOT skip exercises — they build on each other
- Do NOT proceed to the next exercise if the current one fails its success criteria — fix it first
- Query archibase for ANY dimension you're unsure about — don't guess
- If a boolean operation fails, try the multi-box approach from learnings-walls.md #3
- If you discover a specification error in the curriculum, note it in your training report but follow the spec as written

## Time Management

- Exercises 1-3: approximately 30-45 minutes (simple geometry, establishing patterns)
- Exercises 4-6: approximately 45-60 minutes (multi-layer assemblies)
- Exercise 7: approximately 30 minutes (layered roof, systematic)
- Exercises 8-10: approximately 60-90 minutes (furniture scripts + integration)
- Total estimated: 3-4 hours

Report progress at the checkpoints. Andrea will review captures and may adjust remaining exercises based on results.
````

---

*End of curriculum document. This is a living document — update exercise specifications based on training session results.*
