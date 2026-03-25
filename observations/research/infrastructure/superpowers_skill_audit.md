# PROMPT: Superpowers Integration Audit for City101

## Your task

You are helping Andrea — an EPFL BA6 Architecture student — integrate Jesse Vincent's **Superpowers** plugin (https://github.com/obra/superpowers) into the City101 multi-agent repository and design custom architecture-specific skills that extend it.

Andrea's role has evolved beyond architecture into systems engineering: she manages a multi-agent AI workflow (4 Claude accounts × 2 interfaces each = 8 agent slots), coordinates with a partner (Henna), writes data pipelines, builds interactive visualizations, operates QGIS/Rhino/Chrome via MCP, and is writing a research paper about this exact workflow ("From Codebase to Corridor: Agentic AI Workflows for Architectural Design"). The workflow *is* the design contribution as much as the architectural outputs.

---

## Phase 1 — Understand what exists

### 1A. Read the repo

Start by reading the full repo structure and these key files:

```
CLAUDE.md                          ← Current governance/router file
LOCKBOARD.md                       ← Current task coordination
.claude/skills/                    ← Any existing skill files
.claude/commands/                  ← Any existing command files
process/SYSTEM_ARCHITECTURE_*.md   ← Latest system architecture spec (find highest version)
scripts/                           ← Existing data/viz/qgis scripts
datasets/inventory.md              ← What data exists
```

If the repo hasn't been initialized yet, note that — the skill design is still valid, it just means we're building from scratch rather than retrofitting.

### 1B. Read Superpowers

Fetch and read these files from the Superpowers repo to understand the skill format and pipeline:

```
https://raw.githubusercontent.com/obra/superpowers/main/skills/getting-started/SKILL.md
https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md
https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/visual-companion.md
https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md
https://raw.githubusercontent.com/obra/superpowers/main/skills/subagent-driven-development/SKILL.md
https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md
```

Note the YAML front matter format, the trigger/description conventions, and how skills chain into each other (brainstorming → writing-plans → subagent-driven-development).

---

## Phase 2 — Map the overlap

Create a table with three columns:

| Activity Andrea actually does | Covered by Superpowers? | Custom skill needed? |
|-------------------------------|------------------------|---------------------|

Activities to evaluate (this is the real workload, not theoretical):

