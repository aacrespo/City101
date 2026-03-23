# Ex32: Solid Concrete Slab Floor
Source: Deplazes p.457

## Object Inventory (current model)
| Layer | Object | Size (mm) | Material |
|-------|--------|-----------|----------|
| Parquet | Parquet_Ex32 | 500 x 500 x 15 | ready_to_lay_parquet |
| Screed | Screed_Ex32 | 500 x 500 x 80 | cement_screed_UFH |
| ImpactSoundInsulation | ImpactSound_Ex32 | 500 x 500 x 40 | mineral_wool |
| ConcreteSlab | ConcreteSlab_Ex32 | 500 x 500 x 210 | reinforced_concrete_glaze_finish |

Total objects: 4

## Comparison against Deplazes p.457

### Layer order: MATCH
- Correct order: parquet > screed > impact sound insulation > concrete slab
- No soffit plaster needed (glaze finish on concrete underside) — correctly omitted

### Proportions: MATCH
- Thicknesses correct: 15, 80, 40, 210 mm
- Total: 345mm matches spec
- Impact sound at 40mm (correctly thicker than 20mm in prefab floor types)

### Assembly logic: MATCH (with caveats)
- For a solid concrete slab, the assembly IS monolithic — single solid blocks per layer are largely appropriate
- The concrete slab is correctly a single pour (in situ), not prefab elements
- Glaze finish soffit correctly represented via material metadata rather than separate object
- No soffit plaster — correct per spec

### Issues:
1. **Wrong strip width**: Model uses 500x500mm, curriculum specifies 100cm (1000mm) wide strip
2. **Parquet not individualized**: At LOG 300-400, ready-to-lay parquet should show individual planks (~15mm thick, typical widths 90-120mm) with gaps between them. Currently one solid block.
3. **Missing separating layer**: Deplazes mentions separating layer (polystyrene or similar) between insulation and screed
4. **Insulation boards**: Could show individual insulation boards at standard widths (600mm) with staggered joints, but this is a minor point for mineral wool

### Missing elements: none critical (aside from parquet individualization)
### Extra elements: none

## Verdict: WARN

Unlike Ex30/Ex31, the solid concrete slab floor does not have discrete structural components to model — the assembly logic is fundamentally correct. However, the model falls short of LOG 300-400 in two ways: (1) wrong strip width (500mm vs 1000mm), and (2) parquet should be individual planks, not one solid. The missing separating layer is also a gap. These are fixable without a full redo.

### Required fixes:
1. Resize all objects to 1000mm width (curriculum standard)
2. Replace single parquet solid with individual planks at correct widths
3. Add separating layer between insulation and screed
