# 11 — Milestones and Roadmap

Two plans, honestly labelled. **Plan A** is the real one: solo developer + AI assistance, evenings-and-weekends
cadence, milestones measured in *outcomes not dates*. **Plan B** is the reference studio schedule (6–10
people, ~16 months) kept for calibration — it is what this scope costs when someone is paid to do it.

The project is explicitly "a test to see what can be done" — so Plan A is sequenced to produce a playable
answer to that question as early as possible, and every milestone after M2 is optional in a way M0–M2 are not.

---

## Plan A — solo + AI (the operative plan)

Effort units: one **block** ≈ a focused weekend or 2–3 weekday evenings.

### M0 — Toolchain proven (≈ 4 blocks)

The pipeline exists end-to-end at toy fidelity. *No gameplay.*

- Godot 4.5 project boots on the Mac; empty scene at 120 fps.
- `mapgen` ingests the Geofabrik extract + 4 LiDAR tiles, clips to bounds, emits: terrain mesh, road ribbons,
  extruded flat-grey building shells for **one 256 m chunk** of the town centre.
- That chunk loads in Godot with a fly camera.
- Git LFS, CI unit-test skeleton, this PRD merged.

**Exit:** screenshot of grey Market Street geometry from the air, recognisable street pattern vs the real map.

### M1 — Grey-box Atherton, walkable (≈ 8 blocks)

The whole town at zero art quality. *The 1:1 claim becomes checkable here, cheaply.*

- Full-bounds generation: all chunks, terrain with real elevation, all roads, all Tier 3 shells, railway
  embankment, brooks.
- Streaming ring works; gate **G1** passes ([08](08-technical-architecture.md)).
- First-person controller per [04](04-core-gameplay.md) — walk/jog/sprint/crouch/mantle.
- Day/night cycle (light only).
- **The M1 ritual:** walk the whole town, list every geographic error, fix data not geometry. This is where
  local review ([OQ-1](13-open-questions.md)) lands.

**Exit:** 20-minute unedited video walking station → Market Street → Howe Bridge, correct distances and
gradients throughout.

### M2 — The decisive slice (≈ 10 blocks)

400 m of Market Street at real quality + the systems that prove the game. *Everything risky is in this
milestone on purpose.*

- Facade kit v1 (shopfront + terrace typologies) dressing the slice; 2 Tier 1 pubs (Jolly Nailor, Pound Pub)
  with full template interiors, seamless entry.
- Weapons: fists, cue, 9 mm pistol, pump shotgun — full wheel UX, `.tres`-driven.
- NPCs: 60–120 concrete, schedule archetypes (shopper/pub-goer/shopworker), full panic ladder.
- Police response tiers 1–2, physically arriving from Flapper Fold Lane.
- **Gate G2 — the crowd spike.** Rust crowd crate if (realistically: when) GDScript falls over.

**Exit:** the [04](04-core-gameplay.md) acceptance-#4 full-loop video, on-target-hardware, 60 fps HUD showing.
**This milestone answers "what can be done." If the project stopped here it would have succeeded.**

### M3 — The whole town, dressed (≈ 12 blocks)

- All six typology kits; every district dressed; landmark Tier 1 *exteriors* (all ~20).
- Traffic + bus ambient layer; trains running.
- Weather states; audio ambient beds v1.

### M4 — All interiors (≈ 12 blocks)

- Remaining Tier 1 interiors (~18) + Tier 2 template redresses (~12) per [07](07-interiors.md).
- Interior schedules/occupancy live; break-in mechanics; gate **G3**.

### M5 — Full sandbox depth (≈ 8 blocks)

- Full arsenal (15 weapons); police tiers 3–5 incl. helicopter and cordons; fire/ambulance services;
  ambient event scheduler; wanted decay/reset loop complete; gate **G4**.

### M6 — Polish to "high quality" (≈ 10 blocks)

- Audio mix snapshots, the quiet-moment system; rain as hero state; night lighting pass.
- Accessibility commitments from [10](10-ui-ux.md); save system hardened; gate **G5** soak.
- The 10-photo Street View side-by-side test from [09](09-art-and-audio-direction.md).

**Exit = done:** the five success criteria in [01 — Vision](01-vision-and-pillars.md) all pass, including
criterion 1: *a person who knows Atherton recognises it unprompted.*

### Sequencing rules

1. Never start M(n+1) with M(n)'s gate red.
2. Data fixes always via `mapgen` re-run, never hand-patched geometry ([03](03-world-and-map.md)).
3. Any block spent on a feature not in this PRD requires adding it to [13](13-open-questions.md) first —
   scope drift is the #1 risk ([00](00-executive-summary.md)).

---

## Plan B — reference studio schedule (calibration only)

| # | Milestone | Weeks | Team-shape note |
|---|---|---|---|
| M0 | Pre-production: toolchain, data, PRD sign-off | 4 | 2 eng, 1 TA |
| M1 | Grey-box town + controller | 8 | 3 eng, 1 TA |
| M2 | Vertical slice (Market St 400 m, 3 weapons, 20 NPCs, 2 pubs) | 8 | +2 artists, 1 designer |
| M3 | Full map exterior | 12 | art-heavy |
| M4 | Interiors + schedule systems | 12 | full team |
| M5 | Police escalation + full arsenal | 8 | eng-heavy |
| M6 | Content-complete, optimisation | 12 | full team |
| M7 | Release candidate: rating, notarisation, store | 6 | *not applicable to Plan A — exists only if the project is ever published* |
| | **Total** | **~70 weeks** | 6–10 people |

The Plan B numbers are the honest answer to "why is Plan A shaped like that": ~70 team-weeks of studio work
compresses into a solo project only by (a) procedural generation carrying the art volume, (b) cutting M7
entirely, and (c) treating M3–M6 as progressive-enhancement rather than obligations.

## Post-v1 candidate features ("we will add more features later")

Parked, not planned — each becomes a PRD amendment if promoted. Rough order of value:

1. Drivable vehicles (the map's road network is already simulated)
2. Boardable buses/trains on the real routes
3. Pool/darts minigames in the pubs
4. Economy: shop purchases, cash loop
5. Seasonal/event states: Bent 'n' Bongs at the Roller Rink, matchday crowds at full density
6. Character customisation
7. Photo mode (HUD-off already exists — this adds lens controls)
8. Co-op (large; would reopen the engine question)

---

**Previous:** [10 — UI and UX](10-ui-ux.md) · **Next:** [12 — Risks, legal, compliance](12-risks-legal-compliance.md) · **Index:** [PRD README](README.md)
