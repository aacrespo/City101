# Knowledge Feedback Framework — Medical Guidelines Model

## The analogy

| Medical system | Knowledge base system | What it does |
|---------------|----------------------|--------------|
| **Clinical guideline** | Base value (L1) | Authoritative, evidence-based, slow to change. "Prescribe X at dose Y." |
| **Textbook** | Guide (L2) | Explains why the guideline exists, how to apply it, what the reasoning is. |
| **Protocol / procedure** | Script (L3) | Step-by-step execution. "Administer X: prepare, dose, inject, monitor." |
| **Case notes** | Learnings table | What happened when you applied the guideline to a real patient. Context-specific. |
| **Clinical review board** | Human curation | Periodically reviews case notes. Promotes patterns to guidelines. Discards noise. |
| **Adverse event report** | Edge case flag | Something went wrong. Urgent. Gets reviewed faster. |

## Why medical, not legal

The legal framework (law / doctrine / jurisprudence) has a structural problem: jurisprudence can override statute. A court ruling can effectively change the law. That's wrong for a knowledge base — a single bad experience shouldn't change a value that was carefully extracted from source code.

Medical guidelines work differently:
- **Guidelines don't change from one case.** A patient reacting badly to a drug doesn't rewrite the guideline. It generates a case note.
- **Case notes are context-rich.** They include the patient (which lock), the condition (what scale, what material), the outcome (what failed), and the clinician's judgment (what to do instead).
- **Pattern → guideline update requires evidence.** Only when multiple case notes show the same pattern does the review board update the guideline. One case = observation. Five cases = signal. Pattern confirmed = guideline update.
- **The practitioner reads both.** The agent reads the guideline (base value) AND relevant case notes (learnings). It makes a judgment call based on its current context, informed by both.

## How it maps to the bases

### Base values (clinical guidelines)
Authoritative. Extracted from source code, standards, or verified data. Changed rarely, only after review.

```
iboisbase.joint_constraints:
  type_id=14, parameter="chamfer_offset", value=-0.75
  source: compas_wood wood_joint_lib.cpp:2341
```

### Case notes (learnings table)
Context-specific observations from real modeling sessions. Written by review agents. Never override the base.

```sql
CREATE TABLE case_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- What was referenced
    related_table TEXT,          -- joint_constraints, methods, etc.
    related_id TEXT,             -- which row
    base_value TEXT,             -- the guideline value that was applied

    -- What happened
    finding TEXT,                -- "boolean operation failed — geometry too thin"
    context TEXT,                -- "Lock 07 Rennaz, 1:200, timber section 180mm"
    recommendation TEXT,         -- "use chamfer_offset=-0.5 below 200mm section"
    severity TEXT,               -- observation | warning | adverse

    -- Traceability
    session TEXT,                -- which modeling session
    agent TEXT,                  -- which agent/role found this
    lock_node TEXT,              -- which lock (jurisdiction)
    scale TEXT,                  -- modeling scale

    -- Lifecycle
    status TEXT DEFAULT 'pending',  -- pending | confirmed | pattern | promoted | discarded
    review_notes TEXT,              -- human notes when reviewing
    created DATE,
    reviewed DATE
);
```

### Status lifecycle

```
pending ──→ confirmed ──→ pattern ──→ promoted
   │            │                        │
   └→ discarded └→ discarded             └→ base value updated
                                            (guideline change)
```

- **pending**: agent wrote it, nobody's looked yet
- **confirmed**: human verified the observation is real (not a modeling error)
- **pattern**: same finding confirmed across 3+ different contexts (locks, scales, materials)
- **promoted**: pattern is strong enough to update the base value. This is a guideline change — deliberate, documented, traceable.
- **discarded**: one-off, modeling error, or not generalizable

### Adverse events (fast track)
When `severity = 'adverse'` (geometry crashes, structural impossibility, code error in L3 script), the case note gets flagged for immediate review. These skip the slow lifecycle.

## The review board

Not an agent — a human session. Periodically (after a modeling sprint, after testing new L3 scripts, at project milestones):

1. Read all pending case notes: `SELECT * FROM case_notes WHERE status = 'pending'`
2. For each: is this real? Confirm or discard.
3. For confirmed notes: are there patterns? Group by `related_id` and `finding`.
4. For patterns (3+ confirmed notes with same finding): decide whether to update the base value.
5. If promoting: update L1 value, add source attribution ("updated from case notes #12, #15, #23"), update L2 guide if the explanation changed.

## What this means for existing repo files

| File | Role in new framework | Changes? |
|------|----------------------|----------|
| LEARNINGS.md | Highlights reel — most important case notes, always loaded | No change. Stays as-is. New learnings that matter enough get a one-liner added here. |
| observations/INDEX.md | Research findings, dead ends, theory | No change. Different scope — project-level observations, not base-level case notes. |
| state/sessions/ | Session logs — when, what, who | No change. Operational history. |
| 00_Workflow_v04.md | Modeling conventions | No change. This is doctrine (L2-level), not case notes. |

**Nothing existing changes.** The case_notes table is additive — it lives inside each base's SQLite database. The review process is a human session, not automation. LEARNINGS.md keeps working exactly as it does now.

## How it connects to the review workflow

`/rhino-review` already checks geometry. The change:

**Before:** Review findings go to chat → disappear after session.
**After:** Review findings go to chat AND to `case_notes` table in the relevant base.

The review agent needs to know which base to write to:
- Joint geometry wrong → iboisbase case note
- RhinoCommon method used incorrectly → rhinobase case note
- Structural constraint violated → archibase case note
- General modeling issue → LEARNINGS.md (no base, stays in repo)

## Example: full cycle

1. **Guideline**: iboisbase says Vidy tenon-mortise chamfer_offset = -0.75 (from compas_wood)
2. **Modeling**: Agent builds Lock 07 Rennaz, uses chamfer_offset = -0.75 on a 180mm timber section
3. **Review**: `/rhino-review` catches boolean failure — chamfer creates geometry thinner than Rhino tolerance
4. **Case note**: severity=warning, context="Lock 07, 180mm section, 1:200", recommendation="use -0.5 below 200mm"
5. **Status**: pending
6. **Later**: Andrea reviews, confirms the finding. Status → confirmed.
7. **Later**: Same issue found in Lock 03 (Morges, 160mm section) and Lock 08 (Montreux, 190mm). Three confirmed notes with the same pattern.
8. **Review board**: Status → pattern → promoted. Base value updated: chamfer_offset = -0.75 with annotation "reduce to -0.5 for sections < 200mm". L2 guide updated with the scale-dependent rule.
9. **LEARNINGS.md**: One-liner added: "Vidy tenon-mortise chamfer fails below 200mm section — see iboisbase case notes #4, #7, #9"
