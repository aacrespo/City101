#!/usr/bin/env python3
"""Build script for Passenger Flow 24h animation (Map 2).

Reads Phase 1 + ridership + demographics data, pre-processes into compact JS,
generates visualizations/map2_passenger_flow.html with everything embedded inline.

Same architecture as build_train_pulse.py but with passenger-weighted visuals.
"""
import csv, json, os, sys, math
from collections import defaultdict

BASE = "/Users/andreacrespo/CLAUDE/City101_ClaudeCode"
SRC = os.path.join(BASE, "source/animation")
OUT = os.path.join(BASE, "visualizations/map2_passenger_flow.html")

# Fallback: if source/animation doesn't have a file, try output/
def src_path(filename):
    p = os.path.join(SRC, filename)
    if os.path.exists(p):
        return p
    return os.path.join(BASE, "output", filename)

# ─── Read data ───────────────────────────────────────────────────────────────

print("Reading data...")

# 1. Interpolated train positions (same as Map 1)
trains_by_minute = defaultdict(list)
trip_ids = {}  # trip_id string → integer index
trip_lines = {}  # trip_id string → line_name
line_codes = {"Long-distance": 0, "InterRegio": 1, "RegioExpress": 2, "S-Bahn": 3, "Regional": 4}

with open(src_path("gtfs_corridor_trains_interpolated.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        tid = row["trip_id"]
        if tid not in trip_ids:
            trip_ids[tid] = len(trip_ids)
        if tid not in trip_lines:
            trip_lines[tid] = row["line_name"]
        m = int(row["minute_of_day"])
        lat = round(float(row["lat"]), 4)
        lon = round(float(row["lon"]), 4)
        lc = line_codes.get(row["line_name"], 4)
        trains_by_minute[m].append((lat, lon, trip_ids[tid], lc))

# Cap minute 1439 anomaly
if 1438 in trains_by_minute and 1439 in trains_by_minute:
    cap = len(trains_by_minute[1438])
    if len(trains_by_minute[1439]) > cap * 2:
        trains_by_minute[1439] = trains_by_minute[1439][:cap]

total_entries = sum(len(v) for v in trains_by_minute.values())
print(f"  Trains: {total_entries} entries, {len(trip_ids)} trips, {len(trains_by_minute)} minutes")

# 2. Stations
stations = []
with open(src_path("corridor_station_distances_v3.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        stations.append({
            "n": row["station_name"],
            "lat": round(float(row["lat_wgs84"]), 4),
            "lon": round(float(row["lon_wgs84"]), 4),
            "d": round(float(row["distance_from_geneva_km"]), 1),
        })
print(f"  Stations: {len(stations)}")

# 3. Rail lines GeoJSON
with open(src_path("corridor_rail_lines_v3.geojson"), encoding="utf-8") as f:
    rail_geojson = json.load(f)
print(f"  Rail lines: {len(rail_geojson['features'])} features")

# 4. Station ridership
ridership = {}
with open(os.path.join(BASE, "output/station_ridership_v2.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        name = row["station_name"]
        daily = float(row["daily_avg"])
        hourly = []
        for h in range(24):
            hourly.append(round(float(row[f"pct_h{h:02d}"]), 6))
        ridership[name] = {"daily": daily, "hourly": hourly}
print(f"  Ridership: {len(ridership)} stations")

# 5. Demographics
demographics = {}
with open(os.path.join(BASE, "output/corridor_demographics_v2.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        name = row["station_name"]
        demographics[name] = {
            "pop": int(float(row["population_total"])) if row["population_total"] else 0,
            "a0_19": round(float(row["pct_age_0_19"] or 0), 3),
            "a20_39": round(float(row["pct_age_20_39"] or 0), 3),
            "a40_64": round(float(row["pct_age_40_64"] or 0), 3),
            "a65p": round(float(row["pct_age_65plus"] or 0), 3),
            "pt": round(float(row["pct_commute_public_transport"] or 0), 3),
            "car": round(float(row["pct_commute_car"] or 0), 3),
            "front": int(float(row["frontaliers_estimate"] or 0)),
        }
print(f"  Demographics: {len(demographics)} stations")

# 6. Communes GeoJSON (compact)
with open(os.path.join(BASE, "visualizations/site/data/communes.geojson"), encoding="utf-8") as f:
    communes_raw = json.load(f)

# Keep only essential properties + simplify coordinates
communes = {"type": "FeatureCollection", "features": []}
for feat in communes_raw["features"]:
    props = feat["properties"]
    communes["features"].append({
        "type": "Feature",
        "properties": {
            "name": props.get("NAME", ""),
            "pop": props.get("EINWOHNERZAHL", 0),
        },
        "geometry": feat["geometry"],
    })
print(f"  Communes: {len(communes['features'])} features")

# 7. Raw GTFS timetable — build stop sequences per trip and departure counts
def time_to_minutes(t):
    """Convert HH:MM:SS to minutes. Handles >24h GTFS times."""
    parts = t.split(":")
    h, m = int(parts[0]), int(parts[1])
    return h * 60 + m

trip_stops = defaultdict(list)  # trip_id → [(station, minute)]
station_deps = defaultdict(lambda: defaultdict(int))  # station → hour → count

with open(os.path.join(BASE, "output/gtfs_corridor_trains.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        tid = row["trip_id"]
        sname = row["stop_name"]
        dep_min = time_to_minutes(row["departure_time"])
        trip_stops[tid].append((sname, dep_min))
        hour = min(dep_min // 60, 23)  # cap at 23
        station_deps[sname][hour] += 1

# Sort each trip's stops by minute
for tid in trip_stops:
    trip_stops[tid].sort(key=lambda x: x[1])

print(f"  GTFS timetable: {len(trip_stops)} trips with stop sequences")

# ─── Pre-compute passenger estimates per trip per minute ─────────────────────

print("Computing passenger estimates...")

# For each trip, compute estimated passengers at each minute
# Strategy: at each stop, board = hourlyPax / departures, alight = 15% of accumulated (30% at large hubs)
# Then interpolate between stops

# Build: PAX[tripIdx] = estimated passengers (pre-computed per trip-minute range)
# To keep data small, we store per-trip: [(startMinute, endMinute, paxAtStart, paxAtEnd), ...]
# But even simpler: store a single "average pax" per trip, weighted by ridership

# Actually, let's pre-compute PAX per minute per trip and embed as compact data
# Format: P[minute] = [[tripIdx, pax], ...] — parallel to T[minute]

# First, build a lookup from trip_id string to trip index
trip_id_to_idx = trip_ids  # already have this

# For each trip, compute pax at each minute it's active
trip_pax_by_minute = defaultdict(dict)  # tripIdx → minute → pax

for tid, stops in trip_stops.items():
    if tid not in trip_id_to_idx:
        continue
    tidx = trip_id_to_idx[tid]

    accumulated = 0
    # Process each segment between stops
    for i, (sname, dep_min) in enumerate(stops):
        hour = min(dep_min // 60, 23)

        # Alighting at this stop
        if i > 0:
            # Larger stations get more alighting
            rd = ridership.get(sname, None)
            if rd and rd["daily"] > 20000:
                alight_rate = 0.35  # major hub
            elif rd and rd["daily"] > 5000:
                alight_rate = 0.20  # medium station
            else:
                alight_rate = 0.10  # small station

            # At terminus, everyone alights
            if i == len(stops) - 1:
                alight_rate = 1.0

            accumulated = accumulated * (1 - alight_rate)

        # Boarding at this stop
        rd = ridership.get(sname, None)
        if rd:
            hourly_pax = rd["daily"] * rd["hourly"][hour]
            deps = max(station_deps[sname].get(hour, 1), 1)
            boarding = hourly_pax / deps
            # Scale down: not all pax at station board THIS direction
            # Rough: 50% each direction
            boarding *= 0.5
            accumulated += boarding

        # Record pax for this minute
        dep_min_capped = min(dep_min, 1439)
        trip_pax_by_minute[tidx][dep_min_capped] = max(0, round(accumulated))

        # Interpolate to next stop
        if i < len(stops) - 1:
            next_min = min(stops[i + 1][1], 1439)
            span = next_min - dep_min_capped
            if span > 0:
                for m in range(dep_min_capped + 1, next_min):
                    trip_pax_by_minute[tidx][m] = max(0, round(accumulated))

# Build P[minute] = {tripIdx: pax} — but we merge into T format
# Instead of a separate P dict, extend T entries: T[minute] = [[lat, lon, tripIdx, lineCode, pax], ...]
# This keeps it simple for the JS renderer

trains_by_minute_pax = {}
for m in sorted(trains_by_minute.keys()):
    entries = []
    for (lat, lon, tidx, lc) in trains_by_minute[m]:
        pax = trip_pax_by_minute.get(tidx, {}).get(m, 0)
        entries.append((lat, lon, tidx, lc, pax))
    trains_by_minute_pax[m] = entries

# Compute stats
all_pax = []
for m, entries in trains_by_minute_pax.items():
    for e in entries:
        if e[4] > 0:
            all_pax.append(e[4])

if all_pax:
    print(f"  Passenger estimates: median={sorted(all_pax)[len(all_pax)//2]}, "
          f"max={max(all_pax)}, mean={sum(all_pax)/len(all_pax):.0f}")

    # Hourly totals
    for h in [0, 6, 8, 12, 17, 22]:
        m = h * 60 + 30
        if m in trains_by_minute_pax:
            total = sum(e[4] for e in trains_by_minute_pax[m])
            count = len(trains_by_minute_pax[m])
            print(f"    {h:02d}:30 — {count} trains, ~{total} passengers on corridor")

# Compute station hourly pax for rings
station_hourly_pax = {}
for sname, rd in ridership.items():
    hourly = []
    for h in range(24):
        hourly.append(round(rd["daily"] * rd["hourly"][h]))
    station_hourly_pax[sname] = hourly

print(f"  Station hourly pax computed for {len(station_hourly_pax)} stations")

# ─── Build compact JS data ──────────────────────────────────────────────────

print("Building compact JS data...")

# Train data with pax: T[minute] = [[lat,lon,tripIdx,lineCode,pax],...]
t_parts = []
for m in sorted(trains_by_minute_pax.keys()):
    entries = trains_by_minute_pax[m]
    rows = ",".join(f"[{e[0]},{e[1]},{e[2]},{e[3]},{e[4]}]" for e in entries)
    t_parts.append(f"{m}:[{rows}]")
train_js = "const T={" + ",".join(t_parts) + "};"

# Trip meta: TM[tripIdx] = lineCode
tm_arr = [0] * len(trip_ids)
for tid, idx in trip_ids.items():
    tm_arr[idx] = line_codes.get(trip_lines.get(tid, "Regional"), 4)
trip_meta_js = "const TM=[" + ",".join(str(x) for x in tm_arr) + "];"

# Stations with ridership
st_data = []
for s in stations:
    rd = ridership.get(s["n"], None)
    hp = station_hourly_pax.get(s["n"], [0]*24)
    st_data.append({
        "n": s["n"],
        "lat": s["lat"],
        "lon": s["lon"],
        "d": s["d"],
        "daily": rd["daily"] if rd else 0,
        "hp": hp,
    })
st_js = "const ST=" + json.dumps(st_data, separators=(",", ":")) + ";"

# Rail lines
rail_js = "const RL=" + json.dumps(rail_geojson, separators=(",", ":")) + ";"

# Demographics per station
demo_js = "const DM=" + json.dumps(demographics, separators=(",", ":")) + ";"

# Communes GeoJSON (compact)
communes_js = "const CM=" + json.dumps(communes, separators=(",", ":")) + ";"

data_js = "\n".join([train_js, trip_meta_js, st_js, rail_js, demo_js, communes_js])
print(f"  Data JS size: {len(data_js)/1024:.0f} KB")

# ─── Generate HTML ───────────────────────────────────────────────────────────

print("Generating HTML...")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Passenger Flow — 24h Geneva–Villeneuve Corridor</title>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=DM+Sans:wght@400;500;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
:root {{
  --chrome-bg: #0a0a0f;
  --chrome-text: #e8e6e1;
  --chrome-accent: #c9a84c;
  --chrome-muted: #8a8880;
  --chrome-surface: rgba(10, 10, 15, 0.85);
  --gold: #C9A227;
  --gold-bright: #E8C547;
  --font-display: 'Instrument Serif', serif;
  --font-body: 'DM Sans', sans-serif;
  --font-mono: 'DM Mono', monospace;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; background: #0c1445; }}
#map {{
  position: fixed; inset: 0; z-index: 1;
  background: #0c1445;
  transition: background-color 0.3s ease;
}}
#train-canvas {{
  position: fixed; inset: 0; z-index: 500;
  pointer-events: none;
}}
.leaflet-tile-pane {{ opacity: 0.12; }}
.leaflet-control-container {{ display: none; }}

/* Chrome panels */
.panel {{
  position: fixed; z-index: 600;
  background: var(--chrome-surface);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 8px;
  padding: 16px 20px;
  color: var(--chrome-text);
  pointer-events: auto;
}}

/* Title */
#title-panel {{
  top: 24px; left: 24px;
}}
#title-panel h1 {{
  font-family: var(--font-display);
  font-size: 32px; font-weight: 400;
  color: var(--chrome-text);
  line-height: 1.1;
}}
#title-panel .subtitle {{
  font-family: var(--font-body);
  font-size: 13px; color: var(--chrome-muted);
  margin-top: 4px;
}}

/* Counters */
#counter-panel {{
  top: 24px; right: 24px;
  text-align: right;
  min-width: 200px;
}}
#counter-panel .time {{
  font-family: var(--font-mono);
  font-size: 36px; font-weight: 500;
  color: var(--chrome-accent);
  line-height: 1;
}}
#counter-panel .pax-count {{
  font-family: var(--font-mono);
  font-size: 18px; color: var(--chrome-text);
  margin-top: 8px;
}}
#counter-panel .pax-count span {{
  color: var(--gold-bright);
  font-weight: 500;
}}
#counter-panel .train-count {{
  font-family: var(--font-mono);
  font-size: 13px; color: var(--chrome-muted);
  margin-top: 4px;
}}
#counter-panel .period {{
  font-family: var(--font-display);
  font-size: 16px; color: var(--chrome-muted);
  font-style: italic;
  margin-top: 6px;
}}
#counter-panel .daily-total {{
  font-family: var(--font-mono);
  font-size: 11px; color: var(--chrome-muted);
  margin-top: 8px;
  border-top: 1px solid rgba(255,255,255,0.08);
  padding-top: 6px;
}}

