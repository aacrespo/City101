# CLAUDE CODE TASK: Journey-Level On-Train Workability Analysis
# City101 Corridor — Geneva to Villeneuve
# Date: 2026-03-01

## CONTEXT
We're analyzing "working continuity" along the Geneva-Villeneuve corridor (101km lakeside).
The question: when you're ON THE TRAIN, can you actually work?

We already have per-station data (train frequency, infrastructure at stops).
What we DON'T have is per-JOURNEY data — actual connections with travel times, 
train types, and intermediate stop counts.

The unit of measurement must be the JOURNEY (e.g., RE33 Genève-Champel → Renens VD, 25 min),
NOT the hop (e.g., Champel → Sécheron, 2 min). Nobody works for one hop.

## API
Use `https://transport.opendata.ch/v1/connections`

Parameters:
- `from`: origin station name (e.g., "Genève")  
- `to`: destination station name (e.g., "Lausanne")
- `date`: "2026-03-03" (Monday, normal workday)
- `time`: varies by time slot
- `limit`: 6 (get several options per time slot)

Response structure (what matters):
```
connections[].duration        # "00d00:33:00" format
connections[].sections[]     # each leg of the journey
  .journey.name              # "IC 1" or "IR 15" or "RE 33" or "S1"
  .journey.category          # "IC", "IR", "RE", "R", "S", "EC", "TGV"
  .departure.station.name
  .arrival.station.name
  .departure.departure       # ISO datetime
  .arrival.arrival           # ISO datetime
  .journey.passList[]        # intermediate stops (count = stop frequency indicator)
```

## STATIONS (the major nodes — we want connections BETWEEN these)

MAJOR_NODES = [
    "Genève",
    "Genève-Aéroport", 
    "Genève-Champel",
    "Genève-Eaux-Vives",
    "Lancy-Bachet",
    "Lancy-Pont-Rouge",
    "Genève-Sécheron",
    "Versoix",
    "Coppet",
    "Nyon",
    "Gland",
    "Rolle",
    "Allaman",
    "Morges",
    "Bussigny",
    "Renens VD",
    "Lausanne",
    "Puidoux",
    "Cully",
    "Vevey",
    "La Tour-de-Peilz",
    "Montreux",
    "Territet",
    "Villeneuve VD",
    "Aigle",
]

## WHAT TO COMPUTE

### Step 1: Fetch connections for key origin-destination pairs
Not ALL pairs (that's 25×24=600). Focus on:
- **Every consecutive pair** along the main line (24 pairs): Genève→Nyon, Nyon→Gland, etc.
- **Every "hub-to-hub" express pair** (the IC/IR journeys): 
  Genève↔Lausanne, Lausanne↔Montreux, Genève↔Nyon, Lausanne↔Vevey,
  Montreux↔Aigle, Genève↔Morges, Morges↔Lausanne, Vevey↔Montreux
- **Key commuter pairs**: Nyon↔Genève, Morges↔Lausanne, Vevey↔Lausanne, Montreux↔Lausanne

### Step 2: Query at 3 time slots
- `08:00` (morning peak — commuter conditions)
- `12:00` (midday — tourist/flexible worker)
- `20:00` (evening — off-peak)

### Step 3: For each connection returned, extract:
- `from_station`: origin
- `to_station`: destination  
- `time_slot`: "08:00" / "12:00" / "20:00"
- `departure_time`: actual departure
- `arrival_time`: actual arrival
- `duration_min`: total travel time in minutes
- `num_sections`: number of legs (1 = direct, 2+ = transfer required)
- `primary_category`: the train type of the longest leg (IC/IR/RE/R/S)
- `line_name`: e.g., "IC 1", "RE 33", "S1"
- `intermediate_stops`: number of stops between origin and destination
- `stops_per_10min`: intermediate_stops / (duration_min/10) — stop density
- `has_transfer`: boolean — does the journey require changing trains?
- `transfer_station`: if has_transfer, where?
- `transfer_wait_min`: if has_transfer, how long?

### Step 4: Compute workability classification per journey
Based on:
1. **Duration** (must be >= 8 min to be "workable" — below that, not worth opening laptop)
2. **Train type** (IC/IR/EC/TGV = WiFi + tables + power; RE = tables + some power; R/S = no WiFi, fold-down trays)
3. **Stop density** (stops_per_10min: <0.5 = smooth ride; 0.5-1.5 = frequent; >1.5 = constant interruption)
4. **Transfer penalty** (transfer = break in work session, especially if >5 min wait on exposed platform)

Classification:
- **PRIME_WORK**: duration >= 15min, IC/IR/RE, stops_per_10min < 1, no transfer
- **WORKABLE**: duration >= 8min, any long-distance type, stops_per_10min < 2
- **MARGINAL**: duration >= 8min but high stop density OR regional only
- **NOT_WORKABLE**: duration < 8min OR very high stop density (metro/tram conditions)
- **BROKEN**: requires transfer with >10 min wait (work session killed by platform break)

### Step 5: Compute comfort indicators
For known train types:
- IC/EC/TGV: WiFi=yes, table=yes, power=yes, quiet_car=yes → comfort_score=4
- IR: WiFi=yes, table=yes, power=yes, quiet_car=sometimes → comfort_score=3
- RE: WiFi=no, table=yes, power=some, quiet_car=no → comfort_score=2
- R/S: WiFi=no, table=fold_down, power=rare, quiet_car=no → comfort_score=1

## OUTPUT FILES

Write to: `/Users/andreacrespo/CLAUDE/City101_ClaudeCode/output/`

**File 1: `city101_journey_workability.csv`**
One row per connection (expect ~300-500 rows total):
from_station, to_station, time_slot, departure_time, arrival_time, duration_min,
num_sections, primary_category, line_name, intermediate_stops, stops_per_10min,
has_transfer, transfer_station, transfer_wait_min, comfort_score, workability_class

**File 2: `city101_journey_workability_summary.csv`**
One row per OD pair (origin-destination), aggregated across time slots:
from_station, to_station, avg_duration_min, best_category, worst_category,
avg_stops_per_10min, pct_prime_work, pct_workable, pct_not_workable,
requires_transfer_pct, overall_workability (PRIME/WORKABLE/MARGINAL/NOT_WORKABLE/BROKEN)

## TECHNICAL NOTES
- Rate limit: 0.5s between API calls minimum. This is an unofficial API.
- The API uses station names, not IDs. Names must match SBB naming exactly.
- If a station name doesn't resolve, try variants (e.g., "Villeneuve VD" vs "Villeneuve")
- Parse duration from "00d00:33:00" format → 33 minutes
- Some connections may have walking sections (category null) — skip those
- Print progress every 10 queries
- Print a summary at the end
- Total estimated API calls: ~50 OD pairs × 3 time slots × 1 call each = ~150 calls
- At 0.5s per call = ~75 seconds total. Very manageable.

## IMPORTANT
This is a MONOLITHIC SCRIPT — do everything in one execution:
fetch → parse → classify → write CSVs → print summary.
Don't explore data interactively. Write the script, run it once.
