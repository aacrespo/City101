# From Codebase to Corridor: Agentic AI Workflows for Architectural Design

**Andrea Crespo**
EPFL BA6 Architecture Studio — AR-302k, Studio Huang ("Sentient Cities")
March 2026

---

## Introduction: The Convergence

Architecture and software engineering are both design disciplines. Both produce complex artifacts from incomplete information. Both require coordinating multiple specialists toward a coherent whole. Both move through phases of increasing certainty — from brief to concept to detail to delivery. And both, as of 2025-26, are confronting the same question: what happens when AI agents can do meaningful chunks of the work autonomously?

Software engineering is roughly 18-24 months ahead of architecture in systematizing the answer. The reasons are structural, not cultural: code is text, agents operate on text, and the toolchain for version-controlling, testing, and deploying text artifacts has been refined over decades. Architecture's primary artifacts — drawings, models, spatial relationships — resist the text pipeline. A floor plan is not a pull request. A section cut is not a unit test. But the *organizational patterns* that software teams have developed for coordinating AI agents turn out to be remarkably transferable, once you stop looking at the artifacts and start looking at the workflows.

This document explores that transfer. It draws on a specific case study — City101, an EPFL studio project analyzing the 101km Geneva-Villeneuve rail corridor — not because that project set out to build an "AI workflow," but because the demands of rigorous, multi-dimensional spatial analysis forced one to emerge. When you need to coordinate 4 Claude accounts, 49 canonical stations, 20+ datasets, and 2 human collaborators across 11 sessions, you either build infrastructure or you drown. What we built, without initially knowing the vocabulary, mirrors patterns that software teams have been formalizing under names like "supervisor architecture," "data contracts," and "CI/CD pipelines."

The question for architecture is not *whether* agents will reshape practice — they already are, at firms from ZHA to Heatherwick to academic labs at ICD Stuttgart. The question is *how to structure that use* for the kind of work architecture actually requires: spatially embedded, multi-dimensional, iterative, and irreducibly dependent on human judgment about experience.

---

## Section 1: The Territory — Agentic Workflows in Software

### 1.1 What "agentic" means

The term gets overused. Here is the distinction that matters.

A **prompt-response** interaction is a question and an answer. "What is the population of Lausanne?" returns a number. No tool use, no sequencing, no intermediate decisions.

A **chat** interaction is a conversation. The human steers, the model responds, the human adjusts. Most architectural AI use today lives here — iterating on a Midjourney image, refining a Grasshopper definition through dialogue, asking an LLM to restructure a spreadsheet.

An **agentic** interaction is different in kind. The human defines a goal and constraints. The agent determines the path: which tools to use, in what order, what intermediate decisions to make, when to ask for clarification, and when to proceed autonomously. The agent has *bounded autonomy* — it can choose its methods but not its objectives.

In architectural terms: chat is like standing over a drafter's shoulder giving instructions line by line. Agentic is like briefing a junior architect on Monday morning and reviewing their work on Friday. The brief defines the outcome; the junior determines how to get there — which references to pull, which details to develop first, when to check back.

This distinction matters because architecture's complexity demands the agentic mode. You cannot chat your way through analyzing 49 stations across 7 time slots with 5 break dimensions. The combinatorial space is too large for turn-by-turn steering. You need agents that can work autonomously within defined boundaries, report back structured findings, and hand off cleanly to the next phase.

### 1.2 Three dominant patterns

Software engineering has converged on three primary architectures for multi-agent systems. Each has a direct architectural analogy.

**Supervisor pattern.** A coordinator agent receives a task, decomposes it, routes subtasks to specialized worker agents, collects results, and synthesizes the output. The supervisor never does the work itself — it manages. This is the most common production pattern because it is the most controllable. The supervisor can enforce quality gates, retry failed tasks, and maintain global coherence.

Architectural analogy: the project architect who delegates structural calculations, MEP coordination, and facade studies to specialists, then integrates the results into a coherent building.

**Blackboard pattern.** All agents share a common workspace — the "blackboard." Each agent reads the current state, contributes what it can, and writes its contribution back. There is no central coordinator. Coherence emerges from the shared medium and the agents' ability to build on each other's work.

Architectural analogy: the design studio pinup wall, where team members post work, read each other's progress, and develop the project through accumulation rather than delegation. Also: the BIM model as shared truth, where structural, mechanical, and architectural teams all read from and write to the same federated model.

