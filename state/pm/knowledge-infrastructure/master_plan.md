# Master Plan: Knowledge Infrastructure — Feedback Loop

**Goal:** Add case_notes tables to knowledge bases + wire review workflow to write there. Test during lock modeling sessions.

**Created:** 2026-03-26
**Priority:** Post-midterm. First test when modeling resumes.
**Status:** Planned, not started
**Depends on:** rhinobase-iboisbase project (needs at least one base with data to annotate)

---

## Why

Knowledge bases are currently extract-once, query-forever. The medical guidelines model adds a feedback loop: modeling → review → case notes → pattern detection → base updates. Nothing existing changes — this is additive.

Framework documented at: `observations/research/strategy/knowledge_feedback_framework.md`

---

## Phase Overview

```
Phase 1: Schema + Review Wiring ──────── ~1 hr, single session
  └── Add case_notes table to base schemas
  └── Update /rhino-review to write case notes

Phase 2: First Test (during lock modeling) ── no extra time, piggybacks on modeling
  └── Model a lock → review → verify case notes are written correctly

Phase 3: First Review Board ─────────── ~30 min, after 3+ modeling sessions
  └── Andrea reviews accumulated case notes
  └── Confirm/discard/pattern/promote cycle
```

---

## Phase 1: Schema + Review Wiring (1 session, ~1 hr)

**Topology:** Single agent, sequential.

**Tasks:**
1. Add `case_notes` table to base SQLite schema template (the CREATE TABLE from the framework doc)
2. Update `/rhino-review` command to accept an optional `--base [archibase|rhinobase|iboisbase]` flag
3. When review finds an issue, format it as a case note and write to the relevant base's DB
4. If no base is relevant, append to LEARNINGS.md as before (fallback)
5. Print case note to chat so Andrea sees it in real-time

**Does NOT touch:**
- LEARNINGS.md (stays as-is)
- observations/ (stays as-is)
- state/sessions/ (stays as-is)
- Any existing workflow or command beyond /rhino-review

**Success criteria:**
- `/rhino-review` produces a case note in the correct base's SQLite when it finds an issue
- Case note has full context: lock node, scale, agent, finding, recommendation, severity
- Fallback to LEARNINGS.md works when no base is relevant

---

## Phase 2: First Test (during lock modeling, no extra session needed)

**Piggybacks on:** First lock modeling session post-midterm (likely Lock 07 Rennaz or Lock 03 Morges).

**What to verify:**
- Case notes are being written with correct context
- Severity classification makes sense (observation vs warning vs adverse)
- The case notes are queryable: `SELECT * FROM case_notes WHERE lock_node = 'rennaz'`
- No interference with the modeling workflow

---

## Phase 3: First Review Board (~30 min, after 3+ modeling sessions)

**When:** After enough case notes have accumulated to be worth reviewing (minimum ~10 pending notes across 3+ sessions).

**Tasks:**
1. Query all pending case notes across all bases
2. For each: confirm or discard
3. Look for patterns (same finding across different locks/scales)
4. If pattern found: decide whether to promote (update base) or keep as annotated edge case
5. Add important findings to LEARNINGS.md as one-liners

**This is a human session, not an automated process.**
