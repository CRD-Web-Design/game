# Atherton Landmark Register

The authoritative list of named real-world locations to be modelled, with the authoring tier for each and
whether it has a playable interior. This drives asset scheduling in
[11-milestones-and-roadmap.md](../prd/11-milestones-and-roadmap.md).

---

## ⚠️ Accuracy caveat — read this first

This register was compiled from **public web sources only** (CAMRA branch guides, British Listed Buildings,
Wigan Archives, National Churches Trust, local history sites, pub directories, Greater Manchester Police area
pages). It has not been verified on the ground.

Two things follow from that:

1. **Latitude/longitude is deliberately left as `TBC` for most entries.** Precise coordinates are *resolved by
   the pipeline* from OSM and OS Open Names at build time, keyed on the street address and postcode below —
   they are not hand-entered here. Hand-typed coordinates for 40+ buildings would be invented precision, and
   invented precision in a 1:1 map is worse than none.
2. **Street addresses and postcodes are the locator of record.** Where a source gave an address or postcode, it
   is recorded verbatim. Where it did not, the field says `TBC`.

Known gaps and doubts are listed at the bottom under [Unresolved](#unresolved). One source consulted during
research incorrectly placed Pennington Flash Country Park in Atherton — it is in Leigh, outside our bounds, and
is **not** in this register. Treat the rest with the same suspicion until reviewed.

**Reviewer needed:** someone with local knowledge. See [OQ-1](../prd/13-open-questions.md).

---

## Tiers

| Tier | Exterior | Interior | Budget guide |
|---|---|---|---|
| **1** | Hand-modelled, photo-referenced, unique materials | Full bespoke interior, navmeshed, props | 3–10 days each |
| **2** | Hand-adjusted from generated shell, unique facade | Shared template interior, redressed | 1–2 days each |
| **3** | Procedurally generated shell from footprint + height | None — sealed, faked window interiors | Automated |

Everything not listed in this register is Tier 3 by default: roughly 5,000 residential and minor commercial
buildings, generated from footprints. See [03-world-and-map.md](../prd/03-world-and-map.md).

---

## Tier 1 — Civic and heritage

| Landmark | Address | Postcode | Interior | Notes |
|---|---|---|---|---|
| Chowbent Chapel (Unitarian) | Bolton Old Road | TBC | Yes | Built 1721; Grade II\*; oldest place of worship in the town. Whitewashed walls, oak roof trusses, galleried. Anchor landmark. |
| Atherton Town Hall | Bolton Road | TBC | Yes | Former Atherton Urban District Council HQ; now a community hub and public library. Council chamber, library floor, offices. |
| St John the Baptist's Church | TBC | TBC | Yes | Built 1879. Third building on the site — first chapel 1645, Presbyterian. Parish church. |
| Alder House | Alder Street | TBC | Yes | Built 1697; Grade II\*; hammer-dressed stone, stone-slate roof, double-depth plan. Grounds are the Atherton Collieries A.F.C. ground. |
| Chanters Farmhouse | Chanters Avenue | TBC | Yes | Dated 1678 by the `WA 1678` door lintel — thought to be William Atherton. Grade II\*. |
| St Anne's Church | Tyldesley Road, Hindsford | TBC | Yes | Austin & Paley; foundation stone 1889, completed 1901 at £9,000. Grade II. **Redundant** — model as disused. |
| Sacred Heart RC Church | Hindsford | TBC | Template | Roman Catholic parish church. |
| St Richard's RC Church | Mayfield Street | TBC | Template | Built 1928 by Fr T. Almond; site acquired 1889 by Fr O'Neill, originally a school-chapel. |

## Tier 1 — Town centre, retail and pubs

The Market Street run (A577) is the densest and most-trafficked part of the map. It gets the most authoring
attention of anywhere in the game.

| Landmark | Address | Postcode | Interior | Notes |
|---|---|---|---|---|
| Jolly Nailor | 20 Market Street | M46 0DN | Yes | Traditional town-centre pub, small real-ale range and a real cider. Name references the town's nail-making trade. |
| The Wheatsheaf | 48 Market Street | M46 0DG | Yes | Gastropub with accommodation — gives us an upstairs floor. |
| Punch Bowl | 165 Market Street | TBC | Yes | North end of the run. |
| Mechanics Rest / The Taphouse | 119 Market Street | M46 0DF | Yes | |
| The Lamp | 5 Market Street | M46 0DW | Template | |
| Tiki Bar | 68 Market Street | M46 0DA | Template | Late-opening bar — drives the evening NPC schedule. |
| Pound Pub | Market Street | TBC | Yes | Big-screen sports, pool, darts, dominoes, beer garden, function room. Open 09:00–23:00 daily — good for wide-open occupancy variance. |
| Pendle Witch / Witch Tap House | Warburton Place | M46 0EQ | Template | Just off Market Street. |
| Atherton Arms | TBC | M46 9DD | Template | Outside the town-centre cluster. |
| Atherton Market | Town centre | TBC | Yes (open-air) | Traditional outdoor market. Stalls present on market days only — see the NPC schedule in [06](../prd/06-npcs-and-ai.md). |
| Eckersley Precinct | Mealhouse Lane | TBC | Yes | Small shopping precinct, food shops. |
| Tesco Superstore | Tyldesley Road | M46 9DA | Yes | Largest single interior in the game. Shop floor, checkouts, stockroom, staff corridor, car park. |
| Boots the Chemist | Market Street | TBC | Template | |
| Aldi | TBC | TBC | Yes | |
| Co-op Food | TBC | TBC | Template | |
| Asda | TBC | TBC | Template | |

## Tier 1 — Emergency services and institutions

| Landmark | Address | Postcode | Interior | Notes |
|---|---|---|---|---|
| Atherton Police Station | Flapper Fold Lane | TBC | Yes | Origin point for tier 1–3 police response; see [06](../prd/06-npcs-and-ai.md). GMP patrols Atherton, Tyldesley, Astley and Mosley Common from here. Real livery is fine for a personal build; fictionalise only if this is ever published. |
| Atherton Community Fire Station | Adjacent to the police station, Flapper Fold Lane | TBC | Template | Fire and ambulance response origin. Appliance bay. |
| Atherton High School | Hamilton Street | TBC | **No — sealed** | Formerly Atherton Community School / Hesketh Fletcher CofE High School. Exterior only, permanently sealed, no interior, no occupants — this one is a hard no regardless of scope. See [07-interiors.md](../prd/07-interiors.md). |
| Atherton Leisure Centre | TBC | TBC | Template | Needs local verification — see [Unresolved](#unresolved). |

## Tier 1 — Transport

| Landmark | Address | Postcode | Interior | Notes |
|---|---|---|---|---|
| Atherton railway station | Bolton Road | TBC | Yes | On the Manchester–Southport line; third busiest on the line after Manchester Victoria and Wigan Wallgate. 13 miles west of Manchester Victoria. Northern Trains services. Platforms, footbridge, ticket hall. Drives the 07:00–09:00 commuter surge. |
| Hag Fold railway station | Hag Fold estate | TBC | Yes (shelter only) | Built 1987 by British Rail to serve the estate. Staffed 06:25–12:55 weekdays only — model the ticket office as shuttered outside those hours. ~1.2 km northwest of Atherton station. |

## Tier 1 — Industrial heritage

Atherton's identity is a mining town — cotton, nails, collieries, nuts and bolts. The last deep mine closed in
1966. These sites carry that and are among the most visually distinctive locations available.

| Landmark | Address | Postcode | Interior | Notes |
|---|---|---|---|---|
| Howe Bridge Mines Rescue Station | Lovers Lane, Howe Bridge | TBC | Yes | Opened 1908 — **the first mines rescue station in Lancashire**. Extension hall added 1935 by Taylor and Young, part-funded by the Miners' Welfare Fund. |
| Gibfield Colliery pithead baths | Gibfield, off Wigan Road | TBC | Yes | Baths opened September 1913 — **the first in the United Kingdom** to provide on-site washing for miners. The baths building survives; the colliery itself was cleared after 1963. Site is now a business park. |
| Howe Bridge model pit village | Howe Bridge | TBC | Streetscape | Purpose-built colliery village — terraced housing built by the Atherton Collieries owners. Model as a coherent Tier 2 streetscape, not individual Tier 1 buildings. |
| Chanters Colliery site | Tyldesley Road | TBC | No | Closed by 1966. Present-day condition — cleared/redeveloped. |

## Tier 1 — Sport and recreation

| Landmark | Address | Postcode | Interior | Notes |
|---|---|---|---|---|
| Crilly Park | TBC | TBC | Yes | Home of Atherton Laburnum Rovers F.C., North West Counties League Premier Division. Capacity 3,000, 250 seated. Stand, clubhouse, pitch. |
| Alder House ground | Alder Street | TBC | Template | Home of Atherton Collieries A.F.C. — founded 1916 by miners from the six pits in the Atherton Urban District, to raise money for the war effort. Northern Premier League Division One West. |
| Atherton Roller Rink | TBC | TBC | Yes | Current venue of the **Bent 'n' Bongs Beer Bash**, the town's annual beer festival (34 editions as of 2025). Large clear-span interior — good sandbox space. |
| Colliers Wood | TBC | TBC | n/a — terrain | Woodland with a network of over 5 km of trails; the Colliers Wood Circular is a 2.7-mile loop with ~104 m of ascent. Dense-vegetation performance test case. |

## Notable absences

| Site | Why it's not a Tier 1 building |
|---|---|
| **Formby Hall** | **Demolished in 2018.** It hosted the Bent 'n' Bongs Beer Festival each January before closing. The brief is "the town exactly as it looks in real life," so the site is modelled in its **present-day cleared condition**. The festival is represented at the Roller Rink instead. |
| Pennington Flash Country Park | In Leigh, outside the map bounds. A research source wrongly placed it in Atherton. |
| Astley Green Colliery Museum | In Astley, outside the map bounds. Same source error class. |
| Atherton Hall | The historic Atherton family seat — long demolished, and the name is also shared with unrelated buildings elsewhere. Not present in the modern townscape. |

---

## Unresolved

Items needing local verification before they enter production. Each one is cheap to confirm for someone who
knows the town and expensive to get wrong at M3.

1. **Atherton Leisure Centre** — existence, current name and location not confirmed by research. May have been
   renamed, relocated or closed.
2. **Which supermarkets actually exist and where.** Research returned Tesco (Tyldesley Road, confirmed), plus
   unconfirmed mentions of Aldi, Co-op and Asda without addresses. Needs a definitive list.
3. **Pub roster is a snapshot and pubs close.** The list above reflects directory data of uncertain vintage.
   Any pub that has shut since should be modelled as shut — that is what "exactly as it looks in real life"
   means. Specifically unconfirmed: Old Isaacs (a research source listed M46 0DG but could not corroborate it),
   Kings Head / Weavers Rest.
4. **St John the Baptist's Church street address** not captured.
5. **Crilly Park and Atherton Roller Rink addresses** not captured.
6. **Atherton Market** — open-air site location, and which days it trades. Drives an NPC schedule.
7. **Whether Bag Lane still exists as a street.** It appears in historic land-ownership records (properties
   23–28 Bag Lane) and gave its name to the former Atherton Bag Lane railway station, but its current status
   was not confirmed.
8. **Anything significant that is missing entirely.** A register built from the internet will have holes exactly
   where a town's everyday life is — the chippy, the barber, the working men's club, the corner shop everyone
   uses. Those are worth more to authenticity than another listed building.
