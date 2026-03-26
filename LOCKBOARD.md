# Lockboard
**Updated**: 2026-03-25

**Friday March 27 (screen test with Alex) / Monday March 30 (midterm presentation)**

---

## Andrea — Tasks

### Emails — DONE
- [x] Email EPFL RCP re: VM services — sent
- [x] Email ENAC re: Rhino licenses — sent. **APPROVED** (Sébastien). Need VM computer name to activate via LAN Zoo → mcneellic.epfl.ch

### Presentation (Slides)
- [ ] **Slide 5 — Workflow**: Kitchen analogy animation (repo = kitchen, scripts = recipes, DB = ingredients). Pixel agents. Parallel axonometry showing VM vs MCP vs teams. Explains: what happens when you start a session in this repo. v1 animated overnight, needs iteration.
- [ ] **Review canonical kitchen story** — `observations/research/strategy/kitchen_analogy_canonical.md` — review brigade mapping + three pillars before animating further
- [ ] **Slide 5 — Pixel agents concept**: Commander board for architects/construction. Show agents modeling, building. Sister designing character angles (blocker — fallback: show VS Code pixel agents feature + explain vision).
- [ ] Claude character emotes v2 — Blender modeling + render PNGs for gifs/animations. v1 done.
- [ ] Healthcare diagram — animated merry-go-round with time

### Modeling
- [ ] **Rennaz node (Lock 07)** — model with site (Andrea's 1 of 3 site models). Scripts exist (v1–v3).
- [x] Generate "before" scripts for Crissier-Busigny + Nyon-Genolier — **DONE** (v0 scripts, LOG 200, no archibase)

### Infrastructure
- [x] ChromaDB → Qdrant migration — **DONE** (2026-03-25)
- [ ] Continue embedding: YouTube videos + remaining docs with Gemini API — **running overnight March 26**
- [x] Workflow hygiene — token optimization **DONE** (modeler -1200 tokens, pdf refactored, memory trimmed)
- [x] Auto dream — **SKIPPED** (curated memory system better)
- [ ] Set up `/loop` command
- [x] DeepSeek — **PARKED** for app phase
- [x] Integrate Ruflo — **DONE** (agent-team-modeling-v3.md)
- [ ] Lock the lock files — **PARKED** for after midterm

---

## Henna — Tasks

### Modeling
- [ ] **Finish corridor model** — verify geometry works in QGIS → Rhino pipeline (ask Claude to verify)
- [ ] **Model 9 écluse types** (without site)
- [ ] **Model Crissier-Busigny node** (with site) — Henna's 1 of 2
- [ ] **Model Nyon-Genolier node** (with site) — Henna's 2 of 2

### Presentation
- [ ] Redo presentation format — aesthetics, transitions, PowerPoint
- [ ] **Slides 2-3 — Chambre-Lock concept**: All content — diagrams + write speech (2 slides)
- [ ] **Slide 4 — Software architecture**: One big diagram of app info flow + architecture. Gif with highlighted steps if possible.
- [ ] **Slide 5 (partial) — Before/after workflow**: Compare how we worked before vs now. Explain agent interactions, Claude-Rhino MCP, Blender MCP, router architecture. Visual diagrams.
- [ ] **Slide 6 — Archibase**: Explain the knowledge base architecture

---

## Presentation Structure

| Slide | Content | Owner |
|---|---|---|
| 1 | Header / title | Shared |
| 2-3 | Écluse concept — diagrams + speech | Henna |
| 4 | Software architecture — app info flow diagram (gif) | Henna |
| 5 | Workflow — kitchen analogy animation, pixel agents, parallel axo, before/after | Andy (animation) + Henna (before/after diagrams) |
| 6 | Archibase — knowledge base explanation | Henna |
| 7-10 | 3D models (4 slides, order TBD) | Shared |
| 11 | Vision — what's next, scaling, roadmap | Shared |

---

## Nice-to-Have (post-midterm, or if budget allows)

- [ ] **rhinobase + iboisbase** — PM project `rhinobase-iboisbase`. Plan at `state/pm/rhinobase-iboisbase/`. 4 phases, 8 agents, ~4 hrs. Even compas_wood + RhinoCommon API alone would strengthen slide 6.

## Agent / Autonomous Tasks (can run without Andrea)

- [ ] "Before" Rhino scripts for Crissier-Busigny + Nyon-Genolier
- [ ] Blender character emotes v2 rendering (once designs confirmed)
- [ ] Embedding pipeline (ChromaDB stable — Qdrant migration on hold)
- [ ] Kitchen analogy animation iteration (Blender)

---

## Open Blockers

1. **EPFL VM access** — emails sent, waiting on RCP response. Need VM computer name for Rhino license activation (LAN Zoo → mcneellic.epfl.ch)
2. **Andrea's Sister's pixel agent designs** — fallback: VS Code demo + explain vision
3. **Henna needs Blender MCP + router setup** — Rhino multi-instance working, Blender not yet configured
4. **Ramp grades** — Lock 03 Morges scripts still too steep for SIA 500. Needs fix.
