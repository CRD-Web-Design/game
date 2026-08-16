"""Intermediate representation between ingest and mesh generation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Road:
    osm_id: str
    name: str
    highway: str                       # OSM highway class
    points: list[tuple[float, float]]  # local metres, centreline order


@dataclass
class Building:
    osm_id: str
    tags: dict[str, str]
    # First ring = exterior (CCW), rest = holes (CW). Local metres, unclosed.
    rings: list[list[tuple[float, float]]] = field(default_factory=list)


@dataclass
class Features:
    roads: list[Road] = field(default_factory=list)
    buildings: list[Building] = field(default_factory=list)


# Road ribbon width by OSM highway class, metres (PRD 03; UK standard lane widths).
ROAD_WIDTH: dict[str, float] = {
    "primary": 7.3,
    "secondary": 6.5,
    "tertiary": 6.0,
    "residential": 5.5,
    "unclassified": 5.0,
    "service": 4.0,
    "footway": 2.0,
    "path": 1.5,
}
DEFAULT_ROAD_WIDTH = 5.0

# Building height (metres to eaves) by typology when no data (ADR-0002).
TYPOLOGY_HEIGHT: dict[str, float] = {
    "terrace": 5.5,
    "semi": 5.2,
    "detached": 5.8,
    "estate": 5.2,
    "shopfront": 7.5,
    "pub": 7.5,
    "civic": 9.0,
    "industrial": 6.5,
    "default": 6.0,
}
METRES_PER_LEVEL = 3.0


def classify(tags: dict[str, str]) -> str:
    """Footprint typology from OSM-style tags (coarse M0 version).

    The full classifier (footprint shape + district priors) comes with the
    facade kits at M2/M3; tags alone are enough for grey-box heights.
    """
    amenity = tags.get("amenity", "")
    building = tags.get("building", "")
    if amenity == "pub" or building == "pub":
        return "pub"
    if amenity in ("townhall", "library", "place_of_worship", "police", "fire_station"):
        return "civic"
    if building in ("church", "chapel", "civic", "public"):
        return "civic"
    if building in ("retail", "commercial", "shop"):
        return "shopfront"
    if building in ("industrial", "warehouse"):
        return "industrial"
    if building == "terrace":
        return "terrace"
    if building == "semidetached_house":
        return "semi"
    if building == "detached":
        return "detached"
    return "default"


def building_height(b: Building) -> float:
    """Height in metres: explicit tag > levels > typology default."""
    if "height" in b.tags:
        try:
            return max(2.5, float(b.tags["height"].removesuffix(" m").removesuffix("m")))
        except ValueError:
            pass
    if "building:levels" in b.tags:
        try:
            return max(2.5, float(b.tags["building:levels"]) * METRES_PER_LEVEL)
        except ValueError:
            pass
    return TYPOLOGY_HEIGHT[classify(b.tags)]
