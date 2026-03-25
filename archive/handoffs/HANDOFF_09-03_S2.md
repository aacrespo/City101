# HANDOFF — 09 March 2026, Session 2 (Cairn Code)

**Date:** 2026-03-09
**Who:** Andrea + Henna (via Andrea)
**Status:** Final site selection complete. Field visit protocol ready.
**Next actions:**
- Monday 09-03 afternoon: Western corridor field visit (Geneva → Crissier-Bussigny, 4 sites)
- Friday 13-03 afternoon: Eastern corridor field visit (Lausanne → Rennaz, 3 sites)

---

## Decisions made this session

### 1. Final site selection: 7 nodes, 1 network

Evolved from 6 to **7 sites** after cross-referencing with Henna's healthcare-focused list (`assignement 3/city101_healthcare_sites.jsx`). Added **Montreux–Glion Altitude Medicine** (km 85) to fill the 25km gap between CHUV and Rennaz.

**The argument for 7 (brief says 3–5):** The horizontal elevator isn't 7 separate projects — it's one healthcare circuit with 7 locks. Remove any node and the chain breaks. The network covers **three scales** of the same problem:
- **Infrastructure** (nodes 1, 4): how medical goods move through the night
- **Staff access** (nodes 2, 3, 5, 7): how healthcare workers get home after shifts
- **Patient access** (nodes 2, 5, 6): how elderly/rehab populations reach care

### 2. The 7-node healthcare circuit

| Node | Site | km | Lock type | Role in the chain |
|------|------|----|-----------|-------------------|
| 1 | **Geneva North Industrial Belt** | 8 | Cargo ↔ City | Medical supplies enter Switzerland. Airport pharma freight, DHL, Post (blood/samples). **The origin.** |
| 2 | **Nyon Hospital + Genolier Hilltop** | 25 | Valley ↔ Hilltop | Regional hospital at lake + Genolier clinic at 600m+ + Prangins psychiatric. Three healthcare typologies split by altitude. 350 night staff. |
| 3 | **Morges Hospital Gap** | 48 | Last train ↔ First train | Regional hospital, 300 night staff, 4,750 elderly in catchment. Purest expression of the 01:00–05:00 dead window. |
| 4 | **Crissier-Bussigny Night Belt** | 58 | Invisible ↔ Visible | Pharma sorting for CHUV/HUG, Migros hospital food, medical packages. 1,680 night workers. **The supply chain has no public face.** |
| 5 | **Lausanne CHUV Perpendicular** | 65 | Uphill ↔ Downhill | 1,500 night staff dispersing across 250m gradient. Income-transport paradox: cheaper housing = worse night transport. |
| 6 | **Montreux–Glion Altitude Medicine** | 85 | Mountain ↔ Lake | Clinique Valmont rehab at 600m+, funicular stops at night. 23% elderly (highest east of Geneva). Health split between altitude and lakeside. |
| 7 | **Rennaz Hospital Island** | 89 | Rail ↔ Off-rail | 400 night staff, hospital built 2.1km from rail in 2019. 2.6★. The corrective intervention. |

### 3. Why Montreux–Glion was added

From Henna's `city101_healthcare_sites.jsx` (Site #5). Key findings:
- Clinique Valmont at 600m+ — private rehab, 4.5★, shifts on mountainside
- Funicular exists but doesn't run at night
- 23% elderly in Montreux catchment (6,137 people) — highest east of Geneva
- Montreux health ecosystem is **split between lake** (HRC Rennaz) and **mountain** (Valmont)
- Mirrors Nyon→Genolier vertical problem but with rehab/patient access angle
- Fills the 25km gap between CHUV (km 65) and Rennaz (km 89)

### 4. Prototypology: The Relay-Lock (refined)

**System level = Relay.** A chain of 7 nodes along the corridor.
**Building level = Lock.** Architecture that manages the threshold between two states.
**The chamber** = the architectural space where the transition happens.

Each lock-chamber has the same DNA but adapts its program:

| Node | Chamber program leans toward... |
|------|--------------------------------|
| Geneva North | Logistics interface + worker rest |
| Nyon | Vertical connector + staff/patient dual use |
| Morges | Night shelter + elderly mobility hub |
| Crissier-Bussigny | Supply chain civic space + worker visibility |
| Lausanne CHUV | Gradient connector + equity corrector |
| Montreux-Glion | Altitude connector + family/rehab access |
| Rennaz | Rail bridge + emergency access |

