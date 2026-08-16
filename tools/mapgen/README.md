# mapgen

The Atherton map pipeline ([ADR-0002](../../docs/adr/0002-map-data-pipeline.md)): compiles open geodata
into chunked grey-box meshes + a manifest that the Godot side loads at runtime.

## Quickstart (fixture — works anywhere, no downloads)

```sh
pip install -e "tools/mapgen[dev]"
mapgen build --config tools/mapgen/atherton.toml --fixture
```

Output lands in `assets/generated/` (gitignored). Then open the project in Godot 4.5+ and press play —
you spawn on foot in the densest chunk while `src/world/world_streamer.gd` streams the surrounding town
in and out around you. Controls are on the in-game HUD (WASD/Shift/Space; F for noclip fly).

The fixture (`fixtures/market_street.geojson`) is a **synthetic approximation** of the Market Street area —
a handful of roads and buildings at plausible positions inside the real map bounds. It exists so the
pipeline and the Godot loader are testable end-to-end without any data downloads. It is not survey data.

## Real data (on the dev Mac)

Two commands — the pipeline clips to the Atherton bounds itself, so no `osmium-tool`/Homebrew needed:

```sh
pip3 install -e "tools/mapgen[real,dev]"
curl -L -o greater-manchester.osm.pbf \
  https://download.geofabrik.de/europe/united-kingdom/england/greater-manchester-latest.osm.pbf
mapgen build --config tools/mapgen/atherton.toml --pbf greater-manchester.osm.pbf
```

The download is ~100 MB; the build chews through all of Greater Manchester and keeps only what falls
inside the bounds (expect a couple of minutes). First Play after a real build also takes longer while
several hundred chunks parse — watch the Output panel for `loading chunks... N / M`.

Notes:
- **Terrain is still the synthetic gradient** until EA LiDAR is wired in (M1): real streets and buildings
  on a plausible-but-fake slope. For real terrain, download EA Composite DTM 1 m tiles and set
  `[terrain] source="geotiff"` + `geotiff_glob` in `atherton.toml`.
- If you want a smaller file to re-run against, `osmium extract` (from `brew install osmium-tool`) can
  pre-clip the extract — purely an optimisation, never required.

Sources, formats and coordinate systems: [docs/reference/data-sources-and-licences.md](../../docs/reference/data-sources-and-licences.md).

## Tests

```sh
python -m pytest tools/mapgen/tests -q
```

Covers ribbon geometry, extrusion (incl. holes and slopes), terrain seams between chunks, typology
classification, an end-to-end fixture build with a byte-identical determinism check, and the real-data
`.pbf` ingest path against a synthetic PBF (auto-skipped unless the `[real]` extra is installed).

## Design notes

- **Deterministic:** same inputs → byte-identical output (fixed float precision, sorted features/chunks).
- **Local frame:** EPSG:27700 translated to a SW-corner origin; metres everywhere. The Godot axis flip
  (y-up) happens in exactly one place, `meshio.py`.
- **OBJ now, glTF later:** grey-box needs positions only; OBJ is diffable and parsed at runtime by
  `src/world/obj_loader.gd` with no import step. Facade kits at M2 bring materials/UVs and the move to glTF.
- **Stage caching** (per ADR-0002) is not yet implemented — the fixture build takes 20 ms; add caching when
  real-data builds make it worth having.
