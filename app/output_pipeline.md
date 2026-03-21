# Output Pipeline
## Architecture Document 4/6 — "Still on the Line"

How the system generates its three outputs — spec sheet, 3D preview, and Rhino script — from a single shared data model.

---

## 1. The Proposition Data Model

Every output is rendered from the same `Proposition` object. This is the single source of truth. If the spec sheet says one thing and the 3D preview shows another, the data model is wrong — not the renderer.

```json
{
  "proposition_id": "prop_morges_healthcare_2026-03-28T14:22",
  "version": 1,

  "site": {
    "name": "Morges",
    "node_id": 3,
    "km": 48,
    "coords_lv95": { "e": 2527800, "n": 1151900 },
    "coords_wgs84": { "lat": 46.5117, "lon": 6.4985 },
    "commune": "Morges",
    "canton": "VD",
    "elevation_m": 376
  },

  "lock": {
    "type": "temporal",
    "name": "Last Train / First Train",
    "state_a": { "label": "Last train", "time": "00:30", "description": "Final departure, platform empties" },
    "state_b": { "label": "First train", "time": "05:00", "description": "First arrival, platform reactivates" },
    "threshold_sequence": ["approach", "enter", "dwell", "transition", "exit"],
    "dead_window": { "start": "01:30", "end": "03:30" }
  },

  "scores": {
    "night_worker_count":       { "raw": 0.82, "weight": 0.25, "weighted": 0.205 },
    "healthcare_chain_criticality": { "raw": 0.75, "weight": 0.20, "weighted": 0.150 },
    "modal_collapse_severity":  { "raw": 0.90, "weight": 0.25, "weighted": 0.225 },
    "gap_distance":             { "raw": 0.60, "weight": 0.15, "weighted": 0.090 },
    "infrastructure_readiness": { "raw": 0.70, "weight": 0.15, "weighted": 0.105 },
    "total": 0.775
  },

  "chamber": {
    "footprint": { "width_m": 34, "depth_m": 10, "area_m2": 340 },
    "height": { "levels": 2, "floor_to_floor_m": 3.0, "total_m": 8.0 },
    "program": [
      { "type": "rest", "area_pct": 25, "description": "Night worker rest area with reclinable seating" },
      { "type": "dispatch", "area_pct": 15, "description": "Shift coordination and dispatch desk" },
      { "type": "pharmaceutical", "area_pct": 10, "description": "Secure cold-chain storage for lab samples and medications" },
      { "type": "information", "area_pct": 10, "description": "Transport status displays, schedule boards" },
      { "type": "kitchen", "area_pct": 10, "description": "Microwave, hot water, vending — night meal support" },
      { "type": "viewing_gallery", "area_pct": 10, "description": "Glazed east face for dawn observation" },
      { "type": "cargo_hold", "area_pct": 10, "description": "Temporary storage for logistics parcels in transit" },
      { "type": "sanitary", "area_pct": 5, "description": "Restrooms, shower for long-shift workers" },
      { "type": "circulation", "area_pct": 5, "description": "Corridors, stairs, ramps" }
    ],
    "circulations": [
      { "type": "staff", "path": "main_entrance_to_rest_and_dispatch", "priority": 1 },
      { "type": "patient", "path": "accessible_entrance_to_viewing_gallery", "priority": 2 },
      { "type": "cargo", "path": "service_entrance_to_cargo_hold_to_dispatch", "priority": 3 },
      { "type": "home_care", "path": "quick_stop_entrance_to_pharmaceutical_to_exit", "priority": 1 }
    ],
    "orientation": { "primary_axis": "east-west", "entry_direction": "west" },
    "materiality": { "primary": "concrete", "secondary": "steel", "transparency_pct": 35 }
  },

  "context": {
    "terrain": { "elevation_m": 376, "slope_pct": 2.1, "aspect_deg": 170 },
    "infrastructure": {
      "rail_distance_m": 45,
      "bus_stops": ["Morges gare", "Morges centre"],
      "shared_mobility": ["PubliBike Morges gare"]
    },
    "buildings": {
      "adjacent_footprints": [
        { "id": "EGID_12345", "use": "hospital", "height_m": 18, "distance_m": 60 }
      ]
    },
    "cadastre": { "buildable_area_m2": 800, "constraints": ["zone_utilite_publique", "proximity_voie_ferree"] }
  },

  "parameters": {
    "scoring_weights": {
      "night_worker_count": 0.25,
      "healthcare_chain_criticality": 0.20,
      "modal_collapse_severity": 0.25,
      "gap_distance": 0.15,
      "infrastructure_readiness": 0.15
    },
    "design_weights": {
      "visibility_vs_discretion": 0.6,
      "carbon_vs_comfort": 0.4,
      "permanence_vs_lightness": 0.5,
      "enclosure_vs_openness": 0.65
    }
  }
}
```

