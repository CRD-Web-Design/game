"""mapgen CLI.

Fixture build (works anywhere, no data downloads):
    mapgen build --config tools/mapgen/atherton.toml --fixture

Real-data build (on the dev Mac, with mapgen[real] installed and data
downloaded per docs/reference/data-sources-and-licences.md):
    mapgen build --config tools/mapgen/atherton.toml --pbf data/atherton.osm.pbf
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from .config import Config
from .crs import LocalFrame
from .export import build_town
from .ingest import load_geojson, load_osm_pbf
from .terrain import fixture_height_fn, geotiff_height_fn

FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "market_street.geojson"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="mapgen", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="build chunk meshes + manifest")
    b.add_argument("--config", required=True, help="path to atherton.toml")
    src = b.add_mutually_exclusive_group(required=True)
    src.add_argument("--fixture", action="store_true",
                     help="use the bundled synthetic Market Street fixture")
    src.add_argument("--pbf", help="clipped .osm.pbf extract (real data)")
    src.add_argument("--geojson", help="a GeoJSON FeatureCollection (e.g. overrides)")
    b.add_argument("--out", help="output dir (default: [export].out from config, "
                                 "resolved relative to the repo root)")
    b.add_argument("--terrain-all", action="store_true",
                   help="deprecated no-op: terrain now always covers every in-bounds chunk")

    args = ap.parse_args(argv)
    t0 = time.perf_counter()

    cfg = Config.load(args.config)
    frame = LocalFrame.from_bounds(cfg.bounds)

    if args.fixture:
        feats = load_geojson(FIXTURE, frame)
        source = f"fixture:{FIXTURE.name}"
    elif args.pbf:
        feats = load_osm_pbf(args.pbf, frame)
        source = args.pbf
    else:
        feats = load_geojson(args.geojson, frame)
        source = args.geojson

    if cfg.terrain_source == "geotiff" and not args.fixture:
        height_fn = geotiff_height_fn(cfg.geotiff_glob, frame)
    else:
        height_fn = fixture_height_fn(frame)

    if args.out:
        out_dir = Path(args.out)
    else:
        repo_root = Path(args.config).resolve().parents[2]
        out_dir = repo_root / cfg.out_dir

    manifest = build_town(cfg, frame, feats, height_fn, out_dir)

    dt = time.perf_counter() - t0
    c = manifest["counts"]
    print(f"mapgen: {source}")
    print(f"  frame   {frame.extent_x:.0f} m x {frame.extent_y:.0f} m "
          f"(origin E{frame.origin_easting:.0f} N{frame.origin_northing:.0f})")
    print(f"  built   {c['chunks']} chunks | {c['roads']} roads | "
          f"{c['buildings']} buildings")
    print(f"  out     {out_dir}")
    print(f"  took    {dt:.2f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
