# [A04_ACTIVE] Rennaz Lock 07 — Construction-Ready Overnight Build

**Run this prompt in Claude Code with Rhino MCP active.**
**Auto-accept mode ON. No human available.**
**Expected duration: 6-8 hours.**

---

## What you're building

Lock 07 — Bridge Lock at Rennaz (km 89). A timber pedestrian bridge connecting Villeneuve CFF station to HRC Rennaz hospital. LOG 400 / LOD 400 — full construction assemblies, every layer modeled, every connection detailed.

This is the first lock modeled with the full archibase knowledge system. Every assembly comes from Deplazes "Constructing Architecture" or Vittone "Bâtir", referenced below. No guessing thicknesses.

---

## Step 0: Setup

Before spawning any agents:

### 0.1 Read mandatory files
```
Read these files (do NOT skip):
1. .claude/agents/knowledge/rhino-playbook.md — 12 doctrine principles, review modes
2. workflows/agent-team-modeling-v3.md — coordination protocol (health checks, authority, idle rules)
3. This file (you're reading it now — contains all assembly data)
```

### 0.2 Set up Rhino layers
Execute this script FIRST to create the layer tree:

```python
import rhinoscriptsyntax as rs

layers = {
    "Lock_07::Terrain":                    (80, 90, 70),
    "Lock_07::Ground::Site":               (100, 100, 90),
    "Lock_07::Ground::Foundation":         (160, 150, 130),
    "Lock_07::Structure::Columns":         (180, 140, 80),
    "Lock_07::Structure::Beams":           (170, 130, 70),
    "Lock_07::Structure::Slabs":           (190, 160, 100),
    "Lock_07::Structure::Bracing":         (200, 180, 120),
    "Lock_07::Shell::Walls::Station":      (220, 200, 170),
    "Lock_07::Shell::Walls::Hospital":     (210, 190, 160),
    "Lock_07::Shell::Walls::Bridge":       (200, 185, 155),
    "Lock_07::Shell::Facade::Cladding":    (160, 130, 90),
    "Lock_07::Shell::Facade::WindBarrier": (140, 120, 80),
    "Lock_07::Shell::Facade::Insulation":  (240, 220, 100),
    "Lock_07::Shell::Facade::VapourBarrier": (180, 160, 120),
    "Lock_07::Shell::Facade::ServiceCavity": (200, 180, 140),
    "Lock_07::Windows":                    (180, 220, 230),
    "Lock_07::Doors":                      (170, 200, 210),
    "Lock_07::Roof::Structure":            (130, 100, 70),
    "Lock_07::Roof::Insulation":           (240, 220, 100),
    "Lock_07::Roof::Membrane":             (60, 60, 60),
    "Lock_07::Roof::Parapet":              (150, 140, 120),
    "Lock_07::Circulation::BridgeDeck":    (240, 210, 180),
    "Lock_07::Circulation::Ramp":          (230, 200, 170),
    "Lock_07::Circulation::Stairs":        (220, 190, 160),
    "Lock_07::Circulation::Elevator":      (210, 210, 220),
    "Lock_07::Circulation::Guardrails":    (180, 180, 170),
    "Lock_07::Circulation::Handrails":     (200, 190, 170),
    "Lock_07::Circulation::TactileStrips": (255, 200, 0),
}

for name, color in layers.items():
    if not rs.IsLayer(name):
        rs.AddLayer(name, color)

print("Layer tree created: {} layers".format(len(layers)))
```

### 0.3 Create coordination log
Write this file: `output/city101_hub/lock_07_rennaz/coordination_log.md`
```markdown
# Coordination Log — Lock 07 Rennaz Bridge Lock

## Decisions (chronological)

## Interface Alerts

## Open Questions

## Round Summary
```

### 0.4 Helper functions
Every agent uses these. Include in every agent prompt:

```python
# SITE PLACEMENT
# Local coordinates offset from LV95 by E-2560000, N-1137500
# Rennaz terrain tile, terrain elevation ~374m ASL
SITE_ORIGIN = (200, 300, 374.0)

def box(x0, y0, z0, x1, y1, z1, name=None, material=None, thickness_mm=None):
    """Create a box offset by SITE_ORIGIN, with metadata."""
    ox, oy, oz = SITE_ORIGIN
    pts = [
        (x0+ox, y0+oy, z0+oz), (x1+ox, y0+oy, z0+oz),
        (x1+ox, y1+oy, z0+oz), (x0+ox, y1+oy, z0+oz),
        (x0+ox, y0+oy, z1+oz), (x1+ox, y0+oy, z1+oz),
        (x1+ox, y1+oy, z1+oz), (x0+ox, y1+oy, z1+oz),
    ]
    obj = rs.AddBox(pts)
    if name:
        rs.ObjectName(obj, name)
    if material:
        rs.SetUserText(obj, "material", material)
    if thickness_mm:
        rs.SetUserText(obj, "thickness_mm", str(thickness_mm))
    return obj

def box_pts(pts_list, name=None, material=None, thickness_mm=None):
    """For wedge/ramp shapes with explicit 8 points, offset by SITE_ORIGIN."""
    ox, oy, oz = SITE_ORIGIN
    obj = rs.AddBox([(p[0]+ox, p[1]+oy, p[2]+oz) for p in pts_list])
    if name:
        rs.ObjectName(obj, name)
    if material:
        rs.SetUserText(obj, "material", material)
    if thickness_mm:
        rs.SetUserText(obj, "thickness_mm", str(thickness_mm))
    return obj
```

