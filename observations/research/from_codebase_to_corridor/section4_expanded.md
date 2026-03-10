# Section 4: Where Architecture Can Go Beyond Software (Expanded)

The transfer from software to architecture is not one-directional. Architecture has capabilities and requirements that push beyond what software workflows address. These are areas where architectural practice can lead, not follow. What follows grounds each claim in specific tools, projects, and publications.

---

## 4.1 Spatial Reasoning as First-Class Capability

Software agents operate on text and code. Architectural agents must reason about space — distance, adjacency, containment, visibility, flow. This is not a matter of adding a spatial library to a text-processing pipeline. It requires fundamentally different computational substrates.

### COMPAS: Spatial Assembly as Irreducible Computation

The COMPAS framework, developed by the Block Research Group at ETH Zurich with major contributions from Gramazio Kohler Research, is an open-source Python-based computational framework for architecture, structural engineering, and digital fabrication (compas.dev). Its significance for this argument lies in what it computes that has no text or code equivalent.

COMPAS FAB (Fabrication), the robotic fabrication package, formulates architectural assembly as a *planning scene* — a data structure that defines robots, tools, spatial constraints, and collision objects simultaneously (Huang et al., "Automated sequence and motion planning for robotic spatial extrusion of 3D trusses," *Construction Robotics*, 2018). The planner must solve two interlocked problems: *task planning* (the order of discrete assembly steps) and *motion planning* (continuous trajectories through 3D space that avoid collisions). These are spatial queries — "can this beam be placed without colliding with already-placed beams, and does a feasible robot arm path exist to reach this position?" — that cannot be expressed as text diffs, unit tests, or API calls. They require reasoning about 3D occupancy, kinematic reachability, and assembly sequence dependencies simultaneously.

The compas_fab_choreo workshop materials (GitHub: yijiangh/compas_fab_choreo_workshop) demonstrate sequence and motion planning using Choreo as the planning engine, where the spatial constraints include limited workspace, safe operation distances, and proper component placement. A hierarchical planning framework decouples sequence from motion, solving extrusion sequence, end-effector poses, joint configurations, and transition trajectories for spatial trusses with nonstandard topologies. The validation comes from robotically executing and constructing large-scale real-world timber structures — a test that has no software analogy because the "deployment environment" is physical space.

### ICD Stuttgart: Agent-Based Spatial Intelligence

The Institute for Computational Design and Construction (ICD) at the University of Stuttgart, under Achim Menges, has developed agent-based modeling (ABM) as a core research area for architectural design (icd.uni-stuttgart.de/research/research-areas/agent-based-modeling/). Their approach endows the constituent units of an architectural system with *decision-making agency*: individual agents (representing building components, fabrication constraints, or spatial conditions) exhibit distinct behaviors that encapsulate low-level design intentions, interact with one another, and interact with their environment.

This is qualitatively different from software agents coordinating through APIs. ICD's agents reason about material behavior, fabrication feasibility, and structural performance simultaneously. Leder and Menges developed Agent-Based Models for a Modular Collective Robotic Construction System (2025), while related work explores augmenting heuristic behaviors with reinforcement learning in collective robotic construction (2024). The Cyber-Physical Wood Fabrication Platform project (IntCDC Research Project RP-4) establishes continuous feedback loops connecting initial design through to online fabrication adaptation — agents that sense physical reality and modify spatial plans in real time.

A systematic literature review by ICD researchers ("Agent-based modeling and simulation in architecture," 2022) classifies ABM applications in architecture by the entities being modeled, demonstrating that over the last two decades, ABM use has increased significantly. The particular relevance to architecture lies in ABM's ability to integrate many potentially conflicting design criteria — structural constraints, fabrication limits, environmental performance — by distributing decision-making across spatially embedded agents rather than centralizing it in a supervisor.

### Rhino.Compute: Spatial Operations as API

McNeel's compute.rhino3d (GitHub: mcneel/compute.rhino3d) exposes RhinoCommon — the full geometry kernel behind Rhino — as a stateless REST API. It runs headless, without a user interface, processing spatial operations through HTTP requests. The API supports Boolean operations on solids, surface intersections, mesh analysis, curve evaluations, and Grasshopper definition execution — operations that are irreducibly spatial.

