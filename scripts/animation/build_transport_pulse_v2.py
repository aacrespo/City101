#!/usr/bin/env python3
"""
Build script for Transport Pulse v3 — Multimodal Interactive Map.

v3 features: analytics sidebar (donut, sparkline, mode bars, direction split,
pulse rate), symbology overhaul (ferry wake, size hierarchy, funicular cable),
keyboard help panel, dead window label fix, MapLibre 3D terrain, vector mode.

Output: output/transport_pulse_v2/transport_pulse_24h_v2.html
"""
import csv, json, os, sys
from collections import defaultdict

BASE = "/Users/andreacrespo/CLAUDE/city101"
SRC = os.path.join(BASE, "output/transport_pulse_v2")
ANIM_SRC = os.path.join(BASE, "source/animation")
OUT = os.path.join(SRC, "transport_pulse_24h_v2.html")

MODE_CODES = {
    'ic': 0, 'ir': 1, 're': 2, 'sbahn': 3, 'regional': 4,
    'bus': 5, 'noctambus': 6, 'metro': 7, 'ferry': 8,
    'funicular': 9, 'tram': 10, 'narrowgauge': 11, 'lemanexpress': 12,
}

# ─── Read data ───────────────────────────────────────────────────────────────
print("Reading data...")
positions_by_minute = defaultdict(list)
trip_ids = {}
trip_modes = {}
trip_routes = {}
trip_directions = {}
trip_bus_layers = {}

csv_path = os.path.join(SRC, "gtfs_multimodal_interpolated.csv")
corridor_csv = os.path.join(SRC, "gtfs_multimodal_corridor.csv")

bus_layer_lookup = {}
if os.path.exists(corridor_csv):
    with open(corridor_csv, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            tid = row['trip_id']
            if tid not in bus_layer_lookup and row.get('bus_layer', ''):
                bus_layer_lookup[tid] = row['bus_layer']

with open(csv_path, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        tid = row['trip_id']
        if tid not in trip_ids:
            trip_ids[tid] = len(trip_ids)
        if tid not in trip_modes:
            trip_modes[tid] = row['symbol_code']
            trip_routes[tid] = row['route_name']
            trip_directions[tid] = row['direction']
            trip_bus_layers[tid] = bus_layer_lookup.get(tid, '')
        m = int(row['minute_of_day'])
        lat = round(float(row['lat']), 4)
        lon = round(float(row['lon']), 4)
        mc = MODE_CODES.get(row['symbol_code'], 4)
        positions_by_minute[m].append((lat, lon, trip_ids[tid], mc))

if 1438 in positions_by_minute and 1439 in positions_by_minute:
    cap = len(positions_by_minute[1438])
    if len(positions_by_minute[1439]) > cap * 2:
        positions_by_minute[1439] = positions_by_minute[1439][:cap]

total_entries = sum(len(v) for v in positions_by_minute.values())
print(f"  Positions: {total_entries} entries, {len(trip_ids)} trips")

# ─── Fill 2-minute gaps ──────────────────────────────────────────────────────
print("Filling interpolation gaps...")
trip_minute_data = defaultdict(dict)
for m, entries in positions_by_minute.items():
    for lat, lon, tidx, mc in entries:
        trip_minute_data[tidx][m] = (lat, lon, mc)

filled = 0
for tidx, mdata in trip_minute_data.items():
    sorted_mins = sorted(mdata.keys())
    for i in range(len(sorted_mins) - 1):
        m1, m2 = sorted_mins[i], sorted_mins[i + 1]
        if m2 - m1 == 2:
            d1, d2 = mdata[m1], mdata[m2]
            mid = m1 + 1
            positions_by_minute[mid].append((
                round((d1[0] + d2[0]) / 2, 4),
                round((d1[1] + d2[1]) / 2, 4),
                tidx, d1[2]
            ))
            filled += 1

total_entries = sum(len(v) for v in positions_by_minute.values())
print(f"  Filled {filled} gaps, total entries: {total_entries}")

# ─── Stations + GeoJSON ──────────────────────────────────────────────────────
stations = []
with open(os.path.join(ANIM_SRC, "corridor_station_distances_v3.csv"), encoding='utf-8') as f:
    for row in csv.DictReader(f):
        stations.append({
            "n": row["station_name"],
            "lat": round(float(row["lat_wgs84"]), 4),
            "lon": round(float(row["lon_wgs84"]), 4),
            "d": round(float(row["distance_from_geneva_km"]), 1),
        })

with open(os.path.join(ANIM_SRC, "corridor_rail_lines_v3.geojson"), encoding='utf-8') as f:
    rail_geojson = json.load(f)

route_geo_path = os.path.join(SRC, "route_geometries.geojson")
bus_geojson = {"type": "FeatureCollection", "features": []}
if os.path.exists(route_geo_path):
    with open(route_geo_path, encoding='utf-8') as f:
        bus_geojson = json.load(f)

# ─── Station departures ──────────────────────────────────────────────────────
print("Building station departures...")
station_deps = defaultdict(lambda: defaultdict(list))
canonical_names = {s['n'] for s in stations}
if os.path.exists(corridor_csv):
    with open(corridor_csv, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            sname = row['stop_name']
            if sname not in canonical_names:
                continue
            parts = row['departure_time'].strip().split(':')
            if len(parts) == 3:
                hour = int(parts[0]) % 24
                minute = int(parts[0]) * 60 + int(parts[1])
                mc = MODE_CODES.get(row['symbol_code'], 4)
                station_deps[sname][hour].append({'r': row['route_name'], 'm': mc, 't': minute})

for sname in station_deps:
    for hour in station_deps[sname]:
        station_deps[sname][hour] = sorted(station_deps[sname][hour], key=lambda x: x['t'])[:20]

# ─── Pre-compute analytics data ──────────────────────────────────────────────
print("Pre-computing analytics...")

# tripIdx → effective mode code (handling regional bus)
trip_emc = {}
for tid, idx in trip_ids.items():
    mc = MODE_CODES.get(trip_modes.get(tid, 'regional'), 4)
    if mc == 5 and trip_bus_layers.get(tid, '') == 'regional':
        mc = 99
    trip_emc[idx] = mc

# Sparkline: 96 x 15-min buckets
spark_data = []
peak_by_mode = defaultdict(int)
for bucket in range(96):
    mid = bucket * 15 + 7
    entries = positions_by_minute.get(mid, [])
    mc_counts = defaultdict(int)
    for lat, lon, tidx, mc_raw in entries:
        mc_counts[trip_emc.get(tidx, mc_raw)] += 1
    total = sum(mc_counts.values())
    spark_data.append([total, dict(mc_counts)])
    for mc, cnt in mc_counts.items():
        peak_by_mode[mc] = max(peak_by_mode[mc], cnt)

print(f"  Sparkline: {len(spark_data)} buckets, peak total: {max(s[0] for s in spark_data)}")

# Hourly pulse rate (departures per minute)
hourly_pulse = defaultdict(int)
for sname, hours in station_deps.items():
    for hour_str, deps in hours.items():
        hourly_pulse[int(hour_str)] += len(deps)
for h in hourly_pulse:
    hourly_pulse[h] = round(hourly_pulse[h] / 60, 1)

# ─── Build compact JS data ──────────────────────────────────────────────────
print("Building JS data...")

t_parts = []
for m in sorted(positions_by_minute.keys()):
    rows = ",".join(f"[{e[0]},{e[1]},{e[2]},{e[3]}]" for e in positions_by_minute[m])
    t_parts.append(f"{m}:[{rows}]")
train_js = "const T={" + ",".join(t_parts) + "};"

tm_arr = [0] * len(trip_ids)
for tid, idx in trip_ids.items():
    tm_arr[idx] = MODE_CODES.get(trip_modes.get(tid, 'regional'), 4)
trip_meta_js = "const TM=[" + ",".join(str(x) for x in tm_arr) + "];"

tr_arr = []
for tid in sorted(trip_ids.keys(), key=lambda x: trip_ids[x]):
    tr_arr.append(json.dumps([
        trip_routes.get(tid, ''),
        trip_directions.get(tid, ''),
        trip_bus_layers.get(tid, '')
    ], separators=(',', ':')))
trip_route_js = "const TR=[" + ",".join(tr_arr) + "];"

mc_js = "const MC=" + json.dumps({str(v): k for k, v in MODE_CODES.items()}, separators=(',', ':')) + ";"
st_js = "const ST=" + json.dumps(stations, separators=(',', ':')) + ";"
rail_js = "const RL=" + json.dumps(rail_geojson, separators=(',', ':')) + ";"

bg_str = json.dumps(bus_geojson, separators=(',', ':'))
bg_js = "const BG=" + (bg_str if len(bg_str) < 5*1024*1024 else
    json.dumps({"type":"FeatureCollection","features":[]}, separators=(',',':'))) + ";"

sd_js = "const SD=" + json.dumps(dict(station_deps), separators=(',', ':')) + ";"
spark_js = "const SPARK=" + json.dumps(spark_data, separators=(',', ':')) + ";"
peak_js = "const PEAK=" + json.dumps(dict(peak_by_mode), separators=(',', ':')) + ";"
pulse_js = "const PULSE=" + json.dumps(dict(hourly_pulse), separators=(',', ':')) + ";"

data_js = "\n".join([train_js, trip_meta_js, trip_route_js, mc_js, st_js, rail_js, bg_js, sd_js, spark_js, peak_js, pulse_js])
print(f"  Data JS: {len(data_js)/1024:.0f} KB ({len(data_js)/1024/1024:.1f} MB)")

# ─── Generate HTML ───────────────────────────────────────────────────────────
print("Generating HTML (v3)...")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Transport Pulse v3 — Geneva–Villeneuve Corridor</title>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=DM+Sans:wght@400;500;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.js"></script>
<link href="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.css" rel="stylesheet">
<style>
:root {{
  --bg: #0a0a0f; --text: #e8e6e1; --accent: #c9a84c; --muted: #8a8880;
  --surface: rgba(10,10,15,0.88); --border: rgba(255,255,255,0.06);
  --fd: 'Instrument Serif',serif; --fb: 'DM Sans',sans-serif; --fm: 'DM Mono',monospace;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:100%;height:100%;overflow:hidden;background:var(--bg);}}
#map{{position:fixed;inset:0;z-index:1;background:var(--bg);}}
#pulse-canvas{{position:fixed;inset:0;z-index:500;pointer-events:none;}}
#dead-vignette{{position:fixed;inset:0;z-index:450;pointer-events:none;
  box-shadow:inset 0 0 120px rgba(180,30,30,0);transition:box-shadow .5s ease;}}
#dead-vignette.active{{box-shadow:inset 0 0 120px rgba(180,30,30,0.15);}}
.maplibregl-ctrl{{display:none!important;}}
.maplibregl-canvas{{outline:none;}}

.panel{{position:fixed;z-index:600;background:var(--surface);backdrop-filter:blur(8px);
  -webkit-backdrop-filter:blur(8px);border:1px solid var(--border);border-radius:8px;
  padding:16px 20px;color:var(--text);pointer-events:auto;}}

/* Title */
#title-panel{{top:24px;left:24px;}}
#title-panel h1{{font-family:var(--fd);font-size:28px;font-weight:400;line-height:1.1;}}
#title-panel .sub{{font-family:var(--fb);font-size:12px;color:var(--muted);margin-top:4px;}}
#mode-badge{{display:inline-block;font-family:var(--fm);font-size:9px;padding:2px 6px;
  border-radius:3px;margin-top:6px;background:rgba(201,168,76,0.15);color:var(--accent);
  text-transform:uppercase;letter-spacing:.5px;}}

