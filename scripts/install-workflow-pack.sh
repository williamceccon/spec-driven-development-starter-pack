#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_SOURCE="$SCRIPT_DIR/../skills/specify-workflow-pack"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
SKILL_TARGET="$CODEX_HOME_DIR/skills/specify-workflow-pack"
mkdir -p "$(dirname "$SKILL_TARGET")"
rm -rf "$SKILL_TARGET"
cp -R "$SKILL_SOURCE" "$SKILL_TARGET"
echo "Installed specify-workflow-pack to $SKILL_TARGET"
