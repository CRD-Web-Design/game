"""Coordinate systems (see docs/reference/data-sources-and-licences.md).

Everything downstream of ingest works in *local metres*: British National
Grid (EPSG:27700) translated so the southwest corner of the map bounds is
(0, 0). x = east, y = north. Height (z) is metres AOD.

The Godot axis convention (x = east, y = up, z = -north) is applied at the
last moment, in meshio.py, and nowhere else.

Note: pyproj's default WGS84->OSGB36 transform (Helmert, without the OSTN15
grid file) is accurate to ~1-2 m. Fine for M0 grey-box; revisit if survey-
grade alignment is ever needed (pin OSTN15 in the toolchain then).
"""

from __future__ import annotations

from dataclasses import dataclass

from pyproj import Transformer

from .config import Bounds

_TO_BNG = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)


@dataclass(frozen=True)
class LocalFrame:
    """Local metric frame anchored at the SW corner of the map bounds."""

    origin_easting: float
    origin_northing: float
    extent_x: float   # metres, west->east
    extent_y: float   # metres, south->north

    @staticmethod
    def from_bounds(b: Bounds) -> "LocalFrame":
        e0, n0 = _TO_BNG.transform(b.west, b.south)
        e1, n1 = _TO_BNG.transform(b.east, b.north)
        return LocalFrame(e0, n0, e1 - e0, n1 - n0)

    def to_local(self, lon: float, lat: float) -> tuple[float, float]:
        e, n = _TO_BNG.transform(lon, lat)
        return e - self.origin_easting, n - self.origin_northing
