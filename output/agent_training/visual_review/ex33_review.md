# Ex33: Ribbed Concrete Slab Floor
Source: Deplazes p.458

## Object Inventory (current model)
| Layer | Object | Size (mm) | Material |
|-------|--------|-----------|----------|
| Ribs | Rib1_ReinforcedConcrete | 1000 x 150 x 400 | reinforced_concrete |
| Ribs | Rib2_ReinforcedConcrete | 1000 x 150 x 400 | reinforced_concrete |
| TopSlab | TopSlab_ReinforcedConcrete | 1000 x 1000 x 60 | reinforced_concrete |
| ImpactSound | ImpactSound_MineralWool | 1000 x 1000 x 40 | mineral_wool |
| Screed | Screed_Cement | 1000 x 1000 x 80 | cement_screed |
| TileAdhesive | TileAdhesive_Adhesive | 1000 x 1000 x 4 | tile_adhesive |
| StoneTiles | StoneTiles_NaturalStone | 1000 x 1000 x 15 | natural_stone |
| ImpactSoundInsulation | ImpactSoundInsulation_Ex33 | 1000 x 500 x 40 | mineral_wool |

Total objects: 8

## Comparison against Deplazes p.458

### Layer order: MATCH
- Correct order from bottom: ribs + top slab (structural T-section) > impact sound > screed > adhesive > stone tiles
- No soffit treatment (exposed concrete ribs) — correctly omitted

### Proportions: MATCH
- Rib dimensions correct: 150mm wide x 400mm deep
- Top slab: 60mm — within 50-80mm range from spec
- T-section profile matches Deplazes drawing
- Services space visible between ribs (clear gap between the two 150mm ribs in 1000mm strip)

### Assembly logic: MATCH
- The defining feature of a ribbed slab — the T-section with discrete ribs and continuous top slab — IS correctly modeled
- 2 ribs at 500mm c/c spacing per curriculum spec
- Top slab continuous over ribs, forming the characteristic T-section visible in the Deplazes section drawing
- This is fundamentally different from Ex30/31: the structural system is correctly articulated

### Issues:
1. **Duplicate ImpactSoundInsulation**: Two objects on different layers — "ImpactSound" (1000x1000x40) and "ImpactSoundInsulation" (1000x500x40). The 500mm-wide one appears to be an orphan from an earlier attempt.
2. **Stone tiles not individualized**: At LOG 300-400, the 15mm stone tiles should be individual pieces (standard 300x300mm or 400x400mm) with mortar/grout gaps. Currently one 1000x1000mm solid.
3. **Missing separating layer**: Deplazes lists separating layer (1mm plastic sheet) between insulation and screed.

### Missing elements:
- Individual stone tiles with joints
- Separating layer (PE sheet)
- Orphan cleanup needed

### Extra elements:
- Duplicate ImpactSoundInsulation object (orphan at 1000x500mm)

## Verdict: WARN

The structural system is correctly modeled — the ribbed T-section with 2 discrete ribs and continuous top slab matches the Deplazes drawing. This is a significant improvement over Ex30/31 where the structural zone was completely abstracted. However, the model needs cleanup: remove orphan duplicate insulation, individualize stone tiles, and add separating layer. These are minor fixes, not a full redo.

### Required fixes:
1. Remove orphan ImpactSoundInsulation_Ex33 (1000x500mm) object
2. Replace single StoneTiles solid with individual tiles at standard sizes with grout gaps
3. Add separating layer between insulation and screed
