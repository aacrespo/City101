# Tool and Workflow Protocol

## Before doing any repeatable operation
1. Check if a workflow exists in `workflows/` for this task
2. Check if tools exist in `tools/` for the steps
3. If both exist: follow the workflow, use the tools
4. If workflow exists but tool is missing: ask before creating the tool
5. If neither exists: do the task directly, then propose a tool/workflow if it's likely to recur

## When something fails
1. Read the full error
2. Diagnose the root cause
3. Propose a fix — state what you'd change in which file and why
4. Wait for approval
5. Implement the fix
6. Verify it works
7. Update the workflow's History section

## Never do without asking
- Create, modify, or delete any tool
- Create, modify, or deprecate any workflow
- Change any file in .claude/rules/
- Change CLAUDE.md

## You can do without asking
- Retry a failed tool with adjusted parameters
- Read any project file to diagnose a problem
- Run verification tools on data in output/
- Append to LEARNINGS.md
