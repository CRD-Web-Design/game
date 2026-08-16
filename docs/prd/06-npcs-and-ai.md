# 06 — NPCs and AI

The population, its daily life, its reaction to violence, and the emergency-services response. This system is
what turns "you can shoot anyone" into a sandbox with consequence (Pillar 4) rather than a shooting gallery.

---

## Two absolute constraints

Stated once, enforced everywhere, independent of the project ever being published:

1. **No child characters exist in the game.** Not modelled, not silhouetted, not implied by prams or school
   crowds. The school run schedule event is adults-only in composition (and Atherton High School itself is
   sealed with no occupants — see the [landmark register](../reference/atherton-landmark-register.md)).
2. **No real living person is modelled, named, or depicted.** All NPCs are generated composites. Name pools
   avoid collisions with identifiable locals (generic Lancashire name distribution, no surname+role pairings
   that map to real people, e.g. no landlord NPC sharing a name with the real landlord of a modelled pub).

## Population model

Simulation at two levels:

- **Abstract layer (whole town):** a lightweight statistical population — the town "contains" ~2,000 abstract
  residents with home/work/leisure anchors and schedule archetypes. Costs almost nothing; exists so the
  concrete layer has something coherent to sample from.
- **Concrete layer (around the player):** up to **120 embodied NPCs** (+ ~40 vehicles) instantiated within a
  ~250 m ring, sampled from the abstract layer consistent with time, place and schedule. Beyond the ring they
  dissolve back into statistics. Budgets from [08](08-technical-architecture.md).

An NPC who dissolves and later re-concretises is *statistically* consistent (same archetype mix) but not
individually persistent — with one exception: **witnesses and casualties persist** for the duration of a
wanted episode, because consequence requires memory.

## Archetypes and schedules

Schedules are keyed to the real town's rhythm (see [02](02-setting-atherton.md)):

| Archetype | Weekday pattern |
|---|---|
| Commuter | 07:00–09:00 surge to Atherton & Hag Fold stations; reverse 17:00–19:00 |
| Shopworker | 08:30 arrive Market Street/precinct/Tesco; till and shelf idle loops |
| Shopper | 09:30–17:00 town-centre density, peaks Saturday and market day |
| Market trader | Market days only: stall setup 07:00, teardown 16:30 |
| Pub-goer | From 12:00 light, builds after 17:00, peaks 21:00–23:30, staggers home after |
| Pensioner | Mid-morning shops, bookies, early pub session |
| Dog-walker / jogger | Dawn & dusk, Colliers Wood and brook paths |
| Matchday crowd | Sat 14:00–17:15, routes converging on Alder House or Crilly Park |
| Night | After 00:30 the town is near-empty — taxis, a takeaway queue, the odd walker |

Interiors have occupancy curves per schedule (the Pound Pub opens 09:00; Tiki Bar fills late; Tesco staffed
open-to-close). See [07](07-interiors.md).

## Civilian behaviour states

```
IDLE/ROUTINE → CURIOUS (odd sight, distant shot ≥150 m)
            → ALARMED (nearby shot, brandished weapon, violence seen)
                ├─→ FLEE (default; route away via navmesh, favours indoors/away)
                ├─→ COWER (cornered / low-mobility archetype)
                ├─→ REPORT (dial 999 after 8–15 s if safe → feeds police director)
                └─→ [rare archetype flag] HAVE-A-GO (unarmed tackle attempt)
```

- Panic **propagates**: a fleeing crowd alarms NPCs who saw nothing. Market Street at 21:00 should empty in a
  believable cascading wave, not simultaneously.
- Interior NPCs use interior-specific behaviour: bar staff duck behind the bar (which is ballistic cover —
  [05](05-weapons.md) penetration rules), patrons bottleneck at doors, someone pulls the fire alarm.
- Casualties: wounded NPCs crawl, call for help; ambulance crews (see below) collect them. Bodies persist
  through the wanted episode, then are cleaned up on decay/reset.

