#!/usr/bin/env python3
"""Extract machine facts from COMP2000 Submission 1 folders into evidence.csv.

Run from the directory containing this script:  python3 extract_submissions.py
Outputs evidence.csv with one row per student, keyed on the id that prefixes
each submission folder name.  Only facts a script can prove are recorded here;
no grades.
"""

import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import fitz  # pymupdf
except ImportError:
    fitz = None
try:
    import docx
except ImportError:
    docx = None
import zipfile
from xml.etree import ElementTree

BASE = Path(__file__).resolve().parent
SUBMISSIONS = BASE / "submissions"
PRESENTERS = BASE / "presenters.csv"
PARTICIPANTS = BASE / "participants.csv"
OUT = BASE / "evidence.csv"

PRACTICAL_RE = re.compile(
    r"\[Practical_\d+\|([A-Z]{3})\|(\d{1,2}:\d{2}[AP]M)\|([A-Z0-9]+)\]"
)

SECTION_RE = re.compile(r"(\d\.\d)[.\s]")
PROMPT_FRAGS = (
    "paste the first 10 lines", "describe your workflow", "estimate the percentage",
    "list every class", "identify any inheritance", "pick the class",
    "paste one code snippet", "list every place your code uses generics",
    "list every place your code handles exceptions", "paste a code snippet",
    "which week's activity", "list everything you added", "which feature required",
    "paste one code snippet that you are especially proud",
)
GITLOG_RE = re.compile(r"^[*|/\\]?\s*[0-9a-f]{7,40}\b")
DATE_WORDS = re.compile(
    r"\b(?:mon|tue|wed|thu|fri|sat|sun)[a-z]*\b|"
    r"\b\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?\b|"
    r"\b(?:week|wk)\s?\d+\b|"
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s?\d{0,4}\b",
    re.IGNORECASE,
)
GITHUB_HTTP_RE = re.compile(r"https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.\-]+")
GITHUB_SSH_RE = re.compile(r"git@github\.com[:/][A-Za-z0-9_.-]+/[A-Za-z0-9_.\-]+")


def expand_submission_dir(rel):
    """Mirror a submission folder into /tmp, unzipping any inner submission
    zip files (the files the student was told not to zip) so they can be
    classified like normal files.  Returns (tmp_path)."""
    tmp = Path(tempfile.mkdtemp(prefix="subm1_"))
    for f in os.listdir(rel):
        src = rel / f
        if src.is_dir():
            shutil.copytree(src, tmp / f)
        elif src.suffix.lower() == ".zip":
            try:
                with zipfile.ZipFile(src) as z:
                    z.extractall(tmp)
            except Exception:
                shutil.copy2(src, tmp / f)
        else:
            shutil.copy2(src, tmp / f)
    # flatten one level: any subdirectory files get moved up so classify sees them
    for root, dirs, fnames in os.walk(tmp):
        for fn in fnames:
            p = Path(root) / fn
            if p.parent != tmp:
                shutil.move(str(p), tmp / fn)
    return tmp


def read_text(path):
    """Return lowercased text somewhere?  No: return original text of a file."""
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".md" or ext == ".txt" or ext == "":
        try:
            return p.read_text(errors="replace")
        except Exception:
            return ""
    if ext == ".docx" and docx is not None:
        try:
            d = docx.Document(str(p))
            return "\n".join(x.text for x in d.paragraphs if x.text)
        except Exception:
            return ""
    if ext in (".pdf",) and fitz is not None:
        try:
            d = fitz.open(str(p))
            return "\n".join(pg.get_text() for pg in d)
        except Exception:
            return ""
    if ext in (".pdf",) and fitz is None:
        return ""
    if ext in (".odt",):
        try:
            with zipfile.ZipFile(p) as z:
                xml = z.read("content.xml")
            root = ElementTree.fromstring(xml)
            return "\n".join(
                el.text for el in root.iter(
                    "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p"
                )
                if el.text
            )
        except Exception:
            return ""
    return ""  # png/jpg/webp/zip/odt: no text


