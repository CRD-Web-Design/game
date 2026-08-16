"""Unit tests for the geometry stages."""

import math

from mapgen.buildings import (
    DOOR_HEIGHT,
    DOOR_WIDTH,
    EMBED,
    extrude_parts,
    is_enterable,
)
from mapgen.model import Building, Road, building_height, classify, poi_kind
from mapgen.roads import DRAPE_OFFSET, ribbon
from mapgen.terrain import chunk_terrain_mesh

FLAT = lambda x, y: 50.0  # noqa: E731


def _tri_normal_z(verts, tri):
    (x0, y0, _), (x1, y1, _), (x2, y2, _) = (verts[i] for i in tri)
    return (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)


class TestRibbon:
    def test_straight_two_point(self):
        v, t = ribbon([(0, 0), (100, 0)], 6.0, FLAT)
        assert len(v) == 4 and len(t) == 2
        # Width: left/right pair distance
        (lx, ly, _), (rx, ry, _) = v[0], v[1]
        assert math.hypot(lx - rx, ly - ry) == 200 / 200 * 6.0
        # Draped on terrain + offset
        assert all(abs(z - (50.0 + DRAPE_OFFSET)) < 1e-9 for _, _, z in v)

    def test_polyline_vertex_count(self):
        pts = [(0, 0), (50, 0), (100, 30), (150, 30)]
        v, t = ribbon(pts, 7.3, FLAT)
        assert len(v) == 2 * len(pts)
        assert len(t) == 2 * (len(pts) - 1)

    def test_faces_up(self):
        v, t = ribbon([(0, 0), (80, 40), (160, 40)], 5.5, FLAT)
        assert all(_tri_normal_z(v, tri) > 0 for tri in t)

    def test_duplicate_points_dropped(self):
        v, t = ribbon([(0, 0), (0, 0), (100, 0)], 6.0, FLAT)
        assert len(v) == 4

    def test_miter_clamped_on_hairpin(self):
        v, _ = ribbon([(0, 0), (100, 0), (0, 5)], 6.0, FLAT)
        # Sharp corner: miter must not explode beyond MITER_LIMIT * half-width
        (lx, ly, _), (rx, ry, _) = v[2], v[3]
        assert math.hypot(lx - rx, ly - ry) <= 6.0 * 2.0 + 1e-6


class TestExtrude:
    def _square(self, tags=None):
        return Building("t1", tags or {}, [[(0, 0), (10, 0), (10, 10), (0, 10)]])

    def test_sealed_counts(self):
        parts = extrude_parts(self._square(), FLAT)
        wv, wt = parts["walls"]
        rv, rt = parts["roof"]
        assert "floor" not in parts
        assert len(wv) == 16 and len(wt) == 8  # 4 solid wall quads
        assert len(rv) == 4 and len(rt) == 2

    def test_heights(self):
        b = self._square({"building:levels": "2"})
        parts = extrude_parts(b, FLAT)
        zs = sorted({z for _, _, z in parts["walls"][0]})
        assert zs[0] == 50.0 - EMBED
        assert abs(parts["roof"][0][0][2] - (50.0 + 6.0)) < 1e-9  # 2 levels * 3 m

    def test_roof_faces_up_and_matches_area(self):
        parts = extrude_parts(self._square(), FLAT)
        rv, rt = parts["roof"]
        area = 0.0
        for tri in rt:
            assert _tri_normal_z(rv, tri) > 0
            area += abs(_tri_normal_z(rv, tri)) / 2
        assert abs(area - 100.0) < 1e-6

    def test_slope_roof_clears_terrain(self):
        slope = lambda x, y: 50.0 + x  # noqa: E731
        parts = extrude_parts(self._square(), slope)
        assert parts["roof"][0][0][2] >= 60.0  # highest ground + height

    def test_hole_ring(self):
        b = Building(
            "t2", {},
            [[(0, 0), (20, 0), (20, 20), (0, 20)],
             [(8, 8), (8, 12), (12, 12), (12, 8)]],  # CW hole
        )
        rv, rt = extrude_parts(b, FLAT)["roof"]
        area = sum(abs(_tri_normal_z(rv, tri)) / 2 for tri in rt)
        assert abs(area - (400.0 - 16.0)) < 1e-6


