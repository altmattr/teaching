# Marking Guidance for the Agent Pass (Submission 1)

Lessons learnt from comparing the agent's marks in `marks.csv` against the
human markers' marks in `marking.xlsx`. The biggest disagreements cluster into
a small set of repeatable mistakes. Fix these and most of the gap closes.

## 1. Enforce the minimum requirement

A working graphical simulation that compiles and runs using only standard JRE
classes is the floor for this assignment. If that isn't verifiable, every
criterion except the log book scores 0. Evidence like a pasted git log, a
worksheet description, or a presentation is **not** proof of working code.

Before scoring anything, confirm you can actually see the code:

1. Open the repo URL if one is given.
2. If the repo is private or unreachable and no code was included in the
   submission, treat the code criteria as 0.
3. If the repo is reachable but the code clearly does not compile (check the
   marker's staff notes), treat the code criteria as 0.

Five of the twelve worst mismatches were exactly this: the agent scored the
worksheet and presentation evidence, the markers zeroed the code criteria.
All five of those students were marked by AC, who applies the floor
consistently. Match that behaviour.

## 2. Trust the repository over the worksheet

The worksheet tells you what the student *claims*; the repo tells you what they
*built*. Where they disagree, the repo wins.

- Ali Abdo: worksheet generics examples were partly incorrect and referenced
  code that didn't exist. The agent scored the worksheet; the marker penalised.
- Callum Holley and Alexander Batchelor: written answers looked reasonable but
  didn't hold up against the actual code.

Check that named generics classes and exceptions actually exist in the source
before crediting them, and that the design/UML matches the code you can see.

## 3. A missing file is not a missing answer

Do not zero a criterion just because the expected file is absent, if the
content clearly exists elsewhere.

- Hamza Mughal: the design *file* was missing, so the agent gave program design
  0. The marker found a strong design elsewhere in the submission and scored it
  100. Big, avoidable gap.

Conversely, if neither the file nor an equivalent description exists anywhere,
score low (see Spenser Guo and the others with empty worksheets).

## 4. Presentations are not proof of working code

A student presenting earns them the creativity/uniqueness credit, but it does
not fix an unverifiable repo. Do not let "presented: yes" push code criteria
up when the code can't be seen or doesn't compile.

- Mitchell Chiu and Nomikos Reisis both presented and both got creativity 100 in
  the agent pass, but scored 0 on the code criteria from the markers.

## 5. Read the real git history, not the pasted extract

- Shoumik Ghosh: the agent saw a short pasted git log (2 lines) and scored
  version control 60. The actual repo had 30 commits with a full branch/PR
  workflow; the marker scored 100. When a repo is reachable, inspect it directly
  instead of trusting a 2-line summary.
- Utkarsh Ratti: the reverse trap. The final repo looks busy, but nearly all
  commits came after the extension and were submitted late. Mark what existed
  at the due date, and check the marker's staff notes for this kind of context.

## 6. Watch for unreviewable evidence

- Log book: no submitted file, or a file with no extractable text, is not
  verifiable. Score from what can actually be read (worksheet description at
  best), and match the marker's habit of zeroing a completely missing log book.
- Shared work: identical UML diagrams across supposedly independent students
  (Spenser Guo's "SG, FA and BF submitted the same diagram") and byte-identical
  design sections in shared repos should flag for staff, not be scored as-is.

## 7. Try to see what the marker sees

Some mismatches were agent-side reading failures, not student weaknesses:

- Sansarin Sermsoontornsil: the submission looked empty (0-byte download) but
  worked fine direct from iLearn. Before scoring zeros, check whether the
  evidence is genuinely absent rather than merely hard to retrieve.

## Summary rules

| Do | Don't |
| --- | --- |
| Verify the repo opens and the code compiles before scoring code criteria | Score a worksheet or presentation as evidence of working code |
| Check named generics/exceptions actually exist in the source | Trust claims about the code without checking the code |
| Look for the answer across the whole submission before zeroing a criterion | Zero a criterion on a missing file alone |
| Inspect the actual git history when the repo is reachable | Judge commit quality from a 2-line pasted log |
| Watch for late-after-extension commits and mark the due-date state | Mark the final repo state as if it were the due-date state |
| Flag shared diagrams and identical sections for staff | Score shared/copied evidence as if it were individual work |