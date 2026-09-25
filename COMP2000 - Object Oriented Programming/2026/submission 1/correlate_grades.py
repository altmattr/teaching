#!/usr/bin/env python3
"""Compare the grades in marks.csv against the equivalent grades in marking.xlsx."""
import argparse
import csv
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CRITERIA = [
    "version control",
    "program design",
    "generics/exceptions",
    "creativity",
    "log book",
]

CSV_COLUMNS = {
    "version control": "version_control",
    "program design": "program_design",
    "generics/exceptions": "generics_exceptions",
    "creativity": "uniqueness_creativity",
    "log book": "log_book",
}

XLSX_COLUMNS = {
    "version control": "version control",
    "program design": "program design",
    "generics/exceptions": "generics/exceptions",
    "creativity": "creativity",
    "log book": "log book",
}


def read_marks_csv(path: pathlib.Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"id": str}, keep_default_na=False)
    df = df[["id"] + list(CSV_COLUMNS.values())].copy()
    df.columns = ["id"] + list(CSV_COLUMNS.keys())
    return _drop_empty_ids(_as_numeric(df))


def read_marking_xlsx(path: pathlib.Path) -> pd.DataFrame:
    df = pd.read_excel(
        path, sheet_name="evidence", dtype={"id": str}, keep_default_na=False
    )
    df = df[["id", "total"] + list(XLSX_COLUMNS.values())].copy()
    df.columns = ["id", "total"] + list(XLSX_COLUMNS.keys())
    return _drop_empty_ids(_as_numeric(df))


def _drop_empty_ids(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["id"].astype(str).str.strip() != ""].reset_index(drop=True)


def _as_numeric(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if col != "id":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def add_total(df: pd.DataFrame) -> pd.DataFrame:
    df["total"] = df[CRITERIA].mean(axis=1)
    return df


def corr_stats(x: pd.Series, y: pd.Series) -> dict:
    mask = x.notna() & y.notna()
    x, y = x[mask], y[mask]
    n = int(mask.sum())
    pearson = x.corr(y, method="pearson")
    spearman = x.rank().corr(y.rank())
    mad = (x - y).abs().mean()
    return {"n": n, "pearson": pearson, "spearman": spearman, "mad": mad, "x": x, "y": y}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=pathlib.Path, default=pathlib.Path(__file__).parent)
    parser.add_argument("--marks", type=pathlib.Path, default=pathlib.Path("marks.csv"))
    parser.add_argument("--marking", type=pathlib.Path, default=pathlib.Path("marking.xlsx"))
    parser.add_argument("--out", type=pathlib.Path, default=pathlib.Path("grade_correlation.png"))
    args = parser.parse_args()

    marks = args.folder / args.marks
    marking = args.folder / args.marking
    if not marks.exists():
        parser.error(f"missing file: {marks}")
    if not marking.exists():
        parser.error(f"missing file: {marking}")

    csv_df = add_total(read_marks_csv(marks))
    xlsx_df = read_marking_xlsx(marking)

    merged = csv_df.merge(xlsx_df, on="id", suffixes=("_csv", "_xlsx"))
    only_csv = len(csv_df) - len(merged)
    only_xlsx = len(xlsx_df) - len(merged)
    if only_csv or only_xlsx:
        print(f"warning: ids only in marks.csv: {only_csv}, only in marking.xlsx: {only_xlsx}")

    before = len(merged)
    merged = merged[merged["total_xlsx"] != 0]
    dropped = before - len(merged)
    if dropped:
        print(f"excluded {dropped} row(s) with zero total in marking.xlsx")

    labels = list(CRITERIA) + ["total"]
    rows = [corr_stats(merged[f"{c}_csv"], merged[f"{c}_xlsx"]) for c in labels]

    print_table(labels, rows)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    rng = np.random.default_rng(42)
    for ax, label, stats in zip(axes.flat, labels, rows):
        x = stats["x"].to_numpy()
        y = stats["y"].to_numpy()
        x_jitter = x + rng.normal(0, 0.8, size=x.size)
        ax.scatter(x_jitter, y, s=22, alpha=0.6, edgecolors="none", color="#1f77b4")
        if stats["n"] >= 2:
            m, b = np.polyfit(x, y, 1)
            xs = np.linspace(x.min(), x.max(), 50)
            ax.plot(xs, m * xs + b, color="crimson", lw=1.5)
        ax.set_title(f"{label}  (r = {stats['pearson']:.2f}, rho = {stats['spearman']:.2f})")
        ax.set_xlabel("marks.csv")
        ax.set_ylabel("marking.xlsx")
        ax.set_xlim(0, 105)
        ax.set_ylim(0, 105)
        ax.grid(alpha=0.3)

    fig.suptitle("Correlation between marks.csv and marking.xlsx", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    out = args.folder / args.out
    fig.savefig(out, dpi=150)
    print(f"\nsaved: {out}")


def print_table(labels: list[str], rows: list[dict]) -> None:
    header = ("criterion", "n", "pearson r", "r^2", "spearman rho", "mean abs diff")
    print()
    print(f"{header[0]:<22}{header[1]:>5}{header[2]:>11}{header[3]:>7}{header[4]:>14}{header[5]:>15}")
    print("-" * 74)
    for label, stats in zip(labels, rows):
        print(
            f"{label:<22}{stats['n']:>5}{stats['pearson']:>11.3f}"
            f"{stats['pearson']**2:>7.3f}{stats['spearman']:>14.3f}{stats['mad']:>15.2f}"
        )


if __name__ == "__main__":
    main()