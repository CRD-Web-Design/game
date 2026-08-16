"""Build configuration loading."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Bounds:
    north: float
    south: float
    west: float
    east: float


@dataclass(frozen=True)
class Config:
    bounds: Bounds
    chunk_size: float
    terrain_step: float
    terrain_source: str      # "fixture" | "geotiff"
    geotiff_glob: str
    out_dir: str

    @staticmethod
    def load(path: str | Path) -> "Config":
        with open(path, "rb") as f:
            raw = tomllib.load(f)
        b = raw["bounds"]
        return Config(
            bounds=Bounds(b["north"], b["south"], b["west"], b["east"]),
            chunk_size=float(raw["grid"]["chunk_size"]),
            terrain_step=float(raw["grid"]["terrain_step"]),
            terrain_source=raw["terrain"]["source"],
            geotiff_glob=raw["terrain"].get("geotiff_glob", ""),
            out_dir=raw["export"]["out"],
        )