**DAG (Directed Acyclic Graph) pipeline.** Tasks are arranged in a dependency graph. Data flows forward through processing stages. Each stage transforms its inputs and passes outputs to downstream stages. No cycles, no backtracking.

Architectural analogy: the design phase sequence — A01 (data collection) feeds A02 (analysis), which feeds A03 (design intervention). Or more granularly: raw API data feeds a processing script, which feeds a spatial join, which feeds a map, which feeds a narrative.

### 1.3 What actually works

The theoretical patterns are clean. Practice is messier, and the lessons from software teams deploying agent systems in production are instructive.

**Small teams outperform large ones.** Two to three focused agents consistently outperform five to seven narrow specialists. The reason is coordination cost: every additional agent introduces potential naming conflicts, schema mismatches, and communication overhead. The City101 research-with-agent-team protocol states this explicitly: "Prefer fewer, broader agents over many narrow ones. A single agent that searches three BFS tables is better than three agents each searching one table, because the agent can cross-reference findings and adapt its queries based on what it discovers."

**The critical infrastructure is not the agents — it is the contracts between them.** Shared schemas, canonical entity lists, explicit state. Without these, you get what software calls "integration hell" — three agents producing data that cannot be joined because each used a different name for the same station. The City101 project learned this the hard way: "If one agent writes 'Lausanne Gare' and another writes 'Lausanne' and a third writes 'Lausanne CFF', no downstream join works."

**Verification beats generation.** It is cheaper and more reliable to have agents generate work and then verify it rigorously than to attempt error-free generation. This is why software has code review, automated testing, and CI/CD — not because developers are unreliable, but because verification at integration is structurally superior to hoping for correctness at creation.

### 1.4 The collaboration layer

In software, the collaboration infrastructure is mature and largely invisible: git provides version history and branching, GitHub provides code review (pull requests) and automated validation (CI/CD), and issue trackers provide task management. These patterns are beginning to appear in design tools.

**Speckle** offers object-level version control for 3D geometry — you can track changes to individual beams, walls, and spaces across time, with branching for design alternatives and merging for integration. Arup has used Speckle for cross-disciplinary coordination on projects like King's Cross.

**BIMcollab** and **Trimble Connect** provide automated model checking — the architectural equivalent of CI: "does this model have any hard clashes? Do all fire exits meet code?" These run automatically, catching errors before human review.

The **AGENTS.md** format, emerging in software repositories, defines governance rules for AI agents: which files they can modify, what approval gates exist, what coding standards apply. This is nascent but directly applicable to design — imagine a project AGENTS.md that specifies which agents can modify the structural model vs. the facade model vs. the site plan.

The gap between software and architecture collaboration remains significant. Design files are often binary (a .3dm Rhino file cannot be "diffed" line by line the way source code can). "Merging" two spatial design alternatives requires human judgment — you cannot automatically merge two different facade options the way you can merge two branches of code that modify different functions. And the real-time collaboration model (Figma, Google Docs) is expected in design, while software still largely works asynchronously (commit, push, review, merge). These differences are not insurmountable, but they explain why architecture's adoption of agentic workflows lags software's.

---

## Section 2: What is Already Happening in Architecture

### Six patterns from City101

City101 is an EPFL BA6 architecture studio project analyzing the 101km Geneva-Villeneuve rail corridor. The question was straightforward: does this corridor function as one continuous city? Answering it rigorously required analyzing 49 train stations across 5 dimensions of continuity (connectivity, workspace, temporal access, transit frequency, comfort), 7 time slots, multiple pricing regimes, and dozens of datasets from classmates, public APIs, and spatial databases. Two humans (Andrea and Henna) coordinated with four Claude accounts (Cairn, Cairn Code, Lumen, Meridian) across 11 sessions spanning two weeks.

The workflow was not designed in advance. It emerged from the demands of the work. In retrospect, it embodies six patterns that map directly to software engineering practices.

