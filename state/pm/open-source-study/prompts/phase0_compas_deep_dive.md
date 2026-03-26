# Phase 0: COMPAS Deep Dive

**Project:** open-source-study
**Status:** ACTIVE
**Estimated:** 1 session, ~1.5 hrs

---

<context>
You are studying the COMPAS framework (ETH Zurich, Block Research Group) to extract architectural patterns for building "rhinobase" — a knowledge layer that gives AI agents fluency in Rhino modeling.

COMPAS is MIT-licensed. You can use, adapt, and learn from it freely.

We already know:
- compas_wood (IBOIS) has 42+ joint types in C++ with Python bindings
- COMPAS has dedicated packages: compas_rhino, compas_blender, compas_fab (fabrication)
- The core is pure Python with flexible datastructures

Our system:
- 4-layer knowledge architecture: SQLite (structured data) / Markdown (guides) / Code (scripts) / VectorDB (RAG)
- MCP servers connect Claude agents to Rhino
- Parametric scripts generate geometry with construction knowledge baked in
- We need: better datastructures for architectural elements, cleaner Rhino integration patterns, fabrication-aware geometry
</context>

<instructions>

## Research tasks (no code writing)

### 1. Core architecture
Read the COMPAS source and documentation. Answer:
- How does COMPAS structure its datastructures? (meshes, networks, volmeshes — what's the abstraction)
- How does geometry flow between pure Python and Rhino? (compas_rhino bridge pattern)
- How do they handle serialization? (saving/loading architectural data)
- What's their plugin/extension pattern? (how compas_fab, compas_wood etc. extend the core)

### 2. Rhino integration specifically
Focus on compas_rhino:
- How do they create, read, modify Rhino geometry from Python?
- How do they attach data to geometry? (attributes, user text, layers — compare with Rhyton's approach)
- How do they handle the IronPython vs CPython split in Rhino?
- What's their artist/scene pattern for visualization?

### 3. Fabrication patterns
Focus on compas_fab:
- How do they represent fabrication constraints in code?
- Robot planning, tool paths — what's the abstraction level?
- How does design geometry connect to fabrication geometry?

### 4. Extension architecture
- How would someone build a new "compas_X" extension?
- What does the core provide vs what does each extension add?
- How do extensions share data?

## Deliverable

Write `output/open-source-study/compas_patterns.md` with this structure:

```markdown
# COMPAS Patterns — What to Adopt for Rhinobase

## Architecture summary
[One paragraph: what COMPAS is and how it's structured]

## Datastructure patterns
[How they represent architectural/structural elements. What we'd adopt, what we'd skip]

## Rhino integration
[Their bridge pattern. How it compares to our MCP approach. Gaps and opportunities]

## Data-on-geometry
[How they attach metadata to objects. Compare with Rhyton's user-text approach]

## Extension model
[How compas_wood plugs in. What this means for iboisbase as a "compas_X"-like extension]

## Fabrication bridge
[Abstraction patterns from compas_fab. Relevant for our fabrication-bridge project]

## Adopt / Skip / Adapt
| Pattern | Decision | Why |
|---------|----------|-----|
| ... | Adopt / Skip / Adapt | ... |

## Impact on rhinobase-iboisbase project
[Concrete changes to the existing master plan based on what we learned]
```

</instructions>

<verification>
Before finishing, check:
- [ ] Every claim references a specific file or module in COMPAS (not just "they do X")
- [ ] Adopt/Skip/Adapt table has at least 5 entries
- [ ] Impact section has concrete, actionable items (not "we should consider")
- [ ] No code was copied — only patterns described
</verification>
