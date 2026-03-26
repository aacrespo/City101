# Fabrication Bridge — From Design Intent to Physical Object

## The gap

Right now the knowledge system covers two ends:
- **Design end**: archibase (what's allowed structurally) + iboisbase (how joints work)
- **Representation end**: rhinobase (how to model it in Rhino)

What's missing is the middle: **how does a design become a physical object?** That's not one question — it's a chain:

```
Design intent
  → What material? (species, grade, dimensions)
    → Where does it come from? (forest, sawmill, supplier)
      → How far does it travel? (transport, CO2)
        → How is it processed? (CNC, robot, hand)
          → What are the machine constraints? (Raccoon)
            → In what order is it assembled? (Manis)
              → How do you verify quality? (diffCheck)
                → Physical object
```

That chain is the **circuit d'approvisionnement** — the supply circuit. And every step has an ecological footprint.

## Why this matters for City101

The relay-lock project studies supply chains: medicine, staff, patients moving through the corridor. The 01:30-03:30 dead window breaks the healthcare chain.

The fabrication bridge says: the locks themselves are a supply chain. The timber for Lock 03 Morges — where does it come from? If it's IBOIS roundwood from a local forest, scanned with Cockroach, matched to structural needs from iboisbase, fabricated with constraints from Raccoon — that's a traceable, local, ecologically quantified supply chain. The building embodies the same infrastructure logic it houses.

**The lock holds the gap. The supply chain holds the lock.**

## The ecological dimension

Archibase already has KBOB data — 375 Swiss LCA entries for construction materials. That's the carbon cost of material choices. What's missing:

| Stage | What's quantifiable | Data source |
|-------|-------------------|-------------|
| **Material** | Embodied carbon per m³ of timber species | KBOB (already in archibase L1) |
| **Sourcing** | Distance from forest to site | Swiss forestry data + GIS |
| **Transport** | CO2 per ton-km by mode | KBOB transport factors |
| **Processing** | Energy per CNC operation | Raccoon machine profiles (if licensed) |
| **Assembly** | On-site energy, crane hours, labor | Manis assembly sequences + estimates |
| **Waste** | Offcut volume from irregular roundwood | Compas_wood joint geometry → material efficiency |

The roundwood angle is especially interesting: roundwood uses the tree AS-IS. No sawmill, no lamination, no glue. The supply chain is: forest → scan → design → CNC → assemble. Compare that to glulam: forest → sawmill → drying → lamination → glue → press → transport → cut → assemble. Every step adds CO2 and cost.

Damien's 48 scanned trees aren't just geometry — they're the start of a traceable material passport. Each tree has a known origin, known properties, and a design tool that can match it to a structural role. That's a supply chain you can quantify from root to building.

## What fabbase would hold

| Layer | Content |
|-------|---------|
| L1 (SQLite) | Machine profiles (from Raccoon, if licensed), CNC operation costs (time, energy), transport factors (from KBOB), material passports (tree ID → properties → structural role → lock node) |
| L2 (Markdown) | Fabrication guides: CNC workflow, assembly sequencing, quality checkpoints. Supply chain documentation: sourcing options, transport modes, waste streams. |
| L3 (Code) | G-code generation scripts (from Raccoon), assembly sequence optimizer (from Manis), material efficiency calculator (joint geometry → offcut volume), LCA aggregator (sum ecological cost across the chain) |
| L4 (Qdrant) | Fabrication case studies, supplier data, forestry inventories |

## Connection to IBOIS tools

```
Cockroach ──→ scan tree ──→ point cloud
                              ↓
compas_wood ──→ match to structural need ──→ joint design
                              ↓
Manis ──→ assembly sequence ──→ fabrication plan
                              ↓
Raccoon ──→ G-code ──→ CNC/robot execution
                              ↓
diffCheck ──→ scan result ──→ quality verification
                              ↓
                         PHYSICAL OBJECT
```

Each arrow is a data handoff. Each tool contributes knowledge to a different stage. The fabrication bridge is the chain that connects them — and at every link, you can ask "what's the ecological cost?"

## Connection to the corridor

The 9 relay-lock nodes are spread across 89km. Each site has different:
- **Local timber availability** (Jura forests near Nyon vs lake-adjacent near Vevey)
- **Transport distances** (sawmill proximity, rail vs road)
- **Fabrication access** (IBOIS CNC is in Lausanne — how far to each lock site?)
- **Assembly constraints** (urban site in Lancy vs hillside in Genolier)

A fabbase that tracks these per-node would let you compare: "Lock 03 Morges with local roundwood vs imported glulam — what's the carbon difference?" That's a quantified architectural argument, not just a design preference.

## When to build this

**Not now.** This is thesis-scale work. Prerequisites:
1. rhinobase + iboisbase built (knowledge base expansion project)
2. Raccoon licensed (ask Damien tomorrow)
3. At least one lock modeled to LOG 400+ (needs real material assignments)
4. Swiss forestry data sourced (where are the forests along the corridor?)

**First testable moment:** When Lock 07 Rennaz reaches material assignment stage. Pick timber elements, trace them through the chain, calculate the ecological cost. One lock, one supply chain, proof of concept.

## For the IBOIS meeting

This reframes the collaboration beyond "we extract your tools." It becomes: "your scanned trees are the start of a traceable material passport — from forest to building, ecologically quantified. Your tools provide the knowledge at every stage. We provide the system that connects them."

That's a research contribution, not a student project.
