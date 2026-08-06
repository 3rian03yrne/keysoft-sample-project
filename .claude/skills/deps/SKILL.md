# .claude/skills/deps/SKILL.md
---
name: deps
description: Produce a dependency report for the repo.
context: fork                       # verbose work stays out of the main thread
allowed-tools: [Read, Grep, Bash, Write, mcp__github]   # exactly what it needs — Write is for the report
argument-hint: [path]
---
* List dependencies
* Flag outdated dependencies
* Categorize severity of findings low/medium/high
* Include a top level one sentence summary of the findings with a PASS/FAIL
