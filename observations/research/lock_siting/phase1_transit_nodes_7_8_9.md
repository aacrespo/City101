# Phase 1C — Transit Research: Eastern Corridor Nodes (7-9)
**Researcher:** Agent 1C | **Date:** 2026-03-18

---

## Node 7 — Vevey (km 80) — Gap Relay

### Last/First Departures (Weekday) by Mode

| Mode | Operator | Last Departure | First Departure | Dead Window |
|------|----------|---------------|-----------------|-------------|
| Rail (SBB) | SBB/CFF | 01:04 | 05:01 | 3h 57m |
| Bus (line 201) | VMCV | ~00:00 (midnight) | ~05:25 | ~5h 25m |
| Funicular (VCP) | MOB/MVR | 00:07 | 05:32 | 5h 25m |

**Notes on VMCV:** VMCV operates daily service from ~06:00 to midnight on weekdays. The 2025 timetable added an early morning departure on line 201 at 05:25 from "Montreux, Casino" to Vevey. The 2026 network reorganization maintains similar hours with no major changes to line 201. Line 201 is the principal line running through Vevey gare.

**Notes on Funicular (Vevey-Chardonne-Mont-Pelerin):** The VCP funicular runs daily; first departure 05:32, last departure 00:07 on Mon-Thu. Automatic operation. This serves hilltop residential areas (Chardonne, Mont-Pelerin) but NOT the hospital/hotel corridor.

### Dead Window Duration

- **Rail-only dead window:** 3h 57m (01:04-05:01)
- **All-modes dead window:** ~3h 57m. The bus and funicular stop before rail (midnight and 00:07 respectively), and rail provides the latest departure (01:04). First morning service is the rail at 05:01, before the bus (~05:25) and funicular (05:32).
- **Effective dead window: 01:04-05:01 = 3h 57m** (rail governs both boundaries)

### Institutional Transport

- **Nestle HQ:** No night shift operations. Nestle Vevey is an office/headquarters campus (Avenue Nestle 55). Central switchboard hours are 07:30-18:00 Mon-Fri. No night workers to speak of. Corporate office work only.
- **Hotels:** No evidence of organized hotel staff transport. Vevey/Riviera hotels with 24h reception include major properties but night staff commute individually. The Fairmont Le Montreux Palace confirms 24-hour reception. Hotels in Vevey are smaller (7-34 employees total per property).
- **No institutional shuttles found.**

### Walking Assessment

- **Nestle HQ to Vevey gare:** 750m, ~10 min walk. Flat lakeside terrain. Well-lit urban center. Irrelevant at 02:00 (no night workers).
- **Hotels to Vevey gare:** Most Vevey hotels (Astra, Modern Times, Three Crowns) are within 500m of the station, along the lakefront promenade or Grande-Place. Well-lit, pedestrian-friendly, relatively safe at 02:00 (small-town quiet, not isolated).
- **Mont-Pelerin/Chardonne to Vevey gare:** 3-4 km, steep descent through vineyards (Lavaux terraces). No lighting on vineyard paths. The funicular provides service until 00:07 but anyone stranded after that faces a dark, steep walk. This is the altitude vulnerability.

### Who Is Here at 02:00?

- **Hotel night receptionists:** Estimated 15-25 across Vevey proper (based on ~15-20 hotels, not all having 24h reception). Small boutique hotels may not have 24h reception (e.g., Astra Hotel reception closes at 23:00).
- **Restaurant/bar workers:** A handful finishing after midnight closings. Vevey has a modest nightlife compared to Montreux.
- **No hospital night workers** in Vevey itself (nearest hospitals are Montreux and HRC Rennaz).
- **No Nestle workers** — this is entirely an office campus.
- **Estimated total at 02:00:** 20-40 individuals scattered across hotels and a few late-closing venues. Low density, low institutional concentration.

### Data Confidence Summary

| Finding | Confidence | Source |
|---------|-----------|--------|
| Rail dead window 01:04-05:01 | HIGH | existing_data_brief.md (from SBB CSV) |
| VMCV service ends ~midnight weekdays | MEDIUM | vmcv.ch general schedule; exact last departure per stop not verified |
| VCP funicular 00:07-05:32 | MEDIUM | Moovit/tp-info.ch aggregated data |
| Nestle = office only, no night shift | HIGH | nestle.com, switchboard hours 07:30-18:00 |
| Hotel night worker estimate 15-25 | LOW | Extrapolated from hotel count and size; no survey data |
| No institutional shuttles | MEDIUM | No evidence found in web search; absence of evidence |
| VMCV early 05:25 departure (2025) | MEDIUM | Vevey city announcement |

