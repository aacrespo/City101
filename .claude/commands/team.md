# Utility: Team

Dynamically assemble an agent team for any task.

## Process

1. **Understand the task.** Read the user's request (or the prompt from `/brain-dump`).

2. **Identify the roles needed.** Draw from existing project roles:
   - **Analyst** — data collection, API queries, dataset creation, verification
   - **Cartographer** — maps, spatial analysis, GeoJSON, QGIS
   - **Visualizer** — charts, diagrams, scrollytelling, web visualizations
   - **Builder** — deployment, packaging, site assembly, narrative
   - **Modeler** — 3D geometry, Rhino/Grasshopper, physical form

   If the task needs a skill not covered by existing roles, **define a temporary role** on the spot. Describe what it reads, what it produces, and what rules it follows. If the same temporary role appears in 3+ sessions, propose making it permanent.

3. **Design the team structure:**
   - What does each agent read? (context files, datasets, specs)
   - What does each agent produce? (always to `output/`)
   - What are the dependencies? (can they run in parallel, or does agent B need agent A's output?)
   - Who is the lead? (the main session coordinates, reviews, promotes)

4. **Spawn the agents.** Use the Agent tool. For each agent:
   - Give it a clear, scoped task
   - Tell it which files to read
   - Tell it where to write (always `output/`)
   - Tell it to print a summary when done
   - Run independent agents in parallel

5. **Coordinate results:**
   - Collect all agent outputs
   - Cross-reference and verify (use `/verify-data` for datasets)
   - Resolve conflicts or gaps
   - Promote verified output to final locations
   - Summarize what was produced and what needs follow-up

## Rules
- All agent output goes to `output/` — never directly to `datasets/`, `visualizations/`, etc.
- Every agent follows the same project rules (CLAUDE.md, conventions, data protocol)
- Agents should use existing tools from `tools/` when available
- The lead session (you) is responsible for quality — agents produce drafts, you verify
- If a task only needs one role, don't force a team — just do it directly

## When to use this (for any Claude session, not just when the user asks)
Consider assembling a team when:
- The task naturally splits into 2+ distinct deliverables
- Different skills are needed (data + maps, analysis + visualization)
- Sub-tasks can run in parallel to save time
- The main context would get cluttered by doing everything sequentially

Do NOT use a team when:
- The task is simple and focused
- Everything is sequential with tight dependencies
- You'd spend more time coordinating than doing