| Pattern | What it is | Evidence |
|---------|-----------|---------|
| **A: Multi-account coordination** | 4 Claude accounts with different capabilities coordinated through structured handoffs | CLAUDE.md team system; 20 handoff files spanning S1-S11 plus Lumen sub-sessions S8.1-S8.3 |
| **B: Monolithic script as unit of work** | Self-contained scripts: fetch, filter, process, match, write, summary | 8 scripts in `scripts/` (compute_wci.py, fetch_ridership.py, journey_workability.py, etc.) |
| **C: Staged promotion** | Agents write to `output/` staging area; only the lead promotes verified work to `datasets/` | "Move verified outputs from staging to production paths. Only the lead does this." |
| **D: Living state files** | CONTEXT.md (current state), LEARNINGS.md (accumulated pitfalls), handoffs (session continuity) | CONTEXT.md updated through 10+ sessions; LEARNINGS.md with API pitfalls discovered across sessions |
| **E: Canonical entity lists** | 49 stations with canonical names, IDs, and coordinates. Every agent maps to this list before writing output. | "If one agent writes 'Lausanne Gare' and another writes 'Lausanne' and a third writes 'Lausanne CFF', no downstream join works." |
| **F: LOI/LOG/LOD as progressive certainty** | Three independent axes (information, geometry, development) decoupled from traditional BIM LOD | 00_Workflow_v04.md: "Maximize LOI early, add LOG only as LOD increases" |

Each pattern deserves unpacking.

**Pattern A: Multi-account coordination** emerged because different platforms have different capabilities. Cairn on the desktop app has MCP access — it can directly control QGIS, Rhino, Chrome, and the filesystem. Cairn Code (the CLI agent) can spawn parallel subagents and run Python scripts. Lumen on the browser has project knowledge files but no tool access. The insight from LEARNINGS.md: "MCP access comes from the desktop app, not the account. Whichever account is on the desktop app can control spatial tools." This forced a division of labor: Cairn Code produces data in parallel through subagents, Cairn on the desktop validates it spatially through QGIS, and the handoff system keeps both in sync.

**Pattern B: Monolithic scripts** were not an aesthetic choice but a survival strategy. Early sessions tried interactive data exploration — inspecting API responses, filtering interactively, adjusting queries on the fly. This filled the context window and caused conversations to hit their limit before the analysis was complete. The lesson, documented in LEARNINGS.md: "For large data operations: write a single self-contained script that runs end-to-end and prints only a summary." The pattern became: fetch, filter, process, match, write output, print comprehensive summary. The summary must list every dataset queried, row counts, anything unexpected, and download URLs for data not fetched. This way the session stays clean but no leads are lost.

**Pattern C: Staged promotion** is the architectural equivalent of code review. Agents write to `output/` — a staging area. The lead agent or the human reviews the output: Are the coordinates valid? Do the entity names match the canonical list? Are there null values in required fields? Only after verification does the data move to `datasets/`, the production directory that all subsequent analysis reads from. "Nothing goes to `datasets/` unverified."

**Pattern D: Living state files** solved the memory problem. Individual handoff files (20 of them, session-specific) provide traceability but are impractical to read at the start of every session. CONTEXT.md is a living document — updated at the end of each session with the current state of all datasets, all findings, and all open questions. LEARNINGS.md accumulates pitfalls: "The transport.opendata.ch stationboard with limit=30 made every station look identical (~30 trains/hr). Only after removing the cap did the real 42x variation appear." Every new session reads these two files first. The handoffs still exist for the audit trail, but the living files are the primary context.

**Pattern E: Canonical entity lists** are the data contract that makes multi-agent work possible. The 49-station list with exact names, WGS84 and LV95 coordinates, and unique IDs is the join key for every dataset. When a new source calls a station "Gare de Lausanne" instead of "Lausanne," the agent maps it before writing output. Without this, the 33-dataset crossref (2,093 points from classmate data) could never have been produced — each classmate used their own naming conventions.

**Pattern F: LOI/LOG/LOD** is perhaps the most architecturally native pattern. The 00_Workflow_v04.md document defines three independent axes: Level of Information (data richness), Level of Geometry (visual/geometric complexity), and Level of Development (design certainty). The key insight: "Maximize LOI early, add LOG only as LOD increases." In practice, this means collecting every available attribute from every API call from the start ("work rich"), keeping geometric representations simple until design decisions lock, and never confusing a detailed rendering with a decided design. The anti-pattern is explicitly called out: "High LOG + Low LOI + Low LOD: Pretty render, no data, design not locked. Dangerous — looks done but isn't."

### The QGIS MCP workflow

One pattern deserves special attention because it has no direct software equivalent: the spatial validation loop.

Cairn (running on the desktop with MCP access) can directly interact with a live QGIS project containing 60 layers. It can add layers, run spatial queries, check whether a generated dataset places correctly against the Swiss national basemap, and flag coordinates that fall in the lake instead of at a train station. The workflow: Cairn Code (the CLI) spawns agents that produce data in parallel. Cairn (the desktop) loads the output into QGIS, validates it spatially, and promotes it to production if it checks out.

