"""Building footprint -> shell parts: walls, roof, and (for enterable
pubs/shops) a door opening plus interior floor.

Output is split by part so the runtime can texture walls (brick) and roofs
(slate) separately, and so enterable buildings actually have somewhere to
stand inside (PRD 07: pubs and shops accessible and enterable).
"""

from __future__ import annotations

import math

import numpy as np
from mapbox_earcut import triangulate_float64

from .model import Building, building_height, poi_kind
from .terrain import HeightFn

# How far below lowest ground the shell is embedded (hides terrain gaps on slopes).
EMBED = 1.0
DOOR_WIDTH = 1.4
DOOR_HEIGHT = 2.2
FLOOR_LIFT = 0.05          # floor sits just above ground at the door
MIN_ENTERABLE_AREA = 25.0  # m^2
MAX_ENTERABLE_AREA = 1500.0

Part = tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]


def _ring_area(ring: list[tuple[float, float]]) -> float:
    s = 0.0
    for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]):
        s += x0 * y1 - x1 * y0
    return abs(s) / 2.0


def is_enterable(b: Building) -> bool:
    """Pubs and shops with a sane, hole-free footprint get a real doorway."""
    if poi_kind(b.tags) is None:
        return False
    if len(b.rings) != 1 or len(b.rings[0]) < 3:
        return False
    return MIN_ENTERABLE_AREA <= _ring_area(b.rings[0]) <= MAX_ENTERABLE_AREA


def door_edge_index(ring: list[tuple[float, float]]) -> int:
    """Door goes in the longest edge — the best proxy we have for the
    street-facing frontage until the road graph informs it (M3)."""
    best, best_len = 0, -1.0
    for i in range(len(ring)):
        x0, y0 = ring[i]
        x1, y1 = ring[(i + 1) % len(ring)]
        l = math.hypot(x1 - x0, y1 - y0)
        if l > best_len:
            best, best_len = i, l
    return best


def door_position(b: Building) -> tuple[float, float] | None:
    """Door midpoint in plan, for signage and runtime dressing."""
    if not is_enterable(b):
        return None
    ring = b.rings[0]
    i = door_edge_index(ring)
    x0, y0 = ring[i]
    x1, y1 = ring[(i + 1) % len(ring)]
    return (x0 + x1) / 2.0, (y0 + y1) / 2.0


def _wall_quad(verts, tris, p0, p1, z_bot, z_top):
    if z_top - z_bot < 1e-6:
        return
    base = len(verts)
    verts.extend([
        (p0[0], p0[1], z_bot), (p1[0], p1[1], z_bot),
        (p1[0], p1[1], z_top), (p0[0], p0[1], z_top),
    ])
    tris.append((base, base + 1, base + 2))
    tris.append((base, base + 2, base + 3))


def _cap(pts_rings: list[list[tuple[float, float]]], z: float, up: bool) -> Part:
    """Horizontal cap (roof or floor) over rings via earcut."""
    all_pts = [p for ring in pts_rings for p in ring]
    flat = np.array(all_pts, dtype=np.float64)
    ends = np.cumsum([len(r) for r in pts_rings]).astype(np.uint32)
    idx = triangulate_float64(flat, ends)
    verts = [(x, y, z) for x, y in all_pts]
    tris = []
    for k in range(0, len(idx), 3):
        a, b, c = int(idx[k]), int(idx[k + 1]), int(idx[k + 2])
        # earcut preserves CCW input orientation: up-facing as emitted.
        tris.append((a, b, c) if up else (c, b, a))
    return verts, tris


def extrude_parts(b: Building, height_fn: HeightFn) -> dict[str, Part]:
    """Extrude a footprint into parts: {"walls": ..., "roof": ..., "floor"?: ...}.

    Sealed buildings get solid walls + roof (as before). Enterable ones get a
    doorway (gap + lintel) in their longest edge and an interior floor slab.
    """
    if not b.rings or len(b.rings[0]) < 3:
        return {}

    all_pts = [p for ring in b.rings for p in ring]
    ground = [height_fn(x, y) for x, y in all_pts]
    z0 = min(ground) - EMBED
    z1 = max(ground) + building_height(b)

    wv: list = []
    wt: list = []
    parts: dict[str, Part] = {}

    enterable = is_enterable(b)
    door_i = door_edge_index(b.rings[0]) if enterable else -1

    for ring_n, ring in enumerate(b.rings):
        n = len(ring)
        for i in range(n):
            p0, p1 = ring[i], ring[(i + 1) % n]
            if ring_n == 0 and i == door_i and enterable:
                # Doorway: left jamb wall, right jamb wall, lintel above.
                ex, ey = p1[0] - p0[0], p1[1] - p0[1]
                elen = math.hypot(ex, ey)
                w = min(DOOR_WIDTH, elen * 0.5)
                ta = 0.5 - (w / 2.0) / elen
                tb = 0.5 + (w / 2.0) / elen
                a = (p0[0] + ex * ta, p0[1] + ey * ta)
                c = (p0[0] + ex * tb, p0[1] + ey * tb)
                mid = ((a[0] + c[0]) / 2.0, (a[1] + c[1]) / 2.0)
                floor_z = height_fn(mid[0], mid[1]) + FLOOR_LIFT
                lintel_z = min(floor_z + DOOR_HEIGHT, z1 - 0.3)
                _wall_quad(wv, wt, p0, a, z0, z1)
                _wall_quad(wv, wt, c, p1, z0, z1)
                _wall_quad(wv, wt, a, c, lintel_z, z1)
                parts["floor"] = _cap([b.rings[0]], floor_z, up=True)
            else:
                _wall_quad(wv, wt, p0, p1, z0, z1)

    parts["walls"] = (wv, wt)
    parts["roof"] = _cap(b.rings, z1, up=True)
    return parts
