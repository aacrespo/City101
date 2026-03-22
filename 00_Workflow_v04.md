# 00_WORKFLOW Ã¢â‚¬â€ BA6 Sentient Cities Studio

*Living document Ã¢â‚¬â€ update as project evolves*
*Version 04 Ã¢â‚¬â€ 24.02.2026*

---

# PART A: WORKING PRINCIPLES

## 1. CORE PRINCIPLES

### 1.1 For Information (LOI): Work Rich, Export Lean

**Collect maximum data from the start. Simplify only at export for specific outputs.**

- You can't predict what patterns you'll find in analysis
- More attributes = more analytical possibilities
- Filtering down is easy; adding missing data later is painful
- LOI should be HIGH from the beginning

### 1.2 For Geometry (LOG): Start Lean, Refine Progressively

**Keep geometry simple during iteration. Add detail only as design decisions lock.**

- Detailed geometry takes time to create AND to change
- Iterating on simple massing is fast
- Adding detail to a decided design is straightforward
- LOG should FOLLOW LOD (design certainty)

### 1.3 The Combined Principle

| Axis | Early Phase | Late Phase | Why |
|------|-------------|------------|-----|
| **LOI** (Information) | HIGH | HIGH (filtered for output) | Analysis needs rich data |
| **LOG** (Geometry) | LOW | HIGH | Iteration needs flexibility |
| **LOD** (Development) | LOW | HIGH | Decisions lock over time |

**Summary:**
- **LOI**: Work rich, export lean
- **LOG**: Start lean, refine progressively
- **LOD**: Increases as project progresses

---

## 2. THE LOG / LOI / LOD FRAMEWORK

### 2.1 Three Independent Axes

The BIM industry uses three distinct measures that are often confused. We use them precisely:

| Term | Full Name | Question It Answers | What It Measures |
|------|-----------|---------------------|------------------|
| **LOG** | Level of Geometry | What does it *look like*? | Visual/geometric complexity (vertices, surfaces, detail) |
| **LOI** | Level of Information | What do you *know* about it? | Data richness (attributes, metadata, relationships) |
| **LOD** | Level of Development | How much can you *trust* it? | Design certainty, reliability, how "locked" decisions are |

**These three axes are independent.** You can have any combination:

| Combination | What It Means | When It Happens |
|-------------|---------------|-----------------|
| Low LOG + High LOI + Low LOD | Simple geometry, rich data, design not decided | **Early analysis phase** Ã¢Å“â€œ |
| High LOG + Low LOI + Low LOD | Pretty render, no data, design not locked | **Dangerous** Ã¢â‚¬â€ looks done but isn't |
| High LOG + High LOI + Low LOD | Detailed with data, but design still fluid | Detailed study options |
| Low LOG + Low LOI + High LOD | Simple and sparse, but decision is final | Confirmed massing/zoning |
| High LOG + High LOI + High LOD | Detailed, data-rich, design locked | **Construction documents** |

### 2.2 The Key Insight: Decouple LOG from LOI

**Traditional approach:** Increase everything together as project progresses
**Our approach:** Maximize LOI early, add LOG only as LOD increases

Why? Because:
- **High LOI early** = more data for analysis, more patterns to discover
- **Low LOG early** = fast iteration, easy to change
- **LOG follows LOD** = add geometric detail only when design decisions lock

### 2.3 The Formula

**A complete element = LOG + LOI, evaluated at a given LOD**

Or practically:
```
Element completeness = How it looks (LOG) + What you know (LOI)
Element reliability = How decided it is (LOD)
```

### 2.4 The Spectrum (100Ã¢â‚¬â€œ500)

The 100Ã¢â‚¬â€œ500 scale can apply to LOG, LOI, or LOD independently:

**LOG (Level of Geometry) Spectrum:**

| LOG | Geometry | Description |
|-----|----------|-------------|
| **100** | Symbolic | Placeholder, icon, no real geometry |
| **200** | Massing | Approximate size, shape, location |
| **300** | Defined | Accurate dimensions, position, major features |
| **350** | Coordinated | Connections to other elements shown |
| **400** | Detailed | Full assembly detail, materiality |
| **500** | As-built | Verified accurate to reality |

**LOI (Level of Information) Spectrum:**

| LOI | Data Richness | Description |
|-----|---------------|-------------|
| **100** | Minimal | Name/ID only |
| **200** | Basic | Type, category, basic attributes |
| **300** | Extended | Specifications, performance data, metadata |
| **350** | Relational | Connections to other data, systems |
| **400** | Complete | Manufacturer data, costs, maintenance info |
| **500** | Verified | As-built data, confirmed in field |

**LOD (Level of Development) Spectrum:**

| LOD | Design Certainty | Description |
|-----|------------------|-------------|
| **100** | Exploring | Concept only, everything approximate |
| **200** | Direction set | General approach decided, details open |
| **300** | Dimensions matter | Key decisions locked, coordination possible |
| **350** | Relationships locked | Interfaces with other elements decided |
| **400** | Build from this | Verified for fabrication/construction |
| **500** | Matches reality | As-built, field verified |

### 2.5 LOG Per-Element Definitions

The generic spectrum above answers "what LOG level am I at?" The table below answers "what does that LOG level mean for THIS element?"

**LOG 200 — Massing**

| Element | What to model | What to skip |
|---------|--------------|--------------|
| Wall | Single solid, overall thickness | Layers, finish, openings |
| Floor / Roof | Single slab, overall thickness | Layers, edge conditions |
| Opening | Rectangular void, approximate size | Frame, glass, reveals, hardware |
| Furniture | Bounding box, correct overall dimensions | Form, legs, sub-components |
| Connection | Not modeled | — |
| Hardware | Not modeled | — |
| Stairs | Ramp or single solid volume | Treads, stringers, railing |
| Chimney | Vertical box | Flashing, fire stops |

**LOG 300 — Defined**

| Element | What to model | What to skip |
|---------|--------------|--------------|
| Wall | 2-3 zones: structure, insulation, finish (as separate solids) | Individual sub-layers, membranes |
| Floor / Roof | Structure zone vs finish zone distinguished | Individual sub-layers |
| Opening | Correct size + position. Frame as simple rectangular profile. Door/window as flat panel. | Reveal detail, weatherstripping, gaskets |
| Furniture | Recognizable silhouette: table with top + legs, chair with seat + back, bed with frame + mattress | Joinery, edge profiles, drawer runners |
| Connection | Elements positioned to meet correctly | Junction geometry (notches, laps) |
| Hardware | Not modeled | — |
| Stairs | Stringers + treads as separate objects, correct rise/going | Nosing detail, baluster infill |
| Chimney | Pipe with correct dimensions | Fire stop collars, flashing |

**LOG 350 — Coordinated / Assembly**

| Element | What to model | What to skip |
|---------|--------------|--------------|
| Wall | Individual layers as separate solids (cladding, air gap, wind barrier, studs, OSB, service cavity, finish) | Sub-millimeter details, sealant beads |
| Floor / Roof | Individual layers (structure, screed, insulation, membrane, finish, ceiling) | Fasteners, adhesive layers |
| Opening | Frame with reveals, sill projecting, lintel with bearing. Door leaf / window pane as simplified solid. | Gaskets, weatherstripping, hinge mechanism |
| Furniture | Major sub-components as separate objects: table top + legs + stretchers, drawer fronts, shelf boards, headboard | Edge profiles, finger joints, hardware |
| Connection | How layers meet at junctions: wall-floor blocking, corner posts, wind barrier returns, transition seals | Individual fasteners, bolt holes |
| Hardware | Symbolic: handles as simple boxes/cylinders at correct location | Mechanism, screws, springs |
| Stairs | Treads + stringers + railing with posts. Nosing as edge offset. | Baluster infill pattern, bracket detail |
| Chimney | Pipe + fire stop collars at each assembly crossing + flashing at roof | Mortar joints in collar, cap detail |

