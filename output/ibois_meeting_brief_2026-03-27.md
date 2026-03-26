# IBOIS Meeting Brief — March 27, 2026
**Andrea Crespo | AR-302k (Studio Huang) | BA6**

---

## Who is IBOIS

IBOIS (Laboratory for Timber Constructions, EPFL) — Prof. Yves Weinand. They sit at computational geometry + digital fabrication + material intelligence. Key people:

- **Damien Gilliard** — PhD, AR-327 instructor, roundwood database (digital twins of individual trees with properties)
- **Andrea Settimi** — tool builder, Rhino-Python pipeline

Their tools: compas_wood (parametric timber joints), Manis (assembly constraints), Raccoon (CNC machine profiles), diffCheck (quality validation). AR-327 teaches exactly the pipeline our agents use: Python -> RhinoCommon -> BREP geometry.

---

## What City101 brings to the table

A **multi-agent coordination layer** for Rhino, proven in Lock 05 test: 7 specialist agents, 709 objects, inter-agent coordination via MCP. Plus a 4-layer construction knowledge system (archibase: SQLite + Markdown + Scripts + 35K RAG chunks).

Their tools are structured, parameterized knowledge. Our system can load that knowledge into specialist agents that operate in parallel. The missing piece: a shared ontology so different construction domains can talk to each other.

---

## Talking points

### 1. The tree database
> "Your roundwood database with digital twins of individual trees — is that queryable outside the Rhino plugin? Could an external system request 'give me trees 20-30cm diameter, <5 deg taper, harvestable'?"

*Why*: If it has an API or export path, it's immediately agent-integrable.

### 2. compas_wood parameters
> "In compas_wood, are the joint parameters documented as a reference table? Tenon min/max dimensions, clearances, grain constraints? We'd embed those into agent context."

*Why*: Asking if implicit knowledge is also explicit. Yes = reusable. No = research opportunity.

### 3. Fabrication constraints
> "With Raccoon, minimum radius, max depth, tool changeovers — is that externalized as a machine profile? Something that could validate geometry before it hits the CNC?"

*Why*: Opens the "fabrication agent" conversation.

### 4. The pitch
> "We've tested running 7 specialist AI agents on the same Rhino model simultaneously — each with different construction knowledge. Your course literally teaches RhinoPython; our agents run RhinoPython through MCP. Has AR-327 considered whether your parametric tools could work in that split-expertise setup?"

*Why*: Direct connection: their course = our agent fuel.

### 5. The research gap
> "Is there an ontology for timber construction knowledge — something like IFC but at the craft level? Joint types, material constraints, fabrication rules, assembly sequences all in one queryable structure?"

*Why*: This is the thesis-level question. Formalizing what compas_wood/Manis/Raccoon know into a declarative schema.

---

## What collaboration could look like

| Scale | Scope | Timeline |
|-------|-------|----------|
| Quick win | Document compas_wood joint params as reference tables, test loading into agent context | 4 weeks |
| Student project | "Multi-agent timber design" — AR-327 final project using Rhino Router + compas_wood | End of semester |
| Thesis | Formalize "construction knowledge as agent context" — unified schema across materials | Long-term |

---

## Key framing

You're not asking them to change what they do. You're proposing that their parameterized construction knowledge (already structured, already in code) becomes the foundation layer for specialist agents coordinating in real-time.

Their tools are the "law" (doctrine). Your agents are the "lawyers" (applying it). The gap: a shared ontology so they can talk to each other. That's the research contribution.
