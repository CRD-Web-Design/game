# Data Sources

Where the 1:1 geometry comes from, and how to get it. Pipeline mechanics are in
[ADR-0002](../adr/0002-map-data-pipeline.md).

> **Scope note.** This is a **personal, unpublished project**. Licence obligations below are recorded for
> completeness, but essentially all of them — ODbL share-alike, OGL attribution — are triggered by
> *distribution*, and there isn't any. Nothing here should slow you down. The section
> [If this is ever published](#if-this-is-ever-published) collects what would change.
>
> The source recommendations below are made on **technical merit**, not compliance. OSM and LiDAR are simply
> the right inputs for generating real geometry.

---

## Primary sources

### 1. OpenStreetMap — buildings, roads, POIs

The backbone. Supplies building footprints, road centrelines, land use polygons, and named POIs (which is
where most of the [landmark register](atherton-landmark-register.md) locations resolve to real coordinates).

| | |
|---|---|
| **Get it** | [Geofabrik](https://download.geofabrik.de/europe/united-kingdom/england/greater-manchester.html) — Greater Manchester `.osm.pbf` extract, ~50 MB. Clip to the map bounds with `osmium extract`. |
| **Alternative** | Overpass API for targeted queries during development — faster iteration than re-clipping the whole extract. |
| **Format** | PBF → GeoJSON via `osmium` or `ogr2ogr` |
| **Licence** | ODbL 1.0 |

**Quality expectation:** OSM coverage of a Greater Manchester town is good for roads and decent for building
footprints, but **building heights will be largely missing**. Expect to infer heights from storey counts where
tagged and fall back to typology defaults (see ADR-0002). Interior detail and business names are patchy — the
landmark register exists precisely because OSM won't tell you the Jolly Nailor has a beer garden.

### 2. Environment Agency LiDAR — terrain

This is what makes the 30 m → 76 m gradient real rather than guessed.

| | |
|---|---|
| **Get it** | [DEFRA Survey Data Download](https://environment.data.gov.uk/survey) — select the Atherton tiles |
| **Product** | **LiDAR Composite DTM, 1 m resolution.** DTM (terrain), *not* DSM (surface) — DSM includes buildings and vegetation, which you're placing yourself. |
| **Format** | GeoTIFF, OSGB36 / British National Grid (EPSG:27700) |
| **Licence** | Open Government Licence v3 |

1 m DTM at 12.2 km² is roughly 12 million samples — downsample to a 2 m or 4 m heightmap for the engine. The
detail you lose is below what a player can perceive on foot.

**Optional:** the 1 m **DSM** is genuinely useful as a cross-check for building heights where OSM has none —
subtract DTM from DSM inside a footprint polygon and you get a rough roof height for free. Noisy near trees,
but better than a typology default.

### 3. Ordnance Survey Open Data — cross-check

| Product | Use |
|---|---|
| **OS OpenMap Local** | Building footprints — cross-check OSM, fill gaps. Often more complete for outbuildings. |
| **OS Open Roads** | Road network with proper classification. Better classification metadata than OSM. |
| **OS Open Names** | Gazetteer — resolves street names and postcodes to coordinates. **This is what turns the landmark register's postcodes into real positions.** |

Get them from [OS Data Hub](https://osdatahub.os.uk/downloads/open). All OGL v3. All free, no account friction
for the open products.

### 4. Aerial imagery — visual reference only

For getting roof shapes, materials and street furniture right by eye during hand-authoring of Tier 1 buildings.

Reference-only means: look at it, model from what you see. Don't project it as a texture and don't trace
geometry directly off it into shipped assets.

---

## On Google Maps

The Google Maps link that framed this project is a **reference for the map bounds and for orientation** — that
use is completely fine, and Street View is genuinely the best free tool for seeing what a building on Market
Street actually looks like.

What it isn't is a *data source*. Don't scrape tiles, don't project Street View captures as textures, don't
trace geometry off satellite imagery into assets. Two reasons, and for a personal project only the second one
really matters:

1. Google's Terms of Service prohibit it.
2. **It's the worse input anyway.** Satellite imagery gives you pixels; OSM gives you actual footprint polygons
   with metadata, and LiDAR gives you actual elevation in metres. You'd be doing more work for a worse result.

Use Street View the way you'd use a photograph — to know what to build.

---

## Coordinate systems

A recurring source of bugs. Fix the convention early.

| Stage | CRS |
|---|---|
| OSM data | WGS84 / EPSG:4326 (lat-lon degrees) |
| EA LiDAR, OS Open Data | OSGB36 / EPSG:27700 (British National Grid, metres) |
| **Pipeline working CRS** | **EPSG:27700** — it's already in metres, which is what the engine wants |
| Godot world space | Metres, origin at the map-bounds southwest corner, Y-up, Z-forward |

Reproject OSM into EPSG:27700 on ingest, then translate so the southwest corner of the bounds is `(0, 0)`.
Everything downstream is plain metres from that origin, and no part of the runtime ever sees a latitude.

Note the axis convention flip: British National Grid is easting/northing (X, Y), Godot is (X, Z) on the ground
plane with Y as height. Get this wrong and the town is mirrored.

**Map bounds** (from [03-world-and-map.md](../prd/03-world-and-map.md)):

```
North   53.5400
South   53.5100
West    -2.5250
East    -2.4700
```

---

## If this is ever published

Not applicable today. Kept here so the decision is informed rather than accidental.

| Obligation | Trigger | What it requires |
|---|---|---|
| **OSM — ODbL 1.0** | Distributing the game | Attribution: "© OpenStreetMap contributors". Share-alike applies to the *database*, not to rendered output — the usual reading is that shipped geometry derived from OSM is a Produced Work, which requires attribution but not that you open your assets. Worth real legal advice, not a doc footnote. |
| **EA LiDAR, OS Open Data — OGL v3** | Distributing the game | Attribution: "Contains public sector information licensed under the Open Government Licence v3.0" and "© Environment Agency copyright and/or database right" / "Contains OS data © Crown copyright and database right". Permissive otherwise. |
| **Google Maps ToS** | Any use of Google-derived data in assets | Don't. See above. |
| **Real business names and trade dress** | Publication | The substantial one. Depicting named real pubs and shops as sites of gun violence is trademark and passing-off exposure, and a reputational problem in a town of 22,000. Discussed in [12-risks-legal-compliance.md](../prd/12-risks-legal-compliance.md). |
| **Age rating** | Commercial release | PEGI 18 / ESRB M submission. Not needed for a personal build. |
| **macOS notarisation** | Distributing a binary | Apple Developer account, code signing, notarisation. For running on your own Mac, an ad-hoc signature or right-click → Open is enough. |