### Key Finding

Vevey is a **low-intensity node** for the dead window. Its defining feature is the 13km gap from the nearest neighboring node (Montreux), not the number of stranded workers. The night population is sparse: a scattering of hotel receptionists and late-shift hospitality workers. Nestle is irrelevant (daytime office). The real vulnerability is **altitude isolation** — anyone in Chardonne/Mont-Pelerin after the 00:07 funicular is stranded on the hillside until 05:32.

---

## Node 8 — Montreux-Glion (km 85) — Altitude Lock

### Last/First Departures (Weekday) by Mode

| Mode | Operator | Last Departure | First Departure | Dead Window |
|------|----------|---------------|-----------------|-------------|
| Rail (SBB) | SBB/CFF | 00:56 | 04:43 | 3h 47m |
| Rail at Territet | SBB/CFF | 00:56 | 05:01 | 4h 05m |
| Bus (line 201) | VMCV | ~00:00 (midnight) | ~05:25 | ~5h 25m |
| **Territet-Glion Funicular** | MOB/MVR | **01:11** | **05:11** | **4h 00m** |
| Glion-Rochers-de-Naye rack | MOB/MVR | ~16:27 (winter) / ~18:27 (summer) | ~08:28 | N/A (daytime only) |

### Dead Window Duration

- **At Montreux station level:** 00:56-04:43 = 3h 47m (rail governs)
- **At Glion (300m above):** The Territet-Glion funicular is THE critical link. Last departure 01:11, first departure 05:11 = **4h 00m dead window at altitude**.
- **CRITICAL FINDING:** The Territet-Glion funicular runs until 01:11 on weekdays (Mon-Thu), which is later than the last train at Montreux (00:56). This means there is a ~15 minute buffer where someone could arrive at Territet on the last train and still catch the funicular up to Glion. **Glion is NOT fully severed on weekday nights** — the funicular provides the last connection at 01:11.
- **But above Glion:** The Glion-Rochers-de-Naye rack railway is purely daytime (last descent ~16:27 in winter, ~18:27 in summer). Anyone at Rochers-de-Naye or Caux is stranded long before the dead window even begins.
- **Effective dead window for Glion: 01:11-04:43 = 3h 32m** (funicular last → rail first at Montreux)

### Institutional Transport

- **Clinique Valmont (Glion):** Internationally renowned rehabilitation center, ~85 employees, 59 beds, 12 suites. Specializes in orthopaedic and neurological rehabilitation. Staff work 24/7 (rehab patients need continuous care). Estimated 15-25 staff on night shift. **No evidence of staff shuttle found.** Staff likely drive or use the funicular.
- **Clinic Les Alpes (Les Avants, above Glion):** Luxury addiction rehabilitation clinic. Staff described as available "24/7/7" — doctors, nurses, psychologists, counselors, spa therapists, hospitality. Exact night staff count unknown but likely 10-20 given boutique scale. Located even higher than Glion, above the funicular's reach.
- **Hotels (Montreux lakefront):** Fairmont Le Montreux Palace has 24-hour reception. Grand Hotel Suisse Majestic (room service limited hours, but front desk likely 24h). Multiple 4-5 star hotels along the lakefront suggest 30-50 night receptionists/security/housekeeping across Montreux.
- **No institutional shuttles found for any facility.**

### Walking Assessment

- **Clinique Valmont to Territet funicular station:** ~1.2 km, steep descent on winding mountain road. Elevation drop ~200m. Takes ~20 min downhill on foot. **Very poor lighting at night.** Mountain road with no sidewalk in places. At 02:00, this is an isolated, dark walk. Not realistic for most staff.
- **Clinique Valmont to Montreux gare:** ~3.5 km via road. Steep descent followed by lakeside walk. 40-50 min on foot. Not practical at 02:00.
- **Territet station to Montreux gare:** ~1.5 km along lakefront. Flat, relatively well-lit promenade. 18 min walk. Reasonable.
- **Hotels to Montreux gare:** Most major hotels (Fairmont, Majestic) are adjacent to or within 300m of the station. No walking issue.
- **Clinic Les Alpes (Les Avants) to any transit:** Completely isolated at night. 800m+ altitude, no funicular access, rack railway stops by early evening. Staff must drive.