---

## SITE DATA CARD

```
SITE CONDITIONS:
- Location: Rennaz, between Villeneuve CFF and HRC hospital
- LV95: E=2'560'200, N=1'137'800 (center of bridge span)
- Elevation: 374.0m ASL (finish floor reference at ground level)
- Lake Geneva elevation: 372m ASL
- Terrain: Flat (371.95-380.82m range over 1km²)
- Frost depth: 800mm (Swiss Plateau)
- Rainfall: ~1000 mm/yr (Leman basin)
- Slope: <1% (essentially flat)
- Orientation: Y = South (station) → North (hospital)
- Wind: prevailing SW (lake breeze), NE (bise)
- Soil: moraine/gravel (near-lake deposit), good bearing ~200-300 kPa
- Seismic: Zone 1 (low), SIA 261
```

## LEVEL 0 DEFINITION

```
ORIGIN: SITE_ORIGIN = (200, 300, 374.0)
  → All local Z coordinates are RELATIVE to 374.0m ASL
  → Z=0.0 local = 374.0m ASL = ground level
  → Z=4.0 local = 378.0m ASL = bridge deck level

FINISH FLOOR (bridge deck): Z = +4.000
FINISH FLOOR (ground/arrival): Z = +0.000
TOP OF FOUNDATION: Z = -0.050 (50mm below grade)
BOTTOM OF FOUNDATION: Z = -0.800 (frost depth)

STRUCTURAL GRID:
  X-axis (East-West): column lines at X = -5.5, -2.5, 2.5, 5.5 (station)
                                     X = -2.5, 2.5 (bridge)
  Y-axis (South-North): bay lines at Y = -45, -41, -37, -33, -30 (station, 4m bays)
                                       Y = -30, -24, -18, -12, -6, 0, 6, 12, 18, 24, 30 (bridge, 6m bays)
  Z-levels:
    Ground:        Z = 0.000
    Bridge deck:   Z = 4.000
    Ceiling:       Z = 7.500 (chambers)
    Roof structure: Z = 8.000
    Roof top:      Z = 8.336 (top of roof assembly)
```

## BILL OF OBJECTS

### Structure Agent (~80 objects)
| Element | Count | Layer | Dimensions | Notes |
|---------|-------|-------|------------|-------|
| Pad footing (bridge) | 10 | Ground::Foundation | 600×600×400mm | Under each bridge column pair |
| Pad footing (station) | 12 | Ground::Foundation | 600×600×400mm | Under station columns |
| Strip footing (station walls) | 4 | Ground::Foundation | 400mm wide × 400mm deep × wall length | Under perimeter walls |
| Ground slab (station) | 1 | Ground::Foundation | 12000×15000×200mm | +insulation 120mm below |
| Steel shoe connectors | 22 | Structure::Columns | 200×200×150mm plate | On each footing, 30mm capillary gap |
| Bridge columns (GL24h) | 10 | Structure::Columns | 200×200mm, H=4000mm | Pairs at X=±2.5, 5 positions |
| Station columns (GL24h) | 12 | Structure::Columns | 200×200mm, H=4000mm | 4 per bay line, 3 bay lines |
| Deck beams (GL24h) | 11 | Structure::Beams | 140×320mm, L=6000mm | At each bridge bay, deck level |
| Roof beams (GL24h) | 11 | Structure::Beams | 140×280mm, L=6000mm | At each bridge bay, roof level |
| Station deck beams | 8 | Structure::Beams | 140×360mm, L=varies | Spanning 4-6m in station |
| Station roof beams | 8 | Structure::Beams | 140×280mm, L=varies | At roof level |
| CLT bridge deck slab | 10 | Structure::Slabs | 6000×160mm panels | Between deck beams |
| CLT station floor slab | 1 | Structure::Slabs | ~12000×15000×200mm | Station chamber floor |
| CLT station roof slab | 1 | Structure::Slabs | ~12000×15000×160mm | Station roof substrate |
| Steel tension rods | 8 | Structure::Bracing | Ø16mm, X-pattern | Between bridge column pairs |

### Envelope Agent (~200 objects)
| Element | Count | Layer | Notes |
|---------|-------|-------|-------|
| **Station walls — 7 layers each, 4 walls** | 28 | Shell::Walls::Station + Facade sublayers | Each wall = 7 separate solids |
| **Hospital chamber walls — 7 layers each, 3 walls** | 21 | Shell::Walls::Hospital + Facade sublayers | Arrival hall + elevator surround |
| **Bridge enclosure panels** (partial walls) | ~20 | Shell::Walls::Bridge | Panels between posts, lower portion only (waist-to-lintel) |
| **Station windows** (4 large) | 4×5=20 | Windows | Each = frame + glass + sill + lintel + 2 reveals |
| **Bridge lateral openings** (10 bays × 2 sides) | 20×5=100 | Windows | Each = frame + glass + sill + lintel + 2 reveals (or open with frame only) |
| **Station entrance door** (1) | 5 | Doors | Frame + leaf + threshold + 2 reveals |
| **Hospital entrance door** (1) | 5 | Doors | Frame + leaf + threshold + 2 reveals |
| **Internal doors** (WC × 2, storage) | 9 | Doors | Frame + leaf + threshold each |
| **Roof joists** (station) | ~15 | Roof::Structure | 40×300mm at 600mm centers |
| **Roof insulation** (station) | ~15 | Roof::Insulation | 120mm between joists |
| **Roof membrane** (station) | 2 | Roof::Membrane | Bitumen + plywood |
| **Roof parapet** (station perimeter) | 4 | Roof::Parapet | Copings + flashings |
| **Bridge roof panels** | 10 | Roof::Membrane | Between roof beams |

