# ADR-0002 — Map Data Pipeline: OSM + EA LiDAR + OS Open Data → Procedural Town

**Status:** Accepted · **Date:** 2026-08-16

## Context

The brief demands **1:1 geographic accuracy** for 12.2 km² of real town
([03](../prd/03-world-and-map.md)). Hand-modelling ~5,000 buildings is impossible solo; buying the town
doesn't exist as an option; the map must also be *correctable* cheaply when local review
([OQ-1](../prd/13-open-questions.md)) finds errors.

Note: this is a personal, unpublished project — sources below are chosen on technical merit; the (dormant)
licence posture is recorded in [data sources](../reference/data-sources-and-licences.md).

## Decision

A **deterministic, cached, re-runnable offline pipeline** (`tools/mapgen`, Python) that compiles open
geodata into engine-ready assets. The town is *built by code from data*; hand-made art attaches to stable
anchors. No generated geometry is ever hand-edited.

```
inputs:   OSM (Geofabrik GM extract) · EA LiDAR DTM 1 m (+DSM for heights) · OS Open Roads/Names/OpenMap
stages:   ingest → reproject (EPSG:27700, SW-corner origin) → classify → terrain → roads →
          buildings → landmarks(anchors) → props/spawns → export (glTF + JSON)
outputs:  per-chunk terrain meshes + splatmaps · road ribbons · Tier 3 building shells ·
          landmark anchor transforms · POI/spawn/schedule data · pause-map render
```

### Key mechanisms

- **Determinism:** same inputs + same seed = byte-identical output. Source snapshots are archived at M0
  (risk R7). Every stage caches; a data fix re-runs only downstream stages.
- **Anchors, not geometry, for hand work:** Tier 1/2 assets bind to `anchor_id` (stable, derived from
  OSM id + address), so regeneration never orphans or moves hand-made art unless the underlying datum
  actually changed — in which case moving is correct.
- **Typology classification** drives Tier 3 facades: footprint shape + OSM tags + district → one of six
  typologies (Victorian terrace / semi / detached / estate house / shopfront / industrial / civic), each
  with a modular facade kit ([09](../prd/09-art-and-audio-direction.md)). The typology *map* is a reviewable
  intermediate artefact (rendered as a coloured overlay for the OQ-1 pass).
- **Heights:** OSM `building:levels` where tagged → else DSM−DTM median inside footprint → else typology
  default. Provenance recorded per building for later auditing.
- **Registers as pipeline input:** the [landmark](../reference/atherton-landmark-register.md) and
  [street](../reference/atherton-street-register.md) registers live in `data/registers/` as structured data;
  the pipeline resolves register addresses/postcodes to coordinates via OS Open Names and *fails the build*
  on unresolvable Tier 1 entries — the register and the map cannot silently diverge.

## Options considered

- **Hand-model everything (rejected):** studio-scale cost; uncorrectable; the 1:1 claim would decay with
  every error found.
- **Photogrammetry / Google-derived capture (rejected):** ToS-violating for Google sources and, decisively,
  *worse data* — pixels instead of polygons and elevations; enormous cleanup burden; no re-runnability.
- **Buy city-generator middleware (rejected):** generic-city output is the opposite of the recognition
  pillar; none consume UK open data at this fidelity out of the box.
- **In-engine procedural generation at runtime (rejected):** burns the M1's frame budget on work that never
  changes; offline compilation is strictly better here.

## Consequences

- M0's exit criterion is this pipeline working end-to-end on one chunk — the ADR is validated or broken
  within the first four blocks of the project.
- Map errors are *data bugs with data fixes*: edit OSM upstream (improving the public map as a side effect)
  or add a local override layer (`data/registers/overrides.geojson`) — both re-run cleanly. Sequencing rule
  2 in [11](../prd/11-milestones-and-roadmap.md) enforces the no-hand-patching discipline.
- The pause map ([10](../prd/10-ui-ux.md)) renders from the same compiled data, so map and world cannot
  disagree.
- Pipeline toolchain (Python + GDAL/osmium/shapely + Blender headless for kit-bash/LOD bake) becomes a
  hard dependency of the dev environment; pinned via `uv` lockfile in `tools/mapgen`.
