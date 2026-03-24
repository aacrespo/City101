# Ruflo Study Notes: What We Can Steal for Architectural Modeling

**Author**: Cairn Code (CLI)
**Date**: 2026-03-24
**Source**: [ruvnet/ruflo](https://github.com/ruvnet/ruflo) (formerly Claude Flow v2/v3)

---

## What Ruflo Is

Ruflo is a multi-agent orchestration framework built on Claude Code. It coordinates 60+ specialized agents using swarm topologies, shared memory (AgentDB), consensus algorithms, and a self-learning system called SONA. The core idea: a coordinator (queen) manages worker agents through a structured hierarchy, with persistent memory preventing knowledge loss and drift prevention keeping agents on-task.

Much of the codebase is enterprise software infrastructure (WASM boosters, Docker, RL algorithm libraries). The ideas worth studying for us are the coordination patterns, not the implementation.

---

## 1. Anti-Drift Patterns

### How Ruflo Does It

Ruflo prevents agents from going off-track through three mechanisms:

**Hierarchical topology with forced routing.** In hierarchical mode, all communication routes through the queen/coordinator node. Workers cannot message each other directly. The topology manager enforces this structurally — the adjacency list simply doesn't contain worker-to-worker edges. An agent that tries to go rogue has no channel to influence others.

**Heartbeat monitoring with health decay.** A background process checks agent heartbeats every N milliseconds. If an agent misses 3x the heartbeat interval, its health score decays by 0.2 per cycle. Below 0.2 health, auto-recovery triggers (the agent gets reset or replaced). This catches agents that hang, loop, or silently fail.

**Small team size as a design constraint.** The recommended max is 6-8 agents. This isn't a performance limit — it's a drift-prevention measure. More agents means more coordination surface, more message passing, more opportunities for misalignment. The documentation explicitly calls this "reducing the drift surface."

### What We Already Do

Our workflow has strong anti-drift bones:
- Structure-first sequencing (Phase 1 before Phase 2) prevents dependency violations
- The coordination freeze after Phase 1 locks the contract geometry
- The "never say go free" rule and Discuss-Decide-Execute pattern constrain each round
- The 3-4 round rule caps total iterations
- Observation mode rules (questions only, no opinions) prevent premature consensus

### Concrete Proposals

**Proposal 1A: Explicit communication topology per phase.**

Right now, our agents can SendMessage to any other agent at any time. This is mesh topology — fine for small teams, but it's how drift starts. When the shell agent messages the windows agent directly about a wall offset, the lead might never know, and the decision might contradict structure's contract.

Adapt Ruflo's forced routing: during build phases, all inter-agent messages route through the lead. Agents can ask factual questions of each other (our existing Rule 2), but any message that proposes a geometry change must go through the lead first.

Implementation: add to the agent prompt template a communication constraint block:
```
COMMUNICATION RULES (Phase 1-2):
- Factual queries to other agents: ALLOWED (direct)
- Geometry change proposals: ROUTE THROUGH LEAD
- Self-review findings: REPORT TO LEAD
- During observation mode: questions only, proposals stay private
```

This doesn't require any tooling change — it's a prompt-level constraint, like Ruflo's topology is a configuration-level constraint.

**Proposal 1B: Health-check pings between rounds.**

Ruflo's heartbeat system catches silent failures. We've seen this failure mode: an agent's script errors out, the agent says "done" without verifying geometry exists, and the reviewer later finds an empty layer.

Add a mandatory health check between phases. After each agent reports "done," the lead runs a quick diagnostic:
```
For each agent that reported complete:
1. Query Rhino: count objects on agent's layers
2. Compare to expected count from Bill of Objects
3. If count = 0 or < 50% expected: flag, do not proceed to next phase
4. If count reasonable: mark healthy, proceed
```

This is our version of heartbeat monitoring — not checking if the agent process is alive, but checking if the agent's output is real.

**Proposal 1C: Cap team size in the workflow.**

Make the 6-8 agent limit explicit doctrine, not just a guideline from Lock 05. Our training-s3 session proved the same thing Ruflo codifies: 4 modelers produced worse results than 2 would have. Add to the workflow:

```
TEAM SIZE LIMITS:
- Modeler agents: 2-3 (never more than 4)
- Reviewer agents: 1 (2 only for LOG 400+ builds)
- Total agents including lead: max 8
- If the build seems to need more agents, split into two sequential builds instead
```

---

## 2. Shared Memory / AgentDB

### How Ruflo Does It

AgentDB implements a three-tier memory model:
- **In-memory Map** for fast access during a session
- **SQLite persistence** for cross-session survival
- **HNSW vector index** for semantic search ("find patterns similar to this task")

Memory is organized by namespaces (`patterns`, `results`, `learning`, `coordination`). Agents store and retrieve from namespaces using CLI commands. The key design: agents MUST search memory before starting a task, and MUST store patterns after succeeding. This is enforced at the prompt level, not the infrastructure level.

The namespace model provides isolation (my agent's working memory is separate from yours) while allowing explicit sharing (the `patterns` namespace is readable by all agents).

### What We Already Do

We have the conceptual equivalent, but it's scattered:
- **Law** (archibase): shared, read-only reference data (material specs, assembly layers)
- **Doctrine** (rhino-playbook.md): shared principles, read by all agents every session
- **Jurisprudence** (learnings-*.md files): per-domain experience, written after builds
- **Coordination geometry**: structure publishes column positions, slab edges — others read it

The gap: we don't have a structured way for agents to share discoveries DURING a build. If the shell agent discovers that a wall needs to offset 50mm because of a column interference, that discovery lives in the agent's context window. It dies when the session ends. The learnings file captures it post-hoc, but only if the agent remembers to write it.

### Concrete Proposals

**Proposal 2A: Live coordination log (shared memory during builds).**

Create a shared file that agents read/write during a build session — our version of AgentDB's `coordination` namespace:

```
output/city101_hub/[lock_id]/coordination_log.md

## Coordination Log — Lock [ID]
### Decisions
- [structure] Removed Col_L0_0_0 for entrance clearance, added transfer beam
- [shell] Offset north wall 50mm east to clear column flange
- [windows] Reduced NW opening width by 100mm to maintain mullion minimum

### Interface Alerts
- [shell → structure] Wall_L0_North base doesn't align with slab edge at x=3.2
- [circulation → shell] Ramp opening needs 200mm wider clearance

### Open Questions
- [windows] Glass recess depth: 80mm per spec, but reveal depth only 60mm. Which governs?
```

Every agent reads this file at the start of each round. Every agent appends decisions and alerts as they build. The lead reviews it at each phase gate. This is the "shared memory namespace" concept adapted to file-based coordination.

**Proposal 2B: Namespace the learnings files by scope.**

Currently we have `learnings-structure.md`, `learnings-envelope.md`, etc. — per-domain. Ruflo's namespace model suggests adding a second axis: per-build vs cross-build.

```
knowledge/
  learnings-structure.md          # cross-build (jurisprudence) — survives forever
  learnings-envelope.md           # cross-build
  sessions/
    lock05-coordination.md        # per-build — coordination decisions from this build
    lock05-discoveries.md         # per-build — things learned during this build
    cabin-v3-coordination.md
    cabin-v3-discoveries.md
```

Per-build files are the working memory. Cross-build files are the consolidated long-term memory. After a build, the lead distills per-build discoveries into the cross-build learnings. This mirrors Ruflo's consolidation cycle (merge similar patterns, prune low-value ones).

**Proposal 2C: Mandatory memory search before modeling.**

Our workflow already says agents must query archibase before modeling. Extend this to learnings:

```
BEFORE MODELING ANY ELEMENT:
1. Query archibase for assembly layers (LAW)
2. Read rhino-playbook.md (DOCTRINE)
3. Search learnings-[domain].md for the specific element type (JURISPRUDENCE)
4. Search coordination_log.md for any decisions affecting your element (SESSION)
```

Step 3 and 4 are new. This is Ruflo's "ALWAYS search memory BEFORE starting" rule applied to our knowledge system.

---

## 3. Self-Learning Loop (SONA)

### How Ruflo Does It

SONA tracks "trajectories" — the full sequence of actions an agent takes to complete a task, including observations and rewards at each step. When a trajectory succeeds, the system extracts a pattern (the action sequence + final observation) and stores it with a confidence score.

The key mechanisms:
- **Selective learning**: only successful trajectories generate patterns. Failures are archived but don't produce reusable patterns.
- **Confidence scoring**: `confidence = min(1, totalReward / steps)` — more reward per step = higher confidence.
- **Consolidation cycles**: every 30 min to 4 hours, patterns with >95% textual similarity merge, combining usage counts and boosting confidence.
- **Pruning**: patterns scored by confidence (40%) + recency (30%) + usage (20%) + age (10%). Low scorers get removed when storage fills up.
- **Mode switching**: learning rates and thresholds adjust based on task type (real-time vs batch vs research).

### What We Already Do

Our learnings files are a manual version of SONA. Agents write discoveries after builds. The lead distills shared learnings periodically. But the process is inconsistent — agents forget to write, distillation happens sporadically, and there's no confidence scoring or pruning.

The overlap audit from training-s3 is actually a form of trajectory analysis: we tracked which exercises passed/failed, counted objects, identified failure patterns (duplicate geometry, wrong layer prefix, missing metadata), and distilled those into workflow updates.

### Concrete Proposals

**Proposal 3A: Structured learnings format with confidence scoring.**

Replace the free-form learnings files with a structured format that enables scoring and consolidation:

```markdown
## Learnings — Structure Domain

### [PASS] Transfer beam at removed column — Lock 05
- **Context**: Column removed for entrance clearance
- **Action**: Added transfer beam spanning adjacent columns, depth = 1.5x standard beam
- **Result**: Passed review, no deflection concern at this span
- **Confidence**: HIGH (verified in review, reused in cabin-v3)
- **Uses**: 2
- **Last used**: 2026-03-22

### [FAIL] Cantilevered slab without edge beam — Lock 05
- **Context**: Attempted slab extension beyond last column line
- **Action**: Extended slab 1.2m past column without edge beam
- **Result**: Failed review — excessive deflection risk, no edge stiffening
- **Lesson**: Always add edge beam at cantilever. Max cantilever without engineer = 0.6m
- **Confidence**: HIGH (failure is unambiguous)

### [WARN] Column-wall interference at corners — Cabin v2
- **Context**: 400mm column inside 300mm wall at building corner
- **Action**: Offset wall to wrap column, left column exposed on interior
- **Result**: Passed constraints but failed visual coherence — exposed column reads as error
- **Lesson**: At corners, either embed column in thickened wall or make exposure intentional (piloti)
- **Confidence**: MEDIUM (design judgment, not absolute rule)
```

Tags: PASS/FAIL/WARN. Confidence: HIGH/MEDIUM/LOW. Usage count and date enable pruning.

**Proposal 3B: Post-build retrospective as trajectory extraction.**

After each build (our version of trajectory completion), run a structured retrospective:

```
POST-BUILD RETROSPECTIVE (lead runs after Phase 4):
For each agent:
1. What elements did you build? (actions)
2. What passed self-review? What failed? (rewards)
3. What did you have to improvise? (novel patterns)
4. What would you do differently? (negative patterns)

Extract:
- Successful patterns → learnings-[domain].md with PASS tag
- Failed patterns → learnings-[domain].md with FAIL tag
- Novel solutions → learnings-[domain].md with WARN tag (unproven)

Consolidate:
- If a new pattern matches an existing one at >90% similarity, merge (bump usage count)
- If a FAIL pattern contradicts a PASS pattern, flag for human review
```

This is SONA's trajectory-to-pattern extraction adapted to our roundtable format. The simultaneous proposal sharing we already do (Rule 5 in observation mode) is actually a good data collection moment — each agent's notepad IS their trajectory summary.

**Proposal 3C: Learnings pruning cycle.**

Every 5 builds (or monthly), the lead reviews learnings files and prunes:
- Remove patterns with 0 uses and LOW confidence that are >30 days old
- Merge near-duplicate patterns
- Promote WARN patterns to PASS if they've been reused successfully 3+ times
- Archive FAIL patterns that have been superseded by better solutions

This prevents learnings files from growing unboundedly. Ruflo's pruning formula (confidence 40% + recency 30% + usage 20% + age 10%) is a reasonable starting point for scoring which patterns to keep.

---

## 4. Consensus Algorithms

### How Ruflo Does It

Five consensus mechanisms, used depending on context:

| Algorithm | How it works | When used |
|-----------|-------------|-----------|
| **Raft** | Leader maintains authoritative state. Followers replicate. Leader election on failure. | Default for hierarchical topology |
| **Byzantine (BFT)** | Requires 2/3 majority agreement. Tolerates malicious/faulty agents. | High-stakes decisions, security |
| **Gossip** | Agents spread information peer-to-peer, convergence over time | Large swarms, eventual consistency OK |
| **Weighted** | Queen votes count 3x worker votes | Quick decisions with hierarchy |
| **Majority** | Simple >50% vote | Low-stakes, flat teams |

The coordinator triggers consensus when agents disagree about shared state (e.g., two agents claim different values for the same interface dimension).

### What We Already Do

Our consensus mechanism is informal but present:
- The **lead resolves disagreements** at round discussions (effectively Raft — the lead is the leader)
- **Convergence detection** in simultaneous proposals: "three of you flagged the same ramp issue" (effectively majority voting)
- The **structure agent's published geometry is authoritative** (effectively weighted — structure's word is law for the grid)

The gap: we don't have a protocol for when two agents disagree about an interface dimension and the lead isn't sure who's right.

### Concrete Proposals

**Proposal 4A: Weighted authority by domain.**

Formalize who wins disagreements, instead of leaving it to ad-hoc lead judgment:

```
AUTHORITY HIERARCHY FOR INTERFACE DISPUTES:

Structural dimensions (grid, levels, slab edges):
  → Structure agent is authoritative. Period.

Envelope dimensions (wall thickness, insulation, cladding):
  → Shell agent is authoritative.
  → If shell conflicts with structure, structure wins, shell adapts.

Opening dimensions (window sizes, door clearances):
  → Windows agent is authoritative for glass/frame.
  → Shell agent is authoritative for wall void.
  → If opening doesn't fit wall void: shell adjusts void, not windows reducing glass.

Code compliance (railing height, ramp gradient, clearances):
  → The code is authoritative. No agent overrides SIA/VKF.
  → If code conflicts with design intent, flag for human decision.

Visual/proportional judgment:
  → Reviewer is authoritative for Mode B (visual coherence).
  → If reviewer says proportions are wrong, the responsible agent adjusts.
  → If the agent disagrees, escalate to human (Andrea/Henna).
```

This is Ruflo's weighted consensus (queen votes 3x) adapted to architectural domain expertise. Structure's vote on grid dimensions counts more than shell's, just as shell's vote on envelope assembly counts more than structure's.

**Proposal 4B: Convergence-as-signal in round discussions.**

Formalize the convergence detection we already do informally:

```
ROUND DISCUSSION PROTOCOL:
1. All agents share proposals simultaneously
2. Lead counts convergence:
   - 3+ agents flag same issue → CRITICAL, fix immediately
   - 2 agents flag same issue → HIGH, fix this round
   - 1 agent flags unique issue → MEDIUM, discuss briefly, decide if this round or next
   - 0 convergence on an issue → LOW, likely noise, defer or drop
3. For disagreements (two agents propose contradictory fixes):
   - Check authority hierarchy (4A above)
   - If authority is unclear: both agents explain in 30 seconds, lead decides
   - Decision is recorded in coordination_log.md with rationale
```

This is Ruflo's majority consensus adapted to our roundtable format. The convergence count is our voting mechanism.

---

## 5. Swarm Coordination: Queen/Worker Model

### How Ruflo Does It

The 15-agent hierarchy uses domain-based organization:

| Domain | Priority | Role |
|--------|----------|------|
| Queen | 0 | Coordination, oversight, final approval |
| Security | 1 | Validation, threat modeling |
| Core | 2 | Primary implementation |
| Integration | 3 | Cross-system work |
| Support | 4 | Testing, performance, documentation |

The queen never builds — she coordinates. Workers are pooled by domain with capacity limits. Task assignment uses scoring: `base + type_match + health - workload + success_rate - avg_time`. The queen assigns tasks to the best-scoring available worker.

Domain task queues buffer overflow — if all core workers are busy, new core tasks queue rather than being assigned to support workers. This prevents skill mismatch.

### What We Already Do

Our workflow maps roughly to this:
- **Lead** = Queen (coordinates, doesn't build)
- **Structure, Shell, Roof, Ground** = Core domain workers
- **Windows, Circulation, Elevator** = Integration domain workers
- **Reviewer** = Security/validation domain

We already have the Bill of Objects (task assignment), the Interface Registry (cross-domain contracts), and phase sequencing (priority ordering). But task assignment is manual — the lead decides who builds what by hand.

### Concrete Proposals

**Proposal 5A: Scoring-based task assignment for improvement rounds.**

Initial build assignments are design decisions (who owns which system). But improvement rounds — Phase 4 and any fix rounds — could use scoring. When the review identifies 8 issues to fix, instead of the lead manually assigning each one:

```
IMPROVEMENT ROUND TASK SCORING:

For each issue identified in review:
1. Domain match: +50 if the issue is on an agent's own layer
2. Interface proximity: +30 if the issue is at an interface the agent owns
3. Current workload: -20 per unfinished task the agent already has
4. Past success: +10 if the agent has fixed this type of issue before (check learnings)
5. Complexity estimate: assign to highest-scoring agent if complex, any qualified agent if simple

Auto-assign: if one agent scores >80 and all others <40, assign without discussion.
Discuss: if two agents score within 20 points, ask both who's better positioned.
```

This is lightweight — no infrastructure needed, just a mental model for the lead. But it makes assignment decisions transparent and repeatable.

**Proposal 5B: Domain task queues to prevent idle waste.**

Ruflo queues tasks by domain rather than assigning them to whoever's free. We should do the same:

```
When an agent finishes early and enters observation mode:
- DO NOT assign them work from another domain
- DO let them observe and prepare proposals (existing Rule 1)
- DO let them assist their own domain if another agent in the same domain is struggling
- ONLY cross-domain assist if the lead explicitly reassigns (existing Rule 3)

Example: if Shell finishes before Roof, Shell can help Roof (both envelope).
But Shell should NOT start doing Windows work (different domain, different expertise).
```

This is already partially captured in our Rule 3 (reassignment is the lead's call), but making it domain-aware prevents the lead from making bad reassignment decisions.

**Proposal 5C: The queen never builds.**

Make this explicit doctrine. In Lock 05, the lead sometimes built geometry alongside coordinating. This caused coordination gaps — while the lead was heads-down scripting, agents drifted.

```
THE LEAD DOES NOT MODEL.
The lead coordinates, reviews, decides, and documents.
If you need more modeling capacity, spawn another worker agent.
A lead who builds is a worker who doesn't coordinate.
```

Ruflo's queen agent has zero implementation capability by design. Our lead should have the same constraint.

---

## Summary: Priority of Adoption

| Proposal | Effort | Impact | Priority |
|----------|--------|--------|----------|
| 1A: Communication topology per phase | Low (prompt change) | Medium | Do next build |
| 1B: Health-check pings between rounds | Low (Rhino query) | High | Do next build |
| 1C: Cap team size | Zero (add to workflow) | Medium | Do now |
| 2A: Live coordination log | Low (create template) | High | Do next build |
| 2B: Namespace learnings by scope | Medium (restructure files) | Medium | Next week |
| 2C: Mandatory memory search | Low (prompt change) | High | Do next build |
| 3A: Structured learnings format | Medium (rewrite files) | High | Next week |
| 3B: Post-build retrospective | Low (add to workflow) | High | Do next build |
| 3C: Learnings pruning cycle | Low (periodic task) | Medium | Monthly |
| 4A: Weighted authority by domain | Low (add to workflow) | High | Do next build |
| 4B: Convergence-as-signal | Low (add to workflow) | Medium | Do next build |
| 5A: Scoring-based task assignment | Low (mental model) | Medium | Try next build |
| 5B: Domain task queues | Low (clarify rules) | Medium | Do next build |
| 5C: Queen never builds | Zero (add to workflow) | High | Do now |

The highest-impact, lowest-effort changes: health-check pings (1B), live coordination log (2A), weighted authority (4A), and "queen never builds" (5C). These four alone would address the main coordination failures we've seen in Lock 05 and training-s3.

---

*Studied from the Ruflo repository (ruvnet/ruflo), focusing on v3/@claude-flow/swarm and v3/@claude-flow/memory implementations. The RL algorithms and WASM infrastructure are interesting engineering but not applicable to our use case — the coordination patterns are what matter.*

— Cairn Code, 2026-03-24