This is closer to what software calls "integration testing" than anything else in the pipeline — except that the "test" is visual and spatial, not logical. A row of coordinates that passes all schema validation might still be wrong if it places a charging station in the middle of Lake Geneva. The QGIS MCP bridge makes that check automatable.

### Other documented cases

City101 is a student project. The patterns it discovered are appearing at much larger scales across the profession.

**Heatherwick Studio** built a 5-person internal team called "Ge-Code" that developed two tools: Dreamhopper, a text-to-3D plugin for Rhino that generates design concepts from natural language prompts, and Climate Atlas, an internal knowledge base that accumulates project-specific environmental data. They explicitly rejected off-the-shelf AI tools, citing privacy concerns and the need for firm-specific training data. The pattern parallel: tool-first design (build capabilities before workflows) and living state files (Climate Atlas as persistent institutional memory).

**Zaha Hadid Architects (ZHA)** deployed over 20 designers using custom NVIDIA Omniverse extensions where AI models trained on design briefs generate concept options. The pattern parallel: specialized agents per task type — form-generation agents, environmental analysis agents, visualization agents — coordinated through the Omniverse shared environment.

**Vectorworks Text2BIM** demonstrates the supervisor pattern in architectural production. Published in the ASCE Journal of Computing in Civil Engineering (Volume 40, Number 2, March 2026), their system uses four LLM agents in sequence: a Product Owner (interprets the brief), an Architect (spatial logic), a Programmer (generates IFC), and a Reviewer (validates the output). Across 692 test scenarios, the system achieved 91.1% validity — meaning 91.1% of generated BIM elements met schema and spatial constraints. The architecture is pure supervisor pattern with staged verification.

**IAAC HyperBuilding** at the Institute for Advanced Architecture of Catalonia ran a multi-team parametric design exercise where teams made weekly Speckle uploads, tracked progress through Power BI dashboards, and managed upstream/downstream dependencies between structural, envelope, and MEP teams. The pattern parallel: data contracts (Speckle schemas as shared interfaces) and shared task lists (the dashboard as coordination medium).

**Arup's King's Cross R8** project used a live Tekla-Grasshopper link for parallel design development — structural engineers worked in Tekla while architects iterated in Grasshopper, with automated clash detection through Trimble Connect catching conflicts continuously. The pattern parallel: CI/CD (automated validation at every change) and branching for parallel work (structural and architectural streams running simultaneously against a shared model).

**ICD Stuttgart and Gramazio Kohler at ETH Zurich** have pioneered computational fabrication workflows that require new roles — dfab managers, computational designers, robotic fabrication programmers — and new coordination tools. Their fabrication projects use GitHub repositories for version-controlling robotic toolpath code, with the same commit-review-merge cycle that software teams use. The pattern parallel: role specialization (each team member has a defined agent-like scope) and version control as coordination infrastructure.

**Autodesk Forma** embeds AI agents that run parallel evaluations — noise analysis, wind simulation, daylight assessment, embodied carbon calculation — on site designs simultaneously. The user adjusts building massing; all analyses update. The pattern parallel: parallel specialist agents with a shared spatial model as coordination medium.

**QGIS GIS Copilot**, documented as "GIS Copilot: towards an autonomous GIS agent for spatial analysis" (2025), demonstrates LLMs embedded directly in GIS environments that generate and execute spatial analysis workflows autonomously. Given a natural language query ("show me all stations more than 2km from the nearest workspace"), the system generates the appropriate QGIS processing chain — buffer, spatial join, filter — and executes it. This is the QGIS MCP pattern generalized: AI agents that reason about spatial relationships, not just text and code.

### Academic frameworks

The academic community has begun formalizing what practitioners are discovering empirically.

Pantazis (2024), writing in De Gruyter, explores multi-agent form-finding systems where agents with different optimization objectives (structural efficiency, daylight access, view quality) negotiate spatial configurations through iterative negotiation. The framework explicitly addresses the question City101's crossref analysis raised: what happens when independently optimized systems are spatially overlaid?

A three-layer cognitive architecture for AI-assisted urban planning (arxiv, 2025) proposes perception, reasoning, and action layers — mapping roughly to data collection, analysis, and design intervention. The layers operate as semi-autonomous agents coordinated through a shared urban model.

