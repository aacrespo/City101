# Object Catalog — Lock 07 Rennaz Bridge Lock
# Generated 2026-03-27

| Layer | Count | Sample Objects |
|-------|-------|----------------|
| Terrain | 1 | Context_Terrain_Ground |
| Ground::Site | 7 | Context_Building_Residential_NW, Context_Building_Commercial_E, Context_Building_Residential_W |
| Ground::Foundation | 49 | Found_GroundSlab_Station, Found_Strip_East, Found_Strip_West |
| Structure::Columns | 22 | Col_Station_Y-33_X5.5, Col_Station_Y-33_X2.5, Col_Station_Y-33_X-2.5 |
| Structure::Beams | 30 | Beam_Roof_Station_Y-30, Beam_Roof_Station_Y-33, Beam_Roof_Station_Y-37 |
| Structure::Slabs | 12 | Slab_CLT_Station_Roof, Slab_CLT_Station_Floor, Slab_CLT_Bridge_Bay10 |
| Structure::Bracing | 8 | Brace_Rod_Bay4_East, Brace_Rod_Bay4_West, Brace_Rod_Bay3_East |
| Shell::Walls::Station | 18 | Wall_Station_East_Win2Above_L4, Wall_Station_East_Win2Below_L4 |
| Shell::Walls::Hospital | 5 | Wall_Hospital_East_L4, Wall_Hospital_West_L4 |
| Shell::Facade::Cladding | 46 | Wall_Hospital_East_L1_larch, Wall_Hospital_East_L2_battens |
| Shell::Facade::WindBarrier | 23 | Wall_Hospital_East_L3_softboard |
| Shell::Facade::VapourBarrier | 23 | Wall_Hospital_East_L5_plywood |
| Shell::Facade::ServiceCavity | 46 | Wall_Hospital_East_L6_battens, Wall_Hospital_East_L7_particleboard |
| Windows | 28 | Window_Station_East_2_Sill, Window_Station_East_2_Glass |
| Doors | 9 | Door_Hospital_North_Leaf, Door_Hospital_North_Lintel |
| Roof::Structure | 20 | Roof_Joist_20, Roof_Joist_19 |
| Roof::Insulation | 19 | Roof_Insulation_19, Roof_Insulation_18 |
| Roof::Membrane | 4 | Roof_Bridge_Bitumen, Roof_Bridge_Plywood |
| Roof::Parapet | 4 | Roof_Parapet_East, Roof_Parapet_West |
| Circulation::BridgeDeck | 31 | Deck_LaneDivider, Deck_Decking_Bay10 |
| Circulation::Ramp | 24 | Ramp_Col_Run4_Mid, Ramp_Run1_Deck |
| Circulation::Stairs | 5 | Stair_Stringer_East, Stair_Flight2 |
| Circulation::Elevator | 9 | Elevator_RoofSlab, Elevator_Cab |
| Circulation::Guardrails | 68 | Guard_Ramp_Run4_Outer, Guard_Bridge_Post_* |
| Circulation::Handrails | 10 | Handrail_Ramp_Run4_Outer, Handrail_Bridge_* |
| Circulation::TactileStrips | 9 | Tactile_Elevator_Lower, Tactile_Ramp_LandingArrival |

**TOTAL: 530 objects**

## Build Summary
- **Lock**: 07 — Bridge Lock at Rennaz (km 89)
- **Program**: Timber pedestrian bridge, Villeneuve CFF → HRC Rennaz hospital
- **LOD/LOG**: 400 — full construction assemblies
- **Span**: 60m bridge (Y=-30 to 30) + station chamber (Y=-45 to -30) + hospital arrival (Y=30 to 34)
- **Key assemblies**: 7-layer timber frame walls (276mm), 4-layer bridge deck (217mm), flat roof (Deplazes p.475)
- **Structural system**: GL24h columns + beams, CLT slabs, concrete foundations
- **Circulation**: Switchback ramp (6.0% grade, 4 runs), elevator, emergency stair
- **Metadata**: 100% compliance (name + material + thickness_mm on all objects)
- **QC**: All punch list items resolved (stair Z, ramp gradient, ramp arrival)
