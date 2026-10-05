#!/usr/bin/env python3
"""Populate the Moodle grading worksheet with grades + marker feedback from marking.xlsx."""
import argparse
import csv
import pathlib

import pandas as pd

GRADE_COL = "Grade"
FEEDBACK_COL = "Feedback comments"
ID_COL = "ID number"


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
    parser.add_argument(
        "--grading-worksheet",
        type=pathlib.Path,
        default=pathlib.Path("grading worksheet.csv"),
        help="Moodle grading worksheet CSV to populate (default: grading worksheet.csv)",
    )
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

    ws_path = args.folder / args.grading_worksheet
    rows = list(csv.DictReader(open(ws_path, encoding="utf-8-sig")))
    fieldnames = list(rows[0].keys())

    by_id = graded.set_index("idnumber")
    filled = 0
    unmatched = []
    for row in rows:
        sid = row[ID_COL].strip()
        hit = by_id.loc[sid] if sid in by_id.index else None
        if hit is None:
            continue
        row[GRADE_COL] = f"{hit['grade']:.1f}"
        row[FEEDBACK_COL] = hit["feedback"]
        filled += 1

    for sid in by_id.index:
        if sid not in {r[ID_COL].strip() for r in rows}:
            unmatched.append(sid)

    with open(ws_path, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"filled: {filled} row(s) in {ws_path}")
    if unmatched:
        print(f"  warning: {len(unmatched)} graded student(s) not found in worksheet: {unmatched}")
    blank = sum(1 for r in rows if not r[GRADE_COL].strip())
    print(f"rows left blank: {blank}")
    print(f"grade range: {graded['grade'].min():.1f} - {graded['grade'].max():.1f}")


if __name__ == "__main__":
    main()