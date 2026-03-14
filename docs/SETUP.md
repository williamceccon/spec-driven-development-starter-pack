# Setup Guide

## Machine Goals

A ready machine should have:

- Git
- Python 3.12+
- Node.js 18+
- Poetry
- uv
- GitHub CLI (`gh`)
- `specify-cli`
- a global Codex skills directory available at `$CODEX_HOME/skills` or `~/.codex/skills`
- the bundled essential skills installed globally:
  - `specify-workflow-pack`
  - `brainstorming`
  - `gh-fix-ci`
  - `gh-address-comments`

## Windows Notes

The PowerShell bootstrap script prefers `winget` when available.
If `winget` is unavailable, the script prints the commands you still need to run manually.

## macOS Notes

The shell bootstrap script prefers Homebrew when available.
If Homebrew is unavailable, the script prints the commands you still need to run manually.

## Global Skill Installation

The starter repo bundles the required skills under `skills/`.
Use the install script to copy them into your global Codex skills directory:

- `./scripts/install-workflow-pack.ps1`
- `bash ./scripts/install-workflow-pack.sh`

This installs the same baseline on a fresh machine without requiring the source skill repositories.

## Upstream Skill Source

The bundled `brainstorming` skill comes from:

- [benjaminasterA/antigravity-awesome-skills](https://github.com/benjaminasterA/antigravity-awesome-skills)

You can refresh the upstream copy later, but the starter works from the versioned local bundle by default.

## Repo Bootstrap

After machine setup:

1. Run the new-project script.
2. Review the generated `workflow-pack.json`.
3. Review the generated `.github/workflows/ci.yml`.
4. Install runtime dependencies in the new repo.
5. Start the first feature with `/brief "initial feature idea"`.
6. Confirm the generated slug in `BRIEF.md`.
7. Run `/workflow <slug>`.

## Skill Precedence In Generated Repos

Generated repos use this precedence:

1. global skill installed in `$CODEX_HOME/skills` or `~/.codex/skills`
2. repo-local fallback skill under `skills/`
3. explicit failure in `doctor` if neither source exists

Restart Codex after installing new global skills so they appear in future sessions.
