# 01 — Vision and Pillars

## Vision statement

> A shooter sandbox where the map is somewhere that actually exists, at the size it actually is, and the
> pleasure of it is recognition as much as action.

## The four pillars

Every design decision in this document should be traceable to one of these. If a feature doesn't serve a
pillar, it's a candidate for cutting.

### Pillar 1 — Recognition over spectacle

The strongest feeling this game can produce is **"that's the actual chippy"** — not a set-piece explosion. The
map's job is to be *correct*. When a design choice trades accuracy for drama, accuracy wins, because drama is
available in every other shooter and this isn't.

Concretely, this means:

- Real distances, including the boring ones. The walk from Hindsford to the town centre is not compressed.
- Real elevation. The 30 m → 76 m rise across the town is in the terrain, not flattened.
- Buildings that are shut in real life are shut in the game. Formby Hall was demolished in 2018; the site is
  modelled as the cleared ground it is.
- No invented landmark, however good it would be as a level.

### Pillar 2 — Everything you can see, you can approach

The counterweight to a real map is that real towns have a lot of closed doors. The game undermines the
1:1 premise every time the player walks up to a pub and finds a painted-on door.

The answer isn't to open every building — that's ~5,000 interiors, which is impossible. It's to be
**honest and consistent** about the rule: roughly 40 buildings are genuinely enterable, they are the ones that
matter (the pubs, the shops, the civic buildings, the stations), and the rest read unambiguously as private
housing that you wouldn't walk into anyway. A locked terraced front door breaks nothing. A locked pub does.

Interiors are **seamless** — no loading screens, no fade-to-black, no door-triggered teleport. You push a door
and you're inside. See [07 — Interiors](07-interiors.md).

### Pillar 3 — A town that is living, not decorated

NPCs are not scenery. The population runs on **schedules keyed to how the town actually works**: the commuter
surge at Atherton station between seven and nine, the market on market days, the school run, Market Street
filling up in the evening as the pubs get going, and the streets emptying after last orders.

The test: stand still on Market Street for ten minutes at three different times of day and get three
noticeably different towns.

### Pillar 4 — Consequence

You can shoot anyone. What makes that a *sandbox* rather than a shooting gallery is that the world answers.
Civilians panic, scatter, take cover, dial 999. Police respond from Flapper Fold Lane and escalate across five
tiers. The railway line and the brooks become chokepoints in a pursuit because they're chokepoints in the real
street layout.

The interesting content here is emergent and geographic — it comes from the map being real, not from scripting.

---

## What this game is not

Stating these plainly because each one is a plausible drift, and drift is the main risk to a solo project.

| Not | Why |
|---|---|
| **A campaign** | No missions, no story, no progression gates. Free-roam only. Explicitly out of scope. |
| **Multiplayer** | Single-player, offline. Netcode is not in the budget and is not in the brief. |
| **A driving game** | Vehicles exist as traffic and as transport. There is no handling model worth the name, no damage model, no racing. First person on foot is the game. |
| **A survival or crafting game** | No hunger, no inventory management beyond weapons, no base building. |
| **A tourism app** | It is a shooter. Accuracy serves the sandbox; it is not the product on its own. |
| **Photoreal** | The target is *convincing at play speed on an M1*, which is a different and much more achievable goal than photorealism. See [09](09-art-and-audio-direction.md). |
| **A commercial product** | Personal, unpublished. This is what lets the schedule be honest instead of a fantasy. |

## Target experience

A session should look like: spawn somewhere in town, walk, recognise things, find a building you can go in, go
in, look around, cause a problem, deal with the consequences of the problem, walk somewhere else. Twenty
minutes to two hours. No goal state.

The nearest reference points are the free-roam mode of a GTA title, the walking-around parts of *Everybody's
Gone to the Rapture*, and — for the specific pleasure of a hyper-accurate real map — flight-sim scenery. The
combination is the novelty.

## Success criteria

Because this is a test project, success is not commercial. It is:

1. **A person who knows Atherton walks around it and recognises where they are without being told.** This is
   the single criterion that matters most.
2. It runs at 60 fps at 1080p on a base M1 MacBook.
3. You can enter at least 20 real buildings, seamlessly.
4. At least 100 NPCs are alive and behaving on schedule in the town centre at peak.
5. The whole thing was built by one person and an agent in a timescale that didn't require quitting a job.

---

**Previous:** [00 — Executive summary](00-executive-summary.md) · **Next:** [02 — Setting: Atherton](02-setting-atherton.md) · **Index:** [PRD README](README.md)
