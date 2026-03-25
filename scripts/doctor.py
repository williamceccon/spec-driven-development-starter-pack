#!/usr/bin/env python3
import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

from starter_pack import list_addons, load_profile


BASE_TOOLS = ["git", "python", "gh", "specify"]


def load_doctor_module(starter_root: Path):
    module_path = starter_root / "skills" / "specify-workflow-pack" / "scripts" / "doctor_workflow_pack.py"
    spec = importlib.util.spec_from_file_location("doctor_workflow_pack", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_addons(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def tool_failures(profile_tools: list[str]) -> list[str]:
    failures = []
    for tool in profile_tools:
        if tool == "python" and sys.executable:
            continue
        if shutil.which(tool) is None:
            failures.append(f"Missing tool: {tool}")
    return failures


def gh_auth_warning() -> str | None:
    if shutil.which("gh") is None:
        return None
    result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, check=False)
    if result.returncode == 0:
        return None
    return "GitHub CLI is installed but not authenticated. Run `gh auth login` before pushing or using PR automation."


def env_warning(repo: Path) -> str | None:
    if (repo / ".env.example").exists() and not (repo / ".env").exists():
        return "`.env.example` exists but `.env` does not. Copy it before running the project locally."
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Check whether the machine and generated repo are ready for the starter pack workflow")
    parser.add_argument("--profile", default="")
    parser.add_argument("--addons", default="")
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()

    starter_root = Path(__file__).resolve().parent.parent
    repo = Path(args.repo).resolve()
    profile_name = args.profile
    addon_names = parse_addons(args.addons)
    warnings = []

    if not profile_name and (repo / "workflow-pack.json").exists():
        config = json.loads((repo / "workflow-pack.json").read_text(encoding="utf-8"))
        profile_name = config.get("profile", "")
        addon_names = config.get("addons", addon_names)

    profile_tools = list(BASE_TOOLS)
    if profile_name:
        profile = load_profile(starter_root, profile_name)
        profile_tools = list(dict.fromkeys(BASE_TOOLS + profile.get("tool_checks", [])))

    failures = tool_failures(profile_tools)
    auth_warning = gh_auth_warning()
    if auth_warning:
        warnings.append(auth_warning)
    env_state_warning = env_warning(repo)
    if env_state_warning:
        warnings.append(env_state_warning)

    doctor_module = load_doctor_module(starter_root)
    if (repo / "workflow-pack.json").exists():
        config = doctor_module.load_config(repo / "workflow-pack.json")
        failures.extend(doctor_module.validate_repo(repo, config, check_tools=False))

    available_addons = {addon["slug"] for addon in list_addons(starter_root)}
    for addon_name in addon_names:
        if addon_name not in available_addons:
            failures.append(f"Unknown add-on requested: {addon_name}")

    if failures:
        print("Doctor found blocking issues:")
        for failure in failures:
            print(f"- {failure}")
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"- {warning}")
        sys.exit(1)

    print("Doctor checks passed.")
    if profile_name:
        print(f"Profile: {profile_name}")
    if addon_names:
        print(f"Add-ons: {', '.join(addon_names)}")
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")


if __name__ == "__main__":
    main()