/* Layer toggles */
#toggle-panel {{
  top: 120px; left: 24px;
  padding: 12px 16px;
}}
.toggle-row {{
  display: flex; align-items: center; gap: 8px;
  cursor: pointer; padding: 4px 0;
  font-family: var(--font-body);
  font-size: 12px; color: var(--chrome-text);
  opacity: 1; transition: opacity 0.2s;
  user-select: none;
}}
.toggle-row.off {{ opacity: 0.35; }}
.toggle-dot {{
  width: 8px; height: 8px; border-radius: 50%;
  flex-shrink: 0;
}}

/* Legend */
#legend-panel {{
  bottom: 100px; left: 24px;
  padding: 12px 16px;
  font-family: var(--font-body);
  font-size: 11px;
}}
#legend-panel .legend-title {{
  font-family: var(--font-body);
  font-size: 11px;
  color: var(--chrome-muted);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}
.legend-scale {{
  display: flex; align-items: center; gap: 6px;
  margin: 4px 0;
}}
.legend-dot {{
  border-radius: 50%;
  background: var(--gold-bright);
  flex-shrink: 0;
}}
.legend-label {{
  color: var(--chrome-muted);
  font-family: var(--font-mono);
  font-size: 10px;
}}

/* Scrubber */
#scrubber-panel {{
  bottom: 24px; left: 24px; right: 24px;
  border-radius: 12px;
  padding: 14px 20px 10px;
  display: flex; flex-direction: column; gap: 8px;
}}
#scrubber-row {{
  display: flex; align-items: center; gap: 12px;
}}
#play-btn {{
  width: 32px; height: 32px;
  background: none; border: 1.5px solid var(--chrome-accent);
  border-radius: 50%; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  color: var(--chrome-accent);
  flex-shrink: 0;
  transition: background 0.2s;
}}
#play-btn:hover {{ background: rgba(201,168,76,0.15); }}
#play-btn svg {{ width: 14px; height: 14px; fill: var(--chrome-accent); }}
#time-slider {{
  flex: 1;
  -webkit-appearance: none; appearance: none;
  height: 3px; background: rgba(255,255,255,0.15);
  border-radius: 2px; outline: none;
  cursor: pointer;
}}
#time-slider::-webkit-slider-thumb {{
  -webkit-appearance: none; appearance: none;
  width: 14px; height: 14px;
  background: var(--chrome-accent);
  border-radius: 50%; cursor: pointer;
  border: none;
}}
#time-slider::-moz-range-thumb {{
  width: 14px; height: 14px;
  background: var(--chrome-accent);
  border-radius: 50%; cursor: pointer;
  border: none;
}}
#speed-row {{
  display: flex; align-items: center; gap: 6px;
  justify-content: flex-end;
}}
.speed-btn {{
  font-family: var(--font-mono);
  font-size: 11px; color: var(--chrome-muted);
  background: none; border: 1px solid rgba(255,255,255,0.1);
  border-radius: 4px; padding: 2px 8px;
  cursor: pointer; transition: all 0.2s;
}}
.speed-btn.active {{
  color: var(--chrome-accent);
  border-color: var(--chrome-accent);
}}
#hour-marks {{
  display: flex; justify-content: space-between;
  padding: 0 26px 0 44px;
  font-family: var(--font-mono);
  font-size: 10px; color: var(--chrome-muted);
}}