---

## 2. Pipeline Overview

```mermaid
flowchart TB
    subgraph INPUT["Input Layer"]
        DL["Decision Logic<br/>(Architecture Doc 3)"]
        UW["User Weight<br/>Adjustments"]
    end

    DL --> PROP
    UW --> PROP

    PROP["Proposition<br/>Data Model<br/>(JSON)"]

    PROP --> R1["Spec Sheet<br/>Renderer"]
    PROP --> R2["3D Preview<br/>Renderer"]
    PROP --> R3["Rhino Script<br/>Generator"]

    R1 --> O1["PDF / HTML<br/>Technical Document"]
    R2 --> O2["WebGL Scene<br/>in Browser"]
    R3 --> O3["Downloadable<br/>.py Script"]

    style PROP fill:#2d2d2d,stroke:#ff6b35,stroke-width:3px,color:#fff
    style O1 fill:#1a3a1a,stroke:#66bb6a,color:#fff
    style O2 fill:#1a2a3a,stroke:#42a5f5,color:#fff
    style O3 fill:#3a2a1a,stroke:#ffa726,color:#fff
```

When the user adjusts a weight slider, the Proposition is recomputed by the Decision Logic module, and all three renderers consume the updated object. The renderers are stateless — they transform data into output, nothing more.

---

## 3. Output 1: Spec Sheet

### What it contains

```mermaid
flowchart LR
    subgraph SPEC["Spec Sheet Structure"]
        direction TB
        S1["Header<br/>site name, km, coords,<br/>commune, canton"]
        S2["Lock Profile<br/>type, two states,<br/>threshold sequence,<br/>dead window"]
        S3["Scoring Breakdown<br/>5 criteria × raw × weight<br/>= weighted score, total"]
        S4["Chamber Program<br/>~9 program elements<br/>with area percentages"]
        S5["Circulations<br/>staff / patient /<br/>cargo / home care"]
        S6["Metrics<br/>affected population,<br/>gap distance, modal count<br/>day vs night"]
        S7["Fixed Constraints<br/>terrain, infrastructure,<br/>cadastre, adjacent buildings"]
        S8["Flexible Parameters<br/>scoring weights,<br/>design weights"]

        S1 --- S2 --- S3 --- S4 --- S5 --- S6 --- S7 --- S8
    end
```

### Generation pipeline

```mermaid
flowchart LR
    PROP["Proposition<br/>JSON"] --> TPL["Jinja2<br/>Template"]
    TPL --> HTML["Rendered<br/>HTML"]
    HTML --> PDF["PDF Export<br/>(Puppeteer / WeasyPrint)"]

    PROP --> JSON_OUT["Raw JSON<br/>Download"]

    style PROP fill:#2d2d2d,stroke:#ff6b35,color:#fff
```

The spec sheet is the simplest renderer. It is a template that maps Proposition fields to labeled sections. Two output formats:

- **JSON** — machine-readable, used by the other two renderers and by any downstream tool. This is the canonical format.
- **HTML/PDF** — human-readable, styled with the project design system (see `design_system/SPEC.md`). Generated via Jinja2 template with CSS print styles. PDF conversion via headless Chromium (Puppeteer) or WeasyPrint.

The HTML version includes a radar chart of the 5 scoring criteria (using Chart.js or D3) and a stacked bar for program area distribution.

### Spec sheet data mapping