### Circulation Agent (~150 objects)
| Element | Count | Layer | Notes |
|---------|-------|-------|-------|
| **Bridge deck surface** (decking boards) | ~20 | Circulation::BridgeDeck | Individual boards visible at ends, single panel mid-span |
| **Bridge deck membrane** | 10 | Circulation::BridgeDeck | Waterproof layer between beams |
| **Bridge deck substrate** | 10 | Circulation::BridgeDeck | Plywood under membrane |
| **Lane divider** | 1 | Circulation::BridgeDeck | X=0, 100mm wide × 150mm tall |
| **Ramp Run 1** (east, Z=4→3) | 1 | Circulation::Ramp | Y=30→46.7, X=1 to 4 |
| **Landing A** | 1 | Circulation::Ramp | Y=46.7→48.2, Z=3.0, 1500mm deep |
| **Ramp Run 2** (west, Z=3→2) | 1 | Circulation::Ramp | Y=48.2→31.5, X=-4 to -1 |
| **Landing B** | 1 | Circulation::Ramp | Y=31.5→30.0, Z=2.0 |
| **Ramp Run 3** (east, Z=2→1) | 1 | Circulation::Ramp | Y=30→46.7, X=1 to 4, at lower level |
| **Landing C** | 1 | Circulation::Ramp | Y=46.7→48.2, Z=1.0 |
| **Ramp Run 4** (west, Z=1→0) | 1 | Circulation::Ramp | Y=48.2→31.5, X=-4 to -1 |
| **Arrival landing** | 1 | Circulation::Ramp | Z=0.0, ground level |
| **Ramp deck assembly** (each run) | 4×3=12 | Circulation::Ramp | Decking + membrane + CLT per run |
| **Ramp columns** | ~16 | Circulation::Ramp | Supporting ramp structure at each turn |
| **Ramp guardrails** (both sides, all runs) | 8 | Circulation::Guardrails | 1100mm height |
| **Ramp handrails** (both sides, all runs) | 8 | Circulation::Handrails | Ø44mm timber, 850-900mm height |
| **Bridge guardrail posts** | 22 | Circulation::Guardrails | 80×80mm at 1200mm centers, both sides |
| **Bridge guardrail infill** | 20 | Circulation::Guardrails | Horizontal rails 40×60mm |
| **Bridge cap rail** | 2 | Circulation::Guardrails | Continuous Ø50mm timber |
| **Elevator shaft walls** | 4 | Circulation::Elevator | 200mm concrete, 2500×2500mm plan |
| **Elevator doors** (2 levels) | 2 | Circulation::Elevator | 900mm clear width |
| **Elevator cab outline** | 1 | Circulation::Elevator | 1100×2100mm |
| **Emergency stair** | ~10 | Circulation::Stairs | Adjacent to elevator, 1500mm wide |
| **Tactile guidance strips** (bridge) | 10 | Circulation::TactileStrips | Slow lane (west) |
| **Tactile warning strips** (landings) | 6 | Circulation::TactileStrips | At ramp turns + elevator |

### Site Agent (~20 objects)
| Element | Count | Layer | Notes |
|---------|-------|-------|-------|
| **Terrain mesh** | 1 | Terrain | From extracted geodata (simplified) |
| **Route 9 road surface** | 2-3 | Ground::Site | From infrastructure.json |
| **Context buildings** (nearest) | 5-10 | Ground::Site | From buildings.json (simplified massing) |
| **Railway alignment** | 1-2 | Ground::Site | Simplon line (passes 500m from site) |

**TOTAL ESTIMATED: ~450 objects**

---

## ASSEMBLY DATA (embed in agent prompts)

### WALL ASSEMBLY — Timber Platform Frame (Deplazes p.428)
**Total: 276mm. Model each layer as a separate box on its own sublayer.**

For a wall at X=x_inner (interior face), running from Y=y0 to Y=y1, Z=z0 to Z=z1:

```
Layer 7 (interior):  X = x_inner to x_inner + 0.012          ServiceCavity    wood-cement particleboard 12mm
Layer 6:             X = x_inner + 0.012 to x_inner + 0.062  ServiceCavity    vertical battens 50mm
Layer 5:             X = x_inner + 0.062 to x_inner + 0.074  VapourBarrier    plywood 12mm
Layer 4:             X = x_inner + 0.074 to x_inner + 0.194  Insulation       studs 60×120 + Isofloc 120mm
Layer 3:             X = x_inner + 0.194 to x_inner + 0.212  WindBarrier      softboard 18mm
Layer 2:             X = x_inner + 0.212 to x_inner + 0.252  Cladding         ventilated cavity 40mm (battens)
Layer 1 (exterior):  X = x_inner + 0.252 to x_inner + 0.276  Cladding         larch boards 24mm
```

