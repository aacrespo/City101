# /pm — Project Manager

Decompose a goal into phases. Design team topology per phase. Generate executable prompt files. Track progress across sessions.

## Arguments
$ARGUMENTS — the goal to plan (e.g., "model 9 relay-lock nodes for midterm") or "status" to review current plan

## Context to read now
- `CONTEXT.md` — current project state
- `LOCKBOARD.md` — active tasks, blockers, who's doing what
- `CONTEXT_ANDREA.md` and `CONTEXT_HENNA.md` — individual priorities
- `state/pm/master_plan.md` — existing plan (if continuing)
- `state/pm/phase_status.json` — completion tracking (if exists)

## Instructions

### If $ARGUMENTS = "status"
Read `state/pm/master_plan.md` and `state/pm/phase_status.json`. Report:
- Current phase and completion %
- Next phase and what's needed to start
- Any blockers or topology adjustments needed
- Token/session budget vs actual

### If $ARGUMENTS = a new goal

#### Step 1: Parse the goal
- What's being built?
- How many sessions realistically?
- Known constraints (timeline, VM access, data availability)?
- Success criteria?
- Ask the user brief clarifying questions if needed.

#### Step 2: Design phases
Break the goal into 3-5 phases. For each phase:

```
Phase [N]: [Name] ([estimated sessions], [estimated hours])
├── Goal: [one sentence]
├── Topology: [flat/hierarchical] + [broad/narrow context] + [parallel/sequential]
├── Team: [N] agents ([roles])
├── Reads: [data sources, archibase layers]
├── Produces: [deliverables, to output/]
├── Dependencies: [what must be done first]
└── Success: [how to verify this phase is complete]
```

**Topology guidance:**
- **Flat** = agents talk directly. Good for discovery, cross-domain optimization. Risk: conflicts, slow resolution.
- **Hierarchical** = coordinator resolves all. Good for production, tight deadlines. Risk: missed optimizations.
- **Broad context** = all agents see everything. Good for integration. Cost: token-heavy.
- **Narrow context** = each agent sees only their domain. Good for focus. Risk: interface gaps.

#### Step 3: Generate prompt files
For EACH session in the plan, write a complete prompt file to `prompts/`:
- File: `prompts/[A04_ACTIVE]_phase[N]_[brief_title].md`
- Include full team assembly instructions (embed the actual agent spawn prompts — don't reference `/team`)
- Include data sources, interface rules, verification gates
- Include topology declaration and why
- Follow prompt-craft.md principles (context at top, query at bottom, XML tags for separation)

#### Step 4: Write state files
- `state/pm/master_plan.md` — full phase breakdown with topology per phase
- `state/pm/phase_status.json` — tracking:
  ```json
  {
    "goal": "[goal]",
    "created": "[date]",
    "phases": [
      {"name": "[name]", "status": "pending|in_progress|complete", "sessions_planned": N}
    ],
    "current_phase": "[name]"
  }
  ```
- `state/pm/decisions.md` — why each topology was chosen (append-only)

#### Step 5: Present the plan
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

## Integration
- `/session-end` should update `phase_status.json` with session results
- `/auto-dream` should append topology outcomes to `state/pm/topology_history.md`
- `/pm status` is a quick check-in, not a replanning session