| Section | Proposition fields | Format |
|---------|-------------------|--------|
| Header | `site.*` | Name, km marker, dual coordinates |
| Lock Profile | `lock.*` | Lock type badge, state A/B labels, threshold diagram |
| Scoring | `scores.*` | Table: criterion, raw, weight, weighted. Radar chart. |
| Program | `chamber.program[]` | Stacked horizontal bar + table |
| Circulations | `chamber.circulations[]` | Diagram showing 4 paths through chamber plan |
| Metrics | `lock.dead_window`, `context.infrastructure.*`, `scores.night_worker_count.raw` | Key numbers in large type |
| Constraints | `context.terrain`, `context.cadastre`, `context.buildings` | Map thumbnail + constraint list |
| Parameters | `parameters.*` | Slider positions shown as values |

---

## 4. Output 2: 3D Preview

### Architecture

```mermaid
flowchart TB
    subgraph DATA_SOURCES["Data Sources"]
        DEM["data.geo.admin.ch<br/>swissALTI3D<br/>2m DEM tiles"]
        BLD["data.geo.admin.ch<br/>swissBUILDINGS3D<br/>LOD2 footprints"]
        INFRA["OpenStreetMap<br/>rail lines, roads"]
        PROP2["Proposition<br/>JSON"]
    end

    subgraph TRANSFORM["Coordinate Transform"]
        LV95["LV95 coords<br/>EPSG:2056"]
        LOCAL["Local Three.js<br/>coords (origin = site center)"]
        LV95 --> LOCAL
    end

    DEM --> TERRAIN_GEO["Terrain Mesh<br/>BufferGeometry from DEM grid"]
    BLD --> BUILDING_GEO["Building Volumes<br/>Extruded footprints"]
    INFRA --> INFRA_GEO["Infrastructure Lines<br/>Rail + road as 3D paths"]
    PROP2 --> CHAMBER_GEO["Chamber Volume<br/>Parametric box/volumes"]

    TERRAIN_GEO --> SCENE
    BUILDING_GEO --> SCENE
    INFRA_GEO --> SCENE
    CHAMBER_GEO --> SCENE

    TRANSFORM -.-> TERRAIN_GEO
    TRANSFORM -.-> BUILDING_GEO
    TRANSFORM -.-> INFRA_GEO

    SCENE["Three.js Scene"] --> RENDER["WebGL Canvas<br/>orbit / zoom / toggle layers"]

    style PROP2 fill:#2d2d2d,stroke:#ff6b35,color:#fff
    style SCENE fill:#1a2a3a,stroke:#42a5f5,color:#fff
```

### Terrain pipeline

1. **Fetch**: Request DEM tiles from `api3.geo.admin.ch/rest/services/height` (swissALTI3D, 2m resolution). Bounding box = site center +/- 500m. Returns elevation grid.
2. **Parse**: Convert CSV/JSON elevation grid to a `Float32Array` of vertex positions.
3. **Mesh**: Create `THREE.PlaneBufferGeometry` with the correct vertex count, apply elevation values to Y coordinates.
4. **Material**: Hypsometric tinting (elevation-based color ramp) or neutral grey with contour-line texture.

### Building pipeline

1. **Fetch**: Query swissBUILDINGS3D via WFS from `api3.geo.admin.ch` — returns 2.5D footprints with roof heights.
2. **Filter**: Only buildings within 300m radius of site center.
3. **Extrude**: For each footprint polygon, create `THREE.ExtrudeGeometry` with height from the `DACH_MAX` (max roof height) attribute.
4. **Material**: Uniform light grey, semi-transparent. Adjacent buildings from `Proposition.context.buildings` get highlighted.

### Chamber generation (from Proposition)

```mermaid
flowchart LR
    subgraph CHAMBER_PARAMS["Proposition.chamber"]
        FP["footprint<br/>width: 34m<br/>depth: 10m"]
        HT["height<br/>levels: 2<br/>total: 8m"]
        OR["orientation<br/>axis: E-W<br/>entry: west"]
        PR["program[]<br/>rest, dispatch,<br/>pharma, ..."]
    end

    FP --> ENVELOPE["Main Envelope<br/>THREE.BoxGeometry<br/>34 × 10 × 8"]
    HT --> ENVELOPE
    OR --> ROTATE["Rotate to<br/>primary axis"]
    PR --> ZONES["Color-coded<br/>program zones<br/>(subdivide box)"]

    ENVELOPE --> ROTATE --> PLACE["Place at site<br/>elevation from DEM"]
    ZONES --> PLACE
    PLACE --> MESH["Chamber Mesh<br/>Group"]

    style MESH fill:#ff6b35,stroke:#fff,color:#fff
```