Materials for metadata:
- Layer 1: material="larch_boards", thickness_mm=24
- Layer 2: material="ventilated_cavity_battens", thickness_mm=40
- Layer 3: material="bitumen_softboard", thickness_mm=18
- Layer 4: material="spruce_studs_isofloc", thickness_mm=120
- Layer 5: material="plywood_vapour_barrier", thickness_mm=12
- Layer 6: material="service_cavity_battens", thickness_mm=50
- Layer 7: material="wood_cement_particleboard", thickness_mm=12

### BRIDGE DECK ASSEMBLY
**Total: 217mm. Model as 4 layers on Circulation::BridgeDeck.**

For a deck panel between beams at Y=y0 to Y=y1, X=-3 to X=3:
```
Layer 1 (top):    Z = 3.783 to 3.823   Larch decking 40mm     (walking surface)
Layer 2:          Z = 3.781 to 3.783   Bitumen membrane 2mm
Layer 3:          Z = 3.766 to 3.781   Plywood substrate 15mm
Layer 4 (bottom): Z = 3.606 to 3.766   CLT slab 160mm         (structural)
```
Note: deck top = Z=3.823, NOT Z=4.0. The beam top is at Z=4.0. Deck sits between beams.
Actually — recalculate: if beams are at deck level Z=4.0, beam top = 4.0 + 0.32 = 4.32. The CLT slab sits ON TOP of the beams.

**CORRECTED deck assembly (CLT on top of beams):**
```
Beam top:         Z = 4.000 + 0.320 = Z = 4.320 (but beam is below deck)
```

Actually, let me be precise. The beam is a DECK beam that supports the CLT from below:
- Beam bottom: Z = 4.000 - 0.320 = Z = 3.680
- Beam top: Z = 4.000
- CLT bottom: Z = 4.000 (sits on beam top)
- CLT top: Z = 4.160
- Plywood: Z = 4.160 to 4.175
- Membrane: Z = 4.175 to 4.177
- Decking: Z = 4.177 to 4.217

**FINAL deck surface: Z = 4.217 (finish floor level for walking)**

Adjust all references: "deck level" = Z = 4.217 for walking surface, structural reference = Z = 4.0 for beam top.

### FLAT ROOF ASSEMBLY (Deplazes p.475)
**Total: 336mm. Model on Roof:: sublayers.**

For station chamber roof, X=-6 to 6, Y=-45 to -30:
```
Layer 1 (top):    Z = 8.321 to 8.336   Plywood airtight membrane 15mm     Roof::Membrane
Layer 2:          Z = 8.021 to 8.321   Timber joists 40×300 + insulation  Roof::Structure + Roof::Insulation
Layer 3:          Z = 8.000 to 8.021   Plywood deck 21mm                  Roof::Membrane
Layer 4 (top):    Z = 8.021 to 8.028   Bitumen felt 2 layers 7mm         Roof::Membrane
```

Wait — the order should be (bottom to top):
```
Bottom (interior): Z = 8.000   (soffit — exposed structural timber)
Layer 1:  Z = 8.000 to 8.015   Plywood airtight membrane 15mm
Layer 2:  Z = 8.015 to 8.315   Timber joists 40×300 + 120mm insulation between joists
Layer 3:  Z = 8.315 to 8.336   Plywood deck 21mm
Layer 4:  Z = 8.336 to 8.343   Bitumen felt 2 layers 7mm (top surface)
```

**FINAL roof top: Z = 8.343**

### FOUNDATION ASSEMBLY
```
Ground level:     Z = 0.000
Top of footing:   Z = -0.050 (50mm below grade for slab bearing)
Bottom of footing: Z = -0.800 (frost depth)

Pad footing:  600 × 600 × 400mm concrete (Z = -0.800 to -0.400)
Gravel bed:   600 × 600 × 150mm (Z = -0.950 to -0.800) — model as box
Steel shoe:   200 × 200 × 150mm plate (Z = -0.050 to 0.100) — on top of footing
Capillary gap: 30mm air (not modeled — just the gap between shoe top and column bottom)
Column base:  Z = 0.130 (shoe top 0.100 + 30mm gap)
```

Wait — column needs to go from ground to deck. Let me recalculate:
- Column bottom: sits on steel shoe. Shoe top at ~Z=0.100. Plus 30mm gap = Z=0.130.
- Column top: Z=4.000 (supporting deck beams)
- Column clear height: 4.0 - 0.13 = 3.87m

Actually, simplify for modeling: columns from Z=0.0 to Z=4.0 (the shoe/gap is a detail below).
Footings from Z=-0.8 to Z=-0.4.
Steel shoes at Z=-0.05 to Z=0.1 (bridging footing top to column base).

### OPENING ASSEMBLY — WINDOW (LOG 400)

For a window opening 1500mm wide × 2000mm tall in a 276mm wall:

```
LINTEL (GL24h): 140 × 200mm, length = opening_width + 2×150mm bearing
  Position: spanning across top of opening, embedded in wall structure layer
  Z = top_of_opening to top_of_opening + 0.200

FRAME (timber): 80 × 80mm profile, 4 pieces forming rectangle
  Outer face flush with wall structure outer face (Layer 4 outer edge)

GLASS (double-pane): 24mm unit (4+16+4), centered in frame
  Recessed 80mm from exterior wall face

SILL (timber): 30mm thick × (opening_width + 2×40mm overhang)
  Projects 40mm beyond exterior wall face
  Slope: 5° outward for drainage

REVEALS (timber lining): 12mm thick, both sides + top
  Lines the wall void from frame to interior face
```

### OPENING ASSEMBLY — DOOR (LOG 400)

