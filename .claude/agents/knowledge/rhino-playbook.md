# Rhino Modeling Playbook

## How this knowledge system works

This playbook uses a legal framework to organize modeling knowledge:

| Concept | What it is | Where it lives | When to read |
|---------|-----------|----------------|--------------|
| **Law** | Non-negotiable external facts: building codes (SIA, VKF), material physics, archibase specs | `~/CLAUDE/archibase/` (DB + knowledge files) | When you need exact numbers or material properties |
| **Doctrine** | Our modeling principles — how we approach every build | **This file** | Every session, before building |
| **Jurisprudence** | Precedents from past builds — how doctrine was applied, what worked, what failed | `.claude/agents/knowledge/learnings-*.md` | When facing a specific problem similar to a past build |

**Doctrine is short and universal.** If you find yourself writing a specific dimension, a material name, or a build-specific solution in this file, it belongs in jurisprudence (learnings) or law (archibase) instead.

---

## Doctrine

### 1. Everything has a thickness

Nothing is just a surface. A wall is a sequence of layers. A roof is a stack of materials. A floor is an assembly. If you model anything as a zero-thickness surface, you have failed the section test. Every element in a building has material, thickness, and assembly logic.

### 2. Model assemblies, not surfaces

Query archibase for the assembly layers before modeling any element. If the assembly doesn't exist in the database, read the knowledge markdown and construct it from material properties and design rules. Each layer becomes a separate object with material metadata.

### 3. The section test is the gold standard

Put a clipping plane through your model. Read the section bottom to top. Can you identify every layer? Does every material have credible thickness? If you see a single rectangle where there should be layers, or a zero-thickness line where there should be a solid, go back and fix it.

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

### 10. Discover while building

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

---

*Doctrine distilled from cabin v1 (rammed earth, 76 objects), v2 (rammed earth, 87 objects), and v3 (stone + timber frame, 933 objects). Jurisprudence lives in the learnings files. Law lives in archibase.*
