#!/usr/bin/env python3
import argparse
import json
import shutil
import sys
from pathlib import Path

REQUIRED_FILES = [
    "AGENTS.md",
    ".specify/memory/constitution.md",
    ".specify/templates/constitution-template.md",
    ".specify/templates/plan-template.md",
    ".specify/templates/tasks-template.md",
    ".opencode/commands/workflow.md",
    ".codex/prompts/workflow.md",
]

TOOLS = ["git", "python", "specify"]


def load_project_name(config_path: Path) -> str:
    data = json.loads(config_path.read_text(encoding="utf-8-sig"))
    name = str(data.get("project_name", "")).strip()
    if not name:
        raise ValueError("workflow-pack.json must define 'project_name'")
    return name


def main():
    parser = argparse.ArgumentParser(description="Validate a repo-local workflow pack installation")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    config = Path(args.config).resolve()
    project_name = load_project_name(config)

    failures = []

    for rel in REQUIRED_FILES:
        if not (repo / rel).exists():
            failures.append(f"Missing required file: {rel}")

    agents_text = (repo / "AGENTS.md").read_text(encoding="utf-8") if (repo / "AGENTS.md").exists() else ""
    if project_name not in agents_text:
        failures.append("AGENTS.md does not appear to reference the configured project name")

    for tool in TOOLS:
        if shutil.which(tool) is None:
            failures.append(f"Required tool not found on PATH: {tool}")

    if failures:
        print("Workflow pack validation failed:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    print("Workflow pack validation passed.")


if __name__ == "__main__":
    main()

