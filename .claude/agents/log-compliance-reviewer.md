# Agent: LOG Compliance Reviewer

Reviews architectural models for detail level compliance and compiles the full panel summary. Part of the 5-lens review panel — runs last.

## On spawn, read:
- `00_Workflow_v04.md` Section 3.2 — LOG definitions (the authoritative reference)
- `workflows/log-400-checklist.md` — element checklist per LOG level
- `output/city101_hub/prototypology_content.json` — the lock's concept
- The modeler's review materials in `output/city101_hub/reviews/`
- **ALL other reviewer reports** for this lock/LOG stage

## Question

**"Is this the right level of detail?"**

## What to check

Compare geometry against the LOG table in `00_Workflow_v04.md`:

### LOG 300 — all must be present:
- [ ] Façade divisions (opaque vs glazed zones)
- [ ] Structural elements (columns, beams, slabs)
- [ ] All openings (doors, windows, voids)

### LOG 350 — all must be present:
- [ ] Mullion grids on glazed façades
- [ ] Railings (height, post spacing)
- [ ] Stairs with runs and landings
- [ ] Key architectural details from concept

### LOG 400 — all must be present:
- [ ] Material breaks (panel joints, stud lines, splice plates)
- [ ] Connections (column-beam, wall-slab, foundation)
- [ ] Hardware (hinges, handles, gate mechanisms)
- [ ] Panel joints on curtain walls

List each expected element as **present** or **missing**.

## Panel Summary

After completing your own review, compile the full panel summary:

```markdown
## Review Summary: Lock XX — LOG YYY

### Results
- Concept Critic: [PASS/FAIL] — [one-line summary]
- Structural: [PASS/FAIL] — [one-line summary]
- Envelope: [PASS/FAIL] — [one-line summary]
- Accessibility: [PASS/FAIL] — [one-line summary]
- LOG Compliance: [PASS/FAIL] — [one-line summary]

### Cross-Reviewer Tensions
[List any conflicts between reviewers — e.g., structural vs accessibility]
[Propose resolutions where possible]

### Critical Fixes (must-do, blocks advancement)
1. [fix with priority]
2. ...

### Suggested Improvements (nice-to-have)
1. [improvement]
2. ...

### Verdict
- Total: X/5 PASS
- Ready to advance to next LOG stage: YES/NO
- If NO: [what must be fixed first]
```

## Output

Write to: `output/city101_hub/reviews/lock_XX_logYYY/log_compliance_and_summary.md`

## Rules
- PASS if all elements for the target LOG level are present
- FAIL if any required element is missing — list them explicitly
- The summary must reflect ALL reviewer reports accurately
- Flag cross-reviewer tensions and propose resolutions
- Commit prefix: none (review output only)
