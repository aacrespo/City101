# Phase 1: Sprite Rendering — All Accounts, All Animations
**Status:** [A04_ACTIVE]
**Execution:** Single session with Blender MCP
**Estimated time:** 3-4 hours (mostly render time)
**Prerequisites:** Blender open with MCP running on port 9876

---

## Context

You are rendering the complete animation sprite set for the Kitchen analogy presentation. The character model has been updated with:
- **Arm shape keys**: Celebrate, Wave, Reach, Point (plus Basis for idle)
- **Eye shape keys**: happy, sad, angry, wide, squint, half_closed, blink, look_up, look_down, raised
- All saved in `cairn_final_all_emotes v.2.blend`

You need to render **21 animations × 5 account personas = 105 animation sequences**, all with **transparent backgrounds**.

---

## Read first
- `output/kitchen_animation/STORYBOARD.md` — what these sprites are for
- `state/pm/kitchen-animation/master_plan.md` — project context
- `design_system/SPEC.md` — color palette

## Source files

| Account | Color | .blend file |
|---------|-------|------------|
| **Cairn** (Andrea CLI) | Warm gold `#c9a84c` body | `cairn_final_all_emotes v.2.blend` (BASE — has arms + eyes) |
| **Lumen** (Andrea school) | Bright yellow | `lumen_final.blend` |
| **Meridian** (Henna school) | Blue `#5b8fa8` | `meridian_final.blend` |
| **Cadence** (Henna personal) | Purple | `cadence_final.blend` |
| **Nova** (Henna Max) | Pink/coral `#FF7F7F` | `nova_final.blend` |

All at: `output/kitchen_animation/assets/`

**IMPORTANT**: The arm rig and eye shape keys were built in the Cairn file. The other account files do NOT have them yet. You must:
1. Open each account file
2. Replace the eyes with the emote-ready eyes from Cairn (append from `cairn_final_all_emotes v.2.blend`)
3. Replace/update the arms with the shape-keyed arms from Cairn
4. Adjust colors to match that account's palette
5. Then render

---

## Render settings

```python
# Apply to every render
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.render.resolution_percentage = 100
scene.render.film_transparent = True  # TRANSPARENT BACKGROUND
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'  # include alpha channel
```

**Camera**: Keep the existing iso 3/4 camera angle (same as all previous renders).

---

## The 21 animations

Each animation is a combination of arm shape keys, eye shape keys, and optional body movement (via keyframed location/rotation on Cairn_Root).

### Animation definitions

