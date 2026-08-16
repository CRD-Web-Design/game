"""Unit tests for the geometry stages."""

import math

from mapgen.buildings import EMBED, extrude
from mapgen.model import Building, Road, building_height, classify
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

    def test_counts(self):
        v, t = extrude(self._square(), FLAT)
        # walls: 4 edges * 4 verts, roof: 4 verts; tris: 8 wall + 2 roof
        assert len(v) == 20 and len(t) == 10

    def test_heights(self):
        b = self._square({"building:levels": "2"})
        v, _ = extrude(b, FLAT)
        zs = sorted({z for _, _, z in v})
        assert zs[0] == 50.0 - EMBED
        assert abs(zs[-1] - (50.0 + 6.0)) < 1e-9  # 2 levels * 3 m

    def test_roof_faces_up(self):
        v, t = extrude(self._square(), FLAT)
        top = max(z for _, _, z in v)
        roof = [tri for tri in t if all(abs(v[i][2] - top) < 1e-9 for i in tri)]
        assert roof and all(_tri_normal_z(v, tri) > 0 for tri in roof)

    def test_roof_area_matches_footprint(self):
        v, t = extrude(self._square(), FLAT)
        top = max(z for _, _, z in v)
        area = 0.0
        for tri in t:
            if all(abs(v[i][2] - top) < 1e-9 for i in tri):
                area += abs(_tri_normal_z(v, tri)) / 2
        assert abs(area - 100.0) < 1e-6

    def test_slope_roof_clears_terrain(self):
        slope = lambda x, y: 50.0 + x  # noqa: E731
        v, _ = extrude(self._square(), slope)
        top = max(z for _, _, z in v)
        assert top >= 60.0  # highest ground (x=10 -> 60) + height > 60

    def test_hole_ring(self):
        b = Building(
            "t2", {},
            [[(0, 0), (20, 0), (20, 20), (0, 20)],
             [(8, 8), (8, 12), (12, 12), (12, 8)]],  # CW hole
        )
        v, t = extrude(b, FLAT)
        top = max(z for _, _, z in v)
        area = sum(abs(_tri_normal_z(v, tri)) / 2 for tri in t
                   if all(abs(v[i][2] - top) < 1e-9 for i in tri))
        assert abs(area - (400.0 - 16.0)) < 1e-6


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
