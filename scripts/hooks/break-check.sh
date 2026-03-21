#!/bin/bash
# Break reminder hook for city101 team sessions
# Runs as part of the Stop hook. Checks session log for the last
# break marker. If 90+ minutes have passed, outputs a gentle reminder
# to stderr (injected into Claude's context).

LOG=/Users/andreacrespo/CLAUDE/city101/state/session-log.md
TODAY=$(date '+%Y-%m-%d')

# Only run if today's log exists
if [ ! -f "$LOG" ] || ! head -1 "$LOG" | grep -q "$TODAY"; then
  exit 0
fi

# Find the last break marker or session start
LAST_CHECK=$(grep '\[break\]' "$LOG" | tail -1 | grep -oE '[0-9]{2}:[0-9]{2}')

if [ -z "$LAST_CHECK" ]; then
  # No break today — use first log entry as session start baseline
  LAST_CHECK=$(grep '^- ' "$LOG" | head -1 | grep -oE '[0-9]{2}:[0-9]{2}')
fi

# If we still have no reference time, skip
[ -z "$LAST_CHECK" ] && exit 0

# Calculate elapsed minutes
LAST_H=$(echo "$LAST_CHECK" | cut -d: -f1)
LAST_M=$(echo "$LAST_CHECK" | cut -d: -f2)
NOW_H=$(date '+%H')
NOW_M=$(date '+%M')
ELAPSED=$(( (10#$NOW_H * 60 + 10#$NOW_M) - (10#$LAST_H * 60 + 10#$LAST_M) ))

# Handle midnight crossing
if [ "$ELAPSED" -lt 0 ]; then
  ELAPSED=$(( ELAPSED + 1440 ))
fi

if [ "$ELAPSED" -ge 90 ]; then
  echo "[BREAK REMINDER — ${ELAPSED} min since last break] It's been a while — good moment for water, stretching, or stepping away for a few minutes." >&2
fi
