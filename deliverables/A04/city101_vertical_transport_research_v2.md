# The Horizontal Elevator — A Relay-Lock Prototypology for the 101km Healthcare Corridor
## Research v2 for City101 — "Still on the Line"

**Date:** 2026-03-17 (v2)
**v1:** 2026-03-10
**Purpose:** Map concepts from vertical transportation systems onto the horizontal elevator / relay-lock typology. v2 integrates the full healthcare supply chain (46,000-48,000 workers), multimodal transport data (29,135 trips), and a quantitative node selection methodology.

---

## 0. Abstract

The Geneva-Villeneuve rail corridor sustains **81,900 healthcare jobs** — 17.2% of Canton Vaud's entire economy. At any given night, **8,000-10,000 healthcare workers** are on shift across hospitals, nursing homes, home care, and logistics. Between 01:30 and 03:30 on weekday nights, they have **zero public transport**.

This paper proposes a network of **9 relay-lock chambers** — architectural interventions at critical break points along the 101km corridor — that function as a single horizontal elevator. Each chamber manages the threshold between two states (day/night, visible/invisible, rail/off-rail, valley/hilltop, border/corridor) using principles derived from vertical transportation systems: the canal lock, the destination dispatch elevator, the paternoster, the sky lobby, and the relay station.

The 9 nodes are selected through a quantitative scoring framework applied to 24 candidate sites, evaluated across 5 criteria: night worker count, healthcare chain criticality, modal collapse severity, gap distance, and infrastructure readiness. The result is not 9 separate buildings but one distributed machine — remove a node and the chain breaks.

---

## 1. Taxonomy of Vertical Transportation Systems

### 1.1 What each system teaches the chamber

| System | How it works | Key concept for the chamber |
|--------|--------------|-----------------------------|
| **Traction elevator** (geared/gearless) | Motor + sheave + counterweight. Steel ropes. Discrete trips, on-demand. Dwell 3-5s per floor. Industry wait target: 20s. | Sealed box, sensory disconnection. You enter one world and exit another. The transition is invisible. |
| **Hydraulic elevator** | Piston pushes from below. Low-rise only (max ~6 floors). No overhead machine room. Slower, simpler, cheaper. | Not every connection needs the same infrastructure. Some gaps are small and need simple solutions. |
| **Machine-room-less (MRL)** | Motor embedded in the shaft wall — no dedicated machine room. Saves 10% building footprint. | The mechanism can be invisible. The chamber IS the machine. No "back of house" needed. |
| **Double-deck elevator** | Two cabs stacked vertically, serving odd/even floors simultaneously. Passengers pre-sorted by floor parity in the lobby. | One shaft, two programs. Parallel processing of different user types in the same infrastructure. |
| **Destination dispatch** (Schindler PORT, ThyssenKrupp TWIN) | Passengers select destination BEFORE entering. System groups by destination, assigns a specific car. No buttons inside. | Pre-sorting changes the lobby from anxious to certain. The intelligence is in the dispatch, not the cab. |
| **Paternoster** | Continuous chain of open compartments in a vertical loop. Never stops. User must jump on in sync with the machine. Invented 1866 (Peter Ellis). | Continuous flow vs. discrete trips — two fundamentally different philosophies. The user synchronizes with the machine, not the other way around. |
| **Funicular** | Two cars on a single track, counterbalanced by cable. One goes up as the other comes down. Fixed route, fixed gradient. | The connection creates twin settlements. Valley town + hilltop town become functionally interdependent. |
| **Cable car / gondola** (La Paz, Medellín) | Aerial transit over terrain that resists surface infrastructure. Cabins as mobile micro-rooms. 30,000 pax/hr in La Paz. | When the ground doesn't cooperate, you leave it. Each cabin is a miniature chamber in motion. |
| **Inclined elevator** | Oblique movement — neither purely vertical nor horizontal. Follows terrain. | The real-world gap is rarely purely one axis. Nyon→Genolier is an inclined elevator problem. |
| **Rack railway** (Riggenbach, Abt, Strub) | Toothed rail engages a cogwheel for steep grades (up to 48%). Three tooth systems for different gradients. | The infrastructure must match the gradient. Different gaps need different teeth. |
| **Moving walkway / travelator** | Horizontal belt or pallet system. Speed assist only. No enclosure, no threshold moment. | **Negative example:** speed assist alone doesn't create a chamber experience. The chamber needs enclosure, transition, threshold. |
| **MULTI** (ThyssenKrupp) | Rope-free, linear induction motor. Multiple cabins circulate in loops — up one shaft, across horizontally, down another. Each cabin autonomous. Prototype in Rottweil since 2017. | The building becomes a network, not a stack. Cabins are autonomous agents. Increases usable area 25-30%. Eliminates single-path constraints. |
| **Ship lock / canal lock** | Chamber fills/empties to equalize water levels. Vessel enters, gates close, water level changes, gates open on the other side. 5 stages. | The occupant is stationary; the SPACE transitions around them. Gates enforce directionality. The dwell time IS the mechanism. |

### 1.2 Swiss vertical transport precedents

| System | Location | What it teaches |
|--------|----------|-----------------|
| **Lausanne M2** | Ouchy (373m) → Epalinges (711m) | World's steepest metro. 338m rise in 6km. 12% max gradient. Fully automated. Proves a short steep connection can unify a vertically stratified city. |
| **Fribourg funicular** | Lower town → Upper town | Running since 1899. Powered by wastewater — no motor. 2,700 litres fill a tank at top; weight difference drives the system. An economic necessity that became heritage. |
| **Bern Marzili** | Aare river → Bundeshaus | 105m of track, 1M pax/year, since 1885. Connects leisure zone to institutional zone. A 105-meter "elevator" between two completely different urban programs. |
| **Biel-Magglingen** | Biel → Magglingen/Macolin | Links bilingual city to isolated hilltop settlement in the Jura. Without it, Magglingen ceases to function as part of Biel. |
| **Glion-Rochers-de-Naye** | Montreux → Glion → summit | **Directly relevant — this IS Node 8.** Funicular stops at night. Creates the mountain↔lake split that defines the Montreux health ecosystem. |

### 1.3 Hospital vertical transport

Hospitals operate **three segregated vertical systems**:

1. **Staff circulation** — standard elevators, card-access restricted, shift-change peaks
2. **Patient/bed transport** — oversized cabs (2.4m deep minimum), slow speed, smooth acceleration, priority override for emergencies (one button clears all other calls)
3. **Logistics** — clean supply goes up one shaft, dirty/waste goes down another. Automated guided vehicles (AGVs) handle 300-2,000 carts/day. Pneumatic tubes at 7.6 m/s for lab samples, blood, pharmaceuticals (Swisslog systems)

**Key principle:** These three circulations share a building but NEVER mix. Clean/dirty, urgent/scheduled, staff/patient — each has its own path.

**Translation to corridor:** The healthcare circuit has the same three systems — staff access, patient access, cargo logistics — sharing the same rail infrastructure. But the full supply chain research reveals a **fourth circulation**: home care workers who traverse the corridor in network patterns, not point-to-point trips (see 1.6).

### 1.4 The bus as paternoster

The v1 paper was rail-blind. The corridor's actual continuous loop is the **bus network**.

Vernier-Blandonnet has **168 departures in 2 hours** (84/hr) — the highest transit frequency in the entire corridor. Every single departure is bus or tram. Zero trains. The 29,135-trip transport map (v2) reveals that buses outnumber trains roughly **30:1** in total trip count.

The bus is the corridor's paternoster: high-frequency, low-capacity per vehicle, continuous, and spread across the surface. The train is the elevator: discrete trips, high-capacity, on-demand scheduling. The critical difference: **the bus paternoster stops completely on weekday nights.** There is no Noctambus Monday through Thursday. The paternoster goes silent, and only the skeleton elevator schedule (last trains ~00:30, first trains ~04:30) remains — then nothing.

The chamber must interface with bus networks, not just rail platforms. A relay-lock at Morges (Node 4) that ignores the MBC bus hub fails to connect to the actual majority of daily movements.

### 1.5 The boat as parallel corridor

**9 stations** along the corridor have CGN (Compagnie Générale de Navigation) boat access: Geneva, Coppet, Nyon, Rolle, Morges, Cully, Vevey, Montreux, Villeneuve. That is nearly 1 in 5 corridor stations with lake access.

