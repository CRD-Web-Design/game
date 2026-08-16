"""Real-data ingest path (load_osm_pbf), tested against a synthetic .pbf.

Builds a tiny OSM PBF with pyosmium's writer — a named road, a closed
building way, and a far-away road that must be clipped — then runs the same
code path a real Geofabrik extract goes through.

Skipped automatically when the [real] extra isn't installed.
"""

import pytest

osmium = pytest.importorskip("osmium")

from pyproj import Transformer

from mapgen.config import Config
from mapgen.crs import LocalFrame
from mapgen.ingest import load_osm_pbf

from pathlib import Path

CONFIG = Path(__file__).resolve().parents[1] / "atherton.toml"
_TO_WGS = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)


@pytest.fixture(scope="module")
def frame():
    return LocalFrame.from_bounds(Config.load(CONFIG).bounds)


@pytest.fixture(scope="module")
def pbf(tmp_path_factory, frame):
    """Write a minimal .osm.pbf around the town-centre position."""
    def lonlat(x, y):
        return _TO_WGS.transform(frame.origin_easting + x, frame.origin_northing + y)

    path = tmp_path_factory.mktemp("pbf") / "tiny.osm.pbf"
    w = osmium.SimpleWriter(str(path))
    m = osmium.osm.mutable

    nodes = {
        # road through town centre
        1: lonlat(2000.0, 1500.0),
        2: lonlat(2200.0, 1600.0),
        3: lonlat(2400.0, 1700.0),
        # closed building way (10 m x 8 m)
        10: lonlat(2100.0, 1550.0),
        11: lonlat(2110.0, 1550.0),
        12: lonlat(2110.0, 1558.0),
        13: lonlat(2100.0, 1558.0),
        # far outside the frame (should be clipped)
        20: lonlat(60000.0, 60000.0),
        21: lonlat(60100.0, 60000.0),
    }
    for nid, (lon, lat) in sorted(nodes.items()):
        w.add_node(m.Node(id=nid, location=(lon, lat), version=1))

    w.add_way(m.Way(id=100, nodes=[1, 2, 3], version=1,
                    tags={"highway": "primary", "name": "Test Street"}))
    w.add_way(m.Way(id=101, nodes=[10, 11, 12, 13, 10], version=1,
                    tags={"building": "pub", "name": "Test Arms",
                          "building:levels": "2"}))
    w.add_way(m.Way(id=102, nodes=[20, 21], version=1,
                    tags={"highway": "residential"}))
    w.close()
    return path


class TestPbfIngest:
    def test_road_loaded_and_far_road_clipped(self, pbf, frame):
        feats = load_osm_pbf(pbf, frame)
        assert len(feats.roads) == 1
        road = feats.roads[0]
        assert road.name == "Test Street"
        assert road.highway == "primary"
        assert len(road.points) == 3
        # Round-trips WGS84 -> BNG within transform tolerance
        assert abs(road.points[0][0] - 2000.0) < 2.0
        assert abs(road.points[0][1] - 1500.0) < 2.0

    def test_closed_way_becomes_building(self, pbf, frame):
        feats = load_osm_pbf(pbf, frame)
        assert len(feats.buildings) == 1
        b = feats.buildings[0]
        assert b.tags["building"] == "pub"
        assert len(b.rings) == 1
        assert len(b.rings[0]) == 4  # unclosed rectangle
        # Ring oriented CCW as the mesher requires
        area2 = sum(
            x0 * y1 - x1 * y0
            for (x0, y0), (x1, y1) in zip(b.rings[0], b.rings[0][1:] + b.rings[0][:1])
        )
        assert area2 > 0

    def test_building_feeds_mesher(self, pbf, frame):
        """The ingested pub extrudes with a doorway — full path check."""
        from mapgen.buildings import extrude_parts, is_enterable

        feats = load_osm_pbf(pbf, frame)
        b = feats.buildings[0]
        assert is_enterable(b)  # 10 m x 8 m pub
        parts = extrude_parts(b, lambda x, y: 42.0)
        assert parts["walls"][1] and parts["roof"][1] and parts["floor"][1]
        top = max(z for _, _, z in parts["roof"][0])
        assert abs(top - (42.0 + 6.0)) < 1e-6  # 2 levels * 3 m
