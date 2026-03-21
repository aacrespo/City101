# IBOIS × Agent Teams: Research Deep Dive

**Date**: 2026-03-19
**Context**: Preparing for conversation with IBOIS / AR-327 (Comp Design) staff about potential intersection between specialist construction knowledge and multi-agent computational workflows.

---

## 1. IBOIS Lab — What They Actually Do

**Laboratory for Timber Constructions (IBOIS)**, EPFL. Led by Prof. Yves Weinand.

IBOIS is not a traditional timber engineering lab. They sit at the intersection of **computational geometry, digital fabrication, and material intelligence**. Their research treats timber not as a generic building material but as a *variable, scanned, database-tracked physical object* with individual properties.

### Core Research Threads

| Thread | Key idea | Agent relevance |
|--------|----------|-----------------|
| **Biotope-Aware Roundwood** (Damien Gilliard, PhD) | Digital twins of individual trees stored in an object-oriented database. Properties + methods per tree. Design queries the database to find trees matching architectural specs while respecting ecological constraints. Serialization from game dev. | **HIGH** — This IS a structured database of construction elements with parametric properties. Exactly what a specialist agent would consume. |
| **Augmented Carpentry** | AR headset + AI tool detection (TTool) guides carpenters through cuts without shop drawings or jigs. Real-time pose estimation of tool heads. Open source. | **MEDIUM** — The constraint model (what cuts are possible, what tools exist) is implicit in the AR system. Could be externalized as agent knowledge. |
| **Manis** (Timber Plate Joinery Solver) | Grasshopper plugin: topology → joint geometry → CNC toolpaths → robotic trajectories → FEM analysis. Full design-to-fabrication pipeline. | **HIGH** — The joint generation algorithm encodes topological constraints, assembly sequences, and fabrication limits. This is specialist knowledge in code form. |
| **compas_wood** (Petras Vestartas) | COMPAS framework module for parametric timber joint generation. Joint types as parameterized models. | **HIGH** — Joint catalog with parameters = agent fuel. |
| **diffCheck** | Scan-vs-CAD comparison for fabricated timber. Point cloud analysis in Grasshopper. Tests quality of robotic assembly, AR-assisted cuts, CNC machining. | **MEDIUM** — Quality validation agent territory. A "QA agent" that compares as-built to as-designed. |
| **Raccoon** | CNC fabrication: drilling, milling, cutting, sawing. G-Code generation with collision detection. Tested on 5-axis Maka + ABB robots. | **HIGH** — Machine capability limits = fabrication constraint database. |
| **Roundwood Joinery** | Rhino 8 plugin for planning joints in scanned trunks. | **HIGH** — Bridges parametric design with material reality (actual tree geometry). |

### Key People to Know

| Person | Role | Why relevant |
|--------|------|-------------|
| **Damien Gilliard** | PhD candidate, teaches AR-327 | Roundwood database research + course lecturer. Primary contact. |
| **Yves Weinand** | Lab director, Prof. | Overall vision holder. Architect-engineer. |
| **Andrea Settimi** | PhD, developed script-sync & diffCheck | Tool builder. Understands Rhino-Python-VSCode pipeline deeply. |

---

## 2. The Course: AR-327 (Spring 2026)

**"Introduction to Computational Architecture"** — BA level, for absolute programming beginners.

### Structure
12 sessions, Feb–May 2026. Progression:
1. **Sessions 1–5**: Rhino basics → Python fundamentals → OOP
2. **Sessions 6–11**: RhinoPython, RhinoCommon API, 2D/3D geometry, transformations, BREP, Booleans
3. **Session 12**: Final project — **Computational Timber Design**

### What's Interesting for Us

The course teaches students to go from zero Python to writing Rhino scripts that generate timber geometry with Boolean operations. The final two assignments are:
- **08**: BREP joints (Boolean union/difference/intersection for timber connections)
- **09**: Computational Timber (full parametric timber design application)

This is literally the same pipeline we use in our Rhino MCP workflows — but taught as manual scripting. The agent layer we've built sits on top of exactly this skill set.

