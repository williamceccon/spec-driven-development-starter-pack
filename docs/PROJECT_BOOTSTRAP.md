# Project Bootstrap Guide

## What `new-project` Does

The bootstrap script:

1. creates a new target directory
2. copies the default starter profile into it
3. initializes a Git repository
4. runs the bundled workflow-pack installer against the new repo
5. leaves the repo ready for customization and the first commit

## Files Created by Default

- `.gitignore`
- `.github/workflows/ci.yml`
- `workflow-pack.json`
- `AGENTS.md`
- `.specify/memory/constitution.md`
- `.specify/templates/constitution-template.md`
- `.specify/templates/plan-template.md`
- `.specify/templates/tasks-template.md`
- `.opencode/commands/workflow.md`
- `.codex/prompts/workflow.md`
- deprecated legacy redirects under `.opencode/commands/`

## Recommended First Edits In a New Repo

- adjust `workflow-pack.json`
- confirm stack and validation commands
- review coverage threshold
- review CI commands
- add project-specific README content
- install runtime dependencies in the new repo

## Good Practice Checklist

- keep the workflow pack config in version control
- keep CI aligned with the blocking gates in `AGENTS.md`
- keep global skills generic and repo governance local
- only add new technology after approval and research
- always keep `SNAPSHOT.md` as the last stage of the workflow
