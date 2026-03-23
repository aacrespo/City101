# Prompt: Execute Full Training Curriculum (Exercises 18–80)

*Run this in a fresh Claude Code session with Rhino open and `mcpstart` running (port 9002).*
*Requires: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json env.*

---

## What this does

63 construction detail exercises need to be modeled in Rhino. Every exercise is independent — no shared geometry. The full specs are in `output/agent_training/FULL_CURRICULUM.md`. Every dimension comes from the archibase knowledge files.

You are the **team lead**. You create the team, populate the shared task list, spawn teammates, and monitor. You never model anything yourself.

---

## Step 1: Create the team

Use `TeamCreate`:
```
team_name: "training-s3"
description: "Full construction detail training curriculum, exercises 18-80"
```

## Step 2: Create the task list (all 63 exercises)

Use `TaskCreate` for every exercise. Group into 5 waves using `blockedBy` dependencies — teammates auto-discover unblocked tasks.

**Task naming pattern:** `Ex{NN}: {short description}`
**Task description pattern:** Each task description should contain ONLY:
```
Exercise {NN} from output/agent_training/FULL_CURRICULUM.md
Phase {N}, Layer tree: Training{N}::Ex{NN}::*
X-offset: {value}mm, Y-offset: {value}mm
```

Do NOT paste exercise specs into task descriptions. Teammates read the curriculum file directly — this keeps your context clean.

### Wave 1: Floor Systems (no dependencies — starts immediately)
Tasks for Ex 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40

### Wave 2: Wall-Floor Junctions + Facades (blocked by Wave 1 completion)
Tasks for Ex 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29
Each task: `addBlockedBy` → pick ONE Wave 1 task as gate (e.g., the last task in Wave 1). This prevents all 12 from starting before Wave 1 has proven the pipeline works.

### Wave 3: Roof Systems (blocked by Wave 2 gate)
Tasks for Ex 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52

### Wave 4: Windows + Doors (blocked by Wave 3 gate)
Tasks for Ex 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67

### Wave 5: Foundations + Stairs + Structural (blocked by Wave 4 gate)
Tasks for Ex 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80

**Offset grid** to prevent spatial collision in Rhino:
- Within a wave, each exercise gets a unique position:
  - Y-offset: exercise index × 2000mm (exercises spaced 2m apart along Y)
  - X-offset: wave number × 20000mm (waves spaced 20m apart along X)

## Step 3: Spawn 4 teammates

Use the `Agent` tool with `team_name: "training-s3"` and distinct `name` values. Each teammate is a general-purpose agent.

**Teammate prompt (same for all 4, they differentiate by claiming different tasks):**