MCP4IFC (arxiv 2511.05533) proposes using the Model Context Protocol to bridge LLMs and IFC building models, enabling agents to query, reason about, and modify BIM data through natural language. This is the architectural equivalent of giving agents API access to the codebase.

These academic efforts share a common recognition: architectural design is too complex and too multi-dimensional for single-agent AI. The future is in coordination, not capability.

---

## Section 3: The Transferable Patterns

### Software-to-architecture pattern mapping

The patterns discovered in City101 and observed across the profession map systematically to software engineering concepts.

| Software Pattern | Architecture Equivalent | City101 Example |
|-----------------|----------------------|----------------|
| Task decomposition | Investigation decomposition | TODO_4_POINTS.md: 4 independent investigations (Break Points, Temporal, GA, Reviews), each with explicit inputs, outputs, and severity classification |
| Code review / PR | Design verification / staged promotion | QA gate: agents write to `output/`, lead verifies schema + spatial integrity, promotes to `datasets/` |
| CI/CD pipeline | Design pipeline + validation | A01 (collection) feeds A02 (analysis) feeds A03 (intervention); automated coordinate range checks at each handoff |
| Git branching | Analytical alternatives | Lumen's diversity research (S8.1-S8.3) as independent "branch" exploring Shannon indices while Cairn continued temporal analysis on "main" |
| Shared task list | Shared analytical workspace | CONTEXT.md + `datasets/` as single source of truth; any account reads these first |
| Tool-first design | Capability-first design | 8 monolithic scripts as composable, rerunnable tools (compute_wci.py can be re-run when inputs change) |
| API contracts | Data contracts + canonical schemas | Column naming conventions (snake_case, `is_` for booleans, `pct_` for percentages), coordinate validation ranges (lat 46.1-46.6, lon 6.0-7.1) |
| `.env` / config files | Living state files | CONTEXT.md (what exists), LEARNINGS.md (what to avoid), CLAUDE.md (how to work) |
| `README.md` | Project governance | CLAUDE.md as comprehensive entry point (~380 lines): conventions, data inventory, team system, design system |
| Linting / static analysis | Schema validation | Programmatic checks: "assert df['lat_wgs84'].between(46.1, 46.6).all()" before any promotion |

### BIM as natural agent infrastructure

Building Information Modeling, despite its reputation for bureaucratic overhead, turns out to be a surprisingly natural substrate for agentic workflows. The reason is that BIM already embeds the key abstractions that software teams had to invent.

**BIM dimensions as agent specializations.** The "nD BIM" framework assigns specific responsibilities to each dimension:

- **3D**: Geometry and spatial relationships
- **4D**: Construction scheduling and time
- **5D**: Cost estimation and quantity takeoff
- **6D**: Sustainability and energy performance
- **7D**: Facilities management and operations

Each dimension is a natural agent role. A 4D agent reasons about construction sequences. A 5D agent tracks costs as design changes propagate. A 6D agent evaluates embodied carbon and operational energy. The model is the shared workspace; the dimensions are the agent specializations.

**IFC as universal API contract.** The Industry Foundation Classes standard (ISO 16739-1:2024), maintained by buildingSMART, defines a machine-interpretable schema for building data. An IFC file is, in essence, an API contract: it specifies exactly what data types exist (IfcWall, IfcDoor, IfcSpace), what attributes each type carries, and how types relate to each other. When Vectorworks' Text2BIM system generates building elements, it writes IFC. When Trimble Connect checks for clashes, it reads IFC. The schema is the contract.

**Clash detection as CI/CD.** This is perhaps the most direct mapping. In software, continuous integration means: every time code changes, automated tests run to catch errors before they reach production. In BIM, clash detection does the same thing:

- **Hard clashes** (two objects occupying the same space) = type errors in software. A duct passing through a structural beam is as unambiguous as a function expecting a string but receiving an integer.
- **Soft clashes** (clearance violations, maintenance access issues) = performance regressions. The code runs, but not well enough. The beam clears the duct, but there is no room for a wrench.
- **Workflow clashes** (scheduling conflicts, procurement dependencies) = dependency violations. The code compiles, but the build order is wrong.

Studies consistently show 20% cost savings from systematic clash detection on large projects — the same order of magnitude that CI/CD delivers in software development. The mechanism is identical: catching errors at integration rather than at installation.

