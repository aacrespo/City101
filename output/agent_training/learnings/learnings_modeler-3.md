# Learnings — modeler-3

## Ex31: Hourdis Hollow Block Floor
- Straightforward 6-layer horizontal stack. Key differentiator from Ex30 is hourdis block thickness (230mm vs 220mm) and material metadata (`hourdis_hollow_block` vs `hollow_clay_block`).
- The archibase source lists tile adhesive thickness as "--" (negligible) for the hourdis type, but the curriculum spec says 2mm. Follow curriculum spec for exercises.
- Modeling bottom-to-top with cumulative z-offsets is the cleanest approach for floor buildups — no negative coordinates, easy to verify layer contacts.

## Ex32: Solid Concrete Slab Floor
- Found pre-existing duplicate objects on the Ex32 layers (another agent had already created objects without exercise metadata). Always check for existing objects before modeling, and tag with `exercise` metadata to distinguish your work.
- Key differentiator: NO soffit plaster — glaze finish directly on concrete underside. Only 4 layers vs 6 in prefab types (Ex30/Ex31).
- Impact sound insulation is 40mm (double the 20mm in prefab types) because in-situ concrete has less inherent damping than prefab hollow block systems.

## Ex35: Hollow-Core Concrete Slab Floor
- Includes bonding coat (2mm) between precast unit and insulation — unique to hollow-core among the floor types.
- Linoleum at 5mm is the thinnest floor covering in the series.

## Ex37: Solid Timber Floor
- All-timber, dry construction. Rubber separating strips (2mm) provide acoustic decoupling between structural timber and counter-batten layer.

## Ex38: Timber Joist Floor
- First exercise with discrete structural members (joists) rather than a continuous slab. Used 1000mm strip to show 2 joists at 500mm c/c.
- Mineral wool infill between joists fills the same zone height as the joists (200mm) — it sits in the joist cavity, not as a separate layer.
- 10 objects total: continuous layers + 2 joists + 3 insulation infill pieces (left, mid, right of joists).

## Ex40: Hourdis Vittone Comparison
- 3 variant sections side by side (A/B/C) at 1500mm spacing. Each has 2 blocks + 1 rib + 1 topping = 4 objects per variant.
- Rib width (80mm) stays constant; block width varies with joist spacing.

## Wall-Floor Junctions (Ex20-23)
- Wall-floor exercises require modeling in two planes: wall in Y (thickness) and floor in Z (depth). The junction is where they meet.
- For non-loadbearing walls (Ex23), the slab extends past the wall zone to show it's infill, not structural.
- Discrete elements like battens, brackets, and studs bring the exercises to life — they're what distinguishes detail types.
- Ventilated cavity objects are placeholders for air; some debate whether to model them or leave the gap. Modeling as a semi-transparent object with `ventilated_air_cavity` material is the clearest approach for review.

## Roof Exercises (Ex41-49, 52)
- Roof exercises split into warm deck (insulation on slab) vs cold deck (insulation at ceiling level) vs inverted/upside-down (insulation above WP).
- Cold deck (Ex43) requires modeling TWO separate zones: ceiling thermal envelope below and uninsulated roof above, with a void between.
- KompaktDach (Ex46) uses cellular glass bonded in hot bitumen — serves as both insulation AND vapour barrier, eliminating one layer.
- Upside-down (Ex47) puts XPS above WP — must be closed-cell (moisture-resistant). Order of layers is inverted from normal warm deck.
- Ex49 (foot traffic + parapet) is the most complex: two zones (trafficable vs verge), each with different finish layers on a shared slab, plus a parapet wall with cellular glass thermal bridge prevention at the base.
- Dormer (Ex52): 6-layer wall buildup at ~174mm + header beams (chevetre) framing the opening in the main roof.