**Systems / repo / coordination:**
- Session-start: read CLAUDE.md + LOCKBOARD.md, recommend highest-value task
- Session-end: summarize, update CLAUDE.md, update lockboard, pre-commit checklist
- Handoff creation between sessions and accounts
- Branch strategy (andrea/*, henna/*)
- Commit convention ([DATA], [MAP], [VIZ], [BUILD], [FIND], [DEAD], [META])
- Context routing: different agents read different files based on role

**Data engineering:**
- API data collection (transport.opendata.ch, Open Charge Map, Google Places, sharedmobility.ch)
- Monolithic script pattern: single end-to-end script, no interactive exploration, prints summary only
- CSV enrichment pipelines (merge → enrich → review-tag → verify)
- Dataset inventory maintenance
- Dead end documentation (what was tried, why it failed)

**Cartography / GIS:**
- QGIS MCP operations (always LV95/EPSG:2056, never modify originals)
- Print layout generation
- Coordinate system verification before any spatial work
- Swiss TLM highway hierarchy (VERKEHRSBEDEUTUNG field)

**Visualization:**
- Leaflet.js + Canvas animated maps (Train Pulse, Passenger Flow)
- D3 charts
- Scrollytelling website (A.02)
- Design system enforcement (colors, fonts, component specs)

**3D modeling:**
- Rhino MCP operations (RhinoScript, never modify existing geometry)
- Coordinate system documentation in code comments
- `rs.AddBox(corners)` with explicit 8-point arrays pattern

**Research / writing:**
- Research paper drafting and revision
- Process booklet chapters (reflective, first-person)
- Narrative writing for studio deliverables

**Multi-agent coordination:**
- 4 production roles: Analyst, Cartographer, Visualizer, Builder
- Role = context scope (which files to read), not personality
- Subagent delegation for parallel tasks
- Cross-account coordination (Cairn ↔ Lumen, Cadence ↔ Meridian)

**MCP safety:**
- QGIS/Rhino/Chrome MCPs have unrestricted filesystem + network access
- Never modify originals, always write to new paths
- Ask before any filesystem write
- Never read sensitive files outside project scope

---

## Phase 3 — Design the skill tree

Based on the mapping, propose a complete `.superpowers/skills/` directory for the City101 repo. This should include:

### 3A. Which Superpowers core skills to keep as-is
(brainstorming, writing-plans, subagent-driven-development, using-git-worktrees, test-driven-development, etc.)

### 3B. Which Superpowers core skills to override
Write the full SKILL.md for any core skill that needs City101-specific behavior. For example, brainstorming might need to include the LOG/LOI/LOD framework, or the visual companion might need QGIS/Rhino-aware diagram types.

### 3C. New custom skills unique to this project
Write the full SKILL.md (with YAML front matter) for each. These should follow Superpowers conventions but address architectural workflows. Likely candidates:

- **data-pipeline**: The monolithic script pattern, API rate limits, CSV conventions, dataset inventory updates, dead-end documentation
- **cartography**: QGIS MCP safety rules, coordinate system verification, print layout workflow, Swiss-specific conventions
- **spatial-modeling**: Rhino MCP safety rules, coordinate documentation, geometry creation patterns
- **session-handoff**: The handoff protocol (HANDOFF_DD-MM_SX.md format), CLAUDE.md updates, lockboard updates, cross-account continuity
- **mcp-safety**: The full MCP safety ruleset as a skill that gets invoked before any MCP operation
- **field-verification**: Protocol for A.03-style fieldwork (site identification from data → field visit → data validation → correction)
- **design-system**: Color, font, and component enforcement for all visual outputs
- **corridor-analysis**: City101-specific analytical patterns (archipelago framing, working continuity index, station-level analysis, Geneva–Villeneuve corridor conventions)

For each skill, include:
- YAML front matter (name, description — the description is the trigger)
- When to use (trigger conditions)
- Context to load (which repo files)
- Process steps
- Quality gate (checklist before completion)
- What it chains to (which skill comes next)

### 3D. Skill priority mapping

Show how the three-tier priority works for this project:

```
.superpowers/skills/          ← Project skills (City101-specific, highest priority)
~/.claude/skills/             ← Personal skills (Andrea's cross-project patterns)
skills/ (Superpowers core)    ← Base layer (software engineering patterns)
```

Which skills belong at which tier? Some of Andrea's patterns (monolithic scripts, handoff protocol, MCP safety) might be personal skills that apply across projects, not just City101.

---

## Phase 4 — Visual brainstorming companion assessment

The Superpowers visual companion renders HTML in a browser during brainstorming. Assess:

1. **Is this useful for City101?** (Yes/no and why — consider: system architecture diagrams, data flow visualization, map mockups before QGIS, 3D concept sketches before Rhino, website layout iterations)
2. **What custom visual templates would help?** (e.g., corridor map template, station analysis card, data pipeline flowchart, agent coordination diagram)
3. **How does it interact with the existing Visualizer in claude.ai?** (The browser Claude already has an inline SVG/HTML visualizer — does the Superpowers companion add value on top of that, or is it only relevant for Claude Code terminal sessions?)

---

## Phase 5 — Implementation plan

Produce a concrete implementation plan:

1. **Install Superpowers** — exact commands
2. **Create `.superpowers/skills/`** — the directory structure
3. **Write each custom SKILL.md** — full content, ready to commit
4. **Test triggers** — for each custom skill, write 2-3 example prompts that should activate it
5. **Update CLAUDE.md** — add a section noting that Superpowers is installed and how skills interact with the existing role system
6. **Henna onboarding** — what does Henna need to do on her end (Cadence/Meridian)?

---

## Constraints

- **Don't break what works.** The handoff system, the MCP safety rules, the monolithic script pattern — these are battle-tested. Skills should formalize them, not replace them with something untested.
- **Keep it lean.** Superpowers core is <2k tokens bootstrap. Custom skills should be similarly concise (<50 lines each where possible). Andrea's context windows are already under pressure from large datasets and MCP tool descriptions.
- **The repo might not exist yet.** The system architecture spec is at v7 but git initialization has been deferred multiple times. Design skills that work whether the repo is initialized or not.
- **Two humans, eight agent slots.** Skills need to work for both Andrea and Henna, across Claude Code, Cowork, Desktop+MCP, and browser. Not all interfaces support all features.
- **This is an architecture studio, not a software company.** The outputs are maps, models, visualizations, websites, and booklets — not deployed software. TDD and code review patterns from Superpowers core may need adaptation or may not apply at all. Be honest about what doesn't translate.
- **The meta-layer IS a deliverable.** Andrea is writing a research paper about this workflow. The skill design itself is documentation-worthy. Structure it so it's legible to a reader, not just to an agent.

---

## Output format

Deliver as a single markdown document with clear sections matching the phases above. Include all SKILL.md files inline (in code blocks) so they can be copy-pasted into the repo. End with a summary table: skill name → tier (project/personal/core) → trigger description → chains to.
