# Phase 2: Environmental + Sustainability Layer

**Project:** open-source-study
**Status:** ACTIVE
**Estimated:** 1 session, ~1 hr
**Dependencies:** Phase 1 (need data-on-geometry design first)

---

<context>
You are surveying environmental analysis and sustainability tools for architecture to decide what (if anything) to integrate into our knowledge system.

Our system:
- Site extraction pipeline (geodata/scripts/) pulls terrain, buildings, infrastructure, imagery from swisstopo
- archibase has KBOB LCA data (375 Swiss materials)
- Phase 1 designed a data-on-geometry layer for Rhino
- knowledge-infrastructure project plans a feedback loop (case_notes, severity levels, learnings)
- We work along the Geneva–Villeneuve corridor (46.1–46.6°N, 6.0–7.1°E)

Question to answer: should environmental analysis (sun, wind, energy, daylight) be part of our knowledge system, or should it stay as standalone tools (Ladybug) that architects use separately?

Key tools to survey:
- Ladybug Tools (AGPL-3.0) — climate, daylight, energy, CFD for Grasshopper
- Cardinal LCA (Grasshopper) — early-stage LCA for non-experts
- EPiC for Grasshopper (Melbourne) — assemblies + in-viewport charts
- Rhino Circular (Cornell) — circularity indicators on building elements
- openLCA (MPL-2.0) — full LCA platform, broader databases
- ClimateStudio — environmental simulation plugin
</context>

<instructions>

## Research tasks (no code writing)

### 1. Ladybug Tools — architecture and data formats
- What components exist? (Ladybug, Honeybee, Dragonfly, Butterfly — scope of each)
- What data formats do they output? (can we consume their results?)
- How do they attach results to geometry? (compare with Phase 1 data-on-geometry design)
- License: AGPL-3.0 — what does this mean for integration? (copyleft implications)
- Could an MCP agent invoke Ladybug components? Or is it GH-only?

### 2. Sustainability plugins — UX patterns
For Cardinal LCA, EPiC, Rhino Circular:
- How do they make sustainability data visible to non-experts?
- In-viewport visualization approaches (charts, color overlays, labels)
- What's the user interaction model? (select → analyze → display?)
- Any patterns we should adopt for our visualization modes?

### 3. Integration decision
Evaluate three options:
- **A: Full integration** — environmental data becomes part of archibase/rhinobase, agents run analysis
- **B: Bridge** — agents can trigger Ladybug analysis and consume results, but Ladybug stays standalone
- **C: Separate** — environmental analysis stays in Grasshopper, not connected to our system

For each, assess: value added, complexity, license risk, maintenance burden.

## Deliverable

Write `output/open-source-study/environmental_layer.md`:

```markdown
# Environmental + Sustainability Layer — Survey + Decision

## Tool landscape
| Tool | What | License | Data formats | Integration complexity |
|------|------|---------|-------------|----------------------|
| ... | ... | ... | ... | Low/Med/High |

## Ladybug Tools deep dive
[Components, data flow, output formats, AGPL implications]

## Sustainability visualization patterns
[What we learned from Cardinal/EPiC/Rhino Circular about making data visible]

## Integration options
### Option A: Full integration
[Pros, cons, effort, risk]

### Option B: Bridge
[Pros, cons, effort, risk]

### Option C: Separate
[Pros, cons, effort, risk]

## Recommendation
[Which option, why, and what's the first step if we proceed]

## Patterns to adopt regardless
[Visualization or UX patterns worth using even if we don't integrate the tools themselves]

## Impact on knowledge-infrastructure project
[How this affects the feedback loop design]
```

</instructions>

<verification>
- [ ] All three options are evaluated with concrete pros/cons (not just "it depends")
- [ ] AGPL implications are specifically addressed (not just "copyleft")
- [ ] At least 3 visualization patterns documented from sustainability plugins
- [ ] Recommendation is decisive — pick one option with reasoning
</verification>
