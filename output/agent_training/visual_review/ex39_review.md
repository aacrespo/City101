# Ex39: Steel Floor
Source: Deplazes p.464

## Object Inventory
Total objects: 10 (includes duplicates)

Key objects (1000mm set):
- SteelBeam_HEB200: 1000x200x200mm (steel_HEB200)
- ConcreteSlab_ReinforcedConcrete: 1000x1000x200mm
- ImpactSound_MineralWool: 1000x1000x20mm
- Screed_Cement: 1000x1000x60mm
- Magnesite_Flooring: 1000x1000x10mm

Duplicate set (500mm): SteelBeam_HEB200_Ex39, ConcreteSlab_Ex39, Screed_Ex39, ImpactSoundInsulation_Ex39, MagnesiteFlooring_Ex39

## Comparison

### Layer order: MATCH
### Proportions: MATCH
### Assembly logic: MATCH (partially)
- Steel beam (HEB200) supporting concrete slab — correct principle
- Only 1 steel beam modeled (should be 2 for a 1000mm strip at typical beam spacing)

### Issues:
1. Duplicate geometry (500mm orphans from earlier attempt) — persistent pattern
2. Only 1 beam in 1000mm width — typical steel floor has beams at 2-3m spacing, but in a detail model strip, should show relationship between beam and slab more clearly
3. Magnesite flooring should be individualized

## Verdict: WARN

Correct assembly principle. Remove duplicates and individualize finish. The duplicate geometry pattern (500mm vs 1000mm sets on different layer names) is a recurring issue across modeler-4's exercises.
