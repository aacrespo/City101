# TEMPORAL CORRIDOR FINDINGS
**Generated:** 2026-03-01 (Cairn, Point 2 execution)
**Data:** 49 stations × 7 time slots, transport.opendata.ch

---

## 1. The Archipelago is Structural, Not Temporal

The corridor does NOT pulse dramatically. At peak (07-09), **14** of 49 stations are workable (TWCI > 0.2). At worst (05-07), **13** are workable. A swing of just **1** station(s).

**Implication:** The three structural gaps (Nyon→Gland, Gland→Morges, Lavaux Fracture) persist regardless of time. The corridor is *always* an archipelago — it doesn't temporarily become a city at rush hour.

## 2. Service Window Inequality

- **Widest:** Genève = 21.3h (04:00–01:18)
- **Narrowest (served):** Perroy, Couronnette = 18.1h
- **Zero service:** St-Saphorin (Lavaux) — no trains on either weekday or weekend
- **Average:** 20.2h

**Service tiers:**
- 19h+ (all-day city): 44 stations — Genève, Genève-Eaux-Vives, Morges, Genève-Champel, Lancy-Bachet, Lancy-Pont-Rouge, Genève-Sécheron, Genthod-Bellevue...
- 15-19h: 4 stations
- 10-15h: 0 stations
- <10h (partial access): 0 stations

## 3. Frequency Across the Day

| Slot | Window | Avg freq | Max freq | IC trains | Workable |
|------|--------|----------|----------|-----------|----------|
| early_morning | 05-07 | 8.2 | 53.5 | 104 | 13/49 |
| am_peak | 07-09 | 10.3 | 84.0 | 128 | 14/49 |
| midday | 11-13 | 9.4 | 64.0 | 109 | 14/49 |
| pm_peak | 16-18 | 10.3 | 83.5 | 128 | 14/49 |
| evening | 19-21 | 9.4 | 62.0 | 118 | 14/49 |
| late_night | 21-23 | 7.4 | 38.5 | 72 | 13/49 |
| weekend_mid | Sat 11-13 | 8.7 | 55.5 | 113 | 14/49 |

**Peak moment:** pm_peak (16-18) with 128 IC departures across corridor
**Lowest moment:** late_night (21-23) — IC drops to 72 corridor-wide

## 4. The Lavaux Fracture — Temporal Profile

- **Cully**: TWCI 0.073–0.069, service window 20.2h, first train 05:05
- **Epesses**: TWCI 0.051–0.047, service window 20.1h, first train 05:10
- **Rivaz**: TWCI 0.013–0.008, service window 20.1h, first train 05:06
- **St-Saphorin (Lavaux), gare**: TWCI 0.001–0.001, service window 0.0h, first train 

**Key:** The Lavaux Fracture doesn't 'open' at any time — it's permanently below workable threshold. St-Saphorin has *zero* service. Even at peak, Rivaz TWCI = 0.013.

## 5. The 11pm City

At 11pm, the corridor shrinks to **13 stations**:
- Genève: 0.508
- Vernier, Blandonnet: 0.387
- Lausanne: 0.379
- Lausanne-Flon: 0.340
- Renens VD: 0.330
- Genève-Champel: 0.288
- Prilly-Malley: 0.288
- La Tour-de-Peilz: 0.256
- Genève-Sécheron: 0.248
- Genève-Eaux-Vives: 0.242
- Vevey: 0.226
- Montreux: 0.202
- Nyon: 0.201

**Geographic clustering:** Geneva pole ~5, Lausanne pole ~4, Montreux-Vevey 3, Nyon 1

## 6. Weekend vs Weekday

- Weekday midday avg TWCI: **0.1471**
- Weekend midday avg TWCI: **0.1324** (90% of weekday)

The corridor is **10% less workable on weekends** — fewer workspaces open, slightly reduced frequency. The knowledge worker's corridor is a weekday phenomenon.

## 7. Key Numbers for Narrative

- **14/49** stations are workable at peak — 71% are break points regardless of time
- **13** stations function as a city at 11pm
- **21.3h** longest service window (Genève)
- **0h** service at St-Saphorin — a station with no trains
- **72 IC trains** at night vs **128** at peak — the fast corridor halves
- **0.90x** weekend-to-weekday ratio — the corridor shrinks on Saturday

## 8. Integration with Other Findings

- **Spatial WCI (Point 1):** Temporal analysis confirms the archipelago is structural. The same 11 stations that are spatially workable remain workable at all times.
- **GA Cost (Point 3):** The CHF 20 budget corridor (41km) is the same at all times — the economic barrier is time-invariant.
- **Two corridors (existing):** IC trains drop from 128 at peak to 72 at night — the 'workable corridor' (IC with WiFi/tables) contracts more than the regional one.
- **Diversity (Point 4/Lumen):** Stations with highest Shannon diversity (Genève, Lausanne) also have the widest service windows — diversity requires temporal accessibility.
