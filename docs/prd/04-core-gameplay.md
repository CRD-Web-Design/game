# 04 — Core Gameplay

The moment-to-moment feel. Free-roam sandbox: the player is dropped into Atherton with a weapon wheel and no
objectives. Everything below serves walking, looking, entering, shooting, and dealing with what follows.

---

## Player character

An unnamed adult. No character creator in v1 — first-person with visible hands and (stretch) body-awareness
legs/shadow. No voice.

## Movement model

Grounded, weighty, modern-FPS standard. Reference feel: somewhere between GTA V first-person (weight) and
Call of Duty (responsiveness) — closer to the former. This is a town, not an arena.

| Parameter | Value (initial tuning) |
|---|---|
| Walk | 1.6 m/s (real-world pedestrian — the map is 1:1, speeds must be too) |
| Jog (default) | 3.4 m/s |
| Sprint | 6.0 m/s, stamina-limited to ~20 s, recovers in 10 |
| Crouch | 0.9 m/s, toggle or hold (setting) |
| Jump | 1.1 m vertical reach; mantle instead wherever possible |
| Mantle/vault | Auto-detect ledges ≤ 1.2 m — walls, fences, yard gates. Essential in terraced-street geography |
| Fall damage | From > 3 m, scaling; lethal ~12 m |

No slide, no wall-run, no double jump. Ladders and stairs as found in the world.

**Camera:** 90° default horizontal FOV (75–110 configurable), head-bob subtle and toggleable, motion-blur
off by default.

## Gunplay feel

Targets, not simulation-grade ballistics — but grounded, not arcade:

- **Hip fire vs ADS** with distinct spread cones per weapon ([05](05-weapons.md) has the tables).
- **Recoil** as deterministic per-weapon patterns + small random jitter — learnable, mostly vertical.
- **Hitscan** under 50 m for bullets, projectile simulation beyond (and always for thrown weapons). The
  player will rarely notice; the CPU will.
- **Penetration:** thin materials (fence panels, car doors, plasterboard interior walls) pass reduced-damage
  shots per the weapon's penetration class. Brick and stone do not. Pub tables flip and stop pistol rounds —
  improvised cover is a core interior behaviour.
- **Locational damage** on NPCs: head/torso/limb multipliers, limb hits affect movement.
- **Audio propagation:** gunshots are loud. Indoor shots muffle to the street; outdoor shots alert NPCs in a
  ~150 m radius and are reported to the police response director ([06](06-npcs-and-ai.md)).

## Player health

Regenerating two-segment model: a regenerating **resilience** segment (~40%) over a non-regenerating
**health** core restored by first-aid kits found in plausible places (pub first-aid boxes behind the bar, the
chemist, the ambulance). Keeps the sandbox forgiving without making the player unkillable; death = respawn at
a hospital/clinic spawn with weapons retained (it's a sandbox, not a roguelike).

## The sandbox loop

No missions. The loop is intrinsic:

```
explore → recognise → enter → interact/escalate → consequence → evade/reset → explore
```

Systems that make the loop hold up, in priority order:

1. **The world reacting** — NPC panic, police escalation, the town emptying and re-filling. The consequence
   engine is [06](06-npcs-and-ai.md) and it is most of the game.
2. **Interiors as reward for curiosity** — every enterable building has something to look at, pick up, or use
   ([07](07-interiors.md)).
3. **Interactables**, tiered by cost:
   - v1: doors, light switches, taps of both kinds (beer and water), jukebox, pool table (ball physics, no
     full game), fruit machine, TVs, tills (open, cash spills), sittable seats.
   - Later: playable pool, dartboard minigame, tram/bus boarding, shop purchases with an economy.
4. **Physics props** — glasses, bottles, stools, market stalls: enough clutter that a bar fight trashes a bar
   convincingly. Budgeted per interior (~60 active bodies cap per interior, pooled).
5. **Wanted decay and reset** — evading the police response long enough decays the wanted state; a "sleep it
   off" bench/bed interaction hard-resets the world state. World damage (glass, props) resets on a cell-reload
   cadence; bodies are removed by ambulance NPC crews over time.

## Save model

Single free-roam world state. Autosave on quit + manual save slots. Saved: player position, loadout, time of
day, wanted state (zeroed on save — saves are a reset valve, keeping the persistence budget small). Not saved:
prop-level world damage.

## Difficulty

One default tune. Accessibility toggles instead of difficulty tiers: aim assist (off by default on
mouse), damage-taken scalar, stamina off, police-aggression scalar. See [10 — UI/UX](10-ui-ux.md).

## Session shape targets

- Cold boot → playing: < 20 s on target hardware.
- No forced tutorial. A single contextual hint layer (first pickup, first wanted star) that can be disabled.
- 20 minutes of aimless wandering should surprise the player at least twice (a train, a matchday crowd, rain
  starting, a pub argument spilling out) — the ambient event scheduler in [06](06-npcs-and-ai.md) owns this.

## Acceptance criteria

1. Traversal of the full map on foot, no missions, is possible on day one of M1 (grey-box) and never breaks after.
2. A/B footage of walk/jog/sprint against GTA V first-person reads as comparable weight to reviewers.
3. Firing every weapon indoors and out produces distinct audio propagation and NPC reaction radii.
4. The player can enter a pub, start a fight with a pool cue, escalate to a firearm, survive tier-2 police
   response, evade, decay wanted, and return to a re-normalised world — the whole loop, no scripting.

---

**Previous:** [03 — World and map](03-world-and-map.md) · **Next:** [05 — Weapons](05-weapons.md) · **Index:** [PRD README](README.md)