/* Station tooltip */
.station-tooltip {{
  font-family: var(--font-body);
  font-size: 12px;
  background: var(--chrome-surface) !important;
  color: var(--chrome-text) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 4px;
  padding: 4px 8px;
  box-shadow: none !important;
}}
.station-tooltip::before {{ display: none !important; }}
.leaflet-tooltip-top:before, .leaflet-tooltip-bottom:before,
.leaflet-tooltip-left:before, .leaflet-tooltip-right:before {{ display: none !important; }}

/* Demographic layer styles */
.commune-poly {{
  stroke: rgba(201, 162, 39, 0.15);
  stroke-width: 0.5;
}}
</style>
</head>
<body>
<div id="map"></div>
<canvas id="train-canvas"></canvas>

<!-- Title -->
<div class="panel" id="title-panel">
  <h1>Passenger Flow</h1>
  <div class="subtitle">Who rides the Geneva\u2013Villeneuve corridor</div>
</div>

<!-- Counters -->
<div class="panel" id="counter-panel">
  <div class="time" id="clock">06:00</div>
  <div class="pax-count">~<span id="pax-count">0</span> passengers</div>
  <div class="train-count"><span id="train-count">0</span> active trains</div>
  <div class="period" id="period-label">Morning Rush</div>
  <div class="daily-total">Daily total: ~<span id="daily-total">0</span></div>
