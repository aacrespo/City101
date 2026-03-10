#!/usr/bin/env python3
"""Build script for Train Pulse 24h animation.

Reads Phase 1 data from source/animation/, pre-processes into compact JS,
generates visualizations/train_pulse_24h.html with everything embedded inline.
"""
import csv, json, os, sys
from collections import defaultdict

BASE = "/Users/andreacrespo/CLAUDE/City101_ClaudeCode"
SRC = os.path.join(BASE, "source/animation")
OUT = os.path.join(BASE, "visualizations/train_pulse_24h.html")

# ─── Read data ───────────────────────────────────────────────────────────────

print("Reading data...")

# 1. Interpolated train positions
trains_by_minute = defaultdict(list)
trip_ids = {}  # trip_id string → integer index
trip_lines = {}  # trip_id string → line_name
line_codes = {"Long-distance": 0, "InterRegio": 1, "RegioExpress": 2, "S-Bahn": 3, "Regional": 4}

with open(os.path.join(SRC, "gtfs_corridor_trains_interpolated.csv"), encoding="utf-8") as f:
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

# Cap minute 1439 anomaly (GTFS >24:00 capped there)
if 1438 in trains_by_minute and 1439 in trains_by_minute:
    cap = len(trains_by_minute[1438])
    if len(trains_by_minute[1439]) > cap * 2:
        trains_by_minute[1439] = trains_by_minute[1439][:cap]

total_entries = sum(len(v) for v in trains_by_minute.values())
print(f"  Trains: {total_entries} entries, {len(trip_ids)} trips, {len(trains_by_minute)} minutes")

# 2. Stations
stations = []
with open(os.path.join(SRC, "corridor_station_distances_v3.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        stations.append({
            "n": row["station_name"],
            "lat": round(float(row["lat_wgs84"]), 4),
            "lon": round(float(row["lon_wgs84"]), 4),
            "d": round(float(row["distance_from_geneva_km"]), 1),
        })
print(f"  Stations: {len(stations)}")

# 3. Rail lines GeoJSON
with open(os.path.join(SRC, "corridor_rail_lines_v3.geojson"), encoding="utf-8") as f:
    rail_geojson = json.load(f)
print(f"  Rail lines: {len(rail_geojson['features'])} features")

# ─── Build compact JS data ──────────────────────────────────────────────────

print("Building compact JS data...")

# Train data: T[minute] = [[lat,lon,tripIdx,lineCode],...]
t_parts = []
for m in sorted(trains_by_minute.keys()):
    entries = trains_by_minute[m]
    rows = ",".join(f"[{e[0]},{e[1]},{e[2]},{e[3]}]" for e in entries)
    t_parts.append(f"{m}:[{rows}]")
train_js = "const T={" + ",".join(t_parts) + "};"

# Trip meta: TM[tripIdx] = lineCode
tm_arr = [0] * len(trip_ids)
for tid, idx in trip_ids.items():
    tm_arr[idx] = line_codes.get(trip_lines.get(tid, "Regional"), 4)
trip_meta_js = "const TM=[" + ",".join(str(x) for x in tm_arr) + "];"

# Stations
st_js = "const ST=" + json.dumps(stations, separators=(",", ":")) + ";"

# Rail lines (compact)
rail_js = "const RL=" + json.dumps(rail_geojson, separators=(",", ":")) + ";"

data_js = "\n".join([train_js, trip_meta_js, st_js, rail_js])
print(f"  Data JS size: {len(data_js)/1024:.0f} KB")

# ─── Generate HTML ───────────────────────────────────────────────────────────

print("Generating HTML...")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Train Pulse — 24h Geneva–Villeneuve Corridor</title>
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
  min-width: 160px;
}}
#counter-panel .time {{
  font-family: var(--font-mono);
  font-size: 36px; font-weight: 500;
  color: var(--chrome-accent);
  line-height: 1;
}}
#counter-panel .count {{
  font-family: var(--font-mono);
  font-size: 16px; color: var(--chrome-text);
  margin-top: 8px;
}}
#counter-panel .period {{
  font-family: var(--font-display);
  font-size: 16px; color: var(--chrome-muted);
  font-style: italic;
  margin-top: 6px;
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
</style>
</head>
<body>
<div id="map"></div>
<canvas id="train-canvas"></canvas>

<!-- Title -->
<div class="panel" id="title-panel">
  <h1>Train Pulse</h1>
  <div class="subtitle">24 hours on the Geneva–Villeneuve corridor</div>
</div>

<!-- Counters -->
<div class="panel" id="counter-panel">
  <div class="time" id="clock">06:00</div>
  <div class="count"><span id="train-count">0</span> active trains</div>
  <div class="period" id="period-label">First Trains</div>
