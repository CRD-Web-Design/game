"""Building footprint -> extruded grey-box shell (walls + earcut roof)."""

from __future__ import annotations

import numpy as np
from mapbox_earcut import triangulate_float64

from .model import Building, building_height
from .terrain import HeightFn

# How far below lowest ground the shell is embedded (hides terrain gaps on slopes).
EMBED = 1.0


def extrude(
    b: Building,
    height_fn: HeightFn,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    """Extrude a footprint into a closed shell.

    Base sits EMBED below the lowest terrain sample under the footprint;
    the roof is `building_height(b)` above the *highest* sample, so shells
    on slopes never poke terrain through their roofs.
    """
    if not b.rings or len(b.rings[0]) < 3:
        return [], []

    all_pts = [p for ring in b.rings for p in ring]
    ground = [height_fn(x, y) for x, y in all_pts]
    z0 = min(ground) - EMBED
    z1 = max(ground) + building_height(b)

    verts: list[tuple[float, float, float]] = []
    tris: list[tuple[int, int, int]] = []

    # Walls: one quad per edge of every ring.
    for ring in b.rings:
        n = len(ring)
        for i in range(n):
            x0, y0 = ring[i]
            x1, y1 = ring[(i + 1) % n]
            base = len(verts)
            verts.extend([(x0, y0, z0), (x1, y1, z0), (x1, y1, z1), (x0, y0, z1)])
            # Exterior rings are CCW: this winding faces outward.
            tris.append((base, base + 1, base + 2))
            tris.append((base, base + 2, base + 3))

    # Roof: earcut over exterior + holes.
    flat = np.array(all_pts, dtype=np.float64)
    ring_ends = np.cumsum([len(r) for r in b.rings]).astype(np.uint32)
    roof_idx = triangulate_float64(flat, ring_ends)
    roof_base = len(verts)
    verts.extend([(x, y, z1) for x, y in all_pts])
    for k in range(0, len(roof_idx), 3):
        # earcut preserves the outer ring's CCW orientation: already up-facing.
        a, bb, c = int(roof_idx[k]), int(roof_idx[k + 1]), int(roof_idx[k + 2])
        tris.append((roof_base + a, roof_base + bb, roof_base + c))

    return verts, tris