</div>

<!-- Toggles -->
<div class="panel" id="toggle-panel">
  <div class="toggle-row" data-layer="rings">
    <div class="toggle-dot" style="background: rgba(201,162,39,0.6);"></div>
    Station Rings
  </div>
  <div class="toggle-row" data-layer="demos">
    <div class="toggle-dot" style="background: rgba(201,162,39,0.3);"></div>
    Demographics
  </div>
  <div class="toggle-row" data-layer="labels">
    <div class="toggle-dot" style="background: rgba(255,255,255,0.5);"></div>
    Station Labels
  </div>
</div>

<!-- Legend -->
<div class="panel" id="legend-panel">
  <div class="legend-title">Passengers aboard</div>
  <div class="legend-scale">
    <div class="legend-dot" style="width:4px;height:4px;opacity:0.4;"></div>
    <span class="legend-label">&lt; 50</span>
  </div>
  <div class="legend-scale">
    <div class="legend-dot" style="width:8px;height:8px;opacity:0.6;"></div>
    <span class="legend-label">~200</span>
  </div>
  <div class="legend-scale">
    <div class="legend-dot" style="width:14px;height:14px;opacity:0.8;"></div>
    <span class="legend-label">~500</span>
  </div>
  <div class="legend-scale">
    <div class="legend-dot" style="width:20px;height:20px;opacity:1;"></div>
    <span class="legend-label">1000+</span>
  </div>
