# 00 — Executive Summary

## The pitch

An open-world, first-person sandbox shooter where the map is **Atherton, Greater Manchester** — not a
fictionalised version of it, the actual town, built 1:1 from survey data. Real streets at real distances, real
elevation, real buildings on their real footprints. You can walk out of Hag Fold station, up through the estate,
across the railway, into the Jolly Nailor on Market Street, and every one of those distances is the distance it
is in life.

Free-roam only. No campaign, no missions, no progression gates. The town, a weapon wheel, a populated world
that reacts to you, and no instructions.

## Why this, specifically

Open-world shooters invent their cities — Los Santos, Night City, Liberty City. The invention is mostly a legal
and creative convenience, and something is lost in it: the specific texture of a *real* place, where the pub is
where the pub is because of where the pit used to be. Atherton is a former mining town of about 22,000 that
grew along the old Bolton–Leigh road, and it has 300 years of visible history layered into a walkable 12 km².

It is also small enough that 1:1 is actually achievable by a very small team, which is the point — see below.

## What this project actually is

**A personal test project.** Unpublished, single developer, AI-assisted. The stated goal is "to see what can be
done." That framing drives real decisions throughout this document:

- The roadmap leads with a **fast path to something playable**, not a 16-month studio schedule (though one is
  costed in [11](11-milestones-and-roadmap.md) for reference).
- Licensing, age rating and notarisation obligations are **noted but not scheduled** — they attach to
  distribution, and there is none. See [data sources](../reference/data-sources-and-licences.md).
- Fidelity targets are set by what **one person plus generated content** can plausibly reach, with procedural
  generation doing the heavy lifting and hand-authoring reserved for about 40 buildings.

## Hard constraints

| | |
|---|---|
| **Platform** | macOS on Apple Silicon (M1 and later). This is the binding constraint on everything technical. |
| **Engine** | Godot 4.5, Forward+ renderer, Metal backend — see [ADR-0001](../adr/0001-engine-godot-4.md) |
| **Performance floor** | Base M1, 8 GB unified memory, 1080p, 60 fps |
| **Playable area** | ≈ 12.2 km² (3.34 km N–S × 3.64 km E–W) |
| **Mode** | Single-player, offline |

## Content and the two lines that don't move

This is an adult game depicting gun violence in a real, named town, including against civilian NPCs — the
GTA model, explicitly requested. Two constraints hold regardless of the project ever shipping, because they
aren't about ratings boards:

1. **No child characters exist in the game.** Not as targets, not as bystanders, not at all. This is also
   standard practice across the genre for the same reason.
2. **No real living person is modelled, named, or depicted.** NPCs are generated composites.

A third question — whether real business names are appropriate in a *published* build — is deferred, because
for an unpublished personal project it doesn't arise. It's recorded in
[12-risks-legal-compliance.md](12-risks-legal-compliance.md) so that if the project's status ever changes, the
decision gets made deliberately.

## Requirements traceability

Every requirement stated in the brief, mapped to where it is specified.

| # | Requirement | Specified in |
|---|---|---|
| 1 | First-person shooter | [04 — Core gameplay](04-core-gameplay.md) |
| 2 | High quality | [08 — Technical architecture](08-technical-architecture.md), [09 — Art and audio](09-art-and-audio-direction.md) |
| 3 | Set in Atherton, near Wigan | [02 — Setting](02-setting-atherton.md), [03 — World and map](03-world-and-map.md) |
| 4 | Research the real area | [02 — Setting](02-setting-atherton.md) + the three [reference dossiers](../reference/) |
| 5 | Select between different weapons | [05 — Weapons](05-weapons.md) |
| 6 | Landmarks — pubs, shops — accessible and enterable | [07 — Interiors](07-interiors.md), [landmark register](../reference/atherton-landmark-register.md) |
| 7 | NPC characters around the map | [06 — NPCs and AI](06-npcs-and-ai.md) |
| 8 | Modern day, town exactly as it looks in real life | [03 — World and map](03-world-and-map.md) |
| 9 | 1:1 geographic accuracy | [03 — World and map](03-world-and-map.md), [ADR-0002](../adr/0002-map-data-pipeline.md) |
| 10 | Sandbox / free-roam, no campaign | [04 — Core gameplay](04-core-gameplay.md) |
| 11 | Can shoot anyone, GTA-style | [06 — NPCs and AI](06-npcs-and-ai.md) |
| 12 | Playable on an Apple Silicon MacBook | [08 — Technical architecture](08-technical-architecture.md) |
| 13 | More features later — extensible | [11 — Milestones](11-milestones-and-roadmap.md), [13 — Open questions](13-open-questions.md) |

## The honest risk assessment

Three things could sink this, in order of likelihood:

1. **Scope.** 12 km² of hand-verified real town is a *lot* for one person. Mitigation: procedural generation
   for ~5,000 buildings, and a milestone plan that produces something playable at week 6 rather than month 12.
2. **Crowd performance on an 8 GB M1.** 120 NPCs with schedules, pathfinding and physics is the single hardest
   technical target in this document, and Godot is weaker here than Unity. This is deliberately tested at M2,
   early, while changing engines would still be cheap.
3. **Map accuracy.** The research behind the registers is web-sourced and unverified. Building 5,000 wrong
   buildings is expensive. Mitigation: local review before M3, and a grey-box pass at M1 that surfaces errors
   while everything is still cheap to move.

---

**Next:** [01 — Vision and pillars](01-vision-and-pillars.md) · **Index:** [PRD README](README.md)
