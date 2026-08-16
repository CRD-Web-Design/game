# 12 — Risks, Legal and Compliance

Project risks first (the ones that can actually kill this), then the legal register (mostly dormant while the
project stays personal and unpublished — but recorded so that any change of status triggers deliberate
decisions, not accidents).

---

## Project risks

Ranked by (likelihood × impact). Mitigations are already embedded in the milestone plan
([11](11-milestones-and-roadmap.md)); this table is the why.

| # | Risk | L | I | Mitigation |
|---|---|---|---|---|
| R1 | **Scope death.** 12 km² + 40 interiors + crowd AI is studio-scale; solo drift is fatal | High | Fatal | Plan A sequencing: playable answer at M2; M3–M6 optional enhancements; PRD-amendment rule for new features |
| R2 | **Crowd perf on 8 GB M1.** 120 scheduled NPCs is the hardest budget line | High | High | G2 gate at M2, early; Rust crate planned not hoped-for; fallback ladder: 90 NPCs → smaller ring → engine question last |
| R3 | **Map data quality.** Web-sourced registers; OSM gaps; wrong buildings expensive at M3+ | Med | High | Grey-box-first (M1 ritual), local review OQ-1, deterministic re-gen so fixes are data-edits |
| R4 | **Facade kit not good enough** → 5,000 buildings look like dev-art → recognition pillar fails | Med | High | Kit treated as hero asset ([09](09-art-and-audio-direction.md)); M2 slice proves it on the most-seen street first |
| R5 | **Godot production limits** at open-world scale (streaming maturity, editor perf on huge scenes) | Med | Med | Chunked scenes keep editor loads small; ADR-0001 fallback documented; M0 proves pipeline before commitment deepens |
| R6 | **Solo-project bus factor / motivation** | Med | Med | Everything reproducible from repo (pipeline, no hand-patched geometry); milestones end in *demonstrable artefacts* (videos, gate results) for momentum |
| R7 | **LiDAR/OSM licence change or takedown of source data** | Low | Low | Snapshot source data in cold storage at M0 (personal archival copy) |

## Content constraints (active, not dormant)

These two are design law regardless of publication status — see [06](06-npcs-and-ai.md) for enforcement and
the automated audits in [08](08-technical-architecture.md):

1. **No child characters in the game, in any capacity.**
2. **No real living person modelled, named, or depicted.** Includes negative-space collisions: no generated
   NPC landlord in a modelled real pub sharing the real landlord's name; blocklist maintained as data.

And one composition rule from the same family: **interiors of private homes are never enterable** — the
enterable roster is exclusively commercial, civic and heritage premises ([07](07-interiors.md)). Depicting a
real, addressable private house internally crosses a line the pub interiors don't.

## Legal register — dormant while personal/unpublished

The project's status ("personal use only, will not be published — a test to see what can be done") is the
load-bearing fact. Nearly every obligation below is triggered by *distribution*. **If a build is ever shared
beyond the developer's own machines — including a free itch.io upload, a public repo with assets, or a YouTube
build handed to a friend — this register goes from dormant to live and this section must be re-worked before
that happens.** That's the one process rule.

| Item | Dormant because | If ever published |
|---|---|---|
| **Real business names & trade dress** (pubs, shops as violence sites) | No third party ever sees it | The big one. Trademark/passing-off exposure plus a real reputational problem in a town of 22,000. Standard industry answer: fictionalise names ("Jolly Nailer", "Wheatberry") keeping buildings — pipeline already treats signage as swappable data ([09](09-art-and-audio-direction.md)), so this is a content pass, not a rebuild |
| **Police livery** (GMP-accurate acceptable in personal build, [06](06-npcs-and-ai.md)) | Same | Swap to fictional force — material swap by design |
| **OSM ODbL / OGL attribution** | Attribution obligations attach to distribution | Attribution strings ready in [data sources](../reference/data-sources-and-licences.md); ODbL share-alike analysis needed for the derived geometry |
| **Age rating** (content is PEGI 18-class: realistic violence against civilians) | Ratings govern commercial distribution | PEGI/ESRB submission; storefront gates |
| **macOS signing/notarisation** | Ad-hoc signing fine on own machine | Developer ID + notarisation |
| **Music licensing** | Jukebox pool is licensed-free by design ([09](09-art-and-audio-direction.md)) — clean either way | Verify pool licences permit commercial sync |
| **Real-person likeness** | Already prohibited outright | No change — stays prohibited |

### A note on the sensitive premise, on the record

This PRD specifies a game in which the player can commit gun violence against civilians in a faithful replica
of a real, named, small town. The developer chose this deliberately (the GTA model), was advised of the
concern, and confirmed the direction; the project being private makes the choice self-regarding, and this
document implements it fully. The two content constraints above, the private-homes rule, and the
publication-trigger process rule are the guardrails that make "fully" compatible with "responsibly." If the
project's audience ever grows beyond one person, the guardrails grow with it — that's the deal this section
records.

## Compliance checklist (live items only)

- [ ] M0: archive snapshots of all source datasets
- [ ] M2: no-child-skeleton and name-blocklist audits running in CI ([08](08-technical-architecture.md))
- [ ] M3: signage system confirmed data-driven (fictionalisation remains a content-pass away)
- [ ] Ongoing: enterable roster contains zero private dwellings
- [ ] Trigger rule: any distribution intent → this section re-opened first

---

**Previous:** [11 — Milestones](11-milestones-and-roadmap.md) · **Next:** [13 — Open questions](13-open-questions.md) · **Index:** [PRD README](README.md)
