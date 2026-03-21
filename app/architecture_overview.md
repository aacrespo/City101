# System Architecture Overview

**Still on the Line — Relay-Lock Configurator**
Document 1 of 6 | March 2026

---

## 1. System Architecture

The configurator has six modules. Three are corridor-level (shared across all communities), two are community-specific, and one is the interface that ties them together.

```mermaid
graph TB
    subgraph INTERFACE["Interface Layer"]
        MAP[Map + Region Selector]
        COMM[Community Input]
        SLIDERS[Parameter Sliders]
        VIEWER[Output Viewer]
    end

    subgraph KNOWLEDGE["Corridor Knowledge Base"]
        direction LR
        STATIONS[(49 Stations)]
        MODAL[(Modal Diversity)]
        TEMPORAL[(Temporal Frequency)]
        BREAKS[(Break Points)]
        RIDERSHIP[(Ridership)]
        MOBILITY[(Shared Mobility)]
        REMOTE[(Remote Work)]
        EV[(EV Charging)]
    end

    subgraph RESEARCH["Community Research Engine"]
        direction TB
        CACHE[Pre-computed Communities]
        RUNTIME[Runtime Research Pipeline]
        CHAIN[24hr Chain Model]
    end

    subgraph SCORING["Scoring Engine"]
        direction TB
        CORRIDOR_CRIT[Corridor Criteria<br/>Modal Collapse 20%<br/>Gap Distance 15%<br/>Infra Readiness 15%]
        COMMUNITY_CRIT[Community Criteria<br/>Night Workers 25%<br/>Chain Criticality 25%]
        COMPOSITE[Composite Score]
    end

    subgraph PROPOSITION["Proposition Generator"]
        direction TB
        LOCK_SELECT[Lock Type Selection]
        CHAMBER_CONFIG[Chamber Configuration]
        VALIDATION[Region Validation]
    end

    subgraph OUTPUT["Output Pipeline"]
        direction LR
        SPEC[Spec Sheet<br/>JSON/PDF]
        PREVIEW[3D Preview<br/>Three.js]
        RHINO[Rhino Script<br/>.py export]
    end

    %% Data flows
    COMM -->|community name| RESEARCH
    MAP -->|region selection| SCORING
    KNOWLEDGE -->|corridor data| SCORING
    RESEARCH -->|chain model| SCORING
    CORRIDOR_CRIT --> COMPOSITE
    COMMUNITY_CRIT --> COMPOSITE
    SCORING -->|scored sites| PROPOSITION
    SLIDERS -->|weight overrides| PROPOSITION
    MAP -->|user region| VALIDATION
    PROPOSITION -->|chamber config| OUTPUT
    OUTPUT --> VIEWER

    %% Styling
    classDef ai fill:#4a2c6e,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1
    classDef deterministic fill:#1a3a2a,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1
    classDef data fill:#2a2a3a,stroke:#8a8880,stroke-width:1px,color:#e8e6e1
    classDef interface fill:#3a2a1a,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1

    class RUNTIME,CHAIN,VALIDATION ai
    class CORRIDOR_CRIT,COMMUNITY_CRIT,COMPOSITE,LOCK_SELECT,CHAMBER_CONFIG,SPEC,PREVIEW,RHINO deterministic
    class STATIONS,MODAL,TEMPORAL,BREAKS,RIDERSHIP,MOBILITY,REMOTE,EV,CACHE data
    class MAP,COMM,SLIDERS,VIEWER interface
```

**Legend**: Purple = AI-driven. Green = deterministic. Grey = static data. Brown = interface.

---

## 2. Module Descriptions

### 2.1 Corridor Knowledge Base

Static. Loaded once. Does not change per query.

| Dataset | Records | Role in Scoring |
|---------|---------|-----------------|
| 49-station corridor | 49 | Candidate site geography |
| Modal diversity | 49 | **Modal collapse severity** (20% weight) |
| Break points | 49 | **Gap distance** (15% weight) |
| Temporal frequency | 49 x 28 | Night service availability |
| Ridership | 174 | Demand validation |
| Shared mobility | 2,062 | **Infrastructure readiness** (15% weight) |
| Remote work places | 68 | Supporting infrastructure |
| EV charging | 194 | Supporting infrastructure |
| First/last trains | 49 | Dead window definition |
| Station crossref | 49 x 46 | Multi-source validation |

