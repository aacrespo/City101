# /resume-session — Pick up where you left off

Run this when coming back after a break and wanting to continue from a saved session.

## Steps

1. **In parallel:**
   - `date '+%A %Y-%m-%d %H:%M'`
   - Find latest file in `state/sessions/` (if none exist, say so and suggest `/session-start`)
   - `git log --oneline -5`
   - `git status`

2. **Read the session file** found in step 1.

3. **Assess the gap:**
   - < 30 min → fast resume, skip check-in
   - 30–90 min → brief resume
   - 90+ min → suggest a stretch, then resume
   - Next day or later → suggest `/session-start` instead (full briefing)

4. **Check for changes since save:** compare git state from session file vs current — report only what changed (someone else may have pushed, or the other session may have committed).

5. **Present the resume briefing:**

```
## Welcome back

**Saved:** [when]
**Now:** [current time]
**Gap:** [duration]

### Where you left off
[1-3 sentences from "Context to restore" and "Open threads"]

### What changed since
- [git changes, new files, or "Nothing changed"]

### Pick up with
→ [The "Resume with" item from the session file]
```

## Behavior
- Speed is the goal. Get back into context fast.
- Don't re-explain things already known from the session file.
- If the gap is long (next day+), be honest and suggest a full `/session-start`.