/* Counter */
#counter-panel{{top:24px;right:24px;text-align:right;min-width:180px;}}
.ctime{{font-family:var(--fm);font-size:36px;font-weight:500;color:var(--accent);line-height:1;}}
.ccount{{font-family:var(--fm);font-size:14px;margin-top:8px;}}
.cperiod{{font-family:var(--fd);font-size:15px;color:var(--muted);font-style:italic;margin-top:6px;}}
#dead-info{{font-family:var(--fm);font-size:11px;color:#e74c3c;margin-top:6px;display:none;}}
@keyframes dp{{0%,100%{{opacity:1;}}50%{{opacity:.5;}}}}
.dead-pulse{{animation:dp 2s ease-in-out infinite;}}

/* Legend */
#legend-panel{{top:130px;left:24px;padding:10px 14px;max-height:calc(100vh - 260px);
  overflow-y:auto;min-width:175px;}}
#legend-panel::-webkit-scrollbar{{width:4px;}}
#legend-panel::-webkit-scrollbar-thumb{{background:rgba(255,255,255,.15);border-radius:2px;}}
.ls-title{{font-family:var(--fb);font-size:10px;color:var(--muted);text-transform:uppercase;
  letter-spacing:.5px;margin-bottom:4px;margin-top:6px;}}
.ls-title:first-child{{margin-top:0;}}
.lr{{display:flex;align-items:center;gap:7px;cursor:pointer;padding:3px 0;
  font-family:var(--fb);font-size:11px;opacity:1;transition:opacity .2s;user-select:none;}}
.lr.off{{opacity:.25;}}
.lr canvas{{width:12px;height:12px;flex-shrink:0;}}
.lr .lc{{font-family:var(--fm);font-size:10px;color:var(--muted);margin-left:auto;}}
.lr .ls{{font-family:var(--fm);font-size:9px;color:var(--accent);cursor:pointer;
  margin-left:4px;opacity:0;transition:opacity .2s;}}
.lr:hover .ls{{opacity:1;}}

/* Tooltip */
#vtip{{position:fixed;z-index:700;background:var(--surface);backdrop-filter:blur(8px);
  border:1px solid rgba(255,255,255,.1);border-radius:6px;padding:8px 12px;
  font-family:var(--fb);font-size:12px;pointer-events:none;display:none;max-width:200px;color:var(--text);}}
.vtr{{font-family:var(--fm);font-weight:500;font-size:13px;}}
.vtm,.vtd{{font-size:10px;color:var(--muted);margin-top:2px;}}

/* Station info */
#sinfo{{position:fixed;z-index:700;top:24px;left:50%;transform:translateX(-50%);
  background:var(--surface);backdrop-filter:blur(12px);border:1px solid var(--border);
  border-radius:10px;padding:16px 20px;display:none;min-width:280px;max-width:400px;
  max-height:300px;overflow-y:auto;color:var(--text);}}
.si-n{{font-family:var(--fd);font-size:18px;margin-bottom:8px;}}
.si-x{{position:absolute;top:8px;right:12px;cursor:pointer;color:var(--muted);font-size:16px;}}
.si-d{{font-family:var(--fm);font-size:11px;padding:2px 0;border-bottom:1px solid rgba(255,255,255,.04);}}
.si-t{{color:var(--accent);margin-right:8px;}}

/* Snapshot */
#snap-modal{{position:fixed;inset:0;z-index:800;background:rgba(0,0,0,.6);display:none;
  align-items:center;justify-content:center;}}
#snap-modal.visible{{display:flex;}}
#snap-box{{background:var(--surface);backdrop-filter:blur(12px);border:1px solid var(--border);
  border-radius:12px;padding:24px 32px;min-width:300px;max-width:500px;color:var(--text);}}
#snap-box h2{{font-family:var(--fd);font-size:22px;margin-bottom:16px;}}
.sr{{display:flex;justify-content:space-between;font-family:var(--fm);font-size:12px;
  padding:3px 0;border-bottom:1px solid rgba(255,255,255,.04);}}
.sr .sl{{color:var(--muted);}}