Source: `datasets/` directory. All verified through quality gates. Coordinate system: Swiss LV95 / EPSG:2056, converted to WGS84 for web display.

### 2.2 Community Research Engine

This is the hardest module to generalize. It answers: *What does this community's 24-hour chain look like, and where does it break?*

```mermaid
graph LR
    subgraph INPUT
        COMM_NAME[Community Name]
    end

    subgraph CACHE_CHECK["Cache Layer"]
        CHECK{Pre-computed?}
        HC_DATA[Healthcare Data<br/>Full chain model<br/>7 nodes, 5 flow types<br/>Worker counts<br/>Break points mapped]
    end

    subgraph RUNTIME_RESEARCH["Runtime Research"]
        API_QUERY[API Queries<br/>Google Places<br/>transport.opendata.ch<br/>Overpass/OSM]
        LLM_INTERPRET[LLM Interpretation<br/>Chain structure<br/>Worker patterns<br/>Break identification]
        CHAIN_BUILD[Chain Model Builder<br/>Nodes + flows<br/>Temporal pattern<br/>Breaking points]
    end

    subgraph OUTPUT_MODEL["Chain Model Output"]
        WORKERS[Night Worker Estimates]
        CRITICAL[Criticality Scores]
        BREAKS_C[Community Break Points]
    end

    COMM_NAME --> CHECK
    CHECK -->|Yes: healthcare| HC_DATA
    CHECK -->|No: any other| API_QUERY
    HC_DATA --> WORKERS
    HC_DATA --> CRITICAL
    HC_DATA --> BREAKS_C
    API_QUERY --> LLM_INTERPRET
    LLM_INTERPRET --> CHAIN_BUILD
    CHAIN_BUILD --> WORKERS
    CHAIN_BUILD --> CRITICAL
    CHAIN_BUILD --> BREAKS_C

    classDef ai fill:#4a2c6e,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1
    classDef cached fill:#2a2a3a,stroke:#8a8880,stroke-width:1px,color:#e8e6e1
    classDef output fill:#1a3a2a,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1

    class API_QUERY,LLM_INTERPRET,CHAIN_BUILD ai
    class HC_DATA,CHECK cached
    class WORKERS,CRITICAL,BREAKS_C output
```

**Honest assessment of the runtime path:**

The healthcare community took weeks of research across multiple sessions to produce a 7-node chain model with specific worker counts, flow types, and breaking points. The runtime path compresses this into minutes. Quality tradeoffs:

| Aspect | Pre-computed (healthcare) | Runtime (other communities) |
|--------|--------------------------|----------------------------|
| Worker counts | Field-validated estimates | API-derived approximations |
| Chain structure | Manually identified nodes | LLM-inferred from business data |
| Break points | Cross-referenced with transport data | Best-guess from hours + locations |
| Confidence | High | Low-to-medium |
| Time to produce | ~20 hours of research | ~30 seconds of API + LLM |

The runtime path is useful for exploration and hypothesis generation. It should not be presented with the same confidence as pre-computed results. The interface must communicate this difference.

### 2.3 Scoring Engine

Deterministic once inputs are provided. The five criteria split cleanly into two sources.

```mermaid
graph TB
    subgraph CORRIDOR_DATA["From Corridor Knowledge Base"]
        MC[Modal Collapse Severity<br/>Weight: 20%<br/>Source: modal_diversity.csv]
        GD[Gap Distance<br/>Weight: 15%<br/>Source: break_points.csv]
        IR[Infrastructure Readiness<br/>Weight: 15%<br/>Source: shared_mobility.csv + ev_charging + remote_work]
    end

    subgraph COMMUNITY_DATA["From Community Research Engine"]
        NW[Night Worker Count<br/>Weight: 25%<br/>Source: chain model]
        CC[Chain Criticality<br/>Weight: 25%<br/>Source: chain model]
    end

    MC --> NORMALIZE[Normalize 0–1]
    GD --> NORMALIZE
    IR --> NORMALIZE
    NW --> NORMALIZE
    CC --> NORMALIZE

    NORMALIZE --> WEIGHT[Apply Weights]
    WEIGHT --> RANK[Rank Candidate Sites]
    RANK --> TOP_N[Top N Propositions]

    SLIDERS[User Weight Overrides] -.->|optional| WEIGHT

    classDef corridor fill:#1a3a2a,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1
    classDef community fill:#4a2c6e,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1
    classDef engine fill:#2a2a1a,stroke:#c9a84c,stroke-width:1px,color:#e8e6e1

    class MC,GD,IR corridor
    class NW,CC community
    class NORMALIZE,WEIGHT,RANK,TOP_N,SLIDERS engine
```

