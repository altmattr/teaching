# Repeating the Submission 1 marking process

This file records how the marking spreadsheet for week 7 "Submission 1" was
produced, so the process can be rerun (for late submissions, re-marks, or next
semester) and so you can add guidance as you see fit.

## Layout

```
2026/submission 1/
  presenters.csv          roster: First name, Last name, ID number, Email address, Presented
  submissions/            one folder per student: <ID>-<Name>_<id>_assignsubmission_file/
  extract_submissions.py  the evidence script (rerunnable)
  evidence.csv            machine facts, one row per student (script output)
  marks.csv               draft band scores + notes, one row per student (my output)
  analysis.md             week-by-week theme analysis of section 4 answers
  repeat.md               this file
```

As of the full run, the `submissions/` directory holds all 207 folders (the set
grew after the first batch). Everything is done with paths relative to
`2026/submission 1/`.

## Step 1: extract evidence

Run:

```bash
python3 extract_submissions.py
```

from `2026/submission 1/`. This produces `evidence.csv` with one row per
student and the following columns:

`id`, `name`, `email`, `presented`, `worksheet_file`, `worksheet_type`,
`design_file`, `logbook_file`, `other_files`, `repo_url`, `repo_status`,
`branch_count`, `filled_sections`, `gitlog_lines`, `logbook_entries`,
`missing_files`.

What the script does, per student folder:

- reads `presenters.csv` column E; the `presented` flag is `yes` when the cell
  is `yes`/`1`/`true`/`y`, otherwise `no`.
- classifies files by name plus content sniffing. A `.md` is normally the
  worksheet unless its name clearly says log. Design files are usually
  `uml`/`design`/`diagram`/`draw` PDFs or images. Logbooks match `log`/
  `logbook`/`logs` and stay `.md` when the name says so.
- extracts text from `.md` directly, `.docx` via python-docx, `.pdf` via
  pymupdf, `.odt` from the embedded `content.xml`.
- works out which worksheet sections (1.1 to 5.3) are filled, and how long each
  answer is, in `filled_sections` (e.g. `1.1=656,1.2=259`).
- counts git log lines pasted under section 1.1 (`gitlog_lines`) and date /
  week markers in the logbook (`logbook_entries`).
- checks the GitHub URL with `git ls-remote --heads`, giving `repo_status` of
  `reachable` (plus `branch_count`), `private`, `dead`, `no_url` or `timeout`.

Two important behaviours to remember:

1. **Inner zips are unzipped.** Students were told not to zip their three
   files, but some did anyway (e.g. Joshua Mangan 49168312 submitted one zip).
   The script mirrors each folder into a temp dir, expands any `.zip` found,
   and flattens one level of subdirectory, so the classifier sees the files
   even inside a zip.
2. **Missing files are real findings.** If a student genuinely only submitted
   a worksheet (no design, no logbook), the `missing_files` column records it
   and the corresponding rubric items are scored accordingly.

## Step 2: dump the texts for human/LLM review

The evidence script does not save file texts. To review and mark you need the
raw text. `dump_all.py` (run once, in /tmp/opencode) imports the script's own
`classify`/`read_text` and writes, for every submission folder:

- `/tmp/opencode/ws1/<id>_<Name>.txt`    worksheet text (sections 1-5)
- `/tmp/opencode/ws1/<id>_design.txt`    design text or "(no extractable text)"
- `/tmp/opencode/ws1/<id>_log.txt`       logbook text or "(no extractable text)"

Stale dumps must be removed when the submissions folder changes: a student who
had a file restored from the zip in an earlier batch may no longer have it in a
later download, and the old dump would be scored by mistake.

## Step 3: analyse section 4 (what taught the most)