**BIM LOD vs. City101 LOI/LOG/LOD.** Standard BIM practice uses a single LOD (Level of Development) axis that conflates information and geometry — LOD 300 means both "accurately dimensioned geometry" and "sufficient information for coordination." City101's framework decouples them. LOI (information richness) stays high from the start because analysis needs rich data. LOG (geometric detail) starts low because iteration needs flexibility. LOD (design certainty) increases as decisions lock. The practical consequence: in City101, a station might have LOI 400 (full metadata: frequency, ridership, WiFi quality, acoustic data, opening hours, reviews) but LOG 100 (a dot on a map) and LOD 200 (we know something interesting happens here, but we have not designed anything). In standard BIM, that combination is inexpressible.

### Design Ops: the DevOps parallel

DevOps unified software development and operations into a continuous loop: code, build, test, deploy, monitor, feedback, code again. The architectural equivalent — call it Design Ops — would unify design and validation into a similar loop: design, model, check, present, evaluate, revise.

The pieces exist. Grasshopper already enables parametric design iteration. Speckle already enables version-controlled model sharing. BIMcollab already enables automated model checking. The QGIS MCP bridge already enables spatial validation. What is missing is the *integration* — the continuous pipeline where a design change automatically triggers clash detection, energy simulation, cost update, and visual validation, all before the designer's next decision.

City101's pipeline is a crude prototype of this. When the temporal frequency data changed (because the API limit parameter was discovered to be flattening results), the compute_wci.py script was rerun, which updated the WCI scores, which changed the map symbology, which altered the narrative. The pipeline was manual — a human triggered each step — but the dependency chain was explicit and reproducible.

---

## Section 4: Where Architecture Can Go Beyond Software

The transfer from software to architecture is not one-directional. Architecture has capabilities and requirements that push beyond what software workflows address. These are areas where architectural practice can lead, not follow.

### 4.1 Spatial reasoning as first-class capability

Software agents operate on text and code. Architectural agents must reason about space. The QGIS MCP and RhinoMCP bridges are early examples: agents that can query "how many workspaces are within 500m walking distance of this station?" or "does this building mass block the prevailing wind corridor?" These are not text operations — they are spatial operations that require understanding distance, adjacency, containment, visibility, and flow.

The frontier is agents that reason about spatial *experience*, not just spatial *data*. City101's finding that the Nyon-Gland gap is "19.3km — too far to walk, too short for a separate ticket" is a judgment about human experience that no current agent can make autonomously. It requires understanding that 19.3km is about 4 hours of walking, that a transit gap of this length breaks the experience of continuity, and that the pricing structure makes intermediate stops economically irrational. Current agents can compute the distance. They cannot yet feel the gap.

### 4.2 Blackboard architecture suits design better than supervisor

Software teams mostly use the supervisor pattern because it is controllable and predictable. Design work — particularly in early phases — suits the blackboard pattern better.

City101's `datasets/` directory already functions as a blackboard. Any agent can read any dataset. Cross-referencing produces emergent findings that no single agent was tasked with discovering. The correlation between religious Shannon diversity, modal Shannon diversity, cuisine Shannon diversity, and economic category diversity (r = 0.63-0.71) was not in any agent's task specification. It emerged from spatially joining datasets that were not designed to go together. The finding — diversity correlates with urban completeness, with a phase transition at Shannon approximately 1.0 — came from the blackboard, not from a supervisor's task decomposition.

This is why the LEARNINGS.md observation is so significant: "The most valuable insights came from spatially joining datasets that weren't designed to go together." A supervisor would need to anticipate which joins are productive. A blackboard lets agents discover them.

### 4.3 The multidimensional model as coordination medium

Software teams coordinate through APIs — well-defined interfaces between services. Architecture can coordinate through something richer: a shared spatial model that embeds geometry, time, cost, sustainability, and operations in a single queryable medium.

The BIM model is not just documentation. It is the coordination layer. When a structural change propagates through cost, schedule, energy, and maintenance simultaneously, the model is functioning as a real-time blackboard that all agents (human and AI) read from and write to. Software has nothing equivalent — there is no single artifact in a software project that embeds the codebase, the deployment topology, the performance characteristics, the cost model, and the user experience in one queryable structure.

This is architecture's advantage, if it can be operationalized. The nD BIM framework points the way, but current tools fragment the model across discipline-specific applications rather than exposing it as a unified agent-queryable workspace.

### 4.4 Temporal and experiential dimensions

