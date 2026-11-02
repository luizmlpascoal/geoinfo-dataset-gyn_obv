# GYN-OBV: Goiânia Open Buildings Validation dataset

Building-level visual validation and typology labels for **55,590 Google Open Buildings v3 footprints** in Goiânia, Goiás, Brazil.

[![Data licence: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Code licence: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)

GYN-OBV records, for each footprint:

- whether it is a real building;
- its type and status (16 classes);
- a construction-standard flag;
- the year it first appears in the Google Earth image archive.

The footprints are those of most interest for updating the municipal property cadastre: outlines of 50 m² or more that lie outside the municipal lot base or on lots registered as vacant.

The dataset accompanies the paper *GYN-OBV: a building-level visual validation and typology dataset of Google Open Buildings footprints for Goiânia, Brazil*, submitted to GEOINFO 2026, the XXVI Brazilian Symposium on Geoinformatics.

> **Source dataset.** GYN-OBV is a building-level qualification of **[Google Open Buildings](https://sites.research.google/gr/open-buildings/)** (Google Research), version 3 polygons ([Earth Engine catalogue: `GOOGLE/Research/open-buildings/v3/polygons`](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings_v3_polygons)). Every footprint keeps its Open Buildings `plus_code`, so labels can be joined back to the original record. Open Buildings is distributed by Google under CC BY 4.0 or ODbL v1.0, at the user's choice; GYN-OBV uses it under **CC BY 4.0** and is released under the same licence.

> **Privacy.** The release holds only the building outline, the labels and administrative units (region and neighbourhood). It has no owner, taxpayer, cadastral registration, permit, street or address information. The lot register was used only to *select* footprints; none of its attributes is distributed.

---

## Contents

```
.
├── data/
│   ├── gyn_obv.gpkg               # 55,590 footprints with labels (layer "gyn_obv", EPSG:4674)
│   ├── gyn_obv.csv                # same records as a table; outline as WKT in column "wkt"
│   └── class_guide.csv            # the 16 classes: code, label, meaning (EN/PT), group, count
├── docs/
│   └── annotation_protocol.md     # inspection protocol, decision rules, quality control
├── scripts/
│   ├── build_release.py           # how the public files were derived from the internal inspection file
│   └── technical_validation.py    # reproduces every statistic reported below and in the paper
├── results/
│   └── technical_validation.md    # output of technical_validation.py
├── CITATION.cff
├── NOTICE                         # attribution of Google Open Buildings and other sources
├── LICENSE                        # CC BY 4.0 (data)
├── LICENSE-CODE                   # MIT (scripts)
└── requirements.txt
```

## Spatial and temporal coverage

| Item | Value |
|---|---|
| Area | Municipality of Goiânia, Goiás, Brazil (≈ 729 km²), all seven administrative regions |
| Bounding box | 16.461°S–16.826°S, 49.148°W–49.442°W (lon/lat: -49.442, -16.826, -49.148, -16.461) |
| Reference system | SIRGAS 2000, geographic (EPSG:4674) |
| Source footprints | [Google Open Buildings](https://sites.research.google/gr/open-buildings/) v3 polygons (Sirko et al. 2021), retrieved from Google Earth Engine |
| Inspection period | January to March 2026 (`inspection` = `2026-01` or `2026-03`) |
| Year of emergence | 2001–2026; see the censoring note below |

## Data dictionary (`gyn_obv.gpkg`, `gyn_obv.csv`)

| Column | Type | Description |
|---|---|---|
| `fid` | integer | Record identifier (1–55,590). In the GeoPackage it is the feature ID |
| `geometry` / `wkt` | MultiPolygon | Building outline from Open Buildings v3, SIRGAS 2000 (EPSG:4674). The CSV stores it as WKT |
| `plus_code` | text | Open Buildings v3 identifier (full Plus Code, e.g. `58MG5JFF+HPMQ`). It is unique and is the join key to Open Buildings |
| `confidence` | real | Open Buildings v3 confidence score (0.650–0.972). v3 distributes only polygons with confidence ≥ 0.65 |
| `area_m2` | real | Footprint area in m², from Open Buildings v3 (50.2–10,591.8) |
| `region` | text | Administrative region: Centro, Leste, Noroeste, Norte, Oeste, Sudoeste, Sul |
| `neighbourhood` | text | Official neighbourhood (*bairro*) containing the footprint (1,226 values) |
| `class_code` | integer | Supervisor-approved class, 0–15 (table below) |
| `class_label` | text | Class name matching `class_code` |
| `high_standard` | 0/1 | Construction-standard flag set by the inspector (see the protocol). 1 = high standard; empty for 14 records |
| `year_emergence` | integer | Year of the first Google Earth historical image showing the building. Empty when unknown (1,797 records) |
| `inspection` | text | Month of the visual inspection (`YYYY-MM`) |

## Classes

| Code | Label | Meaning | Group | Footprints |
|---:|---|---|---|---:|
| 1 | `CASA_TERREA` | Single-storey house | Residential | 30,808 |
| 8 | `CASA_SOBRADO` | House with two or more storeys | Residential | 2,711 |
| 2 | `CASA_COND_FECHADO` | House in a gated community | Residential | 2,632 |
| 3 | `EDIFICIO_RESIDENCIAL` | Residential building | Residential | 433 |
| 6 | `CASA_AREA_VERDE` | Dwelling in a green area | Residential | 943 |
| 5 | `SALA_COMERCIAL` | Commercial unit or shed | Non-residential | 7,906 |
| 4 | `EDIFICIO_COMERCIAL` | Commercial building | Non-residential | 272 |
| 10 | `PUBLICO` | Public or institutional building | Non-residential | 1,085 |
| 11 | `RELIGIOSO` | Church or temple | Non-residential | 526 |
| 7 | `BENFEITORIA` | Extension of an existing building | Lot transformation | 4,908 |
| 12 | `DEMOLICAO` | Building removed | Lot transformation | 392 |
| 13 | `DEMOLICAO_CONSTRUCAO` | Building removed and replaced | Lot transformation | 371 |
| 14 | `EM_CONSTRUCAO` | Work in progress | Lot transformation | 11 |
| 15 | `CONSTRUCAO_PARALIZADA` | Halted work | Lot transformation | 27 |
| 0 | `FALSO_POLIGONO` | No building (false polygon) | Data quality | 1,737 |
| 9 | `NAO_IDENTIFICADO` | Type cannot be decided from the imagery | Data quality | 828 |

## Methods in brief

1. **Selection.** All Open Buildings v3 footprints of 50 m² or more lying outside the 2025 municipal lot base or on lots registered as vacant (Mapa Urbano Básico Digital de Goiânia, MUBDG).
2. **Inspection.** Trained inspectors worked neighbourhood by neighbourhood in Google Earth Web. They browsed the historical imagery at lot scale and used Street View when the aerial view was not conclusive.
3. **Supervision.** A supervisor reviewed every label and confirmed or corrected it. Only the supervisor-approved label is released.

The full protocol and decision rules are in [`docs/annotation_protocol.md`](docs/annotation_protocol.md).

## Technical validation

All values below are reproduced by `scripts/technical_validation.py`; the full output is in [`results/technical_validation.md`](results/technical_validation.md).

| Indicator | Value (Wilson 95% CI) |
|---|---|
| Commission error (share of `FALSO_POLIGONO`) | 3.12% (2.98–3.27%) |
| Commission error, confidence ≥ 0.80 (76.1% of footprints) | 1.52% (1.41–1.65%) |
| Indeterminacy (share of `NAO_IDENTIFICADO`) | 1.49% (1.39–1.59%) |
| Labels changed by the supervisor (40,680 footprints with kept inspector sheets) | 0.99% (0.90–1.09%) |
| Inter-inspector agreement, 924 footprints labelled twice | 88.9%, Cohen's κ = 0.837 (0.808–0.867) |
| Agreement on building vs. no building, same 924 footprints | 95.1% |

Commission error by confidence band:

| Confidence | Footprints | False polygons, % |
|---|---:|---:|
| 0.65–0.70 | 1,846 | 20.04 (18.28–21.93) |
| 0.70–0.75 | 3,562 | 10.81 (9.83–11.87) |
| 0.75–0.80 | 7,880 | 4.28 (3.85–4.75) |
| 0.80–0.85 | 16,243 | 1.82 (1.63–2.04) |
| 0.85–0.90 | 19,420 | 1.33 (1.18–1.50) |
| ≥ 0.90 | 6,639 | 1.37 (1.12–1.68) |

## Known limitations

- **Purposive subset.** Footprints were chosen by their mismatch with the cadastre. Class shares and the commission error describe this subset, not the whole city.
- **Not assessed.** Omission (buildings missing from Open Buildings) and outline accuracy were not measured.
- **Year of emergence is left-censored.** The value is the first archive image showing the building. Peaks in 2002, 2004, 2008 and 2012 coincide with dates of the Google Earth archive, so for older buildings the year means "already present in the first available image". Values from 2016 onwards are the most informative. The year is meaningful only for confirmed buildings (not for codes 0 and 9).
- **High-standard flag.** The flag is an inspector judgement from combined visual cues; no single cue was applied as an automatic rule. For example, only 250 of the 2,711 two-storey houses are flagged.
- **Imagery.** Labels depend on the Google Earth archive; Street View is sparser in recently built areas.

## Usage example

```python
import geopandas as gpd

gdf = gpd.read_file("data/gyn_obv.gpkg", layer="gyn_obv")

# confirmed buildings that appeared from 2017 on, by region
new = gdf[~gdf.class_code.isin([0, 9]) & (gdf.year_emergence >= 2017)]
print(new.groupby("region").size())

# join back to the full Open Buildings v3 record through the Plus Code
# ob = gpd.read_file("open_buildings_v3_goiania.gpkg"); gdf.merge(ob, left_on="plus_code", right_on="full_plus_code")
```

Reproduce the statistics:

```bash
pip install -r requirements.txt
python scripts/technical_validation.py
```

## Licence and attribution

- **Data** (`data/`): [Creative Commons Attribution 4.0 International](LICENSE).
- **Scripts** (`scripts/`): [MIT](LICENSE-CODE).
- **Outlines, `plus_code`, `confidence` and `area_m2`** derive from [Google Open Buildings](https://sites.research.google/gr/open-buildings/) v3 (Sirko et al. 2021). Google offers that dataset under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) or [ODbL v1.0](https://opendatacommons.org/licenses/odbl/1-0/), at the user's choice; this derivative uses it under CC BY 4.0. Attribution required when reusing GYN-OBV: *“Contains data from Google Open Buildings v3 (Google Research), CC BY 4.0, https://sites.research.google/gr/open-buildings/”* together with the citation of this dataset. See also [`NOTICE`](NOTICE).
- **Labels** come from visual interpretation of Google Earth and Street View imagery by the authors. No imagery is redistributed.
- **Administrative units** come from the Mapa Urbano Básico Digital de Goiânia (Prefeitura de Goiânia).

## Acknowledgements

The dataset was produced in the project *Inteligência Artificial Aplicada para promover uma Gestão eficiente do Dinamismo do Município de Goiânia*. The project runs under Convênio nº 4940406/2024 between the Municipality of Goiânia (Secretaria Municipal da Fazenda, SEFAZ) and the Universidade Federal de Goiás (UFG), through the Centro de Excelência em Inteligência Artificial (CEIA), with the Fundação de Apoio à Pesquisa (FUNAPE) as intervening party. We thank the Prefeitura de Goiânia (SEFAZ and SEPLANH), CEIA-UFG and FUNAPE.

## References

- Sirko, W., Kashubin, S., Ritter, M., Annkah, A., Bouchareb, Y. S. E., Dauphin, Y., Keysers, D., Neumann, M., Cisse, M. and Quinn, J. A. (2021). Continental-scale building detection from high resolution satellite imagery. arXiv:2107.12283. Dataset: https://sites.research.google/gr/open-buildings/.
- Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1):37–46. doi:10.1177/001316446002000104.
- Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. *JASA*, 22(158):209–212. doi:10.1080/01621459.1927.10502953.

## Contact

Luiz Mário Lustosa Pascoal, CEIA / Instituto de Informática, Universidade Federal de Goiás. luizmlpascoal@gmail.com
