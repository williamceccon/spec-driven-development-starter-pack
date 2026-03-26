#!/usr/bin/env python3
import argparse
import json
import shutil
from datetime import date
from pathlib import Path

DEFAULTS = {
    "pack_version": "1.0.0",
    "core_version": "1.0.0",
    "primary_product": "web-first product",
    "legacy_surface": "legacy runtime retained only for compatibility",
    "profile": "generic",
    "profile_version": "1.0.0",
    "profile_options": {},
    "addons": [],
    "supported_platforms": ["Windows", "macOS", "Linux"],
    "artifact_dir": "specs",
    "supported_workspaces": ["Codex", "Claude Code", "OpenCode", "GitHub Copilot", "Antigravity"],
    "coverage_threshold": 100,
    "backend_stack": [],
    "frontend_stack": [],
    "repository_map": [],
    "blocking_gates": [],
    "observational_gates": [],
    "frontend_validation": "",
    "required_skills": ["brainstorming", "gh-fix-ci", "gh-address-comments"],
    "recommended_skills": {},
    "bundled_skills": [],
    "brief_artifact": "BRIEF.md",
    "local_skills_dir": "skills",
    "legacy_commands": ["/feature", "/prd", "/spec", "/code", "/test", "/review", "/fix", "/snapshot"],
    "constitution_version": "2.0.0",
}

REPO_SKILL_MIRRORS = ["skills", ".claude/skills", ".opencode/skills", ".agents/skills"]

TEMPLATE_FILES = {
    "AGENTS.md": "AGENTS.md.tmpl",
    "CLAUDE.md": "AGENTS.md.tmpl",
    ".github/copilot-instructions.md": "copilot-instructions.md.tmpl",
    ".github/agents/brief.agent.md": "brief-copilot.agent.md.tmpl",
    ".github/agents/workflow.agent.md": "workflow-copilot.agent.md.tmpl",
    ".specify/memory/constitution.md": "constitution.md.tmpl",
    ".specify/templates/constitution-template.md": "constitution-template.md.tmpl",
    ".specify/templates/plan-template.md": "plan-template.md.tmpl",
    ".specify/templates/tasks-template.md": "tasks-template.md.tmpl",
    ".claude/commands/brief.md": "brief-claude.md.tmpl",
    ".claude/commands/workflow.md": "workflow-claude.md.tmpl",
    ".opencode/commands/brief.md": "brief-opencode.md.tmpl",
    ".opencode/commands/workflow.md": "workflow-opencode.md.tmpl",
    ".codex/prompts/brief.md": "brief-codex.md.tmpl",
    ".codex/prompts/workflow.md": "workflow-codex.md.tmpl",
}

LEGACY_COMMAND_TARGETS = {
    "/feature": ".opencode/commands/feature.md",
    "/prd": ".opencode/commands/prd.md",
    "/spec": ".opencode/commands/spec.md",
    "/code": ".opencode/commands/code.md",
    "/test": ".opencode/commands/test.md",
    "/review": ".opencode/commands/review.md",
    "/fix": ".opencode/commands/fix.md",
    "/snapshot": ".opencode/commands/snapshot.md",
}


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if "project_name" not in data or not str(data["project_name"]).strip():
        raise ValueError("workflow-pack.json must define a non-empty 'project_name'")
    merged = DEFAULTS | data
    merged["project_name"] = str(merged["project_name"]).strip()
    merged["brief_artifact"] = str(merged.get("brief_artifact") or "BRIEF.md").strip()
    merged["local_skills_dir"] = str(merged.get("local_skills_dir") or "skills").strip().strip("/\\")
    merged["profile"] = str(merged.get("profile") or "generic").strip()
    merged["profile_version"] = str(merged.get("profile_version") or "1.0.0").strip()
    merged["addons"] = [str(addon).strip() for addon in merged.get("addons", []) if str(addon).strip()]
    merged["supported_platforms"] = [
        str(platform).strip() for platform in merged.get("supported_platforms", []) if str(platform).strip()
    ]
    merged["supported_workspaces"] = [
        str(workspace).strip() for workspace in merged.get("supported_workspaces", []) if str(workspace).strip()
    ]
    merged["required_skills"] = [str(skill).strip() for skill in merged.get("required_skills", []) if str(skill).strip()]
    merged["bundled_skills"] = [str(skill).strip() for skill in merged.get("bundled_skills", []) if str(skill).strip()]
    merged["recommended_skills"] = {
        str(bundle).strip(): [str(skill).strip() for skill in skills if str(skill).strip()]
        for bundle, skills in (merged.get("recommended_skills") or {}).items()
        if str(bundle).strip()
    }
    if not merged["required_skills"]:
        raise ValueError("workflow-pack.json must define at least one required skill")
    merged["ratified_date"] = str(merged.get("ratified_date") or date.today().isoformat())
    merged["last_amended_date"] = date.today().isoformat()
    return merged


