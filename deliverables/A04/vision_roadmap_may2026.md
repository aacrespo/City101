# Vision Roadmap — May 2026

**Andrea Crespo & Henna Räsänen**
**AR-302k Studio Huang — Sentient Cities, EPFL BA6**
*Internal strategic document — March 23, 2026*

---

## Part 1: Where We Are

In three weeks, starting from a blank repo and a 101km corridor, we built a working human-AI collaboration environment for architectural design. Here is what exists today:

**Knowledge system (Archibase)**
Four-layer construction knowledge base: SQLite database (99 rows — materials, KBOB LCA data, steel profiles, fire codes, SIA loads, room dimensions, span tables), 33 curated markdown guides, parametric enforcement scripts, and a RAG layer with 35,244 text chunks (Dicobat, 21 SIA norms, Designing Buildings Wiki, Alexander patterns, Bloomsbury) plus 2,480 multimodal image embeddings from Deplazes and Vittone via Gemini Embedding 2.

**Proven modeling workflow**
Lock 05 CHUV: 7 collaborative agents, 709 objects, three review rounds (self-audit, cross-team coordination, free improvement). Agents caught real issues — missing railings, wrong door orientation, code violations — and resolved spatial conflicts that sequential work would miss. The legal knowledge framework structures how agents reason: archibase as law, the playbook as doctrine, accumulated learnings as jurisprudence.

**Infrastructure**
MCP router for multi-instance Rhino control. Session management system. Training pipeline (80 exercises across 3 sessions, 5,248+ objects). Data collection covering 49 stations: transit ridership, EV charging, remote work places, shared mobility, 24h venues, corridor analysis with WCI scoring.

**Presentation layer**
Pixel-agent concept designed. Kitchen analogy (Overcooked vs. real kitchen) for explaining collaboration to non-technical audiences. AI workflow diagrams, healthcare chain visualizations, transport pulse animation — all complete.

**Cost so far: ~$2 in API calls.**

---

## Part 2: This Week → Midterm (March 23–30)

### Monday March 24
- Migrate ChromaDB → Qdrant (ChromaDB segfaults on large collections; 2,480 entries need stable home)
- Continue Gemini image embeddings: SIA norms, Bloomsbury chapters, Dicobat Visuel
- Consolidate Lock 05 live geometry into v4 script

### Tuesday March 25
- Azure VM setup: B2ms Windows instance + Rhino core-hour license ($0.10/hr each)
- SSH tunnel to Mac, validate headless Rhino + rhinomcp on cloud
- Andrea's dad helps with Azure CLI access — EPFL provides $100 free credits

### Wednesday–Thursday March 26–27
- Scale to all 9 corridor nodes — agent teams running in parallel on cloud
- Each node gets multiple iterations (each one improves the playbook)
- Tectonic review Mode C operational: load-path verification from roof to ground
- Begin YouTube tutorial embeddings (tool ready, Qdrant stable)

### Friday–Saturday March 28–29
- Blender MCP integration: import Rhino geometry → furnish, texture, light interiors
- Rendered views of key nodes for presentation
- Narrative locked — Henna formats slides from terminal aesthetic + architecture language

### Sunday March 30 — Midterm
- 9 modeled corridor nodes with construction-grade detail
- Knowledge system demonstrated live
- Collaboration methodology presented as design research, not tech demo

---

## Part 3: April — Expanding the Stack

### a) Site Adaptation Engine

*What it does:* Takes Henna's 3D corridor model as terrain base and places typologies considering circulation flow, entrance positioning, level changes, urban scale, orientation, and neighboring buildings. This is the core architectural intelligence — not just placing a building on a site, but reading the site and letting it shape the building.

*Tools needed:* Terrain import pipeline (exists), QGIS MCP for spatial analysis, corridor dataset crossref with site variables, archibase for dimensional and code constraints.

*Effort:* 2 weeks. The terrain import skill and site context assembly already work. The intelligence layer is about encoding the site-reading logic that Andrea and Henna already practice — translating architectural judgment into queryable rules.

*What it unlocks:* Any point on the corridor becomes a potential site. The system reads it the way an architect would — slope, access, neighbors, flow — and proposes how a building meets the ground.

### b) Supply Chain Scoring (Circuit d'Approvisionnement)

*What it does:* Scores each material choice on three axes: grey energy (énergie grise / embodied carbon), transport distance from source to construction site, and cost. Adjustable weights let the architect explore tradeoffs — local timber vs. imported steel, recycled concrete vs. new.