## Police response — the five tiers

A **response director** (single global system) receives reports (999 calls, heard shots, officer sightings),
maintains an evidence-weighted threat estimate, and escalates. Response originates physically — vehicles
actually depart from Flapper Fold Lane and arrive by road; nothing teleports in. Distance and the road network
therefore matter: trouble in Hindsford buys more time than trouble opposite the station.

| Tier | Trigger (typical) | Response | Kit |
|---|---|---|---|
| 1 | Brawl, brandishing, vandalism | 1 response car, 2 officers | Baton, PAVA; arrest attempt |
| 2 | Shots fired, no casualties | 2–3 cars, area search | Sidearms drawn at threat |
| 3 | Casualties confirmed | 4+ units, ambulance staging, foot pursuit | Sidearms, dog unit |
| 4 | Sustained shooting / multiple casualties | Armed response vehicles, cordon at chokepoints (rail crossings, A-road junctions) | Carbines, shields |
| 5 | Prolonged tier-4 defiance | Full cordon of the town centre, helicopter (audio + searchlight), evacuation of interiors | Marksmen overwatch |

- **Evasion:** line-of-sight break + search timeout (tier-scaled, 90 s → 8 min). Wanted level then decays
  tier by tier. Interiors, back yards (mantle — [04](04-core-gameplay.md)), the brooks and the railway
  embankment are the natural evasion terrain.
- **Fire and ambulance** respond to their own triggers (fires, casualties), stage at range from active
  threats, and are **non-hostile, never armed**. Shooting at them escalates police tier directly.
- **Branding:** vehicles/uniforms read as *plausible UK police* . For this personal build, GMP-accurate
  livery is acceptable (the user's call, see [12](12-risks-legal-compliance.md)); the asset pipeline keeps
  livery as a swappable material so fictionalisation later is a texture change, not a remodel.

## Ambient event scheduler

Low-frequency world events so ten minutes of standing still is never static ([04](04-core-gameplay.md)
session-shape target): a train passing, a bus at its stop, rain starting, a delivery to a pub cellar, gulls
after a dropped chip tray, two NPCs arguing outside the bookies, the matchday crowd. Data-driven event table;
each event is a spawn + behaviour script + schedule window + rarity weight.

## Technical approach

- **Navigation:** Godot NavigationServer, region per chunk; interior navmeshes per building, linked by door
  portals. Off-mesh links for mantles (police tier 3+ can pursue over yard walls).
- **LOD for minds as well as meshes:** full BT + animation ≤ 50 m (~40 NPCs); simplified logic + imposter
  animation 50–250 m; statistical beyond. Crowd updates time-sliced across frames.
- **Performance risk flag:** 120 concrete NPCs on an M1 in GDScript will not fly; crowd tick is a
  **GDExtension (Rust/C++) candidate from day one**. This is the M2 validation spike —
  see [08](08-technical-architecture.md) and [OQ-3](13-open-questions.md).
- Animation: shared skeleton, ~12 body variants × palette + mix-and-match clothing from a Lancashire-normal
  wardrobe. No facial animation in v1; heads turn, that's it.

## Acceptance criteria

1. Time-lapse of Market Street across 24 game-hours shows the schedule table visibly working (empty → market
   → shoppers → pub build-up → kick-out → empty).
2. A single outdoor gunshot at 21:00 on Market Street: ≥ 30 NPCs react within 2 s, panic propagates outward,
   ≥ 1 report call completes, tier-2 arrives by road in a plausible time.
3. Full five-tier escalation reachable and evadable; helicopter audio-searchlight behaves at tier 5.
4. No frame > 16.6 ms attributable to AI with 120 concrete NPCs on target hardware (M2 spike gate).
5. Automated content audit: zero child-proportioned skeletons, zero name-pool collisions with the real-persons
   blocklist.

---

**Previous:** [05 — Weapons](05-weapons.md) · **Next:** [07 — Interiors](07-interiors.md) · **Index:** [PRD README](README.md)
