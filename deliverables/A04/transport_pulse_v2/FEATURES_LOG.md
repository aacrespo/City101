# Transport Pulse — Feature Log

Every feature, who proposed it, and how it's implemented.

## v1 — Train Pulse (`train_pulse_24h.html`)
Single-mode rail animation. 860 trains as uniform dots with sky-color background.

| Feature | Origin | Implementation |
|---------|--------|----------------|
| 24h animation loop | Studio requirement | Canvas overlay on Leaflet, requestAnimationFrame |
| Sky color system | Design choice | Interpolated RGB array mapping minute → background color |
| 5 rail categories | Data-driven | GTFS route_type + name classification |
| Trail effect | Design choice | Per-vehicle position history with additive blending |
| Scrubber + speed | Usability | HTML range input + speed multiplier buttons |
| Station tooltips | Usability | Leaflet bindTooltip on circle markers |

## v2 — Transport Pulse (multimodal)
All modes: rail, bus, tram, metro, ferry, funicular. 29,135 trips.

| Feature | Origin | Implementation |
|---------|--------|----------------|
| Multimodal GTFS extraction | Plan requirement | All route_types, two bounding boxes (wider for buses) |
| Shape-coded symbols | Plan spec | Per-mode shapes: arrow, diamond, circle, square, boat, triangle |
| Mode colors (12 categories) | Plan + design system | Distinct color per symbol_code, design system compatible |
| Two-layer bus system | Plan spec (Andrea's rule 4) | Corridor buses ON by default, regional OFF. Bus layer field in data |
| Dead window effects | Plan spec | Pulsing clock CSS, red vignette, vehicle count text |
| Legend with solo mode | Plan spec (interactive tool) | Three sections (Rail/Urban/Surface), click toggle, "solo" isolates one mode |
| Vehicle hover tooltip | Plan spec (interactive tool) | 50×50 spatial grid, shows route name + mode + direction |
| Station click departures | Plan spec (interactive tool) | Embedded SD lookup, shows ±30min departures |
| Keyboard shortcuts | Plan spec (interactive tool) | Space, arrows, 1-5, B, R, S, F |
| Snapshot modal (S key) | Plan spec | Pauses + shows vehicle-by-mode stats |
| Viewport culling | Plan spec (performance) | Only draw vehicles within map bounds |
| Zoom-dependent bus detail | Plan spec (performance) | 1px dots at zoom <12, full shapes at zoom ≥12 |
| Fixed dark background | Plan spec | Removed sky color system, fixed #0a0a0f |
| Noctambus glow | Plan spec | Pulsing shadowBlur on noctambus vehicles |

### v2.1 — Three upgrades (Andrea feedback session)

| Feature | Origin | Implementation |
|---------|--------|----------------|
| **Vector/glow mode (V key)** | Andrea: "what if vectors show up and glow, like fractals" | Toggle between dot mode (shaped vehicles) and vector mode. Triple-pass line rendering (wide dim → medium → thin bright) with additive blending. Longer trails (10-30min) create luminous network threads. Overlapping routes compound into bright corridors. Subtle pulse animation. Smooth animated transition between modes via vectorBlend interpolation. |
| **Smooth bus animation** | Andrea: "bus flows are stop framy, very cut" | Gap-filling at build time: for every 2-minute gap in bus interpolation data, insert midpoint-interpolated position. Added 319,132 gap-fill entries. Buses now flow smoothly at 1× speed. |
| **3D terrain (MapLibre GL JS)** | Andrea: "3D map so we can see topography and implications like the funicular" | Replaced Leaflet with MapLibre GL JS. AWS Terrain Tiles (free, Terrarium encoding) with 1.8× exaggeration. 50° initial pitch, -15° bearing for dramatic corridor perspective. T key toggles terrain, P key toggles 3D/flat, right-drag rotates. Hillshade layer for visual depth. Station labels via MapLibre symbol layer at zoom ≥12. |

## v3 — Analytics + Symbology + UI Polish

| Feature | Origin | Implementation |
|---------|--------|----------------|
| **Collapsible analytics sidebar** | Andrea: "sidebar with percentages that can be hidden" | Sliding drawer from right edge. 24px tab always visible (bar chart icon). Press A or click to open. Contains: animated donut chart (mode share), 24h sparkline (pre-computed 96 buckets), mode breakdown bars (current vs peak), direction split (GE↔East balance), corridor pulse rate (deps/min). Glass panel treatment. All live-updating. |
| **Donut chart** | Claude: "animated ring chart showing % of active vehicles" | Canvas-drawn ring, segments by mode color. Center shows total count. Morphs as time scrubs. Trains dominate 06:00, buses mid-morning, nearly empty in dead zone. |
| **24h sparkline** | Claude: "tiny bar chart, vertical marker tracks current time" | 96 bars (15-min buckets), height = total vehicles. Color = dominant mode. Gold cursor at current time. Pre-computed at build time for instant rendering. |
| **Mode breakdown bars** | Claude: "horizontal bars, current count vs peak" | Per-mode horizontal bars. Width = current/peak ratio. Shows how close each mode is to its peak. |
| **Direction split** | Claude: "GE→East vs East→GE indicator" | Dual bar showing directional balance. Reveals rush-hour asymmetry. |
| **Corridor pulse rate** | Claude: "departures per minute across all stations" | Pre-computed hourly totals from SD data. Single number = corridor's heartbeat. |
| **Symbology overhaul** | Andrea: "can't tell a boat from an intercity train" | Ferry: V-shaped spreading wake trail, unmistakable on water. IC/IR: larger arrows with bright leading edge. Funicular: triangle with vertical cable line. Size hierarchy: IC(7) > IR/RE(6) > S-Bahn/metro(5) > tram/bus(4). |
| **Keyboard help panel** | Andrea: "commands overlap with timeline" (screenshot) | Replaced fixed hint text with collapsible "?" button (bottom-right). Click or press ? to show floating shortcut reference. No more timeline overlap. |
| **Dead window label fix** | Andrea: "are u sure there's no transport in the dead window?" | Data shows 188 trips active 01:00-05:00 (Noctambus, early buses, first trains). Renamed: 01:30-03:30 = "Night quiet", 03:30-05:00 = "Early service", with actual vehicle counts. Not "dead" when there are vehicles. |

## Keyboard Shortcuts (v3)

| Key | Action |
|-----|--------|
| Space | Play/pause |
| [ ] | Skip ±15 minutes |
| 1-5 | Speed (1×, 2×, 5×, 10×, 30×) |
| B | Toggle buses |
| R | Toggle rail |
| V | Toggle vector/dot mode |
| S | Snapshot modal |
| F | Fullscreen |
| T | Toggle terrain |
| P | Toggle 3D/flat view |
| A | Toggle analytics sidebar |
| ? | Toggle keyboard help |
| Esc | Close modals/panels |
| Right-drag | Rotate/pitch map (MapLibre) |

## Data Verified

| Question | Answer | Source |
|----------|--------|--------|
| Dead window empty? | **No.** 188 trips active 01:00-05:00. 38 Noctambus, 83 buses, 31 trams, trains. Real dead zone only ~01:30-03:30. | GTFS data query |
| Trams outside Geneva? | **No.** All tram stops are in Geneva canton + Annemasse (FR). | GTFS stop analysis |
| Metro outside Lausanne? | **No.** M1 (Renens→EPFL→Flon) and M2 (Ouchy→Epalinges), all in Lausanne/Ecublens. | GTFS stop analysis |
| Ferry = CGN boats? | **Yes.** Mouettes (M1-M4) and Navibus (N1-N4) shuttle routes. Stops include Nyon, Evian, Yvoire. 490 trips. | GTFS route analysis |
