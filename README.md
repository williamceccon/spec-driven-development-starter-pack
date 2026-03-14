# Specify Workflow Starter

An opinionated starter repository for bootstrapping new projects with:

- machine setup for Windows and macOS
- reusable Specify-first governance and workflow
- repo-local `AGENTS.md`, constitution, templates, and workflow commands
- bundled global skill package installation
- starter CI for Python + FastAPI + Next.js style projects
- project bootstrap scripts for creating a new repository from zero

## What This Repo Provides

- `scripts/bootstrap.ps1` and `scripts/bootstrap.sh`
  Install or validate core machine tools such as Git, Python, Node, Poetry, uv, and `specify-cli`.
- `scripts/install-workflow-pack.ps1` and `scripts/install-workflow-pack.sh`
  Install the bundled `specify-workflow-pack` skill into the global Codex skills directory.
- `scripts/doctor.ps1` and `scripts/doctor.sh`
  Validate that the machine is ready for the workflow.
- `scripts/new-project.ps1` and `scripts/new-project.sh`
  Create a new project from the bundled starter profile and install the workflow pack into the new repo.
- `profiles/python-fastapi-nextjs/`
  A default profile with `.gitignore`, CI, and `workflow-pack.json`.
- `skills/specify-workflow-pack/`
  The reusable workflow-pack skill, versioned inside this repo for portability.

## Quick Start

### Windows

```powershell
./scripts/bootstrap.ps1
./scripts/install-workflow-pack.ps1
./scripts/doctor.ps1
./scripts/new-project.ps1 -Name my-new-project -TargetPath C:\Users\WCeccon\OneDrive - SLB\Documents\programming
```

### macOS

```bash
bash ./scripts/bootstrap.sh
bash ./scripts/install-workflow-pack.sh
bash ./scripts/doctor.sh
bash ./scripts/new-project.sh my-new-project "$HOME/Documents/programming"
```

## Default Profile

The bundled profile is `python-fastapi-nextjs` and assumes:

- Python + Poetry backend
- FastAPI application
- optional Next.js frontend
- pytest, coverage, black, flake8, and mypy
- GitHub Actions CI
- Specify-first workflow with final snapshot stage

## Typical Onboarding Flow On a New Machine

1. Clone this repository.
2. Run the platform bootstrap script.
3. Install the bundled workflow pack globally.
4. Run the doctor script.
5. Create a new project from the starter profile.
6. Initialize the new repo on GitHub.
7. Start the first feature with `/workflow`.

## Next Reading

- [`docs/SETUP.md`](docs/SETUP.md)
- [`docs/PROJECT_BOOTSTRAP.md`](docs/PROJECT_BOOTSTRAP.md)
