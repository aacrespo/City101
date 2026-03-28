# Object Catalog — Lock 07 v2 "The Night Line"
# Generated 2026-03-27

## Summary
- **Lock**: 07 — Rennaz Hospital Island (km 89)
- **Program**: 2.1km elevated timber walkway, Villeneuve CFF → HRC Rennaz
- **LOD/LOG**: 400 throughout — full construction assemblies
- **Total objects**: 3,087 across 36 layers
- **Build time**: ~65 minutes (Phase 1: 53 min, Phase 2: 7 min, QC+fixes: 5 min)
- **Team**: 5 building agents + QC reviewer + lead coordinator

## Object Breakdown

| Component | Objects | Description |
|-----------|---------|-------------|
| **Site Context** | **390** | |
| Terrain | 2 | SwissALTI3D mesh (25×500 grid) + flat extension |
| Buildings | 158 | 140 swissTLM3D + 14 Villeneuve massing + 4 landmarks |
| Roads | 225 | 220 swissTLM3D + Route 9 surface + 4 Villeneuve streets |
| Railway | 5 | 2 Simplon tracks + ballast + Villeneuve platform + canopy |
| **Walkway Spine** | **1,894** | |
| Columns | 214 | 107 bays × 2 columns (200×200 GL24h) |
| Beams | 107 | 140×360mm GL24h deck beams |
| Deck | 412 | CLT 160mm + plywood 15mm + membrane 2mm + larch decking 40mm |
| Canopy | 424 | 120×120 columns + 100×200 beams + CLT 80mm panels |
| Guardrails | 420 | 80×80mm posts + 50×50mm cap rails |
| Handrails | 214 | 44×44mm timber, 900mm height |
| Lighting | 103 | Integrated handrail strips |
| **Station Chamber (Villeneuve CFF)** | **233** | |
| Foundation | 13 | Pad + strip footings + ground slab |
| Structure | 24 | GL24h columns + beams + CLT slabs |
| Walls | 16 | 120mm structural stud layer (L4) |
| Facade | 96 | 6 finish layers per wall section (276mm total assembly) |
| Windows | 20 | East lake view + South platform + North panoramic (5-part each) |
| Doors | 16 | 2 platform entrances + 1 walkway double door |
| Roof | 32 | Joists + insulation + membrane + parapets |
| Circulation | 16 | 2-flight stair (376→379.7m) + elevator shaft |
| **Highway Chamber (Route 9 Crossing)** | **266** | |
| Foundation | 8 | Approach column footings |
| Structure | 74 | GL28h approach columns + 40m hybrid truss (chords + posts + tension rods) |
| Deck | 50 | CLT 200mm + surface layers + rest alcove benches |
| Windows | 122 | 62 steel mullions + 60 glass wind barrier panels |
| Guardrails | 12 | Cap rails + canopy panels |
| **Hospital Chamber (HRC Rennaz)** | **304** | |
| Foundation | 32 | Pad + strip footings + ground slabs |
| Structure | 38 | GL24h columns + beams + CLT slabs |
| Walls | 21 | 120mm structural stud layer |
| Facade | 114 | 6 finish layers (arrival hall + vestibule) |
| Windows | 20 | 4 windows × 5-part assembly |
| Doors | 8 | Staff entrance 1200mm + ER access 1500mm |
| Roof | 16 | Flat roof assemblies (arrival + vestibule + ramp tower) |
| Ramp | 31 | 4 switchback runs at 6.0% + landings + guardrails |
| Elevator | 14 | Concrete shaft + cab + 2-level doors |
| Tactile | 10 | Warning strips at landings + elevator |

## Key Dimensions
- Corridor length: ~2.1km (1,239m spine + 3 chambers)
- Ground elevation: 375.0m ASL
- Walking surface: 379.717m ASL (+4.717m above ground)
- Canopy: 382.5m ASL (+7.5m above ground)
- Structural bay: 12m
- Walkway width: 3m (6m at chambers)
- Highway span: 40m clear over Route 9
- Hospital ramp: 4.717m descent at 6.0% grade (4 runs)
- Station stair: 3.717m rise (platform to walkway)

## Material System
- Structure: GL24h / GL28h Swiss glulam
- Slabs: CLT 5-ply (160mm walkway, 200mm highway)
- Walls: 7-layer timber platform frame (276mm, Deplazes p.428)
- Cladding: Larch boards 24mm
- Wind barriers: Insulated glass 24mm in steel frames
- Foundations: Concrete C30
- Decking: Larch anti-slip 40mm

## QC Results
- Metadata compliance: 100% (name + material on all objects)
- SIA 500 ramp compliance: PASS (6.0% all runs)
- Z-level alignment: PASS (all datums verified)
- Chamber-spine connections: PASS (skip zones clean)
- 1 critical fix applied (station window positions)
