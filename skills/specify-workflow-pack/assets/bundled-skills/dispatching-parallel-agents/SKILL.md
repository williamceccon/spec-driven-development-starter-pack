---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
---

# Dispatching Parallel Agents

Use this skill when the work naturally splits into independent domains that can be investigated or implemented in parallel.

Core rules:
- assign one focused agent per independent problem domain
- keep prompts self-contained and narrow in scope
- avoid parallelizing tasks that share files, state, or sequencing
- review and integrate all results together before declaring success

Recommended workflow:
1. Group failures or tasks by subsystem.
2. Confirm the groups are actually independent.
3. Dispatch one agent per group with clear constraints and expected output.
4. Review each result, check for conflicts, and run full verification afterward.
