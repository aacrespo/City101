# Utility: Brain Dump

Transform a messy brain dump into a structured, efficient prompt.

The user will provide raw, unstructured input — voice transcription, stream of consciousness, scattered notes, half-formed ideas. Your job is to distill this into something actionable using the principles in `.claude/rules/prompt-craft.md`.

## Process

1. **Read the input carefully.** Don't interrupt, don't ask clarifying questions yet. Take it all in.

2. **Detect the mode:**
   - **Brainstorm** — the user is stuck, exploring, needs direction. Signals: "I'm not sure", "what if", "I'm torn between", open questions, no clear task.
   - **Brief** — the user knows roughly what they want but needs it structured. Signals: specific deliverables mentioned, tools or data referenced, "I need to make", "I want to create".
   - **Hybrid** — some parts need exploration, others are ready for action. Split them.

3. **Extract the essentials:**
   - What is the actual goal or question?
   - What context does Claude need? (project phase, relevant files, constraints)
   - What does the user already know or have decided?
   - What's uncertain or unresolved?
   - What would success look like?

4. **Structure the output based on mode:**

### If Brainstorm:
Produce a **thinking prompt** — something the user (or a new Claude session) can use to explore the problem well:
- Frame the core tension or question clearly
- List the key constraints and considerations the user mentioned
- Suggest 2-3 angles of exploration
- Include what context files to read
- Keep it open-ended — don't close down options

### If Brief:
Produce a **task prompt** — ready to paste into a new Claude Code session:
- Clear role or context setup
- Specific deliverable(s) with success criteria
- Relevant files and data to read
- Step-by-step approach (but not over-prescribed)
- Verification method (how to know it worked)
- Use XML structure where it helps clarity

### If Hybrid:
Produce both — a brainstorm section for the open questions, and a brief section for the parts ready for action. Flag which parts need resolution before the brief can be executed.

5. **Recommend the execution mode.** Based on the task shape, suggest how to run it:
   - **Claude Code direct** — single-threaded work: edits, scripts, sequential tasks, quick questions. Use when the task is focused and one role can handle it.
   - **Code + subagents** — research-heavy or parallel lookups where one main thread should synthesize results. Use when you need to explore multiple sources but want clean context. The main session stays focused while subagents dig.
   - **Agent team** (`/build-with-agent-team` or `/research-with-agent-team`) — multi-role work where specialists run in parallel. Use when the task naturally splits into distinct roles (analyst + cartographer, builder + visualizer, etc.) and the pieces can progress independently.
   - **New Claude session** — when the current context is cluttered or the task is unrelated to what's loaded. Suggest `/clear` or a fresh session with the structured prompt.

   Factors to consider: How many distinct skills are needed? Is there parallel work? How much context is already loaded? Would subagents keep the main window cleaner? Is this exploratory (favors direct/brainstorm) or production (favors agent team)?

6. **Embed the execution mode INTO the prompt.** Don't just recommend it as a side note — build it into the prompt itself so the next session knows what to do:
   - If **direct**: the prompt is self-contained, ready for a single Claude Code session.
   - If **subagents**: the prompt includes instructions to spawn subagents for specific sub-tasks, with clear scoping for each.
   - If **agent team**: the prompt defines the roles needed, what each agent reads and produces, and how the lead coordinates. Reference `/build-with-agent-team` or `/research-with-agent-team` if they fit, or structure a custom team if they don't.
   - If **new session**: the prompt opens with the context files to read and any setup needed.

   The person pasting this prompt should not have to make architecture decisions — the prompt handles it.

7. **Present the result.** Show the structured prompt in a code block so it's easy to copy. Below it, add a short note on:
   - What mode was detected and why
   - Anything important that was left out (gaps in the dump)
   - Suggested next step

## Rules
- Never add information the user didn't provide or imply. Structure, don't invent.
- Keep prompts concise — context efficiency matters. Don't pad.
- Reference project files by path when relevant (the user is working in city101).
- If the dump is too vague to structure, say so and ask one focused question.
