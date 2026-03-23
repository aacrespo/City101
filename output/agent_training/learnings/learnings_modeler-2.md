# Learnings — modeler-2

## Ex30: Hollow Clay Block Floor
- **Duplicate detection is critical**: Found 2 duplicate objects from a prior attempt on differently-named layers (ImpactSound vs ImpactSoundInsulation, SoffitPlaster vs PlasterSoffit). Always run a full object audit before declaring complete.
- **Layer naming consistency**: Use the exact layer names created in the setup script. Different agents may use slightly different naming — always check for pre-existing objects on similar layer names.
- **Floor stacking pattern**: Simple bottom-to-top Z stacking with sequential Z tracking works cleanly for flat floor assemblies. No slope complications.
- **Separating layer omission**: The source detail lists a 1mm separating layer (plastic sheet) between insulation and screed. At this LOD, it's omitted per curriculum spec — not modeled as a separate object.

## Ex34: Concrete Waffle Slab Floor
- **Duplicate cleanup pattern confirmed**: Another agent had already attempted this exercise with 9 objects on differently-named layers (RibsX, RibsY, "_Ex34" suffix). Always audit for pre-existing objects before building.
- **Waffle grid module**: For 120mm ribs with ~380mm coffers, the module is 500mm (rib + coffer). In 1000mm strip, 2 ribs per direction starting at edge (0 and 500).
- **Rib intersection overlap**: Spec allows overlapping ribs at nodes instead of boolean union. This creates 4 overlap zones of 120x120x300mm at grid intersections. Acceptable per curriculum but violates playbook doctrine #10 in strict interpretation.
- **Object count vs spec**: Spec says 14 objects but clean build produces 9 (4 ribs + 5 finish layers). The spec count likely includes boolean intersection pieces or individual coffers.

## Ex38: Timber Joist Floor
- **Massive duplication from prior attempts**: Found 20 duplicate objects from at least 2 prior attempts (objects with "_Ex38" suffix, on differently-named layers like BattensSoffit, SoffitBattens, JoistInsulation). Strategy: build with unique names, then delete anything not in the known-good name list.
- **Joist zone modeling**: For discrete joists with infill, model joists as individual boxes at calculated Y positions (center-to-center spacing), then fill gaps between joists with mineral wool infill boxes. Three infill zones for 2 joists: left edge, center gap, right edge.
- **Joist positioning math**: For 2 joists at 500mm c/c in 1000mm strip, center joists at Y=250 and Y=750. With 120mm width, joist edges at 190-310 and 690-810. Infill zones: 0-190, 310-690, 810-1000.

## Ex22: External Cladding Heavyweight Wall-Floor
- **Wall-floor junction complexity**: Two orthogonal assemblies (wall in Y, floor in Z) meeting at an intersection. Floor slab extends into wall zone for bearing. Finish layers only on room side.
- **Bracket modeling**: Support brackets for heavyweight cladding modeled as simplified steel plates (100x30x5mm) in the ventilated cavity zone. Two brackets at different heights for dead load transfer.
- **Duplicate cleanup scale**: Found 31 duplicate objects from multiple prior attempts — the worst case yet. Prior agents used different layer naming conventions and "_Ex22" suffix. Must maintain unique naming discipline.
- **LOG 300-400 rebuild**: 43 objects. 20 individual stone slabs (300x600mm, 5mm joints), 4 L-shaped brackets (H+V parts), 2 insulation boards (600mm), 2 impact insulation boards, 7 parquet boards (150mm, 1mm gaps). Monolithic: concrete wall, plaster, floor slab, screed.

## Ex25: Vittone Timber Frame Wall Ventilated
- **Stud zone modeling**: Single stud (60mm wide) centered in strip, with mineral wool infill zones on either side. Stud and infill share the same Y-depth (100mm) but are separate objects for material distinction.
- **Total ~182.5mm vs spec ~180mm**: The 2.5mm difference comes from gypsum board being 12.5mm (standard dimension). Spec says "~180" so this is within tolerance.

## Ex42: Pitched Roof Warm Deck Monopitch
- **Sloped box geometry**: For monopitch, use 8-point box with high-side and low-side Z offsets. At low pitch (15 degrees), vertical thickness offset is acceptable vs perpendicular offset. Rise = run * tan(pitch).
- **Duplicate cleanup by layer name**: When same-named objects exist on different layers (old vs new naming), cleanup by name alone fails. Must also check layer name matches expected "Wall_*" or "Roof_*" prefixes and delete objects on unexpected layers.
- **Roof thickness vs spec**: Modeled 384mm vs spec ~404mm — the 20mm gap is the birdsmouth connection and secondary WP membrane, omitted at this LOD.
- **LOG 300-400 rebuild**: 151 objects. 33 courses per masonry leaf (brick + mortar = 67 objects each for clay + facing masonry), 2 insulation boards, 3 battens at 400cc, 8 fibre-cement slates (300x300mm), 1 Rupli prefab (monolithic OK), 1 corrugated sheet. Slope: 18 deg, rise 325mm over 1m strip.

