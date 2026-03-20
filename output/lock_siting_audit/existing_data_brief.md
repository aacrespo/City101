# Lock Siting Audit — Existing Data Brief

**Compiled:** 2026-03-18
**Purpose:** Shared reference for all Phase 1 transit research agents

---

## 1. The 9 Nodes

| Node | Name | km | Lock Type | Key Population | Key Institution |
|------|------|----|-----------|---------------|-----------------|
| 1 | Lancy-Pont-Rouge | 4 | Border Lock | ~160,000 frontaliers, border workers | HUG (Geneva) nearby |
| 2 | Geneva North Industrial | 8 | Cargo Lock | Logistics workers, pharma, airport staff | GVA Airport, ZIMEYSA zone |
| 3 | Nyon-Genolier | 25 | Altitude Lock | Genolier Clinic staff (~150 night) | Genolier Clinic (hilltop), GHOL Nyon |
| 4 | Morges | 48 | Temporal Lock | ~450 night workers | EHC Morges hospital |
| 5 | Crissier-Bussigny-Ecublens | 58-62 | Visibility Lock / Logistics Engine | Logistics/distribution workers | Crissier distribution hub |
| 6 | Lausanne CHUV | 65 | Gradient Dispatcher | ~13,000 CHUV employees (2,500-3,000/night) | CHUV university hospital |
| 7 | Vevey | 80 | Gap Relay | Tourism/hospitality workers | Nestlé HQ, resort hotels |
| 8 | Montreux-Glion | 85 | Altitude Lock | Rehab/clinic staff, families | Glion clinics, rehab facilities |
| 9 | Rennaz | 89 | Bridge Lock | HRC hospital staff | Hôpital Riviera-Chablais (HRC) |

---

## 2. Rail Dead Windows (Weekday — from first/last trains CSV)

| Station | Last Train | First Train | Dead Window | Duration |
|---------|-----------|-------------|-------------|----------|
| Genève | 01:18 | 04:00 | 01:18–04:00 | 2h42m |
| Lancy-Pont-Rouge | 01:07 | 04:07 | 01:07–04:07 | 3h00m |
| Lancy-Bachet | 01:10 | 04:10 | 01:10–04:10 | 3h00m |
| Genève-Aéroport | 00:19 | 04:58 | 00:19–04:58 | 4h39m |
| Vernier-Blandonnet | 00:46 | 04:04 | 00:46–04:04 | 3h18m |
| Nyon | 01:05 | 04:23 | 01:05–04:23 | 3h18m |
| Morges | 01:07 | 04:01 | 01:07–04:01 | 2h54m |
| Bussigny | 00:55 | 04:48 | 00:55–04:48 | 3h53m |
| Renens VD | 01:14 | 04:46 | 01:14–04:46 | 3h32m |
| Lausanne | 00:34 | 04:38 | 00:34–04:38 | 4h04m |
| Lausanne-Flon | 00:36 | 05:40 | 00:36–05:40 | 5h04m |
| Vevey | 01:04 | 05:01 | 01:04–05:01 | 3h57m |
| La Tour-de-Peilz | 01:02 | 05:11 | 01:02–05:11 | 4h09m |
| Montreux | 00:56 | 04:43 | 00:56–04:43 | 3h47m |
| Territet | 00:56 | 05:01 | 00:56–05:01 | 4h05m |
| Villeneuve VD | 00:51 | 04:57 | 00:51–04:57 | 4h06m |

**Core dead window:** ~01:30–03:30 (when ALL modes are silent). Wider at smaller stations.

---

## 3. Existing Noctambus Data (GTFS — Fri/Sat ONLY)

**559 records** across 22 routes. **ALL are Friday/Saturday night only.**

### Geneva routes (TPG Noctambus)
- Routes 2, 3, 5, 7, 10, 19, 28, 53: Geneva city + communes
- Routes A1–A6: Airport connections
- Route 60: Cross-border to Gex/Ferney (France)
- Route 82: Lancy-Bachet ↔ Plan-les-Ouates ↔ Croix-de-Rozon

### Lausanne routes (TL Noctambus)
- Routes 3, 6, 21: Lausanne city (Prélaz, Chauderon, gare)

### Eastern corridor
- Routes 102, 105: Monthey/Collombey area (TPC)
- Route EV: Regional (La Plaine, Satigny, Russin)

### CRITICAL GAP
**Monday–Thursday: ZERO Noctambus service anywhere on the corridor.**
The audit focuses on weekday dead windows. Noctambus is irrelevant for Mon-Thu.

### Coverage gaps even on Fri/Sat
- **Nyon to Morges (km 25–48):** No Noctambus coverage at all
- **Morges to Lausanne (km 48–65):** No Noctambus
- **Lausanne to Vevey (km 65–80):** No Noctambus
- **Vevey to Rennaz (km 80–89):** No Noctambus
- Only Geneva and Lausanne city centers have Noctambus; the mid-corridor and east are completely unserved

---

## 4. Healthcare Overlay — Night Worker Data

### Hospital night staffing estimates (from v2 research)
| Hospital | Location | Night Staff Estimate | Notes |
|----------|----------|---------------------|-------|
| HUG (Hôpitaux Universitaires de Genève) | Geneva | 3,000–4,000/night | 13,086 employees, 60% nurses from France |
| CHUV | Lausanne | 2,500–3,000/night | 12,844 employees, ~5,257 nurses across 24h |
| EHC Morges | Morges | ~100–150/night | Part of EHC network |
| GHOL Nyon | Nyon | ~80–120/night | Site Nyon + satellites |
| Genolier Clinic | Genolier (hilltop) | ~150/night | Private clinic, 200m above Nyon |
| HRC Rennaz | Rennaz | ~200–300/night | New hospital, opened 2019 |
| Montreux clinics | Glion/Montreux | ~50–80/night | Rehab + private clinics |

