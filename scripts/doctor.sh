#!/usr/bin/env bash
set -euo pipefail
missing=0
for tool in git python3 node npm specify; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Missing: $tool"
    missing=1
  fi
done
if [ "$missing" -ne 0 ]; then
  exit 1
fi
echo "Machine doctor passed."