For main entrance door 900mm clear × 2100mm:

```
FRAME (timber): 100 × 60mm, 3 pieces (head + 2 jambs)
  Flush with interior wall face

LEAF (solid timber): 44mm thick (30mm core + 7mm face each side)
  920mm × 2080mm (slightly smaller than frame opening)

THRESHOLD: 25mm max height, full width
  Flush with deck surface where possible

REVEALS: 12mm timber lining on both sides
```

---

## TEAM ASSEMBLY

Spawn 5 agents total. The session coordinator (you) acts as Lead.

### Agent 1: SITE
```
<agent name="site" role="Site + Context">
You model terrain and surrounding context for Lock 07 Rennaz.

LAYERS: Lock_07::Terrain, Lock_07::Ground::Site

TASK:
1. Import simplified terrain mesh from geodata:
   - Read: output/city101_hub/terrain/city101_node7_rennaz_swissalti3d_2019_2560-1137_2_2056_5728_xyz.csv
   - Create a simplified terrain surface (every 10th point = 50×50 grid)
   - Place on Lock_07::Terrain

2. Model Route 9 road surface:
   - Flat box at Z=-0.05 (slightly below grade), 8m wide, running E-W through site
   - Y position: approximately Y=-10 to Y=-5 (south of bridge center, under the span)

3. Model 3-5 nearest context buildings as simple massing boxes:
   - Read: output/city101_hub/context/city101_node7_rennaz_building_footprint.geojson
   - Pick 3-5 closest to SITE_ORIGIN, extrude footprints to approximate heights (8-12m)

4. Model railway alignment:
   - Single line or thin box showing Simplon railway, ~500m south of site

COORDINATION: Your work is background context. No other agent depends on your geometry dimensionally. Place everything on the correct layers. Name all objects with "Context_" prefix.

EXPECTED OBJECTS: ~20
</agent>
```

### Agent 2: STRUCTURE
```
<agent name="structure" role="Structure + Foundation">
You build the structural skeleton for Lock 07 Rennaz. Timber (GL24h) columns, beams, CLT slabs, concrete foundations.

LAYERS: Lock_07::Structure::Columns, Lock_07::Structure::Beams, Lock_07::Structure::Slabs, Lock_07::Structure::Bracing, Lock_07::Ground::Foundation

CONSTANTS:
COL_W = 0.200          # GL24h column section
DECK_BEAM = (0.140, 0.320)   # width × depth
ROOF_BEAM = (0.140, 0.280)
CLT_DECK = 0.160       # 5-layer CLT slab
CLT_FLOOR = 0.200      # station chamber floor
PAD_FOOTING = (0.600, 0.600, 0.400)
SHOE_H = 0.150

STRUCTURAL GRID (all dimensions in meters, relative to SITE_ORIGIN):

BRIDGE COLUMNS (10 total, 5 pairs):
  Y positions: [-24, -12, 0, 12, 24]
  X positions: [-2.5, 2.5] (each Y position)
  Z: 0.0 to 4.0

STATION COLUMNS (12 total, 3 rows × 4):
  Y positions: [-42, -37, -33]  (note: -30 shared with bridge)
  X positions: [-5.5, -2.5, 2.5, 5.5]
  Z: 0.0 to 4.0

TASK — Build in this order:

1. FOUNDATIONS (Layer: Ground::Foundation)
   - Pad footings under every column: 600×600×400mm, Z=-0.800 to Z=-0.400
   - Steel shoe on each: 200×200×150mm, Z=-0.050 to Z=0.100
   - Strip footings under station perimeter walls: 400mm wide × 400mm deep
     - North wall: Y=-30, X=-6 to 6
     - South wall: Y=-45, X=-6 to 6
     - West wall: X=-6, Y=-45 to -30
     - East wall: X=6, Y=-45 to -30
   - Ground slab (station): X=-6 to 6, Y=-45 to -30, Z=-0.250 to -0.050
     (200mm concrete slab on 120mm insulation — model slab only, note insulation in metadata)

2. COLUMNS (Layer: Structure::Columns)
   - All 22 columns as 200×200mm boxes, Z=0.0 to 4.0
   - Name: Col_Bridge_Y_X or Col_Station_Y_X
   - Material metadata: "glulam_GL24h"
   - Thickness metadata: "200"

3. BEAMS — DECK LEVEL (Layer: Structure::Beams)
   - Bridge deck beams: 11 beams at Y = [-30, -24, ..., 24, 30]
     Each: 140mm wide × 320mm deep, spanning X=-2.5 to X=2.5 (resting on columns)
     Z = 4.0 - 0.320 = 3.680 (bottom) to 4.0 (top)
   - Station deck beams: spanning between station column lines
     At Y = [-42, -37, -33, -30], spanning full station width or to column

4. BEAMS — ROOF LEVEL (Layer: Structure::Beams)
   - Bridge roof beams: 11 beams at same Y positions
     140mm wide × 280mm deep
     Z = 8.0 - 0.280 = 7.720 (bottom) to 8.0 (top)
   - Station roof beams: at same Y positions within station

5. CLT SLABS (Layer: Structure::Slabs)
   - Bridge deck: 10 CLT panels between beams
     Each: X=-3 to 3, Y=beam_Y to next_beam_Y, Z=4.0 to 4.160 (160mm CLT ON TOP of beams)
   - Station floor: single CLT panel X=-6 to 6, Y=-45 to -30, Z=4.0 to 4.200 (200mm)
   - Station roof: CLT panel X=-6 to 6, Y=-45 to -30, Z=8.0 to 8.160 (160mm)

6. BRACING (Layer: Structure::Bracing)
   - Steel tension X-rods between bridge column pairs
   - 8 total (4 bays × 2 faces)
   - Model as thin boxes (Ø16mm = 16×16mm square approximation)

COORDINATION GEOMETRY (publish after building):
Post to coordination log:
- Column positions: list of (X, Y) for all 22 columns
- Slab edges: Z=4.0 (top of beam), Z=4.160/4.200 (top of CLT)
- Roof bearing: Z=8.0 (top of roof beam)

EXPECTED OBJECTS: ~80
After building: print object count per sublayer.
</agent>
```

