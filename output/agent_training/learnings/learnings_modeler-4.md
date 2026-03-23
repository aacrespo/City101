# Learnings — modeler-4

## Ex31: Hourdis Hollow Block Floor
- Spec says 10 objects but only 6 physical layers exist in the buildup table. The "10 objects" count may include separating layers or sub-elements not listed. Modeled the 6 real layers faithfully.
- Hourdis vs hollow clay block: same buildup structure, different block type (230mm vs 190-240mm range). Key differentiator is the `hourdis_hollow_block` material tag.
- Separating layer (1mm plastic sheet) from source detail is omitted in curriculum spec — too thin to model meaningfully at this scale.

## Floor series (Ex31-40): Pattern observations
- Floor exercises follow a consistent pattern: structural zone (bottom) + finish layers (top). The structural zone varies (concrete, timber, steel, hollow block) but finish layers are fairly standard (insulation + screed + covering).
- Object count in specs is aspirational — some count separating layers or sub-elements. Model the real physical layers faithfully.
- For ribbed/waffle slabs (Ex33-34): model ribs as discrete elements, top slab as continuous. Waffle = 2-way ribs (both X and Y).
- Composite steel floors (Ex36 vs Ex39): composite has profiled sheeting integrated with concrete; steel floor has beam below separate slab.
- Vittone comparison exercises (Ex40): side-by-side variants at different depths are effective for showing span-depth relationships.

## Wall-floor junctions (Ex19-23): Pattern observations
- Wall-floor junctions need two assemblies (wall + floor) modeled together. Wall is vertical (Y = thickness), floor is horizontal (Z = thickness).
- Ventilated cavities should be voids (no solid object), not filled boxes.
- For non-loadbearing walls (Ex23), the slab extends past the wall zone to show the slab is the primary structure.
- Bracket/fixing elements in heavyweight cladding (Ex22) can be simplified as small boxes in the cavity zone.

## Timber frame walls (Ex24-25, Ex29): Pattern observations
- Non-ventilated (Ex24) vs ventilated (Ex25): the key visual difference is the 25mm batten cavity between outer board and cladding.
- U-value comparison exercises (Ex29): same layer sequence with varying insulation depth. Tag each variant with U_value metadata for downstream comparison.
- Stud-within-insulation-zone: the stud overlaps the mineral wool solid. This is acceptable — in reality the stud displaces insulation at that location.

## Flat roof series (Ex44-49): Pattern observations
- Warm deck: insulation above slab, WP above insulation. Vapour barrier always on warm side (below insulation).
- Upside-down/inverted (Ex47): WP below insulation. Requires XPS (closed-cell, moisture-resistant).
- Cold deck (Ex48): ventilation within joist zone above insulation. No concrete.
- KompaktDach (Ex46): cellular glass = combined insulation + vapour barrier (no separate VB).
- Thickest to thinnest: Ex49 (619mm, foot traffic) > Ex45 (552mm, heavy flags) > Ex44 (452mm, green) > Ex46 (407mm, KompaktDach) > Ex47 (374mm, inverted) > Ex48 (341mm, cold deck timber).
- Parapet modeling (Ex49): needs cellular glass at base for thermal bridge prevention. Two zones (trafficable + verge) share the same slab.

## Door exercises (Ex63, Ex67): Pattern observations
- Multi-layer door leaf construction (Riweg-Isotherm, Ex63): 7 layers totaling 65mm. Unusual materials include coconut fibre insulation and gold skin. The spec's "~65mm" is approximate — individual layer thicknesses may not sum exactly.
- Pocket sliding doors (Ex67): the double-stud wall creates a cavity the door slides into. Model door in half-open position to show the pocket mechanism.
- Wall around door openings needs 3 zones per layer: left flank, right flank, above opening. Each wall layer gets these 3 pieces.
- Undo in Rhino via rs.Command("_Undo") is unreliable for cleaning up failed attempts — orphan objects persist. Always delete explicitly before rebuilding.

## Foundation exercises (Ex68-72): Pattern observations
- Strip footing (Ex68): wider than the wall above (600mm vs 365mm). DPC separates masonry from concrete.
- Pad footing (Ex69): isolated column support. Footing width scales with load.
- Ground slab (Ex70): continuous horizontal element, layers stack vertically.
- Timber plinth (Ex71): stem wall for frost protection, DPC between concrete and timber, sole plate set back 30mm for tolerance.
- Raft foundation (Ex72): thick slab (350mm) acts as both foundation and ground floor structure.

## Stair exercises (Ex73-76): Pattern observations
- Blondel formula (2h + g = 630mm) must be verified for every stair exercise.
- RC stair (Ex73): monolithic inclined slab with step infill on top. Separate finish layers (stone) on treads and risers.
- Stone cantilevered (Ex74): pure cantilever from wall, 250mm embedment minimum. No stringer — dramatic structural concept.
- Metal stair (Ex75): box-section stringers filled with mineral wool for sound. Timber treads on steel brackets.
- Spiral stair (Ex76): requires actual curved geometry (cylinders, pie-shaped treads, pipe handrail). Box approximation insufficient for this type.

## Structural exercises (Ex77-80): Pattern observations
- Column sizing comparison (Ex77): visual demonstration of load-section relationship. Three columns side by side with different sections and footings.
- Steel connection (Ex78): I-section profiles need flanges + web modeled separately (not just boxes). Base plate with anchor bolts.
- Load-bearing wall system (Ex79): plan section showing how interior bearing walls (murs de refend) halve the span.
- Frame system (Ex80): columns + core only, no bearing walls. Free plan (plan libre). Core provides lateral stability.
