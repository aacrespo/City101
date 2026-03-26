# Open Source Study — Master Plan

**Goal:** Study open-source AEC tools to extract patterns for our knowledge system and agent workflow. Learn what exists, what's usable (MIT), and what to implement ourselves.

**Owner:** Andrea
**Created:** 2026-03-26
**Timeline:** Post-midterm, no rush — learning project
**Estimated:** 3-4 sessions, ~5 hours total

## Why this project

We're building a knowledge-grounded agent workflow for architecture (archibase + MCP + agent teams). Other practices and labs have solved pieces of this puzzle — data-on-geometry, LCA calculation, environmental analysis, fabrication frameworks. Instead of reinventing everything, study what exists, understand the patterns, and build our own implementations informed by proven approaches.

**License constraint:** Only MIT/open-source code can be used directly. Unlicensed repos (HdM Rhyton) are pattern-study only — look, learn, implement your own.

## Sources mapped to existing projects

| Source | License | Feeds into |
|--------|---------|------------|
| COMPAS (ETH) | MIT | rhinobase-iboisbase (framework patterns, compas_wood) |
| Ladybug Tools | AGPL-3.0 | knowledge-infrastructure (environmental data layer) |
| HdM Calc | MIT | fabrication-bridge (LCA schema, KBOB calculation) |
| HdM Rhyton | NO LICENSE | rhinobase (data-on-geometry pattern — implement own) |
| openLCA | MPL-2.0 | fabrication-bridge (broader LCA methodology) |
| Cardinal LCA / EPiC / Rhino Circular | Various | knowledge-infrastructure (UX for making data visible) |
| opensource.construction directory | — | discovery of smaller tools we haven't found yet |

---

## Phase 0: COMPAS Deep Dive (1 session, ~1.5 hrs)

**Goal:** Understand COMPAS architecture — how it structures geometry, data, and CAD integration. Extract patterns for rhinobase.

**Topology:** Flat, narrow context, sequential (one analyst reading code)

**Team:** 1 agent (Analyst) + Claude direct

**Reads:**
- github.com/compas-dev/compas — core library structure
- github.com/compas-dev/compas_fab — fabrication package
- compas.dev documentation — architecture, datastructures, Rhino integration
- Existing: compas_wood analysis from IBOIS brief

**Produces:**
- `output/open-source-study/compas_patterns.md` — architecture summary, datastructure patterns, how they handle Rhino integration, what we'd adopt vs skip
- Update to rhinobase-iboisbase project if COMPAS changes our approach

**Success:** Can explain COMPAS architecture in one paragraph. Know which patterns to adopt for rhinobase.

---

## Phase 1: LCA Schema Study (1 session, ~1.5 hrs)

**Goal:** Study HdM Calc's assembly→material→impact schema and compare with our KBOB data in archibase. Study Rhyton's data-on-geometry pattern (without copying code).

**Topology:** Flat, narrow context, parallel (two independent reads)

**Team:** 2 agents
- Agent A (Analyst): Read HdM Calc source — schema, JSON structure, how assemblies map to materials, how KBOB data is referenced
- Agent B (Analyst): Read Rhyton source — how user text is stored on Rhino objects, color scheme logic, visualization approach

**Reads:**
- github.com/herzogdemeuron/calc (MIT) — C# source, schema definitions, KBOB integration
- github.com/herzogdemeuron/rhyton (NO LICENSE) — Python source, pattern study only
- Our archibase L1 KBOB tables for comparison

**Produces:**
- `output/open-source-study/lca_schema_comparison.md` — HdM schema vs our KBOB structure, gaps, what to adopt
- `output/open-source-study/data_on_geometry_pattern.md` — how to implement Rhyton-like functionality ourselves (original code, informed by their approach)

**Dependencies:** None (can run before or after Phase 0)

**Success:** Have a clear schema design for how archibase LCA data flows onto Rhino geometry. Design is our own, not copied.

---

## Phase 2: Environmental + Sustainability Layer (1 session, ~1 hr)

**Goal:** Understand Ladybug Tools and sustainability plugins — what environmental data they provide, how it could feed into our knowledge system.

**Topology:** Flat, narrow context, sequential

**Team:** 1 agent (Analyst)

**Reads:**
- Ladybug Tools documentation — component structure, data formats, what analysis types are available
- Cardinal LCA, EPiC for Grasshopper, Rhino Circular — how they present sustainability metrics in-viewport
- openLCA — scope and methodology (for future reference)

**Produces:**
- `output/open-source-study/environmental_layer.md` — what Ladybug provides, how it could connect to site-context pipeline, whether it's worth integrating vs using standalone

**Dependencies:** Phase 1 (need to know our data-on-geometry approach first)

**Success:** Decision on whether Ladybug integration is worth pursuing now or later. Know the data formats.

---

## Phase 3: Synthesis + Integration (0.5 session, ~0.5 hrs)

**Goal:** Pull everything together. Update existing PM projects with learnings. Write implementation specs where patterns are clear enough.

**Topology:** Direct (Claude + Andrea, no agents)

**Reads:**
- All Phase 0-2 outputs
- Existing project master plans (rhinobase-iboisbase, knowledge-infrastructure, fabrication-bridge)

**Produces:**
- Updates to existing project master plans with patterns learned
- `output/open-source-study/synthesis.md` — what we learned, what changes, what doesn't
- Append to `state/pm/topology_history.md` with study outcomes

**Dependencies:** Phases 0-2 complete

**Success:** Existing projects updated with concrete patterns. No vague "we should look into X" — everything is either adopted, rejected with reason, or deferred with trigger.

---

## Phase diagram

```
Phase 0 (COMPAS)  ──────────┐
                             ├──→ Phase 3 (Synthesis)
Phase 1 (LCA + Rhyton)  ────┤
        │                    │
        ▼                    │
Phase 2 (Environmental) ────┘

Phases 0 and 1 can run in parallel.
Phase 2 depends on Phase 1.
Phase 3 depends on all.
```

## Connections to existing projects

```
open-source-study
├── Phase 0 (COMPAS) ──→ rhinobase-iboisbase (framework patterns)
├── Phase 1 (LCA) ────→ fabrication-bridge (KBOB schema)
├── Phase 1 (Rhyton) ─→ rhinobase (data-on-geometry)
├── Phase 2 (Env) ────→ knowledge-infrastructure (environmental data)
└── Phase 3 ──────────→ updates all three projects
```