**LOG 400 — Detailed / Fabrication**

| Element | What to model | What to skip |
|---------|--------------|--------------|
| Wall | All layers + edge conditions: drip edges, corner returns, membrane overlaps, reveal returns | Screw patterns, adhesive |
| Floor / Roof | All layers + edge conditions: drainage falls, membrane laps, trim at perimeter | Individual tile/plank joints |
| Opening | Full frame profile, glazing panes with spacer, sill slope, reveal insulation, weatherstrip groove | Glass unit internal structure |
| Furniture | Joinery-level: housing joints, tenons, edge profiles, drawer runners, hinge locations | Glue lines, grain direction |
| Connection | Joints modeled: timber notches, steel brackets, bolt positions, bearing plates | Thread detail, washer geometry |
| Hardware | Simplified solids at correct locations: hinges, handles, locks, brackets | Internal mechanism |
| Stairs | Full detail: nosing profile, baluster pattern, newel posts, handrail profile, bracket fixings | Wood grain, finish layers |
| Chimney | Full assembly: pipe, collars, flashing cricket, cap, fire clearance sleeve | Internal flue lining |

**Adjacency Consistency Rule**

Elements visible together in a section or view should be within ONE LOG step of each other. A LOG 350 wall meeting LOG 100 furniture creates a visual lie — the wall layers have nowhere to terminate convincingly. Minimum: elements in direct contact should be at compatible LOGs.

| If structure is at... | Furniture must be at least... | Why |
|----------------------|------------------------------|-----|
| LOG 200 | LOG 100-200 | Massing study — boxes are fine |
| LOG 300 | LOG 200-300 | Defined — recognizable forms needed |
| LOG 350 | LOG 300 | Assembly — sub-components visible |
| LOG 400 | LOG 350 | Detail — joinery should match |

### 2.6 Custom Level: LOG 350v (Visual)

**LOG 350v** = Presentation-optimized geometry

- **Exterior/visible surfaces**: LOG 400 detail (materiality, textures, edges)
- **Interior/hidden elements**: LOG 200 or omitted entirely
- **Purpose**: Efficient rendering without modeling what won't be seen

**When to use**: Pin-up renders, portfolio images, animations
**When NOT to use**: Sections, coordination, anything showing interior

### 2.6 Working Principle by Project Phase

| Phase | LOG | LOI | LOD | Rationale |
|-------|-----|-----|-----|-----------|
| **Analysis** | 100Ã¢â‚¬â€œ200 | 400Ã¢â‚¬â€œ500 | 100 | Rich data, simple geometry, exploring |
| **Concept** | 200 | 300Ã¢â‚¬â€œ400 | 200 | Massing studies, direction setting |
| **Design Development** | 300 | 300Ã¢â‚¬â€œ400 | 300 | Defined geometry, decisions locking |
| **Detailed Design** | 350 | 350Ã¢â‚¬â€œ400 | 350 | Coordinated, relationships set |
| **Construction Docs** | 400 | 400Ã¢â‚¬â€œ500 | 400 | Full detail, build-ready |
| **As-Built** | 500 | 500 | 500 | Verified complete |

**Key insight:** Notice how LOI starts high and stays high, while LOG increases progressively as LOD increases.

---

## 3. LOG / LOI BY PRODUCTION TYPE

### 3.1 DATA PRODUCTION (QGIS, Geodata, CSV)

For data/analysis work, **LOI is the primary axis** Ã¢â‚¬â€ geometry is secondary.

**Production principle: Work with HIGH LOI from the start.**

| LOI | Data Richness | Use Case |
|-----|---------------|----------|
| **100** | Point locations only (lat/long) | Quick visualization, density maps |
| **200** | + Basic attributes (name, type, category) | Thematic mapping, simple analysis |
| **300** | + Extended attributes (capacity, hours, ratings, metadata) | Comparative analysis, filtering |
| **400** | + Relational data (connections between points, flows, networks) | Network analysis, flow mapping |
| **500** | + Temporal data (time series, change over time) | Dynamic analysis, animations |

**Rule**: Collect at LOI 400Ã¢â‚¬â€œ500. Export simplified versions (LOI 200Ã¢â‚¬â€œ300) for specific maps/outputs.

The LOG for data visualization is typically determined by the output scale (see Part B).

---

### 3.2 3D PRODUCTION (Rhino Models)

For 3D modeling, **LOG and LOI should both be tracked**.

You always model at 1:1. LOG describes **what you model** based on intended use:

| LOG | Geometry | When to Use |
|-----|----------|-------------|
| **100** | Extruded footprints, basic massing | Early massing studies, urban context |
| **200** | Defined volumes, floor plates, major voids | Schematic design, spatial testing |
| **300** | Facade divisions, structural elements, openings | Design development, coordination |
| **350** | Mullions, railings, stairs, key details | Presentation models, renders |
| **400** | Full material breaks, connections, hardware | Fabrication, shop models |
| **500** | As-built accuracy, verified dimensions | Documentation, facilities |

**LOI for 3D models** = metadata, material assignments, object names, layer organization, custom attributes

**Rule**: LOG follows LOD. Don't add geometric detail until design decisions justify it.

#### 3.2.1 Rhino MCP: Plan Before You Model

**Verify coordinate handling before placing geometry, and document a spatial plan before building.**

When modeling through MCP (or any scripted/parametric workflow), the first object you create should be a test to confirm how coordinates behave â€” specifically whether positions reference the object's center, a corner, or the construction plane origin. Different tools and functions handle this differently:

| Method | Position Reference | Predictability |
|--------|--------------------|----------------|
| `create_object` (MCP BOX) | **Center** â€” translation moves the center of the bounding box | Low â€” mental math for every placement |
| `rs.AddBox(corners)` (RhinoScript) | **8 corner points** â€” explicit min/max vertices | High â€” what you type is what you get |
| `rs.AddCylinder(plane, h, r)` | **Base plane center** â€” cylinder grows from plane origin | Medium â€” need to position the plane |

**The spatial plan rule:**

Before creating any geometry, write out (in comments or print statements) the coordinate system and key dimensions:

```python
# COORDINATE SYSTEM:
#   Origin (0,0,0) = interior SW corner at finished floor level
#   X = East (room width 5000)
#   Y = North (room depth 4000)
#   Z = Up (floor 0, ceiling 2800)
#   Wall thickness 200mm extends OUTWARD from interior
#
# TABLE: 2400 Ã— 1000, centered at (2500, 2000)
#   Top surface: Z = 750
#   Legs: Z 0â€“630, inset 60mm from edge
#
# CHAIRS: 8 total, centers 600mm from table edge
#   South (3): X = 1700, 2500, 3300  Y = 900
#   North (3): X = 1700, 2500, 3300  Y = 3100
#   West (1): X = 700  Y = 2000
#   East (1): X = 4300  Y = 2000
```

This takes 2 minutes and prevents the 20-minute debugging session when objects scatter across the viewport. It also survives context compression â€” if the conversation gets long, the spatial plan in the code comments is the reference, not a message from 40 turns ago.

**Practical workflow:**
1. Place one reference object (floor slab or bounding box) and verify its position visually
2. Document the full spatial plan as code comments
3. Build using explicit corner-point geometry (`rs.AddBox`) rather than center-offset placement
4. Capture a viewport after each major group (shell, furniture, details) to catch drift early

**Helper function worth keeping:**
```python
def box(x0, y0, z0, x1, y1, z1):
    """Create a box from min/max corners. No ambiguity."""
    pts = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ]
    return rs.AddBox(pts)
```

---

