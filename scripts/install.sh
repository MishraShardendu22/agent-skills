#!/usr/bin/env bash
# ==============================================================================
# Installer for skills-sync CLI tool
# Usage: curl -fsSL https://raw.githubusercontent.com/MishraShardendu22/agent-skills/main/scripts/install.sh | bash
# ==============================================================================

set -eo pipefail

REPO="MishraShardendu22/agent-skills"
BRANCH="main"
RAW_URL="https://raw.githubusercontent.com/${REPO}/${BRANCH}/scripts/skills-sync.sh"
TARGET_DIR="${HOME}/.local/bin"
TARGET_BIN="${TARGET_DIR}/skills-sync"

echo "[INFO] Installing skills-sync from ${REPO}..."

mkdir -p "$TARGET_DIR"

if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$RAW_URL" -o "$TARGET_BIN"
elif command -v wget >/dev/null 2>&1; then
    wget -qO "$TARGET_BIN" "$RAW_URL"
else
    echo "[ERROR] Neither curl nor wget was found on your system."
    exit 1
fi

chmod +x "$TARGET_BIN"

echo "[SUCCESS] skills-sync installed successfully to ${TARGET_BIN}"

if [[ ":$PATH:" != *":${TARGET_DIR}:"* ]]; then
    echo ""
    echo "[WARN] ${TARGET_DIR} is not currently in your PATH."
    echo "       Add it by appending this line to your ~/.bashrc or ~/.zshrc:"
    echo "       export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo "[INFO] Run 'skills-sync --help' or 'skills-sync pull' in any repo to get started."
