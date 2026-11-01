"""Build the public GYN-OBV release from the internal inspection GeoPackage.

Usage: python scripts/build_release.py <internal_inspection.gpkg>

The internal file is not distributed. This script documents every
transformation applied to it: columns that could help locate a property
through an address are dropped, invalid years are set to null and the
public GeoPackage, CSV and class guide are written to data/.
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

KEEP = ["plus_code", "confidence", "area_m2", "region", "neighbourhood",
        "class_code", "class_label", "high_standard", "year_emergence",
        "inspection", "geometry"]
DROPPED = ["latitude", "longitude", "plus_code_address", "street", "address"]

CLASSES = [
    (0, "FALSO_POLIGONO", "No building (false polygon)", "Sem edificação (falso polígono)", "Data quality"),
    (1, "CASA_TERREA", "Single-storey house", "Casa térrea", "Residential"),
    (2, "CASA_COND_FECHADO", "House in a gated community", "Casa em condomínio fechado", "Residential"),
    (3, "EDIFICIO_RESIDENCIAL", "Residential building", "Edifício residencial", "Residential"),
    (4, "EDIFICIO_COMERCIAL", "Commercial building", "Edifício comercial", "Non-residential"),
    (5, "SALA_COMERCIAL", "Commercial unit or shed", "Sala comercial ou galpão", "Non-residential"),
    (6, "CASA_AREA_VERDE", "Dwelling in a green area", "Moradia em área verde", "Residential"),
    (7, "BENFEITORIA", "Extension of an existing building", "Benfeitoria (ampliação)", "Lot transformation"),
    (8, "CASA_SOBRADO", "House with two or more storeys", "Sobrado", "Residential"),
    (9, "NAO_IDENTIFICADO", "Type cannot be decided from the imagery", "Não identificado", "Data quality"),
    (10, "PUBLICO", "Public or institutional building", "Edificação pública ou institucional", "Non-residential"),
    (11, "RELIGIOSO", "Church or temple", "Templo religioso", "Non-residential"),
    (12, "DEMOLICAO", "Building removed", "Demolição", "Lot transformation"),
    (13, "DEMOLICAO_CONSTRUCAO", "Building removed and replaced", "Demolição seguida de construção", "Lot transformation"),
    (14, "EM_CONSTRUCAO", "Work in progress", "Em construção", "Lot transformation"),
    (15, "CONSTRUCAO_PARALIZADA", "Halted work", "Construção paralisada", "Lot transformation"),
]


def main(src: str) -> None:
    gdf = gpd.read_file(src, layer="gyn_obv")
    assert len(gdf) == 55590 and gdf.plus_code.is_unique
    gdf = gdf.drop(columns=[c for c in DROPPED if c in gdf.columns])[KEEP]

    # years outside the Google Earth archive (data-entry errors) -> null
    bad = gdf.year_emergence.notna() & (gdf.year_emergence < 1990)
    print(f"invalid years set to null: {int(bad.sum())}")
    gdf.loc[bad, "year_emergence"] = np.nan
    gdf["year_emergence"] = gdf.year_emergence.astype("Int64")
    gdf["high_standard"] = gdf.high_standard.astype("Int64")

    gdf = gdf.sort_values(["region", "neighbourhood", "plus_code"]).reset_index(drop=True)
    gdf.insert(0, "fid", np.arange(1, len(gdf) + 1))

    DATA.mkdir(exist_ok=True)
    gdf.to_file(DATA / "gyn_obv.gpkg", layer="gyn_obv", driver="GPKG")
    csv = pd.DataFrame(gdf.drop(columns="geometry"))
    csv["wkt"] = gdf.geometry.to_wkt(rounding_precision=7)
    csv.to_csv(DATA / "gyn_obv.csv", index=False, encoding="utf-8")

    guide = pd.DataFrame(CLASSES, columns=["class_code", "class_label", "meaning_en", "meaning_pt", "group"])
    guide["footprints"] = guide.class_code.map(gdf.class_code.value_counts()).fillna(0).astype(int)
    guide.to_csv(DATA / "class_guide.csv", index=False, encoding="utf-8")
    print(guide[["class_code", "class_label", "footprints"]].to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1])
