# Coordination Log — Lock 07 v2 "The Night Line"

## Design Concept
2.1km elevated timber walkway from Villeneuve CFF to HRC Rennaz.
3 chambers: Station (Villeneuve), Highway (Route 9 crossing), Hospital (HRC).
Full LOG 400 construction assemblies throughout.

## Route Waypoints (local coords: E-2560000, N-1137000)
1. Villeneuve CFF: (1500, 500) — Station Chamber
2. Route du Simplon: (1100, 400) — walkway spine
3. Route 9 crossing: (700, 350) — Highway Chamber
4. Rennaz village: (400, 250) — walkway spine
5. HRC entrance: (200, 100) — Hospital Chamber

## Key Datums
- Ground elevation: ~375.0m ASL throughout (flat)
- Walkway deck height: +4.5m above ground = 379.5m ASL
- Deck assembly top (walking surface): +4.717m = 379.717m ASL
- Structural bay: 12m
- Column section: 200×200mm GL24h
- Deck beam: 140×360mm GL24h
- CLT deck: 160mm
- Walkway width: 3.0m (6.0m at chambers)
- Canopy height: +7.5m above ground
- Guardrail: 1100mm (SIA 358)

## Decisions (chronological)
- [site-agent] Terrain: SwissALTI3D sampled every 20th point (25×500 grid, 12500 vertices) + flat extension at z=375m for x=1000-1700
- [site-agent] Buildings: 140 from swissTLM3D GeoJSON + 14 manual Villeneuve massing + 4 landmarks (HRC, wing, pharmacy, parking) = 158 total
- [site-agent] Roads: 220 from swissTLM3D GeoJSON + Route 9 lofted surface (8m wide) + 4 manual Villeneuve streets = 225 total
- [site-agent] Railway: 2 track curves + ballast bed surface + Villeneuve platform + canopy = 5 objects
- [site-agent] Building heights estimated by footprint area: >2000m²→15m, >500m²→10m, >100m²→8m, else→5m

## Interface Alerts
- Terrain tile covers x=0-1000 only. Extension x=1000-1700 is flat at 375m — no topographic detail for Villeneuve area.
- Railway alignment is approximate (manual waypoints). Real Simplon line position may differ by 50-100m.

## Open Questions
- Terrain for Villeneuve area needs real data (currently flat extension)
- Railway alignment is approximate — verify against swisstopo
- Walkway modeled spine = 1,239m; full corridor including chambers + approaches ≈ 1.5km in model; real route is 2.1km (difference due to straight-line segments vs road-following path)

## QC Results
- 1 CRITICAL fixed: station window positions (X/Y swap)
- Metadata: 100% compliance (name + material)
- All ramps at 6.0% SIA 500
- All Z-levels verified correct
- Chamber-spine skip zones clean

## Final Build Summary
- **Total: 3,087 objects** across 36 layers
- Build time: ~65 minutes
- Team: 5 building agents + QC + lead coordinator
- v2 saved: lock_07_v2.3dm

## Round Summary
### Round 1 — Site Context
- **site-agent**: 390 objects across 4 layers (Terrain: 2, Buildings: 158, Roads: 225, Railway: 5)
- Layers: Lock_07v2::Terrain, Lock_07v2::Context::Buildings, Lock_07v2::Context::Roads, Lock_07v2::Context::Railway
- All objects named and tagged with material/source UserText

### Round 2 — Chambers
#### Station Chamber (station-agent)
- **233 objects** across 8 sublayers under Lock_07v2::Chamber_Station
- Center: (1500, 500), footprint 15×10m, Z=375.0 to 382.96m
- **Foundation** (13): 8 pad footings 600×600×400mm, 4 strip footings, 1 ground slab
- **Structure** (24): 8 GL24h columns ground→deck, 4 roof columns deck→roof, 5 deck beams 140×360, 5 roof beams 140×280, CLT deck + roof slabs
- **Walls** (16 structural stud layers): 4 walls with openings — 120mm timber studs + Isofloc
- **Facade** (96): 6 non-structural layers per wall section (larch cladding, ventilated cavity, softboard wind barrier, plywood vapour barrier, service cavity, wood-cement particleboard)
- **Windows** (20): East 2×2m lake view, 2× South 1.2×1.5m flanking doors, North 3×2m panoramic — each with lintel/sill/frame/glass
- **Doors** (16): 2× South entrance 900×2100 from platform, 1× West double door 1500×2500 to walkway — each with frame/leaf/threshold
- **Roof** (32): 25 joists 40×300 at 600mm c/c, insulation, plywood deck, bitumen membrane, 4 parapets
- **Circulation** (16): 2-flight stair (platform 376.0→walkway 379.717) with stringers/treads/landing/guardrails, elevator shaft (4 concrete walls + 2 doors + cab)
- All objects named StaCh_* with material UserText tags
- Walkway connection: west wall opening at Z=379.0–382.5 with double door, aligned toward spine

### Round 3 — QC Review (qc-agent)
- **3,477 total objects** across 36 layers (vs 3,087 expected — 390 surplus from duplicate context layers)
- Duplicate layers found: Context::Buildings, Context::Roads, Context::Railway, Terrain each appear twice in Rhino layer table — inflating count by ~390
- Station Windows anomaly: 15 of 20 window objects positioned at ~(495-505, 1494-1506) instead of near station center (1500, 500) — coordinates appear swapped/mirrored
- All Z-levels verified correct: terrain 375.0, columns 375.0-379.140, beams 379.140-379.500, deck top 379.717
- Hospital ramp gradient: all 4 runs confirmed at 6.0% (after accounting for 160mm deck thickness)
- Highway truss: 40m clear span confirmed, no columns in X=680-720 zone
- Walkway skip zones: PASS — no spine columns within 30m of any chamber center
- Metadata: 100% name compliance, 100% material compliance, 70% thickness (context objects lack thickness, as expected)
- See QC Punch List sent to team-lead for full findings