*Data sources:* KBOB database (375 Swiss LCA entries, already in archibase SQLite), Swiss supplier directories, transport distance calculation via road network, material cost indices. The KBOB data is the Swiss standard for embodied energy — having it queryable is already an advantage most practices don't have.

*Effort:* 2–3 weeks. KBOB integration is trivial (data exists). Supplier matching and transport scoring need new data collection and a scoring algorithm. Cost estimation is the hardest — Swiss construction pricing is not openly published.

*What it unlocks:* Every material decision in the 3D model carries a sustainability and logistics score. The architect sees the consequences of choices in real time, not after the fact.

### c) Full Construction Spec Sheet

*What it does:* Extracts material quantities from the 3D model, matches to Swiss suppliers, estimates pricing, and checks regulatory compliance against SIA norms and fire codes.

*Tools needed:* Rhino geometry analysis (volumes, areas, counts), archibase queries for code compliance, supplier database (to build), pricing estimation model.

*Effort:* 3–4 weeks. Quantity extraction from Rhino geometry is mechanical. Supplier matching requires building a Swiss market database. Pricing is approximate but useful. Code compliance checking against SIA norms is partially ready (fire requirements and design loads already in archibase).

*What it unlocks:* The output of a modeling session isn't just geometry — it's a construction document. Two people produce what normally requires a quantity surveyor, a specifications writer, and a code consultant.

### d) Construction Site Logistics

*What it does:* Generates a Gantt chart for construction phases, proposes site layout (crane placement, material storage, delivery access), considers weather/season, and produces a role organization diagram.

*Tools needed:* Gantt generation (Mermaid or dedicated library), site layout logic based on building footprint and access roads, construction phase sequencing from archibase knowledge (assembly order, curing times, weather dependencies).

*Effort:* 2–3 weeks. Construction phase knowledge exists in the markdown guides. Site layout is constrained optimization — given the building footprint, access points, and crane reach, place storage and circulation. The role diagram follows from the phase breakdown.

*What it unlocks:* The design doesn't stop at the building — it includes how the building gets built. This is the kind of early integration that only large firms do, because it requires expertise that's expensive to bring in during design phase.

### e) Blender Pipeline (Rendering + Animation)

*What it does:* Transfers Rhino geometry to Blender, applies materials and textures, furnishes interiors, and produces animated walkthroughs showing spatial experience.

*Ecosystem (researched):*
- **ahujasid/blender-mcp** — dominant implementation, ~17.9k GitHub stars. 37 tools: object creation/modification, material control, scene inspection, arbitrary Python execution. Poly Haven integration for textures and HDRIs. Works with Claude.
- **CommonSenseMachines/blender-mcp** — specialized for text-to-4D. Vector search-based 3D model retrieval, text-based animation with Mixamo integration. More useful for asset retrieval than architectural rendering.
- **poly-mcp/Blender-MCP-Server** — 51 tools, thread-safe execution, designed for multi-agent orchestration.

*Effort:* 2 weeks for basic pipeline (geometry transfer + materials + static renders). Animation adds another 2 weeks. The ahujasid server is mature enough to start with.

*What it unlocks:* Photorealistic output from the same model that has construction-grade detail. The walkthrough shows not just what the building looks like, but what it *feels* like to move through.

### f) Archibase Expansion

*What it does:* Deepens and broadens the knowledge base that grounds all agent work.

*Immediate (this week):*
- Qdrant migration — unblocks everything downstream
- SIA norms embedding (21 PDFs)
- Bloomsbury + Dicobat Visuel image embedding

*April:*
- YouTube tutorial embeddings: yt-dlp → ffmpeg keyframes → Gemini describe → embed. Channels: PJ Architecture, Simply Rhino, How to Rhino. This teaches agents *how* to model, not just *what* to build.
- EPFL coursework integration (AR-327 computational architecture, 50+ files identified)
- More construction books as they become available
- Ongoing curation: every build session distills learnings into the playbook, and the playbook feeds back into better builds

*Effort:* Continuous. Each addition compounds — a new book embedded means every future agent session has access to that knowledge.

---

## Part 4: May — The Full Picture

By end of May 2026, the complete workflow looks like this:

**1. Pick a site on the corridor.**
Select a point. The system pulls terrain data, surrounding context, circulation patterns, transit access, and existing constraints.

**2. Generate typology with construction-grade detail.**
Agent teams produce a building — not a massing study, but a structure with real wall assemblies, proper load paths, code-compliant dimensions, and material specifications. Each agent carries domain knowledge from archibase: the structural agent knows span tables, the envelope agent knows layer buildups, the circulation agent knows SIA egress requirements.