### 3.3 3D PRINT PREPARATION (LOG-P)

When exporting for physical models, additional geometry requirements apply:

| Requirement | Description |
|-------------|-------------|
| **Manifold/Watertight** | Every edge connected to exactly 2 faces, no holes |
| **No non-manifold edges** | No edges shared by >2 faces |
| **No zero-thickness** | All elements have real volume |
| **No internal faces** | Delete hidden geometry inside solids |
| **No overlapping geometry** | Boolean or separate cleanly |
| **Minimum wall thickness** | Typically 1Ã¢â‚¬â€œ2mm depending on printer/material |
| **Solid vs shell** | Decide based on print time/material/strength needs |
| **Correct normals** | All face normals pointing outward |

**Rhino commands for checking**:
- `SelBadObjects` Ã¢â‚¬â€ find problematic geometry
- `ShowEdges` > Naked Edges Ã¢â‚¬â€ find open edges
- `Dir` Ã¢â‚¬â€ check/flip surface normals
- `MeshRepair` Ã¢â‚¬â€ fix mesh issues before STL export

**Export formats**: STL, OBJ (check with print service)

**Tip**: Create a `_PRINT` layer or suffix for print-ready duplicates. Keep working model separate.

---

### 3.4 DIAGRAM PRODUCTION

Diagrams are conceptual Ã¢â‚¬â€ LOG refers to **communicative complexity**, LOI to **data depth**.

| LOG | Visual Complexity | Description |
|-----|-------------------|-------------|
| **100** | Iconic | Single concept, minimal elements, maximum abstraction |
| **200** | Relational | 2Ã¢â‚¬â€œ5 elements, showing basic relationships |
| **300** | Systematic | Multiple components, flows, feedback loops |
| **400** | Layered | Multiple overlapping systems, legend required |
| **500** | Annotated | Full explanation, quantitative data embedded |

**Principle**: Match diagram LOG to audience. Pin-up = LOG 200Ã¢â‚¬â€œ300. Final booklet = LOG 300Ã¢â‚¬â€œ400.

---

## 4. DATA COLLECTION PROTOCOL (Maximizing LOI)

### 4.1 Before Querying

Before pulling any dataset, pause and define:

1. **Entity type** Ã¢â‚¬â€ What exactly are we collecting? (charging stations, bus stops, cafÃƒÂ©s...)
2. **All possible attributes** Ã¢â‚¬â€ Brainstorm beyond the obvious. What *might* exist?
3. **Potential sources** Ã¢â‚¬â€ Different sources have different strengths:
   - OSM: community tags, coverage, open
   - Google Places: reviews, hours, photos, popularity
   - Official Swiss: technical specs, compliance, authoritative
   - Academic/reports: behavioral data, studies
   - Social media: sentiment, real usage patterns

### 4.2 Attribute Categories to Consider

Use this as a brainstorming checklist Ã¢â‚¬â€ not everything applies, but scan it:

| Category | Example Attributes |
|----------|-------------------|
| **Identity** | name, ID, type, subtype, operator, brand, network |
| **Location** | coordinates, address, elevation, zone, accessibility |
| **Physical** | size, capacity, material, covered/exposed, condition |
| **Temporal** | hours, seasonality, date established, last updated |
| **Relational** | nearby amenities, connections, catchment area, part of route |
| **Behavioral** | ratings, reviews, usage patterns, wait times, peak hours |
| **Technical** | specs, standards, compliance, power output, compatibility |

### 4.3 After Initial Collection

- **Attribute gap analysis**: What's missing from what we brainstormed?
- **Source check**: Can another source fill the gap?
- **Gap triage**: Is this gap acceptable, or critical to the analysis?

### 4.4 Document in Handoff

When datasets are created or modified, note:
- Sources + query date
- Known attribute gaps
- Any enrichment still needed

---

# PART B: SCALE CONVENTIONS REFERENCE

## 4. FUNDAMENTAL PRINCIPLES

### 4.1 The Universal Rule: As Scale Decreases, Abstraction Increases

Detail drawings show every screw; masterplans show only urban fabric.

### 4.2 The 1mm Rule

**If a real-world element would measure less than approximately 1mm when drawn at the chosen scale, either omit it or represent it with a symbol.**

This single principle governs detail-level decisions across all scales:

| Real element | At 1:50 | At 1:100 | At 1:200 | At 1:500 |
|--------------|---------|----------|----------|----------|
| 200mm wall | 4mm Ã¢Å“â€œ | 2mm Ã¢Å“â€œ | 1mm Ã¢Å“â€œ | 0.4mm Ã¢â€ â€™ single line |
| 50mm insulation | 1mm Ã¢Å“â€œ | 0.5mm Ã¢â€ â€™ line | omit | omit |
| 10mm door frame | 0.2mm Ã¢â€ â€™ simplified | omit | omit | omit |
| 900mm door | 18mm Ã¢Å“â€œ | 9mm Ã¢Å“â€œ | 4.5mm Ã¢Å“â€œ | 1.8mm Ã¢â€ â€™ gap or omit |

### 4.3 Conventions Are Guidelines, Not Laws

**These conventions are calibrated for traditional paper output at specific sizes.**

In practice, output medium changes everything:
- **Color** can replace line weight hierarchy
- **Digital viewing** has no fixed scale Ã¢â‚¬â€ only relative legibility
- **Projection** has different constraints than print
- **Communication intent** may override convention

Use conventions as a starting point, then adapt to your actual output context.

---

## 5. MASTER SCALE OVERVIEW

| Scale | Primary Use | Wall Representation | Line Weights (cut/view/hatch) | Min. Text | Material Hatching |
|-------|-------------|---------------------|-------------------------------|-----------|-------------------|
| **1:1** | Full-size fabrication templates | Every layer, exact thickness | 1.00 / 0.50 / 0.13 mm | 2.5 mm | Realistic: grain, aggregate, texture |
| **1:2** | Joinery, curtain wall profiles | All layers proportional | 0.70Ã¢â‚¬â€œ1.00 / 0.50 / 0.13 mm | 2.5 mm | Detailed, minor simplification |
| **1:5** | Construction details (THE detail standard) | All layers individually drawn | 1.00 / 0.50 / 0.18 mm | 2.5 mm | Full material-specific patterns |
| **1:10** | Assembly details, joinery | Major layers; thin ones combined | 0.70 / 0.50 / 0.18 mm | 2.5 mm | Standard hatch; transition to schematic |
| **1:20** | Room plans, enlarged sections | Layers visible; <5mm layers as lines | 0.70 / 0.35 / 0.13 mm | 2.5 mm | Simplified; thin materials as single lines |
| **1:50** | Execution plans (THE workhorse) | Individual layers with hatching | 0.50 / 0.25 / 0.13 mm | 2.5 mm | Material-specific per element |
| **1:100** | Design plans, building permit | Double-line, solid fill or grey | 0.35Ã¢â‚¬â€œ0.50 / 0.18 / 0.13 mm | 2.0Ã¢â‚¬â€œ2.5 mm | PochÃƒÂ© or simple fill; no layers |
| **1:200** | Concept plans, competitions | Single thick line or solid black | 0.35 / 0.18 / 0.13 mm | 2.0 mm | Solid fill only; no hatching |
| **1:500** | Site plans, landscape | Building footprints as outlines | 0.50 / 0.25 / 0.13 mm | 2.5 mm | Surface/ground cover patterns |
| **1:1000** | Neighborhood, campus plans | Simplified building outlines | 0.35 / 0.18 / 0.09 mm | 2.5 mm | Zone fills, simplified textures |
| **1:2000** | District, zoning plans | Block perimeters | 0.35 / 0.18 / 0.09 mm | 2.5 mm | Color-coded land use zones |
| **1:5000** | Masterplans, transportation | Generalized blocks | 0.25 / 0.18 / 0.09 mm | 2.5 mm | Abstract zone fills |
| **1:10000** | Regional, city-wide plans | Built-up area zones | 0.25 / 0.13 / 0.09 mm | 2.5 mm | Generalized land cover |

