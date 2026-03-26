#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

REQUIRED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    ".github/copilot-instructions.md",
    ".github/agents/brief.agent.md",
    ".github/agents/workflow.agent.md",
    ".specify/memory/constitution.md",
    ".specify/templates/constitution-template.md",
    ".specify/templates/plan-template.md",
    ".specify/templates/tasks-template.md",
    ".claude/commands/brief.md",
    ".claude/commands/workflow.md",
    ".opencode/commands/brief.md",
    ".opencode/commands/workflow.md",
    ".codex/prompts/brief.md",
    ".codex/prompts/workflow.md",
    ".workflow-pack/manifest.json",
]

DEFAULT_REQUIRED_SKILLS = ["brainstorming", "gh-fix-ci", "gh-address-comments"]
DEFAULT_SUPPORTED_WORKSPACES = ["Codex", "Claude Code", "OpenCode", "GitHub Copilot", "Antigravity"]
TOOLS = ["git", "python", "specify", "gh"]
REPO_SKILL_SURFACES = ["skills", ".claude/skills", ".opencode/skills", ".agents/skills"]


def load_config(config_path: Path) -> dict:
    data = json.loads(config_path.read_text(encoding="utf-8-sig"))
    project_name = str(data.get("project_name", "")).strip()
    if not project_name:
        raise ValueError("workflow-pack.json must define 'project_name'")
    return {
        "project_name": project_name,
        "profile": str(data.get("profile") or "generic").strip(),
        "addons": [str(addon).strip() for addon in data.get("addons", []) if str(addon).strip()],
        "supported_workspaces": [
            str(workspace).strip()
            for workspace in data.get("supported_workspaces", DEFAULT_SUPPORTED_WORKSPACES)
            if str(workspace).strip()
        ],
        "bundled_skills": [str(skill).strip() for skill in data.get("bundled_skills", []) if str(skill).strip()],
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

    validate_instruction_surface(repo / "AGENTS.md", "AGENTS.md", config, failures)
    validate_instruction_surface(repo / "CLAUDE.md", "CLAUDE.md", config, failures)

    brief_text = (repo / ".opencode/commands/brief.md").read_text(encoding="utf-8") if (repo / ".opencode/commands/brief.md").exists() else ""
    workflow_text = (repo / ".opencode/commands/workflow.md").read_text(encoding="utf-8") if (repo / ".opencode/commands/workflow.md").exists() else ""
    if config["brief_artifact"] not in brief_text:
        failures.append("OpenCode /brief command does not appear to mention the configured brief artifact")
    if config["brief_artifact"] not in workflow_text or "slug" not in workflow_text.lower():
        failures.append("OpenCode /workflow command does not appear to enforce brief + slug validation")

    claude_brief_text = (repo / ".claude/commands/brief.md").read_text(encoding="utf-8") if (repo / ".claude/commands/brief.md").exists() else ""
    claude_workflow_text = (repo / ".claude/commands/workflow.md").read_text(encoding="utf-8") if (repo / ".claude/commands/workflow.md").exists() else ""
    if config["brief_artifact"] not in claude_brief_text:
        failures.append("Claude Code /brief command does not appear to mention the configured brief artifact")
    if config["brief_artifact"] not in claude_workflow_text or "slug" not in claude_workflow_text.lower():
        failures.append("Claude Code /workflow command does not appear to enforce brief + slug validation")

    copilot_text = (repo / ".github" / "copilot-instructions.md").read_text(encoding="utf-8") if (repo / ".github" / "copilot-instructions.md").exists() else ""
    if config["profile"] not in copilot_text:
        failures.append(".github/copilot-instructions.md does not appear to mention the selected profile")
    if config["brief_artifact"] not in copilot_text:
        failures.append(".github/copilot-instructions.md does not appear to mention the configured brief artifact")
    copilot_brief_agent = (repo / ".github" / "agents" / "brief.agent.md").read_text(encoding="utf-8") if (repo / ".github" / "agents" / "brief.agent.md").exists() else ""
    copilot_workflow_agent = (repo / ".github" / "agents" / "workflow.agent.md").read_text(encoding="utf-8") if (repo / ".github" / "agents" / "workflow.agent.md").exists() else ""
    if config["brief_artifact"] not in copilot_brief_agent:
        failures.append(".github/agents/brief.agent.md does not appear to mention the configured brief artifact")
    if config["brief_artifact"] not in copilot_workflow_agent or "slug" not in copilot_workflow_agent.lower():
        failures.append(".github/agents/workflow.agent.md does not appear to enforce brief + slug validation")

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
            if manifest.get("bundled_skills", []) != config.get("bundled_skills", []):
                failures.append("Workflow manifest bundled skills do not match workflow-pack.json")
            if manifest.get("supported_workspaces", []) != config.get("supported_workspaces", []):
                failures.append("Workflow manifest supported workspaces do not match workflow-pack.json")
    if check_tools:
        for tool in TOOLS:
            if shutil.which(tool) is None:
                failures.append(f"Required tool not found on PATH: {tool}")

    for skill_name in config["required_skills"]:
        global_skill = global_skill_path(skill_name)
        local_skills = [repo / surface / skill_name / "SKILL.md" for surface in repo_skill_surfaces(config)]
        if not global_skill.exists() and not any(path.exists() for path in local_skills):
            failures.append(f"Required skill not available globally or locally: {skill_name}")

    for skill_name in config.get("bundled_skills", []):
        for surface in repo_skill_surfaces(config):
            local_skill = repo / surface / skill_name / "SKILL.md"
            if not local_skill.exists():
                failures.append(f"Bundled skill not available locally at {surface}: {skill_name}")

    return failures


def repo_skill_surfaces(config: dict) -> list[str]:
    surfaces = [config["local_skills_dir"]]
    for surface in REPO_SKILL_SURFACES:
        if surface not in surfaces:
            surfaces.append(surface)
    return surfaces


def validate_instruction_surface(path: Path, label: str, config: dict, failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if config["project_name"] not in text:
        failures.append(f"{label} does not appear to reference the configured project name")
    for expected in ["/brief", "/workflow", config["brief_artifact"]]:
        if expected not in text:
            failures.append(f"{label} does not appear to mention {expected}")
    if config["profile"] not in text:
        failures.append(f"{label} does not appear to mention the selected profile")


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