### Agent 3: ENVELOPE
```
<agent name="envelope" role="Envelope + Openings + Roof">
You build all walls, windows, doors, and roof for Lock 07 Rennaz. Every wall is a 7-layer timber frame assembly at LOG 400.

LAYERS: Lock_07::Shell::*, Lock_07::Windows, Lock_07::Doors, Lock_07::Roof::*

WAIT FOR: Structure agent to publish coordination geometry (column positions, slab edges). Read coordination log before starting.

ASSEMBLY DATA — WALL (276mm total, inside → outside):
  Layer 7 (int):  12mm  wood-cement particleboard   → Shell::Facade::ServiceCavity
  Layer 6:        50mm  service cavity battens       → Shell::Facade::ServiceCavity
  Layer 5:        12mm  plywood vapour barrier       → Shell::Facade::VapourBarrier
  Layer 4:       120mm  studs + Isofloc insulation   → Shell::Facade::Insulation
  Layer 3:        18mm  bitumen softboard            → Shell::Facade::WindBarrier
  Layer 2:        40mm  ventilated cavity battens    → Shell::Facade::Cladding
  Layer 1 (ext):  24mm  larch boards                 → Shell::Facade::Cladding

TASK — Build in this order:

1. STATION CHAMBER WALLS (4 walls, 7 layers each = 28 objects)
   Build on Shell::Walls::Station and Facade:: sublayers.

   For each wall, model 7 separate boxes:

   NORTH WALL (Y=-30, facing bridge):
   - Interior face at Y = -30.000 (flush with bridge connection)
   - Exterior face at Y = -30.276
   - But this wall has the bridge opening (X=-3 to 3, Z=4.0 to 7.5)
   - Model as 2 sections: west pier (X=-6 to -3) and east pier (X=3 to 6)
   - Each section × 7 layers

   SOUTH WALL (Y=-45):
   - Interior face at Y = -44.724
   - Exterior face at Y = -45.000
   - Has entrance door opening: X=-0.5 to 0.5, Z=4.0 to 6.1 (900mm wide × 2100mm tall)
   - Model as 3 sections: west pier, door void, east pier

   WEST WALL (X=-6):
   - Interior face at X = -5.724
   - Exterior face at X = -6.000
   - Has 2 windows: at Y=-40 and Y=-35, each 1500mm wide × 2000mm tall

   EAST WALL (X=6):
   - Interior face at X = 5.724
   - Exterior face at X = 6.000
   - Has 2 windows: same positions as west

2. WINDOWS (each window = frame + glass + sill + lintel + 2 reveals)
   Station windows: 4 total (2 west, 2 east)
   Bridge lateral openings: these are OPEN (no glass) with timber frame only
   - Model frame as 80×80mm timber surround at each bay opening
   - 10 bays × 2 sides = 20 frame assemblies

   For each station window (1500mm W × 2000mm H):
   - Lintel: GL24h 140×200mm, length = 1500+300 = 1800mm, on Beams layer
   - Frame: 4 pieces of 80×80mm timber forming rectangle
   - Glass: 24mm thick panel (1340mm × 1840mm — frame minus 80mm each side)
   - Sill: 30mm thick × 1580mm wide (40mm overhang each side), 5° slope
   - Reveals: 2 pieces 12mm thick × depth_to_interior × opening_height

3. DOORS
   Station south entrance: 900mm clear × 2100mm
   - Frame: 100×60mm timber, 3 pieces
   - Leaf: 44mm thick × 920mm × 2080mm
   - Threshold: 25mm × 1000mm

   Hospital entrance: same spec
   WC doors (×2): 800mm clear × 2100mm, same assembly scaled
   Storage door: 800mm clear × 2100mm

4. ROOF ASSEMBLY
   Station roof (X=-6 to 6, Y=-45 to -30):
   - Joists: 40×300mm at 600mm centers, running Y-direction (N-S)
     Count: (12000/600) = 20 joists
     Z = 8.000 to 8.300 (sitting on CLT roof slab at Z=8.0+0.160=8.160...

   Actually — joists sit on the roof beams/CLT. Let me recalculate:
   - CLT roof slab top: Z = 8.160
   - Joists bottom: Z = 8.160, top: Z = 8.460
   - Insulation between joists: 120mm (rest is air cavity for ventilation)
   - Plywood deck: Z = 8.460 to 8.481
   - Bitumen: Z = 8.481 to 8.488

   Model the joists as individual boxes (LOG 400 = discrete elements).
   Model insulation as continuous panels between joists.
   Model plywood + bitumen as 2 continuous panels.

   Parapet: 300mm above roof membrane, around perimeter
   - 4 pieces: N, S, E, W
   - Coping: 3mm sheet metal on top, 20mm overhang

   Bridge roof: simpler — panels between roof beams
   - 10 panels (one per bay): plywood 21mm + bitumen 7mm
   - Z = 8.000 to 8.028 (sitting directly on roof beams)

5. HOSPITAL CHAMBER WALLS (arrival hall at ground level)
   Smaller structure: 6m × 4m × 3.5m at base of ramp/elevator
   - 3 walls (4th side is open to ramp arrival)
   - Same 7-layer assembly, 276mm

EXPECTED OBJECTS: ~200
After building: print object count per sublayer. Verify every wall has exactly 7 layers.
</agent>
```

