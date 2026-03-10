#!/usr/bin/env bash
set -euo pipefail

# Safe push: pull first, then push. NEVER force-pushes. NEVER deletes.
#
# Usage: bash tools/git/safe_push.sh

echo "=== Safe Push ==="

# Check we're in a git repo
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "ERROR: Not in a git repository."
    exit 1
fi

BRANCH=$(git branch --show-current)
echo "Branch: $BRANCH"

# Warn if on main
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo "WARNING: You are on '$BRANCH'. Are you sure you want to push directly?"
    echo "Continuing (use Ctrl+C to abort)..."
fi

# Check for uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "WARNING: You have uncommitted changes. Commit first, then push."
    git status --short
    exit 1
fi

# Pull before push
echo
echo "Pulling latest..."
git pull --rebase || {
    echo "ERROR: Pull failed. Resolve conflicts, then retry."
    exit 1
}

# Push (NEVER force)
echo
echo "Pushing..."
git push || {
    echo "ERROR: Push failed."
    exit 1
}

echo
echo "=== Push complete ==="
echo "Branch: $BRANCH"
