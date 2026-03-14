# Specify Workflow Starter

An opinionated starter repository for bootstrapping new projects with:

- machine setup for Windows and macOS
- reusable Specify-first governance and workflow
- repo-local `AGENTS.md`, constitution, templates, and workflow commands
- bundled essential skills for brief generation, CI recovery, and PR comment handling
- starter CI for Python + FastAPI + Next.js style projects
- project bootstrap scripts for creating a new repository from zero

## What This Repo Provides

- `scripts/bootstrap.ps1` and `scripts/bootstrap.sh`
  Install or validate core machine tools such as Git, Python, Node, Poetry, uv, GitHub CLI, and `specify-cli`.
- `scripts/install-workflow-pack.ps1` and `scripts/install-workflow-pack.sh`
  Install the bundled skills into the global Codex skills directory.
- `scripts/doctor.ps1` and `scripts/doctor.sh`
  Validate that the machine is ready for the brief-first workflow.
- `scripts/new-project.ps1` and `scripts/new-project.sh`
  Create a new project from the bundled starter profile and install the workflow pack into the new repo.
- `profiles/python-fastapi-nextjs/`
  A default profile with `.gitignore`, CI, and `workflow-pack.json`.
- `skills/`
  Bundled repo-local copies of `specify-workflow-pack`, `brainstorming`, `gh-fix-ci`, and `gh-address-comments`.

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
- brief-first Specify workflow with final snapshot stage

## Brief-First Workflow

1. Start in the generated repo with `/brief "initial feature idea"`.
2. Use the mandatory `brainstorming` skill to refine the feature.
3. Generate `BRIEF.md` with a canonical slug.
4. Run `/workflow <slug>` only after `BRIEF.md` is approved.
5. Let the workflow continue through Specify, validation, fix round, reports, and final snapshot.

## Bundled Essential Skills

The starter ships with these essential skills:

- `brainstorming`
- `gh-fix-ci`
- `gh-address-comments`
- `specify-workflow-pack`

Preferred precedence in generated repos:

1. global skill installed in `$CODEX_HOME/skills` or `~/.codex/skills`
2. repo-local fallback under `skills/`
3. explicit failure from `doctor` if neither is available

The `brainstorming` skill is sourced from [benjaminasterA/antigravity-awesome-skills](https://github.com/benjaminasterA/antigravity-awesome-skills).

## Typical Onboarding Flow On a New Machine

1. Clone this repository.
2. Run the platform bootstrap script.
3. Install the bundled skills globally.
4. Run the doctor script.
5. Create a new project from the starter profile.
6. Review the generated `workflow-pack.json`.
7. In the new repo, start with `/brief "initial feature idea"`.
8. Run `/workflow <slug>` after `BRIEF.md` is approved.

## Roadmap

### v0.1 - Field Validation

Focus on validating the starter in a real new project.

- prove the bootstrap flow on Windows and macOS
- validate `bootstrap`, `doctor`, and `new-project` end to end
- confirm the generated repo is ready for `Specify`, `/brief`, and CI from day one
- collect friction points, missing setup steps, and naming issues from actual use
- stabilize the default `python-fastapi-nextjs` profile

### v0.2 - Reusable Project Profiles

Expand the starter into a more configurable baseline for different project shapes.

- support more than one starter profile
- make workflow configuration more declarative and easier to override per repo
- improve generated docs for setup, daily workflow, and agent compatibility
- add clearer CI defaults and optional gates for lint, typing, and frontend validation
- strengthen cross-platform parity between PowerShell and shell scripts

### v0.3 - Workflow Sync and Upgrades

Make it easier to evolve many repositories from one maintained source.

- add a safer sync/update path for repos created from this starter
- version workflow-pack assets more explicitly
- document upgrade paths for governance, templates, and commands
- add validation checks that warn when a consuming repo drifts from the expected baseline
- improve compatibility for Codex, OpenCode, GitHub Copilot, and Antigravity

### v0.4 - Feature Insights Toolkit

Introduce reusable assistance for shaping features before implementation.

- add a feature-insights tool or skill for turning briefs into scope, risks, open questions, and suggested slices
- generate research prompts for unknown technology decisions
- help compare candidate tools with a bias toward strong free tiers and low lock-in
- identify CI, testing, and rollout implications before implementation starts
- feed stronger inputs into `/workflow` without bloating the bootstrap layer

### v1.0 - Generic Multi-Project Platform

Promote the starter from validated template to durable internal platform.

- treat this repo as the canonical source for new project initialization
- provide a well-documented install, update, and doctor experience for multiple machines and agents
- define stable extension points for profiles, skills, and optional workflow modules
- keep the baseline lightweight while allowing smarter add-ons to evolve independently
- ensure a new repo can be started with solid defaults, green CI expectations, and minimal manual setup

## Next Reading

- [`docs/SETUP.md`](docs/SETUP.md)
- [`docs/PROJECT_BOOTSTRAP.md`](docs/PROJECT_BOOTSTRAP.md)
