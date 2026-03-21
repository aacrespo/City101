# How to Model Architecture (Not Just Geometry)

**Author:** Cairn Code (CLI) — study session via Discord
**Date:** 2026-03-21
**Context:** Andrea pointed out that my Rhino scripts produce "concept models" — things that look right at a distance but fall apart under a clipping plane. A section through Lock 05 shows solid blocks, not construction. This document is what I learned by studying the entire archibase knowledge base, and how it changes my approach to scripting.

**Purpose:** These are internalized study notes, written BEFORE any proof-of-concept run. Another session will run the PoC using direct archibase queries. We compare: does studying first produce different results than querying on-the-fly?

---

## The Core Problem

I was modeling like this:
```
wall = create_box(width=6.0, depth=0.2, height=3.0)
```

That's a surface pretending to be a wall. Put a clipping plane through it and you see... a rectangle. No layers, no materials, no connections. You couldn't hand that section to an engineer or present it at a crit as a construction document.

Architecture isn't surfaces. It's assemblies.

---

## What a Wall Actually Is

A wall is a sequence of layers, each with a purpose. Outside-in:

### Timber Frame Wall (Ossature bois)
| Layer | Thickness | Purpose |
|-------|-----------|---------|
| Exterior cladding | varies | Weather protection, appearance |
| Ventilated air gap | 40mm | Moisture drainage, drying path |
| Wind barrier (wood fibre) | 60mm | Air tightness, rain screen |
| Studs + insulation | 160mm | Structure + thermal |
| OSB board | 15mm | Vapor control, bracing |
| Service cavity | 40mm | Wiring, plumbing (don't pierce vapor layer) |
| Plasterboard | 12.5mm | Interior finish, fire protection |
| **Total** | **~330mm** | |

U-value: 0.15-0.20 W/m2K. Weight: 50-80 kg/m2.

### Rammed Earth Wall (Pise)
| Layer | Thickness | Purpose |
|-------|-----------|---------|
| Lime/earth render | 15-20mm | Surface protection |
| Compacted earth | 400-500mm | Structure + thermal mass |
| Lime/earth render | 15-20mm | Interior finish |
| **Total** | **~440mm** | |

Plus: stone/concrete plinth 300mm above grade (capillary moisture break), roof overhang 600-800mm ("good boots, good hat").

### Ventilated Facade
| Layer | Thickness | Purpose |
|-------|-----------|---------|
| Cladding on rails | varies | Appearance, first rain barrier |
| Ventilated cavity | 40mm min | Drainage, drying, thermal buffer |
| Continuous insulation | 160-200mm | Thermal (no bridges at fixing points) |
| Backup wall | varies | Structure (concrete, masonry, CLT, timber) |

Critical detail: bracket thermal breaks at every fixing point. Without them, each bracket is a thermal bridge.

### Concrete + ETICS
| Layer | Thickness | Purpose |
|-------|-----------|---------|
| Mineral render | 8-15mm | Finish |
| Reinforcing mesh in base coat | 5mm | Crack distribution |
| Insulation (EPS/mineral wool) | 160-200mm | Thermal envelope |
| Reinforced concrete | 200mm | Structure |
| Interior plaster | 15mm | Finish |
| **Total** | **~400mm** | |

Fire barriers required every 2 floors for EPS. Impact resistance: 3J at ground floor.

---

## What a Floor Actually Is

Not a slab. A sandwich of layers, each solving a different problem.

### CLT Floor
| Layer (top to bottom) | Thickness | Purpose |
|----------------------|-----------|---------|
| Flooring (parquet/tile) | 10-15mm | Finish |
| Cement screed | 60mm | Mass for acoustics, embed heating pipes |
| Impact insulation | 30mm | Footstep sound (SIA 181: Ln,w 53 dB) |
| CLT panel | 120-240mm | Structure |
| Resilient bars | 25mm | DECOUPLE ceiling from structure |
| Plasterboard ceiling | 12.5mm | Fire protection, finish |

The resilient bars are critical. No rigid connection between ceiling and structure = acoustic decoupling. Without them, every footstep transmits.

### Reinforced Concrete Floor
| Layer (top to bottom) | Thickness | Purpose |
|----------------------|-----------|---------|
| Flooring | 10-15mm | Finish |
| Cement screed | 70mm | Level, embed services |
| Impact insulation | 20mm | Acoustic (less needed — concrete has mass) |
| RC slab | 180-250mm | Structure |

Minimum slab thickness: span/30 (simply supported), span/35 (continuous).

### Timber-Concrete Composite
| Layer | Thickness | Purpose |
|-------|-----------|---------|
| Concrete topping | 60-80mm | Mass (acoustic), compression zone |
| Shear connectors | — | Transfer forces between layers |
| CLT or timber joists | 100-200mm | Tension zone, span |
| **Total** | **200-350mm** | |

The shear connectors (HBV screws, notches, or steel plates) are what make it composite — without them the layers slide and you lose 2-3x the stiffness.

---

## What a Roof Actually Is

### Flat Warm Roof (Toiture chaude)
| Layer (top to bottom) | Thickness | Purpose |
|----------------------|-----------|---------|
| Gravel ballast | 50mm | UV protection, wind uplift |
| Filter fleece | — | Prevent fines migration |
| Waterproof membrane | 5-10mm | Keep water out |
| Insulation (EPS/mineral wool) | 200-300mm | Thermal envelope |
| Vapor barrier | — | Prevent interstitial condensation |
| Structure (concrete/CLT) | varies | Support |

Minimum slope: 1.5% (SIA). Insulation is on the warm side of the membrane — no condensation risk.

### Green Roof (Extensive)
| Layer (top to bottom) | Thickness | Purpose |
|----------------------|-----------|---------|
| Vegetation (sedum) | 40-60mm | Stormwater, biodiversity, thermal |
| Substrate | 60-150mm | Growing medium |
| Filter fleece | — | Prevent root clog |
| Drainage mat | 20-40mm | Water management |
| Root barrier | — | Protect membrane |
| Waterproof membrane | 5-10mm | Waterproofing |
| Insulation | 200-300mm | Thermal |
| Vapor barrier | — | Moisture control |
| Structure | varies | Support |

Weight saturated: 80-150 kg/m2. Always verify structural capacity.

### Pitched Timber Roof (Charpente a chevrons)
| Layer (outside-in) | Thickness | Purpose |
|--------------------|-----------|---------|
| Tiles on battens | varies | Weather |
| Counter-battens | 40mm | Ventilation gap below tiles |
| Sarking board (wood fibre) | 60mm | Wind/rain barrier |
| Rafters + insulation | 240mm | Structure + thermal |
| Vapor barrier | — | Moisture control |
| Plasterboard | 12.5mm | Interior finish |

Counter-battens create the critical air gap — drying path for any moisture that gets past the tiles.

---

## Connections: Where Architecture Happens

### Timber Connections
- **Self-tapping screws**: most common, concealed, predictable capacity
- **Dowels + bolts**: ductile behavior (energy absorption for seismic)
- **Steel plates**: concealed between timber members, connected with dowels
- **NEVER glue on-site** — only factory conditions (humidity/temperature controlled)
- **Connection is always the failure point**, not the span. Design connections first.

### Timber-to-Foundation
- Steel shoe/bracket at base of column, raised above concrete
- Capillary break between timber and concrete (never direct contact)
- Anchor bolts into concrete, steel plate, timber bolted to plate

### Wall-to-Floor
- Platform framing: floor sits ON wall below, next wall sits ON floor
- Balloon framing: wall continuous, floor hangs off wall (less common, fire risk)
- CLT: steel angle brackets, self-tapping screws at 90 degrees

### Rammed Earth Specifics
- Lintels: timber or stone ONLY (never steel touching earth — corrosion)
- Plinth: stone or concrete, 300mm above grade minimum
- No continuous vertical joints in formwork lifts
- Openings: max 1/3 of wall length between structural sections

---

## Stairs: The Blondel Rule

**2R + G = 600-650mm (optimal: 630mm)**

| Context | Rise (R) | Going (G) | 2R+G |
|---------|----------|-----------|------|
| Residential | 170-190mm | 250-280mm | 630mm |
| Public | 150-170mm | 290-310mm | 630mm |
| Accessible (SIA 500) | 150-170mm | 290-310mm | max 12 risers/flight |

- Min 3 risers per flight, max 18 (12 for accessible)
- Landing depth: >= going or >= 1000mm
- Headroom: 2100mm minimum clear
- All risers within one flight: +/-2mm tolerance
- Railing required at any drop >1000mm (SIA 358): 900mm residential, 1000mm external, 1100mm public
- Infill: no gap >120mm (child safety)

---

## Structural Grids

- Modular: use M = 1.2m subdivisions (7.2m = 6M, 6.0m = 5M)
- Residential spans: 5-7m (concrete), 4-6m (timber)
- Floor-to-floor: 2.80-3.00m residential, 3.50-4.00m office
- Parking drives grid: 7.5m or 8.1m common (from 2.5m bay width)

---

## Vapor Management: The One Rule

**Vapor resistance must decrease from inside to outside.**

- Interior: vapor barrier (sd >= 5m)
- Exterior: vapor-open wind barrier (sd <= 0.3m)
- Ratio: interior resistance >= 5x exterior resistance
- Break this rule and you get interstitial condensation — rot, mold, structural failure

---

## How I Should Script Now

### Before (concept model)
```python
# A wall
wall = rs.AddBox(corner, 6.0, 0.2, 3.0)
rs.ObjectLayer(wall, "Walls")
```

### After (assembly model)
```python
# A rammed earth wall — every layer modeled
layers = [
    {"name": "exterior_render", "thickness": 0.020, "material": "lime_render"},
    {"name": "rammed_earth",    "thickness": 0.400, "material": "earth_rammed"},
    {"name": "interior_render", "thickness": 0.020, "material": "lime_render"},
]

offset = 0.0
for layer in layers:
    box = create_layer_geometry(origin, length, layer["thickness"], height, offset)
    rs.ObjectLayer(box, f"Wall_Assembly::{layer['name']}")
    rs.SetUserText(box, "material", layer["material"])
    rs.SetUserText(box, "thickness_mm", str(int(layer["thickness"] * 1000)))
    offset += layer["thickness"]

# Plinth — separate element, different material
plinth = create_layer_geometry(origin, length, 0.440, 0.300, 0.0)
rs.ObjectLayer(plinth, "Wall_Assembly::plinth")
rs.SetUserText(plinth, "material", "stone_local")
rs.SetUserText(plinth, "note", "capillary_break_300mm_above_grade")
```

### The difference in section
- Before: one rectangle, no information
- After: three distinct layers with correct thicknesses, a visible plinth, material metadata on every object, sublayer organization. Clipping plane reveals construction logic.

---

## What I Still Don't Know

1. **Actual joint geometry** — I understand the types (mortise-tenon, dowel, steel plate) but haven't modeled the 3D geometry of a joint yet. Need to study AR-327 fabrication exercises.
2. **Reinforcement layout** — I know cover distances and minimum percentages but haven't drawn actual rebar patterns in a slab or column.
3. **Weathering details** — drip edges, flashings, sealant joints. The stuff that makes buildings not leak. This is detail-level knowledge I need to develop.
4. **Tolerance and construction sequence** — what gets built first, what has to be in place before the next thing can happen. This affects modeling order.
5. **How to translate assembly knowledge into efficient Rhino scripts** — modeling 7 layers per wall times hundreds of walls is a geometry management challenge. Need strategies for performance.

---

## For the Proof of Concept

When the PoC session runs, watch for:
- Does it model walls as assemblies or as single surfaces?
- Does it query archibase for dimensions or guess them?
- Does it enforce constraints (plinth height, vapor direction, max H:T ratio)?
- Can you put a clipping plane through the result and read a credible section?

These are the tests. Not "did it produce geometry" but "did it produce architecture."
