# Rhino Modeling Playbook

## How this knowledge system works

This playbook uses a legal framework to organize modeling knowledge:

| Concept | What it is | Where it lives | When to read |
|---------|-----------|----------------|--------------|
| **Law** | Non-negotiable external facts: building codes (SIA, VKF), material physics, archibase specs | `~/CLAUDE/archibase/` (DB + knowledge files) | When you need exact numbers or material properties |
| **Doctrine** | Our modeling principles — how we approach every build | **This file** | Every session, before building |
| **Jurisprudence** | Precedents from past builds — how doctrine was applied, what worked, what failed | `.claude/agents/knowledge/learnings-*.md` | When facing a specific problem similar to a past build |

**Doctrine is short and universal.** If you find yourself writing a specific dimension, a material name, or a build-specific solution in this file, it belongs in jurisprudence (learnings) or law (archibase) instead.

**The pieces are known. The composition is the creative act.** Law, doctrine, and jurisprudence are not separate silos — they are combined to create something new. A lawyer doesn't invent statutes; they compose existing law, principles, and precedent into novel arguments. An architect doesn't invent materials; they compose known systems into buildings that never existed before. The unique contribution is always in the combination — how you bring the pieces together for a specific site, program, and set of constraints.

---

## Doctrine

### 1. Everything has a thickness

Nothing is just a surface. A wall is a sequence of layers. A roof is a stack of materials. A floor is an assembly. If you model anything as a zero-thickness surface, you have failed the section test. Every element in a building has material, thickness, and assembly logic.

### 2. Model assemblies, not surfaces

Query archibase for the assembly layers before modeling any element. If the assembly doesn't exist in the database, read the knowledge markdown and construct it from material properties and design rules. Each layer becomes a separate object with material metadata.

### 3. The section test is the gold standard

Put a clipping plane through your model in BOTH directions — cut along X and cut along Y. Problems hide in the direction you didn't check. A corner gap, a transition hole, a missing seal — these are often only visible in one orientation. Read each section bottom to top. Can you identify every layer? Does every material have credible thickness? If you see a single rectangle where there should be layers, or a zero-thickness line where there should be a solid, go back and fix it.

### 4. The envelope must be continuous

Trace a single line around the building section — from foundation, up through walls, across the roof, and back down. This is the thermal envelope. Any break in this line is a failure. Every agent must know WHERE their system meets the envelope and ensure continuity. This applies at:
- Material transitions (capillary breaks + thermal seals)
- Corners (wind barrier wraps — insulation is never exposed)
- Penetrations (fire-rated collars at every assembly layer crossing)
- Openings (reveals and frame seals close every hole)
- Floor-wall junctions (fire stops, rim boards, blocking)

### 5. Connections are where architecture happens

Model the CONNECTION between systems, not just the elements on each side. The joint between wall and foundation, between stone and timber, between rafter and wall plate — these are where buildings succeed or fail. If two systems meet and you haven't modeled what happens at the interface, you've left the hardest problem unsolved.

### 6. Corners are continuous, like rings

Think of rammed earth courses — they wrap the full perimeter as monolithic rings. Apply this principle everywhere. At timber frame corners: wind barrier wraps, a corner post provides structure, insulation stops at the post. At material transitions: seal elements must patch the corner gap. An exposed corner is always wrong.

### 7. Openings are more than voids

An opening is not a hole — it's a complete system: lintel with bearing, frame, leaf/glass, reveals, threshold/sill, hardware. Every layer of the wall assembly must be split at the opening — structure, finish layers, insulation, vapour barrier. The opening must close the thermal envelope at its perimeter.

### 8. Structure before envelope before detail

Build in this order. Structure publishes its geometry (column positions, slab edges, wall tops). Envelope agents build to the structure. Detail agents (openings, circulation) build into the envelope. This is the dependency chain — violating it causes misalignment.

### 9. Every object has identity

Name every object (`Element_Level_Location_SubElement`). Tag every object with material metadata. Use distinct layer colors for section legibility. An unnamed, untagged object is invisible to review and useless for downstream work.

### 10. No overlaps — ever

Two solids cannot occupy the same physical space. This is non-negotiable. In real construction:
- **Stacking**: layers sit ON TOP of each other (tiles, roof layers, floor layers). No interpenetration.
- **Joinery**: one piece fits INTO another through a cut void (mortise-tenon, dado, notch). The void must be boolean-cut from the receiving piece BEFORE the inserted piece is placed.
- **Butting**: pieces meet face-to-face with a gap (mortar joints, expansion gaps). Never overlapping.

If you boolean-intersect any two objects in the model and get a non-zero volume, you have an overlap. Fix it by cutting the receiving piece or adjusting positions. This applies everywhere: wall corners, frame-in-wall, tread-on-stringer, shelf-in-panel.

**Duplicates count as overlaps.** Two identical objects at the same position are the worst kind of overlap — 100% interpenetration. After every boolean operation, verify you haven't left the original behind. Check: same bounding box + same layer = duplicate. Delete the pre-cut original, keep the modified version. Run a duplicate scan before declaring any model clean.

### 11. Nothing floats

Every object must bear on, attach to, or be fastened to something else. Gravity exists. A shelf must rest in its dado or on a cleat. A rafter must sit on a wall plate. A tread must rest in a stringer notch. A leg must touch the floor or touch a rail that touches something that touches the floor. If an object has air below it and no visible connection holding it up, it's wrong.

