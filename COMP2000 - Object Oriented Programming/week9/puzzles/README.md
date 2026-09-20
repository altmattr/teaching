# COMP2000 Week 9: Code golf puzzles

Six programming puzzles.  In each one, transform a list of words.  The stubs
already contain a correct answer written with plain loops: it is deliberately
long.  Golf it down to as few characters as you can.  The golfer with the
fewest characters wins.

## The rule

- The method signature and the imports are fixed.  Do not change them.
- Only the body of the method counts: every character between the braces,
  spaces and newlines included.  The `return` keyword and the closing
  semicolon count.
- Shorter is better.  A correct long answer beats an incorrect short one, but
  among correct answers, fewest characters wins.
- Target Java 11 (the devcontainer).

## How to play

1. Open each `PuzzleN.java`.  The body is a working loop solution; shorten it
   while keeping the tests green.  The starter length is written in a comment
   above each method.
2. Run the tests to check your answers:

   ```bash
   ./run_tests.sh
   ```

3. Count your characters.  For example:

   ```java
   words.removeIf(w -> w.length() < 3); return words;
   ```

   That's 50 characters, spaces included.  Can you do better?

## The puzzles

| Puzzle | Starter | Goal |
| ------ | ------- | ---- |
| `Puzzle1.sortByLength` | 216 | sort the words by length, shortest first |
| `Puzzle2.sortIgnoreCase` | 201 | sort the words ignoring case |
| `Puzzle3.dropShort` | 169 | drop the words shorter than 3 letters |
| `Puzzle4.upperAll` | 140 | shout every word |
| `Puzzle5.normalize` | 471 | shout, drop short words, then sort by length |
| `Puzzle6.reversed` | 166 | reverse every word |

The starter count is the number of characters in the body exactly as given,
spaces and newlines included.  Beat it.

Everything you need is here: the stubs, the JUnit tests, and the two JARs in
`lib/`.