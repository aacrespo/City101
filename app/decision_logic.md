# Decision Logic

**Architecture Document 3 of 6** — Still on the Line
How the system decides which lock type fits, how scoring works, how user adjustments modify propositions.

---

## 1. Decision Tree: User Input to Lock Type Assignment

The full path from a user selecting a community to receiving a proposed lock network.

```mermaid
flowchart TD
    A[User selects community] --> B[AI research engine analyzes community]
    B --> C{Community data sufficient?}
    C -->|No| D[Request additional input from user]
    D --> B
    C -->|Yes| E[Extract breaking points along corridor]

    E --> F[Identify candidate sites]
    F --> G[Score each candidate site<br/>5 criteria, weighted]

    G --> H{Score >= threshold?}
    H -->|Yes| I[Site enters proposed network]
    H -->|No| J[Site gets light intervention only]

    I --> K[Analyze threshold type at site]

    K --> L{What is severed?}
    L -->|Border vs corridor| M[Border Lock]
    L -->|Cargo vs city| N[Cargo Lock]
    L -->|Valley vs hilltop| O[Altitude Lock]
    L -->|Last train vs first train| P[Temporal Lock]
    L -->|Invisible vs visible| Q[Visibility Lock]
    L -->|Uphill vs downhill + equity| R[Gradient Dispatcher]
    L -->|Gap vs gap| S[Gap Relay]
    L -->|Rail vs off-rail| T[Bridge Lock]
    L -->|Machine vs civic| U[Logistics Engine]

    M & N & O & P & Q & R & S & T & U --> V[Generate chamber parameters]
    V --> W[Present proposition to user]
    W --> X{User adjusts?}
    X -->|Weights| G
    X -->|Threshold| H
    X -->|Chamber params| V
    X -->|Accepts| Y[Final network + chamber designs]

    style A fill:#1a1a2e,stroke:#e0e0e0,color:#fff
    style Y fill:#1a1a2e,stroke:#e0e0e0,color:#fff
    style H fill:#2d2d44,stroke:#e0e0e0,color:#fff
    style C fill:#2d2d44,stroke:#e0e0e0,color:#fff
    style L fill:#2d2d44,stroke:#e0e0e0,color:#fff
```

Two things determine the outcome independently:
- **Which sites make the network** is determined by scoring (community-dependent).
- **Which lock type each site gets** is determined by threshold analysis (geography-dependent).

A user changing weights reshuffles which sites qualify. It never changes what lock type a qualifying site receives.

---

## 2. Scoring Pipeline

How raw data becomes a site score, and how the pipeline generalizes from healthcare to any community.

```mermaid
flowchart LR
    subgraph FIXED["CORRIDOR-LEVEL (reusable)"]
        direction TB
        MC[Modal Collapse Severity<br/>weight: 20%]
        GD[Gap Distance<br/>weight: 15%]
        IR[Infrastructure Readiness<br/>weight: 15%]
    end

    subgraph ADAPT["COMMUNITY-LEVEL (needs adaptation)"]
        direction TB
        AP[Affected Population Count<br/>weight: 25%]
        CC[Chain Criticality<br/>weight: 25%]
    end

    subgraph SCORING["SCORING ENGINE"]
        direction TB
        NORM[Normalize each<br/>criterion 0-5]
        WEIGHT[Apply weights]
        SUM[Weighted sum]
    end

    MC --> NORM
    GD --> NORM
    IR --> NORM
    AP --> NORM
    CC --> NORM

    NORM --> WEIGHT --> SUM --> RESULT[Site Score<br/>0.0 - 5.0]

    style FIXED fill:#1a2e1a,stroke:#90ee90,color:#fff
    style ADAPT fill:#2e1a1a,stroke:#ee9090,color:#fff
    style SCORING fill:#1a1a2e,stroke:#9090ee,color:#fff
```

### Normalization rules

Each criterion maps raw data to a 0-5 integer scale. The mapping is criterion-specific:

| Score | Modal Collapse | Gap Distance | Infra Readiness | Affected Population | Chain Criticality |
|-------|---------------|-------------|-----------------|--------------------|--------------------|
| 0 | Ratio < 1.2 | < 3 km | 5+ modes available | < 10 affected | No chain dependency |
| 1 | Ratio 1.2-1.5 | 3-5 km | 4 modes | 10-50 | Minor disruption |
| 2 | Ratio 1.5-2.0 | 5-8 km | 3 modes | 50-150 | Workaround exists |
| 3 | Ratio 2.0-3.0 | 8-12 km | 2 modes | 150-500 | Delayed service |
| 4 | Ratio 3.0-5.0 | 12-18 km | 1 mode | 500-1500 | Service interrupted |
| 5 | Ratio > 5.0 | > 18 km | 0 modes | > 1500 | Chain breaks completely |