The chamber is NOT rendered as detailed architecture. It is a massing volume — a colored box subdivided into program zones. This matches the LOG 200-300 level of the existing Rhino scripts: defined volumes, not detailed construction.

### Lock state visualization

The 3D preview should communicate the lock's two states. Approach by lock type:

| Lock type | State A visualization | State B visualization |
|-----------|----------------------|----------------------|
| Temporal (Morges) | Dark scene, warm interior light, "night chamber" highlighted | Dawn light from east, "dawn chamber" highlighted |
| Gradient (CHUV) | Camera at bottom of slope, looking up | Camera at top, looking down — same volume, different perspective |
| Bridge (Rennaz) | Highlight station end, path fades toward hospital | Highlight hospital end, path fades toward station |
| Altitude | Valley-level camera with upward view | Hilltop camera with downward view |
| Border | Camera on border side | Camera on corridor side |

Implementation: toggle button switches scene lighting, camera position, and material emphasis. No geometry change — the same chamber is read differently.

### Interaction model

- **OrbitControls**: click-drag to rotate, scroll to zoom, right-drag to pan.
- **Layer toggles**: terrain on/off, buildings on/off, infrastructure on/off, chamber on/off.
- **State toggle**: switch between State A and State B visualization.
- **Info overlay**: hover on chamber zones to see program labels and areas from Proposition.

### Performance constraints

- Terrain tile radius: 500m from site center (1000m square). At 2m resolution = 250,000 vertices. Acceptable for modern GPUs but should use LOD decimation beyond 300m.
- Buildings: cap at 200 buildings within the 300m radius. LOD: beyond 200m, render as simple extruded rectangles ignoring roof detail.
- Target: 60fps on a 2020-era laptop with integrated graphics.

### Coordinate transform: LV95 to Three.js

```
three_x = (east_lv95 - site_center_east)
three_z = (north_lv95 - site_center_north) * -1   // Three.js Z is south
three_y = elevation - site_center_elevation         // Y is up in Three.js
```

All geometry is positioned relative to the site center (origin = `Proposition.site.coords_lv95`). This keeps coordinate values small and avoids floating-point precision issues.

### Alternative: MapLibre GL JS for context view

The prototypology explorer already uses Leaflet for 2D mapping. A dual-view approach may be more practical:

```mermaid
flowchart LR
    subgraph CONTEXT_VIEW["Context View (MapLibre GL JS)"]
        MAP["2D/3D map<br/>terrain hillshade<br/>building footprints<br/>corridor overlay"]
    end

    subgraph SITE_VIEW["Site View (Three.js)"]
        SCENE2["Focused 3D scene<br/>chamber + terrain<br/>+ buildings"]
    end

    MAP -- "click site marker" --> SCENE2
    SCENE2 -- "back to map" --> MAP

    style MAP fill:#2a3a2a,stroke:#66bb6a,color:#fff
    style SCENE2 fill:#1a2a3a,stroke:#42a5f5,color:#fff
```

MapLibre GL JS handles the corridor-scale view with terrain hillshading and 3D building extrusion built in. Three.js handles the site-scale focused view with the parametric chamber. This avoids rebuilding map infrastructure in Three.js.

---

## 5. Output 3: Rhino Script

### What exists today

Three working scripts at LOG 200-300:

| Script | Lock type | File | Key geometry |
|--------|-----------|------|-------------|
| Lock 03 Morges | Temporal | `lock_03_morges_temporal.py` | Night chamber (15m) + Gate (4m) + Dawn chamber (15m). Two levels. Columns at 5m grid. Dawn window, west entrance, gate openings. |
| Lock 05 CHUV | Gradient | `lock_05_chuv_gradient_v2.py` | Four stepping levels following 15% grade. Central atrium void. Ramps along east edge. 20m wide x 34m deep. |
| Lock 07 Rennaz | Bridge | `lock_07_rennaz_bridge_v2.py` | 90m linear span. Station platform (south), elevated walkway (fast/slow lanes), hospital ramp (north). V-columns at 12m bays. |

All three scripts share the same structure:
1. Helper function (`box()` for creating boxes from min/max corners)
2. Layer setup (volumes, structure, openings, circulation, floor plates — each with a color)
3. Volume creation (main envelopes)
4. Structure (columns, slabs)
5. Openings (glazing, entrances, voids)
6. Circulation (paths, ramps, stairs)