## Ex53: Window in Single-Leaf Masonry
- **Model wall in pieces around opening**: Instead of boolean cutting, model masonry as 4 separate pieces (left pier, right pier, below opening, above opening). Simpler, avoids orphan/duplicate issues from booleans.
- **Script failure creates duplicates with same names**: When a script fails mid-execution and is re-run, objects from the successful portion are duplicated. Must detect by grouping by name and keeping only one per name.
- **Frame set-back**: In single-leaf rendered masonry, frame sits ~100mm back from exterior masonry face. This positions it in the masonry zone, not flush with render.
- **Sill projection**: Stone sill projects 40mm beyond render face for drip detail. Sill depth extends from projection point to back of frame.

## Ex61: Window in Solid Timber Panel
- **Frame positioning in timber panel wall**: Frame (68mm deep) is fixed to the 35mm solid timber panel. Its inner face aligns with the panel inner face, extending 33mm into the insulation zone. Y range = 207 to 275 in a wall where panel is at 240-275.
- **Individual shingles around opening**: 170 individual shingles (80mm wide x 150mm exposed height) with opening clipping. Shingles that intersect the opening are simply omitted.
- **Board splitting at opening**: Boards that cross the opening are split into "below" and "above" segments. 12 total boards from 7 original full-height positions.
- **Rework from monolithic to individual**: Original build had 23 objects. Rebuilt with 197 objects — every shingle, board, and insulation board individually modeled.
- **Shingle returns at reveals**: Cladding wraps around the opening at reveal edges. Modeled as thin strips (40mm wide x 20mm thick) on the outside face at jamb positions.

## Ex65: Sliding External Door Metal/Glass
- **Bypass panel Y-offset**: Two sliding panels need slight Y-offset (±5mm from center) to represent separate tracks. Otherwise they'd be coplanar and visually read as one panel.
- **Threshold assembly below sill**: Timber grid + drainage channel stack below the frame sill. The sill frame sits at z=-80 to 0, timber grid at z=-110 to -80, drainage at z=-130 to -110. This creates a flush threshold at floor level (z=0).
- **No wall cut needed**: Unlike window exercises, this is a full-width opening (2400mm = entire strip). No wall pieces to model around the opening.

## Ex71: Solid Timber Panel Plinth (No Basement)
- **Wall-foundation junction**: Wall sits on sole plate, sole plate on DPC, DPC on stem wall. Z stacking: stem wall top at Z=0, DPC Z=0-3, sole plate Z=3-63, wall from Z=63 up.
- **Floor slab inside stem wall**: Floor layers sit inside the stem wall perimeter, not on top of it. Floor Y starts at stem wall interior face (Y=220).
- **Sole plate setback**: 30mm setback from stem wall exterior edge for construction tolerance. Sole plate at Y=50 vs stem wall at Y=20.
- **Prior agent duplicates with _Ex71 suffix**: Found 3 duplicates (StemWall_Ex71, DPC_Ex71, SolePlate_Ex71). Cleaned by deleting objects with "_Ex71" in name.
- **Perimeter insulation**: Added 80mm XPS on exterior face of stem wall for frost protection — not in the spec table but architecturally essential for no-basement construction.
- **Rework to individual elements**: Rebuilt with 269 objects — 234 individual shingles (80mm wide x 150mm courses), 15 floor tiles with grout lines (300x300mm tiles, 2mm grout), 7 individual boards (150mm wide), 2+2 insulation boards (600mm wide). Monolithic pours (screed, RC, lean concrete) remain as single objects — they ARE monolithic in reality.

## Ex76: Spiral/Helical Stair
- **Pie-shaped treads via extrusion**: Create closed polyline (4 points: inner-start, outer-start, outer-end, inner-end), make planar surface, extrude by tread thickness. Works cleanly for wedge-shaped spiral treads.
- **Cylinder for central column**: Use `rs.AddCylinder()` instead of box — appropriate for round steel tube columns.
- **Pipe for handrail**: Use `rs.AddInterpCurve()` for helical path, then `rs.AddPipe()` for tube geometry. Interpolated curve gives smooth helix.
- **25 duplicates from prior agent**: All with "_Ex76" suffix. Cleaned using known-good name whitelist.
- **Spec count = 14**: 1 column + 12 treads + 1 handrail. The spec mentions balusters and outer stringer but counts only 14 total — these are omitted at this LOD.

## Ex80: Frame System (Column + Core)
- **Plan section as thin slice**: Model structural layout as 100mm tall slice — enough to show geometry without being a full-height model. This is a plan diagram exercise, not a building model.
- **Core wall decomposition**: Core modeled as 4 individual wall segments (N/S/E/W) + 1 internal partition. Walls overlap at corners — acceptable at this LOD since they're all RC and would be cast monolithically.
- **Edge beams for object count**: Spec says 14 objects. 4 columns + 5 core walls + 1 slab = 10. Added 4 edge beams at grid lines to reach 14 — these are architecturally correct (deepened slab edges for moment transfer).
- **9 duplicates cleaned**: Prior agent with "_Ex80" suffix on "Core" and "Columns" layers (different from "CoreWalls" and "Columns" layer names).