```python
ANIMATIONS = {
    # name: {frames, eye_keys, arm_keys, body_motion, bounce, fps}

    'idle': {
        'frames': 48,
        'eyes': {'Basis': 1.0},  # neutral, with occasional blink
        'arms': {'Basis': 1.0},  # tucked
        'body': 'gentle_bob',     # subtle Y translation ±0.01
        'bounce': True,
        'fps': 10,
        'notes': 'Insert blink at frames 20-24 (blink shape key 0→1→0)'
    },
    'walk': {
        'frames': 24,
        'eyes': {'Basis': 1.0},
        'arms': {'Basis': 1.0},  # arms stay tucked while walking
        'body': 'walk_cycle',     # translate X + bob + leg motion
        'bounce': False,
        'fps': 12,
        'notes': 'Body moves forward, legs alternate. Loop seamlessly.'
    },
    'typing': {
        'frames': 48,
        'eyes': {'squint': 0.3, 'look_down': 0.2},  # focused
        'arms': {'Reach': 0.6},  # arms forward on keyboard
        'body': 'slight_bob',
        'bounce': True,
        'fps': 10,
        'notes': 'Arms do small alternating motions (Reach oscillates 0.5-0.7)'
    },
    'thinking': {
        'frames': 48,
        'eyes': {'squint': 0.5, 'look_up': 0.3},
        'arms': {'Basis': 1.0},  # one arm could do chin touch but keep simple
        'body': 'gentle_bob',
        'bounce': True,
        'fps': 8,
        'notes': 'Slow, contemplative. Eyes shift up slightly.'
    },
    'building': {
        'frames': 48,
        'eyes': {'squint': 0.2},  # focused
        'arms': {'Reach': 0.7},
        'body': 'active_bob',
        'bounce': True,
        'fps': 10,
        'notes': 'Active arm movement — Reach oscillates 0.5-0.9, alternating L/R'
    },
    'carrying': {
        'frames': 48,
        'eyes': {'Basis': 1.0},
        'arms': {'Reach': 0.5},  # arms forward holding something
        'body': 'slow_walk',
        'bounce': False,
        'fps': 10,
        'notes': 'Both arms forward, body moves slowly. Careful posture.'
    },
    'reading': {
        'frames': 48,
        'eyes': {'squint': 0.2, 'look_down': 0.4},
        'arms': {'Reach': 0.4},  # arms forward holding book
        'body': 'still_bob',
        'bounce': True,
        'fps': 8,
        'notes': 'Very subtle movement. Eyes slightly down. Studious.'
    },
    'searching': {
        'frames': 48,
        'eyes': {'wide': 0.3, 'look_up': 0.2},
        'arms': {'Reach': 0.5},
        'body': 'look_around',  # slight rotation left/right
        'bounce': True,
        'fps': 10,
        'notes': 'Head/body turns slightly. Looking for something.'
    },
    'sending': {
        'frames': 24,
        'eyes': {'Basis': 1.0},
        'arms': {'Point': 0.8},  # arm extends out
        'body': 'push_forward',
        'bounce': False,
        'fps': 12,
        'notes': 'Arm extends, releases. Quick motion.'
    },
    'listening': {
        'frames': 48,
        'eyes': {'wide': 0.2, 'raised': 0.3},
        'arms': {'Basis': 1.0},
        'body': 'attentive_tilt',  # slight lean forward
        'bounce': True,
        'fps': 8,
        'notes': 'Attentive pose. Still but present.'
    },
    'celebrate': {
        'frames': 36,
        'eyes': {'happy': 1.0},
        'arms': {'Celebrate': 1.0},
        'body': 'bounce_high',  # bigger Y bounce
        'bounce': False,
        'fps': 12,
        'notes': 'Arms go up over ~8 frames, hold, then down. Eyes happy throughout.'
    },
    'frustration': {
        'frames': 24,
        'eyes': {'angry': 0.7, 'squint': 0.3},
        'arms': {'Basis': 1.0},  # arms stay down, frustrated
        'body': 'shake',  # small X oscillation
        'bounce': True,
        'fps': 10,
        'notes': 'Tense little shake. Could add slight arm raise and drop.'
    },
    'greeting': {
        'frames': 24,
        'eyes': {'happy': 0.7, 'wide': 0.3},
        'arms': {'Wave': 1.0},  # right arm waves
        'body': 'gentle_bob',
        'bounce': True,
        'fps': 12,
        'notes': 'Wave right arm only. Friendly eyes.'
    },
    'surprise': {
        'frames': 18,
        'eyes': {'wide': 1.0},
        'arms': {'Celebrate': 0.5},  # arms go slightly up in shock
        'body': 'jump_back',  # small backward hop
        'bounce': False,
        'fps': 12,
        'notes': 'Quick jump, eyes go wide, arms fly up slightly.'
    },
    'alert': {
        'frames': 18,
        'eyes': {'wide': 0.8, 'raised': 0.5},
        'arms': {'Point': 0.4},  # slight arm raise
        'body': 'snap_attention',
        'bounce': False,
        'fps': 12,
        'notes': 'Snaps to attention. Quick transition.'
    },
    'success': {
        'frames': 24,
        'eyes': {'happy': 1.0},
        'arms': {'Celebrate': 0.8},
        'body': 'nod_bounce',
        'bounce': False,
        'fps': 10,
        'notes': 'Like celebrate but calmer. Satisfied nod + arms up.'
    },
    'spawn': {
        'frames': 12,
        'eyes': {'blink': 1.0},  # starts with blink, opens
        'arms': {'Basis': 1.0},
        'body': 'pop_in',  # scale from 0 to 1
        'bounce': False,
        'fps': 12,
        'notes': 'Character pops in from nothing. Scale 0→1, eyes blink→open.'
    },
    'despawn': {
        'frames': 10,
        'eyes': {'blink': 1.0},  # closes eyes
        'arms': {'Basis': 1.0},
        'body': 'pop_out',  # scale from 1 to 0
        'bounce': False,
        'fps': 12,
        'notes': 'Reverse of spawn. Eyes close, scale 1→0.'
    },
    'run': {
        'frames': 12,
        'eyes': {'wide': 0.3},
        'arms': {'Basis': 1.0},
        'body': 'run_cycle',  # fast walk with bigger bob
        'bounce': False,
        'fps': 16,
        'notes': 'Faster walk. Bigger bob, quicker legs.'
    },
    'sleep': {
        'frames': 72,
        'eyes': {'half_closed': 1.0},
        'arms': {'Basis': 1.0},
        'body': 'slow_breathe',  # very slow Y scale pulse
        'bounce': True,
        'fps': 6,
        'notes': 'Very slow breathing motion. Eyes half closed. Peaceful.'
    },
    'receive_info': {
        'frames': 24,
        'eyes': {'wide': 0.5, 'look_up': 0.3},
        'arms': {'Reach': 0.3},  # slight arm raise to receive
        'body': 'lean_back',  # slight backward lean then forward
        'bounce': False,
        'fps': 10,
        'notes': 'Something arrives. Lean back slightly, then process.'
    },
}
```

