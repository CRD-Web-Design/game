"""Ingest: GeoJSON fixture (always available) or real .osm.pbf (mapgen[real]).

Both paths emit the same Features IR in local metres, so everything
downstream is source-agnostic.
"""

from __future__ import annotations

import json
from pathlib import Path

from .crs import LocalFrame
from .model import Building, Features, Road


def _ring_area2(ring: list[tuple[float, float]]) -> float:
    """Twice the signed area (positive = CCW)."""
    s = 0.0
    for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]):
        s += x0 * y1 - x1 * y0
    return s


def _orient(ring: list[tuple[float, float]], ccw: bool) -> list[tuple[float, float]]:
    if (_ring_area2(ring) > 0) != ccw:
        return ring[::-1]
    return ring


def load_geojson(path: str | Path, frame: LocalFrame) -> Features:
    """Load a GeoJSON FeatureCollection (WGS84) of roads + buildings.

    Used for the bundled test fixture and equally valid for hand-made
    override layers (data/registers/overrides.geojson, ADR-0002).
    """
    with open(path, encoding="utf-8") as f:
        fc = json.load(f)

    feats = Features()
    for feat in fc.get("features", []):
        props = feat.get("properties") or {}
        geom = feat.get("geometry") or {}
        gtype = geom.get("type")
        fid = str(props.get("@id", props.get("id", len(feats.roads) + len(feats.buildings))))

        if gtype == "LineString" and "highway" in props:
            pts = [frame.to_local(lon, lat) for lon, lat in geom["coordinates"]]
            feats.roads.append(
                Road(fid, props.get("name", ""), props["highway"], pts)
            )
        elif gtype == "Polygon" and ("building" in props or "amenity" in props):
            rings = []
            for i, ring in enumerate(geom["coordinates"]):
                pts = [frame.to_local(lon, lat) for lon, lat in ring]
                if pts and pts[0] == pts[-1]:
                    pts = pts[:-1]  # unclose
                rings.append(_orient(pts, ccw=(i == 0)))
            tags = {k: str(v) for k, v in props.items() if not k.startswith("@")}
            feats.buildings.append(Building(fid, tags, rings))

    # Determinism: stable ordering regardless of source file ordering.
    feats.roads.sort(key=lambda r: r.osm_id)
    feats.buildings.sort(key=lambda b: b.osm_id)
    return feats


def load_osm_pbf(path: str | Path, frame: LocalFrame, margin: float = 60.0) -> Features:
    """Load an .osm.pbf extract and clip it to the map bounds.

    Works directly on the whole Geofabrik Greater Manchester extract — no
    `osmium extract` pre-clip needed. Features with no point inside the
    local frame (+ margin metres) are dropped at ingest.

    Requires `pip install -e tools/mapgen[real]`. See
    docs/reference/data-sources-and-licences.md for where to get the data.
    """
    try:
        import osmium
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "osmium is not installed. Real-data ingest needs the [real] extra:\n"
            "  pip install -e tools/mapgen[real]"
        ) from exc

    hi_x, hi_y = frame.extent_x + margin, frame.extent_y + margin

    def in_frame(pts: list[tuple[float, float]]) -> bool:
        return any(-margin <= x <= hi_x and -margin <= y <= hi_y for x, y in pts)

    def ring_pts(ring) -> list[tuple[float, float]]:
        pts = [frame.to_local(n.lon, n.lat) for n in ring]
        if pts and pts[0] == pts[-1]:
            pts = pts[:-1]  # unclose
        return pts

    roads: list[Road] = []
    buildings: list[Building] = []

    class Handler(osmium.SimpleHandler):
        # Roads come from ways; buildings come from the area callback, which
        # assembles BOTH closed building ways and multipolygon relations
        # (courtyards/holes included), so nothing is double-counted.
        def way(self, w):
            tags = {t.k: t.v for t in w.tags}
            if "highway" not in tags:
                return
            try:
                pts = [frame.to_local(n.lon, n.lat) for n in w.nodes]
            except osmium.InvalidLocationError:
                return
            if len(pts) >= 2 and in_frame(pts):
                roads.append(Road(str(w.id), tags.get("name", ""), tags["highway"], pts))

        def area(self, a):
            tags = {t.k: t.v for t in a.tags}
            if "building" not in tags:
                return
            prefix = "w" if a.from_way() else "r"
            try:
                for n_outer, outer in enumerate(a.outer_rings()):
                    rings = [_orient(ring_pts(outer), ccw=True)]
                    if len(rings[0]) < 3 or not in_frame(rings[0]):
                        continue
                    for inner in a.inner_rings(outer):
                        hole = _orient(ring_pts(inner), ccw=False)
                        if len(hole) >= 3:
                            rings.append(hole)
                    buildings.append(
                        Building(f"{prefix}{a.orig_id()}_{n_outer}", tags, rings)
                    )
            except osmium.InvalidLocationError:
                return

    Handler().apply_file(str(path), locations=True)
    roads.sort(key=lambda r: r.osm_id)
    buildings.sort(key=lambda b: b.osm_id)
    return Features(roads, buildings)