## Door Exercises (Ex63, Ex66)
- Ex63 (external hinged): 7-layer leaf at 65mm with coconut fibre insulation, T30 fire rated. Stone threshold, Stahlton lintel.
- Ex66 (internal acoustic): Multi-layer core for 42dB Rw rating. Symmetric sandwich: Al+resin (2mm) → HDF (3.2mm) → 3×particleboard (39mm) → HDF → Al+resin = 49.4mm core + oak lipping to reach 60mm total.
- Internal doors have no threshold (floor-level gap), filler strip above frame to ceiling, and no insulation foam (vs external).
- Individual brick courses with mortar joints for partition wall (LOG 300-400 compliance) yields ~129 wall objects for a 2700mm high wall at 75mm course height.
- Ex67 (sliding pocket): Double-stud wall with pocket cavity between studs. Only top/bottom rails needed for studs in pocket zone (no intermediate studs blocking leaf travel). Leaf shown half-open = half in pocket, half visible in opening.

## Foundation Exercises (Ex71)
- Ex71 (timber plinth): Two-plane detail — wall in Y, floor in Z, stem wall bridging below grade. Sole plate set back 30mm from stem wall edge for construction tolerance.
- Lean concrete starts below z=0 (below grade), so floor assembly spans from negative Z to positive. Total assembly 432mm verified from lean concrete bottom to tile top.

## Stair Exercises (Ex73)
- RC stair uses inclined slab (paillasse) as 8-point box with angled top/bottom faces. Step infills are rectangular boxes sitting on the slab slope.
- Slab thickness is measured perpendicular to slope (180mm), but vertical thickness = 180/cos(angle) = ~219mm. Use 8-point box to get correct angle.
- Stone tread finish has nosing projection (40mm) beyond riser face — extend tread X dimension by nosing amount.
- Individual tread + mortar + riser finishes per step yields high object count (40 for 9 treads) but is LOG 300-400 compliant.
- Ex74 (stone cantilevered): L-shaped quarter-turn with treads embedded 250mm into masonry walls. Pure cantilever — no stringer, no support at free end.
- Ex75 (metal box-section): Angled 8-point boxes for stringers, timber treads between them. Mineral wool fill noted in metadata.
- Ex76 (spiral): Use AddCylinder for central column, polyline-extruded pie shapes for treads, AddPipe for helical handrail. CapPlanarHoles returns bool (True) on success in some Rhino versions — check `!= True` before assigning.

## Metadata Tagging & Cross-Modeler Coordination
- Objects built by other modelers on `TrainingS3::` prefix layers often lack `exercise` metadata tags. Always check BOTH `Training{Phase}::Ex{NN}::*` AND `TrainingS3::Ex{NN}_*` layer prefixes.
- SetUserText tags can be lost between sessions or after context compaction. Re-tag by iterating all objects on exercise layers and checking for missing `exercise` key.
- Batch tagging script pattern: iterate `rs.LayerNames()` filtered by exercise number, then `rs.ObjectsByLayer()`, then `rs.SetUserText()` for each untagged object.
- After tagging 2989 objects across 63 exercises (Ex18-Ex80), zero untagged remain.

## Ex79 Rebuild
- Original had 4510mm spans (not 5000mm per spec) because 10000mm building width minus wall thicknesses left insufficient clear span.
- Fix: building external width = 10980mm (365 + 5000 + 250 + 5000 + 365), giving exactly 5000mm clear spans.
- Masonry facade walls modeled as individual courses (brick 62.5mm + mortar 12.5mm) for LOG 300-400 compliance.
- RC refend (interior bearing wall) correctly monolithic — poured concrete.
- Party wall: solid masonry courses with F180 fire rating metadata.

## LOG 300-400 Compliance Summary
- Low object counts are acceptable when all elements are naturally monolithic: glass (Ex28), poured concrete (Ex32, Ex35, Ex69), steel (Ex36, Ex39), continuous membranes (Ex44, Ex48).
- Monolithic rule: poured concrete/steel/glass/membranes/linoleum/magnesite = OK monolithic. Masonry/tiles/battens/joists/boards/insulation boards = MUST be discrete.
- Phase 3-4 exercises were already upgraded to discrete elements by other modelers before this session — individual courses, tiles, boards all present.
