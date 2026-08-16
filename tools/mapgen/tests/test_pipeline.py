"""End-to-end pipeline tests on the bundled fixture."""

import json
from pathlib import Path

import pytest

from mapgen.cli import main

CONFIG = Path(__file__).resolve().parents[1] / "atherton.toml"


def _build(tmp_path: Path) -> Path:
    out = tmp_path / "generated"
    rc = main(["build", "--config", str(CONFIG), "--fixture", "--out", str(out)])
    assert rc == 0
    return out


def _parse_obj(path: Path):
    verts, faces = [], []
    for line in path.read_text().splitlines():
        if line.startswith("v "):
            verts.append(tuple(float(p) for p in line.split()[1:4]))
        elif line.startswith("f "):
            faces.append(tuple(int(p.split("/")[0]) for p in line.split()[1:]))
    return verts, faces


@pytest.fixture(scope="module")
def out(tmp_path_factory):
    return _build(tmp_path_factory.mktemp("e2e"))


class TestEndToEnd:
    def test_manifest_exists_and_valid(self, out):
        m = json.loads((out / "manifest.json").read_text())
        assert m["version"] == 1
        assert m["counts"]["roads"] == 4
        assert m["counts"]["buildings"] == 12
        assert m["counts"]["chunks"] >= 1
        assert m["chunk_size"] == 256.0

    def test_frame_is_atherton_sized(self, out):
        m = json.loads((out / "manifest.json").read_text())
        # PRD 03: ~3.64 km E-W, ~3.34 km N-S
        assert 3300 < m["extent_x"] < 4000
        assert 3100 < m["extent_y"] < 3600

    def test_all_layer_files_exist_and_parse(self, out):
        m = json.loads((out / "manifest.json").read_text())
        seen_layers = set()
        for chunk in m["chunks"]:
            for layer, fname in chunk["layers"].items():
                seen_layers.add(layer)
                verts, faces = _parse_obj(out / fname)
                assert verts and faces, f"{fname} is empty"
                # All faces triangles, all indices in range
                for f in faces:
                    assert len(f) == 3
                    assert all(1 <= i <= len(verts) for i in f)
        assert seen_layers == {"terrain", "roads", "buildings"}

    def test_town_centre_chunk_is_populated(self, out):
        """The fixture town centre (~2165 E, 1560 N) lands in chunk c_8_6."""
        m = json.loads((out / "manifest.json").read_text())
        centre = next((c for c in m["chunks"] if c["id"] == "c_8_6"), None)
        assert centre is not None
        assert "buildings" in centre["layers"]

    def test_terrain_gradient_present(self, out):
        """Fixture terrain rises south->north (30->76 m, PRD 02)."""
        m = json.loads((out / "manifest.json").read_text())
        chunks = sorted(m["chunks"], key=lambda c: c["j"])
        lo = chunks[0]["aabb"]
        hi = chunks[-1]["aabb"]
        if chunks[0]["j"] < chunks[-1]["j"]:
            assert hi[5] > lo[5]  # max height grows northward

    def test_aabb_heights_sane(self, out):
        m = json.loads((out / "manifest.json").read_text())
        for c in m["chunks"]:
            zmin, zmax = c["aabb"][2], c["aabb"][5]
            assert 20.0 < zmin < zmax < 120.0

    def test_deterministic(self, tmp_path):
        out1 = tmp_path / "a"
        out2 = tmp_path / "b"
        main(["build", "--config", str(CONFIG), "--fixture", "--out", str(out1)])
        main(["build", "--config", str(CONFIG), "--fixture", "--out", str(out2)])
        files1 = sorted(p.name for p in out1.iterdir())
        files2 = sorted(p.name for p in out2.iterdir())
        assert files1 == files2
        for name in files1:
            assert (out1 / name).read_bytes() == (out2 / name).read_bytes(), name