### Software Stack
- Rhino 8 + RhinoCommon API
- Python (CPython via Rhino 8)
- script-sync (their VSCode↔Rhino bridge — compare with our MCP bridge)

---

## 3. What Structured Data Actually Exists

This is the critical question: **is specialist construction knowledge already in machine-readable form?**

### ✅ Yes — Exists in structured/parameterized form

| Data source | What | Format | Access |
|-------------|------|--------|--------|
| **Roundwood tree database** (Gilliard) | Individual tree digital twins: shape, properties, methods | Object-oriented DB, serialized | Research code — would need collaboration |
| **compas_wood joint catalog** | Parameterized timber joint types | Python objects within COMPAS framework | Open source (GitHub) |
| **Manis solver** | Topological constraints → joint geometry rules → toolpaths | Grasshopper components (C#/.NET) | Open source (GitHub) |
| **Raccoon machine profiles** | 5-axis CNC capabilities, collision envelopes | G-Code generation rules | Open source (GitHub) |
| **diffCheck tolerance data** | Scan-vs-CAD deviation metrics for various fabrication methods | Point cloud analysis pipeline | Open source (GitHub) |

### ⚠️ Partially — Exists but not as clean databases

| Knowledge domain | Current form | What's missing |
|------------------|-------------|----------------|
| **Timber joint engineering rules** | Embedded in Manis/compas_wood algorithms | No standalone parameter table (span limits, load capacities separated from code) |
| **CNC fabrication limits** | Encoded in Raccoon's collision detection | Not externalized as a queryable constraint set |
| **Assembly sequence logic** | Manis's assembly solver | Implicit in algorithm, not declarative |

### ❌ No — Doesn't exist as structured data (research gaps)

| Knowledge domain | Current state | Opportunity |
|------------------|--------------|-------------|
| **Craft knowledge ontology** | No IFC-like standard for timber craft | Research gap — exactly what your question about "IFC for craft" targets |
| **Cross-material construction constraints** | Timber tools exist, but nothing spans timber + earth + stone | Huge gap — a "digital piseur" or "digital mason" has no structured knowledge base |
| **Material-constraint-to-geometry mapping** | Each tool does its own thing | No unified schema that says "this material + this constraint → these geometry rules" |

---

## 4. The Intersection: Agent Teams × IBOIS Knowledge

### What We've Proven (Lock 05 Test)

Our Rhino Router MCP test demonstrated:
- **7 specialist agents** working in parallel on one architectural model
- **709 objects** created through coordinated phases (rough-in → detail → review)
- Agents sharing geometry positions, flagging spatial conflicts, cascading improvements
- **Inter-agent coordination** is where the value emerges — not just parallelism

### What IBOIS Has That We Don't

They have **deep, parameterized construction knowledge** — the kind that turns a generic "box at coordinates" into a structurally valid, fabrication-ready timber joint. Their tools encode:

1. **Material constraints** → what timber can/can't do at given dimensions
2. **Fabrication constraints** → what the CNC/robot can actually cut
3. **Assembly constraints** → what sequence allows physical construction
4. **Ecological constraints** → which trees to use without damaging the forest (Gilliard's DB)

### What We Have That They Don't

They work with **single-user, single-tool workflows**. One person runs Grasshopper, tweaks parameters, generates geometry. No notion of:

1. **Parallel specialist agents** with different knowledge domains working simultaneously
2. **Real-time constraint checking** across domains (structure vs. fabrication vs. ecology)
3. **Natural language interface** to construction knowledge ("make a mortise-tenon joint here that the 5-axis can cut")
4. **Coordination protocols** between construction disciplines

### The Synthesis

```
IBOIS knowledge (parameterized construction constraints)
    +
Rhino Router MCP (multi-agent parallel modeling)
    +
Agent specialization (each agent loads domain-specific context)
    =
Multi-agent computational construction system
```

A **Timber Structure Agent** loads compas_wood joint catalog + Manis constraint rules.
A **Fabrication Agent** loads Raccoon machine profiles + diffCheck tolerances.
A **Ecology Agent** loads Gilliard's tree database + forest management rules.
A **Structure Agent** loads engineering parameters from FEM analysis.

They all operate on the same Rhino model through the router, each constraining and enriching the geometry from their specialist perspective.

---

## 5. Strategic Questions — Refined

Based on the research, here are your questions reframed with specific knowledge of what IBOIS has:

### Q1: The Tree Database (→ Gilliard directly)

> "Damien, your roundwood database with digital twins of individual trees — is that data accessible outside of the Rhino plugin? Like, could an external system query 'give me trees between 20-30cm diameter with < 5° taper that are harvestable'?"

**Why this works**: Shows you've read his research. The answer tells you if the database has an API or is locked inside Grasshopper. If queryable → immediate agent integration path.

### Q2: compas_wood Joint Catalog (→ Gilliard or Settimi)

> "In compas_wood, the joint types are parameterized — are those parameters documented somewhere as a reference table? Like, for a tenon joint: min/max dimensions, required clearance, grain direction constraint?"

**Why this works**: You're asking if the implicit knowledge in the code is also explicit somewhere. If yes = agent context file. If no = research contribution opportunity.

### Q3: Fabrication Constraints (→ Settimi or Weinand)

> "With Raccoon and the CNC workflow — is there a profile that describes what the machine can do? Like, minimum radius, max depth, tool changeover constraints? Something that could be loaded into a design tool to pre-validate geometry before sending to fabrication?"

**Why this works**: Raccoon does collision detection, so the constraints exist somewhere. You're asking if they're externalized. This opens the "fabrication agent" conversation naturally.

### Q4: Multi-Agent Framing (→ gauge interest, any of them)

> "We've been experimenting with running multiple AI agents on the same Rhino model simultaneously — each with different knowledge. Like one handles structural logic, another does joinery detailing. Have you thought about whether your parametric tools could work in that kind of split-expertise setup?"

**Why this works**: Describes what you've built without name-dropping or overselling. Invites them to see their tools as agent-loadable knowledge bases. Note: Gilliard's course literally teaches students to write RhinoPython — our agents run RhinoPython through MCP. The connection is direct.

### Q5: The Research Gap (→ Weinand, or as thesis pitch)

> "Is there an ontology or structured taxonomy for timber construction knowledge — something like IFC but at the craft level? Joint types, material constraints, fabrication rules, assembly sequences — all in one queryable structure?"

**Why this works**: If it exists, you want it. If it doesn't, you've identified a research gap that their tools are circling around but haven't formalized. This could be a student project, a thesis, or a collaboration.

### Q6: The "Digital Piseur" Provocation (→ save for if the conversation is going well)

> "What about extending this to other materials? Like, could you imagine a 'digital piseur' — a computational tool that knows rammed earth constraints the way compas_wood knows timber joints? Wall thickness limits, curing time vs. humidity, formwork pressure at different heights?"

**Why this works**: Current research on rammed earth computational design exists (stereotomic vaults, parametric formwork, robotic earth construction) but there's NO equivalent of compas_wood for earth. The IBOIS model of "parameterized construction knowledge" could be a template for other materials.

---

## 6. What Exists in the Wild — Ontologies & Databases

### IFC (Industry Foundation Classes)
- buildingSMART standard for BIM data exchange
- **ifcOWL**: OWL ontology version of IFC schema — makes building data queryable via semantic web
- **ifcOWL-DfMA**: Extension for Design for Manufacturing and Assembly
- **Gap**: IFC models buildings at the component level, not at the craft/joint/fabrication level. A timber beam is an `IfcBeam`, but the mortise-tenon joint connecting it isn't well-represented.

### Digital Construction Ontologies (DiCon)
- Semantic enablers for built assets, design, and construction planning
- Covers agents, resources, spatio-temporal aspects
- **Gap**: Abstract — doesn't encode material-specific construction knowledge

### COMPAS Framework (ETH Zurich / NCCR)
- Open-source computational design platform
- compas_wood is a module within this
- Also: compas_fab (fabrication), compas_fea (finite elements), compas_assembly
- **Closest thing to an ontology for computational construction**, but it's a code framework, not a formal ontology

### Rammed Earth — State of the Art
- Parametric analysis of thermal performance (Delphin models)
- Ray-tracing algorithms for verifying ramming constraints (formwork geometry, rammer reach)
- Stereotomic vault form-finding with fabrication constraints
- Robotic rammed earth fabrication (ETHZ, MIT)
- **Gap**: No compas_earth equivalent. No parameterized database of earth construction constraints.

---

## 7. Connection to City101 / Prototypology

### Why This Matters for A04

The "Sentient Cities" studio explores how infrastructure creates behavior along the Geneva-Villeneuve corridor. The prototypology concept — **site typology generator** where you pick points and get Rhino scripts — is fundamentally about encoding spatial knowledge into computational tools.

IBOIS is doing the same thing for construction: encoding **material and fabrication knowledge** into computational tools. The parallel is:

| City101 | IBOIS |
|---------|-------|
| Site behavior database → agent context | Tree/joint/fabrication database → tool parameters |
| Multi-agent site modeling | Could be: multi-agent construction modeling |
| "Pick a point, get a prototypology" | "Pick a joint type, get a fabrication-ready detail" |
| Rhino Router MCP | Rhino + Grasshopper + compas_wood |

### Potential Collaboration Angles

1. **Student project**: "Multi-agent parametric timber design" — use our router + their joint knowledge
2. **Tool integration**: compas_wood parameters → agent context files → specialist timber agent in our system
3. **Research paper**: Formalize the "construction knowledge as agent context" framework
4. **Thesis direction**: "Ontology of computational construction" — unify what compas_wood, Manis, Raccoon know into a formal, queryable knowledge structure

---

## 8. Sources

### IBOIS Lab
- [IBOIS Homepage](https://www.epfl.ch/labs/ibois/)
- [IBOIS Research](https://www.epfl.ch/labs/ibois/research/)
- [IBOIS Tools](https://www.epfl.ch/labs/ibois/index-html/tools/)
- [IBOIS GitHub](https://github.com/ibois-epfl)
- [Biotope-Aware Roundwood Architecture](https://www.epfl.ch/labs/ibois/research/ongoingresearch/biotope-aware-round-wood-architecture/)
- [Automation & Digitalization Research](https://www.epfl.ch/labs/ibois/research/ongoingresearch/automation-digitalization-and-computational-methods-in-advanced-timber-structures/)

### Course
- [AR-327 Course Website](https://ibois-epfl.github.io/AR-327-2026-Introduction-to-computational-architecture/)
- [EPFL Course Page](https://www.epfl.ch/labs/ibois/introduction-to-computational-architecture/)

### Tools
- [compas_wood (GitHub)](https://github.com/petrasvestartas/compas_wood)
- [Manis (GitHub)](https://github.com/ibois-epfl/Manis-timber-plate-joinery-solver)
- [diffCheck (GitHub)](https://github.com/diffCheckOrg/diffCheck)
- [diffCheck Paper (arXiv)](https://arxiv.org/html/2502.15864v1)
- [Augmented Carpentry (GitHub)](https://github.com/ibois-epfl/augmented-carpentry)
- [TTool (GitHub)](https://github.com/ibois-epfl/TTool)
- [Raccoon (GitHub)](https://github.com/ibois-epfl/Raccoon-ibois)
- [script-sync (GitHub)](https://github.com/ibois-epfl/script-sync)
- [roundwood-joinery (GitHub)](https://github.com/ibois-epfl/roundwood-joinery)

### Ontologies & Frameworks
- [ifcOWL (buildingSMART)](https://technical.buildingsmart.org/standards/ifc/ifc-formats/ifcowl/)
- [Digital Construction Ontologies](https://digitalconstruction.github.io/v/0.5/)
- [COMPAS Framework](https://compas.dev/)

### Rammed Earth Computational Design
- [Computational Fabrication Reinventing Rammed Earth](https://medium.com/@Architects_Blog/from-ancient-walls-to-digital-clay-how-computational-fabrication-is-reinventing-rammed-earth-for-45ceb11a31cb)
- [Stereotomic Rammed Earth Vault (ResearchGate)](https://www.researchgate.net/publication/393194883_Material_informed_computational_design_for_a_stereotomic_rammed_earth_vault)
