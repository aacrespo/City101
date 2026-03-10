# Workflow: Session Management

## Objective
Consistent session start and end procedures for context continuity.

## When to use
- `/session-start` at the beginning of every working session
- `/session-end` at the end of every working session

## Session Start — Steps
1. **Read `CONTEXT.md`** — what's the current project state?
2. **Read `LOCKBOARD.md`** — who's doing what? Any blockers?
3. **Summarize**:
   - Current phase and recent progress
   - Active work per person
   - Blocked items
   - Recommended next steps
4. **Do not modify any files** — session-start is read-only

## Session End — Steps
1. **Update `CONTEXT.md`**:
   - Add today's date and session summary
   - What was accomplished
   - Decisions made
   - Files created or modified
   - Open questions or blockers
2. **Update `LOCKBOARD.md`**:
   - Current work status per person
   - Any new blockers
3. **Commit**:
   ```bash
   git add CONTEXT.md LOCKBOARD.md
   git commit -m "[SYNC] Session end — [brief description]"
   ```
4. **Push**:
   ```bash
   git pull --rebase
   git push
   ```

## Safety
- Never force-push
- Pull before push
- If merge conflict on CONTEXT.md: keep both versions, manually reconcile

## Expected output
- Updated CONTEXT.md and LOCKBOARD.md
- Clean [SYNC] commit pushed to remote

## History
- 10 March 2026: Created (v7 repo setup)