The three corridor-level criteria use the same data and same scales regardless of community. The two community-level criteria require the AI research engine to produce raw numbers per candidate site, which then feed through the same normalization logic.

---

## 3. The Generalization Problem

The v2 paper's two community-specific criteria were healthcare-native. Generalization requires abstracting them without losing precision.

```mermaid
flowchart TD
    subgraph HEALTHCARE["HEALTHCARE (v2 paper)"]
        NW[Night worker count<br/>Nurses, doctors, lab techs<br/>stranded 01:30-03:30]
        HC[Healthcare chain criticality<br/>Blood samples expire,<br/>NICU transfers delayed,<br/>pharmacy restocking fails]
    end

    subgraph GENERIC["GENERIC ABSTRACTION"]
        AP2[Affected population count<br/>People in community X<br/>stranded during critical gap]
        CC2[Chain criticality<br/>What breaks in community X's<br/>supply chain if node fails]
    end

    subgraph BAKERY["EXAMPLE: BAKERY INDUSTRY"]
        BW[Bakers starting 03:00 shift<br/>stranded without transit]
        BC[Flour delivery chain breaks,<br/>morning production delayed,<br/>retail distribution fails]
    end

    subgraph TOURISM["EXAMPLE: TOURISM"]
        TW[Seasonal workers in lakeside<br/>hotels stranded after late shifts]
        TC[Guest transport chain breaks,<br/>airport connections missed,<br/>event logistics fail]
    end

    NW -->|abstract| AP2
    HC -->|abstract| CC2
    AP2 -->|apply| BW
    AP2 -->|apply| TW
    CC2 -->|apply| BC
    CC2 -->|apply| TC

    style HEALTHCARE fill:#2e1a1a,stroke:#ee9090,color:#fff
    style GENERIC fill:#1a1a2e,stroke:#9090ee,color:#fff
    style BAKERY fill:#2e2e1a,stroke:#eeee90,color:#fff
    style TOURISM fill:#1a2e2e,stroke:#90eeee,color:#fff
```

The abstraction holds because the underlying question is always the same: "How many people are stuck, and what breaks while they're stuck?" The community determines the nouns. The scoring framework provides the verbs.

What the AI research engine must produce for any new community:
1. **Per candidate site**: estimated count of affected people during the critical gap window.
2. **Per candidate site**: a chain criticality assessment — what downstream process fails, how severe, and whether workarounds exist.

These two numbers feed into the same normalization table and scoring engine. Everything else is corridor data that's already computed.

---

## 4. Weight Adjustment Flow

What happens when a user moves a slider.

```mermaid
flowchart TD
    subgraph WEIGHTS["USER WEIGHT PANEL"]
        W1["Affected Population: 25%"]
        W2["Chain Criticality: 25%"]
        W3["Modal Collapse: 20%"]
        W4["Gap Distance: 15%"]
        W5["Infra Readiness: 15%"]
        WSUM["Must sum to 100%"]
    end

    WEIGHTS --> RESCORE[Re-score all 24 candidate sites]

    RESCORE --> RANK[Re-rank by new scores]

    RANK --> THRESHOLD{Apply threshold<br/>default 3.0}

    THRESHOLD -->|Above| NEW_NET[New proposed network]
    THRESHOLD -->|Below| LIGHT[Light intervention zone]

    NEW_NET --> COMPARE{Changed from<br/>previous?}
    COMPARE -->|Sites added| ADDED[Highlight new additions<br/>+ their lock types]
    COMPARE -->|Sites removed| REMOVED[Show what dropped out<br/>+ why score fell]
    COMPARE -->|No change| STABLE[Network stable]

    ADDED & REMOVED & STABLE --> DISPLAY[Update map + network view]

    style WEIGHTS fill:#1a1a2e,stroke:#9090ee,color:#fff
    style THRESHOLD fill:#2d2d44,stroke:#e0e0e0,color:#fff
    style COMPARE fill:#2d2d44,stroke:#e0e0e0,color:#fff
```

### Two distinct adjustment layers

Weight adjustment operates on **site selection** only. It never touches chamber design. The system separates these cleanly:

```mermaid
flowchart LR
    subgraph LAYER1["LAYER 1: SITE SELECTION"]
        direction TB
        L1A[5 criterion weights]
        L1B[Node threshold]
        L1C["Output: which sites<br/>are in the network"]
    end

    subgraph LAYER2["LAYER 2: CHAMBER DESIGN"]
        direction TB
        L2A[Visibility vs carbon footprint]
        L2B[Comfort vs efficiency]
        L2C[Circulation priorities<br/>which of 4 to emphasize]
        L2D[Materiality preferences]
        L2E["Output: what the chamber<br/>looks like at each site"]
    end

    L1A --> L1C
    L1B --> L1C
    L1C --> LINK[Selected sites feed<br/>into chamber design]
    LINK --> L2A & L2B & L2C & L2D
    L2A & L2B & L2C & L2D --> L2E

    style LAYER1 fill:#1a2e1a,stroke:#90ee90,color:#fff
    style LAYER2 fill:#2e1a2e,stroke:#ee90ee,color:#fff
```

A user adjusting weights in Layer 1 sees the map change (sites appear/disappear). A user adjusting parameters in Layer 2 sees the 3D model change (chamber form evolves). These are independent interactions that happen in sequence or in parallel, but they never cross.

---

## 5. Lock Type Assignment Matrix

What conditions at a site trigger what lock type. This is the threshold analysis — determined by geography and infrastructure, not by scoring.

```mermaid
flowchart TD
    SITE[Candidate site qualifies<br/>score >= threshold] --> ANALYZE[Analyze physical conditions]

    ANALYZE --> Q1{Crosses national<br/>border?}
    Q1 -->|Yes| BORDER[Border Lock]
    Q1 -->|No| Q2{Major logistics/<br/>cargo corridor?}

    Q2 -->|Yes| Q2B{Adjacent to<br/>civic space?}
    Q2B -->|Yes| LOGISTICS[Logistics Engine]
    Q2B -->|No| CARGO[Cargo Lock]

    Q2 -->|No| Q3{Significant altitude<br/>change?}
    Q3 -->|Yes| Q3B{Steep grade +<br/>equity gap?}
    Q3B -->|Yes| GRADIENT[Gradient Dispatcher]
    Q3B -->|No| ALTITUDE[Altitude Lock]

    Q3 -->|No| Q4{Hospital or critical<br/>facility off-rail?}
    Q4 -->|Yes| BRIDGE[Bridge Lock]
    Q4 -->|No| Q5{Infrastructure exists<br/>but invisible?}

    Q5 -->|Yes| VISIBILITY[Visibility Lock]
    Q5 -->|No| Q6{Between two<br/>geographic voids?}

    Q6 -->|Yes| GAP[Gap Relay]
    Q6 -->|No| TEMPORAL[Temporal Lock]

    style SITE fill:#1a1a2e,stroke:#e0e0e0,color:#fff
    style BORDER fill:#2e1a1a,stroke:#ee9090,color:#fff
    style CARGO fill:#2e1a1a,stroke:#ee9090,color:#fff
    style ALTITUDE fill:#2e1a1a,stroke:#ee9090,color:#fff
    style TEMPORAL fill:#2e1a1a,stroke:#ee9090,color:#fff
    style VISIBILITY fill:#2e1a1a,stroke:#ee9090,color:#fff
    style GRADIENT fill:#2e1a1a,stroke:#ee9090,color:#fff
    style GAP fill:#2e1a1a,stroke:#ee9090,color:#fff
    style BRIDGE fill:#2e1a1a,stroke:#ee9090,color:#fff
    style LOGISTICS fill:#2e1a1a,stroke:#ee9090,color:#fff
```

### Assignment is deterministic, not scored

The decision tree above is evaluated top-to-bottom. A site gets the first lock type whose conditions it satisfies. This means:

- A border crossing with altitude change gets **Border Lock** (border condition takes priority).
- A cargo corridor adjacent to civic space gets **Logistics Engine** (the civic adjacency upgrades it from Cargo Lock).
- A site with no special geographic condition defaults to **Temporal Lock** — the pure dead-window problem that applies everywhere on the corridor.

The priority ordering reflects severity: border failures and logistics disconnections are harder to solve than pure temporal gaps, so they get specialized lock types first.

### Validation against v2 results