**3. Score the supply chain.**
Every material in the model gets scored: embodied carbon from KBOB, transport distance from the nearest Swiss supplier, cost estimate. The architect adjusts weights — prioritize local sourcing, minimize carbon, control budget — and sees the building respond.

**4. Plan construction logistics.**
Phase diagram, site layout, team organization. The building comes with instructions for how to build it.

**5. Render and animate the experience.**
Blender pipeline produces photorealistic images and walkthroughs. The same model that satisfies the structural engineer also produces the image that convinces the client.

**6. All of this with a team of two + AI.**

This is the thesis made tangible. The architect's integrative capacity — holding structural, environmental, regulatory, logistical, and experiential concerns simultaneously — is extended by AI agents that carry domain knowledge. The cost of having the builder, the sustainability consultant, and the structural engineer "in the room" from Phase 0 drops to near zero. The organigram stops being an administrative constraint and becomes a design instrument.

What changes is not the quality of the pieces (a wall assembly is a wall assembly) but *who is listening from the start*. When more domains are present from the beginning, the building is shaped by constraints that traditional practice encounters too late to influence form. The creative act remains human — it's the composition of known knowledge into a specific solution for a specific place. The AI doesn't design. It extends the bandwidth of the people who do.

---

## Part 5: Tool & Workflow Scaling

### MCPs — Current and Needed

| MCP | Status | Purpose |
|-----|--------|---------|
| Rhino (rhinomcp) | Running — router mode, multi-port | 3D modeling |
| Blender (ahujasid) | To integrate — April | Rendering, furnishing, animation |
| QGIS (jjsantos01/qgis_mcp) | To evaluate — April | Spatial analysis, terrain, corridor data |
| Mapbox (official) | To evaluate | Geocoding, routing, isochrones, travel time |
| OSM (NERVsystems/osmmcp) | To evaluate | Neighborhood analysis, EV stations, Overpass queries |
| Discord | Running | Team communication |

**Gap:** No MCP exists for construction material databases or pricing APIs. Archibase is ahead of the public ecosystem here — a future contribution could be publishing a construction knowledge MCP.

### APIs

| API | Status | Use |
|-----|--------|-----|
| Gemini Embedding 2 (Vertex AI) | Active | Multimodal RAG — image + text embedding |
| Gemini Flash/Pro (generation) | Blocked on Vertex auth | Exercise generation, page descriptions |
| SBB Open Data | Used | Transit ridership, frequency |
| DIEMO (DETEC) | Used | EV charging stations |
| Swiss Federal Geodata | Used | Terrain, boundaries |

**To explore:** Swiss supplier databases (if any have APIs), real estate pricing indices, cantonal building permit databases.

### Scheduled Tasks

| Task | Frequency | Purpose |
|------|-----------|---------|
| Corridor data refresh | Weekly | Update transit ridership, shared mobility availability |
| Embedding updates | Nightly (when active) | Process new PDFs added to archibase |
| Playbook distillation | After each build | Convert raw learnings into playbook doctrine |

### Hooks

| Trigger | Action |
|---------|--------|
| Post-model completion | Auto-screenshot all layers, run tectonic review |
| Post-commit to datasets/ | Run verify_dataset.py |
| Session end | Context update, lockboard sync |

### Agent Team Topology

**Flat topology** — for spatially independent work (modeling different nodes in parallel). Each agent gets a site, builds autonomously, reports back. Fast, cheap.

**Hierarchical topology** — for coordinated building systems (Lock 05 pattern). Agents share geometry positions, flag conflicts, cascade improvements. A lead agent coordinates sequencing. Slower, more expensive, but catches integration issues that flat work misses.

**When to use which:** If agents need to share the same physical space (one building, multiple systems), hierarchical. If they work on separate sites or separate deliverables, flat. The overhead of coordination is only worth it when the work is spatially coupled.

---

## Part 6: The Pixel Agent UX

### Current state
Concept documented. The idea: each AI agent has a visual avatar (pixel art character) that makes the collaboration legible. Instead of terminal output, you see a team working — the structural agent checking load paths, the envelope agent wrapping the building, the reviewer walking through.

### Roles needed for architecture
The seven dashboard roles (analyst, cartographer, modeler, visualizer, builder, plus structural and envelope specialists), plus construction-specific roles: site logistics planner, supply chain scorer, code compliance checker. Each gets a distinct visual identity tied to their domain.