**The generalization problem:** Modal collapse, gap distance, and infrastructure readiness are corridor properties. They work for any community. Night worker count and chain criticality are community properties. For healthcare, we have real numbers (300-400 night workers at Morges, 1,900-2,600 at CHUV). For bakeries, we would need to define: what counts as a "night worker" in this context? What makes one bakery's chain more "critical" than another's? The scoring framework holds, but the two community criteria need a community-specific definition layer.

### 2.4 Proposition Generator

Takes scored sites and produces chamber configurations. This is where the typology's vocabulary gets applied.

**9 Lock Types** (from the relay-lock research):

| Lock Type | Threshold | Example Site |
|-----------|-----------|--------------|
| Border Lock | Border / corridor | Geneva border zone |
| Cargo Lock | Cargo / city | Geneva North (ZIMEYSA) |
| Vertical Connector | Valley / hilltop | Nyon-Genolier |
| Temporal Lock | Last train / first train | Morges |
| Visibility Lock | Invisible / visible | Crissier-Bussigny |
| Gradient Dispatcher | Uphill / downhill | Lausanne CHUV |
| Altitude Lock | Mountain / lake | Montreux-Glion |
| Bridge Lock | Rail / off-rail | Rennaz |
| Logistics Engine | Generic threshold | Fallback type |

**Chamber configuration variables** (partially defined — needs formalization):

```
lock_type:           one of 9 types
circulation_types:   [staff, patient, cargo, emergency, public]
chamber_program:     list of spatial functions
threshold_sequence:  entry_state → chamber → exit_state
orientation:         corridor-parallel | corridor-perpendicular | vertical
scale:               LOG 200 (massing) | LOG 300 (detailed)
```

**Open question:** What is the minimal parameter set that fully defines a chamber? The existing Rhino scripts (Morges, CHUV, Rennaz) each handle site-specific geometry. Extracting a common parameter schema from these three scripts is a prerequisite for the proposition generator.

### 2.5 Output Pipeline

Three output formats from the same proposition data.

```mermaid
graph LR
    PROP[Chamber Configuration<br/>+ Site Data<br/>+ Score Breakdown] --> SPEC_GEN[Spec Sheet Generator]
    PROP --> PREVIEW_GEN[3D Preview Renderer]
    PROP --> SCRIPT_GEN[Rhino Script Generator]

    SPEC_GEN --> PDF[PDF / JSON<br/>Printable spec sheet<br/>All parameters listed<br/>Score justification]
    PREVIEW_GEN --> THREE[Three.js Scene<br/>Browser-based 3D<br/>Simplified massing<br/>Site context]
    SCRIPT_GEN --> PY[RhinoCommon .py<br/>Downloadable script<br/>LOG 200–300 geometry<br/>Layer structure per workflow]

    classDef deterministic fill:#1a3a2a,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1
    class SPEC_GEN,PREVIEW_GEN,SCRIPT_GEN,PDF,THREE,PY deterministic
```

All three outputs are deterministic template-filling operations. No AI needed here.

**Rhino integration operates in three modes:**

| Mode | Where | Requirements | Audience |
|------|-------|--------------|----------|
| Preview | Browser (Three.js) | None | Everyone |
| Export | Download .py | Rhino installed | Architects |
| MCP | Direct Rhino control | Rhino + MCP running locally | Power users / development |

The existing 3 Rhino scripts follow the `00_Workflow_v04.md` conventions: LOG 200 for massing, LOG 300 for detail, layers organized by program, Swiss LV95 coordinates. The script generator must produce scripts that conform to this same convention.

### 2.6 Interface Layer

Not a dashboard. Not a visualization. A control surface.

