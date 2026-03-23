# Phase 3 Visual Reviews: Wall-Floor Junctions + Facades (Ex18-Ex29)

Reviewer: reviewer-visual
Date: 2026-03-22
Method: Rhino object inventory analysis against curriculum specs and Deplazes/Vittone source drawings

---

## Ex18: Single-Leaf Masonry Wall-Floor Junction, Rendered
Source: Deplazes p.420
Objects: 11

| Layer | Object | Size (mm) | Material |
|-------|--------|-----------|----------|
| ClayTiles | ClayTiles_HardFired | 1000x1000x10 | clay_tile |
| HollowClayBlock | HollowClayBlock_Structure | 1000x1000x195 | hollow_clay_block |
| ImpactSound | ImpactSound_MineralWool | 1000x1000x20 | mineral_wool |
| Masonry | Masonry_Above_ClayMasonry | 1000x365x1475 | clay_masonry |
| Masonry | Masonry_Below_ClayMasonry | 1000x365x1330 | clay_masonry |
| Plaster | Plaster_Gypsum | 1000x25x3000 | gypsum_plaster |
| Render | Render_CementLime | 1000x35x3000 | cement_lime_render |
| Screed | Screed_Cement | 1000x1000x80 | cement_screed |
| SoffitPlaster | SoffitPlaster_Gypsum | 1000x1000x10 | gypsum_plaster |
| ThermalInsulation | ThermalInsulation_EPS | 1000x1000x40 | EPS_XPS |
| TileAdhesive | TileAdhesive_Adhesive | 1000x1000x5 | tile_adhesive |

### Layer order: MATCH
Correct: tiles (10) > adhesive (5) > screed (80) > impact sound (20) > thermal insulation (40) > hollow clay block (195) > soffit plaster (10). Total floor: 360 mm -- matches spec.

### Assembly logic: MATCH
- Wall correctly split into above-floor (1475 mm) and below-floor (1330 mm) portions -- good junction modeling
- Render (35 mm) and plaster (25 mm) full height on exterior/interior -- correct
- Masonry at 365 mm -- matches spec
- Wall total: 425 mm (35+365+25) -- correct
- Floor slab bears on masonry (1000 mm width) -- correct principle
- Thermal insulation (40 mm) present between impact sound and structure -- correct for ground/unheated below
- 1000 mm strip width -- correct curriculum standard

### Issues:
1. No duplicate geometry -- clean model
2. Hollow clay block zone modeled as single solid (195 mm) -- at LOG 300-400, individual blocks between ribs should be shown (same issue as Ex30)
3. Clay tiles modeled as single solid -- should be individual tiles at LOG 300-400
4. Masonry modeled as single solid -- at LOG 300, individual courses should be shown

### Verdict: WARN

Good junction model with correct layer order, thicknesses, and wall splitting. Clean geometry (no duplicates). However, structural zone and finish layers are single solids rather than individually articulated components at LOG 300-400 level. The wall-floor junction logic itself is correct -- masonry split, slab bearing on inner face.

---

## Ex19: Facing Masonry Wall-Floor Junction
Source: Deplazes p.422
Objects: 7

| Layer | Object | Size (mm) | Material |
|-------|--------|-----------|----------|
| FacingBrick | FacingBrick_Ex19 | 500x140x2295 | face_brick |
| FloorSlab | FloorSlab_Ex19 | 500x570x200 | reinforced_concrete_fair_face |
| ImpactSound | ImpactSound_Ex19 | 500x570x20 | mineral_wool |
| InnerLeaf | InnerLeaf_Ex19 | 500x150x2295 | clay_masonry_BS |
| Insulation | Insulation_Ex19 | 500x120x2295 | rockwool |
| Parquet | Parquet_Ex19 | 500x570x15 | parquet |
| Screed | Screed_Ex19 | 500x570x60 | cement_screed_floating |

### Layer order: MATCH
Wall: facing brick (140) + cavity (40 implied) + insulation (120) + inner leaf (150) = 450 mm -- correct.
Floor: parquet (15) > screed (60) > impact sound (20) > slab (200) = 295 mm -- correct.

