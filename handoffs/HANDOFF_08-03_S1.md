# HANDOFF — 08 March 2026, Session 1 (Cairn Code)

**Date:** 2026-03-08
**Who:** Andrea + Henna (via Andrea)
**Next action:** Field visits — Monday 09-03 afternoon (GE→LS half), Friday 13-03 afternoon (LS→VN half)

---

## What happened this session

### 1. Site selection for "Horizontal Elevator" interventions

Reviewed all 24 sites from `assignement 3/city101_horizontal_elevator_24_sites.jsx`. Through an interview process, narrowed from 24 → 9 → 6 based on these criteria:

**Selection criteria (Andrea's):**
- Skip "no venues" sites — absence alone isn't an architecture project
- Focus on **essential/critical workers** who are stranded: healthcare, logistics, supply chain
- 24h city framing: if needs aren't met, prioritize the workers the city literally can't function without
- Must be justifiable as an **architectural intervention**, not just a policy complaint

**Henna's independent list overlapped strongly.** 5 of her 7 picks matched Andrea's filtered list.

### 2. The 6 selected sites (agreed by both)

Ordered west → east along the corridor:

| # | Site | km | Role in the chain |
|---|------|----|-------------------|
| 2 | **Geneva North Industrial Belt** | 8 | Where medical cargo lands — airport, DHL, Post (blood/sample transport) |
| 19 | **Nyon Industrial + Hospital Night** | 25 | First regional hospital + Genolier hilltop clinic off-grid |
| 4 | **Morges–Rolle Gap** | 48 | Second regional hospital, staff stranded after last train |
| 18 | **Crissier–Bussigny Night Belt** | 58 | Supply/sorting hub — pharma for CHUV/HUG, Migros, packages |
| 10 | **Lausanne Perpendicular (CHUV)** | 65 | Main hospital, 1,500 night staff, 250m altitude split |
| 5 | **Montreux–Rennaz Hospital** | 90 | Newest hospital, built off-rail, eastern anchor |

**Why this set:** They form a **complete healthcare supply chain** from cargo arrival (Geneva) through regional hospitals (Nyon, Morges) to the logistics hub (Crissier) to the main hospital (CHUV) to the eastern hospital (Rennaz). Every link is broken at night.

### 3. The narrative / brief concept

**"Where does the 24h healthcare supply chain break?"**

The hospital doesn't end at its walls. A nurse finishing at 02:00 at CHUV and a pharma sorter finishing at 04:00 in Crissier are part of the same system. Neither can get home. The "horizontal elevator" connects the **invisible shift chain** that keeps the 24h city running.

### 4. Prototypology: The Relay-Lock

Combined two concepts:
- **Relay** (system level): a chain of nodes along the corridor — like postal relay stations
- **Lock** (building level): architecture that manages the threshold between two states, like a canal lock

**The prototypology = a relay network where each node is a lock.**

Each site has a different **lock condition**:

| Site | What's being "locked" between |
|------|-------------------------------|
| Geneva North | Cargo ↔ city (goods arrive, need to distribute) |
| Nyon | Valley ↔ hilltop (hospital in town, clinic above) |
| Morges | Last train ↔ first train (the 4hr dead window) |
| Crissier-Bussigny | Invisible ↔ visible (supply chain has no public face) |
| Lausanne CHUV | Uphill ↔ downhill (250m, 5.8km — most literal "horizontal elevator") |
| Rennaz | Rail ↔ off-rail (hospital built disconnected) |

**The "chamber"** = the architectural space where the transition happens. In a canal lock, you wait while water rises. For essential workers, the chamber is where you spend the dead window (01:00–05:00). Its program is TBD — rest? workspace? handoff point? supply chain interface?

### 5. Data verification results

Ran a verification agent against our datasets. **Key findings:**

#### What's solid:
- Commuter indices: 23/24 exact matches with `city101_ridership_sbb.csv`
- Modal diversity: accurately reflects our Shannon data
- Last/first train times: data exists in `city101_first_last_trains.csv`

#### What's problematic:
- **"Zero nocturnal transport" is overstated.** Actual late-night frequency: Bussigny 9.0 tr/hr, Nyon 7.0, Montreux 10.5, Lausanne 22.0. The real dead window is **01:00–05:00**, not "all night."
- **Night worker counts NOT in any dataset.** The numbers (4,600 / 1,680 / 1,500 / 400 / 300 / 730) were likely estimated externally — no CSV source found. **These need primary source verification.**
- **Hospital ratings (Rennaz 2.6★, Nyon 3.4★) not in station ratings file.** Rennaz isn't even a rail station. Only relevant low rating: Vigie M1 at 2.9★.
- **"Stranded after last train" at Morges** — last train is actually 01:07, which is not terrible. The real gap is 01:07–05:00.
- **Renens commuter index overstated**: JSX says 2.48×, dataset says 2.04.

#### Honest reframing:
The corridor serves essential workers until ~01:00. Then a **4-hour gap** opens (01:00–05:00). The structure of the argument holds, but the JSX overstates it. Night worker counts are the **load-bearing claim** and need proper sourcing (OFS employment data, hospital annual reports, direct inquiry during field visits).

### 6. Field visit plan

**Decision:** Split the corridor. Monday afternoon = western half. Friday afternoon = eastern half.

#### Monday 09-03 afternoon — Geneva → Lausanne (Andrea + Henna together, car available)

| Time | Site | Drive from prev. | What to verify |
|------|------|-------------------|----------------|
| ~13:00 | **Geneva North** (Blandonnet/ZIMEYSA) | Start | Drive the industrial belt loop. Scale of the zone. Any public space? |
| ~14:00 | **Nyon Hospital** | 20min | Hospital in town, then **drive UP to Genolier** — the hilltop disconnection |
| ~15:00 | **Morges, Hôpital de la Côte** | 25min | Hospital periphery. Try to ask staff: "how do you get home after night shift?" |
| ~15:45 | **Crissier-Bussigny** | 10min | Drive through warehouse zone. Contrast logistics sheds vs. residential |
| ~16:30 | Done / debrief | | |

#### Friday 13-03 afternoon — Lausanne → Villeneuve

| Time | Site | Notes |
|------|------|-------|
| TBD | **Lausanne CHUV perpendicular** | M2 up, walk the 250m gradient down. The slope IS the architecture problem. |
| TBD | **Rennaz Hospital** | Drive or train to Villeneuve, then try to reach hospital. Document the gap. |
| TBD | **Additional eastern sites** (see below) | |

#### At EVERY stop, document for the deliverable:
- GPS coordinates (phone)
- Photos: the gap/threshold/empty space where the lock would go
- 1-minute video walking the "broken connection"
- If possible: talk to one worker ("do you take the train?")
- Sketch: where would the chamber sit?
- Note what the JSX got right vs. wrong

### 7. Eastern half gap — additional sites to consider for Friday

The Lausanne→Villeneuve half currently only has 2 of the 6 sites (CHUV and Rennaz). The brief asks for 3–5 intervention sites total, and you may want to investigate additional locations on Friday to either:
- Confirm you don't need more sites east of Lausanne
- Discover a site the data missed
- Strengthen the supply chain argument in the eastern corridor

**Candidates to scout on Friday (from the 24-site list + healthcare logic):**

| Site | km | Why it might fit the healthcare chain |
|------|----|---------------------------------------|
| **Epalinges Medical Hill** (#17) | 66 | Medical satellite 3.4km from rail. Centre médical + Beaumont (CHUV annex). Night shift staff going uphill. Could be the **CHUV lock's second chamber** — the residential end of the perpendicular. |
| **Lausanne Flon Nightlife Circuit** (#20) | 65 | 1,500 CHUV staff + 300 bar workers share the same Mon–Thu dead window. Not healthcare supply chain per se, but the same workers, same gap. |
| **Burier–La Tour Spine** (#11) | 82 | Commuter 3.49, tiny station carrying hillside villages. Between CHUV and Rennaz. If there's healthcare workers commuting through here, it fills the geographic gap. |
| **Lavaux Vineyard Corridor** (#16) | 74 | Lowest ridership, highest day/night ratios, UNESCO constraints. Not healthcare, but the **absence** between your two eastern sites is itself a finding — why does the supply chain skip Lavaux? |
| **Puidoux-Chexbres Hillside** (#22) | 76 | 68% car (highest), 2 tr/hr. Above Lavaux. If Vevey/La Tour hospital workers live here, the vertical disconnection mirrors Nyon→Genolier. |
| **Vevey itself** (not in the 24 sites) | ~80 | Nestlé HQ (4k workers), Hôpital Riviera-Chablais site. Worth a quick stop to check if there's a healthcare node the JSX missed entirely. |

**Recommendation:** On Friday, after CHUV and Rennaz, drive through Vevey and La Tour-de-Peilz. If there's a hospital/medical presence there, you may have found the missing eastern link. If not, the gap between CHUV (km 65) and Rennaz (km 90) is itself a finding — 25km of corridor with no healthcare supply chain to break.

---

## Henna's original picks (for reference)

Montreux–Rennaz Hospital, Saint-Prex Isolated Village, Morges–Rolle Gap, Crissier–Bussigny Night Belt, Geneva North Industrial Belt, Nyon Industrial + Hospital Night, Gland–Rolle La Côte Gap

**Overlap with Andrea:** 5/7 (all except Saint-Prex and Gland-Rolle, which Andrea filtered as "gap/absence" sites)

## Open questions

1. **Night worker numbers need sourcing.** This is the load-bearing claim. Options: OFS employment data, hospital annual reports (HRC Rennaz, CHUV, Hôpital de Nyon, Hôpital de la Côte), or direct questions during field visits.
2. **Prototypology "chamber" program** — what's inside the lock? Rest, workspace, supply handoff, all three? Field visits should inform this.
3. **3–5 or 6 sites?** Brief says 3–5. We have 6. Either justify 6 (the chain needs every link) or merge Crissier + CHUV into one intervention (7km apart, supply hub + hospital = one system).
4. **Eastern half density** — Friday visit should determine if we need a 7th site between CHUV and Rennaz, or if the gap is the argument.

---

## Files referenced this session
- `assignement 3/city101_horizontal_elevator_24_sites.jsx` — the 24 sites source
- `datasets/corridor_analysis/city101_first_last_trains.csv` — verified last train times
- `datasets/corridor_analysis/city101_temporal_frequency.csv` — verified late-night frequencies
- `datasets/stations/city101_station_ratings.csv` — checked for hospital ratings (not found)
- `datasets/transit/city101_ridership_sbb.csv` — verified commuter indices
- `datasets/corridor_analysis/city101_modal_diversity.csv` — verified modal Shannon

## No files were created or modified (except this handoff).