All three use hardcoded dimensions. The parametric version must replace these with variables drawn from the Proposition.

### Parametric generation pipeline

```mermaid
flowchart TB
    PROP3["Proposition<br/>JSON"] --> EXTRACT["Extract<br/>Parameters"]

    EXTRACT --> PARAMS["Parameter Block<br/>width, depth, levels,<br/>floor_to_floor, program_zones,<br/>circulations, orientation,<br/>terrain_profile"]

    PARAMS --> TEMPLATE["Script Template<br/>(Jinja2)"]

    subgraph TEMPLATES["Template Library"]
        T1["temporal_lock.py.j2"]
        T2["gradient_lock.py.j2"]
        T3["bridge_lock.py.j2"]
        T4["altitude_lock.py.j2"]
        T5["border_lock.py.j2"]
    end

    TEMPLATE --> SELECT{"Select template<br/>by lock.type"}
    T1 & T2 & T3 & T4 & T5 --> SELECT

    SELECT --> RENDER_PY["Rendered .py<br/>Script"]

    RENDER_PY --> VALIDATE["Syntax Check<br/>(ast.parse)"]
    VALIDATE --> DOWNLOAD[".py Download<br/>for Architect"]

    style PROP3 fill:#2d2d2d,stroke:#ff6b35,color:#fff
    style DOWNLOAD fill:#3a2a1a,stroke:#ffa726,color:#fff
```

### Template approach

Each lock type has a Jinja2 template (`.py.j2`) that contains the full RhinoCommon script with parameter placeholders. Example structure for the temporal lock:

```python
# --- GENERATED SCRIPT — do not hand-edit ---
# Proposition: {{ proposition_id }}
# Site: {{ site.name }} (km {{ site.km }})
# Lock: {{ lock.type }} — {{ lock.name }}
# Generated: {{ timestamp }}

import rhinoscriptsyntax as rs

# -------------------------------------------------------
# PARAMETERS (from Proposition)
# -------------------------------------------------------
SITE_NAME = "{{ site.name }}"
LOCK_TYPE = "{{ lock.type }}"

# Chamber dimensions
WIDTH = {{ chamber.footprint.width_m }}      # total X extent
DEPTH = {{ chamber.footprint.depth_m }}      # total Y extent
LEVELS = {{ chamber.height.levels }}
FLOOR_TO_FLOOR = {{ chamber.height.floor_to_floor_m }}
TOTAL_HEIGHT = {{ chamber.height.total_m }}

# Program zones
PROGRAM = [
{% for p in chamber.program %}
    {"type": "{{ p.type }}", "area_pct": {{ p.area_pct }}},
{% endfor %}
]

# Orientation
PRIMARY_AXIS = "{{ chamber.orientation.primary_axis }}"
ENTRY_DIR = "{{ chamber.orientation.entry_direction }}"

# Terrain
SITE_ELEVATION = {{ context.terrain.elevation_m }}
SLOPE_PCT = {{ context.terrain.slope_pct }}

# ... (geometry generation functions follow, using these variables)
```

### Parameter-to-geometry mapping

```mermaid
flowchart LR
    subgraph PARAMS2["Proposition Parameters"]
        P1["footprint.width"]
        P2["footprint.depth"]
        P3["height.levels"]
        P4["height.floor_to_floor"]
        P5["program[]"]
        P6["circulations[]"]
        P7["orientation"]
        P8["context.terrain"]
    end

    subgraph GEOMETRY["RhinoCommon Geometry"]
        G1["rs.AddBox<br/>Main envelope(s)"]
        G2["rs.AddBox<br/>Floor slabs<br/>(per level)"]
        G3["rs.AddBox<br/>Columns<br/>(5m grid within footprint)"]
        G4["rs.AddSrfPt<br/>Openings cut<br/>from envelope"]
        G5["rs.AddBox<br/>Program zone<br/>volumes"]
        G6["rs.AddLine / AddCurve<br/>Circulation paths"]
        G7["Rotation transform<br/>about Z axis"]
        G8["Terrain surface<br/>simplified ground plane<br/>with slope"]
    end

    P1 & P2 --> G1
    P3 & P4 --> G2
    P1 & P2 --> G3
    P5 --> G5
    P6 --> G6
    P7 --> G7
    P8 --> G8
    P1 & P4 --> G4
```

