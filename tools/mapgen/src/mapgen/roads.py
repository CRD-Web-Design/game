"""Road centreline -> draped ribbon mesh."""

from __future__ import annotations

import math

from .model import DEFAULT_ROAD_WIDTH, ROAD_WIDTH, Road
from .terrain import HeightFn

# Ribbons float slightly above terrain to avoid z-fighting with the ground.
DRAPE_OFFSET = 0.05
# Miter length clamp for sharp corners (in half-width multiples).
MITER_LIMIT = 2.0


def _norm(vx: float, vy: float) -> tuple[float, float]:
    l = math.hypot(vx, vy)
    return (vx / l, vy / l) if l > 1e-9 else (0.0, 0.0)


def ribbon(
    points: list[tuple[float, float]],
    width: float,
    height_fn: HeightFn,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    """Constant-width ribbon along a polyline, draped on the terrain.

    Left/right edge pairs are emitted per centreline point (miter joins,
    clamped), then stitched into quads. Duplicate consecutive points are
    dropped.
    """
    pts = [points[0]]
    for p in points[1:]:
        if math.hypot(p[0] - pts[-1][0], p[1] - pts[-1][1]) > 1e-6:
            pts.append(p)
    if len(pts) < 2:
        return [], []

    hw = width / 2.0
    # Segment perpendiculars (left-hand normal of travel direction).
    seg_n = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dx, dy = _norm(x1 - x0, y1 - y0)
        seg_n.append((-dy, dx))

    verts: list[tuple[float, float, float]] = []
    for i, (x, y) in enumerate(pts):
        if i == 0:
            nx, ny = seg_n[0]
            scale = 1.0
        elif i == len(pts) - 1:
            nx, ny = seg_n[-1]
            scale = 1.0
        else:
            mx, my = _norm(seg_n[i - 1][0] + seg_n[i][0], seg_n[i - 1][1] + seg_n[i][1])
            if (mx, my) == (0.0, 0.0):  # 180-degree reversal
                mx, my = seg_n[i]
                scale = 1.0
            else:
                dot = mx * seg_n[i][0] + my * seg_n[i][1]
                scale = min(1.0 / max(dot, 1e-3), MITER_LIMIT)
            nx, ny = mx, my
        lx, ly = x + nx * hw * scale, y + ny * hw * scale
        rx, ry = x - nx * hw * scale, y - ny * hw * scale
        verts.append((lx, ly, height_fn(lx, ly) + DRAPE_OFFSET))
        verts.append((rx, ry, height_fn(rx, ry) + DRAPE_OFFSET))

    tris: list[tuple[int, int, int]] = []
    for i in range(len(pts) - 1):
        l0, r0, l1, r1 = 2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 3
        tris.append((l0, r0, r1))
        tris.append((l0, r1, l1))
    return verts, tris


def road_width(road: Road) -> float:
    return ROAD_WIDTH.get(road.highway, DEFAULT_ROAD_WIDTH)