```
You are a construction detail modeling agent on team "training-s3".

<role>
You model construction details in Rhino via MCP. You claim tasks from the shared task list, model each exercise, and mark tasks complete. You work autonomously.
</role>

<setup>
Before your first exercise, read these files ONCE and keep them in context:
1. `.claude/agents/knowledge/rhino-playbook.md` — modeling doctrine (the Three Laws, naming, metadata)
2. `output/agent_training/FULL_CURRICULUM.md` — find your claimed exercise, read ONLY that section

For each exercise, also read the relevant source file from:
`~/CLAUDE/archibase/source/knowledge/construction_details/`
(the curriculum tells you which source file and page)
</setup>

<workflow>
1. Call TaskList to see available (pending, unblocked, unowned) tasks
2. Claim one task: TaskUpdate with owner = your name, status = in_progress
3. Read the exercise spec from FULL_CURRICULUM.md (just that exercise)
4. Read the source detail file for exact dimensions
5. Model in Rhino:
   a. Create the layer tree (e.g., Training4::Ex30::HollowClayBlock::*)
   b. Use this box helper at the top of every script:
      ```python
      def box(x, y, z, L, W, H):
          pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
                 (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
          return rs.AddBox(pts)
      ```
   c. Use the X/Y offset from the task description (prevents collision with other agents)
   d. Model every layer with correct thickness from the source
   e. Name every object (rs.ObjectName) and tag material (rs.SetUserText)
   f. Print summary: exercise number, object count, layer thicknesses
6. Self-review: check Three Laws (thickness, no overlap, nothing floats)
7. Mark task completed: TaskUpdate with status = completed
8. Check TaskList for next available task — claim and repeat
9. When no more tasks are available, notify the lead
</workflow>

<communication>
- If you discover a useful technique (e.g., sloped box pattern for roofs), message your teammates so they benefit:
  SendMessage to "*" with the technique. Keep it brief — one pattern, one example.
- If you hit a Rhino error, try once more. If it persists, mark the task description with the error and move on to the next task.
- If you need a dimension that's ambiguous in the curriculum, check the archibase source file directly. If still unclear, message the lead.
</communication>

<quality>
For EVERY object:
- rs.ObjectName(obj, "LayerName_LevelOrZone_Material")
- rs.SetUserText(obj, "material", "material_name")
- rs.SetUserText(obj, "thickness_mm", "value")
- rs.CurrentLayer("Correct::Layer::Path") BEFORE creation

For EVERY exercise:
- Total assembly thickness must match the source (±1mm for rounding)
- Section test: if you cut through the model, every layer is visible with correct thickness
- No two objects share the same physical space
</quality>
```

Spawn 4 modelers with names: `modeler-1`, `modeler-2`, `modeler-3`, `modeler-4`

### Reviewer teammates (2 additional agents)

Spawn alongside the modelers. They wait for review tasks to unblock.

**Teammate 5: `reviewer-constraints` (Mode A)**

```
You are the constraint reviewer on team "training-s3".

<role>
You verify that completed exercises meet dimensional and structural correctness. You do NOT model anything — you inspect what the modelers built and report issues.
</role>

<setup>
Read once:
1. `.claude/agents/knowledge/rhino-playbook.md` — the Three Laws and review checklist
2. `output/agent_training/FULL_CURRICULUM.md` — reference for expected dimensions
</setup>

<workflow>
1. Call TaskList — look for review tasks (prefixed "Review:") that are pending and unblocked
2. Claim a review task
3. For the exercise being reviewed:
   a. Read the exercise spec from FULL_CURRICULUM.md to know expected dimensions
   b. Query Rhino for all objects on that exercise's layer tree:
      ```python
      import rhinoscriptsyntax as rs
      objs = rs.ObjectsByLayer("Training4::Ex30::*", True)  # recursive
      print(f"Object count: {len(objs)}")
      for obj in objs:
          name = rs.ObjectName(obj)
          mat = rs.GetUserText(obj, "material")
          bb = rs.BoundingBox(obj)
          if bb:
              dims = [bb[1][0]-bb[0][0], bb[3][1]-bb[0][1], bb[4][2]-bb[0][2]]
              print(f"  {name}: {mat}, dims={[round(d,1) for d in dims]}")
      ```
   c. Verify:
      - Object count matches expected (from curriculum)
      - Every object has name AND material metadata
      - Total assembly thickness matches source (sum layer thicknesses, compare to expected total)
      - No bounding-box overlaps between objects on the same layer tree
      - Layer tree structure matches curriculum specification
   d. Write result to task: PASS or FAIL with specific issues
4. If FAIL: message the original modeler directly with what needs fixing:
   SendMessage to "modeler-X": "Ex30 FAIL: missing soffit plaster layer, total thickness 332mm vs expected 342mm"
5. Mark review task completed
6. Claim next review task
</workflow>

<judgement>
- PASS: all dimensions within ±2mm, all metadata present, no overlaps, correct object count (±1)
- WARN: minor issue (e.g., one object missing material tag, thickness off by 3-5mm) — pass with note
- FAIL: structural issue (missing layer, wrong total thickness >5mm, overlapping geometry, wrong layer tree)
</judgement>
```

**Teammate 6: `reviewer-visual` (Mode B)**

```
You are the visual reviewer on team "training-s3".

<role>
You compare Rhino viewport captures of completed exercises against the original construction detail drawings from Deplazes and Vittone. You verify visual coherence — does the model LOOK like the source detail?
</role>

<source-pdfs>
The original book illustrations are in these PDFs:
- Deplazes: ~/CLAUDE/archibase/source/855495177-s03-Andrea-Deplazes-constructing-Architecture.pdf
- Vittone: ~/CLAUDE/archibase/source/806480992-Batir-Manuel-de-la-construction-Rene-Vittone-PDF-FR.pdf

Every exercise in FULL_CURRICULUM.md has a source page reference (e.g., "Deplazes p.421"). Use the Read tool with the `pages` parameter to view the original illustration.
</source-pdfs>

<workflow>
1. Call TaskList — look for visual review tasks (prefixed "VisualReview:") that are pending and unblocked
2. Claim a visual review task
3. For the exercise being reviewed:
   a. Read the exercise spec from FULL_CURRICULUM.md to get the source page number
   b. Read the source PDF page:
      - For Deplazes exercises: Read ~/CLAUDE/archibase/source/855495177-s03-Andrea-Deplazes-constructing-Architecture.pdf pages="{page}"
      - For Vittone exercises: Read ~/CLAUDE/archibase/source/806480992-Batir-Manuel-de-la-construction-Rene-Vittone-PDF-FR.pdf pages="{page}"
      This gives you the ORIGINAL construction detail drawing.
   c. Capture viewport of the modeled exercise in Rhino:
      - First, isolate the exercise layers and frame the view:
      ```python
      import rhinoscriptsyntax as rs
      # Hide all layers except this exercise
      all_layers = rs.LayerNames()
      exercise_prefix = "Training4::Ex30"  # adjust per exercise
      for layer in all_layers:
          if layer.startswith(exercise_prefix):
              rs.LayerVisible(layer, True)
          else:
              rs.LayerVisible(layer, False)
      rs.ZoomExtents()
      ```
      - Then capture: use rhino_capture_viewport tool
      - Capture from TWO angles:
        1. Front/section view (orthographic — shows layer stack)
        2. Perspective view (shows 3D assembly)
   d. Compare the Rhino screenshots against the PDF page:
      - Layer ordering: does the model stack layers in the same order as the drawing?
      - Proportions: is the thickest layer visually the thickest? Are thin layers (2mm render, 0.6mm metal) visibly thin?
      - Assembly logic: does the model show the same construction principle? (e.g., warm deck vs cold deck, insulation position, bearing points)
      - Missing elements: anything in the drawing that's not in the model?
      - Extra elements: anything in the model that's not in the drawing?
   e. Save screenshots to: output/agent_training/visual_review/ex{NN}_section.png and ex{NN}_perspective.png
      (Create the directory if it doesn't exist)
   f. Write a brief visual review note to: output/agent_training/visual_review/ex{NN}_review.md
      Format:
      ```
      # Ex{NN}: {title}
      Source: {book} p.{page}

      ## Comparison
      - Layer order: MATCH / MISMATCH (detail)
      - Proportions: MATCH / MISMATCH (detail)
      - Assembly logic: MATCH / MISMATCH (detail)
      - Missing elements: none / list
      - Extra elements: none / list

      ## Verdict: PASS / WARN / FAIL
      ```
4. If FAIL: message the modeler with what looks wrong:
   SendMessage to "modeler-X": "Ex30 visual FAIL: insulation layer appears above WP in your model but source shows it below. Check warm deck vs cold deck logic."
5. Mark visual review task completed
6. Claim next visual review task
</workflow>

<judgement>
- PASS: model visually matches the source detail drawing in layer order, proportions, and assembly logic
- WARN: minor visual discrepancy (e.g., slightly different proportions but correct logic)
- FAIL: model shows wrong construction principle, missing major element, or fundamentally different layer arrangement than the source
</judgement>
```

### Review task creation

For each modeling exercise, create TWO review tasks that are blocked by the modeling task:

1. `Review: Ex{NN} constraints` — blocked by `Ex{NN}` modeling task, owned by reviewer-constraints
2. `VisualReview: Ex{NN} visual` — blocked by `Ex{NN}` modeling task, owned by reviewer-visual

This means: as soon as a modeler completes an exercise, both review tasks auto-unblock. Reviewers pick them up from the shared task list without lead intervention.

Total tasks: 63 modeling + 63 constraint reviews + 63 visual reviews = **189 tasks**.

### Team summary

| Teammate | Role | Count | Works on |
|----------|------|-------|----------|
| modeler-1 through modeler-4 | Build exercises | 4 | Modeling tasks (self-assigned from pool) |
| reviewer-constraints | Dimensional verification | 1 | Review tasks (auto-unblock after modeling) |
| reviewer-visual | Visual comparison against source PDFs | 1 | VisualReview tasks (auto-unblock after modeling) |
| **Total** | | **6** | |

Spawn all 6 with: `modeler-1`, `modeler-2`, `modeler-3`, `modeler-4`, `reviewer-constraints`, `reviewer-visual`

## Step 4: Monitor

After spawning, your job is lightweight:

1. **Watch for messages.** Teammates auto-deliver messages when they complete tasks or hit issues.
2. **Check TaskList periodically** (every ~5 minutes or when a teammate goes idle). Print a brief progress summary for the user:
   ```
   Wave 1: 8/11 done | Wave 2: blocked | ...
   ```
3. **Handle failures.** If a teammate reports an error, note it. Don't intervene unless it's blocking other work.
4. **Wave transitions are automatic.** When the gate task for a wave completes, blocked tasks auto-unblock. Teammates discover them via TaskList.
5. **When all tasks complete**, print the final summary and shut down teammates:
   ```
   SendMessage to each: { type: "shutdown_request", reason: "All exercises complete" }
   ```

## Step 5: Wrap up

After all teammates shut down:

1. Print final summary:
```
| Wave | Exercises | Modeled | Constraint Review | Visual Review | Objects |
|------|-----------|---------|-------------------|---------------|---------|
| 1    | 30-40     | ?/11    | ? PASS / ? FAIL   | ? PASS / ? FAIL | ?     |
| 2    | 18-29     | ?/12    | ? PASS / ? FAIL   | ? PASS / ? FAIL | ?     |
| 3    | 41-52     | ?/12    | ? PASS / ? FAIL   | ? PASS / ? FAIL | ?     |
| 4    | 53-67     | ?/15    | ? PASS / ? FAIL   | ? PASS / ? FAIL | ?     |
| 5    | 68-80     | ?/13    | ? PASS / ? FAIL   | ? PASS / ? FAIL | ?     |
```

2. Capture viewport of full Rhino model (rhino_capture_viewport) — one aerial showing all exercises

3. Compile visual review gallery: list all screenshots in `output/agent_training/visual_review/` with their PASS/WARN/FAIL verdicts. This directory is the deliverable Andrea can browse to compare models against source details.

4. If failures exist:
   - Constraint failures: spawn a fix-up modeler to address specific issues
   - Visual failures: flag for human review (these may be judgement calls)

5. TeamDelete to clean up

---

## Why Agent Teams (not subagents)

| Feature | Subagents | Agent Teams |
|---------|-----------|-------------|
| Context | Share lead's context | Each has own context |
| Communication | Report back to lead only | Message each other directly |
| Task claiming | Lead assigns explicitly | Self-serve from shared list |
| Idle handling | Wasted | Auto-claim next task |
| Technique sharing | Can't | Broadcast to teammates |
| Lead context cost | Grows with each agent report | Stays flat (just task status) |

The key wins:
- **Self-balancing workload**: Fast agents claim more tasks. No idle waste.
- **Technique propagation**: When modeler-1 figures out the sloped box pattern for roofs, it broadcasts to all. Modeler-3 picks it up for its roof exercises without the lead relaying.
- **Lead stays lean**: You only hold task IDs and status counts, never exercise specs or geometry details.

## Context budget

- **Lead**: ~3K base + ~500 per status check × ~15 checks = ~10K. Very comfortable.
- **Each modeler**: ~5K (prompt+playbook) + ~3K per exercise (read from file, model, discard) × ~16 exercises = ~53K peak. Comfortable within 200K context.
- **reviewer-constraints**: ~5K (prompt+playbook) + ~2K per review × ~63 reviews. Will compress older reviews — only needs current exercise in focus. ~15K active.
- **reviewer-visual**: ~5K (prompt) + ~5K per review (PDF page + 2 screenshots + comparison) × ~63 reviews. Heaviest context user due to images. Will need to compress aggressively — only hold current exercise's images. ~20K active.
- **Total agents**: 6 concurrent. Lead + 4 modelers + 2 reviewers.

## Timing estimate

- Each modeling exercise: ~3-5 minutes (read spec, model 8-16 objects, self-review)
- Each constraint review: ~1-2 minutes (query Rhino, check dimensions)
- Each visual review: ~2-3 minutes (read PDF page, capture viewport, compare, write note)
- 4 modelers in parallel produce ~1 completed exercise per minute
- 2 reviewers can keep up with ~1 review per 2 minutes each = 1 per minute combined
- Pipeline is balanced: modelers produce at same rate reviewers consume
- 63 exercises: ~70-90 minutes modeling + reviews run concurrently
- With overhead and wave gates: ~90-120 minutes total

---

## Alternative: No wave gates (maximum speed)

If you trust the pipeline and want maximum parallelism, skip the `blockedBy` dependencies entirely. Create all 63 tasks as immediately available. 4 teammates grab tasks in ID order and race through them.

**Pro:** Fastest possible execution. No waiting between waves.
**Con:** If there's a systematic issue (wrong Rhino port, bad helper function), all 4 agents hit it simultaneously before you can course-correct.

**Recommendation:** Use wave gates for the first run. If it succeeds, remove gates for future runs.

---

*Written 2026-03-22. Source: FULL_CURRICULUM.md (80 exercises, 63 new), rhino-playbook.md (doctrine), agent-team-modeling-v2.md (team workflow).*
