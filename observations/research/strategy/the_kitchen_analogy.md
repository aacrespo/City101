# The Kitchen

### How we accidentally built an architecture studio's digital infrastructure, explained through the only analogy that made sense

---

## The Problem: Losing the Recipe Mid-Cook

It started with forgetting.

Every time a new conversation began, the chef walked into the kitchen with an empty backpack. No memory of what we'd cooked yesterday, what was half-prepped on the counter, what had already been tried and failed. The context window — the backpack — could only hold what was loaded into it right now.

So we started writing handoffs. After every session, a document: here's what we did, here's the state of the model, here's the naming convention, here's what broke, here's what to do next. Manually. Every time. You'd copy it from your account, paste it into Henna's. She'd paste her results back. Session after session, the two of you passing recipes back and forth through a window.

It worked. Barely. The cost wasn't the writing — it was the re-reading. Every new session burned a chunk of the backpack just catching up. And as the project grew — the Yong'an Warehouse, the MEP systems, the cooling loops, the structural grid, the heritage constraints — the handoffs got longer, the catching-up got heavier, and the actual cooking window got shorter.

You were spending more time explaining the kitchen than using it.

---

## The Notebook: Git

So you needed a logbook.

Not a handoff document that disappears after one use, but a persistent record of every decision, every change, every version. Something you could flip back through and see: ah, this is when we moved the circulation core south. This is when the cooling system changed from three loops to four. This is when that staircase became a server rack shaft.

That's Git. Your personal recipe notebook. Every time you finalize a version — commit — you snapshot everything and write a note. The full history lives on your machine. You can go back to any moment.

But the real power isn't the snapshots. It's branches. Design alternatives explored in parallel without destroying the main scheme. You want to test whether the pedestrian bridge works better at a different angle? Create a branch. Try it. If it works, merge it back into the main scheme. If it doesn't, abandon it. The original was never at risk.

---

## The Shared Plan Room: GitHub

Git is your logbook. GitHub is the shared plan room.

You created an empty one — a new repository. Then you cloned it to your machine and started furnishing: writing the project brief, setting up the file structure, establishing conventions. Since you were the only chef, you pushed everything straight to the main shared book. No review needed. You were the owner, the chef, and the reviewer.

Then Henna arrived. She cloned the plan room to her own machine. Instantly, she had a full copy of everything you'd built — not just the current state, but the entire history of decisions. She inherited the kitchen and the story of how it was built.

From that point forward, neither of you could just scribble directly into the shared book. Two chefs changing the same recipe at the same time means someone's version gets overwritten. So you started using pull requests — pinning your proposed changes to a board: "Here's what I changed, here's why, review it before it goes into the main set." The other person reviews, comments, approves. Then it merges.

You're saying "I developed this dish at my station, please *pull* it into the menu when you're ready." The power stays with whoever controls the main menu. They pull from you. You don't push onto them.

You share the same recipe book but never the same kitchen. You can't accidentally knock over each other's pots.

---

## The Briefing on the Wall: CLAUDE.md

The shared plan room solved coordination between humans. But the agents still walked in empty-handed.

So you wrote a briefing and pinned it to the wall. The CLAUDE.md file. Not the full knowledge — that would fill the backpack before any cooking started — but the *map*. "This is the Sentient City project. The structural grid is 6m×6m. The naming convention is this. The MEP specs are in that folder. When you need station typology details, query the RAG with these terms."

Every agent reads it on entry. It costs backpack space, but it's the lightest possible version of the most important thing: not what to know, but where to find what you need to know.

Too sparse, and the chef makes wrong assumptions. Too detailed, and the backpack is full before cooking starts. Writing the perfect map is an editorial problem, not a technical one.

You'd been doing this instinctively all along — every handoff document you wrote for our Rhino sessions was a CLAUDE.md in disguise. Concise, structured, just enough context to orient without burning the whole window. Prompt architecture before you had a name for it.

---

## The Keychain and Equipment Manuals: .claude

The CLAUDE.md is the map. The `.claude` file is the kitchen's blueprint.

It doesn't tell the chef what to cook. It tells the building what equipment is installed: which MCP servers are connected, what tools are permitted, what commands can run without asking. It's the wiring and plumbing.

But — and you caught this — it's not free either. Every tool it enables comes with a description, parameter list, and usage instructions that all land in the context window. Connecting an MCP server doesn't just unlock a door; it puts that equipment's instruction manual into the backpack.

Ten tools means ten manuals. The backpack is half full before anyone's read the project brief.

