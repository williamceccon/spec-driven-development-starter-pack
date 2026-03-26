#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SOURCE="$SCRIPT_DIR/../skills"
TARGETS=(
  "${CODEX_HOME:-$HOME/.codex}/skills"
  "$HOME/.claude/skills"
  "$HOME/.config/opencode/skills"
  "$HOME/.agents/skills"
)

for target_root in "${TARGETS[@]}"; do
  mkdir -p "$target_root"
  for skill_dir in "$SKILLS_SOURCE"/*; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    rm -rf "$target_root/$skill_name"
    cp -R "$skill_dir" "$target_root/$skill_name"
    echo "Installed $skill_name to $target_root/$skill_name"
  done
done

echo "Restart the agent session you use so new global skills are discovered."
