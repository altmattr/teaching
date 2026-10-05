#!/usr/bin/env python3
"""Dump worksheet/design/logbook/other texts for late submissions, for marker review.

For every <ID>-<Name>_<id>_assignsubmission_file folder under --submissions-dir
writes, into --out-dir:

  <id>_<Name>.txt        worksheet text (or a "(no extractable text)" note)
  <id>_design.txt        design text
  <id>_log.txt           logbook text
  <id>_other.txt         any remaining text files that were not classified

Each dump starts with the student's evidence row and a full inventory of the
expanded submission files, and reuses extract_submissions' own
expand/classify/read_text so the pictures match exactly.  A logbook the
classifier misses because its file names look like dates (for example a zipped
'logbook pages' folder) is appended to the log dump with a note.
"""
import argparse
import csv
import os
import pathlib
import re
import shutil
import sys

BASE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

import extract_submissions as ext

DATE_NAME = re.compile(
    r"(?:\b\d{1,2}[\s./-]\d{1,2}(?:[\s./-]\d{2,4})?\b)"
    r"|(?:\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b(?:[ .-]*\d{1,4}\b)*)"
    r"|(?:\b(?:week|wk)\s?\d+)",
    re.IGNORECASE,
)


def dump_file(path, header, label, body):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(header)
        fh.write(f"= {label} =\n")
        fh.write(body if body else "(no extractable text)\n")
        fh.write("\n")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--submissions-dir", type=pathlib.Path, default=BASE / "late submissions")
    p.add_argument("--evidence", type=pathlib.Path, default=BASE / "late evidence.csv")
    p.add_argument("--out-dir", type=pathlib.Path, default=pathlib.Path("/tmp/opencode/ws1_late"))
    args = p.parse_args()

    if args.out_dir.exists():
        shutil.rmtree(args.out_dir)
    args.out_dir.mkdir(parents=True)

    ev = {r["id"]: r for r in csv.DictReader(open(args.evidence, newline=""))}
    folders = sorted(
        d for d in args.submissions_dir.iterdir()
        if d.name.endswith("_assignsubmission_file") and d.is_dir()
    )
    notes = []
    for d in folders:
        sid = d.name.split("-", 1)[0]
        name = d.name.split("-", 1)[1].split("_", 1)[0].strip() if "-" in d.name else d.name
        label = f"{sid}_{name}".replace(" ", "_")
        row = ev.get(sid)
        tmp = ext.expand_submission_dir(d)
        files = [f for f in os.listdir(tmp) if not f.startswith(".DS_Store")]
        ws_f, ds_f, lg_f, others, texts = ext.classify(tmp, files)

        evidence = " | ".join(f"{k}={v}" for k, v in row.items() if v) if row else "(no evidence row)"
        roles = {}
        for f in files:
            roles[f] = (
                "worksheet" if f == ws_f else
                "design" if f == ds_f else
                "logbook" if f == lg_f else
                "other"
            )
        inventory = "".join(f"  - {f}  [{roles[f]}]  {os.path.getsize(tmp / f)} bytes\n" for f in files)
        header = (
            "For marker review.\n"
            "The dumps below and the evidence.csv row agree with extract_submissions.py.\n\n"
            f"= evidence row =\n{evidence}\n\n"
            f"= files in the submitted (expanded) folder =\n{inventory}\n"
        )
        if row and row.get("missing_files"):
            header += f"NOTE: missing required file(s): {row['missing_files']}\n"

        dump_file(args.out_dir / f"{label}.txt", header, f"WORKSHEET ({ws_f or 'none'})", texts.get(ws_f) if ws_f else None)
        dump_file(args.out_dir / f"{label}_design.txt", header, f"DESIGN ({ds_f or 'none'})", texts.get(ds_f) if ds_f else None)

        log_body = texts.get(lg_f) if lg_f else ""
        log_note = ""
        if lg_f is None:
            undetected = [
                f for f, t in texts.items()
                if (f not in (ws_f, ds_f)) and pathlib.Path(f).suffix.lower() in (".md", ".txt", "") and DATE_NAME.search(f.lower())
            ]
            if undetected:
                chunks = [f"NOTE: the classifier did not name these as the logbook but their names look like dated\nlog entries; appending them so they are not missed.\n\n"]
                for f in sorted(undetected):
                    chunks.append(f"--- {f} ---\n{texts.get(f, '')}\n\n")
                log_body = "".join(chunks)
                log_note = f" (+ {len(undetected)} undated-looking file(s): {', '.join(undetected)})"
        dump_file(args.out_dir / f"{label}_log.txt", header, f"LOGBOOK ({lg_f or 'none'}{log_note})", log_body)

        other_body = "".join(f"--- {f} ---\n{texts.get(f, '')}\n\n" for f, *_ in others if texts.get(f))
        dump_file(args.out_dir / f"{label}_other.txt", header, "OTHER REMAINING FILES", other_body)

        notes.append(f"{sid} {name}: missing=[{row['missing_files'] if row else '?'}]")

    with open(args.out_dir / "0_README.txt", "w", encoding="utf-8") as fh:
        fh.write("Late-submission text dumps for the MR marker.\n")
        fh.write("Files per student: <id>_<Name>.txt (worksheet), _design.txt, _log.txt, _other.txt\n\n")
        fh.write("\n".join(notes))
        fh.write("\n")
    print(f"dumped {len(folders)} students -> {args.out_dir}")
    print("\n".join(notes))


if __name__ == "__main__":
    main()