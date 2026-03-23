# Ex34: Concrete Waffle Slab Floor
Source: Deplazes p.459

## Object Inventory (current model)
| Layer | Object | Size (mm) | Material |
|-------|--------|-----------|----------|
| Ribs | RibX_1_RC | 1000 x 120 x 300 | reinforced_concrete |
| Ribs | RibX_2_RC | 1000 x 120 x 300 | reinforced_concrete |
| Ribs | RibY_1_RC | 120 x 1000 x 300 | reinforced_concrete |
| Ribs | RibY_2_RC | 120 x 1000 x 300 | reinforced_concrete |
| TopSlab | TopSlab_RC | 1000 x 1000 x 60 | reinforced_concrete |
| ImpactSoundInsulation | ImpactSoundInsulation_MineralWool | 1000 x 1000 x 40 | mineral_wool |
| Screed | Screed_CementUFH | 1000 x 1000 x 80 | cement_screed |
| TileAdhesive | TileAdhesive_Adhesive | 1000 x 1000 x 4 | tile_adhesive |
| FloorTiles | FloorTiles_HardFiredClay | 1000 x 1000 x 15 | hard_fired_clay_tiles |

Total objects: 9

## Comparison against Deplazes p.459

### Layer order: MATCH
- Correct order: ribs + top slab (structural waffle) > impact sound > screed > adhesive > floor tiles
- No soffit treatment (exposed waffle pattern) — correctly omitted

### Proportions: MATCH
- Rib dimensions: 120mm wide x 300mm deep — within spec range (ribs 300-900mm per Deplazes)
- Top slab: 60mm — within 50-80mm range
- Coffers between ribs are approximately square — correct

### Assembly logic: MATCH
- The defining feature of a waffle slab — 2-WAY rib grid — is correctly modeled
- 4 ribs total: 2 in X direction + 2 in Y direction, creating the characteristic waffle pattern
- This correctly distinguishes it from Ex33 (1-way ribbed slab with ribs in one direction only)
- Top slab continuous over all ribs
- Coffers visible from below (the open squares between the crossing ribs)
- Matches the Deplazes isometric drawing showing the waffle grid pattern

### Issues:
1. **Floor tiles not individualized**: At LOG 300-400, the 15mm hard-fired clay tiles should be individual pieces with grout gaps. Currently one 1000x1000mm solid.
2. **Missing separating layer**: Deplazes lists separating layer (1mm plastic sheet) between insulation and screed.

### Missing elements:
- Individual floor tiles with joints
- Separating layer (PE sheet)

### Extra elements: none

## Verdict: WARN

The structural system is correctly and distinctively modeled — the 2-way waffle grid with 4 ribs crossing in both directions clearly differentiates this from the 1-way ribbed slab (Ex33). The assembly logic matches the Deplazes drawing. Minor fixes needed: individualize floor tiles and add separating layer.

### Required fixes:
1. Replace single FloorTiles solid with individual tiles at standard sizes with grout gaps
2. Add separating layer between insulation and screed