The significance is architectural: compute.rhino3d makes it possible for an agent to ask "does this building mass intersect the setback envelope?" or "what is the solar exposure of this facade surface?" without requiring a human to open Rhino and visually inspect the result. ShapeDiver builds on this to deliver parametric design evaluation at scale. But the queries themselves — intersection, containment, distance, visibility — are not text operations with spatial metadata attached. They are spatial operations that happen to be invoked through text protocols.

### The Gap: Experience vs. Data

City101's finding that the Nyon-Gland gap is "19.3km — too far to walk, too short for a separate ticket" illustrates what current spatial tools cannot yet do. COMPAS can plan an assembly sequence. Rhino.Compute can measure a distance. ICD's agents can negotiate structural and fabrication constraints. But none can yet judge that 19.3km *breaks the experience of continuity* — that it is simultaneously too long for pedestrian connection and too short to justify a separate transit fare, creating an economically irrational gap. This judgment requires understanding human spatial experience, not just spatial geometry.

---

## 4.2 Blackboard Architecture Suits Design Better Than Supervisor

Software teams frequently default to the supervisor pattern because it is controllable and predictable. Design work — particularly in early phases — suits the blackboard pattern better. Three platforms demonstrate why.

### NVIDIA Omniverse: USD as Shared Blackboard

NVIDIA Omniverse is built on OpenUSD (Universal Scene Description), the open-source 3D composition framework originally developed by Pixar. USD's architecture is explicitly designed for multiple simultaneous writers working on a shared scene — a blackboard in the precise technical sense.

USD's `subLayers` composition arc allows multiple artists or agents to work in their own files (layers), all of which are combined through a "strength ordering" specified in the USD files themselves (openusd.org/dev/usdfaq.html). The composition engine resolves layered contributions similarly to Photoshop layers — each layer can add, modify, or override data from layers below it, without destructive edits. The LIVRPS strength ordering (Local, Inherits, VariantSets, References, Payloads, Specializes) provides a canonical resolution for conflicting opinions across all composition arcs (openusd.org/dev/glossary.html).

This is fundamentally different from software's API-mediated coordination. In a microservices architecture, Service A calls Service B through a defined interface — the contract specifies what data crosses the boundary. In USD's blackboard, multiple contributors write to the *same scene description* simultaneously. A structural engineer modifying load-bearing elements and an architect adjusting spatial layout both write layers that compose into a single resolved scene. Conflicts are resolved by the composition engine's strength ordering, not by API contracts.

Foster + Partners has implemented Omniverse to enable collaborative design across teams in 14 countries (fosterandpartners.com, 2021). Multiple design changes can be visualized simultaneously in real time, allowing design options to be reviewed in parallel — a workflow impossible in API-mediated systems where each service owns its data exclusively. The firm reports that the "vast reduction in time previously required for processing models means more time for creative design and visualisation."

For agentic workflows, the implication is direct: analysis agents (structural, energy, daylighting, wind) can each write their findings as USD layers to a shared scene. The composition engine handles integration. No supervisor needs to route data between agents because the shared scene *is* the coordination medium.

### Bentley iTwin: The Queryable Blackboard

Bentley's iTwin platform takes the blackboard concept further by making the shared model *queryable*. An iTwin integrates engineering data from diverse design tools — MicroStation, Aveva, Revit — into a unified digital twin using Base Infrastructure Schemas (BIS) that standardize disparate formats (developer.bentley.com).

iTwin Experience functions as a "single pane of glass" overlaying engineering technology (ET), operations technology (OT), and information technology (IT) — the model is geo-coordinated, fully searchable, and queryable at any level of granularity (bentley.com/software/itwin/). In 2025-26, Bentley unveiled an AI ecosystem of specialized agents for site-grading optimization, hydraulic calculations, drawing automation, data discovery, and coding assistance (AEC Magazine, 2025). CEO Nicholas Cumins cited a geothermal energy project in Turkey where AI agents evaluated over 10 million scenarios in days, compressing a five-year development timeline into one year (engineering.com, 2025).

