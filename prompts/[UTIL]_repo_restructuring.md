# Prompt: Repo Restructuring

## Task
Audit and restructure the city101 repo. The goal is to make CLAUDE.md a map (table of contents), not a context dump — agents follow paths to load only what they need.

## Steps
1. Read CLAUDE.md, CONTEXT.md, CONTEXT_ANDREA.md to understand current state
2. Explore the full repo structure — especially `output/`, `datasets/`, `source/`, `deliverables/`
3. Identify files in `output/` ready to promote (verified research, finalized outputs)
4. Propose folder reorganization — subfolders where things are getting flat, better groupings
5. Refactor CLAUDE.md to be a routing table: short pointers to where things live, not inline content
6. Document the Henna/Andrea task split for midterm if info is available in handoffs or context files
7. Commit changes with appropriate prefixes

## Constraints
- Never delete files. Move or reorganize only.
- Ask before any structural change that isn't obvious.
- Keep CONTEXT.md as the living state doc — CLAUDE.md becomes the map that points to it.
- Check `output/braindump_2026-03-17_three-things.md` for current priorities and context.
