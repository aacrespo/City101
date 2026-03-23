# Ex31: Hourdis Hollow Block Floor
Source: Deplazes p.456

## Object Inventory (current model)
| Layer | Object | Size (mm) | Material |
|-------|--------|-----------|----------|
| PlainClayTiles | PlainClayTiles_Ex31 | 1000 x 500 x 10 | clay_tile |
| PlainClayTiles | PlainClayTiles_Ex31 | 500 x 500 x 10 | plain_clay_tile |
| TileAdhesive | TileAdhesive_Ex31 | 1000 x 500 x 2 | adhesive |
| TileAdhesive | TileAdhesive_Ex31 | 500 x 500 x 2 | tile_adhesive |
| Screed | Screed_Ex31 | 1000 x 500 x 80 | cement_screed |
| Screed | Screed_Ex31 | 500 x 500 x 80 | cement_screed_UFH |
| ImpactSoundInsulation | ImpactSoundInsulation_Ex31 | 1000 x 500 x 20 | mineral_wool |
| ImpactSoundInsulation | ImpactSound_Ex31 | 500 x 500 x 20 | mineral_wool |
| HourdisBlock | HourdisBlock_Ex31 | 1000 x 500 x 230 | hourdis_hollow_block |
| HourdisBlock | HourdisBlock_Ex31 | 500 x 500 x 230 | hourdis_hollow_block |
| SoffitPlaster | SoffitPlaster_Ex31 | 500 x 500 x 10 | gypsum_plaster |
| PlasterSoffit | PlasterSoffit_Ex31 | 1000 x 500 x 10 | gypsum_plaster |

Total objects: 12

## Comparison against Deplazes p.456

### Layer order: MATCH
- Layers stacked in correct order: tiles > adhesive > screed > impact sound > hourdis block > soffit plaster
- Thicknesses correct (10, 2, 80, 20, 230, 10 mm)

### Proportions: MATCH
- Layer thicknesses dimensionally correct
- Hourdis zone (230mm) correctly thicker than Ex30's hollow clay block (220mm)

### Assembly logic: MISMATCH (critical)
- The Deplazes drawing (p.456, Fig. 2) shows hourdis blocks fitted between reinforced concrete beams with lattice beam reinforcement
- The model has the hourdis zone as solid blocks (one 1000x500mm and one 500x500mm) with no individual hourdis elements or concrete ribs
- A section cut through this floor type should reveal individual hourdis blocks (with their characteristic shape), concrete fill between them, and lattice beam reinforcement

### Anomaly: Duplicate geometry
- Every layer has TWO objects at different sizes (1000x500 and 500x500) — appears to be two modeling attempts overlapping
- Inconsistent material metadata between duplicates (e.g., "clay_tile" vs "plain_clay_tile", "adhesive" vs "tile_adhesive")
- Soffit plaster split across two different layer names (SoffitPlaster and PlasterSoffit)

### Missing elements (LOG 300-400 requirements):
1. **Individual hourdis blocks** — the defining structural element, absent
2. **Concrete ribs/beams** between hourdis blocks — absent
3. **Individual clay tiles** with grout gaps — absent
4. **Separating layer** (PE sheet) — absent
5. **Lattice beam reinforcement** visible in the Deplazes drawing — absent

### Extra elements:
- Duplicate geometry at 500x500mm size (appears to be orphaned earlier attempt)

## Verdict: FAIL

Same fundamental issue as Ex30: LOG 200 abstraction, not LOG 300-400. The structural zone is solid blocks instead of individual hourdis elements between concrete ribs. Additionally, the model has duplicate/overlapping geometry from what appears to be two modeling attempts, creating a messy state. The duplicates have inconsistent metadata.

### Required rework:
1. Remove duplicate 500x500mm geometry (or the 1000x500mm set — pick one canonical size of 1000x1000mm as per curriculum spec)
2. Replace single HourdisBlock solid with individual hourdis elements and concrete ribs
3. Replace single tile layer with individual tiles with grout gaps
4. Add separating layer
5. Standardize material metadata across all objects
