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

### 5. Update context files
- **CONTEXT.md** — update shared project state if phase, narrative, or key decisions changed.
- **CONTEXT_ANDREA.md** or **CONTEXT_HENNA.md** — add session log entry: what happened, files created/modified, findings, blockers. Keep entries concise.

### 6. Update LOCKBOARD.md
Reflect current state: what each person is working on, any blockers.

### 7. Final sync commit and push
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