---

## 6. DETAIL SCALES (1:1 through 1:20)

### 6.1 Scale 1:1 Ã¢â‚¬â€ Full-Size Fabrication Templates

**Use for**: Custom metalwork profiles, moulding cross-sections, gasket details, CNC routing templates

At 1:1, every element appears at actual size Ã¢â‚¬â€ the drawing becomes a direct template for fabrication.

**What to show**:
- Exact material grain and texture (wood growth rings, steel surface finish)
- Precise cross-sectional profiles of every material layer
- All fastener details including screw threads and bolt heads
- Sealant beads and gasket profiles at true thickness
- Tolerances and expansion gaps
- Weld symbols per ISO 2553
- Specific product reference codes
- Surface treatments and coatings with precise hatching

**What to omit**:
- Surrounding context beyond the immediate detail
- Room-level information
- Building grid lines
- General project notes

**Line weights**: 1.0mm for cut boundaries, 0.50mm for visible edges, 0.25mm for dimensions, 0.13Ã¢â‚¬â€œ0.18mm for hatching

**Material representation**: Realistic Ã¢â‚¬â€ concrete shows stipple patterns simulating aggregate, wood displays detailed end-grain growth rings, steel gets dense 45Ã‚Â° cross-hatching, membranes appear at true thickness as solid black strips

**Hatch spacing**: 1Ã¢â‚¬â€œ2mm

---

### 6.2 Scale 1:2 Ã¢â‚¬â€ Complex Component Sections

**Use for**: Curtain wall mullion profiles, window frame sections with all seals, structural steel connections, waterproofing membrane laps

A 0.5mm real membrane appears as 0.25mm on the drawing Ã¢â‚¬â€ still legible. Gasket profiles are simplified slightly from 1:1 but retain their exact shape. Fastener positions use simplified symbols (circles for bolts, crosses for screws) at correct locations. Thread-level detail shifts to ISO 6410 simplified representation.

**Hatch spacing**: 2Ã¢â‚¬â€œ3mm

---

### 6.3 Scale 1:5 Ã¢â‚¬â€ The Construction Detail Standard

**This is the most important detail scale in European practice.** DIN 1356 classifies it as the primary "Detailzeichnung" scale. Wall sections, window head/sill/jamb details, eaves, parapets, balcony waterproofing, and structural connections all live here.

**What to show**:
- Every material layer in wall/floor/roof build-ups drawn to scale
- Screw and bolt positions as simplified symbols at correct locations
- DPC/DPM membranes as thick black lines
- Insulation with standard zigzag hatching
- Cavity widths dimensioned
- Flashing profiles with lap directions
- Timber and steel member sizes labeled
- Movement joints
- Material-specific hatching for every material in section
- Fixing specifications as annotations (e.g., "M10 bolt at 300 c/c")

**What to omit**:
- Individual nail thread details (use symbols)
- Decorative surface textures (note only)
- Furniture and room context
- Excessive rebar detail (reference structural drawings)
- Exact gasket profiles (schematize)

**Line weights**: 1.0mm cut boundaries, 0.50mm visible edges, 0.25mm dimensions. Minimum legible line: 0.18mm; 0.13mm only for finest hatching.

**Hatch spacing**: 3Ã¢â‚¬â€œ5mm

---

### 6.4 Scale 1:10 Ã¢â‚¬â€ Assembly Details and Joinery

**Use for**: Window assemblies, built-in furniture sections, staircase details, ceiling coffer sections, MEP penetration details

The transition from "detailed" to "schematic" representation begins here. Wall build-up layers remain visible but very thin layers (under 2mm real = under 0.2mm on paper) are combined or omitted. Hardware positions appear as simplified symbols. Fasteners are noted by specification rather than drawn in detail.

**Hatch spacing**: 4Ã¢â‚¬â€œ7mm

---

### 6.5 Scale 1:20 Ã¢â‚¬â€ Room Details and Enlarged Plans

**Use for**: Bathroom layouts, kitchen coordination plans, stair sections, interior elevation details

This scale bridges detail and building scales.

**What to show**:
- Door swings with 90Ã‚Â° arcs (MUST be shown)
- Window openings with frame indication and glazing lines
- Floor finishes, skirtings, and thresholds
- Sanitary fixtures as standard plan symbols (not detailed cross-sections)
- Built-in furniture with dimensioned outlines
- Room labels with area (e.g., "BEDROOM 1 / 14.5 mÃ‚Â²")
- Complete dimension chains in meters to three decimal places
- Level markers with triangular symbols
- Cross-reference bubbles linking to 1:5 or 1:10 details

**What to omit**:
- Individual screws and bolt positions (too small to read)

**Line weights**: 0.70mm for section boundaries, 0.35mm for visible edges, 0.25mm for dimensions. Material layers thinner than 5mm real (0.25mm on paper) become single lines rather than filled hatching.

**Hatch spacing**: 5Ã¢â‚¬â€œ10mm

---

## 7. BUILDING SCALES (1:50 through 1:200)

### 7.1 Scale 1:50 Ã¢â‚¬â€ The Execution Plan Workhorse

**1:50 is the universal construction drawing scale across all European standards systems.** Swiss SIA Phase 51 (AusfÃƒÂ¼hrungsprojekt), German HOAI LP5 (AusfÃƒÂ¼hrungsplanung), UK RIBA Stage 4 (Technical Design).

**What to show** (extensive):
- Walls display individual construction layers Ã¢â‚¬â€ structure, insulation, air gap, cladding Ã¢â‚¬â€ each with material-specific hatching
- Doors show full swing arcs with frame profiles, sill details, opening-type indication
- Windows show frame geometry and opening mechanisms
- Built-in furniture with manufacturer dimensions: kitchen appliances, sanitary fixtures, wardrobes
- Stairs with going/rise dimensions, tread numbering, handrail positions, up/down arrows
- Structural columns with profiles; beams above cut plane as dashed lines
- MEP fixtures: outlet positions, switch locations, radiators
- Complete dimension chains: overall, axis-to-axis, wall-to-wall, opening dimensions Ã¢â‚¬â€ in meters to three decimal places (e.g., 3.150)

**What to omit**:
- Electrical wiring routing (separate MEP drawings)
- Full reinforcement details (structural drawings)
- Manufacturing-level joinery details (reference 1:20 or 1:5 details)
- Individual bolt/screw connections

**Line weights**:

| Element | Weight |
|---------|--------|
| Cut walls/floors (structure) | **0.50Ã¢â‚¬â€œ0.70mm** |
| Cut secondary elements | 0.35mm |
| Elements in view (furniture) | 0.25mm |
| Dimensions, annotations | 0.18Ã¢â‚¬â€œ0.25mm |
| Hatching patterns | 0.13Ã¢â‚¬â€œ0.18mm |
| Ground line in sections | 0.70Ã¢â‚¬â€œ1.00mm |

**Text heights on paper**: Room names 3.5Ã¢â‚¬â€œ5.0mm, dimensions 2.5mm, drawing titles 5.0Ã¢â‚¬â€œ7.0mm

**Dimension terminators**: 45Ã‚Â° oblique tick (standard across SIA, DIN, ISO Ã¢â‚¬â€ arrowheads reserved for engineering)

---

### 7.2 Scale 1:100 Ã¢â‚¬â€ The Design Development Scale

Primary scale for Swiss SIA Phase 32 (Bauprojekt), German Bauantrag/building permit submissions, general design coordination.