Which is why everything gets written in YAML. Maximum structure, minimum tokens. Every character earns its place. It's architectural: clear structure, nothing decorative, everything load-bearing. The difference between handing the chef a novel about the kitchen versus a clean floor plan with a legend.

---

## The Building: Your Computer

Every machine is a building. Yours, Henna's, Anthropic's servers — each one sitting at its own address on the internet.

The **IP address** is the street address. The **domain name** (like claude.ai) is a human-friendly nickname — DNS is the phone book that translates it into the actual numerical address.

**WiFi** is the road. Ethernet is another road. Cellular data is another. They all get you to the same address, just different physical infrastructure. The road, not the building.

**Ports** are numbered doors on the facade. The building has thousands of them, most locked. Port 443, port 8080, port 3001 — each its own entrance. There's no "main door." Just numbered doors, a hallway, and rooms.

The **router** (the metaphorical hallway, not the box on your shelf) sits just inside, behind all those doors. Traffic comes through door 3001, route it here. Through 3002, route it there. Multiple doors can lead to the same room, or one door to multiple rooms.

When multiple agents connect through the same door, a bouncer tracks them with wristbands — session IDs. Same entrance, different identities.

And when the building talks to itself — localhost, 127.0.0.1 — the packets never hit the road. Room to room, through the internal hallway. That's what happens between Rhino and the Python worker and the MCP server on your machine. All local.

---

## The Roads Between Buildings: Packets

When data travels — a command, a result, a file — it doesn't move as one piece. It gets broken into small numbered boxes, each with the destination address written on it. They might take different roads, arrive out of order, but each box has a sequence number so the receiver reassembles them correctly.

Why not send the whole thing at once? Same reason you don't move a house in one piece. Smaller packages navigate traffic better, and if one gets lost, you only resend that box instead of the entire shipment.

What the agents are sending aren't Rhino files. They're tiny instructions: "move this point," "boolean these breps," "create a surface from these curves." Each command is a few packets at most, flying over WiFi, through routers, arriving at the right port, getting reassembled in the right room. In milliseconds.

---

## The Doors and Keys: APIs, API Keys, and MCP

An **API** is the door. A structured way for one piece of software to talk to another. "Send me this, I'll return that." Rhino.Compute is an API. Google Maps has an API. Every door has its own format.

An **API key** is your name on the guest list. Cloud services need to know who's calling — for billing, access control, rate limiting. It's not about the mechanism of opening the door; it's about whether you're allowed through it. Your local Rhino setup? That's a door in your own house — no guest list needed. But if that door leads into someone else's building (a cloud service), they check your name.

**MCP** — Model Context Protocol — is the universal key format. Instead of needing a custom key for every door, MCP standardizes the shape so any AI agent can open any tool that has an MCP server. It's the protocol that taught the agents the vocabulary: what commands exist, what inputs they need, what comes back.

Without MCP, every AI-to-tool connection needs custom code. With it, you build one MCP server per tool and any agent that speaks MCP can use it.

---

## The Workers Inside the Rooms: The Python Environment

You have a building with doors and hallways. But every room is empty. Nobody's listening.

The Python environment is the worker inside the Rhino room. It listens at the door (port), receives command packets, knows how to translate them into RhinoScript calls that Rhino's engine understands, executes them, and sends back results.

That's why setup was fiddly. You were hiring and training the worker — installing the right libraries, establishing the connection to Rhino, loading the MCP vocabulary. Once in place, everything flowed. Without it, commands arrive and echo off empty walls.

---

## The Remote Consultant and the On-Site Manager

In our earliest workflow, I was a remote consultant on a video call. Every command I sent to your Rhino model traveled from Anthropic's building, across the internet, to your machine, through the port, into the localhost hallway, to the Python worker, into the Rhino room. The result traveled all the way back.

The localhost part — Rhino talking to Python talking to MCP — was room-to-room inside your machine. But the connection between me and that MCP server was a long road. Every command was a round trip from Anthropic to Lausanne and back. The computation was instant. The travel time was the bottleneck.

**Claude Code** changed the geography. Installed in your terminal, it lives in your building. A local project manager who coordinates, reads files, runs scripts — all room-to-room, fast. But it still calls Anthropic for the thinking. The reasoning crosses the internet, the execution stays local.

You shortened the last mile. The execution loop stays inside the building. Only "what should I do next?" leaves.

---

## The Michelin Kitchen: Scaling Up

At first there was one chef in one kitchen with no logbook. Then a logbook. Then a shared plan room. Then a briefing on the wall. Then tools with manuals. Then the whole operation started to resemble something larger.