Verify: for every object, ask "what is holding this up?" If the answer is "nothing," fix it — either move it into contact or model the connection.

### 12. Discover while building

Query the law (archibase) for assemblies and material properties. Read the jurisprudence (learnings) for techniques from past builds. But when you encounter a problem that has no precedent — like a new material transition or an unusual connection — design the solution. Document what you discover in your learnings file so it becomes jurisprudence for the next build.

---

## Rhinoscriptsyntax Essentials

```python
# Box helper — define at top of EVERY script (state doesn't persist)
def box(x, y, z, L, W, H):
    pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
           (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
    return rs.AddBox(pts)
```

- `rs.CurrentLayer("Parent::Child")` before EVERY creation block
- `rs.SetUserText(obj, "material", value)` on EVERY object
- `rs.ObjectName(obj, name)` on EVERY object
- Break builds into 3-5 separate `rhino_execute_python_code` calls
- Print summary at end of each script (object count, key dimensions)
- For booleans: name AFTER, not before. Pick result by volume, not index. Clean orphans.
- For voids: verify with `rs.SurfaceVolume()` or `rs.IsPointInSurface()`, not bounding boxes.

---

## Review: Two Modes, Both Mandatory

**Mode A — Constraints**: section test, envelope trace, interface alignment, object count, material metadata, code compliance.

**Mode B — Visual coherence**: does it LOOK like the intended building type? Proportions, silhouette, opening rhythm, roof pitch, overhang. Compare against a mental reference of the building type — not just against numbers.

Neither mode alone is sufficient.

### Review hygiene

- **Clipping planes**: DELETE all clipping planes after section tests. They clip the perspective viewport and block visual review. Never leave them behind.
- **Wireframe for joints**: Use wireframe or high-contrast layer colors when reviewing connections (mortise-tenon, corner joints). Shaded perspective makes adjacent same-color objects indistinguishable.
- **Orthographic for patterns**: Front/right orthographic views are far more informative than perspective for reviewing wall bond patterns, coursing, and layer stacks.
- **Volume-based clearance analysis**: Compare tenon volume vs mortise pocket volume to verify fit without needing boolean intersection tests.
- **Blondel rule: going, not tread depth**: The Blondel formula (2R+G = 60-65cm) uses the going (distance between riser faces), NOT the tread depth. Nosing overhang is excluded. A 27cm going with 4cm nosing = 31cm tread, but G=27 for Blondel.
- **Corner layers need corner pieces**: Each wall layer's corner requires an explicit corner piece (square infill) where two arms meet. Arm lengths must be adjusted to avoid overlap.
- **Sill replaces bottom reveal**: In window assemblies, the stone sill serves as the bottom reveal — don't model both.
- **Top/plan views for envelope checks**: Plan section views are essential for verifying continuous insulation wrapping at corners.
- **Boolean voids vs solid objects**: Weatherstrip grooves, mortise pockets, and other voids are modeled as boolean cuts, not separate solids. An empty layer for a void element is correct — the void lives in the parent object's geometry.
- **Counter-batten = ventilation gap**: The counter-batten height IS the ventilation gap dimension. No separate "air gap" object needed.
- **Tile arrays dominate object count**: A 50cm roof strip generates 33 tiles. Plan for this when estimating object counts for full buildings.
- **Chair back legs as structure**: Back legs extending above seat height to form backrest supports is the canonical joinery pattern for simple timber chairs.
- **Monolithic vs discrete rule**: Poured concrete, steel, glass, and membrane sheets are correctly modeled as single solids. Masonry, tiles, timber boards, battens, insulation boards, hollow blocks, and joists MUST be modeled as individual discrete pieces. If you laid/placed/coursed it in real construction, model each piece separately.
- **Duplicate cleanup after every build**: Prior build attempts leave orphan objects. After every exercise, audit each layer for overlapping bounding boxes and delete extras. Two objects at the same position = delete one. This is the #1 failure mode in team builds.
- **State doesn't persist between scripts**: Redefine the box helper, imports, and any variables in every `rhino_execute_python_code` call. Nothing carries over.
- **Print object counts**: After every script run, print the count of objects created. Empty exercises (0 objects despite "complete" status) are a real failure mode — verify geometry exists.
- **Tag metadata immediately**: `rs.ObjectName()`, `rs.SetUserText("material", ...)`, and `rs.SetUserText("thickness_mm", ...)` on every object at creation time. Untagged objects get lost in team builds.
- **Agree on layer prefix before starting**: Layer naming mismatches (e.g., `TrainingS3::` vs `Training{Phase}::`) cause reviewers to find "empty" exercises that actually have geometry. Establish convention before first build.
- **Containment is not overlap**: Mineral wool inside a box-section stringer, or insulation between joists, is containment — not a Law 2 violation. Evaluate each bounding-box overlap for architectural justification before flagging.
- **Discrete element dimensions**: Brick course = 62.5mm + 12.5mm mortar = 75mm. Insulation board = 600mm wide + 2mm gap. Shingle = 80mm wide, 150mm exposed. Floor tile = 300×300mm + 2mm grout. Batten = 50×30mm at 400mm centers.

---

*Doctrine distilled from cabin v1–v3, full training session (10 exercises, 6 furniture scripts, 418 objects across 4 phases), and training-s3 session (63 exercises, 2989 objects, 6 agents, 189 tasks). Jurisprudence lives in the learnings files. Law lives in archibase.*
