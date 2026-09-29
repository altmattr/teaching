#!/usr/bin/env python3
"""One-way ANOVA comparing grades awarded by different markers in marking.xlsx."""
import argparse
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

CRITERIA = [
    "version control",
    "program design",
    "generics/exceptions",
    "creativity",
    "log book",
]


def read_marking(folder: pathlib.Path) -> pd.DataFrame:
    df = pd.read_excel(folder / "marking.xlsx", sheet_name="evidence", dtype={"id": str})
    df["total"] = pd.to_numeric(df["total"], errors="coerce")
    for col in CRITERIA:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["marker"] = df["marker"].astype(str).str.strip()
    df = df[df["total"].notna() & (df["total"] != 0)]
    df = df[df["marker"] != ""]
    return df


def anova_for_series(values: pd.Series, groups: pd.Series) -> dict:
    markers = groups.astype(str)
    present = values.notna() & markers.str.strip().ne("")
    subgroup = pd.DataFrame({"v": values[present], "g": markers[present]})
    gb = [
        subgroup.loc[subgroup["g"] == m, "v"].to_numpy(dtype=float)
        for m in sorted(subgroup["g"].unique())
    ]
    gb = [g for g in gb if g.size > 0]
    group_names = sorted(subgroup["g"].unique())
    if len(gb) < 2:
        return None
    f, p = stats.f_oneway(*gb)
    all_v = np.concatenate(gb)
    grand = all_v.mean()
    ss_between = sum(g.size * (g.mean() - grand) ** 2 for g in gb)
    ss_total = float(((all_v - grand) ** 2).sum())
    eta = ss_between / ss_total if ss_total else np.nan
    lev_f, lev_p = stats.levene(*gb)
    return {
        "groups": [(name, g) for name, g in zip(group_names, gb)],
        "f": f,
        "p": p,
        "eta": eta,
        "levene_p": lev_p,
        "n": all_v.size,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=pathlib.Path, default=pathlib.Path(__file__).parent)
    parser.add_argument("--out", type=pathlib.Path, default=pathlib.Path("marker_anova.png"))
    args = parser.parse_args()

    df = read_marking(args.folder)
    markers = df["marker"]
    variables = list(CRITERIA) + ["total"]

    print(f"graded rows with marker: {len(df)}")
    print(f"markers: {sorted(markers.unique())}\n")
    results = {}
    for var in variables:
        res = anova_for_series(df[var], markers)
        results[var] = res

    print_table(variables, results)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    for ax, var in zip(axes.flat, variables):
        res = results[var]
        if res is None:
            ax.set_title(f"{var}  (fewer than 2 marker groups)")
            ax.axis("off")
            continue
        names = [n for n, _ in res["groups"]]
        data = [g for _, g in res["groups"]]
        bp = ax.boxplot(data, tick_labels=names, widths=0.5, patch_artist=True)
        for i, (patch, name) in enumerate(zip(bp["boxes"], names), start=1):
            grp = [g for n2, g in res["groups"] if n2 == name][0]
            patch.set_facecolor("#1f77b4" if name == min(names) else "#ff7f0e")
            ax.scatter([i], [grp.mean()], color="crimson", zorder=5, s=60, marker="D")
        ax.set_title(f"{var}  (F = {res['f']:.2f}, p = {res['p']:.3f})")
        ax.set_ylabel("mark")
        ax.grid(alpha=0.3, axis="y")
        ax.margins(y=0.1)

    fig.suptitle("One-way ANOVA of grades by marker", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    out = args.folder / args.out
    fig.savefig(out, dpi=150)
    print(f"\nsaved: {out}")


def print_table(variables: list[str], results: dict) -> None:
    print(
        f"{'variable':<22}{'marker':>8}{'n':>5}{'mean':>8}{'sd':>8}"
        f"{'  F':>8}{'p':>9}{'eta^2':>8}{'levene p':>10}"
    )
    print("-" * 86)
    for var in variables:
        res = results[var]
        if res is None:
            print(f"{var:<22} insufficient groups")
            continue
        for name, g in res["groups"]:
            print(
                f"{var:<22}{name:>8}{g.size:>5}{g.mean():>8.2f}{g.std():>8.2f}"
                f"{res['f']:>8.2f}{res['p']:>9.3f}{res['eta']:>8.2f}{res['levene_p']:>10.3f}"
            )
            var = ""
        print()


if __name__ == "__main__":
    main()