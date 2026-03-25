#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

REQUIRED_FILES = [
    "AGENTS.md",
    ".specify/memory/constitution.md",
    ".specify/templates/constitution-template.md",
    ".specify/templates/plan-template.md",
    ".specify/templates/tasks-template.md",
    ".opencode/commands/brief.md",
    ".opencode/commands/workflow.md",
    ".codex/prompts/brief.md",
    ".codex/prompts/workflow.md",
    ".workflow-pack/manifest.json",
]

DEFAULT_REQUIRED_SKILLS = ["brainstorming", "gh-fix-ci", "gh-address-comments"]
TOOLS = ["git", "python", "specify", "gh"]


def load_config(config_path: Path) -> dict:
    data = json.loads(config_path.read_text(encoding="utf-8-sig"))
    project_name = str(data.get("project_name", "")).strip()
    if not project_name:
        raise ValueError("workflow-pack.json must define 'project_name'")
    return {
        "project_name": project_name,
        "profile": str(data.get("profile") or "generic").strip(),
        "addons": [str(addon).strip() for addon in data.get("addons", []) if str(addon).strip()],
        "brief_artifact": str(data.get("brief_artifact") or "BRIEF.md").strip(),
        "local_skills_dir": str(data.get("local_skills_dir") or "skills").strip().strip("/\\"),
        "required_skills": [str(skill).strip() for skill in data.get("required_skills", DEFAULT_REQUIRED_SKILLS) if str(skill).strip()],
        "recommended_skills": {
            str(bundle).strip(): [str(skill).strip() for skill in skills if str(skill).strip()]
            for bundle, skills in (data.get("recommended_skills") or {}).items()
            if str(bundle).strip()
        },
    }


def global_skill_path(skill_name: str) -> Path:
    code_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    return code_home / "skills" / skill_name / "SKILL.md"


def validate_repo(repo: Path, config: dict, check_tools: bool = True) -> list[str]:
    failures = []

    for rel in REQUIRED_FILES:
        if not (repo / rel).exists():
            failures.append(f"Missing required file: {rel}")

    agents_path = repo / "AGENTS.md"
    agents_text = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    if config["project_name"] not in agents_text:
        failures.append("AGENTS.md does not appear to reference the configured project name")
    for expected in ["/brief", "/workflow", config["brief_artifact"]]:
        if expected not in agents_text:
            failures.append(f"AGENTS.md does not appear to mention {expected}")
    if config["profile"] not in agents_text:
        failures.append("AGENTS.md does not appear to mention the selected profile")

    brief_text = (repo / ".opencode/commands/brief.md").read_text(encoding="utf-8") if (repo / ".opencode/commands/brief.md").exists() else ""
    workflow_text = (repo / ".opencode/commands/workflow.md").read_text(encoding="utf-8") if (repo / ".opencode/commands/workflow.md").exists() else ""
    if config["brief_artifact"] not in brief_text:
        failures.append("OpenCode /brief command does not appear to mention the configured brief artifact")
    if config["brief_artifact"] not in workflow_text or "slug" not in workflow_text.lower():
        failures.append("OpenCode /workflow command does not appear to enforce brief + slug validation")

    manifest_path = repo / ".workflow-pack" / "manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            failures.append("Workflow manifest is not valid JSON")
        else:
            if manifest.get("profile", {}).get("name") != config["profile"]:
                failures.append("Workflow manifest profile does not match workflow-pack.json")
            if manifest.get("addons", []) != config["addons"]:
                failures.append("Workflow manifest add-ons do not match workflow-pack.json")
    if check_tools:
        for tool in TOOLS:
            if shutil.which(tool) is None:
                failures.append(f"Required tool not found on PATH: {tool}")

    local_skills_dir = repo / config["local_skills_dir"]
    for skill_name in config["required_skills"]:
        global_skill = global_skill_path(skill_name)
        local_skill = local_skills_dir / skill_name / "SKILL.md"
        if not global_skill.exists() and not local_skill.exists():
            failures.append(f"Required skill not available globally or locally: {skill_name}")

    return failures


def main():
    parser = argparse.ArgumentParser(description="Validate a repo-local workflow pack installation")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    config = load_config(Path(args.config).resolve())
    failures = validate_repo(repo, config)

    if failures:
        print("Workflow pack validation failed:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    print("Workflow pack validation passed.")


if __name__ == "__main__":
    main()
