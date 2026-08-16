# 07 — Interiors

Requirement: landmarks — pubs, shops — are **accessible and enterable**. This section defines what "enterable"
means, which buildings get it, and the templates that make ~40 interiors buildable by one person.

---

## The rule (from Pillar 2)

- **Seamless.** No loading screens, no fade, no teleport. Doors open; you walk through. Interiors live in the
  building's chunk scene and stream with it.
- **Honest.** Enterable buildings are visually signalled the way real open premises are: lit windows, open
  door, signage lit, A-board out. Sealed buildings read as private homes or closed shops. Never a handle on a
  fake door of a "should-be-open" business.
- **Schedule-aware.** Pubs lock outside licensing hours; shops lock outside trading hours; churches have
  open hours. A locked *enterable* building can still be entered the sandbox way — break the door (crowbar) or
  a window (brick), which is noise, which is a police report. Closed-hours entry is burglary gameplay, not a
  wall.

## The roster

The definitive list with tiers lives in the
[landmark register](../reference/atherton-landmark-register.md). Summary count for budgeting:

| Category | Bespoke (Tier 1) | Template (Tier 2) |
|---|---|---|
| Pubs & bars | 5 (Jolly Nailor, Wheatsheaf, Punch Bowl, Taphouse, Pound Pub) | 4 (Lamp, Tiki, Pendle Witch, Atherton Arms) |
| Shops & retail | 3 (Tesco, market + precinct, Aldi) | 3 (Boots, Co-op, Asda) |
| Civic & heritage | 5 (Town Hall, Chowbent Chapel, St John's, Alder House, Chanters Farmhouse) | 2 (Sacred Heart, St Richard's) |
| Transport | 2 (Atherton station, Hag Fold shelter) | — |
| Industrial heritage | 2 (Mines Rescue Station, Gibfield baths) | — |
| Sport & leisure | 2 (Roller Rink, Crilly Park clubhouse) | 2 (Collieries clubhouse, leisure centre TBC) |
| Emergency services | 1 (police station) | 1 (fire station) |
| **Total ≈ 32–40** | **20** | **12** |

St Anne's Hindsford is a special case: modelled enterable but *redundant* — dust, pigeons, no congregation, no
lighting. One of the best atmospheric interiors in the game for free.

**Explicit exclusion:** Atherton High School is sealed permanently, no interior, no occupants, regardless of
build status. (See [06](06-npcs-and-ai.md), constraint 1.)

## The pub template

Pubs are the game's hero interiors — the reason the requirement exists. The template, redressed per pub:

- **Front of house:** bar counter (ballistic cover, [05](05-weapons.md)) with working beer taps, back-bar
  optics and glassware (all breakable), seating zones, pool table (physics balls), dartboard, fruit machine,
  jukebox (licensed-free music pool), TV (sport loop), fireplace where the real pub has one.
- **Service:** cellar (kegs, lines, delivery hatch to street — a real second exit), kitchen where
  applicable, toilets, staff corridor.
- **Upstairs** where the real building has one: function room (Pound Pub), letting rooms (Wheatsheaf),
  landlord's flat (dressed, door locked, breakable).
- **Exterior attachments:** beer garden (Pound Pub), smoking area, bin yard with alley gate — the yard-mantle
  escape route matters to the police-evasion loop.
- **Occupancy:** from the schedule curves in [06](06-npcs-and-ai.md); staff archetypes behind the bar at all
  open hours.

Differentiation between the nine pubs comes from the real buildings' footprints and characters: the Jolly
Nailor small and traditional (real ale, real cider, no TV wall), the Wheatsheaf a gastropub with rooms, the
Pound Pub big-screen sport with function room, the Tiki Bar themed and late. The template supplies systems;
the register supplies identity.

## The shop templates

- **Small shop** (Boots, Co-op, precinct units): sales floor, till point (opens, cash), stockroom, staff
  door to a rear yard.
- **Supermarket** (Tesco — the largest interior in the game): aisle grid (shelving = destructible cover +
  massive prop-spill potential, budget-capped per [04](04-core-gameplay.md)), checkouts, warehouse rear with
  roller door, staff corridor, car park with trolley bays.
- **Open-air** (Atherton Market): stall props on market days, empty ground otherwise — technically an
  exterior but scheduled like an interior.

## Civic and heritage interiors

Modelled from photo reference where available; plausible-period where not (interiors of listed buildings are
poorly documented online — another [OQ-1](13-open-questions.md) item for local review):

- **Chowbent Chapel:** galleried meeting-house interior, box pews, the 1721 austerity — whitewash and oak.
- **Town Hall:** library floor (working returns trolley props), council chamber, offices.
- **Atherton station:** ticket hall, platforms, footbridge; barriers open (no ticketing sim).
- **Mines Rescue Station / Gibfield baths:** the two industrial-heritage museums-in-waiting; dressed to their
  1908/1913 function with interpretive clutter. Pure atmosphere, zero systems.

## Interior systems

- **Lighting:** every interior baked (LightmapGI) with a small dynamic budget (muzzle flash, breakable
  fixtures — breaking lights actually darkens; supports a stealth-adjacent evasion beat).
- **The "hostile interior" state** (from [06](06-npcs-and-ai.md)): once violence starts inside, occupancy
  logic flips — patrons rush doors, staff hide, the room's props become the fight. After reset, the interior
  re-dresses to default (broken glass persists until cell reload).
- **Audio:** each template has an acoustic profile (reverb size, material absorption) — the pub hubbub →
  sudden silence when a weapon comes out is an audio moment worth engineering deliberately.
  See [09](09-art-and-audio-direction.md).
- **Navmesh:** per-interior, portal-linked to the street mesh ([06](06-npcs-and-ai.md)); police tiers 3+
  will breach interiors.

## Acceptance criteria

1. Walk from open street into every Tier 1 interior with zero perceptible load (no hitch > 8 ms).
2. Every enterable building is identifiable as such from the street at a glance, day and night, by lighting
   and signage language alone (playtest: 10/10 correct guesses on unfamiliar buildings).
3. Pub template fully systemic: taps pour, pool balls move, till opens, cellar hatch exits to street.
4. Locked-hours entry via break-in works on every enterable building and generates the appropriate police
   report event.
5. Interior prop budget respected: no interior exceeds its active-physics cap under a "trash everything"
   stress test on target hardware.

---

**Previous:** [06 — NPCs and AI](06-npcs-and-ai.md) · **Next:** [08 — Technical architecture](08-technical-architecture.md) · **Index:** [PRD README](README.md)