### Who Is Here at 02:00?

- **Clinique Valmont night staff:** 15-25 people (nurses, care assistants, night watch). Physically at the clinic in Glion, 300m above Montreux. Trapped at altitude after 01:11 funicular.
- **Clinic Les Alpes night staff:** 10-20 people. At Les Avants, even more isolated. Car-dependent.
- **Hotel night receptionists/security:** 30-50 across Montreux lakefront hotels. At station level — transit-proximate but transit is dead.
- **Late-closing bar/club workers:** Montreux has a more active nightlife than Vevey. Perhaps 20-40 additional workers.
- **Estimated total at 02:00:** 75-135 individuals across altitude zones.

### Data Confidence Summary

| Finding | Confidence | Source |
|---------|-----------|--------|
| Rail dead window 00:56-04:43 | HIGH | existing_data_brief.md (SBB CSV) |
| **Territet-Glion funicular 01:11-05:11** | **HIGH** | Moovit, mob.ch, multiple sources consistent |
| Funicular operates every 20 min, automatic | HIGH | mob.ch, montreuxriviera.com |
| Glion-Rochers rack = daytime only | HIGH | mob.ch, myswitzerland.com |
| Clinique Valmont ~85 employees, 59 beds | HIGH | LinkedIn, swissmedical.net, which-hospital.ch |
| Clinique Valmont night staff 15-25 | MEDIUM | Estimated from bed count and 24/7 operations |
| Clinic Les Alpes 24/7 staff | MEDIUM | recovery.com, mypremiumeurope.com |
| No institutional shuttles found | MEDIUM | Absence of evidence from web search |
| Hotel night worker estimate 30-50 | LOW | Extrapolated from hotel count; no survey |

### Key Finding

The Territet-Glion funicular running until 01:11 is the **single most important transit finding** for this node. Glion is NOT fully severed during weekday nights — there is a narrow window of connection. However, after 01:11, clinic staff at Clinique Valmont (15-25 people) are locked at altitude in a dark, steep environment with no transit for 4 hours. The altitude separation creates two distinct vulnerability zones: Montreux lakefront (transit-proximate, moderate night population) and Glion/above (transit-severed, small but dependent population of healthcare workers). **The lock should sit at the altitude boundary — at or near Territet funicular station — marking the point where vertical severance begins.**

---

## Node 9 — Rennaz (km 89) — Bridge Lock

### Last/First Departures (Weekday) by Mode

| Mode | Operator | Last Departure | First Departure | Dead Window |
|------|----------|---------------|-----------------|-------------|
| Rail at Villeneuve | SBB/CFF | 00:51 | 04:57 | 4h 06m |
| Bus 201 (VMCV) at Rennaz Hopital | VMCV | ~23:53 | ~05:45 | ~5h 52m |
| Bus 111 (TPC) Aigle-Villeneuve | TPC | ~19:00-20:00 (est.) | ~06:42 (est.) | ~10-11h |
| Bus 120 (CarPostal) Monthey-Villeneuve | CarPostal | Evening (unconfirmed) | Morning (unconfirmed) | Unknown |
| Rail at Rennaz | — | **NO STATION** | **NO STATION** | N/A |

**CRITICAL: Rennaz has no rail station.** The nearest rail is Villeneuve (2.1 km from HRC) or Aigle (further east). All transit to HRC depends on bus connections.

**Notes on VMCV 201:** This is the principal bus link. Service from Rennaz Village runs 05:45-23:53 on weekdays. Last bus from Rennaz Hopital toward Vevey/Villeneuve is approximately 23:53. First bus at approximately 05:45. The line runs every 20 minutes during service hours.

**Notes on TPC 111:** The TPC bus 111 (Aigle-Villeneuve via Rennaz) has more limited hours. Based on available schedule data, evening service likely ends around 19:00-20:00, with morning service starting around 06:42. This is a secondary connection primarily serving daytime commuters.

**Notes on CarPostal 120:** Operates Monthey-Bex-Villeneuve. Schedule details for evening service could not be confirmed from web searches.

### Dead Window Duration

