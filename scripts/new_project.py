#!/usr/bin/env python3
import argparse
from pathlib import Path

from starter_pack import create_project, list_addons, list_profiles


def prompt(message: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{message}{suffix}: ").strip()
    return value or (default or "")


def prompt_yes_no(message: str, default: bool = True) -> bool:
    default_label = "Y/n" if default else "y/N"
    value = input(f"{message} [{default_label}]: ").strip().lower()
    if not value:
        return default
    return value in {"y", "yes"}


def choose_profile(starter_root: Path) -> str:
    profiles = list_profiles(starter_root)
    print("Available starter profiles:")
    for index, profile in enumerate(profiles, start=1):
        print(f"  {index}. {profile['slug']} - {profile['display_name']}")
    selection = prompt("Choose a profile number", "1")
    selected_index = max(1, min(len(profiles), int(selection))) - 1
    return profiles[selected_index]["slug"]


def choose_addons(starter_root: Path) -> list[str]:
    addons = list_addons(starter_root)
    print("Optional add-ons:")
    for addon in addons:
        print(f"  - {addon['slug']} ({addon['family']}): {addon['display_name']}")
    raw = prompt("Comma-separated add-ons to include", "")
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a new project from the SPEC-DRIVEN DEVELOPMENT STARTER PACK")
    parser.add_argument("--name")
    parser.add_argument("--target-path")
    parser.add_argument("--profile")
    parser.add_argument("--addons", default="")
    parser.add_argument("--no-git-init", action="store_true")
    parser.add_argument("--no-github-ci", action="store_true")
    parser.add_argument("--list-profiles", action="store_true")
    parser.add_argument("--list-addons", action="store_true")
    args = parser.parse_args()

    starter_root = Path(__file__).resolve().parent.parent

    if args.list_profiles:
        for profile in list_profiles(starter_root, include_planned=True):
            print(f"{profile['slug']}\t{profile['status']}\t{profile['display_name']}")
        return
    if args.list_addons:
        for addon in list_addons(starter_root):
            print(f"{addon['slug']}\t{addon['family']}\t{addon['display_name']}")
        return

    using_flags = bool(args.name and args.target_path and args.profile)
    project_name = args.name or prompt("Project name")
    target_path = args.target_path or prompt("Target directory", str(Path.cwd()))
    profile_name = args.profile or choose_profile(starter_root)
    addon_names = [part.strip() for part in args.addons.split(",") if part.strip()] if args.addons else choose_addons(starter_root)
    initialize_git = (not args.no_git_init) if using_flags else prompt_yes_no("Initialize a Git repository?", True)
    include_github_ci = (not args.no_github_ci) if using_flags else prompt_yes_no("Generate GitHub Actions CI?", True)

    project_path = create_project(
        starter_root=starter_root,
        project_name=project_name,
        target_root=Path(target_path),
        profile_name=profile_name,
        addon_names=addon_names,
        initialize_git=initialize_git,
        include_github_ci=include_github_ci,
    )

    print(f"Project created at {project_path}")
    print("Next steps:")
    print("  1. Review README.md, workflow-pack.json, and .workflow-pack/manifest.json")
    print("  2. Copy .env.example to .env and adjust values if needed")
    print("  3. Install dependencies and run the validation command from the README")
    print("  4. Start your first feature with /brief \"initial feature idea\"")


if __name__ == "__main__":
    main()
