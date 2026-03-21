# Proof of Concept: Archibase + Agent Team → Rhino Geometry

## What this proves

A team of specialized Claude agents can:
1. Query a construction knowledge base (archibase) for real material properties, structural constraints, and Swiss norms
2. Use those constraints to generate parametric geometry in Rhino via MCP
3. Coordinate with each other through shared layers and coordination geometry

This is the demo moment: "every dimension has a source, every constraint is enforced in code, and a team of agents built it together."

## Before you start

### 1. Switch MCP config to router

Edit `.mcp.json` in the city101 repo root:

```json
{
  "mcpServers": {
    "rhino_router": {
      "command": "uv",
      "args": ["run", "experiments/rhino mcp server/rhino_router_mcp.py"],
      "env": {
        "RHINO_INSTANCES": "{\"main\": 9002}"
      }
    }
  }
}
```

### 2. Start Rhino with custom port

In Rhino, run command: `mcpstart`
When prompted for port: type `9002` and press Enter.

> If Rhino says "unknown command mcpstart": the forked plugin isn't installed.
> Check `experiments/rhino mcp server/SETUP.md` for installation steps.
> The fork is at `aacrespo/rhinomcp`, branch `feature/configurable-port`.

### 3. Restart Claude Code

The MCP config only loads on startup. Restart Claude Code after editing `.mcp.json`.

### 4. Verify connection

Ask Claude to run:
```
rhino_list_instances()  → should show "main" on port 9002
rhino_get_document_summary(target="main")  → should return doc info
```

## The test

### Element: Rammed earth wall segment

Why this element:
- Archibase has rich data on rammed earth (L1: KBOB materials, L2: earth guide, L4: Dicobat terms)
- It has real structural constraints (min thickness, max height-to-thickness ratio, max unsupported length)
- It has environmental data (GWP comparison vs concrete)
- It's one of the project's material strategies

### Agent team (3 agents, minimal)

**Agent 1 — Knowledge Agent**
- Role: Query archibase for all constraints needed for a rammed earth exterior wall
- Queries:
  ```python
  import sys
  sys.path.insert(0, '/Users/andreacrespo/CLAUDE/archibase')
  from tools.knowledge_db import ConstructionDB
  from tools.dicobat_query import DicobatRAG

  db = ConstructionDB()
  # Material properties
  earth = db.get_material('earth_rammed')
  # LCA data
  kbob = db.get_kbob('terre')
  # Fire requirements (if available)
  fire = db.get_fire_requirement('habitation', 'low', 'mur_porteur')
  # Loads
  loads = db.get_load('A1')

  # RAG for deep knowledge
  rag = DicobatRAG()
  context = rag.query_for_context("pisé mur porteur terre crue", top_k=5)
  ```
- Also read: `~/CLAUDE/archibase/source/knowledge/materials/rammed_earth.md`
- Output: a constraints dict that Agent 2 consumes

**Agent 2 — Geometry Agent**
- Role: Generate the wall in Rhino using constraints from Agent 1
- Target: `target="main"`
- Creates:
  - Layer tree: `POC::Structure`, `POC::Annotations`
  - Wall segment (box or extruded rectangle): width from constraints, height from floor-to-floor
  - Wall courses (horizontal lines showing rammed earth layer heights, typically 60-80cm)
  - Metadata on every object (material, source norm, constraint value)
- Enforces: min thickness, max h/t ratio, max unsupported length — raises error if violated

**Agent 3 — Reviewer Agent**
- Role: Check the built geometry against the constraints
- Reads the Rhino model state via `rhino_get_objects(target="main", layer_filter="POC")`
- Verifies: dimensions match constraints, layers are correct, metadata is present
- Reports: pass/fail per constraint, with the source (SIA norm, KBOB, L2 guide)

### Success criteria

- [ ] Knowledge agent returns real numbers from archibase (not hardcoded)
- [ ] Geometry agent builds a wall in Rhino with correct dimensions
- [ ] Every dimension traces to a source (db query result, L2 guideline, or design decision)
- [ ] Reviewer confirms constraints are met
- [ ] Viewport capture shows the built geometry

### Expected output

A single wall segment in Rhino with:
- Correct rammed earth thickness (~40-60cm for load-bearing exterior)
- Course lines showing construction layers
- Object attributes linking each dimension to its knowledge source
- A viewport capture saved to `output/city101_hub/poc_archibase_wall.png`
- A summary markdown at `output/city101_hub/poc_archibase_results.md`

## After the test

If it works, this proves the full loop:
```
archibase (knowledge) → agent team (reasoning) → Rhino MCP (geometry)
```

The app becomes the interface that triggers this loop for any site, any material strategy, any program. The agents are the company behind the curtain.

### What to show Huang

"We have a knowledge base with 35,000+ construction references — Swiss norms, KBOB materials data, Dicobat terminology, structural tables. When our agents design, they don't guess dimensions. They query. Every wall thickness comes from SIA, every GWP value from KBOB, every fire rating from VKF. And they build it in Rhino, together, coordinating across layers. This is what the app orchestrates."

## Fallback: single-agent test

If the router isn't working or time is short, you can test knowledge → geometry with a single agent:

1. Keep the standard `.mcp.json` (`uvx rhinomcp`, port 1999)
2. Run `mcpstart` in Rhino (default port)
3. Use `/parametric` skill directly — it already knows how to query archibase
4. Ask it to generate a rammed earth wall with knowledge-grounded constraints

This proves the knowledge bridge works even without the agent team coordination layer.