The architectural significance: iTwin is not just a shared workspace — it is a shared workspace that agents can *query*. An energy agent can ask "what is the U-value of every exterior wall on the north facade?" and receive structured answers from the same model that the structural agent reads for load paths. Software has nothing equivalent — there is no single queryable artifact in a software project that embeds codebase, deployment topology, performance, cost, and user experience.

### Why Blackboard Suits Design

City101's `datasets/` directory already functions as a crude blackboard. The correlation between religious Shannon diversity, modal Shannon diversity, cuisine Shannon diversity, and economic category diversity (r = 0.63-0.71) was not in any agent's task specification. It emerged from spatially joining datasets produced independently. A supervisor would need to anticipate which joins are productive. The blackboard — whether City101's filesystem, Omniverse's USD scene, or iTwin's queryable model — lets agents discover productive combinations without centralized planning.

---

## 4.3 The Multidimensional Model as Coordination Medium

### Beyond API Contracts: The Model as Integration Layer

Software teams coordinate through APIs — well-defined interfaces between services. Each service owns its data; contracts specify what crosses boundaries. Architecture can coordinate through something richer: a shared spatial model that embeds geometry, time, cost, sustainability, and operations in a single medium.

The nD BIM framework assigns each dimension a natural agent specialization (3D geometry, 4D scheduling, 5D cost, 6D sustainability, 7D operations). But current tools fragment the model across discipline-specific applications. Omniverse, iTwin, and Autodesk Tandem represent three different strategies for unifying it.

### Autodesk Tandem: Operations as Model Dimension

Autodesk Tandem extends the BIM model into operations by creating digital twins that connect design data with real-time sensor data, IoT platforms, and building management systems (intandem.autodesk.com). The platform's "trend analysis" capability identifies potential future problems based on current performance patterns, enabling preventive maintenance — the model is not just documentation but a *predictive* coordination medium.

Tandem compiles facility data from every connected asset and system, pulling from BMS, CMMS, IoT platforms, and BIM tools to create a unified spatial and telemetric layer (AEC Magazine, 2025). This is the 7D BIM dimension (facilities management) made concrete: an agent reasoning about operational performance reads from the same model that design agents wrote during project delivery.

### Autodesk Forma: Parallel Analysis as Model Feature

Autodesk Forma (formerly Spacemaker) embeds AI agents that run parallel evaluations — noise analysis, wind simulation, daylight assessment — on site designs simultaneously. The platform's generative design tools propose numerous layout variants based on user-defined parameters, then filter them using ML-powered analyses that provide near-instantaneous predictions comparable in accuracy to full-scale simulations (autodesk.com/products/forma).

The coordination medium is the site model itself. When a user adjusts building massing, all analyses update because all agents read from the same spatial representation. No API contracts mediate between the wind agent and the daylight agent — they share the model. This is the blackboard pattern applied to environmental analysis, and it produces a workflow impossible in software's service-oriented architecture: simultaneous multi-criteria evaluation of spatial configurations.

---

## 4.4 Temporal and Experiential Dimensions

Software optimizes for correctness: does the code do what the specification says? Architecture must reason about experience over time — how a place feels at different hours, how dwell time creates spatial programs, how frequency shapes behavioral rhythms. Three methodological traditions offer frameworks for encoding this temporal-experiential dimension computationally.

### Jan Gehl's Public Life Studies: Structured Observation of Temporal Experience

Jan Gehl and Birgitte Svarre's *How to Study Public Life* (2013) codifies five decades of systematic observation into a methodology with four core techniques: *counting* (quantitative tallies of people by mode, direction, and time), *mapping* (plotting activity locations and types), *tracing* (drawing movement paths within a space), and *tracking* (following individuals to observe behavioral choices). These are supplemented by photography, diary-keeping, and test walks.

The critical insight for agentic workflows: Gehl distinguishes *necessary activities* (functional, weather-independent), *optional activities* (recreational, highly dependent on spatial quality), and *social activities* (emergent from the presence of others). The ratio between these categories at different times of day is a measure of spatial quality that no geometric analysis can produce. A station platform at 8am (all necessary activities — commuters rushing) is a fundamentally different space than the same platform at 11pm (optional activities absent, social activities absent — the space has failed).

