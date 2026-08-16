"""Chunking and export: features -> per-chunk OBJ layers + manifest.json."""

from __future__ import annotations

import json
import math
from pathlib import Path

from . import __version__
from .config import Config
from .crs import LocalFrame
from .buildings import extrude
from .meshio import aabb, write_obj
from .model import Features
from .roads import ribbon, road_width
from .terrain import HeightFn, chunk_terrain_mesh


def _chunk_of(x: float, y: float, cs: float) -> tuple[int, int]:
    return int(math.floor(x / cs)), int(math.floor(y / cs))


def build_town(
    cfg: Config,
    frame: LocalFrame,
    feats: Features,
    height_fn: HeightFn,
    out_dir: Path,
    terrain_all: bool = False,
) -> dict:
    """Generate all chunk meshes + manifest. Returns the manifest dict.

    Chunk population:
    - buildings by footprint centroid;
    - road *segments* by segment midpoint (a long road contributes geometry
      to every chunk it crosses, with at most one segment of slack);
    - terrain for every chunk that received features (or all in-bounds
      chunks with terrain_all=True).
    """
    cs = cfg.chunk_size
    out_dir.mkdir(parents=True, exist_ok=True)

    road_segs: dict[tuple[int, int], list] = {}
    for road in feats.roads:
        w = road_width(road)
        for p0, p1 in zip(road.points, road.points[1:]):
            mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            road_segs.setdefault(_chunk_of(*mid, cs), []).append((road, w, p0, p1))

    bld_in_chunk: dict[tuple[int, int], list] = {}
    for b in feats.buildings:
        ring = b.rings[0]
        cx = sum(p[0] for p in ring) / len(ring)
        cy = sum(p[1] for p in ring) / len(ring)
        bld_in_chunk.setdefault(_chunk_of(cx, cy, cs), []).append(b)

    ni = int(math.ceil(frame.extent_x / cs))
    nj = int(math.ceil(frame.extent_y / cs))
    if terrain_all:
        active = {(i, j) for i in range(ni) for j in range(nj)}
    else:
        active = set(road_segs) | set(bld_in_chunk)
    active = {(i, j) for (i, j) in active if 0 <= i < ni and 0 <= j < nj}

    chunks = []
    for (i, j) in sorted(active):
        cid = f"c_{i}_{j}"
        layers: dict[str, str] = {}
        all_verts = []

        tv, tt = chunk_terrain_mesh(i, j, cs, cfg.terrain_step, height_fn)
        write_obj(out_dir / f"{cid}_terrain.obj", tv, tt, f"{cid}_terrain")
        layers["terrain"] = f"{cid}_terrain.obj"
        all_verts += tv

        segs = road_segs.get((i, j), [])
        if segs:
            rv: list = []
            rt: list = []
            # Consecutive segments of the same road merge back into a
            # polyline so ribbons keep their miter joins within the chunk.
            runs: list[tuple[float, list]] = []
            for road, w, p0, p1 in segs:
                if runs and runs[-1][2] is road and runs[-1][1][-1] == p0:
                    runs[-1][1].append(p1)
                else:
                    runs.append((w, [p0, p1], road))
            for w, pts, _road in runs:
                v, t = ribbon(pts, w, height_fn)
                base = len(rv)
                rv += v
                rt += [(a + base, b + base, c + base) for a, b, c in t]
            write_obj(out_dir / f"{cid}_roads.obj", rv, rt, f"{cid}_roads")
            layers["roads"] = f"{cid}_roads.obj"
            all_verts += rv

        blds = bld_in_chunk.get((i, j), [])
        if blds:
            bv: list = []
            bt: list = []
            for b in blds:
                v, t = extrude(b, height_fn)
                base = len(bv)
                bv += v
                bt += [(a + base, b2 + base, c + base) for a, b2, c in t]
            write_obj(out_dir / f"{cid}_buildings.obj", bv, bt, f"{cid}_buildings")
            layers["buildings"] = f"{cid}_buildings.obj"
            all_verts += bv

        chunks.append({"id": cid, "i": i, "j": j, "layers": layers, "aabb": aabb(all_verts)})

    manifest = {
        "generator": f"mapgen {__version__}",
        "version": 1,
        "crs": "EPSG:27700, local origin at SW corner of bounds",
        "origin_easting": round(frame.origin_easting, 3),
        "origin_northing": round(frame.origin_northing, 3),
        "extent_x": round(frame.extent_x, 3),
        "extent_y": round(frame.extent_y, 3),
        "chunk_size": cs,
        "axis_note": "OBJ/Godot: x=east, y=up, z=-north (see meshio.py)",
        "counts": {
            "chunks": len(chunks),
            "roads": len(feats.roads),
            "buildings": len(feats.buildings),
        },
        "chunks": chunks,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest
