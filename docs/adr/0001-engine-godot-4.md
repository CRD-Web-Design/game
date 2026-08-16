# ADR-0001 — Engine: Godot 4.5

**Status:** Accepted · **Date:** 2026-08-16 · **Revisit trigger:** gate G2 failure at M2 (see Consequences)

## Context

We need an engine for an open-world FPS with these constraints, in priority order:

1. **Must run well on Apple Silicon MacBooks** (floor: base M1, 8 GB) — the user's stated platform.
2. **Solo developer + AI-assisted workflow** — the repo is developed substantially through git-driven,
   text-based tooling. Asset and scene formats that diff/merge as text are worth a great deal.
3. Open-world scale (12.2 km² streamed town), ~120 crowd NPCs, ~40 seamless interiors.
4. Personal, unpublished project — licence cost and store compliance are non-factors, but tooling friction
   is amplified (there is no build engineer).

## Decision

**Godot 4.5, Forward+ renderer on the Metal backend. GDScript for gameplay; Rust GDExtension for hot paths
(crowd tick, streaming, ballistics broadphase). Jolt physics.**

## Options considered

### Godot 4.5 — chosen

**For:**
- Native Metal rendering backend and Apple Silicon editor/export. First-class macOS citizen.
- `.tscn`/`.tres`/`.gd` are plain text — the entire project is git-diffable and directly authorable by
  agent tooling. This is the decisive workflow advantage for this specific project.
- Zero cost, no licensing, no runtime fee, no account.
- Jolt physics built in (4.4+); NavigationServer adequate for the crowd design; GDExtension gives a clean
  native-performance escape hatch in Rust.
- Small, fast editor — matters on the same 8 GB machine that is also the target device.

**Against (accepted honestly):**
- Open-world streaming is not a first-class engine feature — we build ring-streaming ourselves
  ([03](../prd/03-world-and-map.md)). Accepted: our chunked design is simple and the pipeline generates it.
- Crowd/AI at 120 agents will exceed GDScript's budget. Accepted: the Rust crowd crate is planned from the
  start, not a contingency.
- Smaller ecosystem than Unity/Unreal for ready-made FPS systems. Accepted: the systems we need are bespoke
  anyway (schedule crowds, response director, procedural town).

### Unity 6 — rejected, designated fallback

**For:** DOTS/ECS is genuinely the strongest crowd-simulation story of the three; mature asset store;
good Apple Silicon support.
**Against:** binary-leaning serialisation (text YAML scenes exist but merge badly), heavier
editor, licensing/account friction, and the 2023–24 trust damage was resolved but not forgotten. The
workflow cost for an agent-driven solo repo outweighs the crowd advantage — *unless the crowd advantage
turns out to be decisive*, which is exactly what gate G2 measures.

### Unreal Engine 5 — rejected

**For:** highest visual ceiling; best-in-class open-world tooling (World Partition).
**Against:** Lumen/Nanite are effectively unavailable/unproven on the Metal path at our scale; macOS is
visibly a second-tier platform for Epic; `.uasset` binary assets are the worst case for git + agent
workflow; editor resource demands collide with an 8 GB dev machine. The visual ceiling is unreachable solo
anyway — our art direction ([09](../prd/09-art-and-audio-direction.md)) deliberately doesn't need it.

### Web (Three.js/WebGPU) — rejected

Instantly playable and the most agent-friendly of all, but the fidelity and scale ceiling (streaming 12 km²,
120 skinned NPCs, 40 lit interiors) is below the "high quality" bar the brief sets. Right answer for a
prototype, wrong answer for the product.

## Consequences

- The M0 milestone exists specifically to prove the Godot pipeline end-to-end before deeper commitment.
- **Gate G2 (M2 crowd spike) is this ADR's formal revisit trigger.** Failure ladder: optimise (Rust crate,
  time-slicing) → reduce budget (90 NPCs, 250 m ring) → only then reopen this ADR with a costed Unity port
  assessment. The decision will be made by benchmark numbers, not preference.
- Engine version pins to 4.5.x; upgrades only between milestones.
