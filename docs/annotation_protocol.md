# Annotation protocol

This document describes how the GYN-OBV labels were produced. It is meant to let others apply the same protocol in another city and to judge the reliability of each attribute.

## 1. Unit of inspection and selection

- **Unit:** one Google Open Buildings v3 polygon. Version 3 distributes only polygons with confidence ≥ 0.65.
- **Selection:** polygons of 50 m² or more that lie outside the 2025 municipal lot base or on lots registered as vacant (Mapa Urbano Básico Digital de Goiânia). The lot layer was used only for this selection.
- **Result:** 55,590 polygons, inspected neighbourhood by neighbourhood.

## 2. Inspection tools

Inspection used Google Earth Web: historical imagery slider, polygon attribute panel and Street View. No imagery is redistributed with the dataset.

## 3. Procedure per footprint

1. Zoom to lot scale on the most recent image.
2. Browse the historical imagery. Decide whether a building exists within the outline, and whether it was built, extended or demolished over time.
3. Use Street View when the aerial view is not conclusive, for example to check type, storeys, use and status.
4. Check doubtful cases on at least two image dates.
5. Record the class, the construction-standard flag and the year of emergence. Never infer a class beyond the evidence; if the type cannot be decided, use `NAO_IDENTIFICADO`.

## 4. Decision rules

| Situation | Label |
|---|---|
| Outline over paved yard, bare soil, weedy plot or shadow, with no building | `FALSO_POLIGONO` (0) |
| A building is present but its type cannot be decided from aerial imagery or Street View | `NAO_IDENTIFICADO` (9) |
| New volume attached to, or on the same lot as, an existing building, adding built area | `BENFEITORIA` (7) |
| Independent dwelling with one storey | `CASA_TERREA` (1); two or more storeys: `CASA_SOBRADO` (8) |
| Dwelling inside a walled, gated residential development | `CASA_COND_FECHADO` (2) |
| Dwelling on land visibly designated as green or protection area | `CASA_AREA_VERDE` (6) |
| Mixed use (dwelling above or behind a shop) | resolved as `SALA_COMERCIAL` (5) |
| Building visible in earlier images and absent in the latest one | `DEMOLICAO` (12); replaced by a new building: `DEMOLICAO_CONSTRUCAO` (13) |
| Works visible in the latest image | `EM_CONSTRUCAO` (14); unchanged works over several images: `CONSTRUCAO_PARALIZADA` (15) |

The demolition classes were added during the work because the phenomenon was frequent.

## 5. Construction standard (`high_standard`)

The inspector set the flag to 1 when visual cues indicated a high construction standard, judged together. Typical cues were a swimming pool, the number of storeys, recent construction and location in a gated community. No single cue was applied as an automatic rule.

Of the 1,274 flagged footprints, 561 are houses in gated communities, 324 single-storey houses and 250 two-storey houses; the remaining 139 are spread over other classes. The flag is missing for 14 records.

## 6. Year of emergence (`year_emergence`)

- **Definition:** the year of the first historical image in Google Earth Web that shows the building.
- **Censoring:** when the building is already present in the oldest image available at that place, the value equals the date of that image. This produces peaks in 2002, 2004, 2008 and 2012, which are archive dates.
- **Missing values:** 1,797 records are empty: 1,794 recorded as unknown, plus 3 values outside the archive range (data-entry errors) set to null in the release.

## 7. Quality control

- **Supervisor review.** The footprints were split among trained inspectors by neighbourhood. A supervisor reviewed every label, confirming or correcting it, and only the approved label is released.
- **Supervisor changes.** For the 40,680 footprints (73.2%) whose inspector sheets were kept, the supervisor changed or resolved 0.99% of the labels (95% CI 0.90–1.09%). Most changes concerned footprints coded with two classes, resolved as commercial unit when the use was mixed.
- **Double labelling.** 924 footprints were labelled independently by two inspectors.
  - Agreement was 88.9% (Cohen's κ = 0.837, 95% CI 0.808–0.867), and 95.1% for building versus no building.
  - Most disagreements opposed `CASA_TERREA` to `FALSO_POLIGONO` or `NAO_IDENTIFICADO`.

## 8. Privacy

The released files contain only geometry, labels, the Open Buildings identifier and score, and the administrative region and neighbourhood. Owner names, taxpayer and cadastral identifiers, permits, street names and addresses are excluded. `scripts/build_release.py` documents the columns removed from the internal working file.