def bullet_lines(items, fallback):
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def numbered_gate_lines(items, fallback):
    if not items:
        return f"    - {fallback}"
    return "\n".join(f"    - `{item}`" for item in items)


def render(text: str, context: dict) -> str:
    rendered = text
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def build_context(config: dict) -> dict:
    frontend_validation_note = (
        f"- `{config['frontend_validation']}`"
        if config["frontend_validation"]
        else "- Record the frontend validation command used by this repo when frontend work is in scope"
    )
    return {
        "PROJECT_NAME": config["project_name"],
        "PACK_VERSION": config["pack_version"],
        "CORE_VERSION": config["core_version"],
        "PRIMARY_PRODUCT": config["primary_product"],
        "LEGACY_SURFACE": config["legacy_surface"],
        "PROFILE_NAME": config["profile"],
        "PROFILE_VERSION": config["profile_version"],
        "SUPPORTED_PLATFORMS": bullet_lines(config["supported_platforms"], "Windows"),
        "ARTIFACT_DIR": config["artifact_dir"],
        "SUPPORTED_WORKSPACES": bullet_lines(config["supported_workspaces"], "Codex"),
        "WORKSPACE_USAGE": bullet_lines(
            workspace_usage_notes(config["supported_workspaces"]),
            "Use the generated contract files in the workspace supported by your tool.",
        ),
        "BACKEND_STACK": bullet_lines(config["backend_stack"], "Define the backend stack for this repo in workflow-pack.json"),
        "FRONTEND_STACK": bullet_lines(config["frontend_stack"], "Define the frontend stack for this repo in workflow-pack.json or remove the section if not applicable"),
        "REPOSITORY_MAP": bullet_lines(config["repository_map"], "Fill in the concrete repository map for this project"),
        "BLOCKING_GATES": bullet_lines(config["blocking_gates"], "Define blocking gates in workflow-pack.json"),
        "OBSERVATIONAL_GATES": bullet_lines(config["observational_gates"], "Define observational gates in workflow-pack.json"),
        "BLOCKING_GATES_INDENTED": numbered_gate_lines(config["blocking_gates"], "Define blocking gates in workflow-pack.json"),
        "OBSERVATIONAL_GATES_INDENTED": numbered_gate_lines(config["observational_gates"], "Define observational gates in workflow-pack.json"),
        "FRONTEND_VALIDATION_NOTE": frontend_validation_note,
        "COVERAGE_THRESHOLD": str(config["coverage_threshold"]),
        "LEGACY_COMMANDS": bullet_lines(config["legacy_commands"], "/feature"),
        "CONSTITUTION_VERSION": config["constitution_version"],
        "RATIFIED_DATE": config["ratified_date"],
        "LAST_AMENDED_DATE": config["last_amended_date"],
        "BRIEF_ENTRYPOINT": "/brief",
        "WORKFLOW_ENTRYPOINT": "/workflow",
        "BRIEF_ARTIFACT": config["brief_artifact"],
        "LOCAL_SKILLS_DIR": config["local_skills_dir"],
        "REQUIRED_SKILLS": bullet_lines(config["required_skills"], "brainstorming"),
        "BUNDLED_SKILLS": bullet_lines([f"`{skill}`" for skill in config["bundled_skills"]], "Use only the required baseline skills"),
        "RECOMMENDED_SKILLS": bullet_lines(
            [
                f"`{bundle}`: {', '.join(skills)}"
                for bundle, skills in config["recommended_skills"].items()
            ],
            "Document recommended orchestration bundles in workflow-pack.json",
        ),
}


def workspace_usage_notes(workspaces: list[str]) -> list[str]:
    notes = []
    if "Codex" in workspaces:
        notes.append("`Codex`: use `.codex/prompts/brief.md` and `.codex/prompts/workflow.md`, with repo-local skills mirrored from `skills/`.")
    if "Claude Code" in workspaces:
        notes.append("`Claude Code`: use `/brief` and `/workflow` from `.claude/commands/`, with shared policy in `CLAUDE.md` and skills mirrored under `.claude/skills/`.")
    if "OpenCode" in workspaces:
        notes.append("`OpenCode`: use `/brief` and `/workflow` from `.opencode/commands/`, with repo-local skills mirrored under `.opencode/skills/`.")
    if "GitHub Copilot" in workspaces:
        notes.append("`GitHub Copilot`: use `.github/copilot-instructions.md` plus the custom agents in `.github/agents/brief.agent.md` and `.github/agents/workflow.agent.md`.")
    if "Antigravity" in workspaces:
        notes.append("`Antigravity`: use `AGENTS.md` plus the generic `.agents/skills/` mirror. This surface follows shared repo conventions and should be treated as compatibility support unless you verify newer vendor docs.")
    return notes


