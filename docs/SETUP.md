# Setup Guide

## Machine Goals

A ready machine should have:

- Git
- Python 3.12+
- Node.js 18+
- Poetry
- uv
- `specify-cli`
- a global Codex skills directory available at `$CODEX_HOME/skills` or `~/.codex/skills`

## Windows Notes

The PowerShell bootstrap script prefers `winget` when available.
If `winget` is unavailable, the script prints the commands you still need to run manually.

## macOS Notes

The shell bootstrap script prefers Homebrew when available.
If Homebrew is unavailable, the script prints the commands you still need to run manually.

## Global Skill Installation

The starter repo bundles `skills/specify-workflow-pack/` so you do not need to manually reconstruct the workflow on a new machine.
Use the install script to copy it into your global Codex skills directory.

## Repo Bootstrap

After machine setup:

1. Run the new-project script.
2. Review the generated `workflow-pack.json`.
3. Review the generated `.github/workflows/ci.yml`.
4. Commit the initial scaffold.
5. Create the remote GitHub repository.
6. Push and open the first PR when ready.