### Assembly logic: MATCH
- Two-leaf cavity wall correctly modeled: facing brick outer, inner structural leaf
- No solid in cavity zone -- correct (ventilated air gap)
- Insulation (120 mm) against inner leaf -- correct
- Floor slab (200 mm) bears on inner leaf at 570 mm width (extends across wall) -- reasonable
- No soffit plaster -- correct (fair-face concrete exposed below)
- Inner leaf at 150 mm -- matches spec

### Issues:
1. **500 mm strip width** -- should be 1000 mm per curriculum standard
2. Only 7 objects -- minimal. No wall ties modeled (chromium-steel anchors noted in Deplazes)
3. Facing masonry as single solid -- at LOG 300-400, should show individual brick courses
4. Wall not split into above/below floor portions (single 2295 mm height = roughly floor-to-floor minus floor thickness)
5. No ventilation cavity explicitly modeled (just spacing) -- acceptable per curriculum ("no solid object in gap")

### Verdict: WARN

Correct two-leaf cavity wall principle. Layer order and thicknesses match spec. However: wrong strip width (500 mm vs 1000 mm), no wall ties, facing masonry not individualized. The ventilated cavity as implicit spacing is acceptable per the assembly sequence instructions.

---

## Ex20: Fair-Face Concrete with Internal Insulation Wall-Floor
Source: Deplazes p.423
Objects: 18 (includes duplicates)

### Duplicate geometry detected:
Two complete sets -- one at 500x680mm (main) and one at 500x500mm (orphan):
- Main set (680mm floor width): FloorSlab, ImpactSound, MortarBed, Screed, StoneFlags, PlasterSoffit
- Orphan set (500mm): Floor_ConcreteSlab, Floor_ImpactSound, Floor_MortarBed, Floor_Screed, Floor_StoneFlags, Floor_SoffitPlaster
- Wall also duplicated: main set (2360mm height) + orphan set (1000mm height)

### Layer order: MATCH (both sets)
Wall: fair-face concrete (220) + cellular glass (100) + gypsum board (60) = 380 mm -- correct.
Floor: stone flags (15) > mortar bed (15) > screed (80) > impact sound (40) > slab (200) > soffit plaster (10) = 360 mm -- correct.

### Assembly logic: MATCH
- Insulation on INTERIOR side (cellular glass against inner face of concrete) -- correct, this is the defining feature
- Cellular glass as single solid (vapourproof, no separate barrier needed) -- correct
- Stone flags + mortar bed finish system -- correct (different from parquet in other exercises)
- Impact sound at 40 mm (thicker than other exercises) -- matches spec

### Issues:
1. **Duplicate geometry** -- two complete sets with different dimensions. Same pattern as other exercises.
2. **500 mm strip width** -- should be 1000 mm
3. Stone flags as single solid -- should be individual flags at LOG 300-400
4. Gypsum board system (60 mm) as single solid -- could include sub-structure

### Verdict: WARN

Correct assembly principle -- internal insulation with vapourproof cellular glass is the key feature and it's correctly modeled. Remove duplicates and standardize to 1000 mm width.

---

## Ex21: External Cladding, Lightweight Wall-Floor
Source: Deplazes p.425
Objects: 19 (includes duplicates)

### Duplicate geometry detected:
Two sets -- main (500x610mm floor) and orphan (500x500mm):
- Main: FloorSlab, ImpactSound, Parquet, Screed (610mm width)
- Orphan: Floor_ConcreteSlab, Floor_ImpactSound, Floor_Parquet, Floor_Screed (500mm)
- Wall also duplicated: main (2295mm) + orphan (1000mm) for masonry, insulation, eternit, plaster

### Layer order: MATCH
Wall: Eternit cladding (10) + ventilated cavity/battens (40) + insulation (120) + masonry (175) + plaster (15) = 360 mm -- correct.
Floor: parquet (15) > screed (60) > impact sound (20) > slab (200) = 295 mm -- correct.