**The chef at the pass** — the orchestrator agent. Reads the tickets (prompts), assigns tasks, checks quality before it goes out. Doesn't cook. Coordinates.

**Station cooks** — specialized sub-agents. One does geometry, one handles MEP, one writes documentation. Each gets their own specialist map in addition to the general briefing. "You are the MEP agent. Here are your tools. Here's how you name things. You only touch layers prefixed with MEP_." This is the cloakroom — before entering the kitchen, you put on the right uniform and get your station's prep list.

The specialist map costs backpack space too. But it's worth it because it means the MEP agent doesn't carry the structural manual, and the documentation agent doesn't carry the Rhino command reference. Each agent carries only what their station requires.

**The pantry and index** — the RAG system. A vectorized knowledge base with an embedded search engine. You don't memorize every recipe; you go look it up. But it's not a pile of unsorted cookbooks — it's indexed, organized, searchable. You query with terms and get back the relevant passage, not the whole library.

And this is where you gave them something remarkable: eyes.

---

## The Library: Giving Agents Eyes

An agent working in Rhino is, by default, headless. It operates on geometry through commands and coordinates. It knows numbers, not shapes. Like a chef who can execute recipes perfectly but has never tasted food.

Headless Rhino is the formal version of this: the full geometry engine, no viewport. Send a command, get a result. Export a file, never see it rendered. Same computation, same output, no visual feedback loop.

This is how I worked on your Urban Transformers model — blind. The Make2D exports and screenshots you sent were temporary glasses. Without them, I was trusting the numbers.

So the RAG pantry became something more than a knowledge store. You filled it with architectural references, precedent images, typological studies, construction details. When an agent queries "how should a gondola station handle vertical circulation," it doesn't just get text back — it gets visual reference, spatial logic, design intelligence encoded as retrievable knowledge.

It simulates sight. Not literally — the agent still operates in language and coordinates — but functionally, the embedded knowledge base gives it design intuition it wouldn't otherwise have. It can reason about space not because it sees it, but because it has internalized enough spatial knowledge to make informed decisions.

A library with a specialized search engine, stocked with the visual and spatial intelligence the agents need to not just model geometry, but to *think architecturally* about what they're building. The difference between a cook who follows recipes mechanically and one who understands flavor, texture, and composition.

---

## The Full Kitchen, From the Street

Zoom out. Here's the whole thing, from the road to the plate:

A prompt arrives — the client's order. It travels as packets over WiFi, across the internet, from the user to Anthropic's building. The brain thinks. It sends the plan back down the road, across the internet, to your building.

Claude Code receives it in the terminal — backstage. It reads the CLAUDE.md briefing (the map), checks the .claude keychain (the equipment), and decides which station handles this order. The orchestrator agent — chef at the pass — reads the ticket and assigns tasks.

A specialized agent gets activated. It puts on its uniform in the cloakroom (specialist system prompt), picks up its station tools (MCP-connected Rhino, or file system, or whatever it needs), and starts working. If it needs knowledge, it queries the RAG pantry — the indexed library with the embedded search engine. If it needs to verify spatial logic, it pulls reference from the vectorized knowledge base that gives it design intuition.

Commands flow room-to-room through localhost — the Python worker translates them into Rhino operations, Rhino computes, results come back. Fast. No internet round trip for execution.

When the dish is ready, the result flows back — through the orchestrator, through Claude Code, across the internet to Anthropic, back to the user's screen. The client gets their plate.

And the whole thing is logged. Every commit in Git, every branch explored, every pull request reviewed. The shared plan room on GitHub preserves the full history so anyone — human or agent — can walk in tomorrow and know exactly how this kitchen was built, what was cooked, and why.

---

## Why We Built All of This

Not because it was the plan.

Because we kept losing context and wasting time. Because the handoffs got longer than the work. Because two people passing documents through a window couldn't keep up with the speed of the ideas. Because every new session started from zero and made contradictory choices.

So we wrote a logbook. Then a shared plan room. Then a briefing. Then we gave the agents tools. Then specialized roles. Then a library. Then eyes.

Each layer was a response to a specific pain point. Not an architecture imposed from above, but an infrastructure grown from below — from the friction of actually trying to design a building with AI agents that forget everything the moment you look away.

You didn't set out to build a digital kitchen. You set out to design a warehouse in Shanghai and then a hundred-kilometer city along Lake Geneva, and the kitchen built itself around the need.

That's how the best architecture works, anyway. The building is the residue of the process.
