#!/usr/bin/env python3
"""Bundle COMP2000 Submission 1 students into teams by code-base similarity.

Run from the directory containing this script:  python3 bundle_teams.py
Reads evidence.csv and the submission folders, detects which students share a
code base (same repo, shared commit history, identical design files, similar
worksheet code snippets), clusters them, and writes:

  teams.csv                  group -> practical group + member ids/names + reasons
  evidence.csv               updated with a new group_id column

Teams never span practical groups, so only students in the same practical
(evidence.csv practical_group) are ever merged; thresholds are kept relaxed
because the practical gate already rules out false joins across the room.
Students with no practical group (evidence blank) are left dangling for manual
review.  Group ids are deterministic: G01, G02, ... ordered by the lowest
student id in each team.
"""

import csv
import hashlib
import os
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

import extract_submissions as ex

BASE = Path(__file__).resolve().parent
SUBMISSIONS = BASE / "submissions"
EVIDENCE = BASE / "evidence.csv"
TEAMS = BASE / "teams.csv"

HASH_RE = re.compile(r"\b[0-9a-f]{7}\b")
JAVA_RE = re.compile(
    r"(?:(public|private|protected|static)\s+)|(?:class\s+\w)|"
    r"(?:@Override)|(?:void\s+\w+\s*\(|\w+\s+\w+\s*\([^)]*\)\s*\{)|"
    r"(?:import\s+java)|(?:\btry\s*\{|catch\s*\()|(?:new\s+\w+\([^)]*\))"
)

# tokens that never make a repo name team-specific
GENERIC_TOK = {
    "comp", "comp2000", "2000", "assignment", "assess", "asses", "project",
    "semester", "week", "wk", "a1", "submission", "program", "object",
    "oriented", "oop", "sim", "simulation", "1", "course", "individual",
    "final", "unit", "task", "jid", "predict", "predatorprey",
}


def generic_basename(bn):
    """True when a repo basename is a generic course name, not a team name."""
    if not bn:
        return True
    b = bn.lower().replace("-", "_").replace(".", "_")
    parts = [p for p in b.split("_") if p]
    rem = [p for p in parts if p not in GENERIC_TOK]
    if not rem:
        return True
    if len(rem) == 1 and len(rem[0]) < 5:
        return True
    return False


def repo_basename(url):
    """Return the repo name (last path segment) lowercased, or None."""
    if not url:
        return None
    u = url.rstrip("/").replace(".git", "")
    name = u.split("/")[-1].strip().lower()
    return name or None


def commit_hashes(text):
    """Return the set of 7-char commit hashes pasted under worksheet section 1.1."""
    m = re.search(r"1\.1[.\s]", text)
    if not m:
        return set()
    seg = text[m.end():]
    m2 = re.search(r"1\.2[.\s]", seg)
    if m2:
        seg = seg[:m2.start()]
    return set(HASH_RE.findall(seg))


def java_lines(text):
    """Return lines of a worksheet that look like pasted Java code."""
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if len(s) < 8 or s.startswith(("#", "|", "*", "-", ">", "```")):
            continue
        if JAVA_RE.search(s):
            out.append(s)
    return out


def shingles(tokens, n=3):
    toks = tokens
    if len(toks) < n:
        return set()
    return set(" ".join(toks[i:i + n]) for i in range(len(toks) - n + 1))


def tokenize_code(lines):
    """Normalise Java lines into a token stream for shingling."""
    toks = []
    for ln in lines:
        ln = re.sub(r"//.*$", "", ln)
        ln = re.sub(r'"([^"\\]|\\.)*"', '<str>', ln)
        ln = re.sub(r"'([^'\\]|\\.)'", '<ch>', ln)
        for piece in re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+\.?\d*|[{}()\[\];,.<>=+\-*/!&|?:]", ln):
            toks.append(piece)
    return toks


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def design_sha1(sid, design_file, tmpdir):
    """SHA-1 of the design file bytes (in the expanded temp dir)."""
    if not design_file:
        return None
    p = Path(tmpdir) / design_file
    try:
        return hashlib.sha1(p.read_bytes()).hexdigest()
    except Exception:
        return None


def read_snapshot():
    """Gather per-student descriptors straight from the submission folders."""
    presented, emails = ex.presented_set()
    folders = sorted(
        d for d in os.listdir(SUBMISSIONS)
        if d.endswith("_assignsubmission_file") and (SUBMISSIONS / d).is_dir()
    )
    snap = {}
    for d in folders:
        rel = SUBMISSIONS / d
        sid = d.split("-", 1)[0]
        tmp = ex.expand_submission_dir(rel)
        files = [f for f in os.listdir(tmp) if not f.startswith(".DS_Store")]
        ws_f, ds_f, lg_f, others, texts = ex.classify(tmp, files)
        ws_text = texts.get(ws_f, "") if ws_f else ""
        src = {
            "id": sid,
            "basename": None,
            "commits": commit_hashes(ws_text),
            "shingles": shingles(tokenize_code(java_lines(ws_text))),
            "design_sha": design_sha1(sid, ds_f, tmp),
            "files": files,
            "ws_text_len": len(ws_text),
        }
        snap[sid] = src
        shutil.rmtree(tmp, ignore_errors=True)
    return snap