```
+------------------------------------------------------------------+
|  COMMUNITY INPUT          |  MAP (Leaflet / WGS84)               |
|  [________________________] |  [ 101km corridor ]                 |
|  "healthcare"             |  [ 49 station markers ]              |
|                           |  [ scored heat overlay ]             |
|  REGION SELECTOR          |  [ user click → region ]             |
|  Click map or enter name  |  [ lock nodes highlighted ]          |
+---------------------------+                                      |
|  PARAMETER PANEL          |                                      |
|  Night workers    [===|==] 25%                                   |
|  Chain criticality[===|==] 25%                                   |
|  Modal collapse   [==|===] 20%                                   |
|  Gap distance     [=|====] 15%                                   |
|  Infra readiness  [=|====] 15%                                   |
+---------------------------+--------------------------------------+
|  PROPOSITION VIEWER                                              |
|  +------------------+  +------------------+  +-----------------+ |
|  | Spec Sheet       |  | 3D Preview       |  | Rhino Export    | |
|  | Lock: Temporal   |  | [Three.js canvas] |  | [Download .py]  | |
|  | Site: Morges     |  |                  |  |                 | |
|  | Score: 0.82      |  |                  |  |                 | |
|  +------------------+  +------------------+  +-----------------+ |
+------------------------------------------------------------------+
```

The interface must communicate:
- Whether results are pre-computed (high confidence) or runtime-generated (exploratory)
- Why a region was accepted or pushed back
- What changing a weight actually changes in the proposition

---

## 3. Request Lifecycle

What happens when an architect says: "I want to apply the typology to solve healthcare's problem in the Morges region."

```mermaid
sequenceDiagram
    participant A as Architect
    participant UI as Interface
    participant CRE as Community Research
    participant KB as Knowledge Base
    participant SE as Scoring Engine
    participant PG as Proposition Generator
    participant OP as Output Pipeline

    A->>UI: Enter community: "healthcare"
    UI->>CRE: Lookup community
    CRE->>CRE: Cache hit — healthcare is pre-computed
    CRE-->>UI: Chain model loaded (7 nodes, worker counts, break points)

    A->>UI: Select region: Morges area (km 45–52)
    UI->>KB: Fetch corridor data for region
    KB-->>UI: Station data, modal, temporal, breaks

    UI->>SE: Score candidate sites in region
    SE->>SE: Apply 3 corridor criteria (from KB)
    SE->>SE: Apply 2 community criteria (from CRE)
    SE->>SE: Composite score → rank sites
    SE-->>UI: Scored site list

    UI->>PG: Region validation check
    PG->>PG: Morges scores 0.82 — region confirmed
    PG-->>UI: "Region matches breaking point analysis"

    Note over UI: Display scored overlay on map

    A->>UI: Accept top proposition
    UI->>PG: Generate chamber config for Morges
    PG->>PG: Lock type: Temporal Lock
    PG->>PG: Circulation: staff + patient + pharma
    PG->>PG: Program: night shelter + elderly mobility hub
    PG-->>UI: Chamber configuration

    UI->>OP: Generate outputs
    OP-->>UI: Spec sheet + 3D preview + Rhino script

    A->>UI: Adjust weight: increase modal collapse to 30%
    UI->>SE: Recalculate with new weights
    SE-->>UI: Updated scores (ranking may shift)
    UI->>PG: Regenerate if site changed
    PG-->>UI: Updated proposition
```

**Alternate path — region pushback:**

```mermaid
sequenceDiagram
    participant A as Architect
    participant UI as Interface
    participant SE as Scoring Engine
    participant PG as Proposition Generator

    A->>UI: Select region: Lavaux (km 70–80)
    UI->>SE: Score candidate sites in Lavaux
    SE-->>UI: Scores: all below 0.4

    UI->>PG: Region validation
    PG-->>UI: PUSHBACK

    UI->>A: "Lavaux scores low for healthcare.<br/>Reason: No hospital within 20km,<br/>low night worker count,<br/>modal options adequate.<br/>Suggested instead: Morges (0.82),<br/>Rennaz (0.78), Nyon (0.71)"

    A->>UI: Accept suggestion: Morges
    Note over UI: Continue with standard flow
```

---

## 4. AI vs. Deterministic Boundary

This is the most important diagram in the document.

