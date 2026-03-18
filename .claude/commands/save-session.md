# /save-session — Bookmark current work

Run this when pausing work and planning to come back later. Captures everything needed to resume seamlessly. This is NOT the same as `/session-end` — save-session is a bookmark, session-end is a full close-out.

## Steps

1. **In parallel:**
   - `date '+%A %Y-%m-%d %H:%M'`
   - `git status` and `git log --oneline -3`
   - Read `LOCKBOARD.md`

2. **Review the conversation** — what was done, what's open, what was the direction of work.

3. **Write session file** to `state/sessions/YYYY-MM-DD_HHMM.md`:

```markdown
# Session — [YYYY-MM-DD HH:MM]
**Who:** [which team member was working — Andrea/Henna]
**Account:** [Cairn/Cairn Code/Lumen/Meridian/Cadence]

## What we did
- [bullet points of work completed, decisions made, files changed]

## Open threads
- [things started but not finished]
- [questions raised but not answered]

## Blockers
- [anything preventing progress, if any]

## Git state
- Branch: [branch name]
- Status: [clean / uncommitted: list files]
- Last commits: [last 3 oneline]

## Context to restore
- [what we were thinking about / working toward]
- [any decisions that need follow-up]

## Resume with
→ [The ONE thing to pick up first when resuming]
```

4. **Mark break in session log:**
   ```bash
   echo "- $(date '+%A %H:%M') [break] session saved" >> state/session-log.md
   ```

5. **Commit** the session file.

## Behavior
- Be concise but complete — `/resume-session` will read this file.
- If the person mentioned being stuck or having a specific next step in mind, capture that.
