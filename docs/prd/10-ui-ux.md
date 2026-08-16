# 10 — UI and UX

HUD, menus, map, input, accessibility. Principle: the town is the interface — UI exists to get out of its way.

---

## HUD

Minimal, corner-anchored, fades when idle:

| Element | Position | Behaviour |
|---|---|---|
| Health/resilience | Bottom-left | Two-segment bar ([04](04-core-gameplay.md)); hidden at full |
| Weapon + ammo | Bottom-right | Icon, mag / reserve; hidden when fists |
| Wanted tier | Top-right | 0–5 pips ([06](06-npcs-and-ai.md)); pulses while searched-for, hollow while evading |
| Crosshair | Centre | Per-weapon dynamic spread reticle; dot for melee; toggleable |
| Compass strip | Top-centre | Cardinal + street name of current road — the 1:1 map makes street names genuinely navigational |
| Contextual prompt | Centre-low | "Open", "Pick up", "Mantle" — single verb, no tutorialising |
| Hit/damage feedback | Centre | Directional damage vignette; hit-marker optional (off default) |

No minimap. Deliberate: the game is about knowing a real place, and minimaps replace place-knowledge with
icon-following. The compass strip + landmarks + the pause map cover navigation. (Revisit after playtest —
[OQ-7](13-open-questions.md).)

## Pause map

Full-screen street map of Atherton, styled like an OS/A-Z hybrid ([09](09-art-and-audio-direction.md)):

- Real street names, landmark labels for register buildings, player position + facing.
- Enterable buildings distinguished once *discovered* (walked past) — the map fills in as the player learns
  the town, which is the game's actual progression system.
- Free-placement single waypoint → compass strip tick. No pathing line, no GPS voice.
- Zoom from full-town to street level; the map is generated from the same pipeline data as the world, so it
  is never wrong.

## Menus

- **Main:** Continue / New / Load / Settings / Quit. One background: live camera slow-pan of the town at
  current time-of-day.
- **Settings:** Video (preset + individual toggles per [08](08-technical-architecture.md) scalability),
  Audio (4-bus mix: master/ambient/effects/UI), Controls (full rebind), Gameplay (FOV 75–110, head-bob,
  crosshair, hints, aim assist, camera shake), Accessibility (below).
- **Sandbox console** (~ key): give/teleport/time/weather/wanted/perf-HUD — a first-class feature in a test
  build ([08](08-technical-architecture.md)).

## Input

| | |
|---|---|
| Keyboard + mouse | Primary. WASD + standard FPS bindings; weapon wheel on hold-Tab ([05](05-weapons.md)) |
| Gamepad | Full support day one (a MacBook with a pad is a common play setup). Standard twin-stick FPS layout, wheel on hold-Y, gyro aim optional where the pad supports it |
| Trackpad | **Explicitly supported** — it's a MacBook game. Tap-to-fire mode, two-finger look sensitivity curve tuned separately from mouse. Playable, not merely functional: this is a real differentiator for the actual target device |
| Rebinding | Everything; conflicts surfaced, not blocked |

## Accessibility

Baseline commitments, not afterthoughts (they replace difficulty modes — [04](04-core-gameplay.md)):

- **Vision:** UI scale 100–200%, high-contrast HUD variant, colourblind-safe wanted/health palettes
  (verified with simulators), subtitle system for all bark/effort audio with direction indicators.
- **Motor:** hold→toggle alternatives everywhere (ADS, sprint, crouch), aim assist strength slider,
  input-repeat mash alternatives, full rebind incl. gamepad.
- **Vestibular:** FOV floor 75, head-bob/shake/blur all off-able (blur off default).
- **Cognitive:** hint layer toggle, no timed menus, pause-anywhere (single-player — always pausable).
- **Audio:** 4-bus mix, mono downmix option, visual gunshot-direction indicator option.

## First-run flow

Boot → (first run only) preset auto-detect confirm + content notice ([00](00-executive-summary.md) content
section, shown once) → main menu → New → spawn outside Atherton station, 10:00, overcast. No cinematic, no
tutorial level. The contextual hint layer handles the first pickup/mantle/wheel-use, then shuts up.

## Acceptance criteria

1. HUD-off screenshot mode produces a clean frame (photography of the town is an expected player activity).
2. A new player reaches "walking around town, entered a pub, fired a weapon" inside 3 minutes with zero
   tutorial screens.
3. Trackpad-only session (no mouse, no pad) can complete the full sandbox loop from
   [04](04-core-gameplay.md) acceptance #4.
4. All settings persist; rebinds survive updates via versioned config.
5. Colourblind simulation pass on wanted pips and health bar shows distinguishable states in all three
   common CVD types.

---

**Previous:** [09 — Art and audio](09-art-and-audio-direction.md) · **Next:** [11 — Milestones](11-milestones-and-roadmap.md) · **Index:** [PRD README](README.md)