</div>

<!-- Layer toggles -->
<div class="panel" id="toggle-panel">
  <div class="toggle-row" data-line="0"><span class="toggle-dot" style="background:#e74c3c"></span>Long-distance</div>
  <div class="toggle-row" data-line="1"><span class="toggle-dot" style="background:#3498db"></span>InterRegio</div>
  <div class="toggle-row" data-line="2"><span class="toggle-dot" style="background:#2ecc71"></span>RegioExpress</div>
  <div class="toggle-row" data-line="3"><span class="toggle-dot" style="background:#f39c12"></span>S-Bahn</div>
  <div class="toggle-row" data-line="4"><span class="toggle-dot" style="background:#9b59b6"></span>Regional</div>
</div>

<!-- Scrubber -->
<div class="panel" id="scrubber-panel">
  <div id="scrubber-row">
    <button id="play-btn">
      <svg id="play-icon" viewBox="0 0 24 24"><polygon points="6,4 20,12 6,20"/></svg>
      <svg id="pause-icon" viewBox="0 0 24 24" style="display:none"><rect x="5" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
    </button>
    <input type="range" id="time-slider" min="0" max="1440" step="0.1" value="360">
  </div>
  <div id="hour-marks">
    <span>00</span><span>03</span><span>06</span><span>09</span><span>12</span>
    <span>15</span><span>18</span><span>21</span><span>24</span>
  </div>
  <div id="speed-row">
    <span style="font-family:var(--font-body);font-size:11px;color:var(--chrome-muted);margin-right:4px;">Speed</span>
    <button class="speed-btn active" data-speed="1">1×</button>
    <button class="speed-btn" data-speed="2">2×</button>
    <button class="speed-btn" data-speed="5">5×</button>
    <button class="speed-btn" data-speed="10">10×</button>
  </div>
</div>

<script>
{data_js}
</script>
<script>
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

// ─── Period labels ───────────────────────────────────────────────────────
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
  const mm = Math.floor(m % 60);
  return `${{String(h).padStart(2,'0')}}:${{String(mm).padStart(2,'0')}}`;
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

// Station dots
ST.forEach(function(s) {{
  L.circleMarker([s.lat, s.lon], {{
    radius: 2.5,
    color: '#ffffff',
    fillColor: '#ffffff',
    fillOpacity: 0.25,
    weight: 0,
    opacity: 0.25,
  }}).bindTooltip(s.n, {{
    className: 'station-tooltip',
    direction: 'top',
    offset: [0, -6],
  }}).addTo(map);
}});

// ─── Canvas setup ────────────────────────────────────────────────────────
const canvas = document.getElementById('train-canvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {{
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}}
resizeCanvas();
window.addEventListener('resize', function() {{
  resizeCanvas();
  flushTrails();
}});

// ─── Trail tracking ─────────────────────────────────────────────────────
// trails: Map<tripIndex, [{lat, lon, m}]>
const trails = new Map();
const TRAIL_LEN = 3; // minutes of map-time

function flushTrails() {{
  trails.clear();
}}

// Flush trails on map move/zoom (screen coords become stale)
map.on('moveend', flushTrails);
map.on('zoomend', flushTrails);

// ─── Layer visibility ────────────────────────────────────────────────────
const lineVisible = [true, true, true, true, true];

document.querySelectorAll('.toggle-row').forEach(function(el) {{
  el.addEventListener('click', function() {{
    const lc = parseInt(this.dataset.line);
    lineVisible[lc] = !lineVisible[lc];
    this.classList.toggle('off', !lineVisible[lc]);
  }});
}});

// ─── Animation state ─────────────────────────────────────────────────────
let mapTime = 360; // start at 06:00
let playing = true;
let speed = 1;
let lastFrameTs = 0;
let prevMapTime = mapTime;
const MS_PER_MIN = 500; // 1x: 1 map-minute = 500ms → 24h in 12 min

