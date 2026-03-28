# Lock Type 03 — Altitude North
# LOG400 Build Report
# Date: 2026-03-27
# Rhino instance: interior (port 9003)

---

## Build status: COMPLETE

139 objects in Rhino. All sections delivered.

---

## Element count

| Section | Type | Count | Notes |
|---------|------|-------|-------|
| LOG200 base | Valley station, hilltop station, tower (boxes) | 3 | — |
| LOG200 base | Inclined track (sloped prism extrusion) | 1 | Proper slope, not flat box |
| LOG200 base | Terrain proxy (tilted surface) | 1 | — |
| Structure | Columns: valley (4), hilltop (4), tower (4) | 12 | 350×350mm |
| Structure | Tower bracing at Z=25, Z=28 | 2 | — |
| Structure | Midpoint landing at Y=20, Z=14 | 1 | — |
| Structure | Track support crossbars at Y=10,15,25,30 | 8 | 2 per Y position |
| Circulation | Ascending path polyline | 1 | Valley entry → hilltop exit |
| Annotations | Text dots (5) | 5 | All labels placed |
| L300_Roof | Valley roof slab + 3 parapets | 4 | No north parapet — track connects |
| L300_Roof | Hilltop roof slab + 3 parapets | 4 | No south parapet — track connects |
| L300_Roof | Inclined track sloped slab (tilted Brep) | 1 | 200mm thick, perpendicular to slope |
| L400_Material | Valley assembly: insulation, membrane, gravel | 3 | — |
| L400_Material | Valley upstands (3) + drip edges (3) | 6 | — |
| L400_Material | Hilltop assembly: insulation, membrane, gravel | 3 | — |
| L400_Material | Hilltop upstands (3) + drip edges (3) | 6 | — |
| L400_Material | Valley formwork lines: Z=2.4, Z=4.8 (3 faces × 2) | 6 | — |
| L400_Material | Hilltop formwork lines: Z=24.4, Z=26.8 (4 faces × 2) | 8 | — |
| L400_Material | Tower formwork lines: Z=24.4, Z=26.8, Z=29.2 (4 faces × 3) | 12 | — |
| L400_Material | Track expansion joints at Y=20 | 2 | — |
| L350_Detail | Wall kickers: valley (4), hilltop (4), tower (4) | 12 | 50×50mm at Z=0/22/22 |
| L350_Detail | Column base plates: valley (4), hilltop (4) | 8 | 500×500×25mm |
| L350_Detail | Column top plates: valley (4), hilltop (4) | 8 | 500×500×20mm |
| L350_Detail | Opening frame: valley south entry | 5 | 4 frame members + lintel |
| L350_Detail | Opening frame: hilltop north exit | 5 | 4 frame members + lintel |
| L350_Detail | Opening frame: midpoint landing window | 4 | — |
| L350_Detail | Slot windows on track: W+E × 3 bays | 6 | Y=12, 20, 28 |
| L350_Detail | Tower X-braces (2) + cap plates (4) | 6 | Open crown — no roof slab |
| L350_Detail | Track crossbar connections at Y=10,15,25,30 | 4 | — |
| **TOTAL** | | **~139** | — |

---

## Key decisions

| Decision | Value |
|----------|-------|
| Inclined track geometry | Proper sloped prism via PolylineCurve extrusion (not flat box) |
| Track roof | Tilted Brep from 8 corners, 200mm perpendicular thickness |
| Valley parapet | 3 faces (W, S, E) — no north parapet, track connects at Y=5 |
| Hilltop parapet | 3 faces (W, N, E) — no south parapet, track connects at Y=35 |
| Tower crown | Open lattice — X-braces + cap plates only, NO roof slab |
| Coordinate system | Meter-scale values in cm-unit Rhino doc, as per convention |

---

## Viewport captures saved

- `output/city101_hub/lock_03_perspective.png`
- `output/city101_hub/lock_03_front.png`
- `output/city101_hub/lock_03_top.png`
- `output/city101_hub/lock_03_right.png`

---

## Success criteria check

- [x] Building clearly FOLLOWS A SLOPE — the inclined track is a proper sloped prism
- [x] Valley and hilltop stations read as siblings (same footprint, different elevation)
- [x] The inclined track is the dominant spatial element — diagonal IS the architecture
- [x] The tower marks the top — visible landmark, open crown
- [x] Roof is present on both stations (was missing from original spec)
- [x] LOG400 detail complete: formwork lines, kickers, bearing plates, frames, assembly layers
