"""Reproduce the technical-validation statistics reported for GYN-OBV.

Usage: python scripts/technical_validation.py   (writes results/technical_validation.md)
"""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportion_confint

ROOT = Path(__file__).resolve().parents[1]
gdf = gpd.read_file(ROOT / "data" / "gyn_obv.gpkg", layer="gyn_obv", fid_as_index=True)
N = len(gdf)


def wilson(k, n):
    lo, hi = proportion_confint(k, n, alpha=0.05, method="wilson")
    return f"{100*k/n:.2f} ({100*lo:.2f}–{100*hi:.2f})"


out = ["# GYN-OBV technical validation (reproduced from data/gyn_obv.gpkg)", ""]
fp = gdf.class_code == 0
ni = gdf.class_code == 9
ok = ~(fp | ni)
out += [f"- Footprints: {N:,}; total area {gdf.area_m2.sum():,.0f} m²",
        f"- Commission error (FALSO_POLIGONO), % (Wilson 95% CI): {wilson(fp.sum(), N)}; n = {fp.sum():,}",
        f"- Not identified (NAO_IDENTIFICADO), %: {wilson(ni.sum(), N)}; n = {ni.sum():,}",
        f"- Confirmed buildings: {ok.sum():,} ({100*ok.mean():.2f}%), area {gdf.area_m2[ok].sum():,.0f} m²",
        f"- High standard flagged: {int((gdf.high_standard == 1).sum()):,}; missing flag: {int(gdf.high_standard.isna().sum())}",
        ""]

bands = [0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 1.01]
labels = ["0.65–0.70", "0.70–0.75", "0.75–0.80", "0.80–0.85", "0.85–0.90", "≥ 0.90"]
gdf["band"] = pd.cut(gdf.confidence, bands, right=False, labels=labels)
out += ["## Commission and indeterminacy by confidence score", "",
        "| Confidence | Footprints | Share | False polygons, % (CI) | Not identified, % (CI) |", "|---|---:|---:|---:|---:|"]
for b, d in gdf.groupby("band", observed=True):
    out.append(f"| {b} | {len(d):,} | {100*len(d)/N:.1f}% | {wilson((d.class_code==0).sum(), len(d))} | {wilson((d.class_code==9).sum(), len(d))} |")
hi = gdf.confidence >= 0.80
lo = gdf.confidence < 0.75
out += ["", f"- Confidence ≥ 0.80: {100*hi.mean():.1f}% of footprints; commission {wilson((fp & hi).sum(), hi.sum())}",
        f"- Confidence < 0.75: {100*lo.mean():.1f}% of footprints, holding {100*(fp & lo).sum()/fp.sum():.1f}% of the false polygons", ""]

out += ["## Commission by footprint area", "", "| Area (m²) | Footprints | False polygons, % (CI) |", "|---|---:|---:|"]
for name, m in [("50–100", gdf.area_m2 < 100), ("100–200", (gdf.area_m2 >= 100) & (gdf.area_m2 < 200)), ("≥ 200", gdf.area_m2 >= 200)]:
    out.append(f"| {name} | {m.sum():,} | {wilson((fp & m).sum(), m.sum())} |")

out += ["", "## Footprints by region (% of each region)", "",
        "| Region | Footprints | False pol. | Single-storey | Commercial unit | Extension | Gated | Emerged 2016+ |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
for r, d in sorted(gdf.groupby("region"), key=lambda x: -len(x[1])):
    pc = lambda m: f"{100*m.mean():.1f}"
    out.append(f"| {r} | {len(d):,} | {pc(d.class_code==0)} | {pc(d.class_code==1)} | {pc(d.class_code==5)} | {pc(d.class_code==7)} | {pc(d.class_code==2)} | {pc(d.year_emergence>=2016)} |")

y = gdf.year_emergence
out += ["", "## Year of emergence", "",
        f"- 2016 or later: {int((y>=2016).sum()):,} ({100*(y>=2016).mean():.1f}%); earlier: {int((y<2016).sum()):,} ({100*(y<2016).mean():.1f}%); unknown: {int(y.isna().sum()):,} ({100*y.isna().mean():.1f}%)",
        "- Counts by year: " + ", ".join(f"{int(k)}: {v:,}" for k, v in y.value_counts().sort_index().items()), ""]

cls = gdf.groupby("class_label").agg(n=("class_code", "size"), area=("area_m2", "sum"), mean_area=("area_m2", "mean")).sort_values("n", ascending=False)
cls["share_n"] = 100 * cls.n / N
cls["share_area"] = 100 * cls.area / gdf.area_m2.sum()
out += ["## Classes", "", "| Class | Footprints | % | Area (m²) | % area | Mean area (m²) |", "|---|---:|---:|---:|---:|---:|"]
for k, r in cls.iterrows():
    out.append(f"| {k} | {int(r.n):,} | {r.share_n:.1f} | {r.area:,.0f} | {r.share_area:.1f} | {r.mean_area:.0f} |")
out += ["", "## High-standard flag by class", "", pd.crosstab(gdf.class_label, gdf.high_standard).to_markdown()]

(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "technical_validation.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