def classify(relfolder, files):
    """Classify each file as worksheet / design / logbook / other.

    Returns (ws, design, logbook) file names, or None entries when missing.
    """
    def name_sig(low):
        ws = any(k in low for k in (
            "worksheet", "mid-semester submission", "assignment 1 worksheet",
            "week7 worksheet", "assignment submission",
        )) or low.startswith(("w7", "ws7"))
        lg = any(k in low for k in (
            "logbook", "log book", "logs", "weekly", "log 1-6", "log ",
        )) and "worksheet" not in low
        ds = any(k in low for k in (
            "uml", "design", "diagram", "draw", "sketch", "class diagram",
            "mermaid", "architecture", "ecosystem",
        ))
        return ws, lg, ds

    info = []
    for f in files:
        low = f.lower()
        text = read_text(Path(relfolder) / f)
        ws, lg, ds = name_sig(low)

        # content sniffing for ambiguous names
        if not ws and not lg and not ds:
            head = text[:600].lower()
            if re.search(r"1\.?\s*version control|github repo url|student name:.*student id", head):
                ws = True
            elif re.search(r"<<abstract>>|class diagram|:\s*(int|double|boolean|string|void)\b", text[:800].lower()):
                ds = True
            elif re.search(r"\blog ?book\b|entries|week\s?\d", head):
                lg = True
        info.append((f, ws, lg, ds, text, low))

    ws_f = None
    lg_f = None
    ds_f = None
    for f, ws, lg, ds, text, low in info:
        if ws and (ws_f is None or "worksheet" in low):
            ws_f = f
    for f, ws, lg, ds, text, low in info:
        if ds and (ds_f is None or "uml" in low or "design" in low or "diagram" in low):
            ds_f = f
    for f, ws, lg, ds, text, low in info:
        if lg and (lg_f is None or "logbook" in low or "log book" in low or "logs" in low):
            lg_f = f

    # a .md file is normally the worksheet unless its name says log
    for f, ws, lg, ds, text, low in info:
        if lg_f is None and lg and ws_f is None:
            lg_f = f

    others = [f for f in info if f[0] not in (ws_f, lg_f, ds_f)]
    return ws_f, ds_f, lg_f, others, {f[0]: f[4] for f in info}