/* Scrubber */
#scrub{{bottom:24px;left:24px;right:24px;border-radius:12px;padding:14px 20px 10px;
  display:flex;flex-direction:column;gap:6px;}}
#scrub-row{{display:flex;align-items:center;gap:12px;}}
#pbtn{{width:32px;height:32px;background:none;border:1.5px solid var(--accent);
  border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;
  flex-shrink:0;transition:background .2s;}}
#pbtn:hover{{background:rgba(201,168,76,.15);}}
#pbtn svg{{width:14px;height:14px;fill:var(--accent);}}
#sl-wrap{{flex:1;position:relative;height:20px;display:flex;align-items:center;}}
#dz{{position:absolute;left:calc(60/1440*100%);width:calc(240/1440*100%);height:3px;
  background:rgba(231,76,60,.25);border-radius:2px;pointer-events:none;}}
#tslider{{width:100%;-webkit-appearance:none;appearance:none;height:3px;
  background:rgba(255,255,255,.15);border-radius:2px;outline:none;cursor:pointer;
  position:relative;z-index:1;}}
#tslider::-webkit-slider-thumb{{-webkit-appearance:none;width:14px;height:14px;
  background:var(--accent);border-radius:50%;cursor:pointer;border:none;}}
#tslider::-moz-range-thumb{{width:14px;height:14px;background:var(--accent);
  border-radius:50%;cursor:pointer;border:none;}}
#hmarks{{display:flex;justify-content:space-between;padding:0 26px 0 44px;
  font-family:var(--fm);font-size:10px;color:var(--muted);}}
#sprow{{display:flex;align-items:center;gap:6px;justify-content:flex-end;}}
.sbtn{{font-family:var(--fm);font-size:11px;color:var(--muted);background:none;
  border:1px solid rgba(255,255,255,.1);border-radius:4px;padding:2px 8px;cursor:pointer;
  transition:all .2s;}}
.sbtn.active{{color:var(--accent);border-color:var(--accent);}}

/* Analytics sidebar */
#aside{{position:fixed;top:0;right:0;width:280px;height:100%;z-index:650;
  transform:translateX(256px);transition:transform .35s cubic-bezier(.4,0,.2,1);
  pointer-events:none;}}
#aside.open{{transform:translateX(0);}}
#aside-tab{{position:absolute;left:0;top:50%;transform:translateY(-50%);
  width:24px;height:56px;background:var(--surface);backdrop-filter:blur(8px);
  border:1px solid var(--border);border-right:none;border-radius:8px 0 0 8px;
  cursor:pointer;display:flex;align-items:center;justify-content:center;
  pointer-events:auto;color:var(--muted);font-size:14px;transition:color .2s;}}
#aside-tab:hover{{color:var(--accent);}}
#aside-content{{position:absolute;left:24px;top:0;right:0;bottom:0;
  background:var(--surface);backdrop-filter:blur(8px);border-left:1px solid var(--border);
  padding:20px 16px;overflow-y:auto;pointer-events:auto;}}
#aside-content::-webkit-scrollbar{{width:4px;}}
#aside-content::-webkit-scrollbar-thumb{{background:rgba(255,255,255,.15);border-radius:2px;}}
.a-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;}}
.a-header span{{font-family:var(--fd);font-size:18px;}}
.a-close{{cursor:pointer;color:var(--muted);font-size:16px;}}
.a-section{{margin-bottom:16px;}}
.a-label{{font-family:var(--fb);font-size:10px;color:var(--muted);text-transform:uppercase;
  letter-spacing:.5px;margin-bottom:6px;}}
#donut-canvas{{display:block;margin:0 auto;}}
#spark-canvas{{display:block;width:100%;border-radius:4px;background:rgba(255,255,255,.02);}}
.mb-row{{display:flex;align-items:center;gap:6px;padding:2px 0;font-family:var(--fm);font-size:10px;}}
.mb-name{{width:80px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.mb-bar{{flex:1;height:6px;background:rgba(255,255,255,.05);border-radius:3px;overflow:hidden;}}
.mb-fill{{height:100%;border-radius:3px;transition:width .3s ease;}}
.mb-val{{width:28px;text-align:right;color:var(--text);}}
#dir-bar{{display:flex;height:8px;border-radius:4px;overflow:hidden;margin-top:4px;}}
#dir-bar div{{transition:width .3s ease;}}
#dir-labels{{display:flex;justify-content:space-between;font-family:var(--fm);font-size:10px;
  color:var(--muted);margin-top:4px;}}
#pulse-num{{font-family:var(--fm);font-size:28px;font-weight:500;color:var(--accent);}}
#pulse-unit{{font-family:var(--fb);font-size:11px;color:var(--muted);margin-top:2px;}}

/* Keyboard help */
#kb-btn{{position:fixed;bottom:100px;right:24px;z-index:600;width:28px;height:28px;
  background:var(--surface);backdrop-filter:blur(8px);border:1px solid var(--border);
  border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;
  font-family:var(--fm);font-size:13px;color:var(--muted);pointer-events:auto;
  transition:color .2s;}}
#kb-btn:hover{{color:var(--accent);}}
#kb-panel{{position:fixed;bottom:140px;right:24px;z-index:700;background:var(--surface);
  backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:8px;
  padding:12px 16px;display:none;color:var(--text);min-width:200px;}}
#kb-panel.visible{{display:block;}}
.kb-row{{display:flex;gap:12px;padding:2px 0;font-family:var(--fm);font-size:11px;}}
.kb-key{{color:var(--accent);width:50px;text-align:right;}}
.kb-desc{{color:var(--muted);}}

/* MapLibre popup */
.maplibregl-popup-content{{background:var(--surface)!important;color:var(--text)!important;
  font-family:var(--fb)!important;font-size:12px!important;padding:4px 8px!important;
  border-radius:4px!important;border:1px solid rgba(255,255,255,.1)!important;box-shadow:none!important;}}
.maplibregl-popup-tip{{display:none!important;}}
</style>
</head>
<body>
<div id="map"></div>
<canvas id="pulse-canvas"></canvas>
<div id="dead-vignette"></div>

<div id="vtip"><div class="vtr" id="vtr"></div><div class="vtm" id="vtm"></div><div class="vtd" id="vtd"></div></div>

<div id="sinfo">
  <span class="si-x" onclick="closeSI()">&times;</span>
  <div class="si-n" id="si-n"></div>
  <div id="si-d"></div>
</div>

<div id="snap-modal" onclick="closeSS()">
  <div id="snap-box" onclick="event.stopPropagation()">
    <h2 id="snap-t">Snapshot</h2><div id="snap-b"></div>
  </div>
</div>

<div class="panel" id="title-panel">
  <h1>Transport Pulse</h1>
  <div class="sub">Multimodal 24h &mdash; Geneva&ndash;Villeneuve corridor</div>
  <div id="mode-badge">dot mode</div>
</div>

<div class="panel" id="counter-panel">
  <div class="ctime" id="clock">06:00</div>
  <div class="ccount"><span id="vc">0</span> active vehicles</div>
  <div class="cperiod" id="plabel">First Trains</div>
  <div id="dead-info"></div>
</div>

<div class="panel" id="legend-panel"></div>

<!-- Analytics sidebar -->
<div id="aside">
  <div id="aside-tab" onclick="toggleAside()">&#9776;</div>
  <div id="aside-content">
    <div class="a-header"><span>Analytics</span><span class="a-close" onclick="toggleAside()">&times;</span></div>
    <div class="a-section"><canvas id="donut-canvas" width="160" height="160"></canvas></div>
    <div class="a-section">
      <div class="a-label">24h Activity</div>
      <canvas id="spark-canvas" width="240" height="56"></canvas>
    </div>
    <div class="a-section">
      <div class="a-label">Mode Breakdown</div>
      <div id="mbars"></div>
    </div>
    <div class="a-section">
      <div class="a-label">Direction</div>
      <div id="dir-bar"></div>
      <div id="dir-labels"><span id="dl-w">GE&rarr;East 50%</span><span id="dl-e">East&rarr;GE 50%</span></div>
    </div>
    <div class="a-section">
      <div class="a-label">Corridor Pulse</div>
      <div id="pulse-num">0</div>
      <div id="pulse-unit">departures / min across 49 stations</div>
    </div>
  </div>
