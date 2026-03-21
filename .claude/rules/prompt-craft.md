# Prompt Craft

Principles for structuring effective prompts, based on Anthropic's documentation.
Applied automatically when running `/brain-dump` and useful across all roles.

## Core principles
1. **Be clear and direct.** If a colleague with no context would be confused, so will Claude.
2. **Explain the why.** Motivation > instruction. "Do X because Y" beats "Do X."
3. **Show, don't just tell.** 3-5 diverse examples steer output better than paragraphs of rules.
4. **Tell what to do, not what not to do.** "Write in flowing prose" > "Don't use bullet points."
5. **Match style to desired output.** Markdown prompt = markdown response. Prose prompt = prose response.

## Structure techniques
- Use XML tags for separation: `<context>`, `<instructions>`, `<input>`, `<examples>`, `<output>`.
- Put long context/data at the top, query at the bottom (up to 30% quality improvement).
- Set a role in one sentence when it helps focus behavior.
- Use `<thinking>` and `<answer>` tags to separate reasoning from output.

## For complex tasks
- Break into steps: research/plan first, implement second.
- Give Claude a way to verify its work (tests, expected outputs, criteria).
- Ask Claude to self-check before finishing: "Verify your answer against [criteria]."
- Scope narrowly — broad prompts lead to infinite exploration.

## Context efficiency
- Smallest set of high-signal tokens wins. Don't pre-load what can be fetched on demand.
- Compress history into summaries preserving decisions and unresolved issues.
- Subagents explore extensively, return condensed summaries.

## Choosing the execution mode
| Mode | When | Signals |
|------|------|---------|
| Claude Code direct | Focused, sequential, single-role | One file, one script, quick fix |
| Code + subagents | Research-heavy, parallel search, context-sensitive | "Find all X", multiple sources, need synthesis |
| Agent team (`/team`) | Multi-role, parallel production | Distinct deliverables, different skills needed simultaneously |
| New session | Context is cluttered or task is unrelated | Long conversation, switching topics entirely |

**Proactive team assembly:** You do not need to wait for the user to invoke `/team`. When a task naturally splits into 2+ parallel roles, propose assembling a team or just do it. The `/team` command has the full protocol. When generating prompts (via `/brain-dump` or otherwise), embed team assembly instructions directly — don't reference slash commands, write the actual instructions so any session can follow them.

## Prompt file naming (prompts/)

Every prompt file in `prompts/` uses a bracketed prefix showing assignment and status:

```
[A04_ACTIVE]_topic_descriptor.md   ← current work, not yet executed
[A04_DONE]_topic_descriptor.md     ← executed and complete
[UTIL]_topic_descriptor.md         ← not tied to an assignment
```

**When creating a prompt:** always use this prefix. Update `DONE` when the prompt has been run successfully.

## Common anti-patterns to avoid
- Over-aggressive language ("CRITICAL: You MUST") — causes overtriggering. Use calm instructions.
- Prescriptive step-by-step plans — Claude's reasoning often exceeds what you'd prescribe.
- Over-engineering prompts for hypothetical edge cases.
- Dumping everything into context instead of retrieving just-in-time.
