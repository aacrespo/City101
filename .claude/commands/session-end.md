# Utility: Session End

Follow `workflows/session-management.md` to close this session.

## Steps
1. **Update CONTEXT.md** — add what happened this session: decisions made, files created/modified, findings, blockers encountered. Keep it concise.
2. **Update LOCKBOARD.md** — reflect current state: what each person is working on, any new blockers.
3. **Stage and commit** with prefix `[SYNC]`:
   ```
   git add CONTEXT.md LOCKBOARD.md
   git commit -m "[SYNC] Session end — [brief description]"
   ```
4. **Pull then push**:
   ```
   git pull --rebase
   git push
   ```

## Safety
- Never force-push
- Never commit to main directly if on a feature branch
- Pull before push to avoid conflicts
