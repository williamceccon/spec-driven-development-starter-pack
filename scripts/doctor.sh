#!/usr/bin/env bash
set -euo pipefail

missing=0
for tool in git python3 node npm uv poetry gh specify; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Missing tool: $tool"
    missing=1
  fi
done

CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
for skill in specify-workflow-pack brainstorming gh-fix-ci gh-address-comments; do
  if [ ! -f "$CODEX_HOME_DIR/skills/$skill/SKILL.md" ]; then
    echo "Missing global skill: $skill"
    missing=1
  fi
done

if [ "$missing" -ne 0 ]; then
  echo "Run bash ./scripts/install-workflow-pack.sh after cloning the starter."
  exit 1
fi

echo "Machine doctor passed."
