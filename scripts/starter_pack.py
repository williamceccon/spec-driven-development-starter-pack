#!/usr/bin/env python3
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path


SUPPORTED_PLATFORMS = ["Windows", "macOS", "Linux"]
SUPPORTED_WORKSPACES = ["Codex", "Claude Code", "OpenCode", "GitHub Copilot", "Antigravity"]
PACK_VERSION = "1.0.0"
CORE_VERSION = "1.0.0"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render(text: str, context: dict[str, str]) -> str:
    rendered = text
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def unique(items):
    result = []
    seen = set()
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def profile_dir(starter_root: Path, profile_name: str) -> Path:
    path = starter_root / "profiles" / profile_name
    if not path.exists():
        raise FileNotFoundError(f"Unknown profile: {profile_name}")
    return path


def load_profile(starter_root: Path, profile_name: str) -> dict:
    data = read_json(profile_dir(starter_root, profile_name) / "profile.json")
    if data.get("status") != "ready":
        raise ValueError(f"Profile is not ready for generation: {profile_name}")
    data["slug"] = profile_name
    data.setdefault("primary_product", data.get("display_name", profile_name))
    data.setdefault("legacy_surface", "legacy runtime retained only for compatibility")
    data.setdefault("supported_workspaces", SUPPORTED_WORKSPACES)
    data.setdefault("backend_stack", [])
    data.setdefault("frontend_stack", [])
    data.setdefault("repository_map", [])
    data.setdefault("blocking_gates", [])
    data.setdefault("observational_gates", [])
    data.setdefault("required_skills", ["brainstorming", "gh-fix-ci", "gh-address-comments"])
    data.setdefault("recommended_skills", {})
    data.setdefault("bundled_skills", data["required_skills"])
    data.setdefault("install_commands", ["Review the generated README and install project dependencies"])
    data.setdefault("dev_commands", ["Add a development command for this profile"])
    data.setdefault("test_commands", ["Add a validation command for this profile"])
    data.setdefault("env", [])
    data.setdefault("github_notes", [])
    return data


def list_profiles(starter_root: Path, include_planned: bool = False) -> list[dict]:
    profiles = []
    for config_path in sorted((starter_root / "profiles").glob("*/profile.json")):
        data = read_json(config_path)
        data["slug"] = config_path.parent.name
        if not include_planned and data.get("status") != "ready":
            continue
        profiles.append(data)
    return profiles


def addon_paths(starter_root: Path):
    return starter_root.glob("addons/*/*/addon.json")


def load_addon(starter_root: Path, addon_name: str) -> dict:
    for addon_path in addon_paths(starter_root):
        if addon_path.parent.name != addon_name:
            continue
        data = read_json(addon_path)
        data["slug"] = addon_name
        data.setdefault("env", [])
        data.setdefault("recommended_skills", {})
        data.setdefault("bundled_skills", [])
        data.setdefault("blocking_gates", [])
        data.setdefault("observational_gates", [])
        data.setdefault("readme_notes", [])
        data.setdefault("ci_services", [])
        return data
    raise FileNotFoundError(f"Unknown add-on: {addon_name}")


def list_addons(starter_root: Path) -> list[dict]:
    addons = []
    for addon_path in sorted(addon_paths(starter_root)):
        data = read_json(addon_path)
        data["slug"] = addon_path.parent.name
        addons.append(data)
    return addons


def merge_skill_bundles(profile: dict, addons: list[dict]) -> dict:
    merged = {bundle: list(skills) for bundle, skills in profile.get("recommended_skills", {}).items()}
    for addon in addons:
        for bundle, skills in addon.get("recommended_skills", {}).items():
            merged[bundle] = unique(merged.get(bundle, []) + list(skills))
    return merged


def merge_bundled_skills(profile: dict, addons: list[dict]) -> list[str]:
    bundled = list(profile.get("bundled_skills", []))
    for addon in addons:
        bundled.extend(addon.get("bundled_skills", []))
    return unique(bundled)


