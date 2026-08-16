#!/usr/bin/env python3
"""Procedural placeholder textures (M2 grey-box -> textured pass).

Deterministic (fixed seed). Committed outputs live in assets/textures/ so
players never need to run this; re-run it only to tweak the look:

    python3 tools/gen_assets/gen_textures.py

All textures are designed for world-space triplanar mapping (no UVs in the
generated meshes yet), so subtle tiling seams are acceptable.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

OUT = Path(__file__).resolve().parents[2] / "assets" / "textures"
SIZE = 512
RNG = np.random.default_rng(46)  # M46, of course


def _noise(octaves: list[tuple[int, float]]) -> np.ndarray:
    """Value noise in [0,1] from summed re-scaled random grids (wrap-blended)."""
    acc = np.zeros((SIZE, SIZE), dtype=np.float64)
    total = 0.0
    for cells, weight in octaves:
        grid = RNG.random((cells, cells))
        img = Image.fromarray((grid * 255).astype(np.uint8)).resize(
            (SIZE, SIZE), Image.BILINEAR
        )
        img = img.filter(ImageFilter.GaussianBlur(radius=max(1, SIZE // cells // 4)))
        acc += np.asarray(img, dtype=np.float64) / 255.0 * weight
        total += weight
    return acc / total


def _save(name: str, rgb: np.ndarray) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    img.save(OUT / name, optimize=True)
    print(f"  {name}  ({(OUT / name).stat().st_size // 1024} KB)")


def grass() -> None:
    n = _noise([(8, 0.5), (32, 0.3), (128, 0.2)])
    base = np.stack([
        70 + 40 * n,     # R
        96 + 52 * n,     # G
        52 + 26 * n,     # B
    ], axis=-1)
    # Patchy dry spots
    dry = _noise([(6, 1.0)])
    mask = (dry > 0.62)[..., None]
    base = np.where(mask, base * [1.25, 1.12, 0.8], base)
    _save("grass.png", base)


def tarmac() -> None:
    n = _noise([(16, 0.4), (64, 0.35), (256, 0.25)])
    g = 52 + 30 * n
    base = np.stack([g, g, g * 1.04], axis=-1)
    # Sparse aggregate speckle
    speck = RNG.random((SIZE, SIZE)) > 0.995
    base[speck] = [120, 120, 122]
    _save("tarmac.png", base)


def brick() -> None:
    course_h, brick_w, mortar = 16, 44, 3
    img = np.zeros((SIZE, SIZE, 3), dtype=np.float64)
    reds = [(148, 74, 58), (136, 66, 52), (158, 82, 62), (128, 62, 50), (150, 70, 48)]
    for row in range(SIZE // course_h):
        y0 = row * course_h
        offset = (row % 2) * (brick_w // 2)
        x = -offset
        while x < SIZE:
            c = np.array(reds[RNG.integers(0, len(reds))], dtype=np.float64)
            c *= 0.92 + 0.16 * RNG.random()
            x0, x1 = max(x, 0), min(x + brick_w - mortar, SIZE)
            if x1 > x0:
                img[y0:y0 + course_h - mortar, x0:x1] = c
            x += brick_w
    # Mortar fill (zeros -> grey) + grime
    mortar_mask = img.sum(axis=-1) == 0
    img[mortar_mask] = [168, 160, 150]
    grime = _noise([(24, 1.0)])[..., None]
    img *= 0.82 + 0.3 * grime
    _save("brick.png", img)


def slate() -> None:
    course_h = 24
    n = _noise([(32, 0.5), (128, 0.5)])
    g = 58 + 26 * n
    img = np.stack([g * 0.94, g * 0.98, g * 1.08], axis=-1)
    # Course shadow lines
    for row in range(SIZE // course_h):
        y = row * course_h
        img[y:y + 2] *= 0.6
    _save("slate.png", img)


def planks() -> None:
    plank_w = 56
    n = _noise([(4, 0.35), (64, 0.4), (256, 0.25)])
    base = np.stack([120 + 50 * n, 86 + 36 * n, 54 + 22 * n], axis=-1)
    # Vertical grain streaks + plank joints
    streak = _noise([(256, 1.0)]).mean(axis=0, keepdims=True)
    base *= (0.9 + 0.2 * streak)[..., None]
    for col in range(SIZE // plank_w):
        x = col * plank_w
        base[:, x:x + 2] *= 0.55
    _save("planks.png", base)


def pavement() -> None:
    slab = 64
    n = _noise([(32, 0.5), (128, 0.5)])
    g = 120 + 32 * n
    img = np.stack([g, g, g * 0.98], axis=-1)
    for k in range(SIZE // slab):
        img[k * slab:k * slab + 2, :] *= 0.75
        img[:, k * slab:k * slab + 2] *= 0.75
    _save("pavement.png", img)


if __name__ == "__main__":
    print(f"writing textures to {OUT}")
    grass()
    tarmac()
    brick()
    slate()
    planks()
    pavement()
