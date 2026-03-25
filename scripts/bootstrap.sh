#!/usr/bin/env bash
set -euo pipefail

echo "Checking macOS/Linux machine prerequisites for the public starter pack..."
for tool in git python3 gh specify; do
  if command -v "$tool" >/dev/null 2>&1; then
    echo "Found $tool"
  else
    echo "WARN: $tool not found on PATH"
  fi
done

if command -v brew >/dev/null 2>&1; then
  echo "Homebrew available"
else
  echo "WARN: Homebrew not found; install tools manually if missing."
fi

echo "Recommended installs if missing:"
echo "  brew install git python@3.12 gh"
echo "  uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"
echo "  bash ./scripts/install-workflow-pack.sh"
echo "  bash ./scripts/new-project.sh --list-profiles"