### Agent 4: CIRCULATION
```
<agent name="circulation" role="Circulation + Elevator">
You build the bridge deck surface, switchback ramp, elevator, stairs, guardrails, and tactile strips.

LAYERS: Lock_07::Circulation::*

WAIT FOR: Structure agent (deck slab positions, Z levels). Read coordination log.

KEY DIMENSIONS:
- Bridge deck CLT top: Z = 4.160 (structure agent builds this)
- Walking surface top: Z = 4.160 + 0.015 + 0.002 + 0.040 = Z = 4.217
  (CLT + plywood 15mm + membrane 2mm + decking 40mm)
- Ramp start: Z = 4.217 (bridge deck level)
- Ramp end: Z = 0.040 (ground level + 40mm decking)
- Ramp gradient: 6% = 0.06 rise/run
- Ramp width: 1500mm

TASK — Build in this order:

1. BRIDGE DECK SURFACE (Layer: Circulation::BridgeDeck)
   On top of CLT slabs (built by Structure):

   For each of 10 bay panels (between beams):
   - Plywood substrate: Z = 4.160 to 4.175 (15mm)
   - Waterproof membrane: Z = 4.175 to 4.177 (2mm)
   - Timber decking: Z = 4.177 to 4.217 (40mm)

   At the first and last 2 bays, model individual decking boards:
   - Board width: 120mm, gap: 5mm
   - Running X-direction (perpendicular to walking direction)
   - This shows LOG 400 detail at visible ends

   Mid-span (6 central bays): single panel per bay is acceptable

   Lane divider: X = -0.05 to 0.05, Y = -30 to 30, Z = 4.217 to 4.367 (150mm high)
   Material: "timber_larch", thickness_mm: 100

2. SWITCHBACK RAMP (Layer: Circulation::Ramp)

   4.0m total descent at 6% grade.
   Each run: 16.67m long, 1.0m descent.
   Width: 1.5m per run. Gap between parallel runs: 0.5m.

   RAMP GEOMETRY (all Z values are top-of-decking):

   RUN 1 (east side, descending south→north):
   - Start: X=1.0, Y=30.0, Z=4.217
   - End:   X=1.0, Y=46.67, Z=3.217
   - Width: X=1.0 to X=2.5 (1.5m)
   - Model as wedge (box_pts with sloped Z)

   LANDING A (180° turn):
   - X=-2.5 to 2.5, Y=46.67 to 48.17, Z=3.217 (flat)
   - 1500mm deep × 5000mm wide (allows wheelchair turning 1400×1700mm)

   RUN 2 (west side, descending north→south):
   - Start: X=-2.5, Y=48.17, Z=3.217
   - End:   X=-2.5, Y=31.5, Z=2.217
   - Width: X=-2.5 to X=-1.0 (1.5m)

   LANDING B (180° turn):
   - X=-2.5 to 2.5, Y=30.0 to 31.5, Z=2.217 (flat)

   RUN 3 (east side, descending south→north):
   - Start: X=1.0, Y=30.0, Z=2.217
   - End:   X=1.0, Y=46.67, Z=1.217
   - Width: X=1.0 to X=2.5

   LANDING C (180° turn):
   - X=-2.5 to 2.5, Y=46.67 to 48.17, Z=1.217 (flat)

   RUN 4 (west side, descending north→south):
   - Start: X=-2.5, Y=48.17, Z=1.217
   - End:   X=-2.5, Y=31.5, Z=0.217
   - Width: X=-2.5 to X=-1.0

   ARRIVAL LANDING:
   - X=-2.5 to 2.5, Y=30.0 to 31.5, Z=0.217 → transition to ground (Z=0.040 decking on grade)

   Each ramp run = 3-layer assembly:
   - CLT slab: 160mm (structural)
   - Plywood + membrane: 17mm
   - Timber decking: 40mm (anti-slip)

   RAMP SUPPORT COLUMNS:
   - At each landing turn: 4 columns (200×200mm GL24h)
   - Landing A columns: Z=0 to 3.217 (4 columns at corners)
   - Landing B columns: Z=0 to 2.217
   - Landing C columns: Z=0 to 1.217
   - Total: ~12 ramp columns

3. ELEVATOR (Layer: Circulation::Elevator)
   Position: X=-6.0 to -3.5, Y=30.0 to 32.5

   Shaft walls: 200mm concrete, Z=0.0 to 8.5 (extends above roof for machinery)
   - North: X=-6.0 to -3.5, Y=32.3 to 32.5 (200mm)
   - South: X=-6.0 to -3.5, Y=30.0 to 30.2
   - West: X=-6.0 to -5.8, Y=30.0 to 32.5
   - East: X=-3.7 to -3.5, Y=30.0 to 32.5

   Doors (model as thin boxes):
   - Level +4.0: Y=30.0, X=-5.3 to -4.4, Z=4.217 to 6.317 (900mm wide × 2100mm tall)
   - Level 0.0: Y=32.5, X=-5.3 to -4.4, Z=0.0 to 2.1 (opens to hospital side)

   Cab outline: 1100×2100mm box, Z=0.0 to 2.5 (parked at ground)

4. EMERGENCY STAIR (Layer: Circulation::Stairs)
   Adjacent to elevator: X=-3.5 to -2.0, Y=30.0 to 34.0
   Width: 1500mm (SIA public building)
   4.0m total rise, going 280mm, riser 175mm
   Flights: 2 per level (180° turn with landing)
   Model as: 2 sloped solids (stair flights) + 1 landing per half-level
   Individual treads if time allows (LOG 400)

5. GUARDRAILS + HANDRAILS

   BRIDGE GUARDRAILS (Layer: Circulation::Guardrails):
   Both sides (X=-3 and X=3), Y=-30 to 30:
   - Posts: 80×80mm timber at 1200mm centers (50 posts total, 25 per side)
     Z = 4.217 to 4.217 + 1.100 = 5.317
   - Horizontal infill rails: 40×60mm at 100mm vertical spacing
     Model 3 rails per bay: at Z = 4.417, 4.617, 4.817 (200mm spacing)
     ... actually for safety: max 120mm gap. Model rails at ~110mm spacing:
     9 rails per bay from Z=4.317 to Z=5.217, each 40mm tall, 100mm gap
   - Cap rail: continuous 50×50mm (approximate round as square) at Z=5.267 to 5.317

   RAMP GUARDRAILS (Layer: Circulation::Guardrails):
   Both sides of each run, following slope
   - Same post + infill detail, sloped to match ramp
   - Model as sloped boxes using box_pts

   RAMP HANDRAILS (Layer: Circulation::Handrails):
   Both sides, continuous, Ø44mm (model as 44×44mm square box), height 900mm
   Extend 300mm beyond top and bottom of each run

   BRIDGE HANDRAILS:
   Both sides, Ø44mm at 900mm height, Y=-30 to 30

6. TACTILE STRIPS (Layer: Circulation::TactileStrips)
   - Bridge slow lane (west): warning strips at Y=-30 and Y=30, guidance along X=-2.0 to -1.8
   - Ramp landings: warning strips before each turn (400mm deep × full width)
   - Elevator: warning strip at each door (400mm deep × door width + 200mm each side)

EXPECTED OBJECTS: ~150
After building: print ramp gradient verification (rise/run per segment), total object count.
</agent>
```