</div>

<!-- Scrubber -->
<div class="panel" id="scrubber-panel">
  <div id="scrubber-row">
    <button id="play-btn">
      <svg id="play-icon" viewBox="0 0 24 24" style="display:none"><polygon points="6,4 20,12 6,20"/></svg>
      <svg id="pause-icon" viewBox="0 0 24 24"><rect x="5" y="4" width="4" height="16"/><rect x="15" y="4" width="4" height="16"/></svg>
    </button>
    <input type="range" id="time-slider" min="0" max="1439" step="0.5" value="360">
  </div>
  <div id="hour-marks">
    <span>00</span><span>03</span><span>06</span><span>09</span>
    <span>12</span><span>15</span><span>18</span><span>21</span>
  </div>
  <div id="speed-row">
    <button class="speed-btn active" data-speed="1">1\u00d7</button>
    <button class="speed-btn" data-speed="2">2\u00d7</button>
    <button class="speed-btn" data-speed="4">4\u00d7</button>
    <button class="speed-btn" data-speed="8">8\u00d7</button>
  </div>
</div>

<script>
// ─── Embedded data ───────────────────────────────────────────────────────
{data_js}

// ─── Sky color system ────────────────────────────────────────────────────
const SKY = [
  [0,[12,20,69]],[330,[12,20,69]],[360,[45,27,78]],[390,[74,32,64]],
  [420,[232,146,124]],[450,[240,168,104]],[540,[168,208,230]],
  [600,[135,206,235]],[840,[135,206,235]],[1020,[196,180,132]],
  [1080,[212,160,74]],[1110,[212,118,78]],[1170,[107,58,107]],
  [1230,[12,20,69]],[1440,[12,20,69]]
];