- **Rail (at Villeneuve, 2.1 km away):** 00:51-04:57 = 4h 06m
- **Bus (at HRC Rennaz):** 23:53-05:45 = **5h 52m**
- **Effective dead window AT the hospital: 23:53-04:57 = 5h 04m** (last bus from hospital → first train at Villeneuve). But getting from Villeneuve station to the hospital during dead window requires a 2.1 km walk.
- **True dead window for HRC staff: ~23:53-05:45 = 5h 52m** (bus governs both boundaries at the hospital itself)

**This is the longest dead window of any node with a major institution.** The hospital operates 24/7 with 200-300 night staff, yet has nearly 6 hours without ANY public transit service.

### Institutional Transport

- **HRC Hospital shuttle:** **No dedicated hospital shuttle found.** The hospital's official access documentation directs staff and visitors to VMCV bus 201 from Villeneuve station. Citrap-vaud (public transit advocacy group) has been raising alarm about HRC transit access since 2009, proposing a people mover/automated transit system from a theoretical Rennaz rail stop, but this has not been built.
- **Parking situation:** HRC has 1,965 employees but only 912 parking spaces total (515 for direct staff). This means ~1,450 employees cannot park at work — creating massive car dependency with inadequate supply.
- **Shift system:** Hospital operates 3x8-hour shifts (standard Swiss hospital pattern: approximately 06:00-14:00, 14:00-22:00, 22:00-06:00). The night shift (22:00-06:00) begins BEFORE the bus stops and ends AFTER it resumes — but the overlap is razor-thin: last bus ~23:53, shift start 22:00. Workers arriving for night shift can take the bus. Workers LEAVING the night shift at 06:00 must wait for the 05:45 bus (tight) or have already arranged car transport.
- **Citrap-vaud advocacy:** Long-running campaign for better transit access. Proposals include: a Rennaz stop on the Simplon railway line, an automated people mover, extended VMCV hours. None implemented as of 2026.

### Walking Assessment

- **Villeneuve gare to HRC Rennaz:** ~2.1 km (confirmed by multiple sources). Walking time ~25-30 min.
- **Route:** From Villeneuve station, the path crosses Rue des Remparts then follows the cantonal road (Route 9) toward Rennaz. This is a **cantonal highway** environment.
- **Terrain:** Flat (375m altitude). No hills.
- **Pedestrian infrastructure:** The Route 9 / cantonal road was designed for vehicles, not pedestrians. The VMCV 201 extension from Villeneuve to Rennaz was only completed after a long political battle (public inquiry 2017). Before that, there was effectively no public transit to the hospital site. Pedestrian facilities are limited — this is an inter-village highway corridor, not an urban sidewalk.
- **Safety at 02:00:** **Poor.** Route 9 is a cantonal road connecting Villeneuve to the A9 motorway access. At night, it carries truck traffic (the A9 is a major trans-Alpine route). Limited lighting between the villages. Rennaz commune (population 874) has been studying a village crossing redesign to address traffic overload. The walk passes through an area between villages — not urban, not rural, but a highway interface zone.
- **Realistic at 02:00?** Technically walkable but **highly undesirable and potentially unsafe.** A 25-minute walk along a cantonal highway at night, with truck traffic from the A9, limited lighting, and incomplete pedestrian infrastructure. This is the exact scenario the project's "bridge lock" concept addresses.

### Who Is Here at 02:00?

- **HRC night shift staff:** 200-300 people. Nurses, doctors, care assistants, security, cleaning, kitchen prep, administrative on-call. This is a **major acute-care hospital** — the largest single-site employer on the eastern corridor at night.
- **HRC patients:** ~200-300 inpatients (hospital has significant bed capacity as the merged Riviera-Chablais institution).
- **HRC emergency department:** Open 24/7. Receiving ambulances, walk-in emergencies. Additional emergency staff.
- **Supply chain workers:** Truck drivers delivering to HRC (medications, food, lab samples — Swiss Post Innight Medica operates during these hours).
- **Rennaz village residents:** Minimal (population 874 total). A handful awake.
- **Estimated total at 02:00:** 400-600+ individuals at or around HRC, making this the **highest concentration of night-present people** among all 3 eastern corridor nodes.

### Data Confidence Summary