---

## EXECUTION SEQUENCE

### Internal Phase 1: Site + Structure (~1.5 hours)

1. Spawn Site agent and Structure agent in PARALLEL
2. Structure builds foundations first, then columns, then beams, then slabs
3. After Structure completes: **HEALTH CHECK**
   - Query Rhino: count objects on Structure:: layers
   - Expected: ~80. If < 40: FLAG and retry
   - Post results to coordination log
4. Structure publishes coordination geometry to log

### Internal Phase 2: Envelope + Circulation (~2.5 hours)

5. Spawn Envelope agent and Circulation agent in PARALLEL
6. Both read coordination log for Structure positions before building
7. Envelope builds walls (7 layers each!), then windows, then doors, then roof
8. Circulation builds deck surface, then ramp, then elevator, then stairs, then guardrails
9. After both complete: **HEALTH CHECK**
   - Envelope expected: ~200. If < 100: FLAG
   - Circulation expected: ~150. If < 75: FLAG
   - Post results to coordination log

### Internal Phase 3: Review (~1 hour)

10. Lead performs Mode A review:
    - Place clipping plane at Y=0 (bridge mid-span), read section
    - Every wall should show 7 layers with correct thicknesses
    - Deck assembly: decking → membrane → plywood → CLT → beam visible below
    - Check thermal envelope continuity: walls → roof (no gaps at junction)

11. Lead performs Mode B review:
    - Get viewport screenshots from 4 cardinals + aerial
    - Does it look like a timber pedestrian bridge? Proportions, rhythm, silhouette?
    - Ramp should read as a clear switchback descent

12. Fix any issues found — send targeted fixes to specific agents

### Internal Phase 4: Output (~0.5 hours)

13. Capture final viewport screenshots (4 cardinals + aerial + 2 sections)
14. Generate object catalog (layer → name → bounding box → material)
15. Update coordination log with final round summary
16. Print final summary: total objects, objects per layer, key dimensions

---

## OVERNIGHT AUTONOMOUS RULES

1. **No human available.** All decisions follow the authority hierarchy in the workflow. If hierarchy doesn't resolve it, use code compliance as tiebreaker.
2. **If Rhino MCP disconnects:** Stop gracefully. Save coordination log. Print what was completed. Andrea will restart in the morning.
3. **If an agent fails silently (health check < 50%):** Retry that agent once. If second attempt fails, skip and note in coordination log.
4. **Max 3 build rounds** (not counting review). After 3 rounds, move to output regardless.
5. **Every object gets metadata:** name (naming convention), material, thickness_mm. No exceptions.
6. **Break builds into 3-5 separate rhino_execute_python_code calls per agent.** Don't try to build everything in one script — Rhino can choke on large scripts.
7. **Print object counts after every script execution.** This is your diagnostic.