function skyColor(m) {{
  m = ((m % 1440) + 1440) % 1440;
  let i = 0;
  for (let j = 1; j < SKY.length; j++) {{
    if (SKY[j][0] >= m) {{ i = j - 1; break; }}
    if (j === SKY.length - 1) i = j - 1;
  }}
  const [m0, c0] = SKY[i], [m1, c1] = SKY[i + 1];
  const t = m1 > m0 ? (m - m0) / (m1 - m0) : 0;
  const r = Math.round(c0[0] + t * (c1[0] - c0[0]));
  const g = Math.round(c0[1] + t * (c1[1] - c0[1]));
  const b = Math.round(c0[2] + t * (c1[2] - c0[2]));
  return `rgb(${{r}},${{g}},${{b}})`;
}}

function periodLabel(m) {{
  m = ((m % 1440) + 1440) % 1440;
  if (m < 330) return "Night Service";
  if (m < 390) return "First Trains";
  if (m < 540) return "Morning Rush";
  if (m < 690) return "Late Morning";
  if (m < 810) return "Midday";
  if (m < 960) return "Afternoon";
  if (m < 1140) return "Evening Rush";
  if (m < 1260) return "Evening";
  return "Late Night";
}}

function formatTime(m) {{
  m = ((m % 1440) + 1440) % 1440;
  const h = Math.floor(m / 60);
  const mi = Math.floor(m % 60);
  return String(h).padStart(2, '0') + ':' + String(mi).padStart(2, '0');
}}

// ─── Leaflet setup ───────────────────────────────────────────────────────
const map = L.map('map', {{
  center: [46.38, 6.55],
  zoom: 11,
  zoomControl: false,
  attributionControl: false,
}});

L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
  maxZoom: 18,
  subdomains: 'abcd',
}}).addTo(map);

// ─── Demographics layer (below rail lines) ──────────────────────────────
let demosVisible = false;
const maxPop = Math.max(...CM.features.map(f => f.properties.pop || 0));

const demosLayer = L.geoJSON(CM, {{
  style: function(f) {{
    const pop = f.properties.pop || 0;
    const t = Math.sqrt(pop / maxPop);
    const r = Math.round(201 + t * 54);
    const g = Math.round(162 + t * 93);
    const b = Math.round(39 + t * 216);
    return {{
      fillColor: `rgb(${{r}},${{g}},${{b}})`,
      fillOpacity: 0.12 + t * 0.2,
      color: 'rgba(201, 162, 39, 0.15)',
      weight: 0.5,
      interactive: false,
    }};
  }}
}});

// Rail lines
L.geoJSON(RL, {{
  style: function(f) {{
    const lt = f.properties.line_type;
    const isMain = lt === 'standard_gauge';
    const isCeva = lt === 'standard_gauge_leman_express';
    return {{
      color: isMain ? '#ffffff' : (isCeva ? '#ffffff' : '#888888'),
      weight: isMain ? 1.8 : (isCeva ? 1.2 : 0.7),
      opacity: isMain ? 0.22 : (isCeva ? 0.18 : 0.1),
      interactive: false,
    }};
  }}
}}).addTo(map);

// Station markers (small fixed dots — rings are drawn on canvas)
const stationMarkers = [];
ST.forEach(function(s) {{
  const m = L.circleMarker([s.lat, s.lon], {{
    radius: 2,
    color: '#ffffff',
    fillColor: '#ffffff',
    fillOpacity: 0.2,
    weight: 0,
    opacity: 0.2,
  }}).bindTooltip(s.n + ' (' + Math.round(s.daily).toLocaleString() + '/day)', {{
    className: 'station-tooltip',
    direction: 'top',
    offset: [0, -6],
  }}).addTo(map);
  stationMarkers.push(m);
}});