def section_stats(text):
    """Per-question stats.  Returns dict section -> answer char length."""
    stats = {}
    if not text:
        return stats
    markers = [(m.start(), m.group(1)) for m in SECTION_RE.finditer(text)]
    if not markers:
        return stats
    markers.append((len(text), ""))
    for idx in range(len(markers) - 1):
        sec = markers[idx][1]
        if sec not in {"1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "2.4", "3.1", "3.2", "3.3", "4.1", "5.1", "5.2", "5.3"}:
            continue
        body = text[markers[idx][0]:markers[idx + 1][0]]
        body = re.sub(r"\b\d\.\d\b.*", "", body, count=1)  # drop the marker line itself
        body = re.sub(r"\n{2,}", "\n", body)
        for frag in PROMPT_FRAGS:
            body = re.sub(re.escape(frag), "", body, flags=re.IGNORECASE)
        body = body.strip().strip("#").strip(" -_*").strip()
        stats[sec] = len(body)
    return stats


def gitlog_lines(text):
    """Count plausible git log lines pasted under section 1.1."""
    if not text:
        return 0
    m = re.search(r"1\.1[.\s]", text)
    if not m:
        return 0
    seg = text[m.end():]
    m2 = re.search(r"1\.2[.\s]", seg)
    if m2:
        seg = seg[:m2.start()]
    lines = [ln.strip() for ln in seg.splitlines() if ln.strip()]
    loglines = 0
    for ln in lines:
        if GITLOG_RE.match(ln) or ln.startswith("*") or "merge" in ln.lower() or ln.startswith("|"):
            loglines += 1
    return loglines


def logbook_entries(text, fname):
    if not text:
        return "no_text"
    hits = DATE_WORDS.findall(text)
    weeks = len(set(h.lower() for h in hits))
    if weeks == 0:
        return "0"
    return str(weeks)


def repo_urls(text):
    http = GITHUB_HTTP_RE.findall(text)
    ssh = GITHUB_SSH_RE.findall(text)
    return (http[0] if http else None), (ssh[0].replace(":", "/", 1) if ssh else None)


def repo_status(url):
    if not url:
        return "no_url"
    candidates = [url]
    if url.startswith("git@github.com:"):
        candidates.append("https://github.com/" + url.split(":", 1)[1])
    for u in candidates:
        try:
            r = subprocess.run(
                ["git", "ls-remote", "--heads", u],
                capture_output=True, text=True, timeout=25,
            )
            if r.returncode == 0:
                heads = [ln for ln in r.stdout.splitlines() if "refs/heads/" in ln]
                return "reachable", len(heads)
            err = r.stderr.lower()
            if "could not read username" in err or "authentication" in err or "not allowed" in err:
                return "private", 0
            if "repository not found" in err or "could not read from remote" in err or "not a git repository" in err:
                return "dead", 0
            return "unreachable", 0
        except subprocess.TimeoutExpired:
            continue
    return "timeout", 0


def practical_groups():
    """Map student id -> practical group label like 'MON 09:00AM C07'.

    Reads participants.csv (roster export).  The practical sits in a
    [Practical_1|DAY|TIME|ROOM] token inside the Groups column; a student
    present in the file without that token maps to an empty string.
    """
    labels = {}
    if not PARTICIPANTS.exists():
        return labels
    with open(PARTICIPANTS, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        sid = str(r.get("ID number", "")).strip()
        if not sid:
            continue
        m = PRACTICAL_RE.search(r.get("Groups", "") or "")
        if m:
            labels[sid] = f"{m.group(1)} {m.group(2)} {m.group(3)}"
        else:
            labels[sid] = ""
    return labels


def presented_set():
    ids = set()
    if not PRESENTERS.exists():
        return ids, {}
    rows = []
    with open(PRESENTERS, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    emails = {}
    for r in rows[1:]:
        if len(r) < 5:
            continue
        sid = r[2].strip()
        emails[sid] = r[3].strip()
        if r[4].strip().lower() in ("yes", "1", "true", "y"):
            ids.add(sid)
    return ids, emails


def main():
    if not SUBMISSIONS.is_dir():
        sys.exit(f"no submissions dir at {SUBMISSIONS}")
    presented, emails = presented_set()
    practical = practical_groups()
    folders = sorted(
        d for d in os.listdir(SUBMISSIONS)
        if d.endswith("_assignsubmission_file") and (SUBMISSIONS / d).is_dir()
    )

    rows = []
    for d in folders:
        rel = SUBMISSIONS / d
        tmp = expand_submission_dir(rel)
        files = [f for f in os.listdir(tmp) if not f.startswith(".DS_Store")]
        sid = d.split("-", 1)[0]
        name = d.split("-", 1)[1].split("_", 1)[0].strip() if "-" in d else d
        ws_f, ds_f, lg_f, others, texts = classify(tmp, files)

        ws_stats = section_stats(texts.get(ws_f, "")) if ws_f else {}
        git_lines = gitlog_lines(texts.get(ws_f, ""))

        url, _ = repo_urls(texts.get(ws_f, ""))
        status, branches = repo_status(url) if url else ("no_url", 0)

        lg_entries = logbook_entries(texts.get(lg_f, ""), lg_f or "") if lg_f else "missing"

        missing = []
        if ws_f is None:
            missing.append("worksheet")
        if ds_f is None:
            missing.append("design")
        if lg_f is None:
            missing.append("logbook")
        missing = ";".join(missing)

        ws_type = Path(ws_f).suffix.lower() if ws_f else ""
        if ws_f and ws_type == "":
            ws_type = "noext"

        row = {
            "id": sid,
            "name": name,
            "email": emails.get(sid, ""),
            "presented": "yes" if sid in presented else ("no" if emails.get(sid) else "no"),
            "practical_group": practical.get(sid, ""),
            "worksheet_file": ws_f or "",
            "worksheet_type": ws_type,
            "design_file": ds_f or "",
            "logbook_file": lg_f or "",
            "other_files": ";".join(o[0] for o in others),
            "repo_url": url or "",
            "repo_status": status,
            "branch_count": branches,
            "filled_sections": ",".join(f"{k}={v}" for k, v in sorted(ws_stats.items())),
            "gitlog_lines": git_lines,
            "logbook_entries": lg_entries,
            "missing_files": missing,
        }
        rows.append(row)

    cols = [
        "id", "name", "email", "presented", "practical_group",
        "worksheet_file", "worksheet_type", "design_file", "logbook_file", "other_files",
        "repo_url", "repo_status", "branch_count",
        "filled_sections", "gitlog_lines", "logbook_entries", "missing_files",
    ]
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"rows: {len(rows)}  ->  {OUT}")
    print("presented:", sorted(presented))
    no3 = [r["id"] for r in rows if r["missing_files"]]
    print("folders missing a required file:", len(no3), no3)
    nomatch = [r["id"] for r in rows if not r["practical_group"]]
    print("rows without a practical group:", len(nomatch), nomatch)
    cnt = Counter(r["practical_group"] for r in rows if r["practical_group"])
    print("practical groups:", dict(sorted(cnt.items())))


if __name__ == "__main__":
    main()