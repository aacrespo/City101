# GA Cost Map — Findings
**Date**: 2026-03-01 (Cairn, Session 8)
**Method**: Distance-based SBB tariff estimation, calibrated against known prices
**Accuracy**: ±CHF 2-3 (sufficient for ratio-based argument)

---

## The Core Argument

The same 101km corridor is a different city depending on your ticket type:

| Ticket type | Geneva→Lausanne | Geneva→Villeneuve | Full corridor daily |
|---|---|---|---|
| **Full price** | ~CHF 22.70 | ~CHF 26.00 | CHF 45+ return |
| **Halbtax** | ~CHF 11.35 | ~CHF 13.00 | CHF 22+ return |
| **GA** | CHF 0.00 | CHF 0.00 | CHF 10.58 amortized |

**Cost ratio**: A non-GA traveler pays **2.1–2.5x** more per day than a GA holder to use the same corridor.

## Budget Corridors — "How far is YOUR city?"

If you can only spend this much on a one-way ticket from Geneva:

| Budget | Reaches | Distance | The city ends at... |
|---|---|---|---|
| CHF 10 | Coppet | 13km | La Côte begins, city already ended |
| CHF 15 | Prangins | 23km | Just past Nyon |
| CHF 20 | St-Prex | 41km | Still 12km short of Lausanne |
| CHF 23 | Lausanne | 53km | Halfway through the corridor |
| CHF 26 | Villeneuve | 67km | End of lakeside corridor |

**For a CHF 20 daily transport budget (common for low-income workers), the corridor ends at St-Prex.** They can't even reach Lausanne. The "101km city" is a 41km city for them.

## GA Breakeven

- GA annual: CHF 3,860 (2nd class)
- Geneva-Lausanne return: ~CHF 45
- **GA pays for itself after ~85 return trips (4.2 months of daily commuting)**
- For Geneva-Montreux commuters: breakeven at ~74 trips (3.7 months)
- **Anyone commuting >5 months/year MUST have GA** — it's not a luxury, it's rational

## The Short-Hop Tax

Short hops have the worst cost-per-km — the "minimum fare trap":

| Journey | Distance | Price | Cost/km |
|---|---|---|---|
| Lancy-Bachet → Lancy-Pont-Rouge | 1.4km | CHF 3.60 | CHF 2.57/km |
| Montreux → Territet | 1.5km | CHF 3.60 | CHF 2.40/km |
| Geneva → Lausanne | 53km | CHF 22.70 | CHF 0.43/km |
| Geneva → Villeneuve | 67km | CHF 26.00 | CHF 0.39/km |

**Short-hop riders pay 6x more per km.** These are exactly the "last mile" connections that make a corridor work as one city. The pricing punishes corridor integration.

## The Frontalier Blind Spot

~100,000 cross-border workers in Geneva canton:
- Cannot buy GA (French residents)
- Cannot buy Halbtax (requires Swiss domicile)
- Must buy full-price tickets or Léman Express subscriptions
- They experience the MOST fragmented version of the corridor
- They are the corridor's ghost citizens — present in the data, invisible in the pricing

## Connection to WCI

The GA cost map reveals a **third dimension of corridor fragmentation** beyond the spatial WCI:
1. **Spatial**: Infrastructure gaps (Lavaux Fracture, workspace deserts)
2. **Temporal**: Service frequency variation (42x between stations)
3. **Economic**: Ticket type determines effective corridor length

Together: "If you are THIS kind of person, traveling at THIS time, with THIS ticket, here is where the city breaks."

## Data Files

- `city101_ga_cost_od_pairs.csv` — 35 OD pairs with prices (full, halbtax, GA ratio)
- `city101_ga_cost_corridor.csv` — 49 stations with cumulative distance/price from Geneva + budget thresholds

## Notes

- Prices estimated from calibrated SBB distance-based tariff (rail_multiplier = 1.05)
- Calibrated against: Geneva-Lausanne ~CHF 20 full 2nd class, Geneva-Airport ~CHF 6
- SBB APIs (transport.opendata.ch, timetable.search.ch) don't return pricing
- For the cost RATIO argument, ±CHF 2-3 accuracy is sufficient
- GA annual price: CHF 3,860 (2nd class, 2025)
- Halbtax annual: CHF 185