### What the generated script produces in Rhino

The script creates geometry on named layers, matching the existing convention:

| Layer | Content | Source parameters |
|-------|---------|-------------------|
| `Lock_XX::Volumes` | Main chamber envelope(s) | `footprint.*`, `height.*` |
| `Lock_XX::Structure` | Columns at 5m grid, floor slabs per level | `footprint.*`, `height.levels`, `height.floor_to_floor` |
| `Lock_XX::Openings` | Glazed faces, entrances, voids | `chamber.orientation`, `lock.type`-specific rules |
| `Lock_XX::Circulation` | Path lines for each circulation type | `chamber.circulations[]` |
| `Lock_XX::FloorPlates` | Horizontal slabs at each level | `height.levels`, `height.floor_to_floor` |
| `Lock_XX::Context` | Simplified terrain plane, adjacent building boxes, rail/road lines | `context.*` |

The `XX` in `Lock_XX` is the node ID from `Proposition.site.node_id`.

### From hardcoded to parametric: what changes

| Aspect | Current (3 scripts) | Parametric (template) |
|--------|---------------------|----------------------|
| Dimensions | Hardcoded numbers in `box()` calls | Variables from parameter block |
| Lock type | Implicit in script structure | Template selection by `lock.type` |
| Program zones | Not represented (only volumes) | Subdivided volumes colored by type |
| Circulations | Implicit in openings | Explicit path lines on circulation layer |
| Context | None | Terrain plane + adjacent building boxes from Proposition |
| Site coords | Origin = (0,0,0), architect places manually | Origin = (0,0,0) with metadata header showing real coords |
| Layers | Per-script naming | Consistent `Lock_{node_id}::` prefix |

### Stretch goal: Grasshopper definition

A `.gh` Grasshopper definition would allow architects to interactively adjust parameters post-generation. This requires serializing the Proposition parameters as Grasshopper number sliders and text panels, connected to geometry generation components. This is post-midterm scope.

---

## 6. Render Comparison

What each output shows and at what level of detail.

```mermaid
flowchart TB
    subgraph DETAIL["Level of Detail"]
        direction LR
        LOD_DATA["DATA<br/>numbers, scores,<br/>constraints, program"]
        LOD_MASS["MASSING<br/>volumes, placement,<br/>terrain context"]
        LOD_GEOM["GEOMETRY<br/>structure, openings,<br/>circulations, slabs"]
    end

    LOD_DATA --> SPEC_OUT["Spec Sheet<br/>JSON + PDF/HTML"]
    LOD_MASS --> PREVIEW_OUT["3D Preview<br/>WebGL in browser"]
    LOD_GEOM --> RHINO_OUT["Rhino Script<br/>.py for RhinoCommon"]

    style LOD_DATA fill:#1a3a1a,stroke:#66bb6a,color:#fff
    style LOD_MASS fill:#1a2a3a,stroke:#42a5f5,color:#fff
    style LOD_GEOM fill:#3a2a1a,stroke:#ffa726,color:#fff
```

| Dimension | Spec Sheet | 3D Preview | Rhino Script |
|-----------|-----------|------------|-------------|
| **What you see** | Numbers, tables, charts | Colored volumes in terrain | Layered geometry with structure |
| **Level of detail** | Full data — every field in the Proposition | Massing volumes, approximate context | LOG 200-300: volumes, columns, slabs, openings |
| **Interaction** | Read, download | Orbit, zoom, toggle layers, switch states | Open in Rhino, modify, extend |
| **Technology** | Jinja2 + HTML/CSS + Chart.js | Three.js (site) + MapLibre GL (context) | Python + rhinoscriptsyntax + Rhino.Geometry |
| **Generation time** | < 1 second | 2-5 seconds (terrain fetch + render) | < 1 second (template render) |
| **File size** | ~50KB HTML, ~5KB JSON | N/A (rendered in browser) | ~15-30KB .py |
| **Audience** | Planner, reviewer, documentation | Client, public presentation, quick check | Architect doing design development |
| **Editability** | None (read-only output) | None (view-only) | Full — it is source code |

---

## 7. Pipeline Sequence Diagram