</div>

<!-- Keyboard help -->
<div id="kb-btn" onclick="toggleKB()">?</div>
<div id="kb-panel">
  <div class="kb-row"><span class="kb-key">Space</span><span class="kb-desc">play / pause</span></div>
  <div class="kb-row"><span class="kb-key">[ ]</span><span class="kb-desc">&plusmn;15 min</span></div>
  <div class="kb-row"><span class="kb-key">1-5</span><span class="kb-desc">speed</span></div>
  <div class="kb-row"><span class="kb-key">B</span><span class="kb-desc">toggle buses</span></div>
  <div class="kb-row"><span class="kb-key">R</span><span class="kb-desc">toggle rail</span></div>
  <div class="kb-row"><span class="kb-key">V</span><span class="kb-desc">vector mode</span></div>
  <div class="kb-row"><span class="kb-key">A</span><span class="kb-desc">analytics</span></div>
  <div class="kb-row"><span class="kb-key">S</span><span class="kb-desc">snapshot</span></div>
  <div class="kb-row"><span class="kb-key">T</span><span class="kb-desc">terrain</span></div>
  <div class="kb-row"><span class="kb-key">P</span><span class="kb-desc">3D / flat</span></div>
  <div class="kb-row"><span class="kb-key">F</span><span class="kb-desc">fullscreen</span></div>
  <div class="kb-row"><span class="kb-key">Esc</span><span class="kb-desc">close panels</span></div>
  <div style="margin-top:6px;font-family:var(--fm);font-size:10px;color:var(--muted);">Right-drag: rotate map</div>
</div>

<div class="panel" id="scrub">
  <div id="scrub-row">
    <button id="pbtn">
      <svg id="pico" viewBox="0 0 24 24"><polygon points="6,4 20,12 6,20"/></svg>
      <svg id="paico" viewBox="0 0 24 24" style="display:none"><rect x="5" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
    </button>
    <div id="sl-wrap"><div id="dz"></div>
      <input type="range" id="tslider" min="0" max="1440" step="0.1" value="360">
    </div>
  </div>
  <div id="hmarks"><span>00</span><span>03</span><span>06</span><span>09</span><span>12</span><span>15</span><span>18</span><span>21</span><span>24</span></div>
  <div id="sprow">
    <span style="font-family:var(--fb);font-size:11px;color:var(--muted);margin-right:4px;">Speed</span>
    <button class="sbtn active" data-speed="1">1&times;</button>
    <button class="sbtn" data-speed="2">2&times;</button>
    <button class="sbtn" data-speed="5">5&times;</button>
    <button class="sbtn" data-speed="10">10&times;</button>
    <button class="sbtn" data-speed="30">30&times;</button>
  </div>
</div>

<script>
{data_js}
</script>
<script>
// ─── Config ──────────────────────────────────────────────────────────────
const C = {{
  0:  {{n:'IC / Long-distance',c:[231,76,60],   sh:'arrow',   td:3, tv:20,sec:'Rail',   sz:7}},
  1:  {{n:'InterRegio',        c:[52,152,219],  sh:'diamond', td:3, tv:20,sec:'Rail',   sz:6}},
  2:  {{n:'RegioExpress',      c:[46,204,113],  sh:'diamond', td:3, tv:20,sec:'Rail',   sz:6}},
  3:  {{n:'S-Bahn',            c:[243,156,18],  sh:'circle',  td:3, tv:15,sec:'Rail',   sz:5}},
  4:  {{n:'Regional',          c:[155,89,182],  sh:'circle',  td:3, tv:15,sec:'Rail',   sz:5}},
  5:  {{n:'Bus (corridor)',    c:[26,188,156],  sh:'square',  td:1, tv:10,sec:'Surface',sz:3.5}},
  6:  {{n:'Noctambus',         c:[0,212,255],   sh:'square',  td:1, tv:10,sec:'Surface',sz:3.5,glow:1}},
  7:  {{n:'Metro',             c:[224,86,160],  sh:'roundsq', td:2, tv:12,sec:'Urban',  sz:5}},
  8:  {{n:'Ferry',             c:[168,216,234], sh:'boat',    td:5, tv:30,sec:'Surface',sz:5,wake:1}},
  9:  {{n:'Funicular',         c:[201,168,76],  sh:'funi',    td:2, tv:12,sec:'Urban',  sz:5}},
  10: {{n:'Tram',              c:[166,226,46],  sh:'circle',  td:2, tv:12,sec:'Urban',  sz:4}},
  11: {{n:'Narrow-gauge',      c:[155,89,182],  sh:'circle',  td:3, tv:15,sec:'Rail',   sz:5}},
  12: {{n:'Léman Express',     c:[255,255,255], sh:'diamond', td:3, tv:20,sec:'Rail',   sz:6}},
  99: {{n:'Bus (regional)',    c:[26,188,156],  sh:'square',  td:1, tv:10,sec:'Surface',sz:3,off:1,alpha:.5}},
}};

// ─── Utils ───────────────────────────────────────────────────────────────
function pLabel(m) {{
  m=((m%1440)+1440)%1440;
  if(m<90) return "Night Quiet";
  if(m<210) return "Night Quiet";
  if(m<300) return "Early Service";
  if(m<390) return "First Trains";
  if(m<540) return "Morning Rush";
  if(m<690) return "Late Morning";
  if(m<810) return "Midday";
  if(m<960) return "Afternoon";
  if(m<1140) return "Evening Rush";
  if(m<1260) return "Evening";
  if(m<1380) return "Late Night";
  return "Night Quiet";
}}
function fmtT(m){{m=((m%1440)+1440)%1440;return `${{String(Math.floor(m/60)).padStart(2,'0')}}:${{String(Math.floor(m%60)).padStart(2,'0')}}`;}}
function isDead(m){{m=((m%1440)+1440)%1440;return m>=90&&m<300;}}
function emc(ti){{if(TM[ti]===5){{const i=TR[ti];if(i&&i[2]==='regional')return 99;}}return TM[ti];}}

// ─── State ───────────────────────────────────────────────────────────────
const vis={{}},mc={{}};let solo=null,peak=0,rMode='dot',vBlend=0,terrOn=true;
let mt=360,play=true,spd=1,lastTs=0,slDrag=false;
const MS=500;
for(const k in C){{vis[k]=!C[k].off;mc[k]=0;}}

// Direction counts
let dirW=0,dirE=0;

// ─── Map ─────────────────────────────────────────────────────────────────
const map=new maplibregl.Map({{
  container:'map',
  style:{{version:8,sources:{{'bm':{{type:'raster',
    tiles:['https://a.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}@2x.png',
           'https://b.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}@2x.png',
           'https://c.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}@2x.png'],
    tileSize:256,maxzoom:18}}}},
    layers:[{{id:'bm',type:'raster',source:'bm',paint:{{'raster-opacity':0.15}}}}],
    glyphs:'https://demotiles.maplibre.org/font/{{fontstack}}/{{range}}.pbf'}},
  center:[6.55,46.38],zoom:11,pitch:50,bearing:-15,maxPitch:80,antialias:true
}});
const sPop=new maplibregl.Popup({{closeButton:false,closeOnClick:false}});