**The critical shift from 1:50 to 1:100 is wall representation:**
- Walls become **double lines with solid fill** (black, dark grey, or simple diagonal hatching) Ã¢â‚¬â€ no individual material layers
- Load-bearing walls may be distinguished from partitions by fill weight or pattern
- Door swings appear as single-line leaves with 90Ã‚Â° arcs
- Window openings show as wall breaks with glazing lines
- Furniture appears as basic outlines (beds, tables, sofas) in thin line weight
- Stairs simplified with numbered treads, direction arrow, break line, handrail

**What to omit at 1:100**:
- Wall construction layers
- Door/window frame profiles
- MEP fixture details
- Floor finish patterns
- Construction dimension chains
- Stair rise/going dimensions
- Material-specific hatching within walls

**Line weights**: 0.35Ã¢â‚¬â€œ0.50mm for cut walls, 0.18Ã¢â‚¬â€œ0.25mm for visible elements, 0.13mm for hatching

**Text heights**: Room names 2.5Ã¢â‚¬â€œ3.5mm, dimensions 2.0Ã¢â‚¬â€œ2.5mm. Dimensions shift to meters with two decimal places (e.g., 4.50m)

---

### 7.3 Scale 1:200 Ã¢â‚¬â€ Concept and Competition Plans

**Use for**: Early design phases (SIA Phase 2 Vorstudien), competition submissions, large building overviews

**Wall representation**:
- **Single thick lines or solid black fills** (pochÃƒÂ©) creating figure-ground contrast
- "Nolli plan" aesthetic Ã¢â‚¬â€ solid black mass with white room voids
- Doors become simple gaps in wall lines
- Windows may appear as thin line breaks or disappear entirely
- Furniture is omitted
- Only principal building dimensions remain

**Critical consideration**: At 1:200, a 200mm wall is only 1mm on paper Ã¢â‚¬â€ thick line weights can obliterate internal spaces.

**Line weights**: 0.35Ã¢â‚¬â€œ0.50mm building outline, 0.25mm interior walls, 0.13Ã¢â‚¬â€œ0.18mm context

**Material hatching**: Largely eliminated; walls rely on solid fill for legibility

**Minimum legible text**: ~1.8mm per ISO, though 2.0Ã¢â‚¬â€œ2.5mm advisable for room names

---

## 8. URBAN AND SITE SCALES (1:500 through 1:10000)

### 8.1 Scale 1:500 Ã¢â‚¬â€ The Site Plan Standard

Most common scale for European architectural site plans (Situationsplan/Lageplan), landscape plans, Swiss Baubewilligungsplan.

**What to show**:
- Individual building footprints with entrances and access points
- Individual trees drawn to canopy scale (5Ã¢â‚¬â€œ15m diameter)
- Parking spaces individually delineated
- Property boundaries with survey markers
- Setback/building lines (Baulinien)
- **Contour lines at 0.5m intervals** with index contours every 2.5m
- Spot levels at key points
- Road carriageways with kerb lines, footpaths, cycle paths
- Water features with flow direction
- Fencing and wall types
- Landscaping details: paving patterns, planting beds

**Line weights**: 0.50Ã¢â‚¬â€œ0.70mm for property boundaries and proposed buildings, 0.35mm for existing context and roads, 0.25Ã¢â‚¬â€œ0.35mm for index contours, 0.18Ã¢â‚¬â€œ0.25mm for intermediate contours and vegetation, 0.13Ã¢â‚¬â€œ0.18mm for annotations

**Buildings**: Solid black/dark grey fill (proposed) or lighter grey (existing)

**Scale bars**: Show 0Ã¢â‚¬â€œ10Ã¢â‚¬â€œ20Ã¢â‚¬â€œ50m intervals. North arrows 15Ã¢â‚¬â€œ25mm on paper.

---

### 8.2 Scale 1:1000 Ã¢â‚¬â€ Neighborhood and Campus

**Use for**: Large site plans, campus layouts, Swiss Bebauungsplan, park masterplans

- Buildings simplify to **outlines without internal detail**
- Trees shift from individuals to clusters (except significant specimens)
- Parking becomes zone-based rather than individual spaces
- **Contour intervals widen to 1.0m** with 5m index contours
- Street hierarchy differentiated by line weight (primary, secondary, local)
- Property boundaries show major parcels only

---

### 8.3 Scale 1:2000 Ã¢â‚¬â€ District and Zoning Frameworks

**Use for**: Urban design frameworks, zoning maps (Zonenplan), masterplan concepts

- Individual buildings within dense blocks aggregate into **block perimeters**
- Land use zones receive color coding or hatching
- **Contour intervals reach 2.0m**
- Transportation networks show road hierarchy and rail lines
- Individual trees disappear entirely

**Land use color conventions** (European practice):
- Residential: yellow shades (darker = higher density)
- Commercial: red/orange
- Industrial: purple/grey
- Institutional: blue
- Open space: green

**For black-and-white**: Hatching substitutes Ã¢â‚¬â€ residential gets diagonal lines at varying spacing, commercial uses crosshatch, green space uses organic stipple

---

### 8.4 Scale 1:5000 Ã¢â‚¬â€ Masterplans and Strategic Frameworks

- City quarter masterplans and strategic development frameworks
- Generalized building blocks
- Major road networks only
- **5.0m contour intervals**
- Individual building footprints disappear Ã¢â‚¬â€ aggregated into urban fabric blocks
- Only motorways, arterial roads, and rail lines visible

---

### 8.5 Scale 1:10000 Ã¢â‚¬â€ Regional and City-Wide Plans

- Urban areas become generalized built-up zones
- Only major transport corridors, administrative boundaries, rivers, large-scale land use patterns
- **Contour intervals: 5Ã¢â‚¬â€œ10m**
- Line weights compress: 0.25mm maximum for boundaries, 0.13mm for most features, 0.09mm for fills
- Scale bars mark kilometers

---

## 9. CONTOUR INTERVALS BY SCALE

| Scale | Contour Interval | Index Contour |
|-------|------------------|---------------|
| 1:500 | **0.5m** | Every 2.5m |
| 1:1000 | **1.0m** | Every 5m |
| 1:2000 | **2.0m** | Every 10m |
| 1:5000 | **5.0m** | Every 25m |
| 1:10000 | **5Ã¢â‚¬â€œ10m** | Every 25Ã¢â‚¬â€œ50m |

Index contours: 0.25Ã¢â‚¬â€œ0.35mm; intermediate contours: 0.13Ã¢â‚¬â€œ0.18mm
Labels appear on index contours only, oriented so reading uphill reads the number right-side-up.

---

## 10. LINE WEIGHT SYSTEM

### 10.1 The ISO 128 Pen Size Series

All European standards derive from the same geometric progression (Ã¢Ë†Å¡2 ratio):

**0.13, 0.18, 0.25, 0.35, 0.50, 0.70, 1.00, 1.40, 2.00 mm**

Each successive width multiplies by ~1.414, matching Ã¢Ë†Å¡2 scaling of A-series paper. When A3 is photocopied to A4, a 0.35mm line becomes 0.25mm Ã¢â‚¬â€ hierarchy maintained automatically.

### 10.2 The Three-Weight Hierarchy

ISO 128-2 prescribes a **4:2:1 ratio** (extra-wide : wide : narrow), limiting any single drawing to three line weights:

| Function | Ratio | Typical Weights |
|----------|-------|-----------------|
| **Cut elements** (section cuts) | 4 | 0.50Ã¢â‚¬â€œ1.00mm |
| **Visible edges** (in view) | 2 | 0.25Ã¢â‚¬â€œ0.50mm |
| **Secondary** (dimensions, hatching) | 1 | 0.13Ã¢â‚¬â€œ0.25mm |

