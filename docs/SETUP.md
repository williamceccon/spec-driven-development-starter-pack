# Setup Guide

## Machine Goals

A ready machine should have:

- Git
- Python 3.12+
- GitHub CLI (`gh`)
- `specify-cli`
- a global Codex skills directory at `$CODEX_HOME/skills` or `~/.codex/skills`
- the bundled essential skills installed globally:
  - `specify-workflow-pack`
  - `brainstorming`
  - `gh-fix-ci`
  - `gh-address-comments`

Profile-specific tools are validated later by the doctor command once you choose a profile.

## Platform Notes

### Windows

- bootstrap uses PowerShell
- `winget` is preferred when available
- if `winget` is unavailable, the script prints suggested manual installs

### macOS

- bootstrap uses POSIX shell
- Homebrew is preferred when available
- if Homebrew is unavailable, the script prints suggested manual installs

### Linux

- bootstrap uses POSIX shell
- the script validates the same baseline tools as macOS
- package installation commands are printed as suggestions when a package manager is not assumed

## Install the Workflow Pack Skills

Windows:

```powershell
./scripts/install-workflow-pack.ps1
```

macOS / Linux:

```bash
bash ./scripts/install-workflow-pack.sh
```

Restart Codex after installing global skills so new sessions can see them.

## Run Doctor

The doctor flow checks:

- machine tools
- GitHub CLI auth state
- generated repo contract when `workflow-pack.json` exists
- `.env.example` / `.env` setup reminders

Windows:

```powershell
./scripts/doctor.ps1
```

macOS / Linux:

```bash
bash ./scripts/doctor.sh
```

## Discover Profiles And Add-ons

List profiles:

```powershell
./scripts/new-project.ps1 -ListProfiles
```

```bash
bash ./scripts/new-project.sh --list-profiles
```

List add-ons:

```powershell
./scripts/new-project.ps1 -ListAddons
```

```bash
bash ./scripts/new-project.sh --list-addons
```
