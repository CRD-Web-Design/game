# 03 — World and Map

How 12.2 km² of real town becomes a game level, at 1:1, without an art team.

---

## Bounds

Derived from the reference map view (centre 53.5240 N, −2.4923 W) and extended to natural edges:

| Edge | Value | Sealed by |
|---|---|---|
| North | 53.5400 | Open farmland toward Over Hulton |
| South | 53.5100 | Atherleigh / Leigh fringe |
| West | −2.5250 | **Shakerley Brook** — the real western boundary of the township |
| East | −2.4700 | Open land toward Tyldesley |

≈ 3.34 km north–south × 3.64 km east–west ≈ **12.2 km²**. All six districts (town centre/Chowbent, Hindsford,
Howe Bridge, Hag Fold, Atherleigh, Lately Common) fall inside.

**Edge treatment:** no invisible walls. The map edge is soft — streets that leave the bounds are blocked
diegetically (roadworks, a closed level crossing, a flooded underpass) or simply peter out into fields with a
gentle "turn back" fade if the player pushes far past the last content. The brook edge needs nothing; it's a
real barrier.

## What 1:1 means here — and what it doesn't

**It means:** every street on its real alignment at real width; every building on its real footprint at its
real (or best-derived) height; real terrain elevation from LiDAR; landmark buildings recognisable as
themselves; real distances everywhere.

**It doesn't mean:** every brick photoscanned. Fidelity is tiered:

| Tier | Count (est.) | Treatment |
|---|---|---|
| 1 | ~40 | Hand-modelled from photo reference, bespoke interiors — the [landmark register](../reference/atherton-landmark-register.md) |
| 2 | ~200 | Generated shell + hand-tuned facade; shared template interiors for some |
| 3 | ~5,000 | Fully procedural: footprint × height × typology facade kit. Sealed. |

The bet behind the whole project: **Tier 3 at scale + Tier 1 where it counts = recognition** (Pillar 1),
because what makes a town recognisable is its street pattern, massing, and landmarks — not the individual
semis.

## The generation pipeline

Full detail in [ADR-0002](../adr/0002-map-data-pipeline.md); summary:

```
OSM extract (Geofabrik) ─┐
EA LiDAR DTM 1 m ────────┼─→ Python (osmium/GDAL/shapely, EPSG:27700)
OS Open Roads / Names ───┘        │
                                  ├─→ terrain heightmap + splatmaps
                                  ├─→ road ribbon meshes + markings
                                  ├─→ building shells (footprint × height × typology)
                                  ├─→ landmark anchor transforms (for hand-made assets)
                                  └─→ POI/spawn/schedule data (JSON)
                                          │
                              Blender (facade kit-bash, LOD bake)
                                          │
                                  glTF → Godot import
```

Key properties:

- **Deterministic and re-runnable.** The town regenerates from source data + seed. Hand-made Tier 1/2 assets
  attach to *anchor transforms*, so re-running the pipeline after a data fix doesn't destroy hand work.
- **Typology-driven facades.** Each footprint is classified (Victorian terrace / semi / detached / estate
  house / shopfront / industrial shed / civic) from OSM tags, footprint shape and district, then dressed from
  that typology's facade kit. Getting the *typology map* right is what makes districts read correctly —
  pebbledash in Hag Fold, red-brick terrace rows in Howe Bridge.
- **Heights** from OSM tags where present, else DSM−DTM difference, else typology default (terrace 5.5 m to
  eaves, semi 5.2 m, shopfront 7.5 m, etc.).

## World structure in-engine

- **Origin:** southwest corner of bounds. Units = metres. X = east, Z = north (negated per Godot convention),
  Y = up. At 3.6 km maximum extent, single-precision floats are fine — no origin shifting needed.
- **Chunking:** the town is split into **256 m × 256 m chunks** (~15 × 14 grid). Each chunk is a separate
  `.tscn` scene containing its terrain patch, roads, Tier 3 shells and props.
- **Streaming:** ring-based async loading around the player. Full-detail ring ≈ 500 m; imposter ring to
  1.5 km; skyline silhouette beyond. Landmarks keep a low-LOD presence at any distance — you can see
  St John the Baptist's tower from across town, because you can.
- **Interiors** live in their building's scene and stream with it. No separate interior cells — see
  [07](07-interiors.md).

## The railway

The Manchester–Southport line crosses the whole map and is treated as first-class geometry: embankments and
cuttings from LiDAR, bridges and crossings modelled accurately, fencing walkable-up-to. Trains run as
**scheduled ambient events** (non-boardable, v1) — a two-car Northern unit passing every 15–30 minutes each
way, audible before visible. The line's limited crossing points are a deliberate navigation and pursuit
feature, not an obstacle to smooth out.

## Traffic and transport (ambient layer)

- Vehicle traffic simulated on the road graph, weighted to the A577/A579 and bus corridors (582, 583 routes).
- Buses run their real routes as ambient vehicles with stops; non-boardable in v1 (candidate future feature —
  see [13](13-open-questions.md)).
- Parked cars from a density map (dense terraced kerbs, car parks at Tesco/the precinct/the stations).

## Time and weather

- 24-hour day/night cycle, default 1 game-day = 48 real minutes, configurable including real-time.
- Day of week exists (drives market day, matchday, pub schedules).
- Weather states: overcast (default), bright, rain, heavy rain, fog. Northwest England distribution — see
  [09](09-art-and-audio-direction.md).

## Acceptance criteria

1. Overlaying the generated road network on OS Open Roads shows no visible deviation at 1:2500.
2. Spot elevation at 20 sampled points matches LiDAR DTM within ±0.5 m.
3. All landmark-register Tier 1 anchors fall inside the bounds and on their register addresses.
4. A player walking A579 north from the southern edge experiences continuous rising ground (~46 m over the
   traverse), no flat plateau artefacts.
5. Full walk-through of every street with no holes, floating buildings, or z-fighting between chunks.
6. Chunk streaming produces no hitch > 8 ms on the target M1 at walking and sprinting speed.

---

**Previous:** [02 — Setting](02-setting-atherton.md) · **Next:** [04 — Core gameplay](04-core-gameplay.md) · **Index:** [PRD README](README.md)
