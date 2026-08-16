# Atherton — Product Requirements Document

**Version** 0.1 (draft) · **Date** August 2026 · **Status** Awaiting review

A 14-section PRD for an open-world first-person sandbox shooter set in a 1:1 recreation of Atherton,
Greater Manchester. Split into files because the whole thing runs long; each section stands alone but
cross-references the others.

---

## Reading order

If you read three files, read **00**, **03** and **12**.

| # | Section | What's in it |
|---|---|---|
| 00 | [Executive summary](00-executive-summary.md) | The pitch, the constraints, requirements traceability |
| 01 | [Vision and pillars](01-vision-and-pillars.md) | Why this game exists, the four design pillars, what it is not |
| 02 | [Setting: Atherton](02-setting-atherton.md) | Research dossier — geography, history, districts, culture |
| 03 | [World and map](03-world-and-map.md) | Bounds, the 1:1 data pipeline, districts, streaming |
| 04 | [Core gameplay](04-core-gameplay.md) | Movement, gunplay, the sandbox loop, day cycle |
| 05 | [Weapons](05-weapons.md) | Arsenal, selection wheel, ballistics data tables |
| 06 | [NPCs and AI](06-npcs-and-ai.md) | Civilians, schedules, panic ladder, police escalation |
| 07 | [Interiors](07-interiors.md) | Enterable-building spec, pub and shop templates |
| 08 | [Technical architecture](08-technical-architecture.md) | Godot 4, Metal, performance budget, project layout |
| 09 | [Art and audio direction](09-art-and-audio-direction.md) | Visual target, materials, weather, soundscape |
| 10 | [UI and UX](10-ui-ux.md) | HUD, weapon wheel, map, accessibility |
| 11 | [Milestones and roadmap](11-milestones-and-roadmap.md) | M0–M7, staffing models, exit criteria |
| 12 | [Risks, legal and compliance](12-risks-legal-compliance.md) | Likeness, trademark, data licensing, age rating |
| 13 | [Open questions](13-open-questions.md) | What still needs deciding, and by when |

## Reference dossiers

| Document | Purpose |
|---|---|
| [Landmark register](../reference/atherton-landmark-register.md) | Every modelled building — tier, coordinates, interior yes/no |
| [Street register](../reference/atherton-street-register.md) | Road network, classifications, surface notes |
| [Data sources and licences](../reference/data-sources-and-licences.md) | Geometry provenance, attribution obligations, prohibited sources |

## Decision records

| ADR | Decision |
|---|---|
| [0001](../adr/0001-engine-godot-4.md) | Engine: Godot 4.5 |
| [0002](../adr/0002-map-data-pipeline.md) | Map data pipeline: OSM + LiDAR + OS Open Data |

---

## Section status

| Section | Status | Blocking open question |
|---|---|---|
| 00–02 | Drafted | — |
| 03 | Drafted | Landmark register needs local review (OQ-1) |
| 04–05 | Drafted | — |
| 06 | Drafted | Police-force fictionalisation extent (OQ-4) |
| 07 | Drafted | Final Tier-1 interior count depends on staffing (OQ-6) |
| 08 | Drafted | Crowd-density spike must validate the engine choice at M2 (OQ-3) |
| 09–11 | Drafted | — |
| 12 | Drafted | **Real business names in shipping build — decide before M3 (OQ-2)** |
| 13 | Live | — |

## A note on accuracy

The Atherton research in sections 02 and 03 and in the reference dossiers was compiled from public web
sources. It is good but not authoritative — street-level detail on a town this size is patchy online, and at
least one source consulted was outright wrong. Everything geographic is flagged for review by someone with
local knowledge before it drives asset production. See
[13-open-questions.md](13-open-questions.md), OQ-1.
