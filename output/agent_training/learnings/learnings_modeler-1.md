# Learnings — Modeler 1

## Ex30: Hollow Clay Block Floor
- Floor assemblies are straightforward bottom-up stacks; build from soffit plaster upward
- Always run duplicate scan after modeling — prior runs can leave ghost objects on layers
- Tile adhesive at 2mm is the thinnest layer; verify it's not lost visually in reviews

## Ex33: Ribbed Concrete Slab Floor
- Ribbed slabs need separate rib objects below a continuous top slab — T-section profile
- Place ribs first (z=0 upward), then slab on top — ribs hang below, not embedded in slab
- Use rib spacing (500mm c/c) and rib width (150mm) to calculate Y positions: center ± width/2
- Check for prior-run ghost objects by name pattern — delete before final verification

## Ex36: Composite Metal-Concrete Slab Floor
- Steel beam (HEA 200) is narrower than the strip — center it in Y
- Metal sheeting is full-width (spans between beams), only 1mm — acts as formwork + reinforcement
- Composite action means concrete sits directly on metal deck, no gap

## Ex39: Steel Floor
- Key difference from Ex36 (composite): here beam is fully below slab, no metal deck integration
- Steel floor = beam + slab stacked, composite = beam + deck + concrete integrated
- HEB vs HEA: HEB has wider flanges for the same depth — better for floor support

