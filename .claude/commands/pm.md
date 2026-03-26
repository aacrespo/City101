# /pm — Project Manager

Decompose a goal into phases. Design team topology per phase. Generate executable prompt files. Track progress across sessions. Supports multiple projects for both Andrea and Henna.

## Arguments
$ARGUMENTS — one of:
- `"status"` — overview of ALL active projects
- `"status [project-id]"` — detailed status of one project
- `"[goal]"` — a new goal to plan (e.g., "model 9 relay-lock nodes for midterm")

## Context to read now
- `state/pm/projects.json` — project index (read FIRST)
- `CONTEXT.md` — current project state
- `LOCKBOARD.md` — active tasks, blockers, who's doing what
- `CONTEXT_ANDREA.md` and `CONTEXT_HENNA.md` — individual priorities

## Project structure

```
state/pm/
├── projects.json                ← index of all projects
├── [project-id]/                ← one folder per project
│   ├── master_plan.md
│   ├── phase_status.json
│   ├── decisions.md
│   └── prompts/                 ← execution prompts for this project
│       ├── phase0_[title].md
│       └── phase1_[title].md
├── [another-project-id]/
│   └── ...
└── topology_history.md          ← shared learnings across all projects (append-only)

prompts/                          ← standalone prompts only (not managed by PM)
```

## Instructions

### If $ARGUMENTS = "status" (no project ID)
Read `state/pm/projects.json`. For each project, read its `phase_status.json`. Report:

| Project | Owner | Status | Current phase | Priority |
|---------|-------|--------|--------------|----------|

Then highlight: blockers, anything overdue, what to work on next.

### If $ARGUMENTS = "status [project-id]"
Read `state/pm/[project-id]/master_plan.md` and `phase_status.json`. Report:
- Current phase and completion %
- Next phase and what's needed to start
- Any blockers or topology adjustments needed
- Token/session budget vs actual

### If $ARGUMENTS = a new goal

#### Step 1: Parse the goal
- What's being built?
- Who owns it? (Andrea, Henna, or shared)
- How many sessions realistically?
- Known constraints (timeline, VM access, data availability)?
- Success criteria?
- Ask the user brief clarifying questions if needed.

#### Step 2: Pick a project ID
- Format: `[owner]-[brief-topic]` or `[topic]` if shared
- Examples: `andrea-rhinobase`, `henna-corridor-model`, `midterm-production`
- Check `projects.json` — don't collide with existing IDs

#### Step 3: Design phases
Break the goal into 3-5 phases. For each phase:

```
Phase [N]: [Name] ([estimated sessions], [estimated hours])
├── Goal: [one sentence]
├── Topology: [flat/hierarchical] + [broad/narrow context] + [parallel/sequential]
├── Team: [N] agents ([roles])
├── Reads: [data sources, knowledge bases]
├── Produces: [deliverables, to output/]
├── Dependencies: [what must be done first]
└── Success: [how to verify this phase is complete]
```

**Topology guidance:**
- **Flat** = agents talk directly. Good for discovery, cross-domain optimization. Risk: conflicts, slow resolution.
- **Hierarchical** = coordinator resolves all. Good for production, tight deadlines. Risk: missed optimizations.
- **Broad context** = all agents see everything. Good for integration. Cost: token-heavy.
- **Narrow context** = each agent sees only their domain. Good for focus. Risk: interface gaps.

#### Step 4: Generate prompt files
For EACH session in the plan, write a prompt file inside the project folder:
- File: `state/pm/[project-id]/prompts/phase[N]_[brief_title].md`
- Standalone prompts (not part of a PM project) still go in `prompts/`
- Include full team assembly instructions (embed the actual agent spawn prompts — don't reference `/team`)
- Include data sources, interface rules, verification gates
- Include topology declaration and why
- Follow prompt-craft.md principles (context at top, query at bottom, XML tags for separation)

#### Step 5: Write state files
- `state/pm/[project-id]/master_plan.md` — full phase breakdown with topology per phase
- `state/pm/[project-id]/phase_status.json` — tracking:
  ```json
  {
    "goal": "[goal]",
    "owner": "[andrea|henna|shared]",
    "created": "[date]",
    "phases": [
      {"name": "[name]", "status": "pending|in_progress|complete", "sessions_planned": N}
    ],
    "current_phase": "[name]"
  }
  ```
- `state/pm/[project-id]/decisions.md` — why each topology was chosen (append-only)
- Update `state/pm/projects.json` — add the new project to the index

#### Step 6: Present the plan
Show the user:
1. Narrative summary — phases, dependencies, why this topology structure
2. Phase diagram (ASCII) showing order and parallelism
3. File inventory — all prompt files and state files created
4. Recommended first action — which prompt to execute first

## Rules
- Never overwrite existing `master_plan.md` without asking — create `_v2` or update in place
- All prompt files use `[A04_ACTIVE]` prefix — user updates to `[A04_DONE]` after execution
- Decisions log is append-only
- When updating after a phase completes, read `state/pm/topology_history.md` (if exists) to learn from past topology outcomes
- Respect the team size cap from `workflows/agent-team-modeling-v3.md`: max 8 agents, 2-3 modelers
- Any Claude (Cairn, Lumen, Meridian, Cadence) can read/update any project — the state is shared

## Integration
- `/session-end` should update relevant `phase_status.json` files with session results
- `/pm status` is a quick check-in, not a replanning session
- LOCKBOARD.md references projects by ID when relevant