| Site | Conditions present | Assigned lock | v2 match? |
|------|-------------------|---------------|-----------|
| Lausanne CHUV | Steep grade, equity gap, hospital | Gradient Dispatcher | Yes |
| Morges Hospital Gap | Dead window, hospital nearby but not off-rail | Temporal Lock | Yes |
| Crissier-Bussigny-Ecublens | Logistics corridor + civic adjacency / hidden infra | Visibility Lock / Logistics Engine | Yes |
| Rennaz Hospital Island | Hospital off-rail | Bridge Lock | Yes |
| Lancy-Pont-Rouge | French border proximity | Border Lock | Yes |
| Nyon + Genolier | Major altitude change to Genolier clinic | Altitude Lock | Yes |
| Vevey Mid-Gap Relay | Between Lavaux Fracture voids | Gap Relay | Yes |
| Geneva North Industrial Belt | Cargo/logistics corridor, no civic adjacency | Cargo Lock | Yes |
| Montreux-Glion | Altitude change (funicular territory) | Altitude Lock | Yes |

All 9 v2 assignments are reproducible through the decision tree. This validates the tree's ordering.

---

## 6. Fixed vs. Flexible Parameter Diagram

What the system treats as ground truth versus what the user can adjust.

```mermaid
flowchart TD
    subgraph FIXED["FIXED CONSTRAINTS (ground truth)"]
        direction TB
        F1["49 stations: Geneva to Villeneuve"]
        F2["Station distances and altitudes"]
        F3["Existing rail, bus, shared mobility"]
        F4["Dead window: 01:30 - 03:30"]
        F5["3 geographic voids:<br/>Nyon-Gland 19.3km<br/>Gland-Morges 20km<br/>Lavaux Fracture 17.5km"]
        F6["Lock type assignment logic<br/>(geography-determined)"]
    end

    subgraph FLEXIBLE["FLEXIBLE PARAMETERS (user-adjustable)"]
        direction TB

        subgraph SELECTION["Site Selection"]
            S1["Criterion weights<br/>(5 sliders, sum to 100%)"]
            S2["Node threshold<br/>(default 3.0)"]
        end

        subgraph DESIGN["Chamber Design"]
            D1["Visibility vs carbon footprint"]
            D2["Comfort vs efficiency"]
            D3["Circulation priorities<br/>(which of 4 to emphasize)"]
            D4["Materiality preferences"]
            D5["Program mix"]
        end
    end

    subgraph DERIVED["DERIVED (computed, not set)"]
        direction TB
        R1["Corridor-level scores<br/>(from fixed data)"]
        R2["Community-level scores<br/>(from AI research)"]
        R3["Lock type per site<br/>(from threshold analysis)"]
        R4["Chamber geometry<br/>(from design parameters)"]
    end

    FIXED --> R1
    FIXED --> R3
    SELECTION --> R2
    DESIGN --> R4

    style FIXED fill:#2e1a1a,stroke:#ee9090,color:#fff
    style FLEXIBLE fill:#1a2e1a,stroke:#90ee90,color:#fff
    style DERIVED fill:#1a1a2e,stroke:#9090ee,color:#fff
    style SELECTION fill:#1a3e1a,stroke:#90ee90,color:#fff
    style DESIGN fill:#1a3e1a,stroke:#90ee90,color:#fff
```

### The pushback mechanism

When a user selects a region that doesn't match the data, the system uses the fixed constraints to explain why:

```mermaid
sequenceDiagram
    participant U as User
    participant S as Scoring Engine
    participant D as Data Layer

    U->>S: "I want to place a lock at Pully"
    S->>D: Score Pully across 5 criteria
    D-->>S: Score: 2.1 (below 3.0 threshold)
    S->>D: Find nearest qualifying site
    D-->>S: Lausanne CHUV scores 4.55, 3.2km away
    S-->>U: Pully scores 2.1 — below threshold.<br/>Lausanne CHUV (4.55) is 3.2km away<br/>and addresses the same gap.<br/>Proceed anyway or shift to CHUV?

    alt User insists
        U->>S: Proceed with Pully
        S-->>U: Lock placed at Pully.<br/>Score recorded as 2.1.<br/>Network efficiency note attached.
    else User accepts suggestion
        U->>S: Shift to CHUV
        S-->>U: Lock placed at Lausanne CHUV<br/>as Gradient Dispatcher.
    end
```

The pushback is informational, never blocking. The user always has the final say. But the system makes the cost visible: a low-scoring site means the intervention addresses less need per resource spent.

---

## 7. Full Decision Pipeline: End to End

Combining all the above into one view.

