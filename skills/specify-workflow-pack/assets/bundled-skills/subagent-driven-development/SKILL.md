---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development

Use this skill to execute a written plan by dispatching fresh subagents task by task, with review between steps.

Core rules:
- use a fresh subagent for each implementation task
- require spec compliance review before code quality review
- keep the controller focused on coordination, not implementation details
- do not move to the next task while review issues remain open

Recommended workflow:
1. Read the plan and extract concrete tasks.
2. Dispatch an implementer subagent with the exact task text and context.
3. Run spec review on the result.
4. Run code quality review after spec compliance is clean.
5. Mark the task complete and continue to the next one.