### 5. Henna's healthcare list — new dimensions

`city101_healthcare_sites.jsx` introduced two frameworks we didn't have:
- **Staff access vs. Patient access** — two-color classification (red/blue)
- **Income-transport paradox** at CHUV: nurses earning CHF 56k (Renens) have 0 nocturnal stops; doctors earning CHF 95k (Cour) can walk home
- **Elderly demographics**: 18–24% elderly across corridor hospitals, 4,750 in Morges catchment, 6,137 in Montreux
- **Hospital ratings correlated with access**: Rennaz 2.6★ (worst, off-rail), station clinics 4.0★ (best, at rail)

### 6. Data verification summary (from Session 1)

**Solid:** Commuter indices (23/24 exact), modal diversity, last/first train times.

**Problematic:**
- "Zero nocturnal transport" overstated — real dead window is 01:00–05:00, not all night
- Night worker counts (4,600 / 1,680 / 1,500 / 400 / 300 / 730) NOT in any dataset — need primary sourcing
- Hospital ratings (2.6★, 3.0★, 3.4★) not in station ratings CSV — likely from Google directly
- Renens commuter index: JSX says 2.48×, dataset says 2.04

**Field visits are the verification opportunity.**

---

## The narrative in one sentence

*Medical cargo lands at Geneva, gets sorted in Crissier at 3am, reaches CHUV by morning, serves patients who live uphill in Epalinges, while regional hospitals in Nyon, Morges, and Rennaz run parallel night shifts with stranded staff, and rehab patients recover on a mountainside in Glion that no one can reach after dark.*

---

## Field visit protocol

### Brief requirements (from A03 assignment)

> Armed with a map of high-potential areas, engage in on-site fieldwork to investigate each location, documenting via photographs, interviews, drawings, sketches, videos, etc. Critically examine the data generated by the LLM, and identify biases, factual errors, but also correct assumptions. Based on field investigation, verify potential sites or identify new ones, and begin to imagine a strategy for networked, hybrid urban-architectural interventions.

**Deliverables:**
1. Area of investigation report (text, image, updated maps)
2. Combined path dataset (destinations as CSV/GeoJSON)
3. Concept for networked intervention strategy

---

### BEFORE the visits

#### Print / prepare (do this morning)

1. **Print the 7-site summary table** (from this handoff) — one copy each
2. **Print or screenshot the lock-type diagram** for each site — know what you're looking for
3. **Load GPS waypoints on phones.** Coordinates for all 7 sites:

| Site | Lat | Lon | What to pin |
|------|-----|-----|-------------|
| Geneva North (Blandonnet) | 46.223 | 6.093 | ZIMEYSA industrial zone entrance |
| Nyon Hospital (GHOL) | 46.383 | 6.237 | Hospital main entrance |
| Genolier Clinic | ~46.41 | ~6.24 | Hilltop clinic (drive up) |
| Morges Hospital (EHC) | 46.511 | 6.498 | Hospital + station (1.4km gap) |
| Crissier-Bussigny | 46.551 | 6.550 | Bussigny Arc-en-Ciel logistics zone |
| Lausanne CHUV | 46.525 | 6.635 | CHUV main + M2 top station |
| Montreux-Glion (Valmont) | 46.425 | 6.920 | Funicular base + Valmont direction |
| Rennaz HRC | 46.435 | 6.938 | Hospital + Villeneuve station (2.1km gap) |

4. **Prepare interview questions** (keep on phone, screenshot):
   - "Do you work night shifts here? How do you get home?"
   - "What time does the last bus/train pass?"
   - "Do patients/visitors complain about access?"
   - "Where do most staff live?"
   - "Is there anywhere to wait/rest between shifts?"

5. **Prepare a verification checklist per site** (what the data claims vs. what to check):

| Site | Data claims to verify on-site |
|------|-------------------------------|
| Geneva North | Is there ANY public space in the industrial belt? Are DHL/Post visible? Scale? |
| Nyon | How far is hospital from station really? What's the road up to Genolier like? Bus stop? |
| Morges | Is hospital 1.4km from station? What's the walk? Any shelter at hospital bus stop? |
| Crissier-Bussigny | Can you see the warehouses? Any signage for pharma/medical logistics? Residential contrast? |
| CHUV | What does the M2 corridor feel like at the top? Where does the gradient hit hardest? |
| Montreux-Glion | Is the funicular visible? What's the road to Valmont? Any night transport signage? |
| Rennaz | Walk from Villeneuve station to hospital — time it. Is there a sidewalk? Is "car only" real? |