```mermaid
flowchart TD
    START([User begins]) --> COMMUNITY[Select or define community]

    COMMUNITY --> RESEARCH[AI research engine<br/>produces 2 numbers per site:<br/>affected population +<br/>chain criticality]

    RESEARCH --> MERGE[Merge with corridor data<br/>3 fixed criteria already computed]

    MERGE --> SCORE[Score all 24 candidates<br/>5 criteria x weights]

    SCORE --> FILTER{Score >= threshold?}

    FILTER -->|Yes: N sites| LOCK_ASSIGN[Threshold analysis<br/>per qualifying site]
    FILTER -->|No| LIGHT_ZONE[Light intervention<br/>bus, mobility, wayfinding]

    LOCK_ASSIGN --> NETWORK[Proposed lock network<br/>N sites, each with a lock type]

    NETWORK --> USER_REVIEW{User reviews}

    USER_REVIEW -->|Adjust weights| SCORE
    USER_REVIEW -->|Adjust threshold| FILTER
    USER_REVIEW -->|Override site| PUSHBACK[Pushback mechanism<br/>show score comparison]
    USER_REVIEW -->|Accept network| CHAMBER[Chamber design phase]

    PUSHBACK --> USER_DECIDE{Accept suggestion?}
    USER_DECIDE -->|Yes| NETWORK
    USER_DECIDE -->|No, keep override| CHAMBER

    CHAMBER --> PARAMS[User adjusts<br/>chamber parameters]
    PARAMS --> GENERATE[Generate Rhino scripts<br/>per selected site]
    GENERATE --> OUTPUT([Deliverable:<br/>lock network + chamber designs])

    style START fill:#1a1a2e,stroke:#e0e0e0,color:#fff
    style OUTPUT fill:#1a1a2e,stroke:#e0e0e0,color:#fff
    style FILTER fill:#2d2d44,stroke:#e0e0e0,color:#fff
    style USER_REVIEW fill:#2d2d44,stroke:#e0e0e0,color:#fff
    style USER_DECIDE fill:#2d2d44,stroke:#e0e0e0,color:#fff
```

---

## Technical Notes

### On the 1:1 problem (9 types for 9 nodes)

The current taxonomy has 9 lock types assigned to 9 nodes. This appears suspiciously fitted. Two observations temper the concern:

1. **Two nodes share a type.** Nyon + Genolier and Montreux-Glion both receive Altitude Lock. This demonstrates the type is reusable across sites with the same threshold condition. Crissier-Bussigny-Ecublens receives both Visibility Lock and Logistics Engine, suggesting some sites carry compound conditions.

2. **The types emerged from threshold analysis, not from the sites.** Each type corresponds to a distinct kind of severance (border, altitude, temporal, etc.). A new corridor would likely surface a subset of these same types — the geography is different, but the categories of failure are finite.

The real test comes when the tool is applied to a new community. If the same 9 types cover the new community's sites without inventing new ones, the taxonomy holds. If not, it needs extension — and the architecture should support adding lock types without restructuring the scoring engine.

### On the 3.0 threshold

The 3.0 cutoff was determined empirically from the healthcare analysis. It produced a natural break in the score distribution: a visible gap between the 9th-ranked site (3.10) and the 10th (2.85). This suggests the threshold reflects real structure in the data, not an arbitrary line.

For new communities, the threshold should be re-examined. The system defaults to 3.0 but allows user adjustment. A histogram of all candidate scores, with the current threshold marked, should be visible in the interface so users can see where the natural break falls for their community.

### On scoring edge cases

- **Tied scores**: Sites with identical scores are ordered by gap distance (larger gap = higher priority). Rationale: larger gaps leave more people without coverage.
- **Zero-weight criteria**: If a user sets a criterion weight to 0%, that criterion is excluded entirely. The remaining weights are renormalized to sum to 100%. The system warns that reducing to fewer criteria increases sensitivity to the remaining ones.
- **All sites below threshold**: If no site scores above threshold after weight adjustment, the system warns that the community may not have corridor-scale severance, and suggests lowering the threshold or reconsidering the community definition.
- **All sites above threshold**: If all 24 sites score above threshold, the system warns that the threshold may be too low for meaningful differentiation, and suggests raising it or examining whether the community-level data has sufficient variance.

### On the AI research engine's role

The research engine is the only non-deterministic component in the scoring pipeline. Everything else — corridor data, normalization scales, weight application, threshold comparison, lock type assignment — is mechanical. The research engine's job is narrow and well-defined: produce two numbers per candidate site (affected population count, chain criticality score) with supporting evidence.

Quality of output depends entirely on the quality of these two numbers. The system should surface the research engine's confidence level and source material so users can judge whether to trust the scores or override them.
