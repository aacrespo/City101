# SBB Pricing / GA Cost Map — Claude Code Prompt
**Date**: 2026-03-01
**For**: Cairn (Claude Code) or Lumen
**Context**: A02 desk crit March 2nd 1pm. GA hypothesis — "the same corridor is a different city depending on ticket type."

---

## Goal

Compute the **cost to traverse each segment** of the Geneva→Villeneuve corridor by ticket type. Output: a CSV mapping every station pair to its cost under GA, demi-tarif, and full-price tickets. This becomes the GA cost map — the corridor is literally a different length depending on your wallet.

## The argument

- **GA citizen**: ~CHF 10.50/day amortized (CHF 3,860/year ÷ 365). Every journey = CHF 0. The full corridor is one city.
- **Demi-tarif**: Half-price. Geneva→Lausanne ≈ CHF 13. Each hop has a cost but it's manageable for daily commuters.
- **Full price**: Geneva→Lausanne ≈ CHF 26. The corridor fragments — you only go where you must.
- **Frontalier**: Can't buy GA (French resident). Enters via Léman Express. ~100k in Geneva canton alone.

## Data source

**transport.opendata.ch** — the connections endpoint returns pricing.

```
GET https://transport.opendata.ch/v1/connections?from=Geneva&to=Lausanne
```

Response includes `connections[].sections[].journey.passList` and potentially pricing. **However**, the API may not return prices directly. Alternative approaches:

1. **timetable.search.ch** — the underlying SBB API. Try:
   ```
   GET https://timetable.search.ch/api/route.json?from=Genève&to=Lausanne&num=1
   ```
   Check if response includes `price` or `fare` fields.

2. **SBB price API** — try:
   ```
   GET https://b2p.app.sbb.ch/api/fahrplan/route?from=8501008&to=8501120&date=2026-03-02&time=08:00
   ```
   (8501008 = Genève, 8501120 = Lausanne — these are DIDOK/UIC station codes)

3. **Manual fallback**: If APIs don't return prices, use the known SBB tariff structure:
   - SBB uses distance-based pricing (Distanztarif)
   - Price = base fare + per-km rate
   - Demi-tarif = 50% of full price
   - We can compute distances between stations from coordinates and apply the tariff formula

## Stations (our 49)

Use the station list from `datasets/transit/city101_service_frequency_v2.csv`. Key columns: `name`, `station_id`, `lat_wgs84`, `lon_wgs84`.

## OD pairs (35 from journey workability)

Use the 35 origin-destination pairs from `datasets/corridor_analysis/city101_journey_workability_summary.csv`. These are the journeys people actually make.

## What to compute

For each OD pair:
1. **Full price one-way** (Billett)
2. **Demi-tarif one-way** (with Halbtax)
3. **GA daily amortized cost** (CHF 10.50 regardless of journey)
4. **Cost ratio**: full_price / GA_daily — how many times more expensive is the corridor without GA?
5. **Segment distances** (already have coords, compute haversine)

For the corridor-wide map:
1. **Cumulative cost Geneva→each station** by ticket type
2. **"Effective corridor length"** — if you can only afford CHF 20/day on transport, how far does the corridor extend for you?

## Output

```
city101_ga_cost_map.csv
```
Columns: `from_station, to_station, distance_km, price_full_chf, price_halbtax_chf, ga_daily_chf, cost_ratio_vs_ga, cumulative_from_geneva_full, cumulative_from_geneva_halbtax`

Also write a `GA_COST_FINDINGS.md` with key numbers.

## Key numbers to extract

- Geneva→Lausanne: full vs GA ratio
- Geneva→Villeneuve (full corridor): total cost by ticket type
- The "CHF 20 corridor" — how far can a non-GA user travel before hitting CHF 20?
- Which segments have the worst cost-per-km (likely short hops)?
- Frontalier cost: Annemasse→Geneva→Lausanne without any Swiss pass

## Script pattern

Monolithic. Fetch → process → write → print summary. Same as all other scripts.

```python
# Pseudocode
import requests, csv, math, time

STATIONS = load_csv('datasets/transit/city101_service_frequency_v2.csv')
OD_PAIRS = load_csv('datasets/corridor_analysis/city101_journey_workability_summary.csv')

GA_DAILY = 3860 / 365  # CHF 10.56

results = []
for origin, destination in OD_PAIRS:
    # Try API for price
    price = fetch_sbb_price(origin, destination)
    if not price:
        # Fallback: distance-based estimate
        dist = haversine(origin, destination)
        price = estimate_from_tariff(dist)
    
    results.append({
        'from': origin,
        'to': destination,
        'distance_km': dist,
        'price_full': price,
        'price_halbtax': price / 2,
        'ga_daily': GA_DAILY,
        'cost_ratio': price / GA_DAILY,
    })

write_csv(results, 'datasets/corridor_analysis/city101_ga_cost_map.csv')
```

## SBB distance-based tariff (fallback)

If no API returns prices, use the official SBB Distanztarif structure. As of 2024/2025:

| Distance (km) | Full price (2nd class) |
|----------------|----------------------|
| 1-5 | CHF 3.60 |
| 6-10 | CHF 5.60-7.20 |
| 11-20 | CHF 8.40-13.20 |
| 21-30 | CHF 14.80-19.20 |
| 31-40 | CHF 20.40-24.40 |
| 41-50 | CHF 26.00-30.00 |
| 51-60 | CHF 31.60-35.20 |
| 61-80 | CHF 37.60-44.40 |
| 81-100 | CHF 47.20-52.80 |

These are approximate — exact prices depend on route, not straight-line distance. But for the cost gradient argument, ±CHF 2 doesn't change the story. The ratio is what matters.

## Files on Mac

```
~/CLAUDE/City101_ClaudeCode/
├── datasets/
│   ├── corridor_analysis/
│   │   ├── city101_journey_workability_summary.csv  (35 OD pairs)
│   │   ├── city101_station_crossref_classmates.csv  (49 stations enriched)
│   │   └── city101_break_points.csv
│   └── transit/
│       └── city101_service_frequency_v2.csv  (49 stations with IDs)
├── scripts/  (pattern reference)
└── source/   (frozen, don't modify)
```

## Network access

Allowed domains include `transport.opendata.ch`. Check if `timetable.search.ch` or SBB APIs are accessible. If blocked, use the distance-based tariff fallback — it's good enough for the argument.

## Time budget

This should take 30-60 minutes including API exploration. If the API doesn't return prices after 15 minutes of trying, switch to the distance-based tariff fallback immediately. The cost ratio argument works with approximate prices.
