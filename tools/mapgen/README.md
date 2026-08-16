# mapgen

The Atherton map pipeline ([ADR-0002](../../docs/adr/0002-map-data-pipeline.md)): compiles open geodata
into chunked grey-box meshes + a manifest that the Godot side loads at runtime.

## Quickstart (fixture — works anywhere, no downloads)

```sh
pip install -e "tools/mapgen[dev]"
mapgen build --config tools/mapgen/atherton.toml --fixture
```

Output lands in `assets/generated/` (gitignored). Then open the project in Godot 4.5+ and press play —
`src/main/main.gd` loads the manifest and drops a fly camera over the town centre chunk.
RMB-drag to look, WASD + E/Q to fly, Shift for speed.

The fixture (`fixtures/market_street.geojson`) is a **synthetic approximation** of the Market Street area —
a handful of roads and buildings at plausible positions inside the real map bounds. It exists so the
pipeline and the Godot loader are testable end-to-end without any data downloads. It is not survey data.

## Real data (on the dev Mac)

```sh
pip install -e "tools/mapgen[real,dev]"

# 1. OSM: download Greater Manchester from Geofabrik, clip to the Atherton bounds
osmium extract -b -2.5250,53.5100,-2.4700,53.5400 greater-manchester-latest.osm.pbf -o atherton.osm.pbf

# 2. LiDAR (optional at M0): EA Composite DTM 1m tiles for the bounds,
#    then set [terrain] source="geotiff" and geotiff_glob in atherton.toml

mapgen build --config tools/mapgen/atherton.toml --pbf atherton.osm.pbf --terrain-all
```

Sources, formats and coordinate systems: [docs/reference/data-sources-and-licences.md](../../docs/reference/data-sources-and-licences.md).

## Tests

```sh
python -m pytest tools/mapgen/tests -q
```

Covers ribbon geometry, extrusion (incl. holes and slopes), terrain seams between chunks, typology
classification, and an end-to-end fixture build with a byte-identical determinism check.

## Design notes

- **Deterministic:** same inputs → byte-identical output (fixed float precision, sorted features/chunks).
- **Local frame:** EPSG:27700 translated to a SW-corner origin; metres everywhere. The Godot axis flip
  (y-up) happens in exactly one place, `meshio.py`.
- **OBJ now, glTF later:** grey-box needs positions only; OBJ is diffable and parsed at runtime by
  `src/world/obj_loader.gd` with no import step. Facade kits at M2 bring materials/UVs and the move to glTF.
- **Stage caching** (per ADR-0002) is not yet implemented — the fixture build takes 20 ms; add caching when
  real-data builds make it worth having.
