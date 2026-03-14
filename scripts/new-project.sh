#!/usr/bin/env bash
set -euo pipefail
NAME="${1:-}"
TARGET_PATH="${2:-}"
if [ -z "$NAME" ] || [ -z "$TARGET_PATH" ]; then
  echo "Usage: new-project.sh <name> <target-path>"
  exit 1
fi
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROFILE="$REPO_ROOT/profiles/python-fastapi-nextjs"
TARGET_REPO="$TARGET_PATH/$NAME"
if [ -e "$TARGET_REPO" ]; then
  echo "Target repo already exists: $TARGET_REPO"
  exit 1
fi
mkdir -p "$TARGET_REPO"
cp -R "$PROFILE/." "$TARGET_REPO"
python3 - <<PY
from pathlib import Path
path = Path(r'''$TARGET_REPO''') / 'workflow-pack.json'
path.write_text(path.read_text(encoding='utf-8').replace('REPLACE_ME', '$NAME'), encoding='utf-8')
PY
git init "$TARGET_REPO" >/dev/null
python3 "$REPO_ROOT/skills/specify-workflow-pack/scripts/install_workflow_pack.py" --repo "$TARGET_REPO" --config "$TARGET_REPO/workflow-pack.json"
echo "Project created at $TARGET_REPO"