The Gehl Institute formalized this into the Public Life Data Protocol (PLDP), an open data specification developed jointly with the City of Copenhagen, San Francisco, and Seattle DOT (github.com/gehl-institute/pldp). The Protocol includes over 80 ways to note who and how space is occupied at any given moment, with guidelines for observing the same places at different days, times, and weather conditions. It "elevates people-watching into a rigorous research method."

City101's temporal WCI analysis — finding that the corridor's archipelago pattern is structural, not temporal, with workable stations barely changing across 7 time slots — is a computational version of Gehl's temporal observation. The 42-fold frequency variation (Lausanne at 28.5 trains/hr, St-Saphorin at 0.0) is not a bug to fix but a spatial condition that creates radically different experiences of the same infrastructure. A 2-minute wait at Lausanne means the train is part of your walking rhythm. A 37-minute wait at Bossiere means you need a chair, coffee, and WiFi — you need *architecture*.

### Space Syntax: Morphological Predictors of Temporal Flow

Space Syntax, developed by Bill Hillier and Julienne Hanson at UCL, provides a computational framework for relating spatial configuration to movement patterns. The core claim: street network centrality (measured as integration and choice values) predicts pedestrian volumes. Lerman et al. ("Using Space Syntax to Model Pedestrian Movement in Urban Transportation Planning," *Geographical Analysis*, 2014) showed that Multiple Regression Analysis models using spatial variables as independent variables and observed pedestrian volumes as the dependent variable can explain pedestrian distribution primarily through network configuration.

For temporal analysis, Space Syntax movement observation operates in standardized time periods: 8am-10am, 10am-12pm, 12pm-2pm, 2pm-4pm, 4pm-6pm (spacesyntax.online). Agent-based extensions (Raford and Ragland, "Using space syntax and agent-based approaches for modeling pedestrian volume at the urban scale," *Computers, Environment and Urban Systems*, 2017) add a dynamic dimension, modeling how flows change over time as a function of both network configuration and land use attractors.

Recent work has begun bridging Gehl and Space Syntax computationally. He Kanxuan's computer vision framework operationalizes Gehl's PSPL (Public Space Public Life) methodology using webcam data to track walk and stay behaviors at scale, investigating associations with public space features including point of interest density, facade quality, and street furniture (ResearchGate, 2024). This represents the beginning of automated temporal-experiential analysis — agents that can observe how a space is *used*, not just how it is *configured*.

### Computational Phenomenology: Time Makes Space

A neuroscience finding with architectural implications: Sorscher et al. ("Time Makes Space: Emergence of Place Fields in Networks Encoding Temporally Continuous Sensory Experiences," *eLife*, 2024, arxiv:2408.05798) demonstrated that spatial representations emerge from temporal encoding in neural networks. When autoencoders are trained to pattern-complete sensory experiences with activity constraints, spatially localized firing fields (place cells) emerge — the network learns spatial structure from the temporal continuity of traversal.

The architectural translation: the experience of a corridor is not a sequence of spatial snapshots but a continuous temporal unfolding. City101's finding that the Nyon-Gland gap "breaks continuity" is a phenomenological claim — it says something about the *experience* of traversal, not just the metric distance. Current computational frameworks (COMPAS, Space Syntax, Forma) can model static spatial properties. Frameworks that encode temporal experience — the rhythm of stops, the duration of waits, the quality of in-between time — remain largely unbuilt. This is where architecture's disciplinary knowledge about human spatial experience becomes irreplaceable.

---

## 4.5 The Design-Certainty Gradient

Software ships or it does not. A feature is in production or it is not. Architecture evolves through a continuous gradient of certainty — from speculative sketch to coordinated documentation to construction detail. The tools that manage this gradient are beginning to formalize what City101's LOI/LOG/LOD framework proposes.

### ISO 19650: The Standards Catching Up

