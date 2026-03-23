# Ex40: Vittone Semi-Prefab Hollow Block (Hourdis)
Source: Vittone, Batir

## Object Inventory
Total objects: 24 (includes duplicates from two modeling attempts)

Three size variants (A, B, C) representing different hourdis block depths:
- Variant A: blocks 450x500x120mm, ribs 100x500x120mm, topping 1000x500x40mm
- Variant B: blocks 250x500x180mm, ribs 100x500x180mm, topping 600x500x40mm
- Variant C: blocks 250x500x260mm, ribs 100x500x260mm, topping 600x500x40mm

Duplicate set with slightly different dimensions (Block_ prefix vs HollowBlock_ prefix):
- A: 470 vs 450, B: 270 vs 250, C: 270 vs 250, ribs: 80 vs 100

## Comparison

### Assembly logic: MATCH
- Individual hollow blocks modeled as discrete elements — correct!
- Concrete ribs between blocks — correct!
- Concrete topping over blocks — correct!
- Three depth variants showing different hourdis configurations — excellent for comparison
- This is exactly what LOG 300-400 demands: individual structural components, not abstracted solids

### Issues:
1. Duplicate geometry: two full sets with slightly different dimensions (appears to be two modeling attempts)
2. No finish layers modeled (tiles, screed, insulation) — only structural zone
3. Only 500mm depth instead of 1000mm curriculum standard
4. Block internal voids not modeled (hourdis blocks are hollow)

## Verdict: WARN

Significant improvement over Ex30/31 — individual blocks and ribs are modeled, which is the core LOG 300-400 requirement. However: (1) duplicate geometry needs cleanup, (2) finish layers missing, (3) block internal voids should be shown. The three-variant comparison is a nice touch showing different hourdis depths.
