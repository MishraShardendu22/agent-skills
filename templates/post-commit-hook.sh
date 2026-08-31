#!/usr/bin/env bash
# ==============================================================================
# Git Post-Commit Hook — Autonomous Skills Hub Auto-Sync Template
# ==============================================================================
# Add this file to .githooks/post-commit or .git/hooks/post-commit in any repo
# to automatically push new skills upstream whenever a commit modifies .agents/skills/.
# ==============================================================================

set -euo pipefail

if git diff-tree --no-commit-id --name-only -r HEAD | grep -E '^(\.agents/skills/|skills/)' >/dev/null 2>&1; then
    echo "[INFO] Detected changes in .agents/skills/. Triggering automated background sync to agent-skills hub..."
    
    if command -v skills-sync >/dev/null 2>&1; then
        ( skills-sync push >/dev/null 2>&1 & )
    elif [[ -x "./scripts/skills-sync.sh" ]]; then
        ( ./scripts/skills-sync.sh push >/dev/null 2>&1 & )
    fi
fi

exit 0
