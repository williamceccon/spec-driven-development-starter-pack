---
name: specify-workflow-pack
description: Create, install, sync, and validate a reusable Specify-first workflow pack across repositories and workspaces. Use when Codex needs to standardize a repo around AGENTS.md, constitution, Specify templates, multi-agent prompts, autonomous workflow commands, or machine-portable governance shared across Codex, OpenCode, GitHub Copilot, and Antigravity.
---

# Specify Workflow Pack

## Overview

Use this skill to install or refresh a reusable Specify-first workflow pack in a repository without copying your entire global skills setup into that repo.

This skill is for:

- bootstrapping a new repo with a standard governance and workflow layer
- syncing an existing repo to the current workflow pack
- validating whether a machine or repo is ready to use the workflow consistently
- keeping Codex, OpenCode, Copilot, and Antigravity aligned on the same repo-local process

## Quick Start

1. Create a `workflow-pack.json` file in the target repository.
2. Run `scripts/install_workflow_pack.py` from this skill with the repo path and config path.
3. Review the generated diffs in the repo.
4. Run `scripts/doctor_workflow_pack.py` to validate the installation and local tool availability.
5. Commit the generated repo-local files.

## Core Workflow

### 1. Inspect Before Installing

Before writing files, inspect the target repo for:

- existing `AGENTS.md`
- existing `.specify/` assets
- current CI commands and coverage rules
- supported workspaces and agent surfaces already present

If the repo already has governance files, compare them with the generated output before overwriting intentionally customized policy.

### 2. Prepare the Config

Use `workflow-pack.json` as the repo-local contract for the pack.

Read `references/config.md` for:

- required keys
- optional keys
- a complete example
- guidance on how to represent repo-specific commands and structure

### 3. Install or Sync the Pack

Run:

```powershell
python <skill-dir>/scripts/install_workflow_pack.py --repo <repo-path> --config <repo-path>/workflow-pack.json
```

Use `--dry-run` first when you want to see which files will be written without changing the repo.

The installer renders repo-local files from the templates in `assets/templates/`.

### 4. Validate the Result

Run:

```powershell
python <skill-dir>/scripts/doctor_workflow_pack.py --repo <repo-path> --config <repo-path>/workflow-pack.json
```

This validates:

- required generated files exist
- key tools are available on the machine
- the workflow entrypoint files exist where expected
- the repo appears ready for multi-agent use

### 5. Review and Commit

After install or sync:

- inspect diffs carefully
- confirm CI commands still reflect reality
- confirm coverage threshold matches the repo configuration
- confirm repo-specific paths and artifact locations are correct
- commit the generated changes in the target repo

## Bundled Resources

### scripts/

- `install_workflow_pack.py`: render or refresh the repo-local workflow pack from templates
- `doctor_workflow_pack.py`: validate that the repo and machine are ready to use the pack

### references/

- `config.md`: schema and examples for `workflow-pack.json`

### assets/

- `templates/`: renderable templates for AGENTS, constitution, Specify templates, workflow commands, and legacy redirects

## Notes

- Keep the skill global and the generated governance local to each repo.
- Do not copy unrelated global skills into repositories.
- Prefer config-driven repo installation over manual copy/paste.
- When a repo needs different stack, coverage, or validation commands, change `workflow-pack.json`, not the global skill defaults.