## Ex18: Single-Leaf Masonry Wall-Floor Junction
- Wall-floor junctions require splitting the masonry into above-floor and below-floor portions
- Render and plaster can run full height (they don't carry load), but masonry must be interrupted where slab bears
- Slab bearing: extend slab into masonry zone (120mm typical bearing length) — slab starts inside wall
- Floor extends from wall into interior; Y coordinate of slab start = masonry inner face minus bearing depth

## Ex22: External Cladding Heavyweight Wall-Floor
- Ventilated cavity with brackets: model brackets as simplified L-shaped steel pieces (not full cavity fill)
- Stone slabs are 30mm (vs 10mm for lightweight cladding) — mechanical fixings required
- Cavity is 30mm (vs 40mm for lightweight) — tighter gap due to heavier cladding
- Same wall-floor junction pattern: split structural wall at slab, keep cladding + insulation full height

## Ex23: Non-Loadbearing External Wall-Floor
- Non-loadbearing wall = infill only. Slab extends PAST wall zone to show it carries all loads
- Timber stud sits within cellulose insulation zone — same Y depth, narrower X width
- Ventilated cavity (25mm) between particleboard and hardboard — no solid object, just gap
- Thinnest wall type at 188mm — lightweight timber frame construction

## Ex27: Wood Cladding Types (3 variants)
- Multi-variant comparison exercises: place variants side by side with gaps, share backing wall
- Shingle arrays generate many objects fast — limit to representative sample (3x3) not full coverage
- Lap siding overlap: 30mm overlap means 180mm board, 150mm exposed — stack bottom-up
- Vertical boards use T&G or cover strips — model as separate boards with small gaps

## Ex42: Pitched Roof Warm Deck Monopitch
- Sloped roof layers: use sloped_box helper with different z_low/z_high for bottom and top edges
- Rupli prefab element integrates structure + insulation into single 260mm composite — model as one object
- Monopitch = single slope, roof bears on wall plate of inner structural leaf
- Birdsmouth connection (20mm) is a detail, not a continuous layer — acceptable to omit at this LOD

## Ex47: Flat Roof Upside-Down (Inverted)
- INVERTED roof: insulation ABOVE waterproofing — WP on warm side of slab, protected by XPS above
- XPS must be closed-cell (moisture resistant) — only insulation type suitable for inverted roofs
- Use z-accumulator pattern: z += layer_thickness after each layer for clean bottom-up stacking
- Okoume timber decking on top creates raised walkable surface over gravel ballast

## Ex51: Vittone Pitched Roof Exposed Rafters
- Exposed rafter roof: rafter is LOWEST layer (interior finish), insulation goes ON TOP
- z-accumulator + sloped_box: accumulate vertical thickness, add slope rise between low/high ends
- Ventilation gap (30mm) between insulation and underlay — add to accumulator but no solid object
- 30-degree pitch: rise = span * tan(30) = ~577mm per 1000mm span

## Ex54: Window in Double-Leaf Masonry
- Window openings require splitting each wall layer into 4 pieces: below, left, right, above
- Use a helper function (wall_around_opening) to generate all 4 pieces per layer efficiently
- Frame sits in insulation zone (not in masonry leaf) — center frame depth in insulation thickness
- Two separate lintels needed: steel angle for outer leaf, concrete/masonry for inner leaf
- Cavity tray above lintel redirects moisture — thin membrane in cavity zone
- Lintel bearing: extend 100mm past opening on each side

## Ex57: Window in ETICS (External Insulation, Rendered)
- ETICS = 6 wall layers (finish/bonding/undercoat/insulation/masonry/plaster), all split at opening
- Frame sits in insulation zone (Y=26-104), not in masonry — ETICS pushes frame outward
- Insulation returns (30mm XPS) cover exposed masonry at all 4 reveals — thermal bridge prevention
- Mesh reinforcement patches at opening corners prevent render cracking — placed in undercoat layer
- Metal sill projects 40mm past exterior face with drip edge fold — water management critical for ETICS
- Ghost objects from prior training runs: always check ALL layer trees (not just your prefix) for Ex{NN} matches

## Ex64: Hinged External Door Wood/Glass
- Door openings go to floor (z=0) — no "Below" piece needed, only left pier, right pier, above head
- Glazed door leaf = timber stiles/rails frame with glass panel inset — not a solid panel
- Outward-opening: position leaf on EXTERIOR side of frame (lower Y value)
- Steel lintel as L-angle: bottom flange + vertical web, bearing 100mm past opening each side
- Threshold slab (glasolithic concrete) is flush with floor — sits below z=0
- Drainage channel at threshold exterior edge prevents water ingress

## Ex67: Sliding Internal Door Pocket
- Pocket door wall = double-stud with cavity: PB 12.5 + Stud 50 + Pocket 75 + Stud 50 + PB 12.5 = 200mm
- Door leaf (40mm) slides in 75mm pocket — leaf thinner than pocket to allow clearance
- Show door half-open: position leaf straddling pocket entrance for visual clarity
- Overhead track runs full pocket length; floor guide runs full length too
- Header beam above opening carries track load — spans between studs
- Back stud + back PB run full height/width (no opening on pocket side)

## Ex71: Solid Timber Panel Plinth (No Basement)
- No-basement plinth = stem wall for frost protection only (800mm below grade)
- DPC (bitumen felt 3mm) is critical between concrete and timber — prevents capillary rise
- Sole plate cut back 30mm from stem wall edge — construction tolerance for alignment
- Wall starts at z=43 (DPC 3mm + sole plate 40mm above grade)
- Floor slab sits inside stem wall zone at grade level — lean concrete on gravel, build up
- Gravel drainage bed below lean concrete prevents water accumulation

## Ex73: Reinforced Concrete Stair
- RC stair = inclined slab (paillasse) + step infills + finishes — 3 distinct systems
- Inclined slab as 8-point box with angled top/bottom faces; thickness perpendicular = 180/cos(angle) in Z
- Step infills are rectangular boxes from previous step top to current step top
- Tread finish with nosing: extends 40mm past riser face below (except first tread)
- Riser finish: thin stone (20mm) applied to front face of each step
- Blondel check: 2R+G must equal 600-650mm (here 2x175+280=630)
- Landing slab same thickness as inclined slab — structural continuity

## Ex77: RC Column with Pad Footing Load Comparison
- Comparison exercises: place variants side by side at consistent spacing for visual comparison
- Footing size scales with load: 800mm for 350kN, 1200mm for 1250kN, 1600mm for 2000kN
- Pedestal (thickened base) transitions from footing to column — slightly larger than column section
- Beam stubs in both directions show load path into column
- Always tag load_kN and section_mm as metadata for comparison exercises

## Ex78: Steel Column and Beam Connection
- I-section profiles = 2 flanges + 1 web (3 objects per profile), NOT a solid box
- Column orientation: flanges parallel to X, web connects flanges in Y direction
- End plate connection: steel plate between column flange and beam end
- Anchor bolts: M20 = 20mm diameter, 400mm embedded in concrete, protrude 50mm above base plate
- Ghost cleanup essential: prior runs leave objects at different coordinates — filter by X position
- Unnamed objects are ghosts from failed script runs — always delete

## Ex22: External Cladding Heavyweight Wall-Floor
- Stone cladding (30mm) hung on L-shaped steel brackets — model horizontal + vertical leg per bracket
- Brackets at floor level transfer dead load of stone above
- Ventilated cavity (30mm) between stone and insulation — narrower than lightweight (40mm)
- Fair-face concrete wall (200mm) split at floor bearing: below slab + above slab
- Insulation (120mm rockwool) continuous past floor zone — key thermal detail

## Ex23: Non-Loadbearing External Wall-Floor
- Wall is INFILL only (188mm) — concrete slab carries all loads, not the wall
- Slab extends past wall zone to express non-loadbearing condition
- Timber box-frame: plywood vapour check + cellulose insulation + hardboard + cavity + particleboard
- Model 1 timber stud at center of cellulose zone (60mm wide, full height)
- Thinnest wall type at 188mm — compare with 490mm facing masonry (Ex42)

## Ex27: Wood Cladding Types (3 variants)
- Three 500mm samples side by side on shared substrate (insulation + backing board)
- Variant A vertical boards: T&G at 120mm width, no visible gap
- Variant B horizontal lap: 180mm board, 150mm exposed, 30mm overlap — stack bottom to top
- Variant C shingles: 80mm wide, 10mm thick, stagger every other course by half-width
- All three variants need individual battens behind cladding

## Ex47: Upside-Down Flat Roof
- INVERTED = insulation ABOVE waterproofing (XPS on warm slab, WP below)
- XPS specifically (closed-cell) because it handles moisture from above
- Timber decking on raised battens creates walkable surface above chippings
- Wall below: external insulation + rendered (ETICS pattern with clay masonry)
- Individual masonry courses for wall, individual boards for roof insulation

## Ex51: Pitched Roof Exposed Rafters
- Insulation ON TOP of rafters (not between) — rafters are interior finish
- Two insulation layers (2x80mm) staggered to reduce thermal bridging
- Boarding + vapour barrier between rafter and insulation
- Counter battens parallel to slope, battens perpendicular = ventilation + tile support
- U-value metadata: 0.31 W/m2K per Vittone table

## Ex54: Window in Double-Leaf Masonry
- Double leaf: outer 125mm + cavity 20mm + insulation 120mm + inner 125mm
- TWO separate lintels: steel angle for outer leaf, concrete for inner leaf
- Frame (78mm) positioned in insulation zone — not in either masonry leaf
- Cavity tray above lintel redirects moisture out of cavity
- Individual masonry courses on BOTH leaves, each split around opening
- Insulation returns (30mm XPS) at all 4 reveals
