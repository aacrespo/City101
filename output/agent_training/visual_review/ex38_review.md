# Ex38: Timber Joist Floor
Source: Deplazes p.463

## Object Inventory
Total objects: 10

- Joist_1_SpruceC24: 1000x120x200mm (spruce_C24)
- Joist_2_SpruceC24: 1000x120x200mm (spruce_C24)
- SoundInsulation_1_MineralWool: 1000x190x200mm
- SoundInsulation_2_MineralWool: 1000x380x200mm
- SoundInsulation_3_MineralWool: 1000x190x200mm
- CounterFloor_DiagonalBoarding: 1000x1000x20mm
- ImpactSoundBattens: 1000x1000x40mm
- Floorboards_TongueGroove: 1000x1000x24mm
- Particleboard_WoodCement: 1000x1000x15mm
- BattensBelow_Timber: 1000x1000x24mm

## Comparison

### Layer order: MATCH
### Proportions: MATCH
### Assembly logic: MATCH
- Individual timber joists (2 at 120mm wide, 200mm deep) correctly modeled as discrete members
- Mineral wool insulation fitted between joists (3 pieces filling the gaps) — correct assembly pattern
- Counter floor boarding on top of joists
- Impact sound battens layer
- Tongue-and-groove floorboards on top
- Particleboard and battens below for ceiling finish

This is the strongest model so far — individual structural members with infill between them.

### Issues:
1. Floorboards should be individual planks at LOG 300-400 (T&G boards, ~120mm wide), not one solid
2. Counter floor described as "diagonal boarding" — could show individual boards
3. No separating layer between insulation zones

## Verdict: WARN

Good structural articulation — individual joists with infill insulation is correct LOG 300 practice. Finish layers (floorboards, boarding) need individualization for full LOG 300-400. Cleanest model in the batch — no duplicate geometry issues.