```mermaid
graph LR
    subgraph AI_ZONE["AI Zone — Input Processing"]
        direction TB
        A1[Community chain research<br/>Understanding 24hr patterns]
        A2[Breaking point identification<br/>Interpreting where chains fail]
        A3[Region validation<br/>Reasoning about match quality]
        A4[Narrative generation<br/>Explaining propositions]
    end

    subgraph BOUNDARY["Handoff: Chain Model"]
        direction TB
        B1[Worker counts per site]
        B2[Criticality scores per site]
        B3[Break point locations]
        B4[Flow type definitions]
    end

    subgraph DETERMINISTIC_ZONE["Deterministic Zone — Everything Else"]
        direction TB
        D1[Scoring: 5 criteria weighted sum]
        D2[Lock type selection: highest-scoring type]
        D3[Weight adjustment: recalculation]
        D4[Spec sheet: template + data]
        D5[3D preview: parametric geometry]
        D6[Rhino script: template + parameters]
    end

    AI_ZONE --> BOUNDARY
    BOUNDARY --> DETERMINISTIC_ZONE

    classDef ai fill:#4a2c6e,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1
    classDef boundary fill:#3a3a1a,stroke:#c9a84c,stroke-width:3px,color:#e8e6e1
    classDef det fill:#1a3a2a,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1

    class A1,A2,A3,A4 ai
    class B1,B2,B3,B4 boundary
    class D1,D2,D3,D4,D5,D6 det
```

**The key insight: AI is heaviest at the input boundary.** Once a community's 24-hour chain is mapped to worker counts, criticality scores, and break point locations, everything downstream is a weighted sum, a template fill, or a parametric geometry operation.

**Consequence for midterm (March 30):** The demo does not require real-time AI. Hardcode the healthcare chain model as the pre-computed input. The entire deterministic pipeline runs without any LLM calls. Runtime community research is a post-midterm feature.

---

## 5. Tech Stack

```mermaid
graph TB
    subgraph FRONTEND["Frontend"]
        LEAFLET[Leaflet<br/>Map + corridor display<br/>WGS84 / EPSG:4326]
        THREEJS[Three.js<br/>3D chamber preview<br/>Browser-based]
        SVELTE[Svelte or Vanilla JS<br/>Parameter panel<br/>Spec sheet viewer]
    end

    subgraph BACKEND["Backend / Logic"]
        SCORING_JS[Scoring Engine<br/>JS or Python<br/>Pure functions, no state]
        PROP_JS[Proposition Generator<br/>JS or Python<br/>Typology rules + templates]
    end

    subgraph DATA_LAYER["Data Layer"]
        STATIC_JSON[Static JSON<br/>Corridor datasets<br/>Pre-computed community models]
        TEMPLATES[Templates<br/>Spec sheet format<br/>Rhino script skeletons]
    end

    subgraph AI_LAYER["AI Layer (post-midterm)"]
        LLM[LLM API<br/>Community research<br/>Narrative generation]
        APIS[External APIs<br/>Google Places<br/>transport.opendata.ch<br/>Overpass]
    end

    subgraph RHINO_LAYER["Rhino Layer (local)"]
        EXPORT[Script Export<br/>.py download<br/>RhinoCommon compatible]
        MCP[Rhino MCP<br/>Direct manipulation<br/>Local only]
    end

    LEAFLET --> SCORING_JS
    SVELTE --> SCORING_JS
    SCORING_JS --> PROP_JS
    PROP_JS --> THREEJS
    PROP_JS --> EXPORT
    STATIC_JSON --> SCORING_JS
    TEMPLATES --> PROP_JS
    TEMPLATES --> EXPORT
    LLM --> STATIC_JSON
    APIS --> LLM

    classDef frontend fill:#3a2a1a,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1
    classDef backend fill:#1a3a2a,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1
    classDef data fill:#2a2a3a,stroke:#8a8880,stroke-width:1px,color:#e8e6e1
    classDef ai fill:#4a2c6e,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1
    classDef rhino fill:#2a3a3a,stroke:#c9a84c,stroke-width:2px,color:#e8e6e1

    class LEAFLET,THREEJS,SVELTE frontend
    class SCORING_JS,PROP_JS backend
    class STATIC_JSON,TEMPLATES data
    class LLM,APIS ai
    class EXPORT,MCP rhino
```

**Technology choices are not locked.** The critical constraint is that the deterministic pipeline must work as a standalone static site (no server required) for the midterm demo. The AI layer and Rhino MCP are additive capabilities.

**Candidate stack for midterm:**
- Single HTML page with embedded JS (like the existing prototypology explorer)
- Corridor data as static JSON (converted from CSVs in `datasets/`)
- Healthcare chain model as static JSON (from `prototypology_content.json`)
- Leaflet for map, Three.js for 3D preview, vanilla JS for scoring + sliders
- No backend, no API calls, no build step

---

## 6. Critical Issues

### 6.1 Community Criteria Generalization

