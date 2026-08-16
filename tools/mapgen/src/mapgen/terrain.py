"""Terrain height functions and chunk terrain meshes.

A height function maps local (x, y) metres -> height metres AOD. The rest of
the pipeline (road draping, building bases) samples the same function, so
terrain and features can never disagree.
"""

from __future__ import annotations

import math
from typing import Callable

from .crs import LocalFrame

HeightFn = Callable[[float, float], float]


def fixture_height_fn(frame: LocalFrame) -> HeightFn:
    """Synthetic Atherton-like terrain for grey-box and tests.

    Real profile per PRD 02/03: ~30 m AOD in the southwest rising to ~76 m
    in the north, gentle clay-country undulation. Deterministic.
    """
    lo, hi = 30.0, 76.0
    ey = max(frame.extent_y, 1.0)

    def h(x: float, y: float) -> float:
        base = lo + (hi - lo) * min(max(y / ey, 0.0), 1.0)
        undulation = 1.5 * math.sin(x / 180.0) * math.cos(y / 240.0)
        return base + undulation

    return h


def geotiff_height_fn(glob_pattern: str, frame: LocalFrame) -> HeightFn:
    """EA LiDAR Composite DTM tiles (EPSG:27700 GeoTIFF).

    Requires mapgen[real]. Tiles are sampled in BNG coordinates; the local
    frame origin is added back before lookup.
    """
    try:
        import rasterio  # noqa: F401
        from rasterio.merge import merge
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "rasterio is not installed. GeoTIFF terrain needs the [real] extra:\n"
            "  pip install -e tools/mapgen[real]"
        ) from exc

    import glob as _glob

    import numpy as np
    import rasterio

    paths = sorted(_glob.glob(glob_pattern))
    if not paths:
        raise SystemExit(f"No GeoTIFF tiles match {glob_pattern!r}")

    datasets = [rasterio.open(p) for p in paths]
    mosaic, transform = merge(datasets)  # pragma: no cover - needs real data
    band = mosaic[0]
    inv = ~transform

    def h(x: float, y: float) -> float:  # pragma: no cover - needs real data
        col, row = inv * (x + frame.origin_easting, y + frame.origin_northing)
        r, c = int(row), int(col)
        if 0 <= r < band.shape[0] and 0 <= c < band.shape[1]:
            v = float(band[r, c])
            if not np.isnan(v) and v > -100:
                return v
        return 40.0  # benign fallback for nodata pockets

    return h


def chunk_terrain_mesh(
    ci: int,
    cj: int,
    chunk_size: float,
    step: float,
    height_fn: HeightFn,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    """Regular-grid terrain patch for chunk (ci, cj).

    Returns (vertices, triangles) in local metres, z = height. Vertices are
    ordered row-major from the chunk's SW corner; edge vertices are shared
    exactly (same sample positions) with neighbouring chunks, so seams are
    watertight by construction.
    """
    n = int(round(chunk_size / step))
    x0, y0 = ci * chunk_size, cj * chunk_size

    verts: list[tuple[float, float, float]] = []
    for j in range(n + 1):
        for i in range(n + 1):
            x, y = x0 + i * step, y0 + j * step
            verts.append((x, y, height_fn(x, y)))

    tris: list[tuple[int, int, int]] = []
    for j in range(n):
        for i in range(n):
            a = j * (n + 1) + i
            b = a + 1
            c = a + (n + 1)
            d = c + 1
            tris.append((a, b, d))
            tris.append((a, d, c))
    return verts, tris