How the three outputs are generated in response to a user action.

```mermaid
sequenceDiagram
    actor User
    participant UI as Interface
    participant DL as Decision Logic
    participant PM as Proposition Model
    participant SR as Spec Renderer
    participant PR as Preview Renderer
    participant RG as Script Generator

    User->>UI: Adjust weight slider
    UI->>DL: New weights
    DL->>PM: Recompute proposition
    PM-->>DL: Updated Proposition JSON

    par Generate all outputs
        DL->>SR: Proposition JSON
        SR-->>UI: Updated spec sheet (HTML)

        DL->>PR: Proposition JSON
        PR-->>UI: Updated 3D scene

        DL->>RG: Proposition JSON
        RG-->>UI: Script ready for download
    end

    User->>UI: Click "Download Rhino Script"
    UI->>RG: Trigger download
    RG-->>User: lock_03_morges_temporal.py
```

---

## 8. Data Format Boundaries

Where each format lives in the pipeline.

```mermaid
flowchart LR
    subgraph FORMATS["Data Formats"]
        JSON_F["JSON<br/>Proposition model<br/>API responses<br/>config files"]
        HTML_F["HTML/CSS<br/>Spec sheet<br/>Print stylesheet"]
        WEBGL_F["WebGL / GLSL<br/>3D scene<br/>shaders"]
        PY_F["Python<br/>Rhino script<br/>RhinoCommon API"]
        GEO_F["GeoJSON<br/>Building footprints<br/>infrastructure lines"]
        DEM_F["XYZ / GeoTIFF<br/>Terrain elevation<br/>from swissALTI3D"]
    end

    JSON_F --> HTML_F
    JSON_F --> WEBGL_F
    JSON_F --> PY_F
    GEO_F --> WEBGL_F
    DEM_F --> WEBGL_F

    style JSON_F fill:#2d2d2d,stroke:#ff6b35,stroke-width:3px,color:#fff
```

JSON is the lingua franca. Every renderer reads the Proposition as JSON. Terrain and building data arrive as GeoJSON or XYZ grids and are consumed only by the 3D preview renderer. The Rhino script is pure Python — no runtime data fetching, all parameters baked in at generation time.

---

## 9. Midterm vs Post-Midterm Scope

### Midterm (March 30)

| Output | Scope | Effort |
|--------|-------|--------|
| Spec sheet | Full — template + JSON + HTML rendering. All fields populated for healthcare community. | Low |
| 3D preview | Simplified — 2D MapLibre map with extruded chamber box overlay. No terrain mesh, no building volumes. Proof of concept only. | Medium |
| Rhino script | One parametric template (temporal lock). Demonstrate that changing Proposition parameters changes the generated script. Other lock types remain hardcoded. | Low |

### Post-Midterm

| Output | Scope | Effort |
|--------|-------|--------|
| Spec sheet | Add radar chart, print CSS, PDF export. | Low |
| 3D preview | Full Three.js site view with terrain mesh from DEM, building extrusions, lock state toggle. MapLibre for context. | High |
| Rhino script | Templates for all 5 lock types. Context layer (terrain, buildings). Grasshopper definition export (stretch). | Medium |

---

## 10. Open Technical Questions

These require decisions before implementation. Cross-reference with Architecture Doc 6 (Open Questions).

1. **3D preview vs prototypology explorer**: Should the 3D preview be embedded in the same page as the prototypology explorer map, or a separate full-screen view? Embedded keeps context; separate gives more screen space for the 3D scene.

2. **Terrain data caching**: DEM tiles are static. Should they be pre-fetched for all 9 nodes and bundled, or fetched on demand? Pre-fetching adds ~50MB to the deployment but eliminates API latency.

3. **Rhino script validation**: The generated `.py` passes `ast.parse()`, but does it run correctly in Rhino? Need a testing pipeline — either Rhino MCP automated execution or manual spot checks per template.

4. **Chamber subdivision logic**: How are program zones spatially arranged within the chamber footprint? The Proposition lists area percentages, but the spatial layout (which zone is where) needs rules per lock type. This is architectural design work, not engineering.

5. **24hr usage video**: Listed in the brain dump as an output type. This would require Blender rendering driven by a time-varying version of the Proposition (activity levels by hour). Classified as stretch goal — not part of the pipeline for now.
