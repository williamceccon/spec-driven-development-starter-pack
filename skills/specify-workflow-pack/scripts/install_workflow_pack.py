#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

DEFAULTS = {
    "primary_product": "web-first product",
    "legacy_surface": "legacy runtime retained only for compatibility",
    "artifact_dir": "specs",
    "supported_workspaces": ["Codex", "OpenCode", "GitHub Copilot", "Antigravity"],
    "coverage_threshold": 100,
    "backend_stack": [],
    "frontend_stack": [],
    "repository_map": [],
    "blocking_gates": [],
    "observational_gates": [],
    "frontend_validation": "",
    "legacy_commands": ["/feature", "/prd", "/spec", "/code", "/test", "/review", "/fix", "/snapshot"],
    "constitution_version": "1.0.0",
}

TEMPLATE_FILES = {
    "AGENTS.md.tmpl": "AGENTS.md",
    "constitution.md.tmpl": ".specify/memory/constitution.md",
    "constitution-template.md.tmpl": ".specify/templates/constitution-template.md",
    "plan-template.md.tmpl": ".specify/templates/plan-template.md",
    "tasks-template.md.tmpl": ".specify/templates/tasks-template.md",
    "workflow-opencode.md.tmpl": ".opencode/commands/workflow.md",
    "workflow-codex.md.tmpl": ".codex/prompts/workflow.md",
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
    artifact_dir = config["artifact_dir"]
    legacy_commands = config["legacy_commands"]
    frontend_validation_note = (
        f"- `{config['frontend_validation']}`" if config["frontend_validation"] else "- Record the frontend validation command used by this repo when frontend work is in scope"
    )
    return {
        "PROJECT_NAME": config["project_name"],
        "PRIMARY_PRODUCT": config["primary_product"],
        "LEGACY_SURFACE": config["legacy_surface"],
        "ARTIFACT_DIR": artifact_dir,
        "SUPPORTED_WORKSPACES": bullet_lines(config["supported_workspaces"], "Codex"),
        "BACKEND_STACK": bullet_lines(config["backend_stack"], "Define the backend stack for this repo in workflow-pack.json"),
        "FRONTEND_STACK": bullet_lines(config["frontend_stack"], "Define the frontend stack for this repo in workflow-pack.json or remove the section if not applicable"),
        "REPOSITORY_MAP": bullet_lines(config["repository_map"], "Fill in the concrete repository map for this project"),
        "BLOCKING_GATES": bullet_lines(config["blocking_gates"], "Define blocking gates in workflow-pack.json"),
        "OBSERVATIONAL_GATES": bullet_lines(config["observational_gates"], "Define observational gates in workflow-pack.json"),
        "BLOCKING_GATES_INDENTED": numbered_gate_lines(config["blocking_gates"], "Define blocking gates in workflow-pack.json"),
        "OBSERVATIONAL_GATES_INDENTED": numbered_gate_lines(config["observational_gates"], "Define observational gates in workflow-pack.json"),
        "FRONTEND_VALIDATION_NOTE": frontend_validation_note,
        "COVERAGE_THRESHOLD": str(config["coverage_threshold"]),
        "LEGACY_COMMANDS": bullet_lines(legacy_commands, "/feature"),
        "CONSTITUTION_VERSION": config["constitution_version"],
        "RATIFIED_DATE": config["ratified_date"],
        "LAST_AMENDED_DATE": config["last_amended_date"],
        "WORKFLOW_ENTRYPOINT": "/workflow",
    }


def write_file(target: Path, content: str, dry_run: bool):
    if dry_run:
        print(f"DRY RUN: would write {target}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"Wrote {target}")


def legacy_command_content(command: str) -> str:
    return f"---\ndescription: Deprecated legacy command. Use /workflow instead.\nagent: general\nsubtask: false\n---\n\nThis command is deprecated.\n\nThe official project process is now `/workflow`, backed by the Specify-first artifact model in `specs/<feature-branch>/`.\n\nWhen a user invokes `{command}`:\n\n1. Explain that `/workflow` is the canonical autonomous flow\n2. Redirect to `/workflow $ARGUMENTS`\n3. Only continue with the legacy flow if the user explicitly asks to recover a legacy session\n"


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

    config = load_config(config_path)
    context = build_context(config)

    for template_name, relative_target in TEMPLATE_FILES.items():
        template_text = (template_dir / template_name).read_text(encoding="utf-8")
        target = repo / relative_target
        write_file(target, render(template_text, context), args.dry_run)

    for command in config["legacy_commands"]:
        target_rel = LEGACY_COMMAND_TARGETS.get(command)
        if not target_rel:
            continue
        write_file(repo / target_rel, legacy_command_content(command), args.dry_run)

    if args.dry_run:
        print("Dry run completed.")
    else:
        print("Workflow pack install completed.")


if __name__ == "__main__":
    main()