### Sprite strategy
Three options, in order of preference:
1. **Commission Andrea's sister** — hand-drawn pixel art with architectural personality. Unique, on-brand, personal.
2. **Design templates + procedural variation** — base sprite per role, color/accessory variations for specializations. Scalable.
3. **Generate from reference** — use the design system palette, constrain to pixel grid, iterate.

### Visualization of collaboration
Construction site metaphor: agents appear on-site, each in their zone. The structural agent is at the foundation, the envelope agent is on the facade, the reviewer walks the perimeter. When agents communicate (cross-team coordination round), you see them walk to each other. Conflicts appear as visual flags.

### MVP scope
The concept doc estimates 16–24 hours for a working prototype. Scope: 7 role sprites, basic animation (idle, working, communicating), a scene that shows a build session playing out. This becomes thesis material — the organigram visualized as a living workspace.

### Thesis connection
The pixel agent is the organigram made visible. Traditional architecture practice has an org chart on paper — PM, architect, engineers, consultants. Here, the organigram is a design parameter: change who's in the room, change the building. The pixel visualization makes this argument intuitive. You don't need to understand AI to see seven specialists collaborating on a building.

---

## Part 7: Competition Intelligence

### The landscape

**Revit MCP ecosystem** is the most developed in AEC:
- [revit-mcp/revit-mcp](https://github.com/revit-mcp/revit-mcp) — AI Client → MCP Server → WebSocket → Revit Plugin → Revit API
- Autodesk University 2025 featured [a demo](https://github.com/chuongmep/mcp-revit-sample-au2025) of MCP-driven Revit workflows
- The Building Coder blog covered [Revit API Agents and MCP](https://thebuildingcoder.typepad.com/blog/2025/04/revit-api-agents-mcp-copilot-and-codex.html)

**Academic work** is catching up:
- Springer published a [comprehensive review of LLMs in AEC](https://link.springer.com/article/10.1007/s10462-025-11241-7) covering applications across all project phases
- ScienceDirect published work on [AI BIM coordinators using LLM-driven multi-agent systems](https://www.sciencedirect.com/science/article/abs/pii/S092658052500603X)

**Industry adoption** (per Chaos/V-Ray 2026 survey):
- 11% of firms actively using AI in architectural design (up 20% year-over-year)
- Larger firms building agentic pipelines combining numerical evaluation with design visualization
- Structural engineering firms building rapid evaluation engines for system selection

**DeepSeek hackathon winner:** Could not be located through web search. If Andrea has more details (hackathon name, platform, person's name), we can do a targeted search.

### Where we stand

Most teams in the MCP-architecture space are connecting AI to *one* tool (Revit or Blender) for *one* task (modeling or rendering). What distinguishes our approach:

1. **Multi-layer knowledge grounding.** No other project we found has a construction knowledge system comparable to archibase — 35K+ text chunks, 2,480 image embeddings, structured SQLite, curated markdown. Most rely on the LLM's training data alone.

2. **Multi-agent coordination, not single-agent automation.** The Revit MCP demos show one AI talking to one tool. We've demonstrated 7 agents coordinating on a shared model with conflict resolution.

3. **Construction-grade output.** The Blender MCPs produce visual scenes. The Revit MCPs manipulate BIM elements. We produce buildings with real wall assemblies, load paths, and code compliance — the knowledge system ensures the output is buildable, not just renderable.

4. **Framing.** Everyone else is presenting "AI tools for architects." We're presenting a methodology for extending the architect's integrative capacity — a fundamentally different argument about what AI changes in architectural practice.

The gap to watch: if someone combines the Revit MCP with a serious knowledge base and multi-agent coordination, they'd be close to what we're building. No one has yet, but the pieces are all public.

---

## Closing

Every projection in this document connects to something already demonstrated:

- 9 nodes → we've done 1 (Lock 05, 709 objects)
- Cloud scaling → the router works locally, Azure is configured
- Supply chain scoring → KBOB data is queryable in archibase today
- Blender pipeline → mature MCP servers exist, integration is engineering not research
- Spec sheets → material and code data already structured in the knowledge system
- Construction logistics → phase knowledge exists in curated markdown guides

The trajectory is not speculative. Each iteration teaches the system *and* the architects. The playbook gets better after every build. The knowledge base grows with every embedded book. The agents learn from accumulated precedent. And Andrea and Henna learn what questions to ask, what constraints matter, what the AI handles well and where human judgment is irreplaceable.

By May, the question is not whether two people can do the work of a multidisciplinary office. The question is whether the architectural profession is ready to reconsider who needs to be in the room — and when they need to arrive.
