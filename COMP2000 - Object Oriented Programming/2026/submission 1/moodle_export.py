#!/usr/bin/env python3
"""Export graded marks + marker feedback from marking.xlsx to a Moodle import CSV."""
import argparse
import pathlib

import pandas as pd

GRADE_ITEM = "Submission 1"


def read_marking(folder: pathlib.Path) -> pd.DataFrame:
    df = pd.read_excel(folder / "marking.xlsx", sheet_name="evidence", dtype={"id": str})
    df = df.rename(columns={"id": "idnumber", "total": "grade"})
    df["grade"] = pd.to_numeric(df["grade"], errors="coerce")
    df["idnumber"] = df["idnumber"].astype(str).str.strip()
    df["email address"] = df["email"].astype(str).str.strip()
    df["feedback"] = df["notes"].fillna("").astype(str).str.replace("; ", "\n\n").str.strip()
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=pathlib.Path, default=pathlib.Path(__file__).parent)
    parser.add_argument("--out", type=pathlib.Path, default=pathlib.Path("moodle_import.csv"))
    args = parser.parse_args()

    df = read_marking(args.folder)
    graded = df[df["grade"].notna() & (df["grade"] != 0)].copy()
    print(f"graded rows: {len(graded)}")

    bad_id = graded[~graded["idnumber"].str.match(r"^\d{8}$")]
    bad_email = graded[~graded["email address"].str.contains("@")]
    bad_grade = graded[(graded["grade"] < 0) | (graded["grade"] > 100)]
    no_feedback = graded[graded["feedback"] == ""]
    for label, bad in [
        ("non-8-digit id", bad_id),
        ("missing email", bad_email),
        ("grade outside 0-100", bad_grade),
        ("empty feedback", no_feedback),
    ]:
        if not bad.empty:
            print(f"  warning: {len(bad)} row(s) with {label}: {list(bad['idnumber'])}")

    export = graded[["idnumber", "email address"]].copy()
    export[GRADE_ITEM] = graded["grade"].map(lambda v: f"{v:.1f}")
    export[f"{GRADE_ITEM} feedback"] = graded["feedback"]

    export.to_csv(args.folder / args.out, index=False, encoding="utf-8")
    print(f"wrote: {args.folder / args.out}")
    print(f"grade range: {graded['grade'].min():.1f} - {graded['grade'].max():.1f}")
    print(
        f"feedback length: min {graded['feedback'].str.len().min()}, "
        f"median {int(graded['feedback'].str.len().median())}, max {graded['feedback'].str.len().max()}"
    )


if __name__ == "__main__":
    main()