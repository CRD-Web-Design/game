# Atherton

**Working title.** An open-world, first-person sandbox shooter set in a 1:1 geographic recreation of
Atherton — a town of roughly 22,000 people in the Metropolitan Borough of Wigan, Greater Manchester.

This repository contains the design documentation and the **M0 toolchain**: the map-generation pipeline
(`tools/mapgen`) and a Godot 4.5 project skeleton that loads its output under a fly camera.

---

## What this is

Most open-world shooters invent their city. This one doesn't. The premise is that the map *is* Atherton —
real streets at real distances, real elevation, real buildings on their real footprints, and the pubs and
shops along Market Street enterable and modelled inside. You can walk from Hag Fold station to Chowbent
Chapel and the walk takes as long as it takes.

| | |
|---|---|
| **Genre** | Open-world first-person shooter, free-roam sandbox |
| **Setting** | Atherton, Greater Manchester — modern day |
| **Playable area** | ≈ 12.2 km² |
| **Platform** | macOS, Apple Silicon (M1 and later) |
| **Engine** | Godot 4.5+ (tested on 4.7), Forward+ renderer, Metal backend |
| **Mode** | Single-player |
| **Target rating** | PEGI 18 / ESRB M |

## Documentation

Start at **[docs/prd/README.md](docs/prd/README.md)** — the PRD index, with a suggested reading order.

| Area | Location |
|---|---|
| Product requirements (14 sections) | [`docs/prd/`](docs/prd/) |
| Atherton research dossiers | [`docs/reference/`](docs/reference/) |
| Architecture decision records | [`docs/adr/`](docs/adr/) |

The three reference dossiers are the load-bearing ones for anyone building the map:

- [Landmark register](docs/reference/atherton-landmark-register.md) — every modelled building, tiered, with coordinates
- [Street register](docs/reference/atherton-street-register.md) — the road network and its classifications
- [Data sources and licences](docs/reference/data-sources-and-licences.md) — where the geometry comes from and what you must attribute

## Status

**M1 in progress — first-person walking.** The pipeline builds real OSM data end-to-end (28 tests green);
the Godot side streams chunks around a walking player with collision. **The landmark and street registers
were compiled from public web sources and need review by someone who knows the town** — see the accuracy
caveats at the top of each register.

## Run it

```sh
pip install -e "tools/mapgen[dev]"
mapgen build --config tools/mapgen/atherton.toml --fixture   # or --pbf for real Atherton
# open the repo in Godot 4.5+ (macOS, Apple Silicon) and press Play
```

You spawn on foot in the densest chunk (with real data: the town centre).

| Input | Action |
|---|---|
| Click | capture the mouse (Esc releases it) |
| Mouse | look |
| WASD | walk |
| Shift | sprint |
| Space | jump |
| F | toggle noclip fly (E/Q for up/down, Shift for speed) |

Real-data builds (OSM + LiDAR): [tools/mapgen/README.md](tools/mapgen/README.md).

## Content

This game depicts gun violence in a real, named town, including against civilian NPCs. It is designed for an
adult audience. Two constraints are absolute and are specified in
[`docs/prd/06-npcs-and-ai.md`](docs/prd/06-npcs-and-ai.md): the game contains **no child characters of any
kind**, and **no real living person is modelled, named, or depicted**.

The unresolved question of whether real business names ship in the final build is tracked in
[`docs/prd/12-risks-legal-compliance.md`](docs/prd/12-risks-legal-compliance.md) and must be decided before M3.
