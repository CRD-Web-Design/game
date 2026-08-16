"""Atherton map pipeline (ADR-0002).

Compiles open geodata (OSM footprints/roads, EA LiDAR terrain) into
engine-ready chunked meshes + a JSON manifest consumed by the Godot side
(src/world/chunk_loader.gd).

Deterministic: same inputs + same config -> byte-identical output.
"""

__version__ = "0.1.0"
