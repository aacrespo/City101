# Coordination Log — Lock 07 Rennaz Bridge Lock

## Decisions (chronological)

### Site Agent — Context build (2026-03-27)
Built 8 objects across 2 layers:
- **Lock_07::Terrain** (1 object): 200x200m flat terrain plane at Z=374.0m (Context_Terrain_Ground, terrain_grass)
- **Lock_07::Ground::Site** (7 objects):
  - Context_Route9_Road — 8m wide asphalt road running E-W, Y=-10 to -2
  - Context_Railway_Simplon — 2m wide ballast strip at Y=-60 to -58 (Simplon line)
  - Context_Building_HRC_Hospital — 40x30m, 12m tall, concrete (north, Y=55-85)
  - Context_Building_Villeneuve_CFF — 16x7m, 6m tall, masonry (south, Y=-55 to -48)
  - Context_Building_Residential_W — 10x15m, 9m tall, rendered masonry (west)
  - Context_Building_Commercial_E — 15x15m, 8m tall, steel cladding (east)
  - Context_Building_Residential_NW — 8x12m, 7m tall, rendered masonry (northwest)
- All objects named with "Context_" prefix, material metadata set via UserText
- SITE_ORIGIN = (200, 300, 374.0) used for all placement
- Terrain is essentially flat (374m) matching real Rennaz conditions

### Structure Agent — Structural skeleton (2026-03-27)
Built 121 objects across 5 layers:
- **Lock_07::Ground::Foundation** (49 objects): 22 pad footings (600x600x400mm, concrete_C30), 22 steel shoes (200x200x150mm, steel_S355), 4 strip footings (400mm wide x 400mm deep, concrete_C30), 1 ground slab (200mm, concrete_C30)
- **Lock_07::Structure::Columns** (22 objects): 10 bridge columns + 12 station columns (200x200mm GL24h, Z=0.0 to 4.0)
- **Lock_07::Structure::Beams** (30 objects): 11 bridge deck beams + 4 station deck beams (140x320mm) + 11 bridge roof beams + 4 station roof beams (140x280mm)
- **Lock_07::Structure::Slabs** (12 objects): 10 bridge CLT deck panels (160mm) + 1 station floor CLT (200mm) + 1 station roof CLT (160mm)
- **Lock_07::Structure::Bracing** (8 objects): 8 steel tension rods (Ø16mm pipes, steel_S355) in 4 bays x 2 faces

[structure] Coordination Geometry Published:
- Column positions: Bridge at Y=[-24,-12,0,12,24] x X=[-2.5,2.5]; Station at Y=[-42,-37,-33] x X=[-5.5,-2.5,2.5,5.5]
- Deck beam top: Z=4.000
- CLT deck top (bridge): Z=4.160
- CLT floor top (station): Z=4.200
- Roof beam top: Z=8.000
- CLT roof top (station): Z=8.160
- Station footprint: X=-6 to 6, Y=-45 to -30
- Bridge footprint: X=-3 to 3 (CLT), columns at X=+-2.5, Y=-30 to 30
- Foundation bottom: Z=-0.800

### Envelope Agent — Walls, windows, doors, roof (2026-03-27)
Built 245 objects across 11 active layers:
- **Lock_07::Shell::Facade::Cladding** (46 objects): Larch boards (24mm) + ventilated cavity battens (40mm) on all station + hospital walls
- **Lock_07::Shell::Facade::WindBarrier** (23 objects): Bitumen softboard (18mm)
- **Lock_07::Shell::Facade::Insulation** (23 objects): Spruce studs + Isofloc (120mm)
- **Lock_07::Shell::Facade::VapourBarrier** (23 objects): Plywood (12mm)
- **Lock_07::Shell::Facade::ServiceCavity** (46 objects): Wood-cement particleboard (12mm) + service cavity battens (50mm)
- **Lock_07::Windows** (28 objects): 4 windows (2 west, 2 east), each with lintel, frame (4 pieces), glass, sill
- **Lock_07::Doors** (9 objects): Station south entrance + hospital north door (frame, leaf, lintel, threshold)
- **Lock_07::Roof::Structure** (20 objects): 40x300mm GL24h joists at 600mm centers
- **Lock_07::Roof::Insulation** (19 objects): 120mm mineral wool between joists
- **Lock_07::Roof::Membrane** (4 objects): Plywood 21mm + bitumen 7mm on station + bridge roofs
- **Lock_07::Roof::Parapet** (4 objects): 300mm larch parapet around station roof perimeter

Wall assembly: 276mm total (7 layers, inside to outside):
L7 wood-cement 12mm / L6 service cavity 50mm / L5 vapour barrier 12mm / L4 insulation 120mm / L3 wind barrier 18mm / L2 ventilated cavity 40mm / L1 larch cladding 24mm