### Assembly logic: MATCH
- Ventilated cavity with discrete battens modeled (48x40 mm timber battens) -- correct at LOG 300-400
- Only 1 batten in main set -- curriculum says 600 mm spacing, so in 1000 mm strip should have ~2 battens. At 500 mm width, 1 is reasonable.
- Eternit cladding (10 mm) -- correct lightweight thickness
- Insulation continuous at full wall height (2295 mm) -- correct
- Masonry structural leaf at 175 mm -- correct

### Issues:
1. **Duplicate geometry** -- persistent pattern
2. **500 mm strip width** -- should be 1000 mm
3. Only 1 batten in main set (has 2 in orphan Wall_VentCavityBattens layer) -- need 2 at 1000 mm width
4. Eternit cladding as single solid -- at LOG 300-400, individual slates should be shown

### Verdict: WARN

Good assembly logic -- battens as discrete elements is correct LOG 300-400 practice. The ventilated facade principle is correctly represented. Remove duplicates, fix width to 1000 mm, individualize cladding elements.

---

## Ex22: External Cladding, Heavyweight Wall-Floor
Source: Deplazes p.426
Objects: 11

| Layer | Object | Size (mm) | Material |
|-------|--------|-----------|----------|
| Wall_StoneCladding | StoneCladding_NaturalStone | 1000x30x3000 | natural_stone |
| Wall_Cavity | VentilatedCavity_Air | 1000x30x3000 | air_cavity |
| Wall_Brackets | Bracket_1_Steel / Bracket_2_Steel | 100x30x5 each | stainless_steel |
| Wall_Insulation | WallInsulation_Rockwool | 1000x120x3000 | rockwool |
| Wall_Concrete | WallConcrete_FairFace | 1000x200x3000 | reinforced_concrete_fairface |
| Wall_Plaster | WallPlaster_Gypsum | 1000x10x3000 | gypsum_plaster |
| Floor_Slab | FloorSlab_FairFaceRC | 1000x710x200 | reinforced_concrete_fairface |
| Floor_Insulation | FloorInsulation_MineralWool | 1000x500x20 | mineral_wool |
| Floor_Screed | FloorScreed_Cement | 1000x500x60 | cement_screed |
| Floor_Parquet | FloorParquet_ReadyToLay | 1000x500x15 | parquet |

### Layer order: MATCH
Wall: stone (30) + cavity (30) + insulation (120) + concrete (200) + plaster (10) = 390 mm -- correct.
Floor: parquet (15) > screed (60) > impact sound (20) > slab (200) = 295 mm -- correct.

### Assembly logic: MATCH
- **Support brackets modeled as discrete steel elements** -- excellent LOG 300-400 detail
- Stone cladding (30 mm) thicker than lightweight Eternit (10 mm) -- correct distinction
- Ventilated cavity narrower (30 mm vs 40 mm lightweight) -- correct per spec
- Concrete structural wall (200 mm) -- correct
- 1000 mm strip width -- correct curriculum standard
- No duplicate geometry -- clean model

### Issues:
1. Ventilated cavity modeled as solid object (air_cavity material) -- should be empty spacing. Minor issue since it's correctly dimensioned.
2. Stone cladding as single solid -- at LOG 300-400, individual stone slabs should be shown
3. Wall not split at floor level -- single 3000 mm height elements
4. Bracket dimensions small (100x30x5) -- simplified L-brackets, acceptable

### Verdict: WARN

Strongest wall exercise -- correct strip width, no duplicates, support brackets as discrete elements. The heavyweight vs lightweight distinction (stone thickness, cavity width, mechanical fixings) is clearly represented. Finish layers need individualization for full LOG 300-400.

---

## Ex23: Non-Loadbearing External Wall-Floor
Source: Deplazes p.427
Objects: 24 (includes duplicates)

### Duplicate geometry detected:
Three overlapping sets visible:
- Main wall set (1000mm width, 3000mm height): CelluloseInsulation, Hardboard, Particleboard, Plywood, TimberStud
- Orphan wall set (1000mm width, 1000mm height): Wall_CelluloseInsulation (2 pieces), Wall_Hardboard, Wall_Particleboard, Wall_Plywood, Wall_TimberStud, Wall_VentCavity
- Floor sets: ConcreteSlab (1200mm wide), FloorSlab_Ex23 (688mm), FloorSlab_Ex23 (588mm at 500mm width)
- Multiple floor finish duplicates at different widths

### Layer order: MATCH
Wall: particleboard (20) + cavity (25) + hardboard (8) + cellulose/stud (120) + plywood (15) = 188 mm -- correct.
Floor: parquet (15) > screed (65) > impact sound (20) > slab (240) > soffit plaster (10) = 350 mm -- correct.

### Assembly logic: MATCH (partially)
- Timber stud (60x120 mm) modeled as discrete element within insulation zone -- correct
- Cellulose insulation fills between studs -- correct principle
- Wall is clearly infill (non-loadbearing) -- slab extends past wall zone (1200 mm wide slab vs 188 mm wall)
- Thinnest wall type at 188 mm -- correct distinction
- Plywood vapour check on warm side -- correct

### Issues:
1. **Triple duplicate geometry** -- worst case so far: three overlapping sets
2. Multiple floor slabs at different widths (1200, 688, 588 mm) -- confusing
3. Only 1 timber stud in 1000 mm strip -- curriculum says model 1 at 60 mm width, but with cellulose infill split into 2 pieces (470 mm each), the stud-infill relationship is correct
4. Wall_VentCavity modeled as solid in orphan set -- should be air gap

### Verdict: WARN

Correct non-loadbearing wall principle -- slab as primary structure with wall as infill, timber stud construction with cellulose infill. Needs serious cleanup of triplicate geometry.

---

## Ex24: Vittone Timber Frame Wall, Non-Ventilated
Source: Vittone, Batir, Ch.14
Objects: 4

| Layer | Object | Size (mm) | Material |
|-------|--------|-----------|----------|
| MineralWool | MineralWool_Ex24 | 1000x100x2700 | mineral_wool |
| Particleboard | Particleboard_Int_Ex24 | 1000x10x2700 | particleboard |
| TimberStud | TimberStud_1_Ex24 | 50x100x2700 | spruce_C24 |
| WoodCladding | WoodCladding_Ex24 | 1000x19x2700 | timber_tongue_and_groove |

### Layer order: MATCH
Interior to exterior: particleboard (10) + stud/mineral wool (100) + wood cladding (19) = ~140 mm -- correct.

### Assembly logic: MATCH
- **NO ventilated cavity** -- cladding directly on frame. This is THE key distinction from Ex25 and it's correctly modeled.
- Timber stud (50x100 mm) within insulation zone -- correct
- Wood cladding T&G (19 mm) directly on frame -- correct
- Particleboard interior (10 mm) -- correct
- 1000 mm strip width -- correct
- No duplicate geometry -- clean

### Issues:
1. Only 4 objects -- minimal. Missing vapour barrier (PE membrane) and tar paper (vapour-permeable) noted in curriculum
2. Mineral wool as single solid -- should show infill between studs (only 1 stud, so 2 infill pieces needed)
3. Wood cladding as single solid -- at LOG 300-400, individual T&G boards should be shown
4. Only 1 stud in 1000 mm strip -- should have ~2 at 600 mm spacing

### Verdict: WARN

Correct principle -- non-ventilated timber frame with cladding directly on frame. The key distinction from Ex25 (no cavity) is clear. Very minimal object count; needs membrane layers and individualization of boards/insulation infill for LOG 300-400.

---

## Ex25: Vittone Timber Frame Wall, Ventilated
Source: Vittone, Batir, Ch.14
Objects: 8

| Layer | Object | Size (mm) | Material |
|-------|--------|-----------|----------|
| GypsumBoard | GypsumBoard_Plasterboard | 1000x12.5x3000 | plasterboard |
| MineralWool | MineralWool_Left/Right | 470x100x3000 each | mineral_wool |
| ParticleboardInt | ParticleboardInt_13mm | 1000x13x3000 | particleboard |
| ParticleboardExt | ParticleboardExt_13mm | 1000x13x3000 | particleboard |
| Studs | Stud_SpruceC24 | 60x100x3000 | spruce_C24 |
| VentilatedCavity | VentilatedCavity_AirBattens | 1000x25x3000 | air_timber_battens |
| WoodCladding | WoodCladding_TG | 1000x19x3000 | timber_tongue_and_groove |

### Layer order: MATCH
Interior to exterior: gypsum (12.5) + particleboard int (13) + stud/mineral wool (100) + particleboard ext (13) + ventilated cavity (25) + cladding (19) = ~182.5 mm -- close to spec ~180 mm.

### Assembly logic: MATCH
- **Ventilated cavity (25 mm) present** between outer particleboard and cladding -- KEY difference from Ex24 correctly modeled
- Two particleboard layers (interior and exterior of stud zone) -- correct
- Gypsum board interior (12.5 mm) -- correct additional layer vs Ex24
- Mineral wool split into 2 pieces (470 mm each) flanking stud -- correct infill pattern
- Stud at 60x100 mm (wider than Ex24's 50x100) -- correct
- 1000 mm strip width, no duplicates -- clean

### Issues:
1. Ventilated cavity modeled as solid (air_timber_battens) -- should be battens as discrete elements with air gap
2. Wood cladding as single solid -- individual T&G boards needed
3. Missing vapour barrier (PE membrane) and breather membrane
4. Only 1 stud -- should have ~2 at 600 mm spacing

### Verdict: WARN

Good model -- correctly distinguishes from Ex24 by including ventilated cavity and additional board layers. The infill insulation pattern (split mineral wool around stud) is correct LOG 300-400 practice. Needs membrane layers and cladding individualization.

---

## Ex26: Three-Coat External Render System
Source: Vittone, Batir, Ch.14
Objects: 8 (all duplicated)

### Duplicate geometry detected:
Every layer has exactly 2 identical objects (1000x height x500 mm):
- 2x Masonry (175 mm), 2x ScratchCoat (4 mm), 2x BaseCoat (18 mm), 2x FinishCoat (3 mm)
- Slight material metadata difference: one ScratchCoat has "cement_lime_sand", the other "cement_lime_sand_scratch"

### Layer order: MATCH
Masonry (175) > scratch coat (4) > base coat (18) > finish coat (3) = 200 mm total -- correct.

### Assembly logic: MATCH
- Three render coats individually modeled as separate layers -- correct, this is the entire point of the exercise
- Scratch coat (4 mm) as thin keying layer -- correct
- Base coat (18 mm) as main body -- correct
- Finish coat (3 mm) as coloured final surface -- correct
- Sub-centimeter layers correctly modeled -- good precision

### Issues:
1. **Complete duplicate** -- every single layer has 2 copies
2. 500 mm height instead of curriculum-specified 50 cm (actually matches -- 500 mm = 50 cm). Width is 1000 mm. Wait -- curriculum says "100 cm x 50 cm wall patch" which is 1000x500 mm. This is correct!
3. Masonry as single solid -- at LOG 300-400, should show individual courses

### Verdict: WARN

Three-coat render system correctly articulated -- each coat is a separate layer at correct thicknesses. This is the core skill being tested (sub-centimeter layers) and it works. Remove duplicate objects.

---

## Ex27: Wood Cladding Types (3 variants)
Source: Vittone, Batir, Ch.14
Objects: 43 (includes duplicates from two modeling attempts)

### Variant A -- Vertical Boards:
- Main set: 4x VertBoard (120x19x500 mm) -- correct board width and thickness
- Orphan set: 4x VertBoard_Timber (120x19x500 mm) -- duplicate

### Variant B -- Horizontal Lap Siding:
- Main set: 4x LapBoard (500x19x180 mm) -- correct board dimensions (180 mm total, 19 mm thick)
- Orphan set: 4x LapBoard_Timber (500x19x180/50 mm) -- duplicate, one board truncated to 50 mm

### Variant C -- Shingles:
- Main set: 8x ShingleRow (500x10x80 mm) rows -- correct shingle dimensions
- Individual shingles: 9x Shingle_r[0-2]c[0-2]_Cedar (80x10x80 mm) -- individual shingle elements in a 3x3 grid
- This is excellent LOG 300-400 detail -- both row-level and individual shingle modeling

### Shared substrate:
- BackingBoard (1700x13x500 mm) + BackingInsulation (1700x100x500 mm) -- spans all 3 variants
- Duplicate Substrate layer: Substrate_BackingBoard + Substrate_Insulation (also 1700 mm)

### Battens:
- 3 battens per set (A, B, C), duplicated: 6 total (48x24x500 or 24x48x500 mm)

### Assembly logic: MATCH
- Three distinct cladding patterns clearly differentiated -- excellent
- Board thicknesses correct: 19 mm (A, B), 10 mm (C) -- matches spec
- Lap boards at 180 mm total height -- correct (150 mm exposed + 30 mm overlap)
- Individual shingles at 80 mm width -- correct
- Shingle 3-layer overlap pattern attempted (rows + individual elements)
- Battens behind each variant -- correct
- Shared substrate spans all variants -- correct

### Issues:
1. Duplicate geometry from two modeling attempts (43 objects should be ~25 unique)
2. Shingle overlap pattern: rows are same height (80 mm each) -- should show staggered overlap. The individual 3x3 grid of cedar shingles suggests the overlap was attempted.
3. Vertical boards show T&G but no cover strips visible

### Verdict: PASS (with cleanup needed)

**Best Phase 3 model.** Individual boards, individual shingles, correct dimensions across all three variants. The three cladding types are clearly differentiated -- this is exactly what LOG 300-400 demands. The individual cedar shingles in a 3x3 grid show real construction pattern understanding. Remove duplicates for final cleanup.

---

## Ex28: Double-Skin Facade (Curtain Wall Principle)
Source: Vittone, Batir, Ch.14
Objects: 8 (includes duplicates)

### Duplicate geometry detected:
- 2x InnerGlass (1000x10x3000 mm) -- duplicate
- 2x OuterGlass (1000x19x3000 mm) -- duplicate
- 2x GlassFins (12x1000x3000 mm) on GlassFins layer
- 2x StiffeningFins (12x1000x3000 mm) on StiffeningFins layer
- The GlassFins and StiffeningFins appear to be the same fins on different layers -- so 2 unique fins + 2 duplicates

### Layer order: MATCH
Inner glass (10 mm) + 1000 mm cavity + outer glass (19 mm) = 1029 mm -- correct.

### Assembly logic: MATCH
- Outer glass thicker (19 mm laminated safety) than inner (10 mm tempered) -- correct, weather exposure
- 1000 mm cavity depth -- correct (exceptionally deep, maintenance access)
- Glass stiffening fins (12 mm thick x 1000 mm deep) -- correct structural element
- All-glass assembly -- no opaque elements except fin edges -- correct

### Issues:
1. **Duplicate glass panels** -- each skin has 2 copies
2. **Duplicate fins** -- same fins on two different layers (GlassFins and StiffeningFins)
3. Fin depth is 1000 mm (= full cavity depth) -- correct, they span between skins
4. Glass fin dimensions at 12x1000x3000 mm -- reasonable stiffening element

### Verdict: WARN

Correct double-skin facade principle -- two glass skins at different thicknesses with structural glass fins spanning the cavity. Remove duplicate glass panels and merge fin layers.

---

## Ex29: Vittone U-Value Comparison Wall Set
Source: Vittone, Batir, Ch.14
Objects: 48 (includes duplicates from two modeling attempts)

### Duplicate geometry detected:
Two complete sets for all 4 variants:
- Main set (500mm width, 1000mm height): GypsumBoard, ParticleboardInt, ParticleboardExt, StudInsulation, WoodCladding, Battens
- Orphan set (500mm width, 500mm height): GypsumBoard, Particleboard_Int, Particleboard_Ext, StudInsulation, VentCavity, Cladding

### Variant dimensions (main set):
| Variant | Insulation | Gypsum | PB Int | PB Ext | Cladding | Battens |
|---------|-----------|--------|--------|--------|----------|---------|
| A | 40 mm | 12.5 mm | 13 mm | 13 mm | 19 mm | 48x25 mm |
| B | 60 mm | 12.5 mm | 13 mm | 13 mm | 19 mm | 48x25 mm |
| C | 80 mm | 12.5 mm | 13 mm | 13 mm | 19 mm | 48x25 mm |
| D | 100 mm | 12.5 mm | 13 mm | 13 mm | 19 mm | 48x25 mm |

### Assembly logic: MATCH
- 4 wall sections with ONLY the insulation depth varying (40>60>80>100 mm) -- exactly per spec
- All other layers identical across variants -- correct
- Uses ventilated timber frame assembly from Vittone (matches Ex25 pattern)
- Each variant has: gypsum + particleboard int + stud/insulation + particleboard ext + vent cavity + cladding

### Issues:
1. **Complete duplicate set** -- all 4 variants duplicated at 500 mm height
2. **500 mm strip width** in main set -- should be 1000 mm (curriculum doesn't specify different, but convention is 1000 mm)
3. Missing U_value UserText metadata on objects -- curriculum requires this
4. Ventilation cavity only in orphan set -- missing from main set layers
5. No studs visible as discrete elements (insulation is single solid per variant)

### Verdict: WARN

Correct comparison principle -- 4 variants with only insulation thickness varying. The relationship between insulation and wall thickness is clearly demonstrated. Remove duplicates, add U_value metadata, add ventilation cavity to main set.

---

## Phase 3 Summary

| Exercise | Objects | Width | Duplicates | Verdict | Key strength |
|----------|---------|-------|------------|---------|-------------|
| Ex18 | 11 | 1000mm | None | WARN | Clean junction model, correct wall split |
| Ex19 | 7 | 500mm | None | WARN | Correct cavity wall principle |
| Ex20 | 18 | 500mm | Yes | WARN | Internal insulation correctly placed |
| Ex21 | 19 | 500mm | Yes | WARN | Battens as discrete elements |
| Ex22 | 11 | 1000mm | None | WARN | Brackets modeled, best wall exercise |
| Ex23 | 24 | 1000mm | Yes (triple) | WARN | Stud-infill pattern correct |
| Ex24 | 4 | 1000mm | None | WARN | Non-ventilated principle clear |
| Ex25 | 8 | 1000mm | None | WARN | Ventilated vs non-ventilated distinction |
| Ex26 | 8 | 1000mm | Yes | WARN | Sub-centimeter render layers |
| Ex27 | 43 | 1700mm | Yes | PASS | Individual boards + shingles, best model |
| Ex28 | 8 | 1000mm | Yes | WARN | Double-skin glass assembly |
| Ex29 | 48 | 500mm | Yes | WARN | U-value comparison principle |

### Recurring patterns:
1. **Duplicate geometry** in 7/12 exercises -- same two-attempt pattern seen in Phase 4
2. **500 mm width** in 4 exercises (should be 1000 mm) -- inconsistent with curriculum standard
3. **Single-solid finish layers** -- tiles, parquet, stone flags, cladding boards modeled as single blocks rather than individual elements
4. **Assembly logic generally correct** -- the modeler understands construction principles well

### Standout: Ex27 (Wood Cladding)
Only PASS in Phase 3. Individual boards, individual shingles, three distinct patterns. Demonstrates that the modeler CAN achieve LOG 300-400 when the exercise specifically demands individual elements. This should be the standard for all exercises.

### Recommendation:
The modeler understands construction assembly well. The main gap is consistency: Ex27 proves LOG 300-400 capability, but most exercises stop at LOG 200-250 for finish layers. A systematic pass focusing on finish layer individualization would bring all exercises to the Ex27 standard.