class TestEnterable:
    def _pub(self):
        return Building(
            "p1", {"amenity": "pub", "name": "Test Arms"},
            [[(0, 0), (10, 0), (10, 8), (0, 8)]],
        )

    def test_classification(self):
        assert is_enterable(self._pub())
        assert not is_enterable(Building("h", {"building": "terrace"},
                                         [[(0, 0), (10, 0), (10, 8), (0, 8)]]))
        # Too small to be a real pub interior
        tiny = Building("t", {"amenity": "pub"}, [[(0, 0), (2, 0), (2, 2), (0, 2)]])
        assert not is_enterable(tiny)

    def test_door_gap_exists(self):
        parts = extrude_parts(self._pub(), FLAT)
        wv, wt = parts["walls"]
        # Door edge is the longest (y=0, length 10): no wall geometry may
        # cross the door centre (x=5) below lintel height on that edge.
        door_zone = [
            (v0, v1, v2) for (v0, v1, v2) in
            ((wv[a], wv[b], wv[c]) for a, b, c in wt)
            if all(abs(v[1]) < 1e-6 for v in (v0, v1, v2))       # on y=0 edge
            and min(v[0] for v in (v0, v1, v2)) < 5.0 < max(v[0] for v in (v0, v1, v2))
        ]
        floor_z = 50.0 + 0.05
        for tri in door_zone:
            # Anything spanning the doorway must be lintel (above door height)
            assert min(v[2] for v in tri) >= floor_z + DOOR_HEIGHT - 1e-6

    def test_door_width_and_jambs(self):
        parts = extrude_parts(self._pub(), FLAT)
        wv, _ = parts["walls"]
        edge_x = sorted({round(v[0], 4) for v in wv if abs(v[1]) < 1e-6})
        # Jamb inner faces at 5 +/- DOOR_WIDTH/2
        assert round(5.0 - DOOR_WIDTH / 2, 4) in edge_x
        assert round(5.0 + DOOR_WIDTH / 2, 4) in edge_x

    def test_floor_present_and_walkable_height(self):
        parts = extrude_parts(self._pub(), FLAT)
        fv, ft = parts["floor"]
        assert ft, "enterable building must have a floor"
        assert all(abs(z - 50.05) < 1e-6 for _, _, z in fv)
        assert all(_tri_normal_z(fv, tri) > 0 for tri in ft)  # faces up
        area = sum(abs(_tri_normal_z(fv, tri)) / 2 for tri in ft)
        assert abs(area - 80.0) < 1e-6

    def test_poi_kind(self):
        assert poi_kind({"amenity": "pub"}) == "pub"
        assert poi_kind({"building": "retail"}) == "shop"
        assert poi_kind({"shop": "bakery", "building": "yes"}) == "shop"
        assert poi_kind({"building": "terrace"}) is None


class TestTerrain:
    def test_grid_counts(self):
        v, t = chunk_terrain_mesh(0, 0, 256.0, 8.0, FLAT)
        n = 32
        assert len(v) == (n + 1) ** 2
        assert len(t) == 2 * n * n

    def test_edge_vertices_shared_between_chunks(self):
        h = lambda x, y: 30 + 0.01 * x + 0.02 * y  # noqa: E731
        va, _ = chunk_terrain_mesh(0, 0, 256.0, 8.0, h)
        vb, _ = chunk_terrain_mesh(1, 0, 256.0, 8.0, h)
        east_edge = sorted((x, y, z) for x, y, z in va if abs(x - 256.0) < 1e-9)
        west_edge = sorted((x, y, z) for x, y, z in vb if abs(x - 256.0) < 1e-9)
        assert east_edge == west_edge  # watertight seam

    def test_faces_up(self):
        v, t = chunk_terrain_mesh(2, 3, 256.0, 32.0, FLAT)
        assert all(_tri_normal_z(v, tri) > 0 for tri in t)


class TestModel:
    def test_classify(self):
        assert classify({"amenity": "pub"}) == "pub"
        assert classify({"building": "terrace"}) == "terrace"
        assert classify({"amenity": "townhall", "building": "civic"}) == "civic"
        assert classify({"building": "yes"}) == "default"

    def test_height_precedence(self):
        assert building_height(Building("x", {"height": "9.5"}, [])) == 9.5
        assert building_height(Building("x", {"building:levels": "3"}, [])) == 9.0
        assert building_height(Building("x", {"building": "pub"}, [])) == 7.5
        assert building_height(Building("x", {}, [])) == 6.0