The scoring framework's 3 corridor criteria (modal collapse, gap distance, infrastructure readiness) transfer to any community because they describe the corridor, not the community. The 2 community criteria (night worker count, chain criticality) require community-specific definitions.

For healthcare, "night worker count" means staff on shift between 00:30-05:00. For bakeries, it might mean bakers starting at 03:00. For logistics, it might mean warehouse workers on rotating shifts. The *metric shape* is similar (how many people are stranded during the dead window) but the *data source and interpretation* differ completely.

**Proposed abstraction:** Define the community criteria interface as:
- `stranded_worker_count(site, time_window) -> int` — how many community members are cut off from transport at this site during this window
- `chain_break_severity(site) -> float 0-1` — how badly does losing this site's connectivity damage the community's chain

Any community research (pre-computed or runtime) must produce functions matching this interface. The scoring engine does not need to know whether the community is healthcare or bakeries — it receives the same shaped inputs.

### 6.2 Runtime Research Quality

Compressing weeks of research into a runtime query will produce lower-quality results. Strategies to manage this:

1. **Confidence indicator**: Every runtime result carries a confidence score. Display prominently.
2. **Source transparency**: Show the architect what data was found and what was estimated.
3. **Progressive refinement**: Allow saving and manually correcting runtime research results, building the cache over time.
4. **Guardrails**: If the runtime research finds fewer than N data points, say so. Do not hallucinate precision.

### 6.3 Missing Data: Cadastre

The system proposes sites but does not currently know where you can and cannot build. Cadastre data (land use zones, building regulations, protected areas) from the Canton of Vaud's geoportal would add a boolean filter: is this site even buildable?

Without cadastre data, the system proposes sites based on need and infrastructure, but an architect must manually verify buildability. Flag this in every spec sheet.

### 6.4 Chamber Parameter Formalization

The three existing Rhino scripts (Morges, CHUV, Rennaz) each encode site-specific logic. To generate scripts for arbitrary sites, we need a common parameter schema. Extracting this requires:

1. Audit the 3 scripts for shared variables vs. site-specific overrides
2. Define the minimal parameter set: footprint, height, lock orientation, circulation count, program areas
3. Build a template script that accepts parameters and generates geometry
4. Test on a 4th site (not one of the originals) to validate generalization

This is a prerequisite for the proposition generator's Rhino export. For midterm, the three existing scripts can be offered as-is for their respective sites.

### 6.5 The 9-Node vs. N-Node Question

The current research identifies 9 lock types mapped to specific sites along the healthcare chain. When a different community is analyzed, the lock types may apply but the sites will differ. The system must support:
- Fixed vocabulary of lock types (the 9 types are the typology)
- Variable number of nodes per community (healthcare has 7 populated nodes, others may have 3 or 12)
- Variable site assignments (a bakery chain might need a Temporal Lock at Vevey, not Morges)

The 9 lock types are the contribution. The specific sites are instances.

---

## 7. Phasing

```mermaid
gantt
    title Implementation Phases
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section Midterm (Mar 30)
    Static corridor data as JSON          :done, m1, 2026-03-18, 3d
    Healthcare chain model hardcoded      :done, m2, 2026-03-18, 3d
    Scoring engine (JS, pure functions)   :active, m3, 2026-03-20, 4d
    Map interface with scored overlay     :m4, 2026-03-22, 4d
    Parameter sliders with live rescore   :m5, 2026-03-24, 3d
    Spec sheet generation                 :m6, 2026-03-25, 3d
    3D preview (simplified massing)       :m7, 2026-03-26, 4d

    section Post-Midterm
    Runtime community research pipeline   :p1, 2026-04-01, 14d
    Rhino script template generator       :p2, 2026-04-01, 10d
    Region pushback logic                 :p3, 2026-04-07, 7d
    Cadastre data integration             :p4, 2026-04-14, 7d
    Confidence indicators for runtime     :p5, 2026-04-14, 5d
    MCP mode (direct Rhino control)       :p6, 2026-04-21, 7d
```

**Midterm deliverable:** A static-site configurator that takes healthcare as the community, shows scored sites on the corridor map, lets the architect adjust weights, and generates a spec sheet + simplified 3D preview for the top proposition. No server. No AI calls. Deterministic pipeline only.

**Post-midterm:** Add runtime community research, Rhino script generation, region pushback, and cadastre filtering. Each feature is additive — the deterministic core does not change.