The lake is a **second shaft** running parallel to the rail shaft. It offers a lateral alternative — slower, scenic, seasonal (reduced winter service), but architecturally significant. For patient transport, every lakeside hospital (HUG, GHOL Nyon, EHC Morges, HRC Rennaz) has a CGN landing within walking distance.

The boat does not operate at night. But during summer, it provides partial redundancy for the rail corridor's daytime gaps. And the CGN landings themselves — piers, waiting shelters, embarkation points — are existing threshold architectures that the relay-lock could absorb or extend.

### 1.6 The funicular as altitude lock — and the home care traversal

Four corridor stations have funicular access:
- **Lausanne** — M2 metro (Ouchy 373m → Epalinges 711m)
- **Vevey** — Funicular to Chardonne/Mont-Pèlerin
- **Montreux/Territet** — Funicular to Glion, then rack railway to Rochers-de-Naye
- **Territet** — Direct funicular to Glion

Each creates a **twin-settlement dependency**: valley town + hilltop town functionally unified by the cable. When the funicular stops at night, the hilltop settlement is severed. Genolier (NStCM narrow gauge, last train ~21:29) is the most severe case — 150 night clinic staff, car-only after 21:29.

**The missing operating hours table:** The v1 paper cited funiculars as precedents but never mapped which ones along the corridor stop at night. This is a critical data gap — the funicular operating hours are the "lock gates" for vertical access, and they are undocumented in our datasets.

**Home care circulation — a new transport type:** AVASAD (5,000 employees, 90% field-based) and IMAD (2,300 employees) represent a fundamentally different movement pattern. Home care workers do not commute point-to-point. They **circulate** — making 6-10 stops per shift across multiple communes. IMAD confirms a dedicated night team (EMD de nuit) on route 20:00-01:00.

This is neither paternoster (scheduled loop) nor elevator (on-demand point-to-point). It is a **traveling network traversal** — closer to the MULTI system, where autonomous cabins move through the building network without a fixed route. The chamber must accommodate this fourth circulation: not origin-destination but waypoint logic.

---

## 2. Organizational Concepts for the Chamber

### 2.1 The Lock Sequence

A canal lock operates in **five stages**:

```
1. ENTRY        →  vessel arrives from one level
2. SEALING      →  gates close behind it
3. EQUALIZATION →  water level changes (gravity, no pumps)
4. LEVEL MATCH  →  chamber reaches the other side's level
5. EXIT         →  gates open, vessel proceeds
```

**Panama Canal (2016 Neopanamax locks):** 3 lateral water-saving basins per chamber store water at intermediate elevations, recycling 60% of the transition medium. A **stepped equalization cascade** — the transition isn't binary but graduated.

**Canal du Midi:** 91 locks including the Fonserannes staircase — 8 consecutive chambers rising 21.5m. Riquet switched from rectangular to ovoid chambers after a wall collapse: architecture responding to forces.

**Leonardo da Vinci** invented the mitre gate for Milan canals — gates that cannot open until pressure equalizes. A built-in safety mechanism: the architecture prevents premature transition.

**Application to the chamber:**

Each node's chamber follows the lock sequence:

| Stage | What it means at the chamber |
|-------|------------------------------|
| **Entry** | Arrive from one state (night shift ends, last train missed, cargo delivered) |
| **Sealing** | The chamber closes around you (shelter, warmth, information, safety) |
| **Equalization** | The chamber adjusts your state (rest, food, connection to next mode, psychological decompression) |
| **Level matching** | You're now ready for the other side (first bus arrives, shuttle dispatched, cargo sorted) |
| **Exit** | Leave into the new state (home, next shift, hospital, delivery destination) |

**The dwell time IS the architecture.** Like a lock, the chamber's value is proportional to how well it manages the wait — not how fast it eliminates it.

### 2.2 Destination Dispatch

**Schindler PORT (2009):** Passengers enter destination on a touchscreen in the lobby. The system groups people heading to similar floors, assigns them to a specific car, displays the assignment on a screen. No buttons inside the car. Results: 30% fewer stops, reduced wait/travel time, no lobby crowding.

**Evolved from Miconic 10 (1992)** — the first destination dispatch system. Research now uses reinforcement learning and genetic algorithms for real-time optimization.

**The key shift:** Intelligence moves from the cab to the lobby. The cab becomes dumb transport; the lobby becomes the smart interface.

**Application to chamber:** The chamber knows who is coming and where they need to go:

> A night nurse finishes at CHUV at 01:30, needs to reach Renens. The chamber dispatches: **"Shared ride with 3 others heading to Prilly/Renens. Bay 2, departing 01:45."**

Pre-sorting eliminates the worst part of the dead window: not the wait itself, but the **uncertainty** of whether anything is coming. Destination dispatch converts anxiety into scheduled certainty.

### 2.3 Paternoster vs. Elevator

| | Paternoster | Elevator |
|---|-------------|----------|
| **Schedule** | Continuous — always moving | On-demand — responds to calls |
| **User behavior** | Synchronize with the machine | The machine synchronizes with you |
| **Wait time** | Zero (but you must time your entry) | Variable (press button, wait) |
| **Capacity model** | Low per-cabin, high aggregate | High per-cabin, lower aggregate |
| **Philosophy** | The system never stops for you | The system exists to serve your request |

**The corridor already contains both:**
- **Paternoster** = high-frequency bus/tram in Geneva/Lausanne (show up, one comes in 1-3 minutes)
- **Elevator** = IC express (you plan your trip around a specific departure)
- **Dead window (01:30-03:30 weekdays)** = both systems stop. The paternoster goes silent and the elevator has zero cabs running.

**The weekday/weekend split is fundamental.** Friday and Saturday nights, the Noctambus provides a partial paternoster (38 trips, 9 routes, mostly Geneva canton). Monday through Thursday: nothing. Healthcare workers — who work 7 days — experience two different corridors depending on the day. The chamber must be designed for the weekday case, when the system is at its absolute emptiest.

**Application:** During the weekday dead window, the chamber creates its own paternoster-like continuous availability — not a fixed schedule (impossible with low volume) but a sense that the system is always awake. On-demand shuttles, aggregated shared rides, or simply a well-lit, warm, connected space that communicates: "you are not stranded."

### 2.4 Sky Lobby

In supertall buildings, express elevators take you to a **sky lobby** (transfer floor), then local elevators distribute you to individual floors. This reduces shaft count in the tower core by ~40%.

**Application:** Three stations function as sky lobbies — redistribution hubs where corridor-scale movement breaks into local networks:

| Sky lobby | Modes | Role |
|-----------|-------|------|
| **Geneva** (Node 1-2) | 7 modes, Shannon 1.95 | Western anchor. CEVA/Léman Express cross-border. CGN boat. |
| **Lausanne** (Node 6) | 8 modes, Shannon 2.08 | Central anchor. M2 metro, bus, CGN, funicular. Highest modal diversity. |
| **Vevey** (Node 7) | 7 modes, Shannon 1.95 | Eastern relay. Funicular, CGN, VMCV bus, IR stop. Bridges the Lavaux Fracture. |

The other 6 nodes are "local elevator" stops. The chamber at a sky lobby is fundamentally different: higher throughput, more modes converging, more complex dispatch logic.

### 2.5 Relay Station Architecture

**Pony Express (1860-1861):** 157 stations across 3,100km. Two types:
- **Swing stations** — pure handoff. Rider dismounts, fresh horse saddled, rider remounts. Under 1 minute. Minimal structure: a corral, a trough, a roof.
- **Home stations** — rest and recovery. Every 100-160km. Full program: bunkhouse, kitchen, stable, blacksmith.

**Caravanserai (6th c. BCE → 17th c. CE):** Relay/rest stations spaced one day's journey apart (~30-40km). Standard program: rectangular courtyard, vaulted gallery, rooms on 1-2 levels, imposing entrance portal. UNESCO inscribed **56 Persian caravanserais as a single network** — not individual buildings.

**Application to the 9 nodes:**

