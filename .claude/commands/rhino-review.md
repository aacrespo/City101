# Skill: Rhino Review

Run the 5-lens review panel on a lock model's current state in Rhino.

## Input
Arguments: `<lock_number> <log_target>`
Example: `03 400` or `07 300`
If not provided, ask for both.

## Prerequisites
- Rhino MCP must be running
- Lock geometry must exist in Rhino
- `workflows/log-400-checklist.md` must exist

## Process

### Step 1: Gather Review Materials

Via Rhino MCP:
1. **Capture 4 viewports:**
   - Perspective (showing overall form)
   - Plan / top view
   - Section (through the gate/threshold)
   - Detail (closest architectural feature)

2. **Get document summary** — layer tree listing

3. **Get geometry summary:**
   - Object count per layer
   - Bounding box dimensions
   - Key measurements (spans, heights, widths)

4. **Read the lock concept** from `output/city101_hub/prototypology_content.json`

5. **Write review materials** to `output/city101_hub/reviews/lock_XX_logYYY/materials.md`

### Step 2: Spawn Review Panel

Spawn all 5 reviewers as a team (they can read each other's output):

| Reviewer | Agent | Writes to |
|----------|-------|-----------|
| Concept Critic | `.claude/agents/concept-critic.md` | `reviews/lock_XX_logYYY/concept_critic.md` |
| Structural | `.claude/agents/structural-reviewer.md` | `reviews/lock_XX_logYYY/structural.md` |
| Envelope | `.claude/agents/envelope-reviewer.md` | `reviews/lock_XX_logYYY/envelope.md` |
| Accessibility | `.claude/agents/accessibility-reviewer.md` | `reviews/lock_XX_logYYY/accessibility.md` |
| LOG Compliance | `.claude/agents/log-compliance-reviewer.md` | `reviews/lock_XX_logYYY/log_compliance_and_summary.md` |

Spawn concept-critic, structural, envelope, and accessibility in parallel. Spawn log-compliance-reviewer after the others complete (it reads all reviews and compiles the summary).

### Step 3: Report Results

Read the compiled summary from `log_compliance_and_summary.md` and present:
- PASS/FAIL per reviewer
- Cross-reviewer tensions
- Critical fixes (must-do)
- Suggested improvements
- Ready to advance: YES/NO

### Step 4: Handle Iteration (if needed)

If any reviewer FAILed:
1. List the specific fixes needed
2. After modeler applies fixes, re-run ONLY the failed lenses (not all 5)
3. Max 3 iterations per LOG stage — if still failing, flag for human review

## Output
- Review materials in `output/city101_hub/reviews/lock_XX_logYYY/`
- 5 reviewer reports + compiled summary
- Print: verdict and fix list
