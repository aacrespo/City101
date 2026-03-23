# Ex36: Composite Metal-Concrete Slab Floor
Source: Deplazes p.461

## Object Inventory
Total objects: 9 (includes duplicates from earlier attempt)

Key objects (1000mm set):
- SteelBeam_HEA200: 1000x200x190mm (steel_HEA200)
- MetalSheeting_SteelTrapezoidal: 1000x1000x1mm (profiled steel sheet)
- ConcreteTopping_ReinforcedConcrete: 1000x1000x150mm
- ImpactSound_MineralWool: 1000x1000x20mm
- Screed_Cement: 1000x1000x60mm
- Magnesite_Flooring: 1000x1000x10mm

Duplicate set (500mm): ProfiledSheeting, ImpactSoundInsulation, MagnesiteFlooring

## Comparison

### Layer order: MATCH
### Proportions: MATCH
### Assembly logic: MATCH (partially)
- Steel beam (HEA200) + profiled steel sheeting + concrete topping = correct composite floor principle
- The defining feature (steel-concrete composite action) is represented

### Issues:
1. Duplicate geometry (500mm orphans from earlier attempt)
2. Profiled steel sheeting at 1mm is flat — should show trapezoidal profile (corrugated shape). At LOG 300-400, the profile shape should be modeled, not a flat sheet
3. No shear studs/connectors modeled between steel and concrete (LOG 400 detail)
4. Individual magnesite tiles not modeled

## Verdict: WARN

Assembly logic correct — the composite system (steel + profiled sheeting + concrete topping) is present. Needs: remove duplicates, model trapezoidal sheeting profile, individualize floor finish.
