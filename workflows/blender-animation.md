# Workflow: Blender Animation Pipeline

Build animated videos in Blender using MCP router with agent teams.

## When to use
- Animated video production via Blender MCP
- Multi-instance parallel builds (assets on separate instances, then video animation)
- Kitchen analogy animation suite or similar short-form explainer videos

## Required inputs
- Animation spec (storyboards, visual style, character design)
- Blender instances running with MCP addon on specified ports
- Router MCP configured in .mcp.json with BLENDER_INSTANCES

## Pre-flight checklist
- [ ] Blender instances launched and MCP addon running on specified ports
- [ ] Router MCP server running (tools/blender/blender_router_mcp.py)
- [ ] `blender_list_instances()` returns all expected instances as connected
- [ ] Test `blender_execute_code` on each instance (create cube, verify, delete cube)
- [ ] Test Freestyle rendering (render 1 frame with EEVEE + Freestyle 2px ON)
- [ ] If Freestyle fails: document fallback in BUILD_LOG.md
- [ ] Output directories created (assets/, renders/, learnings/)

## Phase 0: Smoke Test
1. Verify MCP connections to all instances
2. Test code execution on each instance (create + delete test cube)
3. Test Freestyle render (1 frame, EEVEE + Freestyle 2px)
4. Create output directory structure
5. If ANY test fails: stop, log error, do not proceed

## Phase 1: Assets (parallel)
Spawn teammates on separate Blender instances:
- House Set Builder (environment, rooms, props)
- Character Builder (blobs, animations, actions)
- Exterior/Camera Rigs (outdoor scene, camera setups, lighting)

Each teammate:
1. Reads the animation spec (law)
2. Reads blender-playbook.md (doctrine)
3. Builds assigned assets following doctrine rules
4. Saves periodically to output directory
5. Writes manifest file (collections, object counts, missing elements)
6. Writes raw learnings to output/kitchen_animation/learnings/

## Phase 1 → 2 Transition
1. Verify all .blend asset files exist
2. Read manifests to confirm coverage
3. Transfer assets between instances via file append or blender_transfer_geometry
4. Clear test objects, prepare clean scenes for video work
5. Update BUILD_LOG.md with Phase 1 results

## Phase 2: Video Animation (parallel, batched by priority)
Each video teammate:
1. Links/appends required assets from Phase 1 .blend files
2. Animates per storyboard (spec has frame-by-frame breakdowns)
3. Renders PNG sequence at draft resolution (960x540)
4. Saves the animated .blend file (for full-resolution re-render later)
5. Writes raw learnings

Batch by priority — most important videos first. Use all available instances.

## Phase 3: Knowledge Distillation (PM only, after all videos)
1. Read all per-agent learnings from output/kitchen_animation/learnings/
2. Distill into topic files in .claude/agents/knowledge/:
   - learnings-blender-materials.md
   - learnings-blender-animation.md
   - learnings-blender-rendering.md
   - learnings-blender-mcp.md
3. Update blender-playbook.md doctrine if universal principles emerged
4. Update LEARNINGS.md with Blender-specific discoveries
5. Write distillation summary to BUILD_LOG.md

## Error handling
- MCP connection failure: retry 3x with 30s wait, then skip and log
- Freestyle render failure: disable Freestyle, continue without outlines
- Character linking failure: build simplified blob directly in scene (fallback in every video prompt)
- Never get stuck: 10-minute timeout on any single retry loop, then skip and move on

## Expected output
- .blend asset files (house, characters, exterior)
- PNG sequences per video in output/kitchen_animation/renders/video_NN/
- Animated .blend files per video (saved after render)
- BUILD_LOG.md with status, issues, recommendations
- Per-agent learnings files
- Updated knowledge system files (after Phase 3)

## History
- 2026-03-24: Created for overnight kitchen animation build