map.on('load',function(){{
  try{{
    map.addSource('dem',{{type:'raster-dem',
      tiles:['https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{{z}}/{{x}}/{{y}}.png'],
      encoding:'terrarium',tileSize:256,maxzoom:15}});
    map.setTerrain({{source:'dem',exaggeration:1.8}});
    map.addLayer({{id:'hs',type:'hillshade',source:'dem',
      paint:{{'hillshade-exaggeration':.5,'hillshade-shadow-color':'#000','hillshade-highlight-color':'#1a1a1a'}}}}, 'bm');
  }}catch(e){{terrOn=false;}}

  map.addSource('rail',{{type:'geojson',data:RL}});
  map.addLayer({{id:'rl',type:'line',source:'rail',paint:{{
    'line-color':'#fff',
    'line-width':['case',['==',['get','line_type'],'standard_gauge'],1.8,
      ['==',['get','line_type'],'standard_gauge_leman_express'],1.2,0.7],
    'line-opacity':['case',['==',['get','line_type'],'standard_gauge'],0.2,
      ['==',['get','line_type'],'standard_gauge_leman_express'],0.15,0.08]}}}});

  if(BG.features&&BG.features.length>0){{
    map.addSource('rg',{{type:'geojson',data:BG}});
    map.addLayer({{id:'rgl',type:'line',source:'rg',paint:{{'line-color':'#1abc9c','line-width':.6,'line-opacity':.06}}}});
  }}

  const stG={{type:'FeatureCollection',features:ST.map(s=>({{type:'Feature',
    properties:{{name:s.n,distance:s.d}},geometry:{{type:'Point',coordinates:[s.lon,s.lat]}}}}))}};
  map.addSource('st',{{type:'geojson',data:stG}});
  map.addLayer({{id:'sd',type:'circle',source:'st',paint:{{'circle-radius':3,'circle-color':'#fff','circle-opacity':.3}}}});
  map.addLayer({{id:'sl',type:'symbol',source:'st',
    layout:{{'text-field':['get','name'],'text-size':10,'text-offset':[0,-1],'text-anchor':'bottom'}},
    paint:{{'text-color':'#8a8880','text-halo-color':'#0a0a0f','text-halo-width':1}},minzoom:12}});

  map.on('mouseenter','sd',function(e){{
    map.getCanvas().style.cursor='pointer';
    sPop.setLngLat(e.features[0].geometry.coordinates).setHTML(e.features[0].properties.name).addTo(map);
  }});
  map.on('mouseleave','sd',function(){{map.getCanvas().style.cursor='';sPop.remove();}});
  map.on('click','sd',function(e){{showSI(e.features[0].properties.name);}});
}});

// ─── Canvas ──────────────────────────────────────────────────────────────
const cv=document.getElementById('pulse-canvas'),cx=cv.getContext('2d');
function rsCv(){{cv.width=innerWidth;cv.height=innerHeight;}}
rsCv();addEventListener('resize',function(){{rsCv();trails.clear();}});

// ─── Spatial grid ────────────────────────────────────────────────────────
const GS=50;let sg={{}},gv=[];
function bsg(v){{sg={{}};gv=v;for(let i=0;i<v.length;i++){{const k=Math.floor(v[i].px/GS)+','+Math.floor(v[i].py/GS);if(!sg[k])sg[k]=[];sg[k].push(i);}}}}
function fvn(px,py,r){{const gx=Math.floor(px/GS),gy=Math.floor(py/GS);let b=null,bd=r*r;
  for(let dx=-1;dx<=1;dx++)for(let dy=-1;dy<=1;dy++){{const c=sg[(gx+dx)+','+(gy+dy)];if(!c)continue;
    for(const i of c){{const v=gv[i],d=(v.px-px)**2+(v.py-py)**2;if(d<bd){{bd=d;b=v;}}}}}}return b;}}

// ─── Trails ──────────────────────────────────────────────────────────────
const trails=new Map();
map.on('moveend',()=>trails.clear());

// ─── Shape drawing ───────────────────────────────────────────────────────
function dShape(x,y,sh,sz,col,a,rot,cfg){{
  cx.save();cx.globalAlpha=a;
  cx.fillStyle=`rgb(${{col[0]}},${{col[1]}},${{col[2]}})`;
  if(cfg&&cfg.glow){{cx.shadowColor=cx.fillStyle;cx.shadowBlur=8+4*Math.sin(Date.now()/300);}}
  cx.translate(x,y);
  if(rot&&(sh==='arrow'))cx.rotate(rot);
  switch(sh){{
    case'arrow':cx.beginPath();cx.moveTo(0,-sz);cx.lineTo(sz*.7,sz*.6);cx.lineTo(0,sz*.3);
      cx.lineTo(-sz*.7,sz*.6);cx.closePath();cx.fill();
      // Bright leading edge for IC/IR
      cx.strokeStyle=`rgba(${{col[0]}},${{col[1]}},${{col[2]}},0.8)`;cx.lineWidth=1.5;
      cx.beginPath();cx.moveTo(-sz*.5,-sz*.7);cx.lineTo(0,-sz);cx.lineTo(sz*.5,-sz*.7);cx.stroke();
      break;
    case'diamond':cx.beginPath();cx.moveTo(0,-sz);cx.lineTo(sz*.7,0);cx.lineTo(0,sz);cx.lineTo(-sz*.7,0);cx.closePath();cx.fill();break;
    case'circle':cx.beginPath();cx.arc(0,0,sz*.55,0,Math.PI*2);cx.fill();break;
    case'square':cx.fillRect(-sz*.45,-sz*.45,sz*.9,sz*.9);break;
    case'roundsq':cx.beginPath();cx.roundRect(-sz*.45,-sz*.45,sz*.9,sz*.9,2);cx.fill();break;
    case'boat':
      // Distinctive boat hull
      cx.beginPath();cx.moveTo(-sz*.5,-sz*.2);cx.quadraticCurveTo(0,-sz*.6,sz*.5,-sz*.2);
      cx.lineTo(sz*.35,sz*.4);cx.quadraticCurveTo(0,sz*.55,-sz*.35,sz*.4);cx.closePath();cx.fill();
      // Mast + flag
      cx.strokeStyle=cx.fillStyle;cx.lineWidth=1;
      cx.beginPath();cx.moveTo(0,-sz*.2);cx.lineTo(0,-sz);cx.stroke();
      cx.beginPath();cx.moveTo(0,-sz);cx.lineTo(sz*.3,-sz*.8);cx.lineTo(0,-sz*.6);cx.fill();
      break;
    case'funi':
      // Triangle + cable line
      cx.beginPath();cx.moveTo(0,-sz*.6);cx.lineTo(sz*.55,sz*.45);cx.lineTo(-sz*.55,sz*.45);cx.closePath();cx.fill();
      cx.strokeStyle=`rgba(${{col[0]}},${{col[1]}},${{col[2]}},0.6)`;cx.lineWidth=1;
      cx.beginPath();cx.moveTo(0,-sz*1.1);cx.lineTo(0,-sz*.6);cx.stroke();
      break;
  }}
  cx.restore();
}}

// ─── Ferry wake effect ───────────────────────────────────────────────────
function drawWake(trail,mt,col){{
  if(trail.length<3)return;
  cx.save();cx.globalCompositeOperation='lighter';
  for(let j=trail.length-2;j>=Math.max(0,trail.length-20);j--){{
    const age=mt-trail[j].m;const tl=5;
    const op=Math.max(0,0.06*(1-age/tl));if(op<=0)continue;
    const p=map.project([trail[j].lon,trail[j].lat]);
    const np=map.project([trail[j+1].lon,trail[j+1].lat]);
    const ang=Math.atan2(np.y-p.y,np.x-p.x);
    const spread=age*2.5;
    const px=Math.sin(ang)*spread,py=-Math.cos(ang)*spread;
    cx.strokeStyle=`rgba(${{col[0]}},${{col[1]}},${{col[2]}},${{op.toFixed(4)}})`;
    cx.lineWidth=.5;
    cx.beginPath();cx.moveTo(p.x-px,p.y-py);cx.lineTo(p.x+px,p.y+py);cx.stroke();
  }}
  cx.restore();
}}

