# EPFL Architecture Folder Scan — Construction Knowledge Extraction

Paste this prompt into a fresh Claude Code session after restarting (Full Disk Access enabled).

---

## Task

Scan 3 years of EPFL architecture coursework and extract everything relevant to construction detail modeling. This is a one-time knowledge raid.

## Folders to scan

```
/Users/andreacrespo/Documents/EPFL cours/Archi/1ère
/Users/andreacrespo/Documents/EPFL cours/Archi/2ème
/Users/andreacrespo/Documents/EPFL cours/Archi/3eme
```

## What to look for

**KEEP — anything related to:**
- Construction details (wall sections, roof sections, floor buildups)
- Structural systems (timber frame, masonry, concrete, steel)
- Material specifications (wood, stone, concrete, insulation, glass)
- Joinery and connections (mortise-tenon, dovetail, steel connections, bolted joints)
- Building envelope (thermal insulation, vapour barriers, waterproofing, DPC)
- Stairs, doors, windows — how they're built, not just drawn
- Facade systems, cladding, ventilated cavities
- Foundation types, ground conditions
- Fire protection, acoustic isolation
- SIA norms, Swiss building codes
- Architectural drawing conventions (plans, sections, details at 1:20, 1:10, 1:5)
- Any course named "construction", "structure", "matériaux", "détails", "enveloppe", "physique du bâtiment"

**IGNORE — skip entirely:**
- Urban planning, landscape, theory/history essays
- Design studio projects (unless they contain construction details)
- Administrative docs (schedules, grades, enrollment)
- Pure math/physics/programming (unless structural engineering)

## Method

1. Launch 3 parallel Explore agents, one per year folder
2. Each agent: list full directory tree, identify relevant files by name/path/content
3. For PDFs: read first pages to confirm relevance
4. For images: check if they show construction details

## Output

For each relevant file found, record:
- Full path
- 1-line description
- Topic category (structure, envelope, materials, joinery, openings, stairs, foundation, codes, drawing conventions)
- Priority (HIGH = directly useful for modeling, MEDIUM = reference, LOW = tangential)

Then:
1. Copy HIGH priority files to `~/CLAUDE/city101/source/epfl_construction/` (organized by topic)
2. Write an index at `~/CLAUDE/city101/source/epfl_construction/INDEX.md`
3. For key PDFs with construction details: extract the critical dimensions, layer buildups, and assembly rules into a summary markdown

## After scanning

**IMPORTANT: Remind Andrea to turn OFF Full Disk Access for Terminal.**
System Settings → Privacy & Security → Full Disk Access → toggle OFF.

## Context

This feeds the training curriculum at `output/agent_training/exercise_curriculum.md` and the playbook at `.claude/agents/knowledge/rhino-playbook.md`. The three modeling laws are:
1. Everything has thickness
2. Nothing overlaps (including duplicates)
3. Nothing floats

Any construction knowledge found should reinforce these principles with real Swiss/EPFL specifications.
