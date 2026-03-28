# Phase 1A: LCA Schema Study (HdM Calc)

**Project:** open-source-study
**Status:** ACTIVE
**Estimated:** ~45 min (runs parallel with Phase 1B)
**License:** MIT — can use directly

---

<context>
You are studying HdM Calc (Herzog & de Meuron's early-stage LCA tool) to understand how a production architecture firm structures the path from building assemblies to environmental impact numbers.

HdM Calc is MIT-licensed C# (.NET). It uses KBOB data — the same Swiss LCA dataset we already have in archibase's L1 SQLite layer (375 materials with embodied carbon, grey energy, UBP scores).

Our current state:
- archibase L1 has KBOB materials in SQLite: material_id, name_de, name_fr, density, gwp_total, gwp_production, penrt, ubp, group, unit
- We have no assembly→material mapping yet
- We have no calculation pipeline from geometry → materials → impact
- The fabrication-bridge project needs this: roundwood as material passport, per-lock supply chain comparison

What we need from this study: their data model for how assemblies are defined, how materials are referenced, how impacts are calculated and stored.
</context>

<instructions>

## Research tasks (no code writing)

### 1. Schema analysis
Read the HdM Calc source code (github.com/herzogdemeuron/calc). Focus on:
- How do they define an **assembly**? (layers, materials, thicknesses — what's the data model)
- How do they reference **KBOB materials**? (UUID, version, language — match against our SQLite schema)
- How do they calculate **impact**? (which KBOB values, what formulas, per-area or per-volume)
- What's a **snapshot**? (their output format — JSON structure, what's stored)

### 2. Interface design
- How does geometry (Revit elements) connect to assemblies?
- Is the mapping manual or automatic?
- What metadata lives on the geometry vs in a separate database?
- How does Directus fit in? (their material database backend)

### 3. Comparison with archibase
- Map their KBOB field names to our SQLite column names
- Identify gaps: what do they store that we don't? What do we have that they don't?
- Their assembly concept vs our current flat material table

## Deliverable

Write `output/open-source-study/lca_schema_comparison.md`:

```markdown
# LCA Schema Comparison — HdM Calc vs Archibase

## HdM Calc architecture
[How it works end-to-end: geometry → assembly → materials → impact → snapshot]

## Assembly data model
[Their schema for defining assemblies. Field names, types, relationships]

## KBOB reference pattern
[How they identify and version KBOB materials. Compare with our SQLite columns]

## Calculation pipeline
[Formulas, units, what goes in, what comes out]

## Snapshot format
[Their output JSON structure — what a completed LCA result looks like]

## Field mapping
| HdM Calc field | Archibase L1 field | Notes |
|----------------|-------------------|-------|
| ... | ... | ... |

## Gaps
| What | HdM has | We have | Action |
|------|---------|---------|--------|
| ... | ... | ... | Add / Skip / Later |

## Proposed assembly table for archibase
[Based on what we learned — a concrete SQLite schema proposal for an assembly table that connects to our existing KBOB materials]

## Impact on fabrication-bridge project
[How this schema feeds into per-lock supply chain comparison]
```

</instructions>

<verification>
- [ ] Field mapping table has at least 8 entries
- [ ] Gaps table identifies what we need to add to archibase
- [ ] Proposed assembly table is a concrete CREATE TABLE statement, not prose
- [ ] Referenced specific files/classes in HdM Calc source
</verification>
