# 5. Proof: City101 and the Locks

The proof is not a demo. It is six months of practice that produced a logic — a way of structuring the relationship between knowledge, organization, and infrastructure that makes the extended architect operational. The full implementation is ahead. What exists now is the logic, tested against real production work, with enough evidence to know it holds.

## City101: six months of corridor analysis

City101 is an EPFL BA6 studio project analyzing the 101km Geneva–Villeneuve rail corridor. Two students, four Claude accounts, 25+ sessions between February and March 2026. The project did not set out to build an "AI workflow." The demands of rigorous, multi-dimensional spatial analysis forced one to emerge.

The numbers: 49 stations, 20+ datasets, 7 time slots, 5 break dimensions (economic, temporal, modal, connectivity, workspace). The deliverables: enriched datasets, interactive visualizations, scrollytelling maps, spatial analyses at corridor and station scale. The team: two humans, multiple agent instances configured as analyst, cartographer, visualizer, builder, modeler — roles activated as needed, reconfigured per task.

What emerged from this practice was not a methodology prescribed in advance. It was a set of patterns discovered through iteration:

**Staged promotion.** Agent output goes to a staging directory first, never directly to production data. Every dataset is verified before it moves. This pattern emerged after an early incident where unverified agent output was treated as ground truth. The verification workflow now has explicit quality gates: coordinate range checks, null field detection, source attribution, outlier flagging.

**Canonical entities.** When one agent writes "Lausanne Gare" and another writes "Lausanne" and a third writes "Lausanne CFF," no downstream join works. The project converged on a canonical station list — 49 entries, fixed IDs, standardized names — that every agent references. This is the architectural equivalent of a coordination drawing: the shared reference that makes independent work combinable.

**Living state.** A context file, updated at the end of every session, capturing the current state of the project: what's been found, what's open, what's changed. Not documentation after the fact — a living document that the next session reads before starting. Combined with a lockboard tracking who is working on what, this solved the duplication problem that plagued the project's first weeks (Conway's Law in action: two siloed human-agent teams producing overlapping datasets).

**Cross-domain emergence.** The finding that defines City101's analytical contribution — that the corridor functions as an archipelago of workable stations, not a continuous line — was not in any task specification. It emerged from spatially joining independently produced datasets. The correlation between religious Shannon diversity, modal Shannon diversity, cuisine Shannon diversity, and economic category diversity (r = 0.63–0.71) appeared because a flat analysis topology allowed agents working on different datasets to contribute to a shared spatial model. A hierarchical topology, routing every finding through a human coordinator, would have needed to anticipate which joins were productive. The flat topology let the data speak.

These patterns — staging, canonical references, living state, cross-domain emergence — are not specific to corridor analysis. They are organizational patterns that any multi-agent design workflow will need. City101 discovered them through practice.

## Lock 05 CHUV: parallel production in shared space

Lock 05 was a single-session build: seven agents, one Rhino file, 709 objects, four production rounds. It was the first demonstrated parallel multi-agent coordination in a live CAD environment.

The setup: each agent was assigned to a distinct layer group (Structure, Shell, Windows, Circulation, Elevator, Roof, Ground). A shared specification defined the structural grid, level datums, wall thicknesses, and interface rules (where one agent's geometry meets another's). The build proceeded in phases: structure first (columns, slabs, beams — the coordination contract), then envelope agents in parallel (shell, roof, ground), then detail agents in parallel (windows, circulation, elevator).

What worked: the layer separation held. Agents stayed on their assigned layers. The structural grid, published as coordination geometry after Phase 1, gave every subsequent agent a shared reference. The interface registry — explicit rules like "glass at wall face minus 80mm recess" — prevented most geometric conflicts. The review gates (self-audit, bilateral check, full model review) caught the remaining issues.

What didn't: the coordination was mostly behavioral — agents followed instructions because they were well-prompted, not because an enforcement mechanism prevented violations. There was no spatial mutex, no automated clash detection, no rollback capability. The build worked because the task was well-structured and the agents complied. At higher density, with more ambiguous spatial assignments, it would break.

The honest assessment: Lock 05 is a proof of concept, not a production system. But it proved something specific — that multiple AI agents can produce significant geometry in shared CAD space, coordinated through organizational structure (layer groups, interface rules, phased production) rather than through technical enforcement. The organigram was the coordination mechanism.

## The logic: three systems

What City101 and the Locks produced, beyond their specific outputs, is a logic for how the extended architect works. Three systems, independent but mutually reinforcing:

**Knowledge management** — four types of resource, each optimized for a different shape of content:

1. *Parametric scripts* (Python/RhinoScript): executable constraints. A rammed earth wall generator that raises a ConstraintViolation if the height-to-thickness ratio exceeds 8:1. Knowledge encoded as code — enforced, not suggested.
2. *Markdown library*: curated narrative knowledge. Typologies, precedents, design concepts, experiential descriptions. The kind of knowledge that needs to be read and interpreted, not computed.
3. *Vector embeddings* (RAG over dense references): encyclopedic construction knowledge — the Dicobat, SIA norms, construction atlases. Too large for context, too unstructured for SQL, too unpredictable in access pattern for a routing table.
4. *Relational database* (SQLite): structured quantitative data. KBOB embodied energy values, span tables, section profiles, fire ratings. Queryable, joinable, authoritative.

Each type answers a different kind of question. "What is the GWP of rammed earth?" → database. "What are the typological precedents for courtyard housing?" → markdown. "How does pisé formwork sequence work?" → vector search over the Dicobat. "Generate a rammed earth wall at these dimensions with constraint validation" → parametric script. An agent's task determines which resources it reaches for — often more than one per task.

**Agent organization** — the organigram, tuned to the task. Flat and broad for discovery (City101's corridor analysis). Hierarchical and scoped for production (Lock 05's phased build). Phase-adaptive, reconfigurable per session, iterable like a floor plan. The three dimensions from §3 — communication topology, context scope, task dependency — are the tuning parameters.

**Technical infrastructure** — the execution environment that makes parallel operation possible. A modified Rhino MCP plugin accepting configurable ports. A router server dispatching commands to multiple Rhino instances. The path to cloud VMs for true parallelism (Azure, headless Rhino on Windows). Currently demonstrated on a single instance; the multi-instance architecture is designed and the router is built.

These three systems are the architecture of the extended architect. Knowledge provides the domain constraints. Organization determines how those constraints interact. Infrastructure makes parallel operation possible. None is sufficient alone. Together, they make it viable for an architect to have structural, buildability, and sustainability knowledge present from Phase 0 — which is the thesis of this document.

## What remains to be built

The logic is established. The full implementation is not.

The knowledge system exists in fragments: some parametric scripts, a partial markdown library, no vector database yet, no structured database. Building these out — importing KBOB into SQLite, embedding the Dicobat into ChromaDB, writing the parametric constraint scripts for key materials — is the implementation work ahead.

The agent organization has been tested at two scales: analytical (City101, 25+ sessions) and geometric (Lock 05, single session). The next test is a full prototypology build: site → terrain → context → architecture, with all three systems active, across multiple sessions.

The infrastructure works on a single Rhino instance. Multi-instance operation requires a Windows environment (Rhino 8 for Mac is single-process). The router is built. The first multi-instance test will happen on a teammate's Windows machine before any cloud investment.

This is not a limitation of the thesis. The thesis is about the logic — the relationship between knowledge, organization, and infrastructure that extends the architect's integrative capacity. The logic holds. The implementation is engineering.