In practice, professional offices use 5Ã¢â‚¬â€œ7 line weights in CAD.

### 10.3 Standards Comparison

| Standard | Cut Elements | Visible Edges | Dimensions | Hatching |
|----------|--------------|---------------|------------|----------|
| **SIA 400** (Swiss) | Dick (0.50Ã¢â‚¬â€œ0.70) | Mittel (0.35) | DÃƒÂ¼nn (0.18Ã¢â‚¬â€œ0.25) | DÃƒÂ¼nn (0.13) |
| **DIN 1356** (German) | Breit (0.50Ã¢â‚¬â€œ1.00) | Breit/Schmal | Schmal (0.25) | Schmal (0.13) |
| **ISO 128** (International) | Wide (Type A) | Wide (Type A) | Narrow (Type B) | Narrow |
| **BS 8888** (British) | Wide (0.50Ã¢â‚¬â€œ0.70) | Wide (0.35Ã¢â‚¬â€œ0.50) | Narrow (0.18Ã¢â‚¬â€œ0.25) | Narrow (0.13) |

### 10.4 Four Pens Cover Most Hand-Drawing

**0.18, 0.25, 0.35, 0.50 mm** handles the majority of architectural drawing at any scale.

---

## 11. TEXT AND ANNOTATION

### 11.1 Text Heights (Constant on Paper)

Regardless of drawing scale, text height is defined as its **printed size on paper**.

ISO 3098 standard height series (Ã¢Ë†Å¡2 progression): **1.8, 2.5, 3.5, 5.0, 7.0, 10, 14, 20 mm**

| Text Purpose | Height on Paper |
|--------------|-----------------|
| Dimensions, general notes | **2.5mm** (universal minimum) |
| Room names, sub-headings | **3.5mm** |
| Drawing titles | **5.0Ã¢â‚¬â€œ7.0mm** |
| Sheet/project titles | **7.0Ã¢â‚¬â€œ10mm** |

**In CAD**: Multiply plotted height by scale factor. 2.5mm text at 1:100 = 250mm model-space height.

**Font**: Sans-serif (ISOCP, Arial, Helvetica). Upper case improves legibility. Stroke thickness Ã¢â€°Ë† 1/10 of character height.

### 11.2 Dimensioning Conventions

**Terminators**: 45Ã‚Â° oblique tick marks for construction drawings (arrowheads reserved for mechanical engineering)

**Units**:
- SIA (Swiss): meters to three decimal places (e.g., 5.230m)
- DIN (German): meters for plans, millimeters for details
- BS (British): historically millimeters, shifting to meters for large-scale

**Level references**:
- SIA: meters above sea level (m ÃƒÂ¼.M. Ã¢â‚¬â€ Meter ÃƒÂ¼ber Meer)
- DIN/BS: project datum (Ã‚Â±0.00 at finished ground floor)

---

## 12. MATERIAL HATCHING

### 12.1 Scale-Dependent Hatching Density

Hatch line spacing should remain **1.5Ã¢â‚¬â€œ3mm on the printed page** regardless of scale.

| Scale | Hatch Spacing on Paper | Approach |
|-------|------------------------|----------|
| 1:1 to 1:2 | 1Ã¢â‚¬â€œ2mm | Dense; realistic texture |
| 1:5 | 3Ã¢â‚¬â€œ5mm | Standard detail hatching |
| 1:10 to 1:20 | 4Ã¢â‚¬â€œ10mm | Wider spacing; thin materials become single lines |
| 1:50 | Standard CAD hatch | Full material patterns |
| 1:100 | Solid fill or simple lines | Material hatching largely omitted |
| 1:200+ | No hatching | Walls as solid pochÃƒÂ© |

### 12.2 Material Conventions (Universal)

| Material | Convention | Notes |
|----------|------------|-------|
| **Reinforced concrete** | 45Ã‚Â° diagonals + stipple dots | Aggregate indication |
| **Masonry** | Diagonal cross-hatching at 45Ã‚Â° | Brick (tight) vs. block (wide) spacing |
| **Steel** | Solid black fill or dense diagonals | Consistent across all standards |
| **Wood (section)** | Concentric arcs (growth rings) | SIA/DIN nearly identical |
| **Insulation** | Zigzag/sinusoidal wavy lines | Universal |
| **Earth** | Diagonal lines with scattered dots | Minor variations |
| **Glass** | Single thin line or solid fill | Consistent |

**Rule**: Adjacent cut materials must alternate hatching direction. Large cut areas may limit hatching to a zone following the contour.

---

# PART C: OUTPUT-SPECIFIC CONSIDERATIONS

## 13. THE OUTPUT CHANGES EVERYTHING

**Standard conventions assume traditional paper output at specific sizes. Modern outputs vary significantly.**

### 13.1 Output Types and Their Constraints

| Output Type | Scale Matters? | Key Constraint | Adaptation Needed |
|-------------|----------------|----------------|-------------------|
| **Paper print (A1, A0)** | Yes Ã¢â‚¬â€ fixed | Physical line thickness, viewing distance | Follow conventions closely |
| **Paper print (A3, A4)** | Yes Ã¢â‚¬â€ fixed | Reduced size, line legibility | May need thicker lines, simpler detail |
| **Pin-up panel** | Yes Ã¢â‚¬â€ fixed | Viewing distance (1Ã¢â‚¬â€œ3m typical) | Heavier lines, larger text than conventions suggest |
| **Screen/digital** | No Ã¢â‚¬â€ zoomable | Viewport size, pixel density | Relative legibility matters, not absolute scale |
| **Projection** | No Ã¢â‚¬â€ variable | Room size, ambient light, resolution | Heavy contrast, simplified detail |
| **PDF for review** | Partially | Screen viewing + potential print | Dual optimization needed |

### 13.2 When Scale Doesn't Apply

**Digital viewing fundamentally changes the relationship:**

- There's no fixed "scale" Ã¢â‚¬â€ users zoom in and out
- A 1:500 site plan viewed at 100% on a laptop might show a 50m Ãƒâ€” 50m area
- The same plan zoomed to 200% shows 25m Ãƒâ€” 25m at "1:250 equivalent"
- **What matters: legibility relative to likely viewing context**

**Questions to ask for digital output:**
- What's the minimum viewport size this will be viewed at?
- What elements must remain legible at minimum zoom?
- What elements can rely on zoom-in for detail?

---

## 14. COLOR VS. LINE WEIGHT

### 14.1 Color as Hierarchy

**When using color, you may not need the same line weight hierarchy Ã¢â‚¬â€ color IS the hierarchy.**

Example approaches:

| Monochrome Approach | Color Alternative |
|---------------------|-------------------|
| Heavy line = cut elements | Red = new/proposed |
| Medium line = visible | Grey = existing |
| Light line = secondary | Black = retained |

| Monochrome Approach | Color Alternative |
|---------------------|-------------------|
| Line weight shows depth | Color shows systems |
| Hatching shows materials | Color fills show materials |
| Solid black = structure | Blue = water, Red = fire, Yellow = electrical |

### 14.2 Color Considerations

**Advantages of color:**
- Faster visual parsing
- Can encode additional information layers
- More engaging for presentations
- Distinguishes systems that would overlap in B&W

**Risks of color:**
- May not print well in B&W (always test!)
- Colorblind accessibility (avoid red-green distinctions alone)
- Projectors wash out subtle color differences
- Some review contexts require B&W (permit submissions)

**SIA 400 principle**: *"Sinnbilder werden wenn immer mÃƒÂ¶glich schwarzweiss dargestellt"* Ã¢â‚¬â€ Symbols shown in B&W whenever possible. Color improves readability but must not carry information unavailable in B&W.

### 14.3 Testing Your Output

