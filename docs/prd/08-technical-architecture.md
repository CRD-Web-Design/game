# 08 — Technical Architecture

Engine, performance budget, project structure, and the build/test story. The binding constraint from the
brief: **runs well on an Apple Silicon MacBook.**

---

## Engine: Godot 4.5

Decision and alternatives in [ADR-0001](../adr/0001-engine-godot-4.md). One-line rationale: native Metal
backend on Apple Silicon, text-based scenes that a git-driven, agent-assisted workflow can actually author,
zero licence friction for a personal project. Unity 6 is the documented fallback if the M2 crowd spike fails
(see below); Unreal was rejected for macOS-support and workflow reasons.

- **Renderer:** Forward+ (Metal). Not the mobile renderer — we need its lighting features; not compatibility —
  we don't need GLES fallback.
- **Physics:** Jolt (built-in since 4.4).
- **Scripting:** GDScript for gameplay logic; **GDExtension (Rust)** for identified hot paths only: crowd
  simulation tick, chunk streaming, procedural building instancing, ballistics broadphase. Rust over C++ for
  the solo-dev safety margin.
- **Version pin:** 4.5.x, upgraded deliberately, never mid-milestone.

## Target hardware and budget

**Floor:** MacBook Air M1, 8 GB unified memory, 1080p → **60 fps sustained**.
**Comfort:** M3/M4 or Pro/Max silicon → high preset, 120 fps where the display allows.

| Budget | Value | Notes |
|---|---|---|
| Frame | 16.6 ms (≈11 GPU / ≈5 CPU) | Measured, not vibes — see profiling gates below |
| Draw calls | < 2,500/frame | Multimesh + chunk merge makes this feasible at town scale |
| Triangles | < 4 M/frame | LOD discipline on Tier 3 shells |
| Resident memory | < 5 GB | 8 GB machine minus OS/browser reality |
| Streaming ring | 500 m full / 1.5 km imposter | From [03](03-world-and-map.md) |
| Concrete NPCs / vehicles | 120 / 40 | From [06](06-npcs-and-ai.md) |
| Active physics props | 60 per interior, pooled | From [07](07-interiors.md) |
| Chunk-load hitch | < 8 ms | Async + time-sliced instancing |

**Scalability presets:** Low (720p internal, 30 fps cap, 250 m ring, 60 NPCs) → Medium (the M1 floor spec) →
High (native res, 1 km full ring, richer shadows). Auto-detected, user-overridable.

**Lighting strategy:** baked LightmapGI for all interiors; exterior = directional sun/moon + SSIL + SSAO.
**SDFGI stays off** — it does not fit the M1 GPU budget at this scene scale. Reflections: baked probes
indoors, screen-space outdoors.

## Project layout

```
game/
  project.godot
  src/                    # GDScript, mirrors runtime systems
    player/               # controller, camera, health
    weapons/              # weapon system + WeaponDef resources
    ai/                   # civilian BTs, response director, schedules
    world/                # streaming, chunks, time/weather, events
    interiors/            # templates, door/portal logic, props
    ui/
  native/                 # Rust GDExtension crates
    crowd/  streaming/  ballistics/
  assets/
    generated/            # pipeline output — never hand-edited, gitignored
    handmade/             # Tier 1/2 models, materials, audio
  data/
    weapons/  schedules/  events/  spawns/   # .tres + JSON
    registers/            # landmark/street data consumed by pipeline
  tools/
    mapgen/               # the Python pipeline (ADR-0002)
  tests/
    unit/  scenes/        # GUT unit tests + scene-based harnesses
docs/                     # this PRD
```

Git discipline: `assets/generated` is reproducible and ignored; `assets/handmade` uses **Git LFS** from day
one (checked: repo host supports it) — glTF + textures will pass 1 GB quickly.

## The map pipeline as a build step

`tools/mapgen` is a deterministic Python CLI (`mapgen build --bounds atherton.toml --seed N`) with cached
stages (ingest → classify → terrain → roads → buildings → export). Full spec in
[ADR-0002](../adr/0002-map-data-pipeline.md). It runs on the dev Mac; nothing in the runtime depends on it.
Regeneration after a data correction is expected and cheap; hand-made assets bind to stable anchor IDs, not to
generated geometry.

## Performance gates (enforced, not aspirational)

Automated benchmark scenes run per milestone (headless where possible, scripted camera where not):

| Gate | Scene | Pass |
|---|---|---|
| G1 (M1 milestone) | Grey-box town flyover + sprint traverse | 60 fps, no hitch > 8 ms |
| G2 (M2) | **Crowd spike:** Market Street, 120 NPCs, full schedules, one gunshot event | AI ≤ 5 ms/frame — **this gate decides the engine** ([OQ-3](13-open-questions.md)) |
| G3 (M4) | Tesco interior trash-everything stress | 60 fps, prop cap holds |
| G4 (M5) | Tier-5 response: cordon + helicopter + 120 NPCs + fire | 60 fps on Medium preset |
| G5 (M6) | 2-hour soak, scripted wander | No leak > 100 MB/h, no degradation |

If G2 fails after the Rust crowd crate and honest optimisation: reduce concrete-NPC budget first (90 is still
a living town); switching engines is the last resort and the fallback ADR documents the port cost.

## Testing and CI

- **Unit:** GUT for pure logic (ballistics math, schedule resolution, response-director state machine).
- **Scene harnesses:** scripted scenarios asserting the acceptance criteria in each PRD section (e.g. the
  [06](06-npcs-and-ai.md) gunshot-reaction test is a scene that fires and counts state transitions).
- **Content audits as tests:** the landmark-register consistency check, the no-child-skeleton audit, the
  name-blocklist audit ([06](06-npcs-and-ai.md)) run in CI.
- **CI:** GitHub Actions, `godotengine/godot` headless Linux for unit + audit jobs on every push. Performance
  gates run on the actual Mac (self-hosted runner or manual per-milestone ritual — solo project, manual is
  acceptable; results committed to `docs/perf/`).

## Build and distribution

- Export: macOS `.app`, Apple Silicon only (no universal binary — nothing to gain).
- **Signing: ad-hoc.** Personal build, no Developer ID, no notarisation. Gatekeeper right-click-open is fine.
  (What would change for distribution: [data sources](../reference/data-sources-and-licences.md), last section.)
- Debug/sandbox console ships enabled ([05](05-weapons.md) give-all, teleport, time-set, wanted-set,
  perf HUD) — it's a test project; the console *is* a feature.

## Save format

Single JSON save (player state, time, loadout, settings) + versioned schema. Nothing clever; see scope in
[04](04-core-gameplay.md).

---

**Previous:** [07 — Interiors](07-interiors.md) · **Next:** [09 — Art and audio](09-art-and-audio-direction.md) · **Index:** [PRD README](README.md)