`analysis.md` summarises the section 4 answers ("Which week's activity taught
you the most?") across the full set of 207. A keyword scan attributes each
answer to a week and a topic; blanks and vague replies are counted separately.
Method: grep each worksheet dump for "taught ... the most", take a 500-char
window around it, pull the first `week N` mention and a topic keyword. The
2026 pattern: week 6 (exceptions) leads, then week 4 (inheritance), week 5
(generics), week 7 (showcase); error handling is the dominant theme overall.

## Step 4: draft the marks

`marks.csv` has one row per submitted student with the five rubric items as
`0 / 60 / 72 / 84 / 100`:

`version_control`, `program_design`, `generics_exceptions`,
`uniqueness_creativity`, `log_book`, plus `total` (left blank for you) and
`notes`.

The rubric comes from `project/task.tex` (the week 7 submission table). In
short:

- **version control**: no/dead/team repo link collapses to 0-60; a working
  public repo reaches 60; regular commits 72; meaningful discrete commits you
  can explain 84; branches/PRs/collaborative workflow 100. A pasted git log in
  the worksheet can rescue an otherwise unverifiable repo.
- **program design**: none 0; basic class sketch 60; classes, fields and
  relationships 72; appropriate inheritance 84; design accurate to the code 100.
- **generics and exceptions**: neither used 0; basic use of both 60; both
  appropriate and justified 72; well-integrated with written explanation 84;
  thoughtful use or justified avoidance 100.
- **uniqueness and creativity**: direct copy of class work 0; minor mods 60;
  some mods 72; substantial improvements 84; unexpected/advanced features 100.
  Presented students (evidence `presented=yes`) get 100 regardless.
- **log book**: none 0; entries for each activity 60; most signed/timely 72;
  reflection linking activities to the project 84; insight across multiple
  weeks 100.

To draft the marks I sent the worksheet/design/logbook text dumps plus the
evidence rows to parallel LLM agents, each instructed on the rubric bands (only
{0,60,72,84,100}), the presented rule, and a strict output format. The agent
rows were consolidated into `marks.csv` and machine-checked:

- 207 rows, all IDs join with `evidence.csv`;
- every score in a valid band; `total` empty; every email present;
- presented=yes implies `uniqueness_creativity = 100` (spot fix three missed);
- blank-text image PDF logbooks scored 0 (or 60 where a real reflection was
  found); notes say when a logbook could not be verified.

## Presenters

The presenter bonus for uniqueness and creativity is driven by
`presenters.csv` column E. After the full downloads it is filled in (yes/no for
every row); 87 submitters are marked yes, and all of them carry a 100 in
`uniqueness_creativity`. If a worksheet itself also says "presented in class"
that is captured by the note as well.

## Things that surprised us (worth keeping in mind)

- The first batch of 112 folders was replaced by the full download of 207; a
  few files that existed in the old folders (e.g. a worksheet for Seokmin Cho
  and one for Nomikos Reisis) are absent from the new set. The dumps were
  regenerated from scratch; do not trust old dump text for changed folders.
- A handful of worksheet files are 0-byte (e.g. Sansarin Sermsoontornsil
  48827835, Chris Zhou 47777796) or missing entirely (Spenser Guo 47785721,
  Aarya Alhad Tamhane 48766380, Seokmin Cho 48925381, Nomikos Reisis 49066315,
  Mitchell Chiu 49147641). Those students score 0 for any missing item.
- Several logbook PDFs are image-only scans with no text layer (Anton
  Chistiakov 42870691 28 pages, Brian Cheng 47357681, Tengis Chadraabal
  48977489, William Brown 49047418, Harrison Mcluckie 49154788). They were
  scored 0 unless a real reflection could be found; decide whether you want a
  manual look before finalising.
- Compiled counts for the full 207: repo_status reachable 182 / private 14 /
  no_url 11; worksheet types md 185 / docx 2 / pdf 14 / noext 1; 23 folders
  missing at least one required file; 2 students with no worksheet have only
  design+logbook.
- `48815861-Callum Holley` gave no repo URL at all (version control 0).
- Private repos were scored from whatever the worksheet pasted (git logs, PR
  links); with no paste they are 0. Decide whether that is the policy you want
  and adjust `marks.csv` accordingly before filling in totals.

## For the marker (you)

- The `total` column in `marks.csv` is yours.
- Check the `notes` column before trusting any score; every band decision is
  summarised there.
- Rerun `extract_submissions.py` before adding late submissions so the roster
  and repo checks stay current, then re-dump the new folders and carry the new
  rows over into `marks.csv`.