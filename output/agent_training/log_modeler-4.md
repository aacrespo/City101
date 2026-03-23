# Modeler-4 Log

## Exercises completed

### Session rebuild — Individual element detail (LOG 300-400)
All exercises rebuilt with individual construction elements per team lead directive.

| Ex | Objects | Type | Notes |
|----|---------|------|-------|
| Ex18 | 81 | Wall-floor junction, single-leaf | Individual 238mm masonry courses, HCB blocks+ribs, tiles |
| Ex19 | 93 | Wall-floor, facing masonry | Individual facing+inner courses with mortar, insulation boards, parquet |
| Ex20 | 46 | Wall-floor, fair-face concrete | Individual stone flags, cellular glass boards, gypsum boards |
| Ex21 | 211 | Wall-floor, lightweight cladding | Individual Eternit slates, masonry courses, battens, parquet |
| Ex22 | 40 | Wall-floor, heavyweight cladding | Individual stone slabs, insulation boards, brackets |
| Ex23 | 37 | Wall-floor, non-loadbearing | Individual particleboard, plywood, parquet boards |
| Ex25 | 23 | Timber frame ventilated | Individual gypsum, particleboard, studs, cladding boards |
| Ex26 | 16 | Three-coat render | Individual masonry courses + 3 render layers |
| Ex27 | 80 | Wood cladding 3 variants | Individual boards, siding, shingles per variant |
| Ex28 | 4 | Double-skin facade | All glass (naturally monolithic), 2 fins |
| Ex33 | 23 | Ribbed concrete slab | Individual ribs, stone tiles |
| Ex36 | 9 | Composite metal-concrete | Decomposed I-section, metal sheeting |
| Ex39 | 8 | Steel floor | Decomposed HEB beam, concrete slab |
| Ex47 | 25 | Flat roof upside-down | Individual XPS boards, battens, decking, wall masonry courses |
| Ex51 | 26 | Pitched roof exposed rafters | Individual boarding, 2-layer insulation, battens, tiles |
| Ex57 | 123 | Window in ETICS | Individual masonry courses around opening, render layers, insulation returns |
| Ex64 | 187 | Hinged external door glass | Individual masonry, Eternit slates, glazed door leaf detail |
| Ex69 | 5 | Pad footing | Fixed to spec dimensions (1200x1200), added base plate |
| Ex77 | 15 | RC column load comparison | 3 columns with scaled footings, lean concrete, gravel |
| Ex78 | 12 | Steel column-beam connection | Decomposed HEA 280 + HEB 300, base plate, anchor bolts, end plate |
| Ex79 | 12 | Bearing wall system | Fixed dimensions (10000mm building width, 5000mm spans) |

### Grand total: 63/63 exercises with objects, 3122 total objects

## Learnings

### Individual element patterns (established in this rebuild)
- **Masonry courses**: 65mm brick + 10mm mortar for standard facing/clay masonry; 238mm for large-format units (36.5x24.8x23.8cm)
- **Tiles**: ~300x300mm with 3mm grout gaps (floor tiles, stone flags)
- **Parquet boards**: ~150mm wide with 2mm gaps
- **Insulation boards**: ~600mm with 2mm joints
- **Gypsum boards**: ~600mm wide with 2mm joints
- **Eternit slates**: ~300x600mm with 3-5mm joints
- **Battens**: individual members at specified c/c spacing
- **Shingles**: 80mm wide with overlap pattern

### Monolithic vs discrete rule
- **Monolithic OK**: poured concrete (slabs, screeds), steel beams/columns, glass, membranes, applied renders/plasters, tile adhesive
- **Must be discrete**: masonry courses, tiles, boards, battens, insulation boards, joists, shingles

### Script efficiency
- Reusable box/tag/ensure_layer helpers are essential
- Wall-with-opening pattern: 4 pieces (left, right, below, above)
- I-section decomposition: 2 flanges + web for steel profiles
- Masonry course loop: while z < height, alternate course + mortar
- Two-zone wall pattern: lower (0 to slab) + upper (slab+floor to top) for wall-floor junctions

### Layer naming confirmed
- `TrainingN::ExNN::SystemName::LayerName` format
- Material name in layer path helps identification
