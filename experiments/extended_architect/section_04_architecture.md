# 4. The Architecture: How It Works

§5 describes the logic — three systems (knowledge, organization, infrastructure) that make the extended architect operational. This section describes the mechanics: how each system is built, what it handles well, and where its limits are.

## 4.1 The knowledge system: what agents know

An agent without domain knowledge is a generalist with access to a geometry engine. It can produce walls, columns, slabs — but it cannot tell you whether a rammed earth wall at 500mm thickness will survive its first winter in Vaud, or whether the structural grid you drew requires a transfer beam at that span. Domain knowledge is what turns a geometry agent into a structural agent, a buildability agent, a sustainability agent.

The problem is that domain knowledge comes in different shapes. The GWP of rammed earth is a number in a table. The typological precedent for courtyard housing is a narrative with spatial diagrams. The construction sequence for pisé formwork is an encyclopedia entry with illustrations. The structural limit for a height-to-thickness ratio is a rule that should prevent a wall from being built wrong. No single storage format handles all of these.

Four knowledge layers, each optimized for a different content shape:

**Layer 1 — Structured database (SQLite).** Tabular, quantitative, joinable data. The KBOB database (608KB, freely available) provides embodied energy, GWP, and UBP for Swiss construction materials — the numbers a sustainability agent needs to compare rammed earth against concrete. SIA span tables give a structural agent the maximum beam span for a given timber section. VKF fire tables tell a compliance agent the REI requirement for a party wall by use type and building height. Steel section profiles (HEA/HEB/IPE) give dimensions, weights, and moments of inertia.

An agent queries this layer with SQL:

```sql
SELECT material, gwp_kgco2_per_m3, source_version
FROM materials WHERE material = 'rammed_earth';
```

The answer is deterministic, authoritative, and fast. The database is a derived artifact — rebuilt from source files (Excel, CSV) that live in git. When KBOB publishes a new version, the source file is updated and the database is regenerated.

**Layer 2 — File tree (Markdown).** Curated narrative knowledge: typological descriptions, design precedents, construction guidelines, material behavior in prose. A timber agent reading about Lacaton & Vassal's housing strategies gets context that no database row can provide — the spatial logic of the double-height winter garden, the relationship between structure and envelope, the economic argument for generous volume over expensive finishes.

Each file is self-contained, under 3,000 tokens. Directories have routing tables (README files) that tell an agent which files are relevant to its current task. The access pattern is a cascade: agent reads branch README → selects specific file → reads it → acts. Simple, deterministic, works at the scale of dozens to low hundreds of files. Beyond that, the routing table becomes unwieldy and a vector database (Layer 4) is more appropriate.

**Layer 3 — Parametric scripts (Python/RhinoScript).** This is where knowledge becomes enforcement. A rammed earth wall script doesn't suggest a maximum height-to-thickness ratio — it raises a `ConstraintViolation` if the ratio exceeds 8:1. The agent can't build a non-compliant wall. The error message explains why: "Height/thickness ratio 9.2 exceeds structural limit of 8. Either reduce wall height to 4000mm or increase thickness to 545mm."

This is a fundamentally different knowledge model. The script is the spec. The error message is the documentation. Constraints are enforced, not suggested — an agent can't misread a constraint, it can only trigger it or satisfy it. The scripts consume the other layers: a wall generator imports GWP values from the database (Layer 1), reads construction guidelines from the file tree (Layer 2), and produces geometry with embedded data (carbon numbers, compliance notes, construction sequence references).

The limitation is maintenance. Each script is code that must be written by someone who understands both the domain (structural engineering, material science, construction practice) and the programming. A constraint that says "maximum compaction reach is 600mm" is only as good as the domain expert who specified it.

**Layer 4 — RAG over dense references (Vector DB).** Encyclopedic, unstructured knowledge that is too large for context, too narrative for SQL, and too unpredictable in access pattern for a file tree. The Dicobat (Dictionnaire général du bâtiment) is the paradigmatic case: hundreds of pages, thousands of entries, cross-referenced definitions mixing techniques, materials, history, and norms.

The pipeline: extract text → chunk at natural boundaries (dictionary entries, clause boundaries) → embed with Gemini Embedding → store in ChromaDB. An agent queries with natural language: `knowledge_search("assemblage à tenon et mortaise")` and gets back the relevant encyclopedia entry. The agent doesn't know about embeddings or vectors — it asks a question and gets grounded text.

This layer handles what the others cannot: the moment when an agent encounters a term it doesn't know, a technique it hasn't seen, a norm clause it needs to check. The Dicobat, SIA norm full texts (local only, copyright-protected), construction atlases — dense reference works that an architect would pull off the shelf. The vector database is the digital shelf.

**The layers are parallel, not stacked.** An agent working a single task may use one, two, or all four. A timber specialist designing a joint detail might: search the Dicobat for traditional proportions (Layer 4) → query SIA 265 span limits for the section (Layer 1) → generate geometry with embedded constraints (Layer 3). The layers are tools on a workbench. The task determines which tools get picked up.

## 4.2 Geometric coordination: how agents share space

When multiple agents produce geometry in a shared file, they need a way to not break each other's work. Three mechanisms, deployed progressively — not as alternatives but as cumulative layers of assurance.