| Finding | Confidence | Source |
|---------|-----------|--------|
| Rail at Villeneuve 00:51-04:57 | HIGH | existing_data_brief.md (SBB CSV) |
| Rennaz has NO rail station | HIGH | Multiple sources, HRC access docs |
| VMCV 201 last bus ~23:53 from Rennaz | MEDIUM | Moovit schedule data; not verified against official 2025/2026 PDF |
| VMCV 201 first bus ~05:45 from Rennaz | MEDIUM | Moovit schedule data |
| VMCV 201 every 20 min during service | HIGH | HRC official access PDF, multiple sources |
| HRC 1,965 employees | HIGH | 20 Minutes, Transitec parking study |
| HRC 912 parking spaces (515 staff) | HIGH | Transitec parking study, 20 Minutes |
| HRC night staff 200-300 | MEDIUM | existing_data_brief.md (from healthcare research) |
| No hospital shuttle exists | MEDIUM | Absence from HRC official access docs; Citrap advocacy confirms reliance on bus |
| TPC 111 evening hours ~19:00-20:00 | LOW | Partial schedule data only; exact times unconfirmed |
| CarPostal 120 schedule | LOW | PDF exists but detailed times not extracted |
| Walking distance 2.1 km | HIGH | Multiple sources, HRC documentation |
| Walking route along cantonal highway | MEDIUM | Citrap-vaud, commune documents, news articles |
| Walking safety poor at night | MEDIUM | Infrastructure assessment from news coverage; no direct 02:00 observation |

### Key Finding

Rennaz is the **most acute transit desert** in the eastern corridor. A major hospital with 200-300 night staff has a nearly 6-hour dead window at its doorstep, no rail station, no shuttle, and insufficient parking. The 2.1 km walk to Villeneuve station follows a cantonal highway that is unsafe for pedestrians at night. Every night, hundreds of healthcare workers must drive because there is literally no alternative. The bridge lock concept is validated: **the gap between Villeneuve station and HRC is not just distance — it is a hostile, car-dependent highway environment that severs the hospital from the rail network during the hours when its most essential workers are present.**

---

## Cross-Node Observations

### 1. The Eastern Corridor Gradient

The three nodes form a clear gradient of severity:

| Node | Dead Window (all modes) | Night Population | Institutional Dependency | Severity |
|------|------------------------|-----------------|-------------------------|----------|
| 7 - Vevey | 3h 57m | 20-40 (low) | None (Nestle = daytime) | LOW |
| 8 - Montreux-Glion | 3h 32m - 4h 00m | 75-135 (moderate) | Clinique Valmont (altitude-severed) | MEDIUM-HIGH |
| 9 - Rennaz | 5h 52m | 400-600+ (high) | HRC hospital (highway-severed) | CRITICAL |

### 2. The Altitude Pattern

Both Nodes 7 and 8 share an altitude vulnerability that the western corridor lacks:
- **Vevey:** Chardonne/Mont-Pelerin funicular stops at 00:07 — hilltop residents stranded
- **Montreux:** Territet-Glion funicular stops at 01:11 — clinic staff stranded
- **Above Glion:** Rack railway is daytime-only — Rochers-de-Naye/Caux permanently severed at night

The funiculars are **lifelines that define the dead window at altitude.** Their operating hours directly determine who is locked up and who can descend.

### 3. VMCV as the Regional Backbone

VMCV line 201 is the single most important bus route for all three nodes. It runs Vevey-La Tour-de-Peilz-Montreux-Villeneuve-Rennaz. Its weekday service window (~05:25/05:45 to ~23:53/midnight) defines the bus dead window across the entire eastern corridor. Any extension of VMCV 201 evening service would benefit all three nodes simultaneously.

### 4. No Institutional Shuttles Anywhere

Despite:
- A major hospital (HRC, 1,965 employees)
- Multiple clinics (Valmont, Les Alpes)
- Dozens of hotels with night staff
- Nestle's headquarters

...there is **zero evidence of any employer-operated night shuttle** in the Vevey-Montreux-Rennaz corridor. Night workers are entirely dependent on public transit (which stops) or private cars (with insufficient parking at HRC).

### 5. The Rennaz Rail Gap

The most significant infrastructure gap in the eastern corridor is the **absence of a rail station at Rennaz.** The Simplon railway line passes within 500m of HRC, but there is no stop. Citrap-vaud has advocated for a Rennaz station since 2009. If built, it would:
- Eliminate the 2.1 km highway walk from Villeneuve
- Potentially enable early morning/late night train stops
- Connect HRC directly to the rail network

This is a known, long-standing, politically contentious gap.

### 6. Tourism vs. Healthcare Night Populations

