# Ex30: Hollow Clay Block Floor
Source: Deplazes p.455

## Object Inventory (current model)
| Layer | Object | Size (mm) | Material |
|-------|--------|-----------|----------|
| ClayTiles | ClayTiles_ClayTile | 1000 x 1000 x 10 | clay_tile |
| TileAdhesive | TileAdhesive_Adhesive | 1000 x 1000 x 2 | tile_adhesive |
| Screed | Screed_Cement | 1000 x 1000 x 80 | cement_screed |
| ImpactSoundInsulation | ImpactSoundInsulation_MineralWool | 1000 x 1000 x 20 | mineral_wool |
| HollowClayBlock | HollowClayBlock_Structure | 1000 x 1000 x 220 | hollow_clay_block |
| PlasterSoffit | PlasterSoffit_Gypsum | 1000 x 1000 x 10 | gypsum_plaster |

Total objects: 6

## Comparison against Deplazes p.455

### Layer order: MATCH
- Layers are stacked in correct order: tiles > adhesive > screed > impact sound > hollow clay block zone > soffit plaster
- Thicknesses match the source spec (10, 2, 80, 20, 220, 10 mm)

### Proportions: MATCH
- Layer thicknesses are dimensionally correct
- The hollow clay block zone (220mm) is clearly the thickest element, as expected

### Assembly logic: MISMATCH (critical)
- The Deplazes drawing (p.455, Fig. 1) clearly shows the hollow clay block floor as a system of **individual hollow clay blocks sitting between reinforced concrete ribs** — not a monolithic slab
- The model represents the entire 220mm structural zone as ONE solid box (1000x1000x220mm)
- In reality, a section cut through this floor type reveals: individual hollow blocks with their characteristic internal voids, concrete ribs between them, and reinforcement
- At LOG 300-400, the structural zone must show individual blocks and ribs

### Missing elements (LOG 300-400 requirements):
1. **Individual hollow clay blocks** — the defining feature of this floor type, completely absent
2. **Concrete ribs** between blocks — absent
3. **Individual clay tiles** — should be ~3 tiles at 30x30cm in a 100cm strip, not one 1000x1000mm slab
4. **Tile gaps/joints** — mortar or grout lines between individual tiles
5. **Separating layer** (PE sheet) — mentioned in Deplazes spec between insulation and screed, not modeled

### Extra elements: none

## Verdict: FAIL

The model is at LOG 200 (abstracted single blocks per layer), not LOG 300-400. Every layer is a single 1000x1000mm solid. The most critical failure is the hollow clay block structural zone: the Deplazes drawing explicitly shows individual blocks between concrete ribs, which is the defining characteristic of this floor type. Without modeling these components individually, a section cut through the model cannot distinguish this floor type from a solid concrete slab — defeating the purpose of the exercise.

### Required rework:
1. Replace the single HollowClayBlock solid with individual hollow clay blocks (with internal voids) and concrete ribs between them
2. Replace the single ClayTiles solid with ~3 individual tiles at 30x30cm with grout gaps
3. Add separating layer (PE sheet, ~1mm) between impact sound insulation and screed
4. All other layers may remain as single solids (screed, adhesive, insulation, plaster are legitimately continuous in reality)
