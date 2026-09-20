# What Taught the Most? A Look Through the Worksheets

This version covers the full set of 207 submissions. I read every student who
answered the question in section 4, "Which week's activity taught you the
most?", and pulled out the week (and the topic) each one credited. That's 203
usable worksheets (the other four had no extractable worksheet at all); of
those, 170 pointed at a specific week and 33 were vague or blank.

## Week 6 wins, and it's not close

Almost a quarter of the class (48 answers) pointed at week 6. That was the week
the class got hands-on with exceptions, specifically the barcode exercise, and
it clearly landed. Time and again students wrote some version of: "I finally
understood how errors move up the call stack." The activity made propagation
visible, showed where `throw` and `throws` belong, and clicked for people who
had been pasting `try/catch` blocks without really knowing what they did.

Why does this matter? Exception handling is the one topic that people said went
from scary to obvious in a single session. That's a textbook sign of a good
activity.

## The runner-up weeks

| Week | Topic | Students citing it |
|------|-------|----------|
| 6  | exceptions (barcode exercise) | 48 |
| 4  | inheritance and overloading | 44 |
| 5  | generics and type erasure | 33 |
| 7  | project showcase, seeing other teams' work | 17 |
| 3  | UML and class design | 12 |
| 2  | git and version control | 11 |
| 1  | team setup | 5 |
| ?  | vague or no clear week given | 33 |

The first three weeks are on the leaderboard for different reasons.

- **Week 4 (inheritance):** the design week. Students talked about moving from
  abstract ideas to actually planning class hierarchies, splitting shared
  behaviour into a superclass, and using `@Override`. Several said it directly
  shaped their project code. Inheritance is the single most-named topic up
  there (29 of the 44).
- **Week 5 (generics):** the "break it on purpose" exercise. The `Container<T>`
  task, where you try to force a runtime error without adding explicit casts,
  made type erasure click. A few students even chased it all week after class.
- **Week 6 (exceptions):** the outright winner on its own, and the barcode
  activity is the named highlight almost every time.
- **Week 7 (showcase):** the surprise of the full set. It jumped from 7 to 17
  mentions and the answers are split between presenting ("I had to explain my
  own code") and watching other teams ("seeing a peer's custom exceptions guard
  against logical errors"). Week 7 reads as a real teaching moment, not just an
  admin showcase.
- **Week 2 (git):** the clear winner for anyone who hadn't used command-line git
  before. They said it paid off all semester in how their teams worked.
- **Week 3 (UML):** a stepping stone into the project for several students,
  even if they didn't frame it as their biggest lesson.

## One theme runs under everything: errors

If you squint at the topics rather than the weeks, a pattern shows. Exceptions
dominated (93 mentions), but that's partly because week 5's generics exercise
was really an exercise in *understanding runtime errors too*. To debug your
deliberately broken `Container<T>` you had to read the call stack. So weeks 5
and 6 blur together for quite a few students, and both taught error handling in
a practical, memorable way. Combined, week 5 plus week 6 answer for 81 of the
170 week-specific replies, and nearly all of them are about error handling
rather than syntax.

## Caveats before you over-read this

- 33 answers were vague ("all weeks were equally valuable") or blank; each is
  counted once under "no clear week", not ignored.
- A further 4 submissions have no extractable worksheet at all (either the file
  is missing or it's a 0-byte `worksheet-7.md`).
- The counts come from scanning each answer's text for a week number and a
  topic keyword. It's honest but not surgical. A student writing "until week 6
  I didn't get exceptions" is counted as crediting week 6, which is fair, but
  the odd sentence will have escaped the net.

## What to take away

Week 6's barcode activity is the clear high point: make error handling the
centre of the week and students leave genuinely understanding it. Week 4
(inheritance) is a close second and is the one that most directly feeds the
project design. The full set has also confirmed week 7's showcase earns its
place: seeing other teams' implementations is a genuine teaching moment, not a
formality. If you had to keep just one activity for next term, the week 6
exception traversal one is still the keeper.