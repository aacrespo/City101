# Build rhinobase — RhinoCommon Knowledge for Agent Fluency

## Context

Agents write RhinoPython through `rhino_execute_python_code` (MCP) but pick methods from training data — sometimes guessing wrong, sometimes missing better approaches. A structured knowledge base of the RhinoCommon API, patterns, and idiomatic solutions makes every Rhino script more reliable.

This is **rhinobase** — the modeling knowledge counterpart to archibase (construction knowledge). Same 4-layer pattern, different domain.

**Source:** https://developer.rhino3d.com/api/rhinocommon/
**Also:** McNeel developer guides, McNeel Discourse forum (RhinoPython threads)

## Layer architecture

| Layer | Storage | What goes here |
|-------|---------|----------------|
| L1 | SQLite (`rhinocommon.db`) | API reference: namespaces, classes, methods, properties, signatures |
| L2 | Markdown guides | Patterns, tutorials, when-to-use-what, common pitfalls |
| L3 | Python scripts | Reusable geometry operations (create, transform, boolean, analyze) |
| L4 | Vector DB (Qdrant) | Forum solutions, worked examples, idiomatic code snippets |

## Output structure

```
output/rhinobase/
├── rhinocommon.db           ← L1: SQLite API reference
├── README.md                ← overview + how agents use this
├── guides/                  ← L2: markdown
│   ├── 00_index.md
│   ├── 01_geometry_fundamentals.md    ← Point3d, Vector3d, Plane, Transform
│   ├── 02_curves.md                   ← Line, Arc, Polyline, NurbsCurve
│   ├── 03_surfaces_and_breps.md       ← THE hard one: Surface vs Brep vs Extrusion
│   ├── 04_mesh_operations.md          ← when Mesh beats Brep, conversion
│   ├── 05_booleans_and_splitting.md   ← BooleanUnion/Difference/Intersection, trim, split
│   ├── 06_transforms.md              ← Move, Rotate, Scale, Orient, Mirror, Project
│   ├── 07_layers_and_attributes.md    ← document management, colors, materials
│   ├── 08_performance_patterns.md     ← batch ops, when to commit, scriptcontext tips
│   └── 09_mcp_specific.md            ← patterns specific to working through rhino_execute_python_code
├── scripts/                 ← L3: reusable operations
│   └── (created in Phase 2, after L1/L2 exist)
└── chunks/                  ← L4: for Qdrant ingestion
    └── forum_solutions/     ← question + answer + code, tagged by topic
```

## Agent assignments

### Agent F — API Reference (L1)

Scrape the RhinoCommon API into SQLite:

```sql
CREATE TABLE namespaces (
    name TEXT PRIMARY KEY,
    description TEXT,
    class_count INTEGER
);

CREATE TABLE classes (
    name TEXT PRIMARY KEY,
    namespace TEXT REFERENCES namespaces(name),
    description TEXT,
    base_class TEXT,
    is_struct INTEGER,
    is_enum INTEGER
);

CREATE TABLE methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT REFERENCES classes(name),
    method_name TEXT,
    is_static INTEGER,
    is_constructor INTEGER,
    return_type TEXT,
    parameters TEXT,           -- JSON: [{name, type, description, default, is_optional}]
    description TEXT,
    remarks TEXT,               -- additional notes from docs
    example_code TEXT
);

CREATE TABLE properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT REFERENCES classes(name),
    property_name TEXT,
    type TEXT,
    readable INTEGER,
    writable INTEGER,
    is_static INTEGER,
    description TEXT
);

CREATE TABLE enums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enum_name TEXT,
    namespace TEXT,
    member_name TEXT,
    member_value INTEGER,
    description TEXT
);
```

**Priority namespaces** (scrape these first, they cover 90% of architectural scripting):

1. `Rhino.Geometry` — the core: Point3d, Vector3d, Plane, Transform, Line, Arc, Circle, Polyline, PolylineCurve, NurbsCurve, NurbsSurface, Brep, BrepFace, Mesh, Extrusion, BoundingBox, Interval
2. `Rhino.DocObjects` — ObjectAttributes, Layer, ObjectTable, adding/modifying objects
3. `Rhino.RhinoDoc` — ActiveDoc, Objects, Layers, Views
4. `Rhino.Geometry.Intersect` — Intersection class (curve-curve, curve-surface, surface-surface)
5. `Rhino.Geometry.Collections` — BrepFaceList, BrepEdgeList, MeshVertexList, etc.
6. `Rhino.Display` — DisplayMaterial, color (useful for visualization through MCP)

**Secondary namespaces** (scrape if time allows):
7. `Rhino.Geometry.Morphs` — space morphs, flow along surface
8. `Rhino.Input` — GetPoint, GetObject (less relevant for MCP, but contextually useful)
9. `Rhino.FileIO` — import/export formats
10. `Rhino.Commands` — Result enum