The eastern corridor's night population splits into two distinct groups:
- **Tourism/hospitality workers** (Vevey + Montreux lakefront): small numbers, dispersed, mostly at station level. Individual problem — each person finds their own way home.
- **Healthcare workers** (Glion clinics + HRC): large concentrated numbers at specific institutions, altitude-separated or highway-separated from transit. Institutional problem — the system fails a whole workforce.

The lock siting should prioritize the institutional concentrations (Glion altitude boundary, Rennaz highway crossing) over the diffuse hotel worker population.

### 7. Data Gaps Requiring Field Verification

| Gap | Why It Matters | How to Verify |
|-----|---------------|---------------|
| Exact VMCV 201 last departure per stop (Vevey, Montreux, Villeneuve, Rennaz) | Determines precise dead window start | Download official PDF timetable from tp-info.ch |
| TPC 111 evening schedule details | Determines if there's any secondary bus option | Download from tpc.ch |
| CarPostal 120 evening schedule | Additional connection from Valais side | Download from postauto.ch |
| HRC shift change times (exact) | Determines if 22:00 shift start aligns with last bus | Contact HRC HR department |
| HRC staff commute survey | How many drive vs. bus vs. carpool? | Contact HRC or Citrap-vaud |
| Walking route Villeneuve-HRC: lighting, sidewalk status | Safety assessment for bridge lock concept | Field visit at 02:00 |
| Clinique Valmont: staff commute patterns | How do night staff get to/from Glion? | Contact clinic |
| Territet-Glion funicular: any maintenance closures? | Could temporarily sever Glion completely | Check mob.ch/infotrafic |

---

## Sources

- [VMCV Official Site](https://www.vmcv.ch/)
- [VMCV 2026 Timetable](https://horaire26.vmcv.ch/en/all-lines/)
- [VMCV Line 201 Schedule (tp-info.ch)](https://www.tp-info.ch/sites/default/files/fap/2025/pdf/10.201.pdf)
- [MOB/GoldenPass - Territet-Glion Funicular](https://www.mob.ch/en/stories/territet-glion-funicular)
- [Moovit - Territet-Glion TG Schedule](https://moovitapp.com/index/en/public_transit-line-tg-Gen%C3%A8ve-3522-3753244-161349938-1)
- [Moovit - VCP Funicular Schedule](https://moovitapp.com/index/en/public_transit-line-vcp-Gen%C3%A8ve-3522-3753267-161350096-1)
- [HRC Official Access Document (PDF)](https://www.hopitalrivierachablais.ch/upload/docs/application/pdf/2019-10/acces_a_rennaz_en_voiture_ou_transports_publics.pdf)
- [HRC Official Site](https://www.hopitalrivierachablais.ch/jcms/hrc_20954/fr/centre-hospitalier-de-rennaz)
- [Citrap-vaud - HRC Transport Advocacy](https://www.citrap-vaud.ch/nos-groupes-de-travail/gr-riviera/hopital-riviera-chablais-vaud-valais-hrc/)
- [20 Minutes - Rennaz Hospital Access Problems](https://www.20min.ch/fr/story/rejoindre-lhopital-de-rennaz-peut-ressembler-a-un-long-pensum-181278241240)
- [24 Heures - HRC Access Without Car](https://www.24heures.ch/hrc-aller-a-rennaz-sans-auto-cest-possible-659834329006)
- [Transitec - HRC Parking Study](https://transitec.net/fr/references/presentation-d-etudes/item/11793-gestion-du-stationnement-de-l-hopital-riviera-chablais-hrc-rennaz.html)
- [TPC Line 111 Schedule (PDF)](https://tpc.ch/wp-content/uploads/horaires-2025-111-aigle-villeneuve.pdf)
- [TPC Official Site](https://tpc.ch/)
- [Clinique Valmont - Swiss Medical Network](https://www.swissmedical.net/en/hospitals/valmont)
- [Clinic Les Alpes](https://recovery.com/clinic-les-alpes/)
- [Montreux Riviera Tourism](https://www.montreuxriviera.com/en/P77460/funicular-territet-glion)
- [Nestle Global Addresses](https://www.nestle.com/about/locations/global-addresses)
- [Rennaz Commune](https://rennaz.ch/la-commune)
- [Vevey City - VMCV 2025 Changes](https://www.vevey.ch/actualites/vmcv-nouvelle-offre2025)
- [Montreux City - 2026 Transport Changes](https://www.montreux.ch/news/vue/article/changement-horaire-transports-publics-2026)
