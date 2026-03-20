# Lock Siting Audit — All 9 Nodes

## The Problem We Discovered

During Lock 03 (Morges) re-siting, we traced a geometric walking route from EHC Morges hospital to Gare de Morges and tried to place the lock along it. Andrea caught the flaw: **you can't site a lock by optimizing a line between two points.** A nurse finishing at 2am is not going to walk 30 minutes alone in the dark. The lock is waiting infrastructure — it needs to be where the person IS when the gap hits, not at a convenient midpoint.

**The rule**: Start from the person. Who are they, where are they at 02:00, what do they need, are they safe? Both endpoints of the connection matter. You can't tell the story of one without the other.

## What This Prompt Does

For each of the 9 relay-lock nodes, audit the siting logic by answering:

1. **Who is affected?** (specific roles — nurse, logistics driver, on-call doctor, etc.)
2. **Where are they at 02:00?** (physically — hospital ward, warehouse, hotel, home?)
3. **What transit exists during the dead window (01:30–03:30)?** Research actual Morges/Nyon/Lausanne/etc. night bus routes. Is there a shuttle? Noctambus? Nothing?
4. **What's the gap?** Not the geographic distance — the EXPERIENTIAL gap. "Shift ends at 02:00, next bus at 05:15, 3h15min of nothing" is a gap. "Shift ends at 02:00, Noctambus N2 at 02:30" is NOT a gap.
5. **Where should the lock be?** Near the origin (where people are), the destination (where they need to go), or somewhere in between? Why?
6. **What needs to be in the 3D model?** Both endpoints? The route between? Just the lock site? What context tells the story?

## The 9 Nodes

### Node 1 — Lancy-Pont-Rouge (km 4) — Border Lock
- **Lock type**: Frontalier equalization + cross-border dispatch
- **Key population**: ~160,000 frontaliers, customs/border workers
- **Key question**: Frontaliers vanish at 18:00. Who's still here at 02:00? Is this even a dead-window problem, or a different kind of gap (economic/administrative)?

### Node 2 — Geneva North Industrial Belt (km 8) — Cargo Lock
- **Lock type**: Logistics interface + pharma + airport
- **Key population**: Logistics workers, pharma distributors, airport staff
- **Key question**: Where do overnight cargo operations happen? Is the worker at a warehouse, at the airport, in a truck? Where does the chain break — is it the person who's stuck, or the goods?

### Node 3 — Nyon + Genolier (km 25) — Altitude Lock
- **Lock type**: Valley-hilltop connector + staff/patient dual use
- **Key population**: Hospital staff at Genolier Clinic (hilltop), patients
- **Key question**: 200m elevation drop between Genolier and Nyon station. Is there a shuttle? Do staff drive? If someone can't drive (patient, junior staff), what happens at 02:00? The altitude IS the gap — not time, but topology.

### Node 4 — Morges (km 48) — Temporal Lock ← ACTIVE, NEEDS FIX
- **Lock type**: Dead window shelter (01:07–04:01) + Nine Hours Hotel model
- **Key population**: ~450 night workers, EHC Morges hospital staff
- **Key questions already identified**:
  - Is there a night bus from EHC Morges? (MBC network)
  - Does the nurse wait at the hospital or go somewhere?
  - Should the lock be near the hospital (where they ARE) or near the station?
  - Is the 30min walk safe? Is it even realistic?
  - Hospital is NOT in the current 3D model (terrain tile stops 50m short)
- **Current model state**: Terrain tile 2527-1151, buildings 3D (1,127), lock at local (-60, 0, 381.5). Hospital at ~LV95 (2527800, 1152050) — just outside northern edge.

### Node 5 — Crissier-Bussigny-Ecublens (km 58–62) — Logistics Engine
- **Lock type**: Machine room exposed as civic infrastructure
- **Key population**: Logistics/distribution workers (Crissier = major logistics hub)
- **Key question**: This is a LOGISTICS node. The "person" might be a truck driver, a warehouse worker. They're at the distribution center, not at a train station. Where does THEIR chain break at 02:00? Do they even use public transit?