Software optimizes for correctness: does the code do what the specification says? Architecture must reason about experience over time. The temporal WCI finding — that the corridor's archipelago pattern is structural, not temporal, with the number of workable stations barely changing across 7 time slots (14 at peak, 13 at 11pm) — has no software equivalent. It is a finding about *how a place feels at different hours*, derived from data but meaningful only through the lens of human experience.

The 42-fold frequency variation across the corridor (Lausanne at 28.5 trains per hour, St-Saphorin at 0.0) is not a bug to be fixed. It is a spatial condition that creates radically different experiences of the same infrastructure. A 2-minute wait at Lausanne means the train is part of your walking rhythm. A 37-minute wait at Bossiere means you need a chair, a coffee, and WiFi — you need architecture.

Agents that can reason about temporal experience — not just temporal data — would be genuinely new. The gap between "this station has 2.0 trains per hour" and "this station creates a 30-minute program that demands spatial design" is where architecture's disciplinary knowledge becomes irreplaceable.

### 4.5 The design-certainty gradient

Software ships or it does not. A feature is either in production or it is not. Architecture evolves through a continuous gradient of certainty — from speculative sketch to coordinated documentation to construction detail. The LOI/LOG/LOD framework formalizes this gradient, and it has direct implications for how agents should allocate effort.

In early phases (high LOI, low LOG, low LOD), agents should maximize data collection and minimize geometric commitment. "Work rich, export lean." In late phases (high LOI, high LOG, high LOD), agents should focus on coordination and clash detection. The anti-pattern — deploying high-LOG agents in low-LOD phases — produces beautiful renderings of undecided designs. "Looks done but isn't."

This gradient does not exist in software, where the equivalent would be code that compiles but whose architectural decisions have not been made. Software has a word for this: prototype. But software prototypes are disposable. Architectural prototypes (massing studies, site models, spatial diagrams) accumulate into the design. The certainty gradient is not about discarding early work but about progressively committing to it.

### 4.6 Narrative as integration layer

City101's most significant outputs are not datasets. They are arguments. "5 break dimensions" led to "archipelago" which led to "two corridors on the same tracks" which led to "160,000 ghost citizens." No single agent produced this narrative arc. It emerged from accumulated evidence across sessions, accounts, and analytical dimensions.

The narrative is the integration layer that makes individual findings cohere into a design argument. Software has nothing equivalent — there is no "narrative" layer in a microservices architecture that explains why the services are organized the way they are. (Architecture Decision Records come closest, but they document decisions, not arguments.)

For architecture, the implication is that agentic workflows need a synthesis step that is fundamentally different from software's integration testing. It is not enough to verify that all datasets are schema-compliant and spatially valid. Someone — human or agent — must ask: "What do these findings *mean* for the design?" That question requires disciplinary judgment, theoretical frameworks (Comtesse's diversity formula, Deleuze's significance of surface), and the ability to move between scales and dimensions. It is the hardest part of the workflow to systematize, and arguably the part that should remain human longest.

---

## Conclusion: Practical Recommendations

### For agents

**1. Start with the data contract, not the agent.** Before spawning any agent, define the canonical entity list, the output schema, the coordinate validation ranges, and the join keys. City101's 49-station list with exact names and coordinates made everything downstream possible. Without it, no cross-referencing works.

**2. Use 2-3 focused agents, not 5-7 narrow ones.** Coordination cost scales quadratically with team size. A single agent that can cross-reference its own findings is more valuable than two agents that cannot talk to each other. The City101 research protocol is explicit: "Prefer fewer, broader agents over many narrow ones."

**3. Build living state files.** CONTEXT.md (what exists), LEARNINGS.md (what to avoid), and a governance document (CLAUDE.md or equivalent) that any agent reads at session start. These files survive across sessions, across accounts, and across humans. They are the institutional memory that makes agentic work cumulative rather than repetitive.

**4. Stage and verify before promoting.** Agents write to a staging area. A verification pass — programmatic (coordinate ranges, schema compliance, null checks) and spatial (does this place correctly on a map?) — gates promotion to production. Nothing enters the canonical datasets unverified. This is the single most important practice for maintaining data integrity in multi-agent workflows.

**5. Let the workflow emerge from the question.** City101 did not start with an "AI workflow design phase." It started with a question — does this corridor function as one city? — and the workflow emerged from the demands of answering that question rigorously. The best agent workflows are discovered, not designed. Build what you need, when you need it, and formalize only what proves useful across multiple sessions.

