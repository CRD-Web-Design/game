# Atherton Street Register

The road network of the playable area, with classification and gameplay notes. The pipeline generates road
geometry automatically from OSM centrelines ([ADR-0002](../adr/0002-map-data-pipeline.md)); this register
exists to record what matters about each route so the generated output can be sanity-checked and hand-tuned.

**Same caveat as the landmark register:** compiled from web sources, unverified on the ground. Street-level
detail for a town this size is thin online. Flagged for local review — see [OQ-1](../prd/13-open-questions.md).

---

## Classified roads

Atherton sits on two crossing A-roads. Their junction is effectively the centre of the map and the busiest
traffic node in the game.

| Road | Route | Notes |
|---|---|---|
| **A577** | Market Street → Mealhouse Lane | The Wigan–Bolton axis and the town's retail spine. Market Street is the pub-and-shop run; almost every Tier 1 retail interior is on it. Highest NPC and vehicle density in the game. |
| **A579** | Bolton Road | The **old main road** from Bolton to Leigh — the historic route the town grew along. Runs north–south. Atherton Town Hall and Atherton railway station are on it. Also forms part of the eastern map boundary. |

## Principal local roads

| Road | Notes |
|---|---|
| **Bolton Old Road** | Chowbent Chapel sits here. Postcode district M46 9. The older parallel alignment to Bolton Road. |
| **Tyldesley Road** | Runs southeast toward Tyldesley. Tesco Superstore (M46 9DA), St Anne's Church Hindsford, and the former Chanters Colliery site are all on it. |
| **Leigh Road** | South, toward Leigh and the Atherleigh area. |
| **Flapper Fold Lane** | Police station and community fire station. Connects to Mealhouse Lane (A577) and Market Street (A577). Emergency-response vehicles spawn onto the network here. |
| **Lovers Lane** | Howe Bridge. Site of the 1908 Mines Rescue Station. |
| **Alder Street** | Alder House (1697) and the Atherton Collieries A.F.C. ground. |
| **Chanters Avenue** | Chanters Farmhouse (1678). Near "The Valley", where Chanters Brook runs. |
| **Hamilton Street** | Atherton High School. |
| **Mayfield Street** | St Richard's RC Church. |
| **Warburton Place** | Pendle Witch / Witch Tap House. Small side street off the Market Street cluster. |
| **Fold Road** | Local distributor. |
| **Bag Lane** | Historic — appears in old land-ownership records and named the former Atherton Bag Lane station. **Current status unconfirmed** (see landmark register, Unresolved item 7). |

## Bus corridors

Useful because bus routes trace the roads that actually carry through-traffic, which is what the vehicle
traffic simulation should weight toward.

| Service | Route |
|---|---|
| **582** | Leigh ↔ Atherton ↔ Bolton. Frequent. |
| **583** | Tyldesley ↔ Atherton ↔ Hag Fold ↔ Abbey Lane ↔ Leigh. |

## Rail corridor

The **Manchester–Southport line** cuts across the map roughly east–west, with two stations inside the bounds:
Atherton and Hag Fold (~1.2 km apart). Eastbound runs toward Walkden, Swinton, Salford and Manchester
Victoria; westbound toward Hindley and Wigan Wallgate.

Gameplay significance: the line is a **linear barrier** across the map. Crossings are limited, which naturally
channels both pedestrian and vehicle movement and gives the police escalation system chokepoints to work with.
Model the embankments, fencing and bridges accurately — they matter more to navigation than their visual
prominence suggests.

## Watercourses and terrain

| Feature | Notes |
|---|---|
| **Shakerley Brook** | Forms the **western border** of Atherton. Doubles as a natural map edge. |
| **Chanters Brook** | Flows through the area known locally as **"The Valley"**. The only meaningful topographic incision in the town. |

**Elevation:** the southwest of the township sits around **30 m** above sea level, rising to about **76 m** in
the north. That is a real 46 m gradient across roughly 3 km — gentle, but enough that it should be felt when
walking north and visible in sightlines down the A579. Soil is clay across much of the township, which is worth
noting for material and drainage detail.

---

## Districts

| District | Position | Character |
|---|---|---|
| **Atherton town centre / Chowbent** | Centre | The retail core. Market Street, the pubs, the market, the civic buildings. Densest geometry, densest crowds. |
| **Hindsford** | South, toward the Leigh boundary | Smaller residential area. St Anne's, Sacred Heart. |
| **Howe Bridge** | East | The model pit village — purpose-built colliery housing, the Mines Rescue Station. The most architecturally coherent district and the strongest sense of place. |
| **Hag Fold** | West | Post-war estate, served by its own 1987 station. |
| **Atherleigh** | South | Toward Leigh. |
| **Lately Common** | Periphery | Edge of the mapped area. |

Since 1974 Atherton and its neighbourhoods of Hag Fold, Hindsford and Howe Bridge have formed a township of the
Metropolitan Borough of Wigan.

---

## Unresolved

1. Bag Lane's current existence and alignment.
2. Whether any of the above have been pedestrianised, made one-way, or realigned recently — the town centre in
   particular. One-way systems significantly affect the vehicle traffic sim.
3. The residential street network is **not** enumerated here — roughly 5,000 buildings sit on streets this
   register doesn't name. Those come wholesale from OSM. This register covers only what needs hand attention.
4. Car parks, which the traffic and police-response systems both need, are not yet catalogued.
