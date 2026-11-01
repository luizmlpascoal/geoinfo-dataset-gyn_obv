# GYN-OBV technical validation (reproduced from data/gyn_obv.gpkg)

- Footprints: 55,590; total area 9,048,945 m²
- Commission error (FALSO_POLIGONO), % (Wilson 95% CI): 3.12 (2.98–3.27); n = 1,737
- Not identified (NAO_IDENTIFICADO), %: 1.49 (1.39–1.59); n = 828
- Confirmed buildings: 53,025 (95.39%), area 8,631,000 m²
- High standard flagged: 1,274; missing flag: 14

## Commission and indeterminacy by confidence score

| Confidence | Footprints | Share | False polygons, % (CI) | Not identified, % (CI) |
|---|---:|---:|---:|---:|
| 0.65–0.70 | 1,846 | 3.3% | 20.04 (18.28–21.93) | 2.33 (1.73–3.12) |
| 0.70–0.75 | 3,562 | 6.4% | 10.81 (9.83–11.87) | 1.71 (1.34–2.19) |
| 0.75–0.80 | 7,880 | 14.2% | 4.28 (3.85–4.75) | 1.61 (1.36–1.91) |
| 0.80–0.85 | 16,243 | 29.2% | 1.82 (1.63–2.04) | 1.31 (1.14–1.49) |
| 0.85–0.90 | 19,420 | 34.9% | 1.33 (1.18–1.50) | 1.42 (1.26–1.59) |
| ≥ 0.90 | 6,639 | 11.9% | 1.37 (1.12–1.68) | 1.66 (1.38–1.99) |

- Confidence ≥ 0.80: 76.1% of footprints; commission 1.52 (1.41–1.65)
- Confidence < 0.75: 9.7% of footprints, holding 43.5% of the false polygons

## Commission by footprint area

| Area (m²) | Footprints | False polygons, % (CI) |
|---|---:|---:|
| 50–100 | 20,510 | 4.00 (3.74–4.28) |
| 100–200 | 23,668 | 2.44 (2.25–2.65) |
| ≥ 200 | 11,412 | 2.96 (2.67–3.29) |

## Footprints by region (% of each region)

| Region | Footprints | False pol. | Single-storey | Commercial unit | Extension | Gated | Emerged 2016+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Oeste | 15,309 | 3.2 | 55.4 | 13.4 | 12.0 | 4.3 | 29.9 |
| Sudoeste | 12,337 | 2.4 | 60.8 | 18.4 | 3.6 | 1.5 | 28.5 |
| Noroeste | 9,629 | 2.9 | 56.8 | 11.0 | 10.9 | 7.6 | 26.7 |
| Norte | 9,627 | 2.9 | 49.3 | 9.6 | 11.2 | 4.2 | 30.0 |
| Leste | 6,376 | 3.0 | 63.3 | 12.2 | 4.5 | 10.1 | 36.5 |
| Centro | 1,309 | 9.5 | 33.7 | 39.1 | 6.9 | 0.4 | 20.5 |
| Sul | 1,003 | 8.4 | 13.8 | 29.3 | 13.1 | 1.3 | 34.3 |

## Year of emergence

- 2016 or later: 16,494 (29.7%); earlier: 37,299 (67.1%); unknown: 1,797 (3.2%)
- Counts by year: 2001: 1, 2002: 3,652, 2003: 203, 2004: 3,150, 2005: 1,201, 2006: 1,596, 2007: 338, 2008: 7,988, 2009: 1,810, 2010: 215, 2011: 29, 2012: 7,999, 2013: 3,092, 2014: 2,739, 2015: 3,286, 2016: 1,930, 2017: 1,952, 2018: 1,469, 2019: 1,436, 2020: 2,097, 2021: 2,156, 2022: 1,486, 2023: 2,773, 2024: 884, 2025: 309, 2026: 2

## Classes

| Class | Footprints | % | Area (m²) | % area | Mean area (m²) |
|---|---:|---:|---:|---:|---:|
| CASA_TERREA | 30,808 | 55.4 | 4,136,634 | 45.7 | 134 |
| SALA_COMERCIAL | 7,906 | 14.2 | 2,017,947 | 22.3 | 255 |
| BENFEITORIA | 4,908 | 8.8 | 648,897 | 7.2 | 132 |
| CASA_SOBRADO | 2,711 | 4.9 | 406,998 | 4.5 | 150 |
| CASA_COND_FECHADO | 2,632 | 4.7 | 418,916 | 4.6 | 159 |
| FALSO_POLIGONO | 1,737 | 3.1 | 284,007 | 3.1 | 164 |
| PUBLICO | 1,085 | 2.0 | 346,508 | 3.8 | 319 |
| CASA_AREA_VERDE | 943 | 1.7 | 162,631 | 1.8 | 172 |
| NAO_IDENTIFICADO | 828 | 1.5 | 133,938 | 1.5 | 162 |
| RELIGIOSO | 526 | 0.9 | 122,245 | 1.4 | 232 |
| EDIFICIO_RESIDENCIAL | 433 | 0.8 | 111,250 | 1.2 | 257 |
| DEMOLICAO | 392 | 0.7 | 68,343 | 0.8 | 174 |
| DEMOLICAO_CONSTRUCAO | 371 | 0.7 | 85,133 | 0.9 | 229 |
| EDIFICIO_COMERCIAL | 272 | 0.5 | 99,535 | 1.1 | 366 |
| CONSTRUCAO_PARALIZADA | 27 | 0.0 | 3,889 | 0.0 | 144 |
| EM_CONSTRUCAO | 11 | 0.0 | 2,074 | 0.0 | 189 |

## High-standard flag by class

| class_label           |   0.0 |   1.0 |
|:----------------------|------:|------:|
| BENFEITORIA           |  4855 |    52 |
| CASA_AREA_VERDE       |   885 |    58 |
| CASA_COND_FECHADO     |  2071 |   561 |
| CASA_SOBRADO          |  2460 |   250 |
| CASA_TERREA           | 30475 |   324 |
| CONSTRUCAO_PARALIZADA |    27 |     0 |
| DEMOLICAO             |   392 |     0 |
| DEMOLICAO_CONSTRUCAO  |   371 |     0 |
| EDIFICIO_COMERCIAL    |   268 |     4 |
| EDIFICIO_RESIDENCIAL  |   423 |     9 |
| EM_CONSTRUCAO         |    11 |     0 |
| FALSO_POLIGONO        |  1736 |     1 |
| NAO_IDENTIFICADO      |   827 |     1 |
| PUBLICO               |  1084 |     1 |
| RELIGIOSO             |   526 |     0 |
| SALA_COMERCIAL        |  7891 |    13 |
