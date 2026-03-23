# Ex35: Hollow-Core Concrete Slab Floor
Source: Deplazes p.460

## Object Inventory (current model)
| Layer | Object | Size (mm) | Material |
|-------|--------|-----------|----------|
| Linoleum | Linoleum_Ex35 | 1000 x 500 x 5 | linoleum |
| Linoleum | Linoleum_Ex35 | 500 x 500 x 5 | linoleum |
| Screed | Screed_Ex35 | 1000 x 500 x 80 | cement_screed |
| Screed | Screed_Ex35 | 500 x 500 x 80 | cement_screed_UFH |
| ImpactSoundInsulation | ImpactSoundInsulation_Ex35 | 1000 x 500 x 40 | mineral_wool |
| ImpactSoundInsulation | ImpactSound_Ex35 | 500 x 500 x 40 | mineral_wool |
| HollowCoreUnit | HollowCoreUnit_Ex35 | 1000 x 500 x 200 | precast_prestressed_concrete |
| HollowCoreUnit | HollowCoreUnit_Ex35 | 500 x 500 x 200 | precast_prestressed_concrete |
| BondingCoat | BondingCoat_Ex35 | 1000 x 500 x 2 | bonding_agent |
| BondingCoat | BondingCoat_Ex35 | 500 x 500 x 2 | bonding_agent |
| SoffitPlaster | SoffitPlaster_Ex35 | 500 x 500 x 10 | gypsum_plaster |
| PlasterSoffit | PlasterSoffit_Ex35 | 1000 x 500 x 10 | gypsum_plaster |

Total objects: 12

## Comparison against Deplazes p.460

### Layer order: MATCH
- Correct order: linoleum > screed > impact sound > hollow-core unit > bonding coat > soffit plaster
- Thicknesses match spec: 5, 80, 40, 200, 2, 10 mm

### Proportions: MATCH
- Hollow-core unit at 200mm (within 120-300mm range)
- All layer thicknesses correct

### Assembly logic: MISMATCH (critical)
- The Deplazes drawing (p.460) clearly shows the **hollow cores** — circular/oval voids running longitudinally through the precast slab. This is THE defining feature of this floor type.
- In section, you see: solid concrete webs between hollow tubes, creating a distinctive profile that is immediately recognizable
- The model has the hollow-core unit as a **solid block** (1000x500x200mm / 500x500x200mm) with NO internal voids
- Without the voids, a section cut cannot distinguish this from a solid concrete slab (Ex32) — defeating the purpose of the exercise
- At LOG 300-400, the circular voids must be modeled as boolean cuts through the slab

### Anomaly: Duplicate geometry
- Same issue as Ex31: every layer has TWO objects at different sizes (1000x500 and 500x500)
- Inconsistent material metadata between duplicates
- Soffit plaster split across two different layer names

### Missing elements (LOG 300-400 requirements):
1. **Hollow cores (voids)** — the defining feature, completely absent. Should be circular/oval boolean cuts visible in section
2. **Individual precast units** — hollow-core slabs are placed as individual planks side by side (visible in Deplazes isometric). In a 1000mm strip, should show at least the joint between units
3. **Grout** at joints between precast units (noted in Deplazes drawing)
4. **Separating layer** (PE sheet) between insulation and screed
5. **Bearing pad / mortar bed** at supports (noted in Deplazes drawing)

### Extra elements:
- Duplicate geometry at 500x500mm size (orphaned earlier attempt)

## Verdict: FAIL

The model fundamentally fails to represent a hollow-core slab. Without the characteristic internal voids (hollow cores), the section is indistinguishable from a solid concrete slab. The Deplazes drawing prominently shows these voids as the primary visual and structural feature. Additionally, the duplicate geometry issue from Ex31 persists.

### Required rework:
1. Remove duplicate geometry (standardize to 1000x1000mm strip per curriculum)
2. Model hollow-core unit with circular/oval void boolean cuts through the slab — this is the entire point of the exercise
3. Show joint between individual precast units
4. Add separating layer
5. Standardize material metadata and layer naming