---

## Execution steps

### Step 1: Set up transparent rendering
Open `cairn_final_all_emotes v.2.blend`. Configure render settings (transparent, RGBA, 512×512). Remove or hide the Ground object.

### Step 2: Render Cairn (base character)
For each of the 21 animations:
1. Set eye shape keys per the definition
2. Set arm shape keys per the definition
3. Keyframe body motion (location/rotation on Cairn_Root) across the frame range
4. Render all frames to: `output/kitchen_animation/renders/cairn/{animation_name}/frame_NNNN.png`

### Step 3: Render other accounts
For each account (Lumen, Meridian, Cadence, Nova):
1. Open their .blend file
2. Append the arm meshes (with shape keys) and eye meshes (with shape keys) from `cairn_final_all_emotes v.2.blend`
3. Replace the existing simple arms/eyes with the emote-ready versions
4. Match the account's body color
5. Configure transparent rendering
6. Render all 21 animations to: `output/kitchen_animation/renders/{account_name}/{animation_name}/frame_NNNN.png`

### Step 4: Extract key frames for kitchen HTML sprites
After all full animations are rendered, copy key frames to a sprites folder:
```
output/kitchen_animation/sprites/{account}/
├── idle_01.png, idle_02.png          (2 frames for bob)
├── walk_01.png ... walk_04.png       (4 key frames)
├── typing_01.png, typing_02.png
├── celebrate_01.png
├── wave_01.png
├── reach_01.png
├── point_01.png
├── sad_01.png
├── thinking_01.png
├── spawn_01.png ... spawn_03.png
├── despawn_01.png, despawn_02.png
└── neutral_01.png
```

### Step 5: Also render grey (desaturated) variants for Cairn
For Scene 1 of the kitchen animation, Claude enters grey (no context).
- Desaturate the Cairn body material to greyscale
- Render: idle (2 frames) + walk (4 frames) as grey
- Save to: `output/kitchen_animation/sprites/cairn_grey/`
- Then render 3-4 transition frames: grey → gold (interpolate material color)
- Save to: `output/kitchen_animation/sprites/cairn_transition/`

---

## Output structure
```
output/kitchen_animation/
├── renders/                    ← full animation sequences (for GIFs)
│   ├── cairn/
│   │   ├── idle/frame_0001.png ... frame_0048.png
│   │   ├── walk/frame_0001.png ... frame_0024.png
│   │   ├── typing/...
│   │   └── ... (21 folders)
│   ├── lumen/
│   │   └── ... (21 folders)
│   ├── meridian/
│   │   └── ...
│   ├── cadence/
│   │   └── ...
│   └── nova/
│       └── ...
├── sprites/                    ← key frames for HTML (extracted from renders)
│   ├── cairn/
│   ├── cairn_grey/
│   ├── cairn_transition/
│   ├── lumen/
│   ├── meridian/
│   ├── cadence/
│   └── nova/
└── gifs/                       ← generated by tools/export/png_to_gif.py after renders
```

## After rendering
Run the GIF tool on all renders:
```bash
python3 tools/export/png_to_gif.py output/kitchen_animation/renders/cairn/ --all --fps 10 --bounce
```
Repeat for each account. GIFs go to `output/kitchen_animation/gifs/{account}/`.

---

## Blender MCP tips
- Use `bpy.ops.render.render(write_still=True)` per frame, not animation render (more control)
- Hide Ground object: `bpy.data.objects['Ground'].hide_render = True`
- `scene.render.film_transparent = True` for alpha
- When appending objects from another .blend, use `bpy.data.libraries.load()`
- Keyframe shape keys: `key_block.value = X` then `key_block.keyframe_insert(data_path='value', frame=N)`
- Keyframe location: `obj.location.z = X` then `obj.keyframe_insert(data_path='location', frame=N)`
- **DO NOT modify or save over the source .blend files.** Work in copies or temporary scenes.
- sRGB color conversion is required for correct colors (see kitchen_set_build_v2.md for the function)

## Verification
After rendering, check:
- [ ] All PNGs have transparent backgrounds (alpha channel present)
- [ ] 21 animations × 5 accounts = 105 folders
- [ ] Frame counts match definitions
- [ ] Colors match each account persona
- [ ] No grey background bleeding in renders
- [ ] Sprites folder has key frames extracted
- [ ] Grey + transition variants exist for Cairn
