# 05 — Weapons

The arsenal, the selection UX, and the data model. Requirement: the player **selects between different
weapons**; this is the core verb after movement.

---

## Design stance

Modern-day UK-plausible, not military fantasy. The tone is *illicit and improvised* — the weapons you'd
plausibly find in a Northern town's black market and behind its bars, not a NATO armoury. This is flavour, not
simulation: it keeps the arsenal coherent with the setting (Pillar 1) while still covering every classic FPS
weapon role.

No attachments system in v1. No weapon degradation. Ammo by calibre class, found/looted.

## The wheel

- **Hold `Tab` / gamepad `Y`:** radial wheel, time dilates to 20%, 8 slots, mouse/stick to select.
- **Tap:** quick-swap to previous weapon.
- **Scroll / d-pad:** cycle within slot category.
- Each slot holds one carried weapon of its class; picking up a second swaps and drops (no infinite backpack —
  keeps loadouts characterful).

| Slot | Class |
|---|---|
| 1 | Fists / melee |
| 2 | Sidearm |
| 3 | Shotgun |
| 4 | SMG / machine pistol |
| 5 | Rifle |
| 6 | Marksman |
| 7 | Thrown |
| 8 | Special / future (empty in v1 — reserved for later features) |

## Arsenal v1 — 15 weapons

Names are generic/fictional (no real manufacturer marks — they'd be wrong for the setting anyway).

### Melee

| Weapon | Damage | Speed | Notes |
|---|---|---|---|
| Fists | 10 | fast | Always available |
| Snooker cue | 25 | fast | Found in every pub; breaks after ~6 hits into a sharper half |
| Cricket bat | 35 | med | Sports shop, sheds |
| Crowbar | 30 | med | Also opens boarded doors/crates — the utility melee |
| Wheel brace | 28 | med | Cars, garages |

### Firearms

Columns: damage per round (torso, 10 m) · RPM · effective range (m, start of falloff) · magazine · reload (s) ·
penetration class (0 none / 1 thin / 2 board+car / 3 brick-chip).

| Weapon | Dmg | RPM | Range | Mag | Reload | Pen | Role |
|---|---|---|---|---|---|---|---|
| 9 mm semi-auto pistol | 26 | 300 (semi) | 35 | 15 | 1.8 | 1 | Baseline sidearm |
| .38 revolver | 42 | 150 (semi) | 30 | 6 | 3.2 | 1 | Heavy sidearm, loud |
| Machine pistol | 18 | 900 | 20 | 20 | 2.2 | 1 | Spray sidearm, brutal recoil |
| Side-by-side shotgun | 12×9 pellets | 90 | 15 | 2 | 2.6 | 0 | The farm gun; devastating close |
| Pump-action shotgun | 10×8 | 70 | 18 | 6 | 0.7/shell | 0 | Sustained close-quarters |
| 9 mm compact SMG | 22 | 750 | 40 | 30 | 2.4 | 1 | Mid-range automatic |
| Bolt-action hunting rifle | 90 | 45 | 250 | 5 | 3.0 | 2 | Scoped; the long option |
| Semi-auto carbine | 34 | 400 (semi) | 120 | 20 | 2.5 | 2 | All-rounder |
| Marksman rifle | 65 | 120 (semi) | 300 | 10 | 2.8 | 3 | Rare spawn; apex weapon |

### Thrown

| Weapon | Effect | Notes |
|---|---|---|
| Brick | 20 impact, physics | Infinite in the right alleys; breaks windows — the humble entry tool |
| Molotov | Fire pool 4 m, 8 s | Fire propagates to props, not structural buildings (perf + taste); heavy police escalation |
| Flashbang | 4 s blind/deafen radius 8 m | NPC and player both affected |

## Handling data model

Each weapon is a Godot `.tres` resource — designers (or the agent) tune without touching code:

```
WeaponDef:
  id, display_name, slot, mesh, anim_set, audio_set
  damage, rpm, mode (semi/auto/pump/bolt), mag_size, reserve_max
  reload_s, reload_style (mag/shell/cylinder)
  spread_deg: { hip_stand, hip_move, ads_stand, ads_move }
  recoil: { pattern: Curve2D, recovery_s, ads_multiplier }
  range_falloff: Curve   # damage multiplier over distance
  penetration_class: 0-3
  loudness_radius_m     # drives NPC alert + police reporting
  rarity_tier           # drives spawn tables
```

**Spread baselines** (degrees, half-angle): pistol hip-stand 2.2 / ADS 0.5; SMG hip 3.0 / ADS 1.0; shotgun
fixed cone 5.5; rifles hip 4.0 / ADS 0.15. Movement multiplies ×1.6, crouch ×0.8.

## Acquisition

No shops selling guns (it's England). Weapons enter the sandbox as:

- **Placed spawns** in plausible locations — crowbar in the rail depot, cricket bat in the sports shop,
  side-by-side at the farm on the map edge, cue in every pub.
- **Police drops** — escalation tiers carry period-appropriate kit ([06](06-npcs-and-ai.md)): baton →
  sidearm → carbine at armed-response tier. Fighting the escalation is the main firearms faucet, which is a
  deliberate difficulty loop: better guns require surviving harder response.
- **Rare fixed spawns** for the marksman rifle (one location, rotates weekly by calendar).
- **Debug/sandbox menu** (this is a personal test build — a give-all console exists and isn't hidden).

## Audio identity

Each firearm needs a distinct report; the town's acoustics do half the work — see [09](09-art-and-audio-direction.md).
Interior shots ring; the terraced streets of Howe Bridge should echo differently from the open Tesco car park.

## Acceptance criteria

1. All 15 weapons selectable via wheel, quick-swap and cycle, with correct slotting.
2. Per-weapon recoil patterns reproducible in an automated test (fire 30 rounds scripted → screenshot spread
   matches stored reference within tolerance).
3. Weapon stats live-reload from `.tres` edits without restart.
4. Shotgun vs plasterboard vs brick behaves per penetration table in a test scene.
5. A blindfolded listener can distinguish revolver / pump / SMG / bolt rifle by audio alone.

---

**Previous:** [04 — Core gameplay](04-core-gameplay.md) · **Next:** [06 — NPCs and AI](06-npcs-and-ai.md) · **Index:** [PRD README](README.md)