### For collaboration

**6. Adopt object-level version control for geometry.** Speckle and similar platforms let you track changes to individual design elements, branch for alternatives, and merge when decisions converge. File-level versioning (_v2, _v3 suffixes) does not scale. Object-level versioning does.

**7. Write a design governance file.** The equivalent of AGENTS.md for a design project: which agents or team members can modify which parts of the model, what review gates exist, what naming conventions apply. City101's CLAUDE.md is nearly 400 lines — substantial for a studio project, but the principle of explicit governance is sound.

**8. Tie versions to design decisions, not dates.** Software branches are named for features, not calendar dates: `feature/new-login` not `branch-march-5`. Design versions should similarly tie to decisions: "massing-option-B" not "v3." This makes the version history legible and the design rationale traceable.

**9. Use co-author attribution for AI contributions.** When an agent produces a dataset, a script, or an analysis, attribute it. City101's CONTEXT.md tracks which account produced which dataset ("NEW S8 (Lumen)" vs "NEW Cairn S9"). This is not formality — it is traceability. When a downstream error is found, you need to know which agent's output to re-verify.

### For BIM integration

**10. Treat the model as queryable data, not just documentation.** A BIM model that can only be viewed is a drawing. A BIM model that can be queried ("show me all spaces with less than 300 lux at 3pm in December") is an analytical tool. MCP4IFC and similar bridges make this possible — agents that can ask questions of the model and receive structured answers.

**11. Assign agents to BIM dimensions.** Each nD dimension (3D geometry, 4D schedule, 5D cost, 6D sustainability, 7D operations) is a natural agent specialization. Structural agents reason about load paths. Energy agents reason about thermal performance. Cost agents track quantity takeoffs. The model is the shared blackboard; the dimensions are the agent roles. Conflicts between dimensions — the structural solution that breaks the energy target — surface automatically through the shared model, just as conflicts between datasets surfaced in City101 through spatial cross-referencing.

**12. Use clash detection as continuous integration.** Every model change should trigger automated checks: hard clashes, soft clashes, code compliance, performance targets. Arup's Tekla-Grasshopper workflow at King's Cross demonstrates this at production scale. The BCF (BIM Collaboration Format) standard from buildingSMART provides a structured format for issue tracking — the architectural equivalent of GitHub Issues.

---

## References

### Firm case studies
- Heatherwick Studio Ge-Code team — constructionmanagement.co.uk
- ZHA + NVIDIA Omniverse — wallpaper.com
- Arup King's Cross R8 Tekla-Grasshopper — tekla.com, csengineermag.com
- IAAC HyperBuilding — blog.iaac.net
- Speckle + Arup — speckle.systems/customer-stories

### Tools and platforms
- Vectorworks Text2BIM — ASCE Journal of Computing in Civil Engineering, Vol. 40, No. 2, March 2026
- RhinoMCP — discourse.mcneel.com
- QGIS MCP — github.com/jjsantos01/qgis_mcp
- Autodesk Forma — autodesk.com
- Speckle — speckle.systems
- BIMcollab — bimcollab.com
- buildingSMART IFC — ISO 16739-1:2024

### Academic
- Pantazis (2024), *Designing with Multi-Agent Systems*, De Gruyter
- MCP4IFC — arxiv 2511.05533
- "GIS Copilot: towards an autonomous GIS agent for spatial analysis" (2025)
- buildingSMART BCF (BIM Collaboration Format)

### Conferences
- ACADIA 2024: "Designing Change"
- eCAADe 2024: "Data-Driven Intelligence"
- Autodesk University 2025

### Research institutions
- ICD Stuttgart (UniStuttgart-ICD on GitHub)
- Gramazio Kohler Research, ETH Zurich
- MIT Media Lab
- DesignMorphine

### City101 project files
- `CLAUDE.md` — project governance and conventions
- `CONTEXT.md` — living project state
- `LEARNINGS.md` — accumulated insights and pitfalls
- `TODO_4_POINTS.md` — investigation decomposition framework
- `00_Workflow_v04.md` — LOI/LOG/LOD framework
- `.claude/commands/research-with-agent-team.md` — agent team coordination protocol
- `handoffs/` — 20 session handoff files (S1-S11 + sub-sessions)
- `scripts/` — 8 monolithic Python scripts
- `datasets/` — production data (49-station crossref, WCI, temporal, modal, GA cost, ridership, etc.)
