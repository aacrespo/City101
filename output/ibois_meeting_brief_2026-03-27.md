# IBOIS Meeting Brief — March 27, 2026
**Andrea Crespo | AR-302k (Studio Huang) | BA6**

---

## Who is IBOIS

IBOIS (Laboratory for Timber Constructions, EPFL) — Prof. Yves Weinand. They sit at computational geometry + digital fabrication + material intelligence. Key people:

- **Damien Gilliard** — PhD, AR-327 instructor, roundwood database. **Not an AI user at all** — thinks in geometry and Python, not agents. His PhD is literally about shape-aware design with real scanned trees.
- **Andrea Settimi** — tool builder, Rhino-Python pipeline
- **Petras Vestartas** — compas_wood author (joint generation)

Their tools (you've checked every repo):

| Tool | What | License | Can we extract? |
|------|------|---------|-----------------|
| compas_wood | Joint generation, 42+ types | MIT | Yes — already read the C++ |
| Manis | Assembly constraints, CNC toolpaths, robot trajectories | MIT | Yes |
| diffCheck | CAD-vs-scan quality validation | GPL-3.0 | Yes (data/thresholds only) |
| Cockroach | Point cloud processing (Open3D, CGAL, PCL) | LGPL-3.0 | Yes |
| Raccoon | CNC G-code, machine profiles, collision detection | **No license** | **Ask Damien** |
| catalogue-explorer | Web viewer for scanned objects | **No license** | **Ask Damien** |

AR-327 teaches the same pipeline: Python → RhinoCommon → BREP geometry.

---

## What you've already done (prep work)

- Read Damien's roundwood paper (48 trees, 11-point skeletons, shape-aware design method)
- Installed compas_wood, read the C++ source — found 42+ joint types, mapped the 3 configurable params, identified constraint values embedded in geometry code
- Checked every IBOIS repo on GitHub — licenses, languages, what's extractable
- Built a prompt to systematically extract knowledge from all 4 open-source tools into a unified database

## What City101 brings to the table

A system that takes construction knowledge from code and makes it queryable. We already have a database (archibase) with Swiss materials, structural loads, fire codes, steel profiles — 35K+ reference entries that scripts can look up at runtime. The same approach works for timber: extract the joint rules from compas_wood, the assembly logic from Manis, the quality tolerances from diffCheck, the point cloud pipeline from Cockroach — and connect them.

Right now each IBOIS tool is its own island. compas_wood doesn't know about Manis's assembly rules. Manis doesn't know about diffCheck's tolerances. The knowledge exists but isn't connected. We can build that connection layer.

---

## Talking points

### 1. The tree database
> "Your roundwood database — can you query it? Like, could I say 'give me trees 20-30cm diameter, under 5 degrees taper' and get results? Or is it more like a collection you browse manually?"

*Why*: Understanding what's queryable tells you what's automatable.

### 2. The point clouds and his PhD work
> "I read your paper on the roundwood design method — the 48 scanned trees reduced to 11-point skeletons. How far along is that? Can you already match a structural need to a specific tree in the database, or is that still the goal?"

*Why*: Shows you've done your homework. His paper (Gilliard & Weinand, 2025) already proposes exactly the material-first design loop — designing from what's available rather than specifying ideal sections. Don't pitch this idea to him. He invented it. Instead, ask where he is with it and what's missing.

> "The skeleton extraction — is that automated now, or does each tree still need manual cleanup? And what properties come out beyond geometry — do you get structural grades, or is that a separate step?"

*Why*: Understanding his pipeline's bottlenecks tells you where automation (your side) could actually help.

### 3. compas_wood — you already know the answer
You've looked at the code. Here's what you found:

**42+ joint types** across 7 categories: finger joints (in-plane/out-of-plane), tenon-mortise, butterfly/Hilti, cross-cutting, drilling, rotated, boundary. Each procedurally generated in C++.

**From Python you can control 3 things per joint category:**
- `division_length` — spacing between features (defaults: 300mm or 450mm)
- `shift` — offset along edge (0–1)
- `type_id` — which variant (0–69 index)

**Everything else is in the C++ source** (`wood_joint_lib.cpp`, ~6400 lines) — readable, but spread across geometry generation functions rather than collected in one place. Chamfer offsets (-0.75), tenon profiles in unit-space [-0.5, 0.5], division clamping (2–100), interpolation formulas. The knowledge is all there, it's just interleaved with the geometry code rather than sitting in a reference table.

> "I read through compas_wood's source — the joint generation is impressive, 42 types across 7 categories. I could see the constraint values in the C++ — the chamfer offsets, the tenon proportions, the division ranges. We've been extracting exactly that kind of embedded knowledge from code and organizing it into reference tables that a design tool can query. Would it be useful to do that for compas_wood?"

*Why*: You're showing you've already done the work of reading the code. And you're offering something concrete: turning knowledge that's scattered across 6400 lines of C++ into something structured and queryable. That's a contribution, not a request.

### 4. Raccoon licensing
> "I looked at Raccoon on GitHub — the G-code generation, the Tools.txt machine profiles. It doesn't have a license on the repo. Is that intentional, or just hasn't been added yet? We'd love to include the machine constraints in what we're building, but without a license we can't touch the code."

*Why*: Direct, respectful, necessary. Raccoon's `Tools.txt` (machine parameters as a config file) is exactly the kind of externalized knowledge that slots straight into L1. But no license = no permission. This is the one thing you actually need from them.

### 5. diffCheck + Manis
> "diffCheck and Manis are both MIT — we've looked at those too. The quality tolerances in diffCheck, the assembly sequencing in Manis. Have you ever wanted to connect those? Like, 'for this joint type, here are the design rules, the assembly order, the fabrication method, and the acceptable tolerance' — all in one place?"

*Why*: You're describing what you're literally building. And you're asking if they've wanted the same thing — which positions it as a shared problem, not your project alone.

### 6. The pitch (keep it grounded)
> "In AR-327 you teach students to write RhinoPython scripts that encode construction rules. We've been experimenting with having AI write and run those same kinds of scripts — you give it the rules, it generates the geometry. Basically automating what your students learn to do by hand. Could be interesting to try with compas_wood or the roundwood database."

*Why*: Frame it as "automating the student workflow," not "multi-agent coordination." Same thing, zero jargon.

### 7. The supply chain question
> "Something I keep thinking about — your scanned trees have a known origin, known properties. If you design with them, you can trace the material from the forest to the building. Has anyone quantified that? The ecological cost of roundwood vs glulam, not just in material terms but the whole chain — sourcing, transport, processing, waste?"

*Why*: This reframes his roundwood database from a geometry tool to a **material passport**. Each scanned tree is the start of a traceable supply chain. KBOB (Swiss LCA data) already has the carbon factors — connecting them to his trees is a research contribution neither of you could do alone.

> "Our project studies infrastructure supply chains along the Geneva–Villeneuve corridor. The buildings we're designing are on that corridor. If the timber comes from local forests — Jura near Nyon, say — we can quantify: how far does the material travel, what's the fabrication energy, what's the waste from working with irregular roundwood vs milled sections?"

*Why*: Grounds it in your actual project. Not hypothetical. The 9 relay-lock nodes sit along 89km of corridor with different local timber availability. Per-node supply chain comparison is a real deliverable.

### 8. The bigger question
> "You've built compas_wood for joints, Manis for assembly, Raccoon for fabrication, diffCheck for validation — but they're separate tools. Has anyone tried to connect them into one chain where a design decision flows all the way through to fabrication and you can measure the ecological cost at every step?"

*Why*: Same question as before, but now it ends with the ecological dimension. That's the hook that makes it more than a software integration problem.

---

## What collaboration could look like

| Scale | Scope | Timeline |
|-------|-------|----------|
| Quick win | Extract compas_wood + Manis + diffCheck + Cockroach into a unified reference database. Share the CSVs with IBOIS — "here's your own knowledge, organized." | 4 weeks |
| Next step | Connect the roundwood database: scan → skeleton (Cockroach) → properties (L1) → match to structural need → joint selection (compas_wood) → quality check (diffCheck). One loop, real trees. | 6-8 weeks |
| Student project | AR-327 final project: AI-assisted roundwood design using Damien's 48-tree database | End of semester |
| Research | The connection layer + ecological quantification: traceable material passports from forest to building, per-lock supply chain comparison, roundwood vs glulam lifecycle | Long-term / thesis |

---

## Key framing

**Damien is not an AI person.** No ChatGPT, no agent experience. He's a computational geometry researcher who writes Python and works with point clouds. Don't lead with "agents" or "MCP" — lead with what his data could *do* that it can't do now.

The angle: "You have scanned trees with real geometry. Right now that data lives in a database. What if a design tool could automatically match structural needs to your actual scanned inventory — pick the right tree for the right beam, adapt the joint to the real taper? That's what we're building."

Frame the AI part as automation of what a skilled person would do manually: look at available wood, assess its properties, decide where it fits in the structure. The computer just does it faster and across more options simultaneously.

Don't say "agent." Say "script that knows about timber" or "automated assistant" or just "the system." Meet him where he is.