def write_file(target: Path, content: str, dry_run: bool):
    if dry_run:
        print(f"DRY RUN: would write {target}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"Wrote {target}")


def copy_required_skill(skill_dir: Path, target_dir: Path, dry_run: bool):
    if dry_run:
        print(f"DRY RUN: would copy skill {skill_dir.name} to {target_dir}")
        return
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(skill_dir, target_dir)
    print(f"Copied required skill {skill_dir.name} to {target_dir}")


def resolve_skill_source(skill_name: str, required_skills_dir: Path, bundled_skills_dir: Path) -> Path:
    required_path = required_skills_dir / skill_name
    if required_path.exists():
        return required_path

    bundled_path = bundled_skills_dir / skill_name
    if bundled_path.exists():
        return bundled_path

    raise FileNotFoundError(
        f"Skill bundle not found in required or bundled assets: {skill_name}"
    )


def repo_skill_targets(config: dict) -> list[str]:
    targets = [config["local_skills_dir"]]
    for mirror in REPO_SKILL_MIRRORS:
        if mirror not in targets:
            targets.append(mirror)
    return targets


def build_manifest(config: dict) -> dict:
    return {
        "project_name": config["project_name"],
        "pack_version": config["pack_version"],
        "core_version": config["core_version"],
        "profile": {
            "name": config["profile"],
            "version": config.get("profile_version", DEFAULTS["profile_version"]),
            "options": config.get("profile_options", {}),
        },
        "addons": list(config.get("addons", [])),
        "required_skills": list(config.get("required_skills", [])),
        "bundled_skills": list(config.get("bundled_skills", [])),
        "recommended_skills": dict(config.get("recommended_skills", {})),
        "supported_platforms": list(config.get("supported_platforms", DEFAULTS["supported_platforms"])),
        "supported_workspaces": list(config.get("supported_workspaces", DEFAULTS["supported_workspaces"])),
        "generated_surfaces": [
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
            "skills/",
            ".claude/skills/",
            ".opencode/skills/",
            ".agents/skills/",
            ".workflow-pack/manifest.json",
        ],
        "installed_at": date.today().isoformat(),
    }


def legacy_command_content(command: str) -> str:
    return (
        "---\n"
        "description: Deprecated legacy command. Use /brief and /workflow instead.\n"
        "agent: general\n"
        "subtask: false\n"
        "---\n\n"
        "This command is deprecated.\n\n"
        "The official project process is now `/brief` followed by `/workflow <slug>`, backed by the Specify-first artifact model in `specs/<feature-branch>/`.\n\n"
        f"When a user invokes {command}:\n\n"
        "1. Explain that `/brief` is the canonical starting point for a new feature\n"
        "2. Redirect to `/brief $ARGUMENTS` if the feature brief does not exist yet\n"
        "3. Redirect to `/workflow <slug>` if `BRIEF.md` already exists and the slug is known\n"
        "4. Only continue with the legacy flow if the user explicitly asks to recover a legacy session\n"
    )


def main():
    parser = argparse.ArgumentParser(description="Install or refresh a repo-local Specify workflow pack")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    config_path = Path(args.config).resolve()
    skill_dir = Path(__file__).resolve().parent.parent
    template_dir = skill_dir / "assets" / "templates"
    required_skills_dir = skill_dir / "assets" / "required-skills"
    bundled_skills_dir = skill_dir / "assets" / "bundled-skills"

    config = load_config(config_path)
    context = build_context(config)

    for relative_target, template_name in TEMPLATE_FILES.items():
        template_text = (template_dir / template_name).read_text(encoding="utf-8")
        target = repo / relative_target
        write_file(target, render(template_text, context), args.dry_run)

    for command in config["legacy_commands"]:
        target_rel = LEGACY_COMMAND_TARGETS.get(command)
        if target_rel:
            write_file(repo / target_rel, legacy_command_content(command), args.dry_run)

    copied_skills = set()
    for skill_name in config["required_skills"]:
        source_skill = resolve_skill_source(skill_name, required_skills_dir, bundled_skills_dir)
        for relative_target in repo_skill_targets(config):
            target_skill = repo / relative_target / skill_name
            copy_required_skill(source_skill, target_skill, args.dry_run)
        copied_skills.add(skill_name)

    for skill_name in config["bundled_skills"]:
        if skill_name in copied_skills:
            continue
        source_skill = resolve_skill_source(skill_name, required_skills_dir, bundled_skills_dir)
        for relative_target in repo_skill_targets(config):
            target_skill = repo / relative_target / skill_name
            copy_required_skill(source_skill, target_skill, args.dry_run)
        copied_skills.add(skill_name)

    manifest_target = repo / ".workflow-pack" / "manifest.json"
    write_file(manifest_target, json.dumps(build_manifest(config), indent=2) + "\n", args.dry_run)

    print("Dry run completed." if args.dry_run else "Workflow pack install completed.")


if __name__ == "__main__":
    main()