// ─── Draw trains ─────────────────────────────────────────────────────────
function drawTrains(mt) {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const m0 = Math.floor(mt);
  const m1 = m0 + 1;
  const frac = mt - m0;
  const cur = T[m0] || [];
  const nxt = T[m1 >= 1440 ? 0 : m1] || [];

  // Build next-minute lookup for interpolation
  const nxtMap = new Map();
  for (let i = 0; i < nxt.length; i++) {{
    nxtMap.set(nxt[i][2], nxt[i]); // key: tripIndex
  }}

  // Update trail history
  for (let i = 0; i < cur.length; i++) {{
    const e = cur[i];
    const ti = e[2], lc = e[3];
    if (!lineVisible[lc]) continue;

    let lat = e[0], lon = e[1];
    const n = nxtMap.get(ti);
    if (n) {{
      lat += frac * (n[0] - e[0]);
      lon += frac * (n[1] - e[1]);
    }}

    if (!trails.has(ti)) trails.set(ti, []);
    const trail = trails.get(ti);
    trail.push({{lat, lon, m: mt}});
    // Trim old entries
    while (trail.length > 0 && mt - trail[0].m > TRAIL_LEN) {{
      trail.shift();
    }}
  }}

  // Remove trails for trips no longer active
  const activeTripSet = new Set();
  for (let i = 0; i < cur.length; i++) activeTripSet.add(cur[i][2]);
  for (const [ti, trail] of trails) {{
    if (!activeTripSet.has(ti)) {{
      // Keep decaying
      while (trail.length > 0 && mt - trail[0].m > TRAIL_LEN) {{
        trail.shift();
      }}
      if (trail.length === 0) trails.delete(ti);
    }}
  }}

  // Line category colors: [r,g,b]
  const LC = [[231,76,60],[52,152,219],[46,204,113],[243,156,18],[155,89,182]];

  // Draw all trail points with additive blending
  ctx.globalCompositeOperation = 'lighter';
  let activeCount = 0;

  for (const [ti, trail] of trails) {{
    const lc = TM[ti];
    if (!lineVisible[lc]) continue;
    const c = LC[lc];

    for (let j = 0; j < trail.length; j++) {{
      const p = trail[j];
      const age = mt - p.m;
      const opacity = Math.max(0, 0.15 * (1 - age / TRAIL_LEN));
      if (opacity <= 0) continue;

      const pt = map.latLngToContainerPoint([p.lat, p.lon]);
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, 2, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${{c[0]}},${{c[1]}},${{c[2]}},${{opacity.toFixed(3)}})`;
      ctx.fill();
    }}

    // Draw head (latest position) brighter
    if (trail.length > 0 && activeTripSet.has(ti)) {{
      const head = trail[trail.length - 1];
      const pt = map.latLngToContainerPoint([head.lat, head.lon]);
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, 3, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${{c[0]}},${{c[1]}},${{c[2]}},0.9)`;
      ctx.fill();
      activeCount++;
    }}
  }}

  ctx.globalCompositeOperation = 'source-over';
  return activeCount;
}}

// ─── Chrome updates ──────────────────────────────────────────────────────
const clockEl = document.getElementById('clock');
const countEl = document.getElementById('train-count');
const periodEl = document.getElementById('period-label');
const sliderEl = document.getElementById('time-slider');
const mapEl = document.getElementById('map');

function updateChrome(mt, count) {{
  clockEl.textContent = formatTime(mt);
  countEl.textContent = count;
  periodEl.textContent = periodLabel(mt);
  mapEl.style.backgroundColor = skyColor(mt);
  if (!sliderDragging) sliderEl.value = mt;
}}

// ─── Scrubber interaction ────────────────────────────────────────────────
let sliderDragging = false;

sliderEl.addEventListener('input', function() {{
  const newTime = parseFloat(this.value);
  // Detect midnight crossing (large jump backward) → flush trails
  if (Math.abs(newTime - mapTime) > 60) {{
    flushTrails();
  }}
  mapTime = newTime;
  prevMapTime = mapTime;
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
// Show pause icon initially (since playing=true)
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
  const dt = Math.min(ts - lastFrameTs, 100); // cap at 100ms to avoid jumps
  lastFrameTs = ts;

  if (playing && !sliderDragging) {{
    prevMapTime = mapTime;
    mapTime += (dt / MS_PER_MIN) * speed;
    // Midnight wrap → flush trails
    if (mapTime >= 1440) {{
      mapTime -= 1440;
      flushTrails();
    }}
  }}

  const count = drawTrains(mapTime);
  updateChrome(mapTime, count);
  requestAnimationFrame(animate);
}}

requestAnimationFrame(animate);
</script>
</body>
</html>"""

# ─── Write output ─────────────────────────────────────────────────────────────

print(f"Writing {OUT}...")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

size_kb = os.path.getsize(OUT) / 1024
print(f"\n{'='*60}")
print(f"DONE")
print(f"{'='*60}")
print(f"  Output: {OUT}")
print(f"  Size: {size_kb:.0f} KB ({size_kb/1024:.1f} MB)")
print(f"  Trips: {len(trip_ids)}")
print(f"  Minutes with data: {len(trains_by_minute)}")
print(f"  Total train entries: {total_entries}")
print(f"  Stations: {len(stations)}")
print(f"  Rail features: {len(rail_geojson['features'])}")
print(f"\n  Open in Chrome: file://{OUT}")