// ─── Canvas setup ────────────────────────────────────────────────────────
const canvas = document.getElementById('train-canvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {{
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// ─── Layer visibility ────────────────────────────────────────────────────
let ringsVisible = true;
let labelsVisible = true;

document.querySelectorAll('.toggle-row').forEach(function(el) {{
  el.addEventListener('click', function() {{
    const layer = this.dataset.layer;
    if (layer === 'rings') {{
      ringsVisible = !ringsVisible;
      this.classList.toggle('off', !ringsVisible);
    }} else if (layer === 'demos') {{
      demosVisible = !demosVisible;
      this.classList.toggle('off', !demosVisible);
      if (demosVisible) {{
        demosLayer.addTo(map);
      }} else {{
        map.removeLayer(demosLayer);
      }}
    }} else if (layer === 'labels') {{
      labelsVisible = !labelsVisible;
      this.classList.toggle('off', !labelsVisible);
      stationMarkers.forEach(function(m) {{
        if (labelsVisible) m.addTo(map);
        else map.removeLayer(m);
      }});
    }}
  }});
}});

// ─── Animation state ─────────────────────────────────────────────────────
let mapTime = 360;
let playing = true;
let speed = 1;
let lastFrameTs = 0;
const MS_PER_MIN = 500;
let dailyPaxAccum = 0;
let lastAccumMinute = -1;

// ─── Draw passenger-weighted trains + station rings ──────────────────────
function drawScene(mt, now) {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const m0 = Math.floor(mt);
  const m1 = m0 + 1;
  const frac = mt - m0;
  const cur = T[m0] || [];
  const nxt = T[m1 >= 1440 ? 0 : m1] || [];
  const hour = Math.floor(m0 / 60);

  // Build next-minute lookup
  const nxtMap = new Map();
  for (let i = 0; i < nxt.length; i++) {{
    nxtMap.set(nxt[i][2], nxt[i]);
  }}

  // ─── Station rings ────────────────────────────────────────────────────
  if (ringsVisible) {{
    const breathe = 0.15 + 0.12 * Math.sin(now / 1200);
    const maxHourly = 12000; // Lausanne peak ~12k/hr

    for (let i = 0; i < ST.length; i++) {{
      const s = ST[i];
      const hp = s.hp[hour] || 0;
      if (hp < 50) continue;

      const pt = map.latLngToContainerPoint([s.lat, s.lon]);
      const radius = Math.max(4, Math.sqrt(hp / maxHourly) * 40);

      // Outer ring
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, radius, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(201, 162, 39, ${{(breathe * 0.8).toFixed(3)}})`;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Inner glow
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, radius * 0.6, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(201, 162, 39, ${{(breathe * 0.15).toFixed(3)}})`;
      ctx.fill();
    }}
  }}

  // ─── Passenger-weighted train dots ─────────────────────────────────────
  ctx.globalCompositeOperation = 'lighter';
  let activeCount = 0;
  let totalPax = 0;

  for (let i = 0; i < cur.length; i++) {{
    const e = cur[i];
    const tidx = e[2], lc = e[3], pax = e[4];

    // Interpolate position
    let lat = e[0], lon = e[1];
    const n = nxtMap.get(tidx);
    if (n) {{
      lat += frac * (n[0] - e[0]);
      lon += frac * (n[1] - e[1]);
    }}

    const pt = map.latLngToContainerPoint([lat, lon]);

    // Radius scales with sqrt of passengers
    const radius = Math.max(2, Math.sqrt(Math.max(pax, 1)) * 0.45);

    // Opacity: low load = dim, high load = bright
    const loadFrac = Math.min(1, pax / 800);
    const opacity = 0.25 + 0.7 * loadFrac;

    // Gold color with brightness by load
    const r = Math.round(232 + loadFrac * 23);
    const g = Math.round(180 + loadFrac * 17);
    const b = Math.round(50 + loadFrac * 21);

    // Draw dot
    ctx.beginPath();
    ctx.arc(pt.x, pt.y, radius, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${{r}},${{g}},${{b}},${{opacity.toFixed(3)}})`;
    ctx.fill();

    // Outer glow for high-load trains
    if (pax > 200) {{
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, radius * 1.8, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(232,197,71,${{(opacity * 0.12).toFixed(3)}})`;
      ctx.fill();
    }}

    activeCount++;
    totalPax += pax;
  }}

  ctx.globalCompositeOperation = 'source-over';

  // Accumulate daily total
  const currentMinute = Math.floor(mt);
  if (currentMinute !== lastAccumMinute && currentMinute > lastAccumMinute) {{
    // Add boarding passengers for this minute across all stations
    for (let i = 0; i < ST.length; i++) {{
      dailyPaxAccum += (ST[i].hp[hour] || 0) / 60; // per-minute boarding
    }}
    lastAccumMinute = currentMinute;
  }}

  return {{ trains: activeCount, pax: totalPax }};
}}