def merge_env(profile: dict, addons: list[dict]) -> list[dict]:
    env_entries = list(profile.get("env", []))
    env_names = {entry["name"] for entry in env_entries}
    for addon in addons:
        for entry in addon.get("env", []):
            if entry["name"] in env_names:
                continue
            env_entries.append(entry)
            env_names.add(entry["name"])
    return env_entries


def merge_workflow_config(project_name: str, profile: dict, addons: list[dict]) -> dict:
    recommended_skills = merge_skill_bundles(profile, addons)
    bundled_skills = merge_bundled_skills(profile, addons)
    return {
        "project_name": project_name,
        "pack_version": PACK_VERSION,
        "core_version": CORE_VERSION,
        "profile": profile["slug"],
        "profile_version": profile["profile_version"],
        "profile_options": {},
        "addons": [addon["slug"] for addon in addons],
        "supported_platforms": SUPPORTED_PLATFORMS,
        "primary_product": profile["primary_product"],
        "legacy_surface": profile["legacy_surface"],
        "artifact_dir": "specs",
        "supported_workspaces": profile["supported_workspaces"],
        "coverage_threshold": 100,
        "backend_stack": profile["backend_stack"],
        "frontend_stack": profile["frontend_stack"],
        "repository_map": profile["repository_map"],
        "blocking_gates": unique(
            list(profile["blocking_gates"])
            + [gate for addon in addons for gate in addon.get("blocking_gates", [])]
        ),
        "observational_gates": unique(
            list(profile["observational_gates"])
            + [gate for addon in addons for gate in addon.get("observational_gates", [])]
        ),
        "frontend_validation": "",
        "required_skills": profile["required_skills"],
        "recommended_skills": recommended_skills,
        "bundled_skills": bundled_skills,
        "brief_artifact": "BRIEF.md",
        "local_skills_dir": "skills",
        "constitution_version": "2.0.0",
    }


def markdown_list(items: list[str], empty_fallback: str) -> str:
    if not items:
        return f"- {empty_fallback}"
    return "\n".join(f"- {item}" for item in items)


def inline_code_list(items: list[str], empty_fallback: str) -> str:
    if not items:
        return empty_fallback
    return ", ".join(f"`{item}`" for item in items)


def numbered_commands(commands: list[str]) -> str:
    return "\n".join(f"{index}. `{command}`" for index, command in enumerate(commands, start=1))


def environment_section(env_entries: list[dict]) -> str:
    if not env_entries:
        return "- No environment variables are required by default."
    lines = []
    for entry in env_entries:
        lines.append(f"- `{entry['name']}`: `{entry['value']}`")
        lines.append(f"  {entry['description']}")
    return "\n".join(lines)


def addon_details(addons: list[dict]) -> str:
    if not addons:
        return "- No optional add-ons were selected."
    lines = []
    for addon in addons:
        lines.append(f"- `{addon['slug']}`: {addon['description']}")
        for note in addon.get("readme_notes", []):
            lines.append(f"  {note}")
    return "\n".join(lines)


def github_notes(profile: dict) -> str:
    notes = list(profile.get("github_notes", []))
    notes.append("Commit early, then push after the first passing local validation run.")
    return markdown_list(notes, "Create a GitHub repository before you invite collaborators.")


def first_thirty_minutes(profile: dict, addons: list[dict]) -> str:
    steps = [
        "Clone or create the project directory generated from this starter.",
        "Read `workflow-pack.json` and `.workflow-pack/manifest.json` to understand the selected profile and add-ons.",
        "Copy `.env.example` to `.env` and adjust values for your machine.",
        "Run the install commands below and then run the validation command once.",
        "Start your first scoped feature with `/brief` instead of jumping into code."
    ]
    if addons:
        steps.append("If you chose database add-ons, start the local services you need before wiring real application code.")
    return numbered_commands(steps)


def push_to_github_steps() -> str:
    return numbered_commands(
        [
            "Create an empty repository on GitHub.",
            "Run `git init` if the repo is not initialized yet.",
            "Run `git add .` and `git commit -m \"chore: bootstrap project\"`.",
            "Run `git branch -M main`.",
            "Run `git remote add origin <your-github-url>`.",
            "Run `git push -u origin main`."
        ]
    )


