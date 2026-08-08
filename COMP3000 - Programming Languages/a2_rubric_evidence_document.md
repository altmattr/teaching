# A2 Rubric Evidence Document

This document is part of your second submission.  Complete it and include it in your submission zip, alongside your source code.  It explains how the submission is marked and what you need to tell your marker.

## How it works

Here you will explain to your marker how you have achieved each rubric item.  Include this completed document in your submission zip, alongside your source code.  Each rubric item has one section where you explain yourself and an attached video giving an example of what that rubric item is looking for.

Your submission will be marked out of **16** with marks for:

1. An expression language: example program with an expression, output at least one flow (2)
2. A more complex expression language: model multiple days, output on each day (2)
3. Dam syntax: syntax and parsing only (2)
4. Dam evaluation: simple dams affect output sensibly (2)
5. Interesting dam algorithms: dam can do a conditional, explain design and implementation (2)
6. Log-book (2)
7. Language quality (2)
8. Uniqueness and creativity (2)

## 1. An expression language: example program with an expression, output at least one flow (2)

- 2 Example program has an expression and outputs at least one flow.
- -2 Example program missing.
- -1 Example program has no expression.
- -1 Lacking output of at least one flow.
- -0.5 Some more explanation of the language could have improved this answer.
- -0.5 Rainfall does not appear to be user definable.
- -0.5 River catchment size does not appear to be user definable.

Your language must be able to interpret an expression language which describes simple river flows.  The interpreter must output something when it is finished indicating at least one of the flows in the system.  We recommend outputting all named flows, but you could have a special output expression in which case you will output just that expression.

Video: https://ilearn.mq.edu.au/pluginfile.php/9814546/question/questiontext/16519095/1/122955576/rubric%201.mov

### Your explanation

_Write your explanation here; add as much space as you need and point to the relevant example program in your zip._

## 2. A more complex expression language: model multiple days, output on each day (2)

- 2 Can model multiple days and output each day.
- -1 Cannot model multiple days.
- -1 Does not output results for each day.
- -0.5 Models a limited/fixed number of days (10).
- -0.5 Calculations are instantaneous and don't predict based on water flows from previous days.

You will get these marks if your expression language can model the flow over multiple days and the output of your interpreter shows the predicted flows on all those days.  As with the last item, you may output just one flow, or all named flows, or whatever makes most sense for your language.

Video: https://ilearn.mq.edu.au/pluginfile.php/9814546/question/questiontext/16519095/2/122955577/rubric%202.mov

### Your explanation

_Write your explanation here; add as much space as you need and point to the relevant example program in your zip._

## 3. Dam syntax: syntax and parsing only (2)

- 2 Syntax exists and parsing works as expected.
- -1 Dams are not part of the language.
- -1 Dam does not have syntax.
- -1 Dam example does not parse.
- -1 No grammar, or no grammar for dams.
- -0.5 Grammar isn't a full grammar for the language.
- -0.5 Minor mismatch between grammar and examples.
- -0.5 Full grammar is hard to read, unclear if it is correct.
- -1 Major mismatch between grammar and examples.

Your language has a syntax to support dams.  Dams don't always let all or none of the flow through, they run some "algorithm" to decide how much flow to let through.  You will get this grade if you have example programs demonstrating your dam syntax and your parser can successfully parse those programs.  Your marker may write their own program so please include a full grammar here.

Video: https://ilearn.mq.edu.au/pluginfile.php/9814546/question/questiontext/16519095/3/122955578/rubric%203.mov

### Your explanation

_Write your explanation here; add as much space as you need and point to the relevant example program in your zip._

## 4. Dam evaluation: simple dams affect output sensibly (2)

- 2 Outputs for no-flow, half-flow, and full-flow all work as expected.
- -0.5 No check occurs for whether release fraction > 1.
- -1 No user-settable parameters for dams, so half-flow or no-flow dams can't be specified.
- -1 Full-flow dam changes output, when it should not.
- -1 Half-flow dam doesn't halve the flow, when it should.
- -1 No-flow dam seems to still allow some water through, when it should not.

The interpreter can run the dam's algorithm accurately and downstream river flows reflect its behaviour.

Video: https://ilearn.mq.edu.au/pluginfile.php/9814546/question/questiontext/16519095/4/122955579/rubric%204.mov

### Your explanation

_Write your explanation here; add as much space as you need and point to the relevant example program in your zip._

## 5. Interesting dam algorithms: dam can do a conditional, explain design and implementation (2)

- 1 Design and implementation both explained.
- 1 Dam syntax has the ability to express a user-defined conditional.
- -1 Dam algorithm is hard-coded, not programmable via the domain-specific language, although parameters can be modified.
- -1 Dam behaviour seems hard-coded, rather than programmable via the domain-specific language.
- -1 Dam syntax has no ability to express a user-defined conditional.
- -0.5 No explanation of dam design.
- -0.5 No explanation of dam implementation.
- -0.5 Implementation explained but not design decisions.
- -0.5 Design decisions explained but implementation not explained.
- -1 Scant/lacking explanation of dam design and implementation.

The output from a dam can depend on at least two of the following:

- the flow into the dam
- today's rain
- the dam level

To get these marks you must explain the language design decisions and implementation steps you took to achieve this.  Your marker might try to write their own programs so make sure you explain the system well.

Video: https://ilearn.mq.edu.au/pluginfile.php/9814546/question/questiontext/16519095/5/122955580/rubric%205.mov

### Your explanation

_Write your explanation here; add as much space as you need and point to the relevant example program in your zip._

## 6. Log-book (2)

- 2 Complete and timely entries throughout the semester.
- 1 Some entries, but inconsistent across the semester.
- 0 No logbook submitted or no entries.

Log-book entries showing consistent workshop engagement throughout the semester.  No logbook = 0 marks.  Complete and timely entries = full marks.

## 7. Language quality (2)

- 2 Nothing bad or weird in how the language is defined, and the design is clearly well thought out.
- 1 Nothing bad or weird in how the language is defined, but the design is unremarkable.
- 0 Something bad or weird in how the language is defined.

Your marker will give low, medium, or high marks for the quality of your language.  You can explain here the decisions you made to help convince them of the quality of your language.

### Your explanation

_Write your explanation here; add as much space as you need and point to the relevant example program in your zip._

Video: https://ilearn.mq.edu.au/pluginfile.php/9814546/question/questiontext/16519095/6/122955581/rubric%206%20and%207.mov

## 8. Uniqueness and creativity (2)

- 2 Clearly unique and creative.
- 1 Goes beyond the exemplar code.
- 0 Does not go beyond the exemplar code, or is essentially the same as Lox.

Your marker will give zero, one, or two marks for how far your submission goes beyond class work and the example solutions.  You may use this space to explain what is unique and creative about your language.  You can present your work in the week 13 class to guarantee full marks for this rubric item.

### Your explanation

_Write your explanation here; add as much space as you need and point to the relevant example program in your zip._
