# 09 — Art and Audio Direction

The look and sound of Atherton, and how to hit "high quality" on an M1 with a team of one.

---

## Visual target

**Grounded realism at play speed** — not photorealism. The reference feel is overcast-day documentary
photography of the North West: diffuse light, saturated brick reds and wet tarmac greys, signage colour
pops. The player should stop noticing the graphics in five minutes and start noticing the town.

Reference points: *Everybody's Gone to the Rapture* (British place-realism on a budget), GTA V's weather
palette (not its LA saturation), Google Street View of Market Street (literally — it's the ground truth for
what things look like).

### Why this target is achievable solo

- Diffuse overcast lighting is *cheap and flattering* — it hides texture repetition and LOD seams that harsh
  sun exposes. The default weather is also the easiest to render well.
- The palette does the identity work: red brick + slate + UPVC white + tarmac is a small, coherent material
  set. Maybe 30 core tileable materials cover 90% of the town.
- Tier 3 buildings live or die on **facade kit quality**, not variety: per
  [ADR-0002](../adr/0002-map-data-pipeline.md), six typologies × modular door/window/brick/roof pieces ×
  parameterised grime and paint. Budget the kit like a hero asset — it *is* the town.

### Material and asset rules

- PBR throughout, 1K textures standard / 2K for Tier 1 hero surfaces, trim sheets everywhere.
- Weathering is Lancashire-specific: soot-darkened brick tops, moss on north roofs, damp lines under sills.
- Signage: Tier 1 buildings get bespoke signs (real names as per register); Tier 3 shopfronts draw from a
  generic-plausible pool (no accidental real-business collisions on unmodelled premises).
- Street furniture set: UK-correct — Wigan-borough wheelie bins, GM-style lamp columns, red postboxes, bus
  shelters, bollards. This set sells the country more than any building does.
- Vegetation: hawthorn/sycamore/bramble kit for the brooks and pit land; Colliers Wood is the density test.

### Weather and time

From [03](03-world-and-map.md): overcast default, bright, rain, heavy rain, fog. Rain is the hero state —
wet-surface response, puddle decals in real kerb low-spots (LiDAR gives them for free), audio layer. Night is
sodium-and-LED mixed street lighting; the town centre glows, the estates pool light at lamps, the pit-land
paths are genuinely dark (gameplay: evasion terrain).

## Audio direction

Audio carries place-authenticity at least as hard as visuals, and it's cheaper.

### Ambient beds

Layered by district + time + weather:

- **Town centre day:** traffic wash (A577/A579), pedestrian chatter, market PA on market days, shop doors.
- **Town centre night:** pub spill (muffled music + crowd through walls — each pub leaks its own character),
  taxis idling, kick-out-time vocal texture after 23:00.
- **Estates:** dogs, distant trampoline squeak, lawnmowers (weekend schedule), TV bleed at night.
- **Pit land / brooks / Colliers Wood:** birdsong (UK species, seasonally plausible), water, wind in
  sycamores, the M61 as a distant pink-noise floor to the north.
- **The railway:** the two-car Northern unit is a scheduled audio event — rail joint rhythm, horn at the
  crossings, Doppler. Audible ~40 s before visible. The single most place-setting sound in the game.

### Gunfire acoustics

From [05](05-weapons.md): distinct per-weapon reports, and the *environment* does the drama —
terraced-street slapback in Howe Bridge, open-lot bloom in the Tesco car park, interior ring + muffled
street-side transmission. Implementation: per-space reverb zones + a cheap outdoor early-reflection
approximation driven by building density around the listener.

### The quiet moment

Engineered deliberately ([07](07-interiors.md)): pub hubbub → weapon drawn → bed ducks to silence → one
glass sets down. The audio system supports **state-driven mix snapshots** (routine / tension / hostile /
aftermath) globally and per-interior.

### Voice

No recorded dialogue in v1. NPC vocalisation = wordless efforts + a small bark set. **If barks are added,
accent is Wigan-borough Lancashire, not Manchester** ([02](02-setting-atherton.md)) — wrong accent would be
the single most immersion-breaking asset in the game for the one audience member who matters. Generated-voice
barks are acceptable for a personal build; a real local voice is better and cheap at this scale.

### Music

None during play (the world is the soundtrack) except **diegetic**: pub jukeboxes and TVs, licensed-free
pool. A single menu theme, brass-band-adjacent arrangement — the one permitted sentimentality.

## UI visual language

Minimal diegetic-leaning HUD (full spec in [10](10-ui-ux.md)): clean sans overlays, no gold filigree, no
sci-fi. The pause map is styled as an OS-style street map — the aesthetic bridge between game and the real
place it depicts.

## Acceptance criteria

1. A 10-photo side-by-side (screenshot vs Street View, same corners) reads as "same place" to a stranger.
2. Material count audit: ≤ 40 core tileables outside Tier 1 assets.
3. Blindfold district test: town centre / estate / pit land distinguishable by ambient audio alone.
4. The train pass is audible, locatable and Doppler-correct from 3 test points.
5. Rain state changes surfaces, audio and NPC behaviour (umbrellas up, awning-sheltering) simultaneously.

---

**Previous:** [08 — Technical architecture](08-technical-architecture.md) · **Next:** [10 — UI and UX](10-ui-ux.md) · **Index:** [PRD README](README.md)
