# Utility: Session End

Close the session: commit all work, sync with remote, flag Drive uploads.

## Steps

### 1. Pull first
```
git pull
```
Get any changes from remote before committing.

### 2. Review all local changes
Run `git status` and `git diff`. Identify everything that changed this session.

### 3. Commit by category
Group changed files by type and commit each group with the correct prefix:
- `[DATA]` — datasets, CSVs, GeoJSON
- `[VIZ]` — visualizations, charts, HTML
- `[MAP]` — map outputs, spatial files
- `[MODEL]` — 3D models, geometry
- `[FIND]` — documented discoveries
- `[DEAD]` — documented dead ends
- `[BUILD]` — deployment, packaging

Do NOT bundle unrelated changes into one commit. Each commit = one logical piece of work.

### 4. Flag Drive uploads
Check for any new or modified files that are gitignored (PNG, PDF, PPTX, QGZ, 3DM, etc.).
For each one, tell the user:
- **File**: the local path
- **Upload to**: the matching Drive folder:

  | Type | Drive folder |
  |------|-------------|
  | Datasets (CSV, GeoJSON) | `City101_Team_Drive/03_Datasets/[subfolder matching repo]` |
  | Maps (PNG/PDF exports) | `City101_Team_Drive/05_Maps/` |
  | Narrative docs | `City101_Team_Drive/02_Narrative/` |
  | Scripts | `City101_Team_Drive/04_Scripts/` |
  | Research | `City101_Team_Drive/06_Research/` |
  | QGIS project (.qgz) | `City101_Team_Drive/` (root) |
  | Presentations (.pptx) | `City101_Team_Drive/07_Deliverables/A0X/` |
  | Field photos | `City101_Team_Drive/07_Deliverables/A0X/fieldwork/` |
  | Workflow docs | `City101_Team_Drive/00_Workflow/` |

- **Placeholder**: create or update a `.md` placeholder next to the gitignored file with: description, Drive location, last updated date, author.

### 5. Quick retro (automatic)
Before updating context, reflect on the session:
- **What worked?** — tools, approaches, or decisions that went well
- **What didn't?** — friction, dead ends, things that took too long
- **What did we learn?** — anything worth adding to LEARNINGS.md
- **Patterns noticed?** — did we use a temporary role or repeat a workflow that should be formalized? If something happened 3+ times across sessions, propose making it a tool, workflow, or permanent role.

Share the retro with the user (keep it brief — 3-5 bullet points total). Append any genuine learnings to LEARNINGS.md. Don't force it — if the session was straightforward, say so.

### 6. Update context files
- **CONTEXT.md** — update shared project state if phase, narrative, or key decisions changed.
- **CONTEXT_ANDREA.md** or **CONTEXT_HENNA.md** — add session log entry: what happened, files created/modified, findings, blockers. Keep entries concise.

### 7. Handoff note (automatic)
Write a handoff section in the person's CONTEXT file (CONTEXT_ANDREA.md or CONTEXT_HENNA.md) under a `## Handoff` heading. This is what the OTHER person (or a future Claude session) needs to know:
- **What was done** — brief summary of deliverables and changes
- **What's next** — immediate next steps, in priority order
- **Watch out for** — blockers, open questions, things that might break
- **Files to look at** — key files created or modified this session

Keep it short enough to scan in 30 seconds. Overwrite the previous handoff each time — it's always "latest state," not a log.

### 8. Update LOCKBOARD.md
Reflect current state: what each person is working on, any blockers.

### 9. Final sync commit and push
```
git add CONTEXT.md CONTEXT_ANDREA.md CONTEXT_HENNA.md LOCKBOARD.md [any new placeholder .md files]
git commit -m "[SYNC] Session end — [brief description]"
git pull --rebase
git push
```

## Safety
- Never force-push
- Never commit to main directly if on a feature branch
- Pull before push to avoid conflicts
- Ask before committing files the user hasn't mentioned
