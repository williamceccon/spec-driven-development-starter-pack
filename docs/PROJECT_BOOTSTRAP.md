# Project Bootstrap Guide

## What `new-project` Does

The guided generator:

1. selects a profile
2. applies optional add-ons
3. writes a beginner-friendly `README.md`
4. writes `.env.example`
5. writes `workflow-pack.json`
6. installs repo-local workflow governance
7. writes `.workflow-pack/manifest.json`
8. optionally initializes Git

## Files Generated In A New Repo

- `README.md`
- `.env.example`
- `workflow-pack.json`
- `.workflow-pack/manifest.json`
- `AGENTS.md`
- `.specify/memory/constitution.md`
- `.specify/templates/constitution-template.md`
- `.specify/templates/plan-template.md`
- `.specify/templates/tasks-template.md`
- `.opencode/commands/brief.md`
- `.opencode/commands/workflow.md`
- `.codex/prompts/brief.md`
- `.codex/prompts/workflow.md`
- repo-local fallback skills under `skills/`
- profile starter files such as `.gitignore`, CI, or starter source files

## Why The Manifest Matters

`.workflow-pack/manifest.json` records:

- installed pack version
- installed core version
- selected profile
- selected add-ons
- required skills
- recommended skill bundles
- generated repo surfaces

This is the machine-readable contract for future sync and drift detection work.

## Recommended First Steps In A Generated Repo

1. Read `README.md`
2. Copy `.env.example` to `.env`
3. Review `workflow-pack.json`
4. Review `.workflow-pack/manifest.json`
5. Install dependencies using the generated commands
6. Run the validation command once before creating real features
7. Create the GitHub repository and push
8. Start the first feature with `/brief`

## Good Practice Checklist

- keep `workflow-pack.json` in version control
- keep `.workflow-pack/manifest.json` in version control
- keep CI aligned with the generated validation gates
- keep required fallback skills versioned under `skills/`
- treat add-ons as explicit project decisions, not hidden defaults
- keep `SNAPSHOT.md` as the last workflow artifact