[envelope] Coordination Geometry Published:
- Station door threshold: Z=4.200 (south wall, X=-0.45 to 0.45)
- Bridge opening at north wall: X=-3 to 3, Z=4.200 to 8.0 (full height)
- Hospital chamber: X=-3 to 3, Y=30 to 34, Z=0 to 3.5 (south side open)
- Hospital door: north wall Y=34, X=-0.5 to 0.5, Z=0 to 2.1
- Station window sills: Z=5.0, heads: Z=7.0
- Roof membrane top (station): Z=8.488
- Roof membrane top (bridge): Z=8.028
- Parapet top: Z=8.788

### Circulation Agent — Deck, ramp, elevator, guardrails, tactile (2026-03-27)
Built 156 objects across 7 layers:
- **Lock_07::Circulation::BridgeDeck** (31 objects): 10 bays x 3 layers (plywood 15mm + bitumen membrane 2mm + larch decking 40mm) + 1 lane divider. Walking surface Z=4.217
- **Lock_07::Circulation::Ramp** (24 objects): 4 switchback runs at 6.0% grade (17.57m each, 1.054m descent), 4 landings (A/B/C/Arrival), 16 GL24h support columns (200x200mm). Total descent 4.217m from bridge to ground Z=0.0
- **Lock_07::Circulation::Elevator** (9 objects): Concrete C30 shaft (200mm walls, X=-6 to -3.5, Y=30 to 32.5, Z=0 to 8.5), pit slab, roof slab, cab (1100x2100mm), 2 doors (upper Z=4.217, lower Z=0.0)
- **Lock_07::Circulation::Stairs** (5 objects): 2 concrete flights (Z=0 to 2.109, Z=2.109 to 4.217) + mid-landing + 2 steel stringers. Position X=-3.5 to -2.0, Y=30 to 34
- **Lock_07::Circulation::Guardrails** (68 objects): 50 bridge posts (80x80mm at 2.4m centers, both sides) + 2 cap rails + 6 horizontal infill rails + 8 ramp guardrail pieces (4 runs x 2 sides). Height 1100mm
- **Lock_07::Circulation::Handrails** (10 objects): 2 bridge handrails (44x44mm stainless steel, Z=5.117) + 8 ramp handrails (900mm height, 300mm extensions)
- **Lock_07::Circulation::TactileStrips** (9 objects): 1 bridge guidance strip + 2 bridge warnings + 4 ramp landing warnings + 2 elevator door warnings (5mm raised)

[circulation] Coordination Geometry Published:
- Walking surface (bridge): Z=4.217
- Ramp start: Y=30.0 (north end of bridge), Z=4.217
- Ramp arrival: Z=0.0 (ground level)
- Ramp gradient: 6.0% all runs
- Elevator shaft: X=-6.0 to -3.5, Y=30.0 to 32.5
- Elevator doors: upper Z=4.217 (south face), lower Z=0.0 (north face)
- Stair position: X=-3.5 to -2.0, Y=30.0 to 34.0
- Guardrail top (bridge): Z=5.317
- Handrail height (bridge): Z=5.161

## Interface Alerts
- Elevator shaft (X=-6 to -3.5) extends west of station footprint — envelope agent should confirm no wall conflicts
- Ramp extends north of bridge to Y~49m — near hospital context building (Y=55-85), clearance OK

### QC Agent — Review (2026-03-27)
Reviewed full model (538 objects, 28 layers) with Mode A (constraint checks) and Mode B (visual coherence).

**Mode A results:**
- A1 Object counts: ALL PASS — every layer matches expected counts
- A2 Z-levels: ALL PASS — foundation 373.2, columns 374-378, deck beam top 378, CLT 378.16, roof beam 382
- A3 Metadata: 20/20 sampled objects have name + material + thickness_mm (100%)
- A4 Wall assembly: PASS — south station wall 276mm, 7 layers correctly distributed across Facade and Walls sublayers
- A5 Known issues:
  - Shell::Walls::Station (18 objects) and Shell::Walls::Hospital (5 objects) are NOT empty — they correctly hold L4 structural studs
  - CRITICAL: Stairs start at Z=373.850 (150mm below ground), total rise 4.367m vs expected 4.217m
  - WARNING: Ramp gradient 6.2% (slightly over SIA 500 max 6.0%), arrival at Z=373.96 (40mm below ground)

**Mode B results:**
- Viewport capture shows 538 objects present; surfaces render white (no display materials assigned)
- Proportions appear correct from perspective overview

**Punch list sent to team-lead:**
- 1 CRITICAL: stair Z-coordinates (circulation-agent)
- 2 WARNINGS: ramp gradient + ramp arrival Z (circulation-agent)
- 3 NOTES: cosmetic/informational
- 7 PASS items

## Open Questions

## Round Summary
