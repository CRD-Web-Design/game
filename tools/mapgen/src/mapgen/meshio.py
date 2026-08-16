"""OBJ mesh writer.

OBJ for M0 grey-box because it is trivially deterministic, diffable, and
parsed at runtime by src/world/obj_loader.gd with no import step. The
pipeline moves to glTF when materials/UVs arrive (M2, facade kits).

Axis convention (the ONLY place it changes — see crs.py):
  pipeline (x=east, y=north, z=up)  ->  Godot/OBJ (x=east, y=up, z=-north)
"""

from __future__ import annotations

from pathlib import Path

Vec3 = tuple[float, float, float]
Tri = tuple[int, int, int]


def write_obj(path: str | Path, verts: list[Vec3], tris: list[Tri], name: str) -> None:
    lines = [f"# mapgen grey-box: {name}", f"o {name}"]
    for x, y, z in verts:
        # east, up, -north; fixed precision for byte-identical rebuilds.
        lines.append(f"v {x:.3f} {z:.3f} {-y:.3f}")
    for a, b, c in tris:
        # OBJ is 1-indexed. Pipeline triangles wind CCW-outward; Godot's
        # front-face convention is CLOCKWISE, so emit reversed. (The axis map
        # itself is a pure rotation, det +1 — it does not flip winding.)
        lines.append(f"f {a + 1} {c + 1} {b + 1}")
    lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def aabb(verts: list[Vec3]) -> list[float] | None:
    """[min_x, min_y, min_z, max_x, max_y, max_z] in pipeline axes."""
    if not verts:
        return None
    xs, ys, zs = zip(*verts)
    return [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)]