**Skill: prompt-level discipline.** Each agent receives spatial constraints in its instructions: "You operate exclusively on layer `STRUCTURE::COLUMNS`. Do not create objects outside this layer." This is the baseline — always present, always necessary, never sufficient alone.

It works because language models are generally compliant with clear instructions. It fails because compliance is probabilistic. An agent that writes to the wrong layer doesn't announce it. There's no enforcement, no detection, no rollback. The Lock 05 build relied primarily on this level, and it worked — but it worked because the task was well-structured, not because the mechanism is robust.

**Tool: spatial mutex via MCP.** A dedicated function that agents call before writing geometry:

```
claim_zone(agent_id="structural", bbox=[x0,y0,z0, x1,y1,z1])
→ {"status": "granted"} or {"status": "conflict", "claimed_by": "mep"}
```

This is a spatial mutex — the same pattern used in concurrent programming for shared memory access, applied to geometric space. The MCP server maintains a zone registry. Agents that don't claim before writing are violating a protocol, not just ignoring an instruction. The registry is auditable: what was claimed, when, by whom.

The open design question is granularity. Object-level claims are precise but create contention. Bounding-box claims are fast but coarse — an agent claims a volume, not just its geometry. Layer-level claims are the current implicit model (each agent owns its layers), but they don't catch intra-layer conflicts. The right default depends on the project's geometric density.

**Agent: coordinator with clash detection.** A dedicated agent with read access to all layers and no write access. It monitors geometry production, runs clash detection after each round, and issues resolution instructions: "Structural column at [x,y,z] conflicts with MEP riser. Structural agent: offset column 200mm east."

The coordinator adds something the other mechanisms lack: semantic resolution. It can distinguish a layer violation (trivial — move the object) from a discipline conflict (the column is inside the MEP service zone — that's a design decision, not a spatial error). But it adds latency — every production round is mediated — and it's a single point of failure. Necessary at the discipline-specialization phase. Premature before then.

**Deploy progressively:** prompt discipline always, spatial mutex when multiple agents share dense geometry, coordinator when discipline conflicts require semantic resolution. Don't skip levels.

## 4.3 Execution infrastructure: where it runs

**Local — single Rhino instance.** What exists now. One Rhino process, one `.3dm` file, multiple agents connected through MCP. Layer groups provide spatial separation. Demonstrated: 7 agents, 709 objects. The limit is contention — a single Rhino process serializes geometry operations, so agents wait for each other.

**Router — multi-instance dispatch.** A proxy server between agent sessions and Rhino instances. Maintains an instance registry (name → host:port) and routes MCP commands by target. Agent Team A works in Rhino instance 1 (Building A), Team B in instance 2 (Building B). True isolation — separate processes, separate files.

The router is built. The multi-instance target doesn't yet exist on Mac — Rhino 8 for Mac is a single-process application, architecturally blocked by the license manager. First multi-instance test: a teammate's Windows machine. No cost, no cloud, validates the router with real parallel operation.

**Cloud — Azure VMs for true parallelism.** Windows VMs running Rhino headlessly, connected via SSH tunnel to the router. On-demand provisioning (start when a session begins, deallocate when idle). A golden image — one VM configured with Rhino, the MCP plugin, and required Grasshopper plugins — cloned for each new instance.

This is the path to scaling: multiple Rhino instances on demand, each hosting an agent team, a coordinator agent reading across all instances. The infrastructure is designed. The licensing question (whether educational Rhino licenses support cloud core-hour billing) is unresolved and must be confirmed with McNeel before investment.

## 4.4 The blackboard: the shared model

All of the above converges on a single idea: agents coordinate through a shared spatial model, not through API contracts. The Rhino file with its layer groups is a working version of this — crude, but functional. Every agent reads from and writes to the same geometric space. Coordination happens through the model itself: the structural grid published after Phase 1 is the contract that envelope agents build against. The model is the communication medium.

This is the blackboard pattern from software architecture, applied to design. NVIDIA's Omniverse implements it through OpenUSD — multiple writers contributing layers to a shared scene, with a composition engine resolving conflicts through strength ordering. Bentley's iTwin makes the shared model queryable — an energy agent can ask "what is the U-value of every exterior wall on the north facade?" and get structured answers from the same model the structural agent reads. Autodesk Forma embeds parallel analysis agents (wind, noise, daylight) that all read from and respond to the same site model simultaneously.

The Rhino file is none of these. It has no composition engine, no query interface, no parallel analysis. But it has the essential property: a single geometric space where all agents' contributions coexist and can be inspected together. The layer tree is the organizational structure. The coordination geometry (published column positions, slab edges, level datums) is the shared contract. The review gates verify that the contributions are compatible.

The trajectory — from a Rhino file with layer groups to a USD scene with composition arcs to a queryable digital twin — is a trajectory of increasing sophistication around the same idea: the model as coordination medium. The blackboard is the right pattern for design because design is not a pipeline (data flows forward, each stage transforms) but a conversation (contributions accumulate, interact, and produce emergent properties). The archipelago emerged from City101's blackboard. The integrated building emerges from the shared model.