### Node 6 — Lausanne CHUV (km 65) — Gradient Dispatcher ← HAS 3D MODEL
- **Lock type**: Dispatcher + income-transport paradox corrector
- **Key population**: ~13,000 CHUV employees, students, patients
- **Key question**: CHUV is ON the metro (M2). Does M2 run at 02:00? If not, staff are stuck on a steep hill (slope = the gradient). The lock might need to solve the VERTICAL gap (hill) not just the temporal gap. Where are the night staff coming FROM? Residences? Other hospitals?
- **Current model state**: Lock 05 built at v3, has site context.

### Node 7 — Vevey (km 80) — Gap Relay
- **Lock type**: Intermediate lock (Panama water-saving basin analogy)
- **Key population**: Tourism/hospitality workers (resort town)
- **Key question**: 13km gap from nearest node. Who's in Vevey at 02:00? Hotel night staff? Nestlé shift workers? Where do they live, and can they get home?

### Node 8 — Montreux-Glion (km 85) — Altitude Lock
- **Lock type**: Funicular base + family/rehab access
- **Key population**: Rehab patients, clinic staff, families visiting
- **Key question**: Glion funicular schedule. Does it run at night? If a family member needs to visit a patient in Glion at 02:00, what happens? The altitude is the constraint — same as Nyon-Genolier but steeper.

### Node 9 — Rennaz (km 89) — Bridge Lock ← HAS 3D MODEL
- **Lock type**: Off-rail corrective (2.1km from Villeneuve station)
- **Key population**: Rennaz hospital (Hôpital Riviera-Chablais) staff
- **Key question**: The hospital is 2.1km from the station. Same problem as Morges but shorter distance. Is there a shuttle? What's the walk like at 02:00? Is it safe (highway environment)?
- **Current model state**: Lock 07 built at v3, has site context.

## How to Execute

### Phase 1: Transit research (for all 9 nodes)
For each node, find:
- Night bus/Noctambus routes serving the area (TPG, TL, MBC, VMCV, TPC networks)
- Last departure and first departure during weekday dead window
- Any institutional shuttles (hospitals often run their own)
- Walking distance + time from key institutions to nearest transit stop
- Safety assessment (lighting, pedestrian infrastructure, isolation)

### Phase 2: Siting re-evaluation
For each node, produce a one-paragraph siting rationale:
- Where the affected person IS at 02:00
- What they need (shelter, coordination, transport, safe waiting)
- Where the lock should be sited, and WHY
- What the 3D model needs to show (both endpoints? route? context radius?)

### Phase 3: Model corrections
For the 3 nodes with existing models (Morges, CHUV, Rennaz):
- Flag if the current siting is wrong
- Specify new SITE_ORIGIN if needed
- Specify terrain tile extensions if needed
- Specify any missing context (hospital building not in model, key road not shown, etc.)

## Output Format

For each node, a card:

```
NODE [N] — [Name] — [Lock Type]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PERSON: [who, where at 02:00]
TRANSIT: [what exists during dead window]
GAP: [the actual experiential gap]
SITING: [where the lock should be + why]
MODEL NEEDS: [what the 3D model must show]
STATUS: [correct / needs revision / not yet modeled]
```

## Key References
- Dead window: 01:30–03:30 (weekdays). Last train Lausanne 01:28, first return 03:32.
- Architecture doc: `output/app_architecture/ARCHITECTURE_DESIGN_DOC.md`
- v2 paper: `deliverables/A04/city101_vertical_transport_research_v2.md`
- Node scoring: see architecture doc Section "Scoring Engine"
- Existing lock scripts: `output/city101_hub/rhino_scripts/lock_*.py`
- Terrain/context data: `output/city101_hub/` (terrain, context, site_modeling)
