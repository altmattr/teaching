# Week 9 code golf: teacher reference

Reference bodies for each puzzle.  These are starting points, not champions.
Counted characters = every character of the method body exactly as written,
spaces and newlines included.  The method signature and the imports are free
(they are identical for every team), and the count comment sits outside the
body.

## Starter bodies (in the stubs)

| Puzzle | Starter count |
| ------ | ------------- |
| `Puzzle1.sortByLength` | 216 |
| `Puzzle2.sortIgnoreCase` | 201 |
| `Puzzle3.dropShort` | 169 |
| `Puzzle4.upperAll` | 140 |
| `Puzzle5.normalize` | 471 |
| `Puzzle6.reversed` | 166 |

The loops are deliberately verbose so the lambda win is obvious.  Every
puzzle below collapses the loop into a single functional call on the list,
using only lambdas, method references, and the collection methods
`sort`/`removeIf`/`replaceAll` from the week 9 lecture.

## Reference lambda bodies

### Puzzle 1: sortByLength

```java
words.sort(Comparator.comparingInt(String::length)); return words;
```

Count: 66.  Win over starter: 150.

### Puzzle 2: sortIgnoreCase

```java
words.sort((a, b) -> a.compareToIgnoreCase(b)); return words;
```

Count: 61.  Win over starter: 140.

### Puzzle 3: dropShort

```java
words.removeIf(w -> w.length() < 3); return words;
```

Count: 50.  Win over starter: 119.

### Puzzle 4: upperAll

```java
words.replaceAll(String::toUpperCase); return words;
```

Count: 52.  Win over starter: 88.

### Puzzle 5: normalize

```java
words.replaceAll(String::toUpperCase); words.removeIf(w -> w.length() < 3); words.sort(Comparator.comparingInt(String::length)); return words;
```

Count: 142.  Win over starter: 329.

### Puzzle 6: reversed

```java
words.replaceAll(w -> new StringBuilder(w).reverse().toString()); return words;
```

Count: 79.  Win over starter: 87.

All counts are for the body as written on one line, spaces included but no
leading space or newline.  A student who reformats to a single line can match
these exactly; any extra indentation adds to their total.

## Notes for running the class

- `run_tests.sh` compiles and runs all six tests.  Point teams at it and to
  `README.md`.
- The methods mutate their argument and return it, so the reference bodies
  sort/filter/transform the list in place.  This matches the `sort`,
  `removeIf`, and `replaceAll` style shown in the lecture, which are all
  in-place.
- During reporting, project each team's body and count characters.  The
  simplest way to count a body fairly is to have each team report the
  character count their editor shows for the selected body text, then
  spot-check a few with `wc -c`.
- The `lib/` JARs are JUnit 4.13.2 and hamcrest 1.3, matching the COMP2010
  copies.  Java 11 is the target (devcontainer).
- If a team's answer passes tests but uses a loop instead of a lambda, accept
  it if shorter: the activity rewards the fewest characters, whatever the
  technique.  The "lambda tricks learned from other teams" reporting prompt
  still applies.
- These puzzles deliberately avoid the Streams API (that is week 10 material).
  The wins come purely from `List.sort`, `removeIf`, `replaceAll`,
  `Comparator` methods, method references, and lambda expressions.