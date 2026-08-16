#!/usr/bin/env python3
"""Procedural placeholder sound effects (16-bit mono WAV, 22.05 kHz).

Deterministic. Committed outputs live in assets/sfx/; re-run to tweak:

    python3 tools/gen_assets/gen_sfx.py

Synthesised, not sampled — good enough to make the sandbox feel alive until
a real audio pass (PRD 09).
"""

from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parents[2] / "assets" / "sfx"
SR = 22050
RNG = np.random.default_rng(1721)  # Chowbent Chapel's year


def _save(name: str, samples: np.ndarray) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    clipped = np.clip(samples, -1.0, 1.0)
    data = (clipped * 32000).astype(np.int16)
    with wave.open(str(OUT / name), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(data.tobytes())
    print(f"  {name}  ({(OUT / name).stat().st_size // 1024} KB)")


def _env(n: int, attack: float, decay: float) -> np.ndarray:
    t = np.arange(n) / SR
    return np.minimum(t / max(attack, 1e-4), 1.0) * np.exp(-t / decay)


def gunshot(name: str, length: float, boom_hz: float, boom_amt: float,
            crack_amt: float, decay: float) -> None:
    n = int(SR * length)
    t = np.arange(n) / SR
    crack = RNG.standard_normal(n) * _env(n, 0.001, decay * 0.5) * crack_amt
    boom = np.sin(2 * np.pi * boom_hz * t * np.exp(-t * 3)) * _env(n, 0.002, decay) * boom_amt
    _save(name, crack + boom)


def click(name: str, times: list[float], length: float) -> None:
    n = int(SR * length)
    out = np.zeros(n)
    for t0 in times:
        i = int(t0 * SR)
        burst = int(0.008 * SR)
        if i + burst < n:
            out[i:i + burst] += RNG.standard_normal(burst) * _env(burst, 0.0005, 0.004) * 0.5
    _save(name, out)


def thud(name: str) -> None:
    n = int(SR * 0.12)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 95 * t) * _env(n, 0.001, 0.03) * 0.8
    snap = RNG.standard_normal(n) * _env(n, 0.0005, 0.008) * 0.25
    _save(name, body + snap)


if __name__ == "__main__":
    print(f"writing sfx to {OUT}")
    gunshot("pistol.wav", 0.30, 140.0, 0.55, 0.85, 0.06)
    gunshot("shotgun.wav", 0.45, 90.0, 0.95, 0.75, 0.11)
    gunshot("smg.wav", 0.22, 160.0, 0.45, 0.80, 0.045)
    click("reload.wav", [0.0, 0.14, 0.32], 0.45)
    click("dryfire.wav", [0.0], 0.08)
    thud("hit.wav")
    thud("punch.wav")
