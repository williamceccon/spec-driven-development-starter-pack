#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SOURCE="$SCRIPT_DIR/../skills"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
SKILLS_TARGET="$CODEX_HOME_DIR/skills"
mkdir -p "$SKILLS_TARGET"

for skill_dir in "$SKILLS_SOURCE"/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  rm -rf "$SKILLS_TARGET/$skill_name"
  cp -R "$skill_dir" "$SKILLS_TARGET/$skill_name"
  echo "Installed $skill_name to $SKILLS_TARGET/$skill_name"
done

echo "Restart Codex to pick up new skills."
