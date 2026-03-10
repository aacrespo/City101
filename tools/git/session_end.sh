#!/usr/bin/env bash
set -euo pipefail

# Session end: stage context files, commit with [SYNC], pull, push.
# Safety: NEVER force-pushes. NEVER deletes branches. Pulls before push.
#
# Usage: bash tools/git/session_end.sh "brief description of session"

DESCRIPTION="${1:-session update}"
DATE=$(date +%Y-%m-%d)

echo "=== Session End ==="
echo "Date: $DATE"
echo "Description: $DESCRIPTION"
echo

# Check we're in a git repo
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "ERROR: Not in a git repository."
    exit 1
fi

BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"

# Warn if on main
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo "WARNING: You are on '$BRANCH'. Consider using a feature branch."
    echo "Continuing anyway (session-end context updates are OK on main)."
fi

# Stage context files
echo
echo "Staging CONTEXT.md and LOCKBOARD.md..."
git add CONTEXT.md LOCKBOARD.md 2>/dev/null || true

# Check if there's anything to commit
if git diff --cached --quiet; then
    echo "Nothing staged to commit. CONTEXT.md and LOCKBOARD.md unchanged."
    exit 0
fi

# Commit
COMMIT_MSG="[SYNC] Session end — $DESCRIPTION ($DATE)"
echo "Committing: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

# Pull before push (rebase to keep history clean)
echo
echo "Pulling latest changes..."
git pull --rebase || {
    echo "ERROR: Pull failed. Resolve conflicts manually, then push."
    exit 1
}

# Push (NEVER force)
echo
echo "Pushing..."
git push || {
    echo "ERROR: Push failed. Check remote and try again."
    exit 1
}

echo
echo "=== Session end complete ==="
echo "Commit: $COMMIT_MSG"
echo "Branch: $BRANCH"