### Total corridor night healthcare workers: 8,000–10,000
### Key supply chains (ALL road-dependent during dead window):
- Medication, food, staff, patients, postal, lab samples, waste, emergency
- Swiss Post "Innight Medica": deliveries to 220+ hospitals by 06:00 (truck only)
- Only 1 true 24h pharmacy on entire 101km (Pharma24 at HUG, Geneva)

---

## 5. Transport Operators by Region

| Region | Rail | Bus | Metro/Funicular | Key Night Questions |
|--------|------|-----|-----------------|-------------------|
| **Geneva** (Nodes 1-2) | SBB/CFF, SNCF (Léman Express) | TPG | — | TPG Noctambus = Fri/Sat only. SNCF cross-border night? Airport shuttles? |
| **Nyon** (Node 3) | SBB/CFF | NStCM (narrow gauge to Genolier) | — | NStCM last train ~21:29. Genolier shuttle? |
| **Morges** (Node 4) | SBB/CFF | MBC (Morges-Bière-Cossonay) | — | MBC night service? EHC shuttle? |
| **Crissier** (Node 5) | SBB/CFF | TL (Transports Lausannois) | — | Employer transport? Distribution center shift buses? |
| **Lausanne** (Node 6) | SBB/CFF | TL | M2 metro (Ouchy→Epalinges) | M2 last run? TL Noctambus = Fri/Sat only. CHUV shuttle? |
| **Vevey** (Node 7) | SBB/CFF | VMCV | Vevey-Chardonne funicular | VMCV night? Funicular hours? Hotel staff transport? |
| **Montreux** (Node 8) | SBB/CFF | VMCV | Territet-Glion funicular, MVR rack | Funicular night hours? Glion clinic shuttle? |
| **Rennaz** (Node 9) | — (no station) | TPC, VMCV | — | HRC shuttle to Villeneuve station? Walk safety on Route 9? |

---

## 6. Existing 3D Model States

### Lock 03 — Morges (Temporal Lock)
- **Script:** `lock_03_morges_temporal_v4.py`
- **LOD:** LOG 400 (138 objects)
- **SITE_ORIGIN:** (-60, 0, 381.5) — PROVISIONAL
- **LV95:** E 2,527,440, N 1,151,500
- **Terrain tile:** 2527-1151 (1km²)
- **Known issues:**
  - Hospital (EHC Morges) at ~N 1,152,050 — 50m beyond terrain tile north edge
  - Lock sits on rail embankment (Z=381.5), town is 6m below at Z=375-378
  - Walking route goes through town center, NOT Av. de Marcelin
  - Position is provisional — halt pending this audit

### Lock 05 — CHUV (Gradient Dispatcher)
- **Script:** `lock_05_chuv_gradient_v3.py`
- **LOD:** LOG 200-300
- **Known issues:**
  - Hospital is 132m beyond terrain tile
  - M2 metro hours unknown — if M2 stops at night, the 250m gradient IS the gap
  - 4-level gradient dispatcher concept may need rethinking if no night M2

### Lock 07 — Rennaz (Bridge Lock)
- **Script:** `lock_07_rennaz_bridge_v3.py`
- **LOD:** LOG 200-300
- **Known issues:**
  - Hospital (HRC) is 644m beyond terrain tile
  - 2.1km station-to-hospital axis
  - "Bridge lock" orientation needs validation against actual walking route
  - Highway environment — safety at 02:00 is a question

---

## 7. The Siting Rule (from Morges discovery)

**Start from the person, not the geometry.**

1. Who is the person? (ICU nurse, logistics driver, hotel receptionist)
2. Where are they physically at 02:00? (hospital ward, warehouse, hotel lobby)
3. What transit exists during the dead window? (shuttle? night bus? nothing?)
4. What's the experiential gap? (not distance — the felt reality of being stranded)
5. Where should the lock be? Near origin, destination, or transit node?
6. What must the 3D model show? Both endpoints of the connection.

**The lock is waiting infrastructure — it needs to be where the person IS when the gap hits.**

---

## 8. What Each Phase 1 Agent Must Produce Per Node

For each assigned node, a structured card:

```
### Node [N] — [Name]

#### Last/First Departures (Weekday) by Mode
- Rail: last [time], first [time] → dead window [duration]
- Bus [operator]: last [time], first [time] → dead window [duration]
- Metro/Funicular: last [time], first [time] → dead window [duration]

#### Dead Window Duration
[Exact minutes from last departure of ANY mode to first departure of ANY mode]

#### Institutional Transport
- [Hospital/employer] shuttle: [details or "none found"]
- [Other]: [details]

#### Walking Assessment
- From [institution] to [transit stop]: [distance]m, [time]min
- Terrain: [flat/hilly/steep gradient]
- Safety at 02:00: [lighting, pedestrian infrastructure, isolation level]
- Realistic? [yes/no + why]

#### Data Confidence
- [Finding]: [HIGH/MEDIUM/LOW] — [source]
```

**Critical distinction:** Research WEEKDAY schedules. Noctambus is Fri/Sat only and does NOT help.

**Operators to check online:**
- TPG (Genève): tpg.ch
- TL (Lausanne): t-l.ch
- MBC (Morges region): mbc.ch
- NStCM (Nyon-St-Cergue): nstcm.ch
- VMCV (Vevey-Montreux): vmcv.ch
- MVR/MOB (Montreux-Glion-Rochers): mob.ch or goldenpass.ch
- TPC (Chablais): tpc.ch
- M2 metro: t-l.ch (operated by TL)
- SBB/CFF: sbb.ch (national rail)