def workspace_usage_notes(workspaces: list[str]) -> str:
    notes = []
    if "Codex" in workspaces:
        notes.append("- `Codex`: use `.codex/prompts/brief.md` and `.codex/prompts/workflow.md`.")
    if "Claude Code" in workspaces:
        notes.append("- `Claude Code`: use `/brief` and `/workflow` from `.claude/commands/`, with shared policy in `CLAUDE.md`.")
    if "OpenCode" in workspaces:
        notes.append("- `OpenCode`: use `/brief` and `/workflow` from `.opencode/commands/`.")
    if "GitHub Copilot" in workspaces:
        notes.append("- `GitHub Copilot`: use `.github/copilot-instructions.md` and the custom agents in `.github/agents/`.")
    if "Antigravity" in workspaces:
        notes.append("- `Antigravity`: use `AGENTS.md` and `.agents/skills/` as the compatibility surface.")
    if not notes:
        notes.append("- Use the generated repo contract files with the workspace supported by your tool.")
    return "\n".join(notes)


def build_context(project_name: str, profile: dict, addons: list[dict], workflow_config: dict) -> dict[str, str]:
    return {
        "PROJECT_NAME": project_name,
        "PROFILE_NAME": profile["slug"],
        "PROFILE_VERSION": profile["profile_version"],
        "PROFILE_DESCRIPTION": profile["description"],
        "ADDON_LIST": ", ".join(f"`{addon['slug']}`" for addon in addons) if addons else "none",
        "SUPPORTED_PLATFORMS": ", ".join(SUPPORTED_PLATFORMS),
        "SUPPORTED_WORKSPACES": ", ".join(workflow_config["supported_workspaces"]),
        "WORKSPACE_USAGE": workspace_usage_notes(workflow_config["supported_workspaces"]),
        "INSTALL_COMMANDS": numbered_commands(profile["install_commands"]),
        "DEV_COMMANDS": numbered_commands(profile["dev_commands"]),
        "TEST_COMMANDS": numbered_commands(profile["test_commands"]),
        "ENVIRONMENT_VARIABLES": environment_section(merge_env(profile, addons)),
        "FIRST_30_MINUTES": first_thirty_minutes(profile, addons),
        "GITHUB_NOTES": github_notes(profile),
        "PUSH_TO_GITHUB": push_to_github_steps(),
        "ADDON_DETAILS": addon_details(addons),
        "BUNDLED_SKILLS": markdown_list(
            [f"`{skill}`" for skill in workflow_config["bundled_skills"]],
            "No repo-local skills were bundled for this profile."
        ),
        "BUNDLED_SKILLS_INLINE": inline_code_list(
            workflow_config["bundled_skills"],
            "none"
        ),
        "CI_SERVICES": build_ci_services(addons),
    }


def build_ci_services(addons: list[dict]) -> str:
    ci_lines = []
    for addon in addons:
        ci_lines.extend(addon.get("ci_services", []))
    if not ci_lines:
        return ""
    return "\n".join(ci_lines)


def render_profile_template(starter_root: Path, profile_name: str, target_path: Path, context: dict[str, str]) -> None:
    template_root = profile_dir(starter_root, profile_name) / "template"
    if not template_root.exists():
        return
    for source_path in template_root.rglob("*"):
        if source_path.is_dir():
            continue
        relative_path = source_path.relative_to(template_root)
        target_relative = relative_path.with_name(relative_path.name.removesuffix(".tmpl"))
        target_file = target_path / target_relative
        target_file.parent.mkdir(parents=True, exist_ok=True)
        text = source_path.read_text(encoding="utf-8")
        if source_path.suffix == ".tmpl":
            target_file.write_text(render(text, context), encoding="utf-8")
        else:
            target_file.write_text(render(text, context), encoding="utf-8")


def write_env_example(target_path: Path, env_entries: list[dict]) -> None:
    if not env_entries:
        content = "# No environment variables are required by default.\n"
    else:
        lines = ["# Copy this file to .env and adjust values for your machine."]
        for entry in env_entries:
            lines.append(f"# {entry['description']}")
            lines.append(f"{entry['name']}={entry['value']}")
            lines.append("")
        content = "\n".join(lines).rstrip() + "\n"
    (target_path / ".env.example").write_text(content, encoding="utf-8")


