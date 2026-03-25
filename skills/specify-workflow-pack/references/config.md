# workflow-pack.json

Use `workflow-pack.json` at the repository root as the repo-local workflow contract.

## Minimum Example

```json
{
  "project_name": "example-project",
  "profile": "python-api"
}
```

## Recommended Example

```json
{
  "project_name": "example-project",
  "pack_version": "1.0.0",
  "core_version": "1.0.0",
  "profile": "python-api",
  "profile_version": "1.0.0",
  "profile_options": {},
  "addons": ["postgres", "core-workflow"],
  "supported_platforms": ["Windows", "macOS", "Linux"],
  "primary_product": "Python API service",
  "legacy_surface": "legacy runtime retained only for compatibility",
  "artifact_dir": "specs",
  "supported_workspaces": ["Codex", "OpenCode", "GitHub Copilot", "Antigravity"],
  "coverage_threshold": 100,
  "backend_stack": ["Python 3.12+", "venv", "pip", "HTTP service starter"],
  "frontend_stack": [],
  "repository_map": [
    "`src/` -> backend application code",
    "`tests/` -> automated tests",
    "`skills/` -> repo-local fallback skills"
  ],
  "blocking_gates": [
    "python -m unittest discover -s tests -p 'test_*.py' -v"
  ],
  "observational_gates": [
    "python -m compileall src",
    "Document database migrations before merging schema changes"
  ],
  "required_skills": ["brainstorming", "gh-fix-ci", "gh-address-comments"],
  "bundled_skills": [
    "brainstorming",
    "gh-fix-ci",
    "gh-address-comments",
    "writing-plans",
    "verification-before-completion",
    "systematic-debugging",
    "test-driven-development",
    "requesting-code-review",
    "skill-creator"
  ],
  "recommended_skills": {
    "core-workflow": ["brainstorming", "writing-plans", "verification-before-completion"],
    "quality": ["requesting-code-review", "systematic-debugging", "test-driven-development"]
  },
  "brief_artifact": "BRIEF.md",
  "local_skills_dir": "skills",
  "constitution_version": "2.0.0"
}
```

## Supported Keys

- `project_name`: Required display name for generated workflow files
- `pack_version`: Version of the public starter pack contract
- `core_version`: Version of the core workflow layer
- `profile`: Selected project profile slug
- `profile_version`: Version of the selected profile
- `profile_options`: Optional profile-specific settings
- `addons`: Selected add-on slugs
- `supported_platforms`: Target operating systems for the generated repo
- `primary_product`: Short description of the main product surface
- `legacy_surface`: Short description of what remains legacy
- `artifact_dir`: Defaults to `specs`
- `supported_workspaces`: Agent/tool surfaces this repo should support
- `coverage_threshold`: Repository threshold for coverage-sensitive workflows
- `backend_stack`: Backend technologies for this repo
- `frontend_stack`: Frontend technologies for this repo
- `repository_map`: Key repo directories and responsibilities
- `blocking_gates`: Validation commands that block completion
- `observational_gates`: Checks that should be recorded even when non-blocking
- `frontend_validation`: Optional frontend validation command
- `required_skills`: Required baseline skills
- `bundled_skills`: Repo-local vendored skills copied into generated repositories for the selected profile or add-ons
- `recommended_skills`: Optional orchestration bundles by name
- `brief_artifact`: Defaults to `BRIEF.md`
- `local_skills_dir`: Defaults to `skills`
- `legacy_commands`: Deprecated commands that should redirect to the brief-first flow
- `constitution_version`: Constitution version for generated Specify files
- `ratified_date`: Optional initial ratified date

## Contract Notes

- `.workflow-pack/manifest.json` is generated from `workflow-pack.json`
- generated repos should work with global skills or repo-local fallback skills
- `bundled_skills` should match skills available under `skills/specify-workflow-pack/assets/bundled-skills/`
- `BRIEF.md` is still created later by `/brief`, not by the starter generator
- `profile` and `addons` should match the generated manifest