| Node type | Corridor nodes | Dwell character |
|-----------|---------------|-----------------|
| **Swing station** (quick handoff) | Geneva North (Node 2), Crissier-Bussigny-Ecublens (Node 5) | Cargo transfer, logistics interface. Minutes, not hours. |
| **Home station** (rest/recovery) | Morges (Node 4), Montreux-Glion (Node 8) | Night shelter, waiting, capsule rest. Hours (the full dead window). |
| **Sky lobby** (redistribution) | Lausanne CHUV (Node 6), Vevey (Node 7) | Multi-modal interchange, dispatch, gradient navigation. |
| **Border station** | Lancy-Pont-Rouge (Node 1) | Cross-border threshold. Frontalier equalization. |
| **Altitude station** | Nyon-Genolier (Node 3) | Valley-hilltop connector. Vertical access management. |
| **Terminus** | Rennaz (Node 9) | Bridge/corrective. The gap that shouldn't exist. |

Like the caravanserai network: **the value is in the system, not any individual node.** 9 chambers spaced along 101km averages ~11km between nodes — comparable to caravanserai spacing scaled for motorized travel.

### 2.6 Threshold Chambers — Airlock, Narthex, Genkan

Three precedents for the chamber as transition space between two states:

**Airlock (spacecraft, submarines, hospitals)**
- Two doors, never both open simultaneously
- Gradual pressure transition — prevents shock
- **Asymmetric timing**: lock-in is fast (minutes), lock-out/decompression can take hours
- Variants: cascading (flow from critical to less critical), pressure bubble (positive to both sides), pressure sink (negative for containment)
- **Chamber lesson:** Entry is quick (night shift ends, you're in). Exit may require waiting (equalization with the next mode). The asymmetry is the design.

**Narthex (church architecture)**
- Threshold between secular exterior and sacred interior
- Functions: climatic buffer, gathering space, psychological preparation, social filter
- Byzantine theology: narthex = earth, nave = heaven, sanctuary = divine
- Double narthex (esonarthex + exonarthex): graduated transition through multiple thresholds
- **Chamber lesson:** The chamber prepares you for a state change. Leaving a night shift is not the same state as arriving home. The narthex is where the shift from "professional" to "personal" begins.

**Genkan (Japanese entrance)**
- Ground-level foyer (stone/tile) with a raised wooden platform into the home
- Shoe removal = ritual marking the boundary: "you leave the outside world at the threshold"
- Dates back 1,000+ years. The step is both physical and psychological.
- **Chamber lesson:** The GA tap-in COULD be a genkan moment — a ritual marking "you are now in the corridor's care." Currently invisible. The chamber could make this threshold legible and meaningful.

### 2.7 Adaptive Architecture — Cedric Price

**Fun Palace (1961-1972, unbuilt)**
- Commissioned by Joan Littlewood for the Theatre Royal, Stratford East
- A structural framework with daily reconfigurable components: movable walls, floors, ramps, stages, screens, sound systems
- "Behaviour would be unstable, indeterminate, and unknown in advance"
- Planned obsolescence — intended for dismantling after 10 years
- Directly influenced the Centre Pompidou

**Generator (1976-1979, unbuilt)**
- 150 mobile 12'×12' cubes on a grid
- The building "knew itself" and readjusted to users' desires
- Key innovation: the computer could **"become bored and induce changes"** if users weren't changing anything
- Considered the first conceived "intelligent building"

**Price's philosophy:** "Questioned architecture's identification with building alone, instead proposing a time-based approach conceived as a series of interventions that were both adaptable and impermanent."

**Application to chamber:**
- **Time-adaptive:** co-working by day, social space by evening, shelter by night, logistics interface at 03:00
- **Programmatically uncertain:** built for 10-15 years until the corridor's identity solidifies enough to warrant permanent architecture
- **Self-reconfiguring:** if a program goes unused (like Generator's "boredom"), the space shifts. Data-driven: ridership patterns, shift schedules, and usage sensors drive reconfiguration.

### 2.8 Home Care Circulation — A New Transport Type

AVASAD (Canton Vaud, 5,000 employees) and IMAD (Canton Geneva, 2,300 employees) together field **7,300 home care workers**, 90% of whom are field-based. They do not commute to a fixed workplace. They **traverse** the corridor — making insulin injections, wound care visits, palliative care checks across multiple communes per shift.

IMAD confirms a dedicated **EMD de nuit** (night home care team) and workers on route until 01:00. AVASAD confirms evening/night visits for insulin, wound care, and palliative patients.

This is a fundamentally different circulation from the three hospital types (staff, patient, cargo). Home care workers are:
- **Mobile**: moving between 6-10 locations per shift
- **Distributed**: covering communes, not confined to a building
- **Time-sensitive**: visits are scheduled around patient needs (insulin timing, palliative windows)
- **Dependent on traversal infrastructure**: they need the corridor to be permeable, not just connectable between two points

The Pony Express swing station is the closest architectural analogy: a waypoint where the rider (home care worker) regathers — restocks supplies, warms up, checks the next route, connects to updated dispatch. The chamber serves as a **field base**, not a terminus.

---

## 3. The Koolhaas Frame

### The elevator as anti-architecture

From *Delirious New York* (1978): The elevator, with steel frame + electricity + air conditioning, created "another species of architecture." The **1909 Theorem**: once the elevator meets the steel frame, "any given site can now be multiplied ad infinitum." Each floor becomes independent — connected only by "the common data of elevators, service cores, columns and external envelope."

From *S,M,L,XL* (1995), "Bigness": "The elevator — with its potential to establish mechanical rather than architectural connections — and its family of related inventions render null and void the classical repertoire of architecture. Issues of composition, scale, proportion, and detail are now moot."

### The Downtown Athletic Club

Koolhaas's key case study: a "Constructivist Social Condenser" where each level describes a different "performance" — 7th floor = golf course, 9th = boxing + oyster bar, 10th = Turkish bath, 12th = swimming pool. The elevator enables this **layering of wildly different programs** that would be impossible if connected by stairs or ramps.

### Translation to corridor

**The train is anti-urban** in the same way the elevator is anti-architectural. It creates mechanical connections between communes, making each station-commune independent. The 49 stations are 49 "floors" stacked horizontally, connected only by the common data of rail, electricity, and schedule.

**But like the Downtown Athletic Club:** the 9 lock-chambers should embrace programmatic discontinuity. Lancy-Pont-Rouge (border equalization) has no reason to resemble Montreux-Glion (altitude medicine). They share DNA (lock sequence, threshold logic, dispatch intelligence) but their programs are as different as a golf course and a Turkish bath.

### Social hierarchy inversion

| Era | Vertical (building) | Horizontal (corridor) |
|-----|---------------------|-----------------------|
| **Before the technology** | Wealthy live low (easy access). Poor live high (walk-up garrets). | Proximity to Geneva/Lausanne = premium. Distance = friction. |
| **After the technology** | Elevator inverts: penthouse = premium. Height = status. | GA inverts: Lavaux/Montreux = desirable. The whole corridor is "one floor." |
| **When the technology stops** | Power outage: upper floors are trapped. Hierarchy re-inverts. | **01:30-03:30 weekday dead window**: distance = disadvantage again. The inversion fractures — but only on weekdays. Friday/Saturday, Noctambus provides partial coverage. The collapse is temporal AND calendrical. |
| **The border dimension** | N/A — buildings don't cross borders. | **7,200 frontalier healthcare workers** exist in permanent partial inversion. Swiss wages, French transit. At 02:00, a French nurse leaving HUG faces a double inversion: no Swiss transit AND no French transit. The border is an elevator shaft with no cab. |

**The chamber is the architecture that keeps the inversion working 24 hours, 7 days.** It's the emergency generator for the horizontal elevator.

---

## 4. Translation Table — Vertical → Horizontal

| Vertical concept | Horizontal corridor equivalent |
|-----------------|-------------------------------|
| Elevator shaft | Rail line (101km) |
| Floor / landing | Station-commune |
| Penthouse (premium top) | Lavaux / Montreux (scenic, desirable with GA) |
| Basement / service floor | Crissier-Bussigny (invisible logistics) |
| Machine room | Switching yards, substations, signal infrastructure |
| Elevator cab | Train car (IC = luxury cab with WiFi/tables; S-Bahn = utility cab) |
| Elevator lobby | Station concourse / the chamber |
| Sky lobby (transfer floor) | Lausanne / Geneva / Vevey (redistribution hubs) |
| Destination dispatch | Pre-sorting by IC/IR/S tiers; chamber dispatch during dead window |
| Paternoster (continuous loop) | High-frequency bus/tram (show up and go) |
| Elevator (discrete trip) | IC express (plan your trip, wait for departure) |
| Counterweight | Return trip — for every nurse going home, a fresh shift arrives |
| Emergency override | Priority transport for medical emergencies |
| Clean/dirty separation | Staff ↔ patient ↔ cargo routing in the chamber |
| Double-deck (two cabs, one shaft) | Two corridors on the same tracks (IC + S-Bahn) |
| Funicular twin settlement | Valley town + hilltop (Nyon + Genolier, Montreux + Glion) |
| Lock chamber | The chamber — space where transition happens |
| Lock equalization | Dwell time — the wait that enables connection |
| Lock gates | Operating hours — the "gates" that open/close the corridor |
| Lock safety (mitre gate) | Architecture that prevents premature transition (you can't leave until you're ready) |
| Panama water-saving basins | Stepped equalization — intermediate states between origin and destination |
| Airlock asymmetry | Fast entry to chamber, slow exit (wait for next mode) |
| Narthex | Psychological preparation space — professional → personal |
| Genkan ritual | GA tap-in as legible threshold marking |
| MULTI (rope-free, multi-directional) | Network of 9 nodes — connections aren't single-path |
| Fun Palace adaptivity | Chamber reconfigures: day ≠ evening ≠ night ≠ 03:00 |
| Generator "boredom" | Data-driven program shifts when usage patterns change |
| Swing station (Pony Express) | Quick-handoff nodes (Geneva North, Crissier-Bussigny) |
| Home station (Pony Express) | Rest/recovery nodes (Morges, Montreux-Glion) |
| Caravanserai network | The 9 chambers as one UNESCO-style inscription — the system, not the parts |
| Bus network | The paternoster the corridor already has — 84 dep/hr at peak, 0 on weeknights |
| CGN boat (lake corridor) | Second shaft — lateral redundancy, seasonal, daytime only |
| Funicular operating hours | Lock gates for altitude — when the funicular stops, the hilltop is severed |
| Narrow gauge feeder (NStCM, MOB, TPC) | Branch tubes extending the corridor's reach into valleys and hilltops |
| Home care circulation | MULTI-style network traversal — autonomous agents with no fixed route |
| Frontalier crossing | Cross-shaft transfer — the cab crosses between buildings (countries) |
| Guard pharmacy (on-call) | Emergency override with surcharge — architecture of last resort |
| Blood bank at M2 terminus | Critical resource on an inaccessible floor during power outage |

---

## 5. The Corridor Breaks — A Quantitative Analysis

### 5.1 Five Dimensions of Breaking

Every station along the 101km corridor has been scored across five break dimensions:

| Dimension | What it measures | Scoring |
|-----------|-----------------|---------|
| **Transit break** | Trains per hour below threshold, wait time above 15 min | Severity 0-3 |
| **Workspace break** | No coworking/library within walkable distance | Severity 0-3 |
| **Connectivity break** | No WiFi within walkable distance | Severity 0-3 |
| **Amenity void** | Zero workspace AND zero WiFi (complete desert) | Boolean |
| **Mobility break** | No shared mobility (bikes/scooters) | Boolean |

**Results across 49 stations:**

| Classification | Count | Description |
|----------------|-------|-------------|
| **TOTAL RUPTURE** | 3 | All dimensions fail. St-Saphorin (0 trains, WCI 0.0003), Denges-Echandens (2 tr/hr), Perroy (3 tr/hr, 0 shared mobility) |
| **MAJOR** | 35 | Most infrastructure missing. Includes Aigle, Bussigny, Bex, St-Prex, Rivaz, Lancy-Bachet, Territet |
| **MODERATE** | 5 | Mixed. Vernier-Blandonnet (84 tr/hr but no workspace), Renens, Allaman |
| **MINOR** | 3 | Infrastructure present but with gaps. Coppet, Versoix, Rolle |
| **CONTINUOUS** | 11 | Fully integrated. Geneva, Lausanne, Vevey, Morges, Montreux, Nyon, Gland, Lausanne-Flon, Villeneuve, Genève-Sécheron, La Tour-de-Peilz |

**Only 11 of 49 stations (22%) maintain full working continuity.** The corridor is 78% broken.

### 5.2 Three Permanent Geographic Gaps

Three gaps persist at **all hours of the day** — they are structural, not temporal:

| Gap | Distance | Stations inside | Worst WCI | Why it matters |
|-----|----------|----------------|-----------|----------------|
| **Nyon → Gland** | 19.3 km | Founex (0.014), Coppet (0.066), Tannay (0.150), Mies (0.030) | 0.014 | Start of the 23km no-ER zone (Nyon to Morges) |
| **Gland → Morges** | 20 km | Rolle (0.097), Perroy (0.011), Allaman (0.084), St-Prex (0.016) | 0.011 | La Côte's blind spot — 51,800 scattered residents |
| **Lavaux Fracture** | 17.5 km | Grandvaux (0.016), Cully (0.063), Epesses (0.041), Rivaz (0.013), St-Saphorin (0.0003) | 0.0003 | UNESCO constraints prevent road expansion. The fracture is permanent. |

The Lavaux Fracture is not a temporal problem that "opens" during rush hour. Even at peak, St-Saphorin has 0 trains. The fracture is **geologically determined** — the same terrain that makes the landscape UNESCO-worthy makes it transit-hostile.

### 5.3 The Healthcare Overlay

Layering the healthcare supply chain research onto the break point data reveals four critical failures:

**Layer 1 — Emergency Response:**
- **23 km with no Emergency Room** between Nyon (km 25) and Morges (km 48). Ambulance response for this zone comes from CSU Nyon (GHOL) and CSU Morges-Aubonne (EHC), meeting somewhere around Rolle.
- **20 km with no ambulance base** in the Lavaux section (km 63-82). Winding roads, steep terrain. Estimated response time: 20-25 minutes from either direction.
- Night crew reductions: SIS Geneva 3→1 caserne, Riviera 3-4→2 crews, SPSL Lausanne staffing crisis (1/3 absent 2023-24).

**Layer 2 — Staff Access:**
- **ZERO weekday night public transport** for 8,000-10,000 healthcare workers on shift.
- CHUV alone: 2,500-3,000 per night (12,844 employees, ~5,257 nurses across 24h services, 3 rotations).
- HUG: 3,000-4,000 per night (13,086 employees, 60% of nurses from France).
- Night taxi costs: Morges-Nyon CHF 55, Lausanne-Vevey CHF 80, Nyon round trip CHF 110.

**Layer 3 — Supply Chain:**
- All 8 supply chains (medication, food, staff, patients, postal, lab samples, waste, emergency) are **100% road-dependent** during the dead window.
- Swiss Post "Innight Medica" delivers to 220+ hospital operating theaters by 06:00 — entirely by truck.
- Emergency blood delivery protocol at 03:00: **unclear** (not documented by any hospital).

**Layer 4 — Facility Access:**
- **1 true 24h pharmacy** (Pharma24 at HUG, Geneva) for the entire 101 km.
- Pharmacie 24 in Lausanne closes at midnight despite its name.
- 55 km from Morges to Villeneuve: ZERO pharmacy access overnight.
- Guard pharmacy on-call system: CHF 17.30-50.00 surcharge, phone-based.

### 5.4 The Bus Blind Spot

The daytime modal diversity at most stations is a **nighttime illusion**.

| Station | Daytime modes | Daytime dep/2hr | Night modes | Night dep/2hr |
|---------|--------------|----------------|-------------|---------------|
| Vernier-Blandonnet | 4 (rail, tram, bus, Léman Express) | 168 | ~1 (last rail) | ~2-3 |
| Lausanne | 8 (rail, metro, bus, boat, funicular...) | 57 | ~1 (last rail) | ~4-5 |
| Morges | 5 (rail, bus, boat, shared bikes) | 32 | ~1 (last rail) | ~3-4 |
| Nyon | 6 (rail, bus, NStCM, boat, shared bikes) | 29 | ~1 (last rail) | ~2-3 |

The modal diversity that makes a station feel "well-connected" by day evaporates at night. A station with 6 modes during the day may function as a 1-mode station (or 0-mode) after midnight. The 42× frequency variation between Lausanne (28.5 tr/hr) and St-Saphorin (0.0 tr/hr) is structural — it persists at every hour across all 7 measured time slots.

**IC trains collapse 44% from peak to late night** (128 → 72 departures corridor-wide). The "workable corridor" (IC + workspace access) contracts to 13 stations by 11pm — and then to zero at 01:30.

---

## 6. Node Selection Methodology

### 6.1 Scoring Framework

To move from intuitive to data-driven node selection, we apply 5 criteria to all 24 candidate horizontal elevator sites:

| Criterion | Weight | What it measures | Data source | Scoring |
|-----------|--------|-----------------|-------------|---------|
| **Night worker count** | 25% | People stranded during dead window | Hospital employment data, night shift ratios, 24-site mapping | 0-5 (per 500 workers) |
| **Healthcare chain criticality** | 25% | What breaks if this node fails | Healthcare gap analysis (4 layers), supply chain research | 0-5 (severity of chain break) |
| **Modal collapse severity** | 20% | Ratio of daytime modes to nighttime availability | Modal diversity data, temporal frequency | 0-5 (higher = worse collapse) |
| **Gap distance** | 15% | km to nearest functional node in each direction | Break point data, geographic gap analysis | 0-5 (per 5km of gap) |
| **Infrastructure readiness** | 15% | Existing modes, shared mobility, transit frequency to build on | Modal diversity, station break points | 0-5 (existing infrastructure quality) |

### 6.2 Scoring the 24 Sites

| Rank | Site | km | Night workers | HC criticality | Modal collapse | Gap distance | Infra readiness | Total | Tier |
|------|------|----|--------------|----------------|----------------|-------------|-----------------|-------|------|
| 1 | **Lausanne CHUV Perpendicular** | 65 | 5 (2,500-3,000) | 5 (blood bank, EMS bottleneck, psychiatric) | 4 (8→~1 modes) | 3 (24km to Rennaz) | 5 (8 modes, M2) | **4.55** | CRITICAL |
| 2 | **Morges Hospital Gap** | 48 | 3 (550 stranded) | 5 (23km no-ER zone, last ER heading east) | 4 (5→~1 modes) | 5 (20km gap each direction) | 4 (5 modes, CGN) | **4.30** | CRITICAL |
| 3 | **Crissier-Bussigny-Ecublens** | 58-62 | 4 (1,680 night) | 5 (single pharma hub for Romandie, PLEXUS) | 3 (transit strong but no night) | 2 (near Lausanne) | 4 (bus, rail) | **3.90** | CRITICAL |
| 4 | **Rennaz Hospital Island** | 89 | 3 (400 night) | 5 (only hospital for 190k catchment, off-rail) | 4 (4 bus lines, 0 nocturnal) | 4 (2.1km off-rail, end of corridor) | 2 (bus-only, no rail) | **3.85** | CRITICAL |
| 5 | **Lancy-Pont-Rouge** | 4 | 3 (1,200 night + 7,200 frontalier) | 4 (border gateway for 60% HUG nurses) | 3 (5→~1 modes) | 2 (Geneva well-served) | 5 (CEVA, tram, shared bikes) | **3.50** | CRITICAL |
| 6 | **Nyon Hospital + Genolier** | 25 | 3 (730 night) | 4 (start of 23km no-ER, hilltop clinic severed) | 4 (6→~1 modes, NStCM stops 21:29) | 4 (19.3km gap to Gland) | 4 (6 modes, NStCM, CGN) | **3.75** | HIGH |
| 7 | **Vevey Mid-Gap Relay** | 80 | 2 (moderate) | 3 (bridges CHUV-Rennaz gap, psychiatric) | 3 (7→~1 modes) | 4 (24km gap mid-point) | 5 (7 modes, WCI 0.40) | **3.25** | HIGH |
| 8 | **Geneva North Industrial** | 8 | 5 (4,600 night) | 3 (logistics workers, airport pharma) | 3 (strong transit but no night) | 1 (Geneva well-served) | 5 (84 dep/hr, excellent) | **3.45** | HIGH |
| 9 | **Montreux-Glion Altitude** | 85 | 2 (moderate) | 3 (altitude medicine, psychiatric, elderly) | 4 (7→~1 modes, funicular stops) | 3 (between Vevey and Rennaz) | 4 (7 modes, funicular, MOB) | **3.10** | HIGH |
| 10 | Lausanne Flon Nightlife | 65 | 2 (300 bar staff) | 2 (nightlife, not healthcare primary) | 3 | 1 | 5 | 2.50 | — |
| 11 | Founex-Nyon Gap | 28 | 1 | 2 | 3 | 4 | 2 | 2.30 | — |
| 12 | Gland-Rolle Gap | 38 | 1 | 2 | 3 | 4 | 3 | 2.45 | — |
| 13 | Ecublens Campus | 62 | 2 (800 night) | 2 | 3 | 1 | 4 | 2.40 | — |
| 14 | Sécheron International | 6 | 1 | 2 | 3 | 1 | 4 | 2.10 | — |
| 15-24 | Remaining 10 sites | — | 0-2 | 1-2 | 2-3 | 1-3 | 1-4 | 1.2-2.3 | — |

**The scoring produces a natural break at 3.0:** the top 9 sites cluster above this threshold, confirming a 9-node network. Below 3.0, sites are important but do not warrant a full relay-lock intervention — they are better served by lighter measures (improved bus connections, shared mobility, wayfinding).

**Key validation:** CHUV and Morges score highest, which aligns with the healthcare supply chain finding that these are where the chain most critically breaks. Rennaz's high score is driven by its extreme infrastructure deficit (bus-only, 2.1km off-rail) despite moderate night worker count.

---

## 7. The 9 Nodes — Chamber Concepts

### Node 1: Lancy-Pont-Rouge — The Border Lock (km 4)
**Lock type:** Border ↔ Corridor
**Vertical analogy:** Cross-shaft transfer — the MULTI cab that crosses between two buildings. The Léman Express (CEVA line) is the physical shaft; the border is where two building systems meet.

**Key data:** 5 modes (rail, Léman Express, tram 15, bus, shared bikes — 197 vehicles). Commuter swing 4.04× (10,100 weekday vs 2,500 weekend). 7,200 frontalier healthcare workers cross into Geneva daily. 60% of HUG nurses live in France. Last Léman Express Mon-Thu ~00:30, first ~05:00. Weekend: hourly night trains exist. 1,200 night workers in immediate zone.

**Chamber concept:** A **border equalizer** at the CEVA interchange. The frontalier nurse finishing at HUG at 01:30 faces a double dead window — no Swiss transit and no French transit. The chamber at Lancy-Pont-Rouge is the threshold where the two national transit systems meet, and where their shared failure is architecturally managed.

Destination dispatch for frontaliers: "3 others heading to Annemasse. Bay 1, departing 01:50." The genkan moment: crossing the border is currently frictionless (Schengen) but architecturally invisible. The chamber makes the crossing legible — you are leaving one transit system's jurisdiction and entering another's.

The weekday/weekend split is most visible here: on Friday/Saturday, the Léman Express runs hourly night trains through Lancy-Pont-Rouge. Monday-Thursday: nothing. The chamber's program shifts accordingly — weekend waypoint vs. weekday shelter.

**Sketch prompt:** The CEVA station's lower level, extended with a covered waiting/dispatch zone. One face toward Geneva (HUG, tram 15). The other toward France (Léman Express platform to Annemasse). A dispatch screen showing shared rides to French border communes. Warm, lit, open during the dead window.

---

### Node 2: Geneva North Industrial Belt (km 8)
**Lock type:** Cargo ↔ City
**Vertical analogy:** Freight elevator — oversized, slow, no passengers. Loading dock = lobby. But with a twist: the v2 data shows this zone has **84 departures/hr** during the day (highest on the corridor, all bus/tram). The transit is excellent. The break is not transport — it is **visibility**.

**Key data:** 4,600 night workers. ZIMEYSA/ZIMEYSAVER 380+ hectares, 500+ companies, RUBIX medical/R&D complex. Airport: 3,000 night workers. DHL 300, Post 600 (02:00-05:00), Port Franc 500. 12,000 frontaliers. 3 late-night venues. 54% car dependency despite strong transit. WCI 0.46 (MODERATE — workspace and WiFi breaks, not transit).

**Chamber concept:** A **visibility lock** — not a transport bridge (transit is strong) but an architectural device that makes the supply chain visible as civic infrastructure. Currently: pharma sorting, airport logistics, medical device assembly, postal processing. 4,600 workers, invisible to the city.

The chamber combines: a viewing gallery onto the logistics activity (the architectural equivalent of making the service elevator the main elevator), a worker amenity space (rest that logistics workers currently lack), and connection to the adjacent residential neighborhoods that pretend the warehouses don't exist.

Reframed from v1: the v1 paper proposed "worker rest pods" and "cargo lock." The v2 data shows the real problem is not transport (84 dep/hr!) but the **zero-workspace, zero-WiFi** amenity void for a zone with 4,600 night workers. The chamber creates the social infrastructure that the transport infrastructure already provides but the built environment does not.

**Sketch prompt:** A structure at the ZIMEYSA edge, where warehouse meets residential. One side: glass wall onto the sorting/distribution floor. Other side: lit entrance from the Vernier neighborhood. Between: a warm shared space (café, rest area, dispatch information, WiFi). Bus/tram stops integrated — not a new transport node but a social node on an existing transport backbone.

---

### Node 3: Nyon Hospital + Genolier Hilltop (km 25)
**Lock type:** Valley ↔ Hilltop
**Vertical analogy:** Inclined elevator / funicular — the gap is altitude, not distance. 350m elevation between lake hospital (GHOL Nyon) and hilltop clinic (Clinique de Genolier).

**Key data:** Nyon: 6 modes (Shannon 1.79), 14.5 tr/hr, CGN boat, NStCM narrow gauge to Genolier/St-Cergue. **NStCM last train ~21:29 to Genolier** — car-only after that. 730 night workers: hospital (200), industrial (300), Genolier clinic (150, hilltop, zero nocturnal transport), hotels (30). Genolier = Swiss Medical Network, joined Mayo Clinic Care Network 2025. GHOL: 6 operating theatres, heliport, SMUR base. Start of the 23km no-ER gap heading east.

**Chamber concept:** A **vertical connector** at the hinge point where flat lakeside meets steep hillside. The NStCM track defines the connection — trains run until 21:29, then the hilltop is severed. The chamber sits at Nyon station where the main line (SBB) meets the branch (NStCM), functioning as a **base camp** for the vertical journey.

Dual circulation: staff shuttle ascending (evening shift change at Genolier), patient/family transport descending (visiting hours, rehab discharge at Genolier — one of most modern radio-oncology centres in Europe).

The 23km no-ER gap starts here. Nyon's GHOL is the last emergency department heading east until Morges. The chamber must include emergency dispatch visibility — ambulance routing, SMUR status, the gap made legible.

**Sketch prompt:** Nyon station's platform, extended to bridge the SBB/NStCM interchange. A covered waiting chamber where the main line meets the branch line. One face looking down to the lake/CGN landing. The other angled up toward the NStCM track to Genolier. Dispatch screen for night shuttle to the hilltop clinic. Warm, lit, operational until the NStCM resumes at ~05:40.

---

### Node 4: Morges Hospital Gap (km 48)
**Lock type:** Last train ↔ First train
**Vertical analogy:** Night lobby — the elevator isn't coming. The lobby IS the architecture.

**Key data:** 5 modes (Shannon 1.61): rail (IR stop), MBC bus hub, CGN boat, shared bikes. 16 tr/hr, including 12 IR. First train 04:01, last train 01:07. **True dead window: 01:07-04:01 (3 hours).** 550 stranded night workers (hospital 300, industrial 250). EHC Morges hospital: 1.4km from rail, rated 3.0★ (worst on corridor). 4,750 elderly in catchment (19%). SMUR base + 2 ambulances covering Rolle to Lausanne west.

This node sits at the critical junction: last ER heading east before the 23km gap. CHUV's EMS bed blockage (36-49 beds) creates overflow pressure — patients who should be in nursing homes are stuck at CHUV, and regional hospitals like Morges absorb the spillover.

**Chamber concept:** A **temporal lock** — architecture for the 01:07-04:01 void. The purest expression of the lock-as-waiting-space. Reference: **Nine Hours Hotel** (Naruse Inokuma, Tokyo, 2019), designed explicitly for people who missed the last train. Its 4-scene sequence: (1) Reception — check in, receive minimal kit. (2) Prologue corridor — transition from public to private. (3) Sanitary lounge — wash, decompress. (4) Sleep pod — rest until morning.

For Morges: the chamber offers shelter, rest, information (countdown to first transport at 04:01), connection (WiFi, charging, dispatch screen), and critically: **pharmaceutical micro-dispensing**. Morges is 48km from the only 24h pharmacy (Pharma24 at HUG). An automated system for common medications with pharmacist video consultation addresses the single-pharmacy gap.

The MBC bus hub is Morges' real local network — not the IR trains. The chamber must interface with the bus schedule as prominently as the rail schedule.

**Sketch prompt:** A narrow, warm, lit space attached to the hospital's night entrance OR at the station where MBC buses converge. Capsule-like rest alcoves along one wall. A dispatch screen showing countdown to first transport. A pharmaceutical dispensing unit. A small kitchen counter. The 1.4km walk to the station rendered visible on a wall map with lit path guidance.

---

### Node 5: Crissier-Bussigny-Ecublens Logistics Belt (km 58-62)
**Lock type:** Invisible ↔ Visible
**Vertical analogy:** Machine room — the space that makes the building work but that no one sees. Except this machine room is the largest healthcare logistics concentration on the corridor.

**Key data:** Within this 4km belt:
- **PLEXUS-Santé** (Bussigny): Joint CHUV-HUG warehouse, 4,100 m², 58,000 boxes, 3,500 orders/day. "Possibly the most automated hospital warehouse in Europe."
- **CHUV CPA** (Bussigny): Central food production, 4,800 m², 6,800+ meals/day, 28 cold storage rooms
- **Galexis Ecublens**: Pharma distribution hub, 100,000 packs/day, **single distribution point for all of Romandie**. CHF 34M modernization 2022. ~300-400 employees at Ecublens (estimated). Pre-dawn picking starts before dawn.
- **B. Braun Crissier**: Medical device manufacturing, 350 employees, 12 million units/year
- **1,680 total night workers** across the belt. Zero nocturnal transport within 2km.

This is not a node — it is the **engine room** of the corridor's healthcare system. Geneva and Lausanne's hospital systems physically merge here in shared infrastructure. PLEXUS serves both CHUV and HUG — consumables for Geneva travel ~60 km from Bussigny.

**Chamber concept:** A **logistics exchange** — the v1 paper proposed a "civic window" (viewing gallery onto sorting activity). The v2 data demands more: this is where all 8 supply chain flows (medication, food, staff, patients, postal, lab samples, waste, emergency) converge physically before diverging. The chamber makes this convergence architecturally legible and provides the 1,680 night workers with what they lack: rest, food, transit information, social space.

Like the MRL (machine-room-less) elevator: the aspiration is to make the machine room disappear into the architecture. But here the opposite is proposed — make the machine room visible. The corridor's healthcare system depends on this invisible belt. The chamber argues: if you benefit from the system, you should see the system.

**Sketch prompt:** A structure straddling the boundary between the PLEXUS/Galexis logistics zone and the adjacent residential street in Bussigny/Crissier. One side: observation window onto automated sorting. Other side: warm, lit entrance from the neighborhood, bus stop integrated. Between: worker amenity space (rest, food, WiFi) and a dispatch/information wall showing real-time flows — where the pharma packs are heading, which hospital kitchens are receiving, how many medical devices shipped tonight.

---

### Node 6: Lausanne CHUV Perpendicular (km 65)
**Lock type:** Uphill ↔ Downhill
**Vertical analogy:** Sky lobby + destination dispatch — the major interchange where corridor-scale movement redistributes into local networks across a 250m gradient.

**Key data:** 8 modes (Shannon 2.08, highest on corridor). 28.5 tr/hr (highest rail frequency). **2,500-3,000 night workers per night** at CHUV alone (12,844 employees, ~5,257 nurses across 24h services, 3×8h rotations). M2 metro stops at midnight. 8,400 frontaliers. TI CRS blood bank at Épalinges (M2 terminus) — **inaccessible during dead window when M2 stops.** 24% of CHUV ambulance transfers are psychiatric (to/from Hôpital de Cery in Prilly). 36-49 beds permanently blocked by EMS placement backlog. Unisanté transferred ER to CHUV in 2024, causing 24.4% surge in ER visits.

CHUV nurses earning CHF 56,000 live in Renens/Prilly (accessible by night; 9 tr/hr late). Doctors earning CHF 95,000 live in Cour (walkable). The income-transport paradox: the people who can least afford a taxi are the ones who need it most.

**Chamber concept:** A **gradient dispatcher**. Like Schindler PORT, the chamber reads where you need to go and assigns you a mode:

| Destination | Altitude | Assigned mode |
|-------------|----------|---------------|
| Renens / Prilly (CHF 56k nurses) | ~420m | Shared shuttle, bay 1 |
| Chailly / Sallaz (mid-range) | ~550m | E-bike dock or minibus |
| Epalinges (M2 terminus, blood bank) | ~711m | Night shuttle, bay 3 |
| Cery (psychiatric hospital) | ~500m | Dedicated psychiatric transport, bay 4 |

The chamber sits at CHUV (the "sky lobby") and dispatches into the local vertical network. It eliminates the income-transport paradox by creating equity of access regardless of where on the gradient you live.

The blood bank access problem is new to v2: TI CRS headquarters at Épalinges processes 700+ mobile blood drives/year and maintains 24h blood product delivery. But its location at the M2 terminus means physical access is severed during the dead window. The chamber must include a blood logistics interface — coordinating between the TI CRS and CHUV's needs when the M2 isn't running.

**Sketch prompt:** A covered dispatch hall at CHUV's staff exit. A screen showing real-time departure assignments (like an airport gate display, but for 4-5 bays serving different gradient zones). E-bike parking integrated. Warm, lit, visible from inside the hospital. A dedicated psychiatric transport bay (discreet, calming). A pharmaceutical dispensing unit (CHUV is 65km from the only 24h pharmacy at HUG).

---

### Node 7: Vevey Mid-Gap Relay (km 80)
**Lock type:** Gap ↔ Gap
**Vertical analogy:** Panama water-saving basin — an intermediate level between two main locks. Vevey sits between CHUV (km 65) and Rennaz (km 89), bridging the 24km gap.

**Key data:** 7 modes (Shannon 1.95, tied with Geneva and Montreux). 20 tr/hr (3rd highest on corridor). CGN boat, funicular to Chardonne/Mont-Pèlerin, VMCV urban bus, IR stop. WCI 0.40 (CONTINUOUS — one of only 11 fully working stations). 75 station richness within 1km. Fondation de Nant psychiatric day centre in Vevey. Fondation de Nant stationary psychiatric facility in Montreux (nearby). 20-22% elderly in catchment (6,476 people). 4 medical facilities within 0.5km of rail.

Vevey is the **only working node** in the eastern corridor between Lausanne and Villeneuve. Everything around it breaks: La Tour-de-Peilz has only 4 tr/hr, Burier 4 tr/hr, Clarens 4 tr/hr, the Lavaux stations behind it are MAJOR breaks. Vevey is an island of function in a sea of fragmentation.

**Chamber concept:** A **gap relay** — not a primary healthcare node (no major hospital) but the intermediate lock that prevents the eastern corridor from being a 24km void between CHUV and Rennaz. Like the Panama water-saving basin that stores water at intermediate elevations, Vevey stores connectivity.

The architectural program is lighter than the primary nodes: information hub (real-time status of Rennaz bus connections, CHUV gradient dispatch, CGN boat schedule), shared mobility dispatch (e-bikes for the lakeside route to Montreux/Rennaz), connection to the funicular altitude network (Chardonne psychiatric access). The chamber doubles as a psychiatric interface — connecting Fondation de Nant's Vevey and Montreux facilities to the broader network, managing the 24% of CHUV transfers that are psychiatric.

**Sketch prompt:** Vevey station's lakeside face, extended toward the CGN landing. A slim information pavilion that connects the rail platform to the bus stops (VMCV) and the funicular entrance. Dispatch screens for three directions: west (Lausanne/CHUV, 15km), east (Montreux/Rennaz, 9km), up (Chardonne/Mont-Pèlerin, funicular). Bench seating oriented toward the lake. Lighter, smaller than the major nodes — a relay, not a destination.

---

### Node 8: Montreux-Glion Altitude Medicine (km 85)
**Lock type:** Mountain ↔ Lake
**Vertical analogy:** Funicular — literally. The existing Glion funicular IS the vertical transport mechanism; it just stops running at night.

**Key data:** 7 modes (Shannon 1.95). MOB narrow gauge (Montreux-Oberland Bernois to Interlaken/Zweisimmen), funicular to Glion/Rochers-de-Naye, CGN boat, VMCV bus, PE panoramic express. 23% elderly in Montreux catchment (highest east of Geneva, 6,137 people). Clinique Valmont rehab at 600m+ altitude (85-120 staff, 59 beds, 4.5★). Clinique CIC in Clarens. Fondation de Nant psychiatric facility (stationary, addiction). LBG hospital laundry at Chailly-Montreux (serves 30+ hospitals, 80+ EMS — a supply chain node).

The split between mountain care (Valmont rehab, private) and lakeside care (HRC Rennaz, public) is physical. The funicular creates the valley-hilltop dependency: without it, Glion/Valmont is severed from the lakeside network.

**Chamber concept:** An **altitude lock** at the funicular's base station. The existing infrastructure (funicular, track, stations) defines the connection. The architectural intervention extends the funicular's operating logic into the dead window — not by running the funicular 24h (impractical) but by creating a chamber that manages the wait and provides alternative connection.

Like the Fribourg funicular (powered by wastewater, no motor) — the intervention should be as light as possible. The mountain already provides the mechanism (gravity, gradient); the architecture just needs to make it usable at night.

The LBG hospital laundry in Chailly-Montreux is an unexpected supply chain node: 30+ hospitals and 80+ EMS facilities send their laundry here. The chamber should acknowledge this — the altitude lock manages not just people but the linen and sterilization circuit that keeps hospitals running.

**Sketch prompt:** The funicular base station, extended with a lit waiting chamber. A map showing Valmont above, HRC Rennaz below, Fondation de Nant nearby. A dispatch screen for night shuttle or shared taxi up the mountain road. The MOB connection to the Oberland visible. Bench seating oriented toward the lake view (the orientation tells you: you're at the threshold between mountain and water).

---

### Node 9: Rennaz Hospital Island (km 89)
**Lock type:** Rail ↔ Off-rail
**Vertical analogy:** The missing elevator — a building built on a floor with no elevator stop. HRC Rennaz was built in 2019, 2.1km from the nearest rail station (Villeneuve). 2.6★ rating (worst hospital on corridor). 400 night staff.

**Key data:** 4 bus lines serve Rennaz. **None are nocturnal.** 190,000 catchment population (intercantonal: Vaud + Valais — the only cross-cantonal hospital). PHEL (Pharmacie des Hôpitaux de l'Est Lémanique) with global dispensing robot, moved here October 2019. 2.75× slower by public transport than car. Proposed monorail never built. CSU-CAVD ambulance base at Rennaz.

The hospital was placed off-rail in 2019. The proposed monorail connecting it to Villeneuve station was never built. The chamber is retroactive correction — the architecture that should have existed when the hospital was placed here.

**Chamber concept:** A **bridge lock** — the lightest physical intervention in the network but the most critical corrective. The gap is simple: 2.1km of road between Villeneuve station and hospital, with no sidewalk, no lighting, no bus at night.

The chamber is not a single building but a **connective tissue**: a covered, lit, dispatched path or shuttle link connecting Villeneuve station to HRC Rennaz. The PHEL robot pharmacy is already here — making this the only node in the eastern corridor with automated pharmaceutical capability. The chamber extends that logic: if the pharmacy can automate, the transport link should too.

Like Rennaz itself, this is the corrective intervention. The architecture argues: the mistake was made in 2019; the lock fixes it retroactively. The 2.6★ rating is partly about accessibility — patients and staff rating the journey, not just the hospital.

**Sketch prompt:** A minimal covered walkway/cycle path from Villeneuve station toward HRC Rennaz. Lighting columns every 50m. A shelter at each end with dispatch information and PHEL pharmaceutical access. The path itself IS the chamber — the transition happens during the walk/ride, not in a room. At 2.1km, this is a 25-minute walk or 8-minute bike ride. The architecture makes it safe, lit, and legible at 03:00.

---

## 8. Four Design Principles

### Principle 1: The chamber manages dwell, not speed

Like a canal lock, the value is in how well it manages the wait. The equalization time is the architecture. **Don't try to make the gap disappear — design the experience of being inside it.**

The true dead window is **01:30-03:30 on weekdays** — 2 hours, not 4. That's more intense than the v1 estimate, but shorter. The remaining hours (00:30-01:30 and 03:30-05:00) have scattered service — 188 trips active in the broader window. The chamber's program must account for this granularity: shelter mode during the 2-hour absolute void, dispatch mode during the flanking hours when some service exists.

The weekday/weekend split is critical. Friday and Saturday, Noctambus provides partial coverage. Monday through Thursday: nothing. The Nine Hours Hotel and the caravanserai understood this — the architecture of waiting is the architecture of certainty. Even if the wait is long, knowing it will end is the design.

### Principle 2: Four circulations, one chamber

Hospitals use segregated vertical systems (staff, patient, cargo). The full supply chain research reveals a **fourth circulation** that the v1 paper missed:

1. **Staff** — a night nurse resting between shifts
2. **Patient** — an elderly person waiting for morning transport home
3. **Cargo** — a pharma pallet being sorted for morning delivery
4. **Home care** — an AVASAD worker regrouping between house visits, restocking supplies, checking dispatch for the next stop

These are four different "elevator programs" sharing infrastructure. The chamber keeps them legible and separate, like clean/dirty elevator shafts in a hospital. The home care circulation demands **waypoint logic**: not a terminus where you arrive and leave, but a pit stop where you resupply and continue.

### Principle 3: The network is the building

Like the caravanserai (56 buildings = 1 UNESCO inscription) and MULTI (multiple cabins = 1 system), the 9 chambers are **one horizontal elevator**. Remove a node and the chain breaks.

The Lavaux Fracture (km 72-80) is the void that proves the network thesis. It is the **anti-node** — a structural gap that no single chamber can fill (UNESCO constraints, zero trains, permanent TOTAL RUPTURE at St-Saphorin). The network routes around it: Vevey (Node 7) to the east and Lausanne (Node 6) to the west bracket the fracture. The gap is not solved — it is acknowledged and managed by the nodes on either side.

The dispatch intelligence is distributed across the network. A nurse at CHUV (Node 6) who needs to reach Morges is served by the CHUV dispatcher coordinating with the Morges shelter (Node 4). The nodes talk to each other.

### Principle 4: The bus is the invisible elevator

The v1 paper treated the corridor as a rail system. The v2 data shows it is overwhelmingly a bus system — 30:1 trip ratio. The relay-lock prototypology must interface with bus networks as prominently as rail platforms.

At Morges (Node 4), the MBC bus hub moves more people locally than the IR trains. At Nyon (Node 3), the NStCM narrow gauge is the lifeline to Genolier. At Vevey (Node 7), VMCV urban buses connect the hillside communes. At Rennaz (Node 9), buses are the *only* public transport.

Each chamber must include bus bay design, bus schedule display, and physical adjacency to bus stops — not just rail platform integration. The bus is the paternoster the corridor already has. When it stops on weekday nights, the chamber must fill its role: continuous availability through on-demand dispatch, shared rides, or simply the assurance that the system hasn't forgotten you.

---

## 9. References

### Vertical transportation
- Koolhaas, Rem. *Delirious New York* (1978). Chapter on the Downtown Athletic Club.
- Koolhaas, Rem. "Bigness, or the Problem of Large" in *S,M,L,XL* (1995).
- Schindler Group. PORT Technology — destination dispatch system (2009).
- ThyssenKrupp. MULTI — rope-free, multi-directional elevator. Rottweil test tower (2017).

### Lock systems
- Panama Canal Authority. Third Set of Locks (Agua Clara, Cocoli), water-saving basin design (2016).
- Canal du Midi, Pierre-Paul Riquet. Fonserannes staircase locks (1681).
- Da Vinci, Leonardo. Mitre gate design for Milan canals (late 15th century).

### Relay architecture
- Pony Express National Historic Trail. Station typology (swing vs. home stations).
- UNESCO. Persian Caravanserai (inscribed as a network, 2023).

### Threshold / chamber
- Hertzberger, Herman. *Lessons for Students in Architecture* — threshold theory.
- Kurokawa, Kisho. "The capsule is cyborg architecture" — Metabolist theory.
- Naruse Inokuma Architects. Nine Hours Hotel, various locations (2009-present).

### Adaptive architecture
- Price, Cedric. Fun Palace (1961-1972, unbuilt). With Joan Littlewood.
- Price, Cedric. Generator (1976-1979, unbuilt). The "bored" building.

### Swiss vertical urbanism
- Lausanne M2 metro (opened 2008). Gradient: 338m in 6km.
- Funiculaire de Fribourg (1899-present). Wastewater-powered.
- Bern Marzilibahn (1885-present). 105m, 1M pax/year.

### Hospital logistics
- Swisslog Healthcare. Pneumatic tube systems and AGV networks.
- Hospital elevator segregation: bed transport, staff, clean/dirty logistics.

### Healthcare supply chain (v2 additions)
- HUG rapport annuel 2024. 13,086 employees, 146,767 ER cases.
- CHUV rapport annuel 2024. 12,844 employees, 92,674 ER cases.
- GHOL rapport annuel 2024. Nyon district, 30,000+ ER visits.
- EHC website (ehc-vd.ch). Morges-Aubonne-Gilly network.
- HRC website (hopitalrivierachablais.ch). Rennaz, 190,000 catchment.
- Galenica Group / Galexis AG. Ecublens hub, 100,000 packs/day (2022 press release).
- Swiss Post. Innight Medica service — 220+ hospital deliveries.
- PLEXUS-Santé. CHUV-HUG joint warehouse, Bussigny (swissinfo.ch, 2019).
- B. Braun Crissier. Medical devices, 12M units/year.
- Transfusion Interrégionale CRS. Épalinges, 350 employees, 700+ mobile drives/year.

### Cross-border workers
- Observatoire statistique transfrontalier (2022). 7,200 healthcare frontaliers.
- Groupe Ecomedia. 60% of Geneva hospital nurses from France.
- Amicale des Frontaliers. Geneva recruitment moratorium (October 2024).

### Transport data
- SBB/CFF timetable data (2026-03-02 query). Service frequency, first/last trains.
- TPG Noctambus. Weekend-only night buses, Geneva canton.
- NStCM. Nyon-St-Cergue-Morez narrow gauge. Last service ~21:29.
- CGN. Compagnie Générale de Navigation, Lake Geneva.
- MOB. Montreux-Oberland Bernois railway.
- VMCV. Vevey-Montreux-Chillon-Villeneuve urban bus network.
- MBC. Morges-Bière-Cossonay regional bus.

### Night work regulations
- SECO. Nuit et dimanche travail (Swiss labour law, night/Sunday work).
- CHUV union documents. 3×8h shift structure, equal night rotation.

### Nursing homes / EMS
- SOMED (OFS). Statistique des institutions médico-sociales 2024.
- État de Vaud. 156 EMS, ~6,000 beds.
- République et Canton de Genève. 54 EMS, 4,126 beds.

### Home care
- AVASAD / CMS-Vaud. 5,000 employees, 49-50 CMS centres.
- IMAD Geneva. 2,300 employees, EMD de nuit confirmed.

---

*Research v2 compiled 2026-03-17 by Cairn Code for City101 A04 prototypology phase.*
*v1: 2026-03-10. v2 integrates healthcare supply chain research (Cairn/Cadence, 2026-03-15), multimodal transport data (29,135 trips), and break point analysis (49 stations, 5 dimensions).*
