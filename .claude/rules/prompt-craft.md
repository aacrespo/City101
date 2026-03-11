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

## Common anti-patterns to avoid
- Over-aggressive language ("CRITICAL: You MUST") — causes overtriggering. Use calm instructions.
- Prescriptive step-by-step plans — Claude's reasoning often exceeds what you'd prescribe.
- Over-engineering prompts for hypothetical edge cases.
- Dumping everything into context instead of retrieving just-in-time.