**Scraping approach:**
- The API docs are HTML pages organized by namespace → class → members
- Start from https://developer.rhino3d.com/api/rhinocommon/
- Each class page has: description, constructors, properties, methods, events, remarks
- Extract method signatures carefully — parameter types and defaults matter for script correctness
- If a method page has example code, capture it

### Agent G — Developer Guides (L2)

Write 9 markdown guides covering the core patterns. For each guide:
- What the pattern is (one paragraph)
- When to use it (decision criteria)
- Working code example (tested against API docs, uses real method signatures)
- Common pitfalls (things that silently fail or produce wrong geometry)
- Related RhinoCommon classes/methods (cross-reference to L1)

**Source material:**
- McNeel developer guides: https://developer.rhino3d.com/guides/rhinopython/
- RhinoCommon samples: any examples linked from the API docs
- The guides we already know from scripting experience

**Guide 03 (Surfaces and Breps) is the priority.** This is where agents fail most. The distinction between Surface, BrepFace, Brep, Extrusion, and when RhinoCommon silently converts between them — that's the knowledge gap. Cover:
- Brep = boundary representation = collection of faces, edges, vertices
- BrepFace wraps a Surface — you trim surfaces by putting them in Breps
- Extrusion is a lightweight Brep (faster but limited) — `IsExtrusion` check
- `Brep.CreateFromSurface()` vs `Brep.CreateFromMesh()` vs `Brep.CreatePlanarBreps()`
- Boolean operations require CLOSED Breps (solids) — the #1 silent failure

**Guide 09 (MCP-specific) is unique to us.** Cover:
- Scripts run through `rhino_execute_python_code` as string — no persistent state between calls
- Use `scriptcontext.doc` not `Rhino.RhinoDoc.ActiveDoc` (depends on context)
- Return GUIDs as strings for subsequent MCP calls
- Error handling: script failures in MCP return the traceback as a string
- Layer management: always check if layer exists before creating
- Batch operations: create all geometry, add all at once (fewer MCP round-trips)

### Agent H — Forum Idioms (L4 / Qdrant)

Scrape high-value McNeel Discourse threads into chunks for vector embedding:

**Search strategy:**
- McNeel Discourse: https://discourse.mcneel.com/
- Search terms: "RhinoPython", "rhinocommon", "scriptcontext", "python script"
- Filter by: has accepted answer or high-value replies (code blocks present)
- Categories: Scripting, Rhino Developer, RhinoCommon

**Chunk format:**
```json
{
  "question": "How do I create a lofted surface between curves?",
  "answer": "Use Brep.CreateFromLoft with the curves...",
  "code": "import Rhino.Geometry as rg\ncurves = [...]\nloft = rg.Brep.CreateFromLoft(curves, ...)",
  "topic_tags": ["surface", "loft", "brep"],
  "rhinocommon_classes": ["Brep", "NurbsCurve"],
  "source_url": "https://discourse.mcneel.com/t/...",
  "quality": "accepted_answer"
}
```

**Target:** 500+ chunks covering the most common operations.

**Priority topics** (by frequency of agent need):
1. Creating geometry: loft, sweep, extrude, revolve, pipe
2. Boolean operations: why they fail, how to fix
3. Curve operations: offset, fillet, join, split, divide
4. Surface operations: trim, split, project, closest point
5. Mesh↔Brep conversion: when and how
6. Transformations: orient, remap, project to plane
7. Document operations: layers, attributes, selection

**Fallback if forum scraping hits rate limits:** Curate 100 threads manually from the most common topics. Quality over quantity — 100 well-chosen examples beat 500 random ones.

## Success criteria

- **L1:** Priority namespaces fully scraped. An agent can query: `SELECT method_name, parameters, return_type FROM methods WHERE class_name = 'Brep' AND method_name LIKE '%Loft%'` and get the right signature.
- **L2:** All 9 guides written. Guide 03 (Breps) correctly explains the Surface/BrepFace/Brep/Extrusion distinctions. Guide 09 (MCP) covers the specific patterns for `rhino_execute_python_code`.
- **L4:** 500+ chunks tagged and ready for Qdrant ingestion. An agent searching "boolean union fails" gets threads about open vs closed Breps.
- **Integration test:** An agent that has never modeled before can query rhinobase to write a correct script that creates a lofted surface, adds it to a layer, and returns the GUID — without guessing method signatures.

## Attribution

RhinoCommon API documentation by Robert McNeel & Associates. Licensed under MIT.
McNeel Discourse content is CC-BY-SA or user-contributed — attribute threads to original authors.