**Always test before final output:**
- Print a sample at actual size
- View on target screen/projector
- Check B&W conversion if color used
- Verify from intended viewing distance

---

## 15. DIGITAL AND PROJECTION SPECIFICS

### 15.1 Screen Output Guidelines

| Screen Context | Minimum Line | Minimum Text | Notes |
|----------------|--------------|--------------|-------|
| Large monitor (27"+) close viewing | 1px | 10px | Detail work acceptable |
| Laptop (13Ã¢â‚¬â€œ15") | 1.5Ã¢â‚¬â€œ2px | 12px | Simplify detail |
| Tablet/iPad | 2px | 14px | Touch interaction, less precision |
| Phone | 3px+ | 16px+ | Only for overview/navigation |

**Pixel vs. mm**: At 96 DPI (typical screen), 1mm Ã¢â€°Ë† 3.8 pixels. A 0.13mm line = 0.5px = invisible.

### 15.2 Projection Guidelines

Projectors typically:
- Wash out fine lines
- Reduce contrast
- Blur fine text
- Depend heavily on room lighting

**Adaptation for projection:**
- Increase line weights by 50Ã¢â‚¬â€œ100%
- Minimum text: 5mm equivalent at slide scale
- High contrast: avoid mid-greys
- Test in actual room conditions if possible

### 15.3 PDF Optimization

For PDFs that will be both viewed on screen and potentially printed:
- Use vector graphics (not rasterized)
- Embed fonts
- Test at 100% and 50% zoom
- Include scale bar (written scale useless after zoom)

---

# PART D: STUDIO FRAMEWORK

## 16. BA6 SENTIENT CITIES CONTEXT

### 16.1 Semester Arc

- BA5 = "Urban brain" Ã¢â‚¬â€ the central intelligence
- **BA6 = Organs, nervous systems, distributed sensors** Ã¢â‚¬â€ the city's pulse, patterns, rhythms
- Focus: **Peripheral Typologies** Ã¢â‚¬â€ nodes in a cognitive urban system
- Approach: Architecture that senses and responds *with and through machines*

### 16.2 Key Questions (from course brief)

Use these to test your work:

- [ ] What are the aesthetics of data?
- [ ] How can cognition be spatialized?
- [ ] How might flows of sensing, computation, and action take on physical and cultural meaning?
- [ ] What if a city begins to dream? What would those dreams be?
- [ ] What roles would citizens play in them?

### 16.3 Assessment Criteria

Self-review against these before crits:

1. **Conceptual strength and innovation** Ã¢â‚¬â€ Is the idea compelling?
2. **Coherence and resolution of architectural translation** Ã¢â‚¬â€ Does the design follow from the concept?
3. **Representative clarity and expressive power** Ã¢â‚¬â€ Are the drawings/models communicating well?
4. **Persuasiveness of communication** Ã¢â‚¬â€ Can you argue for this convincingly?

---

## 17. PROJECT PHASES AND TYPICAL SCALES

| SIA (Swiss) | HOAI (German) | RIBA (British) | Typical Scales |
|-------------|---------------|----------------|----------------|
| Phase 2: Vorstudien | LP2: Vorplanung | Stage 2: Concept Design | 1:500, 1:200 |
| Phase 31: Vorprojekt | LP3: Entwurfsplanung | Stage 3: Spatial Coordination | **1:100** |
| Phase 32: Bauprojekt | LP4: Genehmigungsplanung | Stage 3 (planning) | 1:100 |
| Phase 51: AusfÃƒÂ¼hrungsprojekt | LP5: AusfÃƒÂ¼hrungsplanung | Stage 4: Technical Design | **1:50**, 1:20Ã¢â‚¬â€œ1:1 |

**Universal pattern**: Concept at 1:200, design at 1:100, construction at 1:50, details at 1:20 down to 1:1.

---

# PART E: HANDOFF SYSTEM

## 18. WHEN TO CREATE HANDOFFS

**Mandatory:**
- End of every working session
- Before uploading heavy documents (summarize intent first)
- When a major decision is made
- When context compression happens mid-conversation

**Optional checkpoints:**
- New dataset created or significantly modified
- Technical problem solved (or identified)
- New idea or framing developed
- Anything painful to lose or re-explain

---

## 19. HANDOFF TEMPLATE

```markdown
# HANDOFF Ã¢â‚¬â€ [DD-MM] Session [n]

## Last action
[1-2 sentences: what we just did/decided]

## Current state
[Active datasets, files, what's loaded in QGIS/Rhino, LOG/LOI levels of current work]

## Open threads
[What's in progress or unresolved]

## Key decisions made (cumulative)
[Running list of settled decisions Ã¢â‚¬â€ don't re-litigate these]

## Technical notes
[File paths, CRS, parameters, anything specific to pick up work]

## Data sources (this session)
[One line per dataset created/modified. Include source + date. Skip if no data work.]
- Example: EV charging points: OSM Overpass (17.02.26) + Google Places API (17.02.26)

## Crit notes (if any)
[Optional. Only if there was a review/crit worth capturing. 5 bullets max.]
```

### Naming Convention

`HANDOFF_DD-MM_S[n].md`

- DD-MM = date
- S[n] = session number that day (S1, S2, S3...)
- Each new handoff **replaces** the previous one (don't accumulate)

---

# PART F: FILE CONVENTIONS

## 20. FILE NAMING

### 20.1 General Pattern

`[DATE]_[TYPE]_[DESCRIPTION]_[LOD]_v[##]`

Examples:
- `260217_map_ev-charging-dwell_LOD200_v01`
- `260217_model_peripheral-node_LOD350v_v02`
- `260217_diagram_flow-analysis_LOD100_v01`

### 20.2 Type Prefixes

| Prefix | Use for |
|--------|---------|
| `map_` | QGIS outputs, spatial analysis |
| `model_` | Rhino/3D files |
| `diagram_` | Conceptual/analytical graphics |
| `render_` | Presentation images |
| `data_` | CSV, GeoJSON, datasets |
| `doc_` | Written documents, reports |

### 20.3 Version Control

- `v01`, `v02`, `v03`... for iterations
- Keep previous versions (don't overwrite)
- Note version changes in handoff

---

## 21. TOOLS & TECHNICAL SETUP

### 21.1 Software Stack

| Tool | Use | CRS/Settings |
|------|-----|--------------|
| QGIS | Spatial analysis, mapping | Swiss LV95 / EPSG:2056 |
| Rhino | 3D modeling | Units: meters |
| Grasshopper | Parametric workflows | Ã¢â‚¬â€ |
| Claude (this) | Research, analysis, coding, documentation | Ã¢â‚¬â€ |

### 21.2 Data Sources

- **OpenStreetMap** (via OSM MCP)
- **Google Places API**
- **Swisstopo** (TLM3D, Boundaries, SWISSBUILDINGS)
- **Swiss official datasets**

### 21.3 MCP Servers Available

- OSM MCP (needed SSL cert fix on macOS)
- Rhino MCP
- QGIS MCP

---

# PART G: WORKING WITH CLAUDE

## 22. CONTEXT MANAGEMENT

**Problem**: Long conversations get compressed, losing early nuance.

**Mitigations**:
- Create handoffs during sessions, not just at the end
- Shorter focused conversations > one mega-session
- Front-load intent before uploading documents
- If I summarize documents immediately, that survives compression better

---

## 23. WHAT CLAUDE DOES AUTOMATICALLY

(Add these to project instructions)

- Check for HANDOFF file at start of every conversation
- Summarize uploaded documents immediately upon receipt
- Flag checkpoint moments: "This seems like a good handoff point"
- Use LOD terminology when discussing models
- Refer to this 00_Workflow doc for standards

---

## 24. HOW TO WORK TOGETHER

- Thinking partner, not just task executor
- Bring me in at any stage Ã¢â‚¬â€ messy ideas welcome
- Philosophical tangents are valuable, not wasted time
- The handoff system preserves the trail; the conversation is the exploration

---

# PART H: TEAM SYSTEM

## 25. THE TEAM

### 25.1 People

| Person | Flow | Focus |
|--------|------|-------|
| **Andrea** | Flow of people | EV charging dwell contexts, remote work infrastructure, working continuity |
| **Henna** | Flow of people | Transit ridership, psycho-comfort, thermal comfort, cultural circuits |

### 25.2 Claude Accounts

| Name | Account | Owner | Tier | Role | Special access |
|------|---------|-------|------|------|----------------|
| **Cairn** | Andrea personal | Andrea | Max | Heavy lifting, task coordination, strategic thinking | Full usage, coordinator role |
| **Lumen** | Andrea school | Andrea | Team/school | Specialized tasks | School-specific tools & resources |
| **Meridian** | Henna school | Henna | Team/school | Henna's analytical work | School-specific tools & resources |
| **Cadence** | Henna personal | Henna | Pro | Henna's heavy lifting (not yet used for studio) | — |

### 25.3 Coordination Rule

**Whoever is in the active session coordinates.** Any Claude can allocate tasks — not just Cairn. If Andrea and Henna are working with Meridian on narrative and it's natural to split tasks from there, Meridian does it. The principle is: **the Claude with the most current context allocates.**

Allocation logic (same for any Claude):

1. **Intensity** — heavy data processing and long analysis → Max/Pro accounts
2. **Access needs** — school-specific resources → school accounts
3. **Efficiency** — quick simple tasks → lowest-availability accounts (use them up wisely)
4. **Dependencies** — if Task B needs Task A's output, schedule A first on the right account

---

## 26. TEAM HANDOFFS

### 26.1 When to Create

A team handoff is needed when:
- A decision affects both Andrea and Henna's work
- One person's output becomes the other's input (data dependency)
- Tasks are split between team members
- After a joint crit or shared teacher feedback
- When task allocation changes

A team handoff is **not** needed for:
- Individual analytical work that doesn't affect the other person
- Personal workflow decisions

### 26.2 Team Handoff Template

```markdown
# TEAM HANDOFF — [DD-MM]

## Shared decisions
[Decisions that both team members need to respect]

## Task split
| Task | Assigned to | Account | Status | Deadline |
|------|-------------|---------|--------|----------|
| ... | Andrea | Cairn | In progress | ... |
| ... | Henna | Meridian | Not started | ... |

## Data dependencies
[What one person is producing that the other needs]
- Andrea → Henna: [dataset/output, expected format, when]
- Henna → Andrea: [dataset/output, expected format, when]

## Usage budget
| Account | Daily remaining | Weekly remaining | Allocated tasks |
|---------|----------------|------------------|-----------------|
| Cairn (Max) | [high/med/low] | [high/med/low] | [task list] |
| Lumen (school) | [high/med/low] | [high/med/low] | [task list] |
| Meridian (school) | [high/med/low] | [high/med/low] | [task list] |
| Cadence (Pro) | [high/med/low] | [high/med/low] | [task list] |

## Next sync point
[When do you next need to compare notes? After X is done? Before crit?]
```

### 26.3 Naming Convention

`TEAM_HANDOFF_DD-MM.md`

- One per day maximum (overwrite if updated same day)
- Goes into **both** Andrea's and Henna's project files
- Any Claude can generate it — whichever is in the active session

### 26.4 How It Flows

```
Andrea works with Cairn (heavy session)
    → Cairn flags: "this affects Henna's work"
    → Cairn generates TEAM_HANDOFF
    → Andrea drops it into Henna's project (and her own)

Henna works with Meridian
    → Meridian reads TEAM_HANDOFF, knows what Andrea decided/produced
    → Meridian does Henna's tasks
    → If something changes, Meridian generates updated TEAM_HANDOFF
    → Henna drops it back into Andrea's project

Andrea + Henna work together with Meridian (joint session)
    → Meridian coordinates directly — no need to route through Cairn
    → Meridian generates TEAM_HANDOFF with updated task split
    → Both drop it into their own projects

Andrea returns to Cairn
    → Cairn reads updated TEAM_HANDOFF
    → Loop continues
```

The individual handoffs (`HANDOFF_DD-MM_S[n].md`) still work exactly as before — they track each person's internal progress. Team handoffs only track the **shared interface** between the two workflows.

---

## 27. TASK ALLOCATION PROTOCOL

### 27.1 At the Start of a Work Block

Andrea (or Henna) tells whichever Claude they're working with:
> "Here's usage: Cairn daily [X] weekly [X], Lumen daily [X] weekly [X], Meridian daily [X] weekly [X], Cadence daily [X] weekly [X]. Here's what needs doing: [task list]. Allocate."

That Claude then:
1. Lists all pending tasks from the latest handoffs + team handoff
2. Estimates intensity per task (light / medium / heavy)
3. Checks daily limits first (can this get done today?), then weekly budget
4. Matches tasks to accounts based on usage + access needs
5. Produces an updated task split table

### 27.2 Task Intensity Guide

| Intensity | Examples | Best for |
|-----------|----------|----------|
| **Heavy** | Data enrichment pipelines, cross-reference analysis, long strategic discussions, map production | Max / Pro accounts |
| **Medium** | Dataset creation, QGIS styling, targeted analysis, drafting sections | Any account with moderate usage |
| **Light** | Quick questions, file formatting, handoff generation, small edits | Low-usage accounts (spend them wisely) |
| **Access-specific** | School resources, specific MCP tools, team-shared drives | School accounts regardless of usage |

### 27.3 Example Allocation

```
Available today: Cairn 70%, Lumen 20%, Meridian 40%, Cadence 60%
Weekly budget:   Cairn plenty, Lumen low, Meridian medium, Cadence full (unused for studio)

Tasks:
1. Enrich wifi dataset with temporal data → HEAVY → Cairn (daily budget allows it)
2. Generate point cloud sections → MEDIUM + needs school lidar → Lumen (spend remaining daily)
3. Henna's ridership temporal analysis → HEAVY → Cadence (onboard for studio work)
4. Cross-reference Andrea + Henna datasets → HEAVY → Cairn
5. Format team presentation slides → LIGHT → Meridian
6. Narrative draft for A02 → MEDIUM → Meridian (Andrea + Henna working together)
```

---

## 28. RULES FOR ALL CLAUDES

Every Claude in the team system should:

1. **Read the latest team handoff** at conversation start (alongside individual handoff)
2. **Respect task allocations** — if a task is assigned to another account, don't duplicate it
3. **Flag cross-team impacts** — "this changes something Henna/Andrea needs to know"
4. **Any Claude can coordinate** — whoever has the most current context allocates tasks. Don't wait for a specific account.
5. **Keep handoffs lean** — the system only works if the files stay small enough to actually read
6. **Use names** — always refer to Cairn, Lumen, Meridian, Cadence in handoffs so the trail is clear about who decided/produced what


---

# REVISION LOG

| Date | Version | Change |
|------|---------|--------|
| 17.02.2026 | v01 | Initial creation Ã¢â‚¬â€ LOD system, handoff template, workflow protocols |
| 17.02.2026 | v02 | Integrated comprehensive scale conventions, added output-specific considerations (color, digital, projection), restructured into parts |
| 18.02.2026 | v03 | Added Section 3.2.1 â€” Rhino MCP coordinate handling and spatial plan rule (learned from dining room modeling session) |
| 24.02.2026 | v04 | Added Part H — Team System (Andrea + Henna coordination, Cairn/Lumen/Meridian/Cadence accounts, team handoffs, task allocation protocol) |
