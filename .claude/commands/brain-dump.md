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

5. **Present the result.** Show the structured prompt in a code block so it's easy to copy. Below it, add a short note on:
   - What mode was detected and why
   - Anything important that was left out (gaps in the dump)
   - Suggested next step

## Rules
- Never add information the user didn't provide or imply. Structure, don't invent.
- Keep prompts concise — context efficiency matters. Don't pad.
- Reference project files by path when relevant (the user is working in city101).
- If the dump is too vague to structure, say so and ask one focused question.