// ─── Draw vehicles ───────────────────────────────────────────────────────
function draw(t){{
  cx.clearRect(0,0,cv.width,cv.height);
  const m0=Math.floor(t),fr=t-m0;
  const cur=T[m0]||[],nxt=T[(m0+1)>=1440?0:m0+1]||[];
  const nm=new Map();for(let i=0;i<nxt.length;i++)nm.set(nxt[i][2],nxt[i]);

  const zm=map.getZoom(),vehs=[];const aSet=new Set();
  for(const k in mc)mc[k]=0;
  dirW=0;dirE=0;

  for(let i=0;i<cur.length;i++){{
    const e=cur[i],ti=e[2],em=emc(ti);
    if(solo!==null&&em!==solo)continue;if(!vis[em])continue;
    let la=e[0],lo=e[1];const n=nm.get(ti);
    if(n){{la+=fr*(n[0]-e[0]);lo+=fr*(n[1]-e[1]);}}
    const pt=map.project([lo,la]);
    if(pt.x<-80||pt.x>cv.width+80||pt.y<-80||pt.y>cv.height+80)continue;
    aSet.add(ti);mc[em]=(mc[em]||0)+1;
    // Direction
    const info=TR[ti];if(info){{if(info[1]==='GE→East')dirW++;else if(info[1]==='East→GE')dirE++;}}

    const cfg=C[em]||C[4];const tl=vBlend>.5?cfg.tv:cfg.td;
    if(!trails.has(ti))trails.set(ti,[]);
    const trail=trails.get(ti);trail.push({{lat:la,lon:lo,m:t}});
    while(trail.length>0&&t-trail[0].m>tl)trail.shift();
    let rot=0;if(trail.length>=2){{const pv=trail[trail.length-2];const pp=map.project([pv.lon,pv.lat]);
      rot=Math.atan2(pt.y-pp.y,pt.x-pp.x)+Math.PI/2;}}
    vehs.push({{px:pt.x,py:pt.y,lat:la,lon:lo,ti,mc:em,rot,trail,cfg}});
  }}
  for(const[ti,trail]of trails){{if(!aSet.has(ti)){{
    while(trail.length>0&&t-trail[0].m>10)trail.shift();if(!trail.length)trails.delete(ti);}}}}

  // ── Dot mode ──
  if(vBlend<1){{
    const da=1-vBlend;
    // Ferry wakes first (under everything)
    for(const v of vehs)if(v.cfg.wake)drawWake(v.trail,t,v.cfg.c);
    // Trail dots
    cx.globalCompositeOperation='lighter';
    for(const v of vehs){{const c=v.cfg.c,tl=v.cfg.td,ba=(v.cfg.alpha||1)*da;
      for(let j=0;j<v.trail.length-1;j++){{const p=v.trail[j],age=t-p.m;
        const op=Math.max(0,.12*ba*(1-age/tl));if(op<=0)continue;
        const pt=map.project([p.lon,p.lat]);
        const r=(v.mc===5||v.mc===99)&&zm<12?.8:1.5;
        cx.beginPath();cx.arc(pt.x,pt.y,r,0,Math.PI*2);
        cx.fillStyle=`rgba(${{c[0]}},${{c[1]}},${{c[2]}},${{op.toFixed(3)}})`;cx.fill();}}}}
    // Heads
    cx.globalCompositeOperation='source-over';
    for(const v of vehs){{const c=v.cfg.c,ba=(v.cfg.alpha||1)*da;
      if((v.mc===5||v.mc===99)&&zm<12){{
        cx.beginPath();cx.arc(v.px,v.py,1.5,0,Math.PI*2);
        cx.fillStyle=`rgba(${{c[0]}},${{c[1]}},${{c[2]}},${{(.7*ba).toFixed(2)}})`;cx.fill();
      }}else{{
        const sz=v.cfg.sz*(zm>=14?1.3:zm>=12?1.1:1);
        dShape(v.px,v.py,v.cfg.sh,sz,c,.9*ba,v.rot,v.cfg);
      }}
    }}
  }}

  // ── Vector mode ──
  if(vBlend>0){{
    const va=vBlend,pulse=.8+.2*Math.sin(Date.now()/2000);
    cx.globalCompositeOperation='lighter';cx.lineCap='round';cx.lineJoin='round';
    for(const v of vehs){{if(v.trail.length<2)continue;
      const c=v.cfg.c,ba=(v.cfg.alpha||1)*va*pulse;
      const pts=v.trail.map(p=>map.project([p.lon,p.lat]));
      // 3-pass glow
      const passes=[[4,.03],[1.5,.08],[.5,.2]];
      for(const[lw,op]of passes){{
        cx.lineWidth=lw;cx.strokeStyle=`rgba(${{c[0]}},${{c[1]}},${{c[2]}},${{(op*ba).toFixed(4)}})`;
        cx.beginPath();cx.moveTo(pts[0].x,pts[0].y);
        for(let j=1;j<pts.length;j++)cx.lineTo(pts[j].x,pts[j].y);cx.stroke();
      }}
    }}
  }}
  cx.globalCompositeOperation='source-over';
  bsg(vehs);
  const total=Object.values(mc).reduce((a,b)=>a+b,0);
  if(total>peak)peak=total;
  return total;
}}

// ─── Analytics sidebar ───────────────────────────────────────────────────
let asideOpen=false;
function toggleAside(){{asideOpen=!asideOpen;document.getElementById('aside').classList.toggle('open',asideOpen);}}

// Donut
const donutCv=document.getElementById('donut-canvas');const dCtx=donutCv.getContext('2d');
function drawDonut(){{
  const w=donutCv.width,h=donutCv.height,cx2=w/2,cy2=h/2;
  const oR=70,iR=46;dCtx.clearRect(0,0,w,h);
  const total=Object.values(mc).reduce((a,b)=>a+b,0);
  if(total===0){{dCtx.fillStyle='#8a8880';dCtx.font='500 22px "DM Mono"';dCtx.textAlign='center';
    dCtx.textBaseline='middle';dCtx.fillText('0',cx2,cy2);return;}}
  let ang=-Math.PI/2;
  // Sort by count descending for visual clarity
  const sorted=Object.entries(mc).filter(([k,v])=>v>0).sort((a,b)=>b[1]-a[1]);
  for(const[k,cnt]of sorted){{
    const cfg=C[k]||C[4],c=cfg.c;const slice=(cnt/total)*Math.PI*2;
    dCtx.beginPath();dCtx.arc(cx2,cy2,oR,ang,ang+slice);dCtx.arc(cx2,cy2,iR,ang+slice,ang,true);
    dCtx.closePath();dCtx.fillStyle=`rgb(${{c[0]}},${{c[1]}},${{c[2]}})`;dCtx.fill();
    ang+=slice;
  }}
  dCtx.fillStyle='#e8e6e1';dCtx.font='500 22px "DM Mono"';dCtx.textAlign='center';
  dCtx.textBaseline='middle';dCtx.fillText(total,cx2,cy2-6);
  dCtx.font='400 10px "DM Sans"';dCtx.fillStyle='#8a8880';dCtx.fillText('vehicles',cx2,cy2+12);
}}

// Sparkline
const spkCv=document.getElementById('spark-canvas');const sCtx=spkCv.getContext('2d');
function drawSparkline(){{
  const w=spkCv.width,h=spkCv.height;sCtx.clearRect(0,0,w,h);
  const mx=Math.max(...SPARK.map(d=>d[0]),1);const bw=w/96;
  for(let i=0;i<96;i++){{
    const[total,modes]=SPARK[i];const bh=total>0?(total/mx)*(h-4):0;
    // Dominant mode color
    let mxMc=4,mxCnt=0;for(const[k,v]of Object.entries(modes))if(v>mxCnt){{mxCnt=v;mxMc=k;}}
    const cfg=C[mxMc]||C[4],c=cfg.c;
    sCtx.fillStyle=`rgba(${{c[0]}},${{c[1]}},${{c[2]}},0.5)`;
    sCtx.fillRect(i*bw,h-bh,bw-.5,bh);
  }}
  // Dead zone shade
  sCtx.fillStyle='rgba(231,76,60,0.08)';sCtx.fillRect(4*bw,0,12*bw,h);
  // Cursor
  const bucket=Math.floor(((mt%1440+1440)%1440)/15);
  sCtx.strokeStyle='#c9a84c';sCtx.lineWidth=1.5;
  sCtx.beginPath();sCtx.moveTo(bucket*bw+bw/2,0);sCtx.lineTo(bucket*bw+bw/2,h);sCtx.stroke();
}}

