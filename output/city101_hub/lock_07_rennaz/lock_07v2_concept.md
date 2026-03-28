# Lock 07 v2 — "The Night Line"

## The Problem
HRC Rennaz hospital (2,500 staff, 180,000 catchment, 24/7 ER) is a mobility island.
2.1km from Villeneuve CFF — the only rail connection. Route 9 cantonal highway
between them is hostile to pedestrians. No sidewalks, truck traffic, unlit at night.

Bus 201 dead window: 23:53 to 05:45 = **5h 52m with zero transit**.
200-300 night shift workers stranded every night. No shuttle exists.

## The Lock Concept
The lock doesn't eliminate the gap. It **inhabits** it.

Following the canal lock sequence:
1. **Entry** — Station Chamber at Villeneuve CFF
2. **Sealing** — Protected corridor separates walker from Route 9
3. **Equalization** — Highway Chamber at the Route 9 crossing (the threshold between rail-world and hospital-world)
4. **Level-matching** — Gradual descent toward hospital ground
5. **Exit** — Hospital Chamber at HRC campus

## Architecture
A 2.1km elevated timber walkway — "The Night Line" — visible from Route 9 as a lit
ribbon above the highway. At 02:00, when the corridor goes dark, this line stays on.

### Walkway Spine (LOD 200)
- GL24h timber columns every 12m, 4.5m above ground
- CLT deck, 3m clear width (stretcher-capable, two-way)
- Partial timber canopy (weather protection)
- Lighting integrated into handrails
- 175 structural bays across 2.1km

### Station Chamber — Villeneuve CFF (LOG 400)
- Platform-level connection to Simplon line trains
- Heated waiting room (the dead-window dwelling space)
- GA tap-in as entry ritual (genkan threshold)
- Bike parking, info displays, vending
- 7-layer timber frame walls (276mm, Deplazes p.428)

### Highway Chamber — Route 9 Crossing (LOG 400)
- Longest span (~40m clear over Route 9 + shoulders)
- Steel-timber hybrid truss (GL28h bottom chord, steel tension rods)
- Widened deck (6m) with rest alcove, seating, views
- The "equalization" moment — you're suspended between two worlds
- Glazed wind barriers (see the corridor you're crossing)

### Hospital Chamber — HRC Rennaz (LOG 400)
- Arrival hall at bridge level (+4.5m)
- Switchback ramp (6% grade, SIA 500) descending to hospital ground
- Stretcher-rated elevator to emergency entrance
- Staff entrance vestibule
- 7-layer timber frame walls

## Key Numbers
- Corridor length: 2,100m
- Walking time: 25-30 min (15-18 min with moving walkway sections)
- Elevation: ~375m ASL throughout (flat Rhone delta)
- Deck height: +4.5m above ground (clears Route 9)
- Width: 3m walkway, 6m at chambers
- Structural bay: 12m (GL24h columns, CLT deck)
- Material: Swiss timber (GL24h/GL28h glulam, CLT, larch cladding)

## Route (local coords, E-2560000 / N-1137000)
Waypoints:
1. Villeneuve CFF: (1500, 500)
2. Route du Simplon south: (1100, 400)
3. Route 9 crossing: (700, 350)
4. Rennaz village: (400, 250)
5. HRC entrance: (200, 100)

## Model Strategy
- Full 2.1km at LOD 200 (walkway spine)
- 3 chambers at LOG 400 (full construction assemblies)
- Real terrain from swissALTI3D + extended flat for Villeneuve area
- Real buildings + roads from swisstopo GeoJSON
- Target: ~600-800 objects
