# Project Bootstrap Guide

## What `new-project` Does

The bootstrap script:

1. creates a new target directory
2. copies the default starter profile into it
3. initializes a Git repository
4. runs the bundled workflow-pack installer against the new repo
5. copies repo-local fallback skills into the generated repo
6. leaves the repo ready for customization and the first brief

## Files Created by Default

- `.gitignore`
- `.github/workflows/ci.yml`
- `workflow-pack.json`
- `AGENTS.md`
- `.specify/memory/constitution.md`
- `.specify/templates/constitution-template.md`
- `.specify/templates/plan-template.md`
- `.specify/templates/tasks-template.md`
- `.opencode/commands/brief.md`
- `.opencode/commands/workflow.md`
- `.codex/prompts/brief.md`
- `.codex/prompts/workflow.md`
- `skills/brainstorming/`
- `skills/gh-fix-ci/`
- `skills/gh-address-comments/`
- deprecated legacy redirects under `.opencode/commands/`

## Recommended First Edits In a New Repo

- adjust `workflow-pack.json`
- confirm stack and validation commands
- review coverage threshold
- review CI commands
- add project-specific README content
- install runtime dependencies in the new repo

## First Functional Steps In a New Repo

1. Explain the feature with `/brief "initial feature idea"`.
2. Refine the idea through brainstorming until `BRIEF.md` is complete.
3. Confirm the slug in `BRIEF.md`.
4. Run `/workflow <slug>` using that exact slug.

## Good Practice Checklist

- keep the workflow pack config in version control
- keep CI aligned with the blocking gates in `AGENTS.md`
- keep essential fallback skills versioned under `skills/`
- only add new technology after approval and research
- always keep `SNAPSHOT.md` as the last stage of the workflow