def write_generated_readme(starter_root: Path, target_path: Path, context: dict[str, str]) -> None:
    template_path = starter_root / "core" / "templates" / "generated-README.md.tmpl"
    template_text = template_path.read_text(encoding="utf-8")
    (target_path / "README.md").write_text(render(template_text, context), encoding="utf-8")


def load_installer_module(starter_root: Path):
    module_path = starter_root / "skills" / "specify-workflow-pack" / "scripts" / "install_workflow_pack.py"
    spec = importlib.util.spec_from_file_location("install_workflow_pack", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def install_workflow_pack(starter_root: Path, target_path: Path) -> None:
    module = load_installer_module(starter_root)
    config = module.load_config(target_path / "workflow-pack.json")
    skill_dir = starter_root / "skills" / "specify-workflow-pack"
    template_dir = skill_dir / "assets" / "templates"
    required_skills_dir = skill_dir / "assets" / "required-skills"
    bundled_skills_dir = skill_dir / "assets" / "bundled-skills"
    context = module.build_context(config)

    for relative_target, template_name in module.TEMPLATE_FILES.items():
        template_text = (template_dir / template_name).read_text(encoding="utf-8")
        module.write_file(target_path / relative_target, module.render(template_text, context), dry_run=False)

    for command in config["legacy_commands"]:
        target_rel = module.LEGACY_COMMAND_TARGETS.get(command)
        if target_rel:
            module.write_file(target_path / target_rel, module.legacy_command_content(command), dry_run=False)

    copied_skills = set()
    for skill_name in config["required_skills"]:
        source_skill = module.resolve_skill_source(skill_name, required_skills_dir, bundled_skills_dir)
        for relative_target in module.repo_skill_targets(config):
            target_skill = target_path / relative_target / skill_name
            module.copy_required_skill(source_skill, target_skill, dry_run=False)
        copied_skills.add(skill_name)

    for skill_name in config.get("bundled_skills", []):
        if skill_name in copied_skills:
            continue
        source_skill = module.resolve_skill_source(skill_name, required_skills_dir, bundled_skills_dir)
        for relative_target in module.repo_skill_targets(config):
            target_skill = target_path / relative_target / skill_name
            module.copy_required_skill(source_skill, target_skill, dry_run=False)
        copied_skills.add(skill_name)

    module.write_file(
        target_path / ".workflow-pack" / "manifest.json",
        json.dumps(module.build_manifest(config), indent=2) + "\n",
        dry_run=False,
    )


def create_project(
    starter_root: Path,
    project_name: str,
    target_root: Path,
    profile_name: str,
    addon_names: list[str] | None = None,
    initialize_git: bool = True,
    include_github_ci: bool = True,
) -> Path:
    starter_root = starter_root.resolve()
    target_root = target_root.resolve()
    addon_names = addon_names or []
    profile = load_profile(starter_root, profile_name)
    addons = [load_addon(starter_root, addon_name) for addon_name in addon_names]
    project_path = target_root / project_name
    if project_path.exists():
        raise FileExistsError(f"Target repo already exists: {project_path}")

    project_path.mkdir(parents=True)
    workflow_config = merge_workflow_config(project_name, profile, addons)
    context = build_context(project_name, profile, addons, workflow_config)

    render_profile_template(starter_root, profile_name, project_path, context)
    write_env_example(project_path, merge_env(profile, addons))
    write_generated_readme(starter_root, project_path, context)
    (project_path / "workflow-pack.json").write_text(json.dumps(workflow_config, indent=2) + "\n", encoding="utf-8")
    install_workflow_pack(starter_root, project_path)
    if not include_github_ci:
        workflow_path = project_path / ".github" / "workflows" / "ci.yml"
        if workflow_path.exists():
            workflow_path.unlink()

    if initialize_git:
        subprocess.run(["git", "init", str(project_path)], check=True, stdout=subprocess.DEVNULL)

    return project_path


__all__ = [
    "create_project",
    "list_addons",
    "list_profiles",
    "load_addon",
    "load_profile",
    "merge_workflow_config",
]
