# 13 — Open Questions

Live register. Each question has an owner-by-default (the developer), a decision deadline expressed as a
milestone, and the section it blocks. New feature ideas land here first before entering scope
(sequencing rule 3, [11](11-milestones-and-roadmap.md)).

---

| ID | Question | Decide by | Blocks | Notes |
|---|---|---|---|---|
| **OQ-1** | **Local review of the registers.** Who with knowledge of Atherton walks the landmark and street registers (and later the M1 grey-box) and corrects them? | Before M3 art spend; ideally at M1 | [03](03-world-and-map.md), asset budget | The registers' own Unresolved sections list the specific items: leisure centre, supermarket roster, pub closures, market days, Bag Lane, missing everyday places. The developer appears to know the area — this may just be a self-review pass with fresh eyes |
| **OQ-2** | **Real business names — keep permanently?** Currently: yes, real names, per the personal-use decision | Only if publication status changes | [12](12-risks-legal-compliance.md) | Dormant. Signage stays data-driven so it never becomes urgent |
| **OQ-3** | **Does Godot survive the crowd spike (gate G2)?** | M2, hard gate | Everything | The fallback ladder is defined ([08](08-technical-architecture.md)): 90 NPCs → 250 m ring → Unity port as last resort. Decision is made by the benchmark, not by preference |
| **OQ-4** | **Police livery: GMP-accurate or generic-UK?** Currently GMP-accurate is acceptable for the personal build | M5 (when response tiers 3–5 get assets) | [06](06-npcs-and-ai.md) | Cosmetic either way — material swap by design |
| **OQ-5** | **Day length default.** 48-min days specified; is that right for a wander-paced sandbox? | M2 playtest | [03](03-world-and-map.md) | Cheap to change; playtest, don't debate |
| **OQ-6** | **Final Tier 1 interior count.** 20 bespoke interiors specified; solo reality may say 12 | End of M4 | [07](07-interiors.md), [11](11-milestones-and-roadmap.md) | Cut from the bottom of the register's atmosphere-only entries (Gibfield baths, Rescue Station) before touching any pub |
| **OQ-7** | **No-minimap decision.** Compass-strip-only navigation is a real design bet | M3 playtest | [10](10-ui-ux.md) | If wayfinding frustrates, add an optional minimap rather than abandoning the bet — setting, off by default |
| **OQ-8** | **Trains/buses: ambient-only confirmed?** Boardable transit is parked in post-v1 | v1 scope is closed — parked | [11](11-milestones-and-roadmap.md) | Only here because it will keep coming up. The answer is post-v1 |
| **OQ-9** | **Seasonal calendar.** Day-of-week exists (market, matchday). Do seasons/dates exist (Bent 'n' Bongs in January, winter light)? | M3 | [03](03-world-and-map.md), [09](09-art-and-audio-direction.md) | Lean: probably a v1 "no" with the event-scheduler hooks left in place |
| **OQ-10** | **What does "done" mean for a test project?** Success criteria in [01](01-vision-and-pillars.md) define v1-done. But the stated purpose is "see what can be done" — M2 already answers that | Developer's call, revisit after M2 | Plan A M3–M6 | The PRD's honest position: M2 is the experiment's answer; M3–M6 are the reward for liking the answer |

## Resolved this draft

| ID | Question | Resolution |
|---|---|---|
| ~OQ-A~ | Engine | Godot 4.5 — [ADR-0001](../adr/0001-engine-godot-4.md) |
| ~OQ-B~ | Premise/hostiles | GTA-model civilian sandbox — user decision, recorded in [00](00-executive-summary.md) and [12](12-risks-legal-compliance.md) |
| ~OQ-C~ | Scope | Free-roam sandbox only, no campaign |
| ~OQ-D~ | Map fidelity | 1:1 from survey data — [ADR-0002](../adr/0002-map-data-pipeline.md) |
| ~OQ-E~ | Licensing posture | Personal/unpublished — obligations dormant, register kept ([12](12-risks-legal-compliance.md)) |
| ~OQ-F~ | Target hardware | Apple Silicon, floor = base M1 8 GB |

---

**Previous:** [12 — Risks, legal, compliance](12-risks-legal-compliance.md) · **Index:** [PRD README](README.md)
