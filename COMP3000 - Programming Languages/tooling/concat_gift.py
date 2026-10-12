#!/usr/bin/env python3
"""Concatenate generated .gift files, keeping a single venue.

Reads build/<topic>/<topic>.gift (written by tooling/v2.py), keeps only the
questions belonging to one venue, and writes them to a single file with a
rewritten $CATEGORY. The category is the prefix plus the topic from the
source category, so each question keeps its week:

    $CATEGORY: 2026/Exam/5_representing

  python3 tooling/concat_gift.py --venue Exam
  python3 tooling/concat_gift.py --venue "Past Exams" --output build/past.gift

Generated files only - this never reads src/ and never runs a build.
"""
import argparse
import glob
import os
import re
import sys

# v2.py normalises venue names this way before writing them into $CATEGORY,
# so the incoming --venue has to go through the same mangling or "Past Exams"
# will never match the "PastExams" sitting in the file.
def normalise(name):
    return re.sub(r"<.*>", "", re.sub(r"[^a-zA-Z0-9_]", "", name)).strip()


def natural_key(name):
    # Tagged tuples: the tagged int/str mix would TypeError in a plain sort key.
    return [(0, int(p)) if p.isdigit() else (1, p) for p in re.split(r"(\d+)", name)]


def split_blocks(text):
    blocks = [b for b in re.split(r"(?m)^(?=\$CATEGORY:)", text) if b.strip()]
    good = []
    for block in blocks:
        first, _, rest = block.partition("\n")
        if not first.startswith("$CATEGORY:"):
            raise ValueError(f"block does not start with $CATEGORY: {first[:60]!r}")
        if "::" not in rest:
            raise ValueError(f"block has no question header: {first[:60]!r}")
        if "$CATEGORY:" in rest:
            raise ValueError(f"$CATEGORY inside question body: {first[:60]!r}")
        good.append((first, rest))
    return good


def question_name(body):
    m = re.match(r"\s*::(.*?)::", body)
    return m.group(1) if m else None


def main():
    parser = argparse.ArgumentParser(
        description="Concatenate generated .gift files, keeping a single venue."
    )
    parser.add_argument("--venue", required=True, help="venue to keep, e.g. Exam")
    parser.add_argument(
        "--category",
        help="category prefix, topic is appended (default: 2026/<venue>)",
    )
    parser.add_argument(
        "--output",
        help="output path (default: build/<venue lowercased>.gift)",
    )
    parser.add_argument(
        "--glob",
        default="build/*/*.gift",
        help="input files (default: build/*/*.gift)",
    )
    args = parser.parse_args()

    venue = normalise(args.venue)
    if not venue:
        sys.exit(f"error: --venue {args.venue!r} normalises to nothing")

    category = args.category if args.category else f"2026/{venue}"
    output = args.output if args.output else f"build/{venue.lower()}.gift"

    paths = [p for p in glob.glob(args.glob) if os.path.abspath(p) != os.path.abspath(output)]
    if not paths:
        sys.exit(f"error: no files match {args.glob!r} - run tooling/v2.py first")

    # Natural topic order, not glob order.
    paths.sort(key=lambda p: natural_key(os.path.basename(os.path.dirname(p))))

    kept = []
    skipped_empty = []
    available = {}
    for path in paths:
        topic = os.path.basename(os.path.dirname(path))
        try:
            text = open(path, encoding="utf-8").read()
        except OSError as exc:
            sys.exit(f"error: cannot read {path}: {exc}")
        if not text.strip():
            skipped_empty.append(topic)
            continue
        blocks = split_blocks(text)
        for block_head, body in blocks:
            cat = block_head[len("$CATEGORY:"):].strip()
            cat_venue = cat.rsplit("/", 1)[-1] if cat else ""
            # Take the topic from the source category, not the directory name -
            # v2.py writes clean_topic here but opens the file with the raw
            # name, so they only match while topic names stay alphanumeric.
            cat_topic = cat.split("/", 1)[0] if "/" in cat else topic
            available[cat_venue] = available.get(cat_venue, 0) + 1
            if cat_venue == venue:
                kept.append((topic, f"$CATEGORY: {category}/{cat_topic}", body.rstrip("\n")))

    if not available:
        sys.exit(
            "error: no $CATEGORY lines found in any input - "
            "the files look empty or were written by an older tool."
        )

    if not kept:
        listing = ", ".join(f"{v} ({n})" for v, n in sorted(available.items()))
        sys.exit(
            f"error: no questions in venue {venue!r}. Available venues: {listing}\n"
            f"       (if this venue should exist, the build is stale - rerun tooling/v2.py)"
        )

    names = [question_name(body) for _, _, body in kept]
    dupes = sorted({n for n in names if n and names.count(n) > 1})
    if dupes:
        print(f"warning: duplicate question names (Moodle may complain): {', '.join(dupes)}", file=sys.stderr)

    # Join with a blank line; each block already carries its own trailing newlines.
    out = "\n\n".join(f"{head}\n{body}" for _, head, body in kept) + "\n"

    parent = os.path.dirname(output)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output, "w", encoding="utf-8") as fh:
        fh.write(out)

    per_topic = {}
    for topic, _, _ in kept:
        per_topic[topic] = per_topic.get(topic, 0) + 1

    print(f"venue {venue!r} -> {output}")
    print(f"  category: {category}/<topic>")
    for topic, count in per_topic.items():
        print(f"    {topic:26} {count}")
    print(f"  questions: {len(kept)}")
    if skipped_empty:
        print(f"  empty files skipped: {', '.join(skipped_empty)}")


if __name__ == "__main__":
    main()
