# Phase 1B: Data-on-Geometry Pattern (HdM Rhyton)

**Project:** open-source-study
**Status:** ACTIVE
**Estimated:** ~45 min (runs parallel with Phase 1A)
**License:** NO LICENSE — pattern study only, no code reuse

---

<context>
You are studying the patterns in HdM Rhyton (github.com/herzogdemeuron/rhyton) to understand how they attach structured data to Rhino geometry and visualize it. You will then design our own implementation.

CRITICAL LICENSE CONSTRAINT: Rhyton has no open-source license. Default copyright applies. You may:
- Read the code to understand the approach
- Describe the patterns in your own words
- Design and write an original implementation inspired by the concepts

You may NOT:
- Copy any code, even small snippets
- Create derivative works of their code
- Reproduce their specific implementation logic

The concepts themselves (storing key-value data on Rhino objects, color-coding by value) are standard techniques — not copyrightable. The specific code is.

Our context:
- MCP server connects Claude agents to Rhino (rhinomcp)
- Parametric scripts generate geometry with construction knowledge
- archibase has materials, assemblies, fire codes, structural data
- We need a way to tag Rhino objects with this data and visualize it (e.g., color by embodied carbon, label by material, highlight by fire rating)
- This is for rhinobase — the Rhino modeling knowledge layer
</context>

<instructions>

## Research tasks

### 1. Pattern extraction (read Rhyton source)
Understand their approach at the concept level:
- How do they store key-value data on Rhino objects? (which Rhino API — UserText, attributes, other?)
- How do they read it back?
- How do they map values to colors? (continuous gradient? discrete categories? custom schemes?)
- How do they handle color scheme persistence? (where is the scheme stored?)
- How do they revert objects to original appearance after visualization?
- How do they export data from geometry? (CSV, JSON — what's the extraction pattern?)

### 2. Survey of standard Rhino techniques
Independent of Rhyton, research:
- RhinoCommon `ObjectAttributes.SetUserString()` / `GetUserString()`
- Rhino document user text vs object user text
- `rhinoscriptsyntax.SetUserText()` — how it differs
- Layer-based data organization
- Display conduits for temporary visualization
- Rhino's built-in text dots

### 3. Design our implementation
Based on patterns learned + standard Rhino techniques, design an original system for rhinobase:
- How will archibase data get tagged onto geometry? (after script generation? during? on demand?)
- What data goes on each object? (material, assembly, LCA values, fire rating, structural load)
- How will agents query this data? (MCP tool? Python function?)
- How will visualization work? (color modes, labels, on/off toggle)
- How will data survive file save/reopen?

## Deliverable

Write `output/open-source-study/data_on_geometry_pattern.md`:

```markdown
# Data-on-Geometry — Pattern Study + Our Design

## Concept (general, not Rhyton-specific)
[The idea: structured metadata on 3D objects, queryable and visualizable. Standard technique across BIM/CAD tools]

## Available Rhino APIs
[UserText, attributes, layers, display conduits — what Rhino provides natively]

## Pattern observations
[What we learned about effective approaches from studying existing tools. No code, no attribution to specific unlicensed implementations]

## Our design: rhinobase data layer

### Data schema per object
[What key-value pairs we'd store. Namespace convention (e.g., `rb:material`, `rb:gwp`, `rb:fire_rating`)]

### Tagging workflow
[When and how data gets attached — during parametric generation, post-generation enrichment, or manual assignment]

### Query interface
[MCP tool spec for agents to read/filter/aggregate object data]

### Visualization modes
| Mode | What it shows | Color scheme |
|------|--------------|-------------|
| Material | Material type | Categorical palette |
| Carbon | Embodied GWP | Red→Green gradient |
| Fire | Fire rating | Code-standard colors |
| Assembly | Assembly type | Categorical |
| Custom | Any key | Auto-detect continuous vs categorical |

### Persistence
[How data survives save/reopen. How it stays in sync with archibase updates]

### MCP integration
[How this connects to existing rhinomcp tools. New tools needed?]

## Implementation plan
[Ordered steps to build this. What comes first, what can wait]
```

</instructions>

<verification>
- [ ] No code from unlicensed sources was copied or closely paraphrased
- [ ] Design uses standard Rhino APIs (UserText, attributes, display conduits)
- [ ] Namespace convention is defined with at least 6 key names
- [ ] MCP tool interface is specified (input/output, not just "we need a tool")
- [ ] At least 4 visualization modes designed
</verification>