// ─── Chrome updates ──────────────────────────────────────────────────────
const clockEl = document.getElementById('clock');
const paxCountEl = document.getElementById('pax-count');
const trainCountEl = document.getElementById('train-count');
const periodEl = document.getElementById('period-label');
const dailyTotalEl = document.getElementById('daily-total');
const sliderEl = document.getElementById('time-slider');
const mapEl = document.getElementById('map');

function updateChrome(mt, stats) {{
  clockEl.textContent = formatTime(mt);
  paxCountEl.textContent = Math.round(stats.pax).toLocaleString();
  trainCountEl.textContent = stats.trains;
  periodEl.textContent = periodLabel(mt);
  dailyTotalEl.textContent = Math.round(dailyPaxAccum).toLocaleString();
  mapEl.style.backgroundColor = skyColor(mt);
  if (!sliderDragging) sliderEl.value = mt;
}}

// ─── Scrubber interaction ────────────────────────────────────────────────
let sliderDragging = false;

sliderEl.addEventListener('input', function() {{
  const newTime = parseFloat(this.value);
  if (Math.abs(newTime - mapTime) > 60) {{
    // Reset daily accumulation on big jumps
    dailyPaxAccum = 0;
    lastAccumMinute = -1;
  }}
  mapTime = newTime;
  sliderDragging = true;
}});
sliderEl.addEventListener('mousedown', function() {{ sliderDragging = true; }});
sliderEl.addEventListener('touchstart', function() {{ sliderDragging = true; }});
sliderEl.addEventListener('mouseup', function() {{ sliderDragging = false; }});
sliderEl.addEventListener('touchend', function() {{ sliderDragging = false; }});

// Play/pause
const playIcon = document.getElementById('play-icon');
const pauseIcon = document.getElementById('pause-icon');
document.getElementById('play-btn').addEventListener('click', function() {{
  playing = !playing;
  playIcon.style.display = playing ? 'none' : 'block';
  pauseIcon.style.display = playing ? 'block' : 'none';
}});
playIcon.style.display = 'none';
pauseIcon.style.display = 'block';

// Speed buttons
document.querySelectorAll('.speed-btn').forEach(function(btn) {{
  btn.addEventListener('click', function() {{
    speed = parseInt(this.dataset.speed);
    document.querySelectorAll('.speed-btn').forEach(function(b) {{ b.classList.remove('active'); }});
    this.classList.add('active');
  }});
}});

// ─── Main animation loop ────────────────────────────────────────────────
function animate(ts) {{
  if (lastFrameTs === 0) lastFrameTs = ts;
  const dt = Math.min(ts - lastFrameTs, 100);
  lastFrameTs = ts;

  if (playing && !sliderDragging) {{
    mapTime += (dt / MS_PER_MIN) * speed;
    if (mapTime >= 1440) {{
      mapTime -= 1440;
      dailyPaxAccum = 0;
      lastAccumMinute = -1;
    }}
  }}

  const stats = drawScene(mapTime, ts);
  updateChrome(mapTime, stats);
  requestAnimationFrame(animate);
}}

requestAnimationFrame(animate);
</script>
</body>
</html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

size_kb = os.path.getsize(OUT) / 1024
print(f"\nDone! Written to {OUT}")
print(f"  File size: {size_kb:.0f} KB")
print(f"  Embedded data: {len(data_js)/1024:.0f} KB")
print(f"  Stations with ridership: {sum(1 for s in st_data if s['daily'] > 0)}")
print(f"  Communes for choropleth: {len(communes['features'])}")