// Mode bars
function buildModeBars(){{
  const el=document.getElementById('mbars');let html='';
  const order=[0,1,2,3,4,11,12,7,10,9,5,6,8,99];
  for(const k of order){{
    if(!C[k])continue;const cfg=C[k],c=cfg.c;
    html+=`<div class="mb-row"><span class="mb-name">${{cfg.n}}</span>`;
    html+=`<div class="mb-bar"><div class="mb-fill" id="mbf-${{k}}" style="width:0;background:rgb(${{c[0]}},${{c[1]}},${{c[2]}})"></div></div>`;
    html+=`<span class="mb-val" id="mbv-${{k}}">0</span></div>`;
  }}
  el.innerHTML=html;
}}
function updateModeBars(){{
  for(const k in C){{
    const cur=mc[k]||0;const pk=PEAK[k]||1;
    const fill=document.getElementById('mbf-'+k);
    const val=document.getElementById('mbv-'+k);
    if(fill)fill.style.width=Math.min(100,cur/pk*100)+'%';
    if(val)val.textContent=cur;
  }}
}}

// Direction
function updateDir(){{
  const total=dirW+dirE;if(total===0)return;
  const wPct=Math.round(dirW/total*100),ePct=100-wPct;
  document.getElementById('dir-bar').innerHTML=
    `<div style="width:${{wPct}}%;background:#3498db;"></div><div style="width:${{ePct}}%;background:#e74c3c;"></div>`;
  document.getElementById('dl-w').textContent=`GE→East ${{wPct}}%`;
  document.getElementById('dl-e').textContent=`East→GE ${{ePct}}%`;
}}

// Pulse
function updatePulse(){{
  const h=Math.floor(((mt%1440+1440)%1440)/60);
  const rate=PULSE[h]||0;
  document.getElementById('pulse-num').textContent=rate.toFixed(1);
}}

buildModeBars();

let lastSidebarUpdate=0;
function updateSidebar(ts){{
  if(ts-lastSidebarUpdate<200)return;lastSidebarUpdate=ts;
  if(!asideOpen)return;
  drawDonut();drawSparkline();updateModeBars();updateDir();updatePulse();
}}

// ─── Legend ───────────────────────────────────────────────────────────────
function buildLegend(){{
  const p=document.getElementById('legend-panel');
  const secs={{Rail:[],Urban:[],Surface:[]}};
  for(const k in C){{const s=C[k].sec;if(!secs[s])secs[s]=[];secs[s].push(parseInt(k));}}
  let h='';
  for(const sec of['Rail','Urban','Surface']){{
    if(!secs[sec]||!secs[sec].length)continue;
    h+=`<div class="ls-title">${{sec}}</div>`;
    for(const k of secs[sec]){{
      const cfg=C[k],off=cfg.off?' off':'',c=cfg.c;
      h+=`<div class="lr${{off}}" data-mc="${{k}}"><canvas width="12" height="12"></canvas>`;
      h+=`<span>${{cfg.n}}</span><span class="lc" id="lc-${{k}}">0</span>`;
      h+=`<span class="ls" data-mc="${{k}}">solo</span></div>`;
    }}
  }}
  p.innerHTML=h;

  // Draw icons
  p.querySelectorAll('.lr').forEach(row=>{{
    const k=parseInt(row.dataset.mc),cfg=C[k],c=cfg.c;
    const lc=row.querySelector('canvas').getContext('2d');
    lc.fillStyle=`rgb(${{c[0]}},${{c[1]}},${{c[2]}})`;
    switch(cfg.sh){{
      case'arrow':lc.beginPath();lc.moveTo(6,1);lc.lineTo(11,9);lc.lineTo(6,7);lc.lineTo(1,9);lc.closePath();lc.fill();break;
      case'diamond':lc.beginPath();lc.moveTo(6,1);lc.lineTo(11,6);lc.lineTo(6,11);lc.lineTo(1,6);lc.closePath();lc.fill();break;
      case'circle':lc.beginPath();lc.arc(6,6,4,0,Math.PI*2);lc.fill();break;
      case'square':lc.fillRect(3,3,6,6);break;
      case'roundsq':lc.beginPath();lc.roundRect(3,3,6,6,1.5);lc.fill();break;
      case'boat':lc.beginPath();lc.moveTo(1,5);lc.quadraticCurveTo(6,1,11,5);lc.lineTo(9,9);lc.quadraticCurveTo(6,10,3,9);lc.closePath();lc.fill();lc.fillRect(5,1,2,4);break;
      case'funi':lc.beginPath();lc.moveTo(6,3);lc.lineTo(10,9);lc.lineTo(2,9);lc.closePath();lc.fill();lc.strokeStyle=lc.fillStyle;lc.lineWidth=1;lc.beginPath();lc.moveTo(6,0);lc.lineTo(6,3);lc.stroke();break;
    }}
    row.addEventListener('click',function(e){{
      if(e.target.classList.contains('ls'))return;
      if(solo!==null){{solo=null;resetVis();}}else{{vis[k]=!vis[k];this.classList.toggle('off',!vis[k]);}}
      trails.clear();
    }});
  }});
  p.querySelectorAll('.ls').forEach(el=>{{
    el.addEventListener('click',function(e){{
      e.stopPropagation();const k=parseInt(this.dataset.mc);
      if(solo===k){{solo=null;resetVis();}}else{{
        solo=k;for(const m in C)vis[m]=false;vis[k]=true;
        p.querySelectorAll('.lr').forEach(r=>r.classList.toggle('off',parseInt(r.dataset.mc)!==k));
      }}trails.clear();
    }});
  }});
}}
function resetVis(){{
  const p=document.getElementById('legend-panel');p.querySelectorAll('.lr').forEach(r=>r.classList.remove('off'));
  for(const k in C){{vis[k]=!C[k].off;if(C[k].off){{const r=p.querySelector(`[data-mc="${{k}}"]`);if(r)r.classList.add('off');}}}}
}}
function updLC(){{for(const k in mc){{const el=document.getElementById('lc-'+k);if(el)el.textContent=mc[k]||0;}}}}
buildLegend();

// ─── Station info ────────────────────────────────────────────────────────
function showSI(name){{
  document.getElementById('si-n').textContent=name;
  const cm=Math.floor(mt),ch=Math.floor(cm/60),deps=[];
  const sd=SD[name];if(sd)for(let h=Math.max(0,ch-1);h<=Math.min(23,ch+1);h++){{
    const hd=sd[h];if(hd)for(const d of hd)if(Math.abs(d.t-cm)<=30)deps.push(d);
  }}
  deps.sort((a,b)=>a.t-b.t);
  let h='';if(!deps.length)h='<div style="color:var(--muted);font-size:12px;margin-top:8px;">No departures &plusmn;30 min</div>';
  else for(const d of deps){{
    const past=d.t<cm,mn=C[d.m]?C[d.m].n:'';
    h+=`<div class="si-d" style="${{past?'opacity:.4':''}}">`
      +`<span class="si-t">${{fmtT(d.t)}}</span>${{d.r}} <span style="color:var(--muted);font-size:10px;">(${{mn}})</span></div>`;
  }}
  document.getElementById('si-d').innerHTML=h;
  document.getElementById('sinfo').style.display='block';
}}
function closeSI(){{document.getElementById('sinfo').style.display='none';}}