The international BIM standard ISO 19650 (replacing UK's PAS 1192) introduced the concept of *Level of Information Need* (LOIN), which explicitly separates geometric information, alphanumeric information, and documentation requirements (ISO 19650-1:2018). This is the standards world catching up to what City101's framework proposes: that information richness (LOI), geometric detail (LOG), and design certainty (LOD) are independent axes.

Under PAS 1192-2, UK practice already differentiated LOD (Level of Detail — graphical) from LOI (Level of Information — non-graphical), allowing a facade to be LOD 4 but LOI 2 depending on the project phase (rvtparametrix.co.uk). ISO 19650's LOIN goes further by requiring consideration of *what the model information will be used for* — the purpose determines the required granularity, not a blanket LOD specification. The Danish method, built on the principle of "evolving detailing," has each party add information at progressively higher levels through the process (thenbs.com).

The anti-pattern identified in City101's 00_Workflow_v04.md — "High LOG + Low LOI + Low LOD: Pretty render, no data, design not locked. Dangerous — looks done but isn't" — has a standards equivalent: ISO 19650 warns against delivering "too much information" (which is wasteful and overloads systems) as well as too little (which increases risk). The right level of information need is defined *per exchange*, not globally.

### Speckle: Object-Level Version Control with Branching

Speckle (speckle.systems) provides what the certainty gradient needs at the tool level: object-level version control with branching for design alternatives. Speckle is "the Git & Hub for geometry and BIM data" — it decomposes 3D data into atomic parts, hashes them, and stores them in a versioned object graph (speckle.guide/user/concepts.html).

Branches give an extra layer of organization within a stream, and users frequently use them for parallel design studies and options. All streams start with a `main` branch; additional branches allow working on multiple versions in parallel — high-certainty elements on `main`, speculative alternatives on feature branches. The visual diff capability lets users compare any two versions with one click, seeing exactly what was added, removed, changed, or stayed the same (docs.speckle.systems/3d-viewer/compare-versions).

Federation Models (formerly branches) are now infinitely nestable, allowing grouping and subgrouping of model collections. This maps directly to the certainty gradient: structural elements at LOD 400 live in a high-certainty branch; facade options being explored at LOD 200 live in speculative branches; all share the same LOI-rich data foundation.

### Forma: Certainty Through Evaluation

Autodesk Forma's design option workflow embodies the certainty gradient operationally. Site Automation generates multiple layout variants from user-defined parameters. AI-powered analyses (wind, noise, daylight) evaluate each variant near-instantaneously. Users filter options based on performance criteria until they have a selection of viable designs to develop further (autodesk.com/products/forma).

This is the certainty gradient made computational: many options at low certainty (generated variants), progressive filtering through analysis (increasing certainty), convergence on a small set for detailed development (high certainty). The LOI remains high throughout — every variant carries the same environmental analysis data. The LOG increases only for surviving options. The LOD increases as design decisions lock.

---

## 4.6 Narrative as Integration Layer

City101's most significant outputs are not datasets but arguments. "5 break dimensions" led to "archipelago" which led to "two corridors on the same tracks" which led to "160,000 ghost citizens." No single agent produced this narrative arc. The question is whether the "why" of design can be structured alongside the "what" — and whether doing so changes how agents contribute to design.

### Rittel's IBIS: The Original Design Argumentation System

The Issue-Based Information System (IBIS), developed by Werner Kunz and Horst Rittel at UC Berkeley in the 1960s-70s, was created specifically for the kind of reasoning architecture requires. Kunz and Rittel described IBIS as "meant to support coordination and planning of political decision processes" — recognizing that design is argumentation, not optimization (Kunz and Rittel, "Issues as Elements of Information Systems," Working Paper 131, 1970).

IBIS structures discourse through three elements: *Issues* (questions to be resolved), *Positions* (possible answers), and *Arguments* (evidence supporting or opposing positions). The framework was designed for *wicked problems* — problems where the formulation of the problem is itself part of the problem, where there is no definitive solution, and where every intervention changes the problem space. Architecture, as Rittel explicitly argued, is the paradigmatic wicked problem domain.

The tool lineage from IBIS is instructive. gIBIS (Conklin and Begeman, 1988) was the first graphical hypertext IBIS implementation. PHIBIS (McCall, 1983) added procedural hierarchy. Compendium, the open-source descendant, provided a visual environment for mapping ideas and arguments using IBIS notation with hypertext links and database interoperability (compendium.open.ac.uk). Compendium's ten node types — question, answer, pro, con, note, decision, reference, argument, list view, map view — represent a mature vocabulary for design reasoning.

### D-Agree: AI-Facilitated Argumentation

D-Agree, developed at Nagoya Institute of Technology and Kyoto University, represents the state of the art in AI-facilitated argumentation using IBIS structure (presented at AAAI-20). The system hosts web-based discussions where an AI facilitation agent automatically extracts discussion structure from posted text, labels contributions according to IBIS categories (issue, position, argument), and drives discussions toward group consensus. D-Agree extends the earlier COLLAGREE system by replacing human facilitators with AI agents (Ito et al., 2020).

The architectural implication: if AI can extract IBIS structure from unstructured discussion, it can potentially extract design rationale from design reviews, crit sessions, and team conversations. The gap between "we discussed the facade options" and "the south facade uses perforated panels because: (Position) they reduce solar gain by 40%, (Argument-Pro) they maintain views to the lake, (Argument-Con) they increase embodied carbon by 15%, (Decision) accepted because thermal performance outweighs carbon cost at this latitude" is exactly the gap between undocumented design and structured design rationale.

### Architecture Decision Records: Software's Closest Analog

Software engineering's Architecture Decision Records (ADRs) are the nearest equivalent to structured design rationale (adr.github.io). An ADR captures a single decision along with its context, alternatives considered, and consequences. The format forces explicit documentation of *why* — preventing what practitioners call "decision amnesia" where teams revisit settled debates because no one remembers the reasoning.

The MADR (Markdown Any Decision Record) template includes: Title, Status, Context, Decision, Consequences. AWS's prescriptive guidance adds: Assumptions, Constraints, Positions Considered, Arguments For/Against each position (docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/). This is IBIS in all but name — issues (context), positions (alternatives), arguments (pros/cons), and a recorded decision.

But ADRs document *discrete decisions*. Architecture's narrative layer is something different — it is the *argument that connects decisions into a coherent whole*. City101's narrative arc is not a collection of independent decisions. It is a sustained argument: the corridor appears continuous but functions as an archipelago; the archipelago pattern is structural, not temporal; the structural cause is a combination of frequency, pricing, workspace, and connectivity gaps; the 160,000 frontaliers who disappear at 18:00 are the human consequence. Each finding depends on the previous; the narrative is the integration.

### What Would Computational Narrative Look Like?

No current tool captures design narrative computationally. IBIS captures argumentation structure. ADRs capture decision rationale. BIM captures spatial and performance data. But the layer that says "these three findings, from independent analyses, converge to mean *this* for the design" — that synthesis remains human work.

City101's CONTEXT.md is a primitive version: a living document updated each session with findings, patterns, and open questions. LEARNINGS.md accumulates pitfalls. The handoff files trace how understanding evolved across sessions. Together they form a traceable narrative, but one expressed in natural language, not in structured data.

The research frontier is tools that formalize this layer — where the connection between a Shannon diversity analysis, a temporal frequency map, and a GA pricing model is not just spatially coincident (all three show the same gap at Lavaux) but argumentatively linked (the diversity deficit *follows from* the frequency gap, which *follows from* the pricing structure, which *produces* the invisible population). Agent systems that can traverse these argumentative links — not just produce individual analyses but trace their implications through a design argument — would represent a genuinely new capability. Rittel's IBIS, extended with spatial data and temporal evidence, points the direction. The tools do not yet exist.

---

## Summary: Five Capabilities Beyond Software

| Capability | Software Equivalent | Architecture's Extension | Enabling Tools |
|-----------|---------------------|------------------------|----------------|
| Spatial reasoning | Text/code operations | 3D occupancy, assembly feasibility, kinematic reachability | COMPAS FAB, Rhino.Compute, ICD ABM |
| Blackboard coordination | API contracts between services | Shared spatial model with simultaneous multi-agent writing | Omniverse/USD, Bentley iTwin, Autodesk Tandem |
| Multidimensional model | Separate databases per service | Single queryable artifact embedding geometry + time + cost + performance | nD BIM, Forma parallel analysis, iTwin Cloud Connect |
| Temporal-experiential reasoning | Correctness testing | How space feels across time, dwell-time as spatial program | Gehl PLDP, Space Syntax temporal observation, City101 temporal WCI |
| Narrative integration | ADRs (discrete decisions) | Sustained design argument connecting independent findings | IBIS/Compendium, D-Agree, CONTEXT.md as primitive prototype |

Each of these capabilities exists in embryonic form. None is fully realized. The gap between "agents that compute spatial metrics" and "agents that reason about spatial experience" defines the research frontier for agentic workflows in architecture.

---

## References for Section 4

### Spatial Reasoning
- COMPAS framework: compas.dev; Block Research Group, ETH Zurich
- COMPAS FAB: github.com/compas-dev/compas_fab
- Huang et al., "Automated sequence and motion planning for robotic spatial extrusion of 3D trusses," *Construction Robotics*, 2018
- compas_fab_choreo workshop: github.com/yijiangh/compas_fab_choreo_workshop
- ICD Stuttgart, Agent-Based Modeling research area: icd.uni-stuttgart.de/research/research-areas/agent-based-modeling/
- ICD Stuttgart, "Agent-based modeling and simulation in architecture," 2022
- Leder and Menges, "Agent-Based Models for a Modular Collective Robotic Construction System," 2025
- IntCDC Cyber-Physical Wood Fabrication Platform (RP-4): intcdc.uni-stuttgart.de
- McNeel compute.rhino3d: github.com/mcneel/compute.rhino3d; rhino3d.com/compute

### Blackboard and Digital Twin Platforms
- NVIDIA Omniverse: nvidia.com/en-us/omniverse/
- OpenUSD specification: openusd.org/dev/usdfaq.html; openusd.org/dev/glossary.html
- Foster + Partners Omniverse collaboration: fosterandpartners.com/news (2021)
- Bentley iTwin Platform: developer.bentley.com; bentley.com/software/itwin/
- Bentley AI agents ecosystem: AEC Magazine, "Bentley Systems shapes its AI future," 2025; engineering.com, "Bentley bets big on AI for infrastructure," 2025
- Autodesk Tandem: intandem.autodesk.com; AEC Magazine, "Autodesk Tandem in 2025," 2025

### Temporal-Experiential Reasoning
- Gehl, Jan and Svarre, Birgitte, *How to Study Public Life*, Island Press, 2013
- Gehl Institute, Public Life Data Protocol: github.com/gehl-institute/pldp
- He Kanxuan, "Revisiting Gehl's urban design principles with computer vision and webcam data," ResearchGate, 2024
- Lerman et al., "Using Space Syntax to Model Pedestrian Movement in Urban Transportation Planning," *Geographical Analysis*, 2014
- Raford and Ragland, "Using space syntax and agent-based approaches for modeling pedestrian volume at the urban scale," *Computers, Environment and Urban Systems*, 2017
- Space Syntax Online Training Platform: spacesyntax.online
- Sorscher et al., "Time Makes Space: Emergence of Place Fields in Networks Encoding Temporally Continuous Sensory Experiences," *eLife*, 2024 (arxiv:2408.05798)

### Certainty Gradient
- ISO 19650-1:2018, Organization and digitization of information about buildings and civil engineering works
- UK PAS 1192-2 (superseded by ISO 19650)
- NBS, "Level of detail LOD and digital plans of work": thenbs.com
- Speckle core concepts: speckle.guide/user/concepts.html
- Speckle version comparison: docs.speckle.systems/3d-viewer/compare-versions
- Autodesk Forma: autodesk.com/products/forma

### Narrative and Design Rationale
- Kunz, Werner and Rittel, Horst W.J., "Issues as Elements of Information Systems," Working Paper 131, UC Berkeley, 1970
- Conklin, Jeff and Begeman, Michael, "gIBIS: A Hypertext Tool for Exploratory Policy Discussion," *CSCW '88*, 1988
- Compendium software: compendium.open.ac.uk (open-source, LGPL)
- Ito et al., "D-Agree: Crowd Discussion Support System Based on Automated Facilitation Agent," AAAI-20, 2020
- Architecture Decision Records: adr.github.io
- MADR (Markdown Any Decision Records): adr.github.io/madr/
- AWS, "ADR process," Prescriptive Guidance: docs.aws.amazon.com