6. **Gear:**
   - Phone (GPS, photos, video, voice memos)
   - Sketchbook + pencil
   - Measuring tape or phone distance app
   - Portable charger
   - The car (Henna's)

---

### DURING the visits

#### Monday 09-03 afternoon — Western corridor (4 sites)

**Andrea starts in Geneva. Henna drives from Lausanne to Geneva. Meet up, then do all 4 together by car.**

| Time | Site | Duration | What to do |
|------|------|----------|------------|
| ~13:00 | **Geneva North** | 45 min | Drive the full ZIMEYSA → Blandonnet → airport cargo zone loop. Stop at 2-3 points. Photo the scale — these are massive industrial blocks. Look for: any human-scale space between the sheds. Any bus stop. Any sign of night activity (24h signage, security booths, lit windows). Sketch the threshold between industrial zone and residential Vernier. |
| ~14:00 | **Nyon Hospital** | 60 min | Park at GHOL hospital. Walk to the station (0.7km) — time it, photograph the route. Is it lit? Sheltered? Then **drive up to Genolier** — this is the key moment. Document the road: switchbacks, altitude gain, visibility of the lake below. At Genolier: is there a bus stop? What's the last service posted? Where would a lock connect valley to hilltop? Quick stop at Prangins psychiatric if time allows. |
| ~15:15 | **Morges Hospital** | 45 min | Park at hospital. Walk to station (claimed 1.4km) — time it. Photo the route: is it walkable at 01:00? Lit? Any shelter? At the hospital: look for night shift evidence (staff entrance, parking patterns, any 24h signage). Compare with the walk-in clinics AT the station (Permanence des Halles, CMM). The contrast = the argument. Try to ask one person. |
| ~16:15 | **Crissier-Bussigny** | 30 min | Drive through the logistics belt. Photo the warehouse landscape — the Bussigny Arc-en-Ciel zone, Voxel, any pharma/medical logistics signage. Then drive 2 minutes to the nearest residential street. Photo the contrast. Where would a lock make the invisible visible? This is the fastest stop — the car drive IS the documentation. |
| ~17:00 | **Debrief in car / café** | 30 min | Compare notes. What surprised you? What did the data get wrong? What did it get right? Voice-record a 5-minute summary. |

#### Friday 13-03 afternoon — Eastern corridor (3 sites)

| Time | Site | Duration | What to do |
|------|------|----------|------------|
| ~13:00 | **Lausanne CHUV** | 75 min | This is the most architectural visit. Start at the TOP — Epalinges or Chailly. Walk/drive DOWN the gradient to CHUV. Document: the slope, the residential neighborhoods on the way down (Pierre-de-Plan, Sallaz — these are where CHF 56-60k nurses live). At CHUV: the staff entrance, the M2 station, the night-shift handover zone. Walk from CHUV down to Ouchy if time — the full 250m vertical section. Sketch where the lock would sit on this gradient. |
| ~14:30 | **Montreux-Glion** | 60 min | Drive or train to Montreux. Find the funicular to Glion. Document: base station, operating hours posted, the altitude visible from below. If possible, ride up (or drive up to Glion). At the top: where is Valmont? Can you see the lake? The town? This is where the mountain ↔ lake split becomes physical. Photo the Montreux medical cluster from above — 31 health buildings, elderly town. Sketch the vertical connection. |
| ~15:45 | **Rennaz Hospital** | 60 min | The most important documentation. Go to Villeneuve station first. **Walk to HRC Rennaz** — time it, GPS track it, photograph every meter. Is there a sidewalk? Street lighting? Any bus stop? Any signage pointing to the hospital? This walk IS the evidence. At the hospital: the entrance, the parking (how big?), any 24h signage. Look for the old Vevey Providence site too (0.5km from La Tour station) — the before/after contrast. |
| ~17:00 | **Debrief** | 30 min | Same as Monday — compare, voice-record, note surprises. |

#### At EVERY stop — documentation protocol

Do these 7 things at each site. Make it a habit:

1. **GPS pin** — drop a pin on Google Maps, screenshot it with coordinates visible
2. **Context photo** — wide shot showing the site in its surroundings (the "where")
3. **Detail photo** — the specific gap/threshold/empty space where the lock would go (the "what")
4. **1-minute video** — walk the "broken connection" (hospital to station, valley to hill, warehouse to residential). Narrate what you see.
5. **Voice memo** — 30 seconds: "What surprised me here. What the data got right. What it got wrong."
6. **Quick sketch** — even 2 minutes. Where would the chamber sit? What's the threshold?
7. **Interview attempt** — ask one person if possible. Even a failed attempt is data ("nobody was around at 15:00 on a Monday").

#### Interview targets by site

| Site | Who to try to talk to |
|------|----------------------|
| Geneva North | Security guard, truck driver at loading dock, anyone in a safety vest |
| Nyon | Hospital reception, bus driver at Genolier, pharmacy staff |
| Morges | Hospital staff at entrance/café, station kiosk worker |
| Crissier-Bussigny | Anyone visible outside a warehouse — unlikely, but try |
| CHUV | Nurses outside smoking/on break, M2 metro attendant, café worker near staff entrance |
| Montreux-Glion | Funicular operator, Valmont reception, elderly resident in Glion |
| Rennaz | Hospital reception/info desk, anyone walking the Villeneuve→Rennaz road, bus driver |

---

### AFTER the visits

#### Same evening (Monday + Friday)

1. **Transfer all photos/videos** to a shared folder (Google Drive or local)
2. **Name files consistently:** `site[N]_[sitename]_[type]_[seq].jpg`
   - e.g. `site2_nyon_context_01.jpg`, `site7_rennaz_walk_video_01.mp4`
3. **Transcribe voice memos** — key quotes only, bullet points
4. **Fill in the verification table:**

| Site | Data claim | Verified? | What we actually found | Photo ref |
|------|-----------|-----------|----------------------|-----------|
| Geneva North | "4,600 night workers" | ? | | |
| Geneva North | "3 venues" | ? | | |
| Nyon | "Genolier 3.6km from rail" | ? | | |
| Nyon | "0 nocturnal transport to hilltop" | ? | | |
| Morges | "1.4km hospital to station" | ? | | |
| Morges | "300 night staff stranded" | ? | | |
| Crissier | "CHUV-HUG pharma supply" | ? | | |
| Crissier | "zero public space" | ? | | |
| CHUV | "250m altitude split" | ? | | |
| CHUV | "M2 stops ~00:36" | ? | | |
| Montreux-Glion | "Valmont at 600m+" | ? | | |
| Montreux-Glion | "Funicular doesn't run at night" | ? | | |
| Rennaz | "2.1km from Villeneuve station" | ? | | |
| Rennaz | "car only" | ? | | |
| Rennaz | "2.6★" | ? | | |

5. **Note any NEW sites discovered** — places you drove past that weren't on the list but should be

#### Before submission

6. **Create the path dataset** (CSV + GeoJSON) — deliverable requirement:

CSV columns: `id, site_name, lat, lon, arrival_time, departure_time, type (staff_access/patient_access/infrastructure), lock_type, verified_claims, new_findings, photo_count, interview_count`

7. **Write the investigation report** — structure:
   - The network concept (1 paragraph)
   - 7 site summaries (verified findings, surprises, photos)
   - Verification table (what the LLM got right/wrong/couldn't verify)
   - Prototypology sketch (the relay-lock concept, informed by what we saw)
   - Next steps toward design

8. **Update maps** — mark the 7 sites on a corridor map with lock-type annotations

---

## Open questions (carried forward + new)

1. **Night worker numbers** — still the load-bearing claim, still unsourced. Field visits are the chance to get at least anecdotal confirmation.
2. **Chamber program** — field visits should reveal what essential workers actually need at 01:00–05:00. Ask them.
3. **7 sites vs brief's "3–5"** — argument is ready: it's one network, 7 nodes. The network IS the project, not the individual sites.
4. **Henna's healthcare list added elderly demographics** — 18–24% elderly across catchments. This strengthens the patient access argument. Integrate into the report.
5. **Income-transport paradox** (from Henna's list) — CHUV nurses earning less live further with worse night transport. Powerful equity angle. Needs verification: are Renens/Prilly really where CHUV staff live?

---

## Files referenced

- `assignement 3/city101_horizontal_elevator_24_sites.jsx` — original 24 sites
- `assignement 3/city101_healthcare_sites.jsx` — Henna's 8 healthcare-focused sites (new)
- `handoffs/HANDOFF_08-03_S1.md` — previous session handoff
- All dataset verification from Session 1 still applies (see HANDOFF_08-03_S1.md §5)

## Files created this session
- `handoffs/HANDOFF_09-03_S2.md` — this file