// ─── Snapshot ────────────────────────────────────────────────────────────
function showSS(){{
  document.getElementById('snap-t').textContent=`Snapshot — ${{fmtT(mt)}}`;
  const total=Object.values(mc).reduce((a,b)=>a+b,0);
  let h=`<div class="sr"><span class="sl">Total</span><span>${{total}}</span></div>`;
  h+=`<div class="sr"><span class="sl">Peak</span><span>${{peak}}</span></div>`;
  h+=`<div class="sr"><span class="sl">Period</span><span>${{pLabel(mt)}}</span></div><div style="height:8px"></div>`;
  for(const k in C)if((mc[k]||0)>0)h+=`<div class="sr"><span class="sl">${{C[k].n}}</span><span>${{mc[k]}}</span></div>`;
  document.getElementById('snap-b').innerHTML=h;
  document.getElementById('snap-modal').classList.add('visible');
  play=false;document.getElementById('pico').style.display='block';document.getElementById('paico').style.display='none';
}}
function closeSS(){{document.getElementById('snap-modal').classList.remove('visible');}}

// ─── KB help ─────────────────────────────────────────────────────────────
function toggleKB(){{document.getElementById('kb-panel').classList.toggle('visible');}}

// ─── Chrome ──────────────────────────────────────────────────────────────
function updChrome(t,cnt){{
  document.getElementById('clock').textContent=fmtT(t);
  document.getElementById('vc').textContent=cnt;
  document.getElementById('plabel').textContent=pLabel(t);
  if(!slDrag)document.getElementById('tslider').value=t;
  updLC();
  const di=document.getElementById('dead-info'),dv=document.getElementById('dead-vignette');
  if(isDead(t)){{
    document.getElementById('clock').classList.add('dead-pulse');
    const m=((t%1440)+1440)%1440;
    if(m>=90&&m<210)di.textContent=`Night quiet — ${{cnt}} vehicles`;
    else di.textContent=`Early service — ${{cnt}} vehicles (peak: ${{peak}})`;
    di.style.display='block';dv.classList.add('active');
  }}else{{document.getElementById('clock').classList.remove('dead-pulse');di.style.display='none';dv.classList.remove('active');}}
}}

// ─── Hover ───────────────────────────────────────────────────────────────
const tip=document.getElementById('vtip');
document.addEventListener('mousemove',function(e){{
  const v=fvn(e.clientX,e.clientY,12);
  if(v){{const info=TR[v.ti];document.getElementById('vtr').textContent=info?info[0]:'Unknown';
    document.getElementById('vtm').textContent=v.cfg.n;document.getElementById('vtd').textContent=info?info[1]:'';
    tip.style.left=(e.clientX+16)+'px';tip.style.top=(e.clientY-10)+'px';tip.style.display='block';
  }}else tip.style.display='none';
}});

// ─── Scrubber ────────────────────────────────────────────────────────────
const sl=document.getElementById('tslider');
sl.addEventListener('input',function(){{const n=parseFloat(this.value);if(Math.abs(n-mt)>60)trails.clear();mt=n;slDrag=true;}});
sl.addEventListener('mousedown',()=>slDrag=true);sl.addEventListener('touchstart',()=>slDrag=true);
sl.addEventListener('mouseup',()=>slDrag=false);sl.addEventListener('touchend',()=>slDrag=false);

document.getElementById('pbtn').addEventListener('click',function(){{
  play=!play;document.getElementById('pico').style.display=play?'none':'block';
  document.getElementById('paico').style.display=play?'block':'none';
}});
document.getElementById('pico').style.display='none';
document.getElementById('paico').style.display='block';
document.querySelectorAll('.sbtn').forEach(b=>{{
  b.addEventListener('click',function(){{spd=parseInt(this.dataset.speed);
    document.querySelectorAll('.sbtn').forEach(x=>x.classList.remove('active'));this.classList.add('active');}});
}});

// ─── Keyboard ────────────────────────────────────────────────────────────
document.addEventListener('keydown',function(e){{
  if(e.target.tagName==='INPUT')return;
  switch(e.key){{
    case' ':e.preventDefault();play=!play;
      document.getElementById('pico').style.display=play?'none':'block';
      document.getElementById('paico').style.display=play?'block':'none';break;
    case'[':mt=Math.max(0,mt-15);trails.clear();break;
    case']':mt=Math.min(1439,mt+15);trails.clear();break;
    case'1':spd=1;uSB();break;case'2':spd=2;uSB();break;case'3':spd=5;uSB();break;
    case'4':spd=10;uSB();break;case'5':spd=30;uSB();break;
    case'b':case'B':vis[5]=!vis[5];vis[99]=vis[5];
      document.querySelectorAll('[data-mc="5"],[data-mc="99"]').forEach(r=>r.classList.toggle('off',!vis[5]));
      trails.clear();break;
    case'r':case'R':const rm=[0,1,2,3,4,11,12],on=rm.some(m=>vis[m]);
      rm.forEach(m=>{{vis[m]=!on;const r=document.querySelector(`[data-mc="${{m}}"]`);if(r)r.classList.toggle('off',on);}});
      trails.clear();break;
    case'v':case'V':rMode=rMode==='dot'?'vector':'dot';
      document.getElementById('mode-badge').textContent=rMode==='dot'?'dot mode':'vector mode';
      trails.clear();break;
    case'a':case'A':toggleAside();break;
    case't':case'T':terrOn=!terrOn;try{{if(terrOn)map.setTerrain({{source:'dem',exaggeration:1.8}});
      else map.setTerrain(null);}}catch(e){{}}break;
    case'p':case'P':map.easeTo({{pitch:map.getPitch()>10?0:50,duration:800}});break;
    case's':case'S':showSS();break;
    case'f':case'F':if(document.fullscreenElement)document.exitFullscreen();
      else document.documentElement.requestFullscreen();break;
    case'?':toggleKB();break;
    case'Escape':closeSS();closeSI();
      document.getElementById('kb-panel').classList.remove('visible');break;
  }}
}});
function uSB(){{document.querySelectorAll('.sbtn').forEach(b=>b.classList.toggle('active',parseInt(b.dataset.speed)===spd));}}

// ─── Animation ───────────────────────────────────────────────────────────
function animate(ts){{
  if(lastTs===0)lastTs=ts;const dt=Math.min(ts-lastTs,100);lastTs=ts;
  const tgt=rMode==='vector'?1:0;
  if(Math.abs(vBlend-tgt)>.01)vBlend+=(tgt-vBlend)*Math.min(1,dt*.004);else vBlend=tgt;
  if(play&&!slDrag){{mt+=(dt/MS)*spd;if(mt>=1440){{mt-=1440;peak=0;trails.clear();}}}}
  const cnt=draw(mt);updChrome(mt,cnt);updateSidebar(ts);
  requestAnimationFrame(animate);
}}
requestAnimationFrame(animate);
</script>
</body>
</html>"""

# ─── Write ────────────────────────────────────────────────────────────────────
print(f"Writing {OUT}...")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

sz = os.path.getsize(OUT) / 1024
print(f"\n{'='*60}")
print("DONE — Transport Pulse v3")
print(f"{'='*60}")
print(f"  Output: {OUT}")
print(f"  Size: {sz:.0f} KB ({sz/1024:.1f} MB)")
print(f"  Trips: {len(trip_ids)}")
print(f"  Entries (gap-filled): {total_entries}")
print(f"  Sparkline: 96 buckets, peak {max(s[0] for s in spark_data)}")
print(f"\n  New in v3:")
print(f"    - Analytics sidebar (donut, sparkline, mode bars, direction, pulse)")
print(f"    - Symbology: ferry wake, IC bright edge, funicular cable, size hierarchy")
print(f"    - Keyboard help panel (?)")
print(f"    - Dead window: 'Night quiet' / 'Early service' labels")
print(f"\n  Open in Chrome: file://{OUT}")