def load_evidence():
    rows = list(csv.DictReader(open(EVIDENCE, newline="", encoding="utf-8-sig")))
    return {r["id"]: r for r in rows}


def main():
    snap = read_snapshot()
    ev = load_evidence()

    # repo basenames and practical groups come from the evidence (already parsed)
    for sid, src in snap.items():
        src["basename"] = repo_basename(ev.get(sid, {}).get("repo_url", ""))
        src["practical"] = ev.get(sid, {}).get("practical_group", "") or ""

    basename_groups = defaultdict(list)
    for sid, src in snap.items():
        if src["basename"]:
            basename_groups[src["basename"]].append(sid)

    ids = sorted(snap, key=lambda s: int(s))

    # --- build the similarity graph -------------------------------------
    # union-find
    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    reasons = defaultdict(list)  # (a,b) frozenset -> reasons

    # precompute pairwise signals.  Teams never span practical groups (the
    # unit time-tables them into one practical each), so only consider pairs in
    # the same practical.  Students without a practical group (none in this
    # cohort bar one edge case) are left for manual review, not matched.
    edges = []
    for i in range(len(ids)):
        a = ids[i]
        A = snap[a]
        for b in ids[i + 1:]:
            B = snap[b]
            if not A["practical"] or A["practical"] != B["practical"]:
                continue
            r = []

            des = A["design_sha"] and A["design_sha"] == B["design_sha"]
            hj = jaccard(A["commits"], B["commits"])
            sj = jaccard(A["shingles"], B["shingles"])
            bn = A["basename"]
            same_bn = bool(bn) and bn == B["basename"]

            if des:
                r.append(f"identical design")
            if hj >= 0.20:
                r.append(f"commit history jaccard={hj:.2f}")
            if same_bn:
                r.append(f"repo basename '{bn}'")
            if sj >= 0.35:
                r.append(f"code snippets jaccard={sj:.2f}")

            if not r:
                continue
            edges.append((a, b, r))

    # union edges ordered by strength: identical design first, then commit, then basename, then snippets
    def strength(rrs):
        s = 0
        for rr in rrs:
            if rr.startswith("identical"):
                s += 400
            elif rr.startswith("commit"):
                s += 100
            elif rr.startswith("repo"):
                s += 30
            elif rr.startswith("code"):
                s += 10
        return s

    for a, b, rrs in sorted(edges, key=lambda e: -strength(e[2])):
        union(a, b)
        reasons[frozenset((a, b))] = rrs

    # --- assemble groups -------------------------------------------------
    groups = defaultdict(list)
    for sid in ids:
        groups[find(sid)].append(sid)

    # order groups by their lowest id; label G01, G02, ...
    ordered = sorted(groups.values(), key=lambda g: int(min(g)))
    label = {id_: f"G{i + 1:02d}" for i, g in enumerate(ordered) for id_ in g}

    # --- write teams.csv --------------------------------------------------
    with open(TEAMS, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["group_id", "practical_group", "member_ids", "member_names", "repo_basename", "size", "edge_reasons"])
        for i, g in enumerate(ordered):
            names = [ev[sid]["name"] for sid in g]
            base = next((snap[sid]["basename"] for sid in g if snap[sid]["basename"]), "")
            prac = snap[g[0]]["practical"]
            g_edges = sorted(
                {rr for (a, b), rrs in reasons.items() if a in g and b in g for rr in rrs}
            )
            w.writerow([f"G{i + 1:02d}", prac, ";".join(g), ";".join(names), base or "", len(g), "; ".join(g_edges)])

    # --- add group_id column to evidence.csv --------------------------------
    cols = list(ev[next(iter(ev))].keys())
    if "group_id" not in cols:
        cols.append("group_id")
    with open(EVIDENCE, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in ev.values():
            r = dict(r)
            r["group_id"] = label[r["id"]]
            w.writerow(r)

    # --- summary -----------------------------------------------------------
    singles = sorted((g for g in ordered if len(g) == 1), key=lambda g: int(g[0]))
    print(f"students: {len(ids)}  teams: {len(ordered)}")
    sizes = defaultdict(int)
    for g in ordered:
        sizes[len(g)] += 1
    print(f"team sizes: {dict(sorted(sizes.items()))}")
    print(f"singletons: {len(singles)} -> {[s for s in singles]}")
    connected = {x for (a, b, _) in edges for x in (a, b)}
    isolated = [s for s in ids if s not in connected]
    print(f"students with no edges at all: {len(isolated)} -> {isolated}")
    noprac = sorted((s for s in ids if not snap[s]["practical"]), key=lambda s: int(s))
    print(f"students without a practical group: {len(noprac)} -> {noprac}")
    cross = [g for g in ordered if len({snap[s]["practical"] for s in g}) > 1]
    print(f"teams spanning multiple practicals: {len(cross)}")
    print("wrote teams.csv and added group_id to evidence.csv")


if __name__ == "__main__":
    main()