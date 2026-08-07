---
title: "COMP3000 Week 1"
subtitle: "Team Based Learning + Domain-Specific Languages"
author: "COMP3000 Programming Languages"
date: ""
header-includes:
  - \input{slides/preamble_beamer.tex}
---

## Welcome to COMP3000

- 13 lectures, 110 minutes each
- Every lecture is followed by a two-hour collaborative workshop
- Today: what the unit is about, how classes run, and the big idea that drives everything
- No preparation needed this week -- but from Week 2 on there is

::: notes
Walk through the shape of the unit before diving into content. Emphasise the lecture-to-workshop rhythm: the lecture introduces, the workshop applies.
:::

## What the unit is about

- You will **design and build your own programming language**
- Not a toy: a language that solves a real problem
- The domain this year: **modelling water flows in river systems**

\begin{center}
\includegraphics[width=0.45\textwidth]{googong.jpg}
\end{center}

*The Googong Dam -- one of the river flows students model.*

::: notes
Show the dam image. This is the hook: languages are usually described as general-purpose tools, but here we build a *little language* for a specific job, the way industry actually uses them.
:::

## Why a language for water flows?

- River managers need to know what rainfall does to river levels over time
- Flood prediction, dam strategies, public safety
- Normally done with simulation software
- We will do it with a **custom language** instead
- No such language exists yet -- you will build it

::: notes
Frame as EPIC: purpose that inspires, impact that matters. The students are filling a real hole.
:::

## How the classes run -- Team Based Learning

- The unit runs on **TBL**: you work in a team for all 13 weeks
- Each week follows a fixed cycle:
  - **iRAT** -- individual multiple-choice quiz (done before class)
  - **tRAT** -- the same quiz, answered with your team
  - **FAT** -- class-wide discussion of the answers
  - **Application Task** -- one hour of team work on the assignment
- Pre-reading every week, starting Week 2

::: notes
iRAT before class; tRAT + FAT + application task in class. Team contracts are made in Week 1.
:::

## Teams matter

- You'll form teams today and stay in them all semester
- The workshops build your assignment *as a team*
- Everyone draws on the shared pool of team work for their own submission
- Teams write a **contract** in Week 1: expectations, and how a member can be excluded
- If you stop showing up, your team can replace you

::: notes
Stress the team contract activity in today's workshop. The logbook is personal, but the work is shared.
:::

## Domain-specific languages -- the big idea

- A **domain-specific language** (DSL) is a language built for one job
- Ch 1 calls them *"little languages"* -- "pidgins tailor-built to a specific task"
- Think application scripting languages, template engines, markup formats, config files
- Contrast with a **general-purpose language** (GPL): Java, C, Python -- built for any job

::: notes
Definition from the textbook: "For every successful general-purpose language, there are a thousand successful niche ones."
:::

## Little languages are everywhere

\includegraphics[width=0.5\textwidth]{text/site/image/introduction/little-languages.png}

- SQL, regex, LaTeX, Make, CSS, shell -- all little languages
- Almost every large software project needs a handful
- When you can, **reuse an existing one** instead of rolling your own

::: notes
"Once you factor in documentation, debuggers, editor support, syntax highlighting, and all the other trappings, doing it yourself becomes a tall order." -- ch 1
:::

## Some well-known DSLs

- **SQL** -- querying relational databases
- **Regular expressions** -- pattern matching in text
- **LaTeX** -- typesetting documents
- **Make** -- describing build dependencies
- **Dream Maker** -- the game *Space Station 13* is built in it
- **strudel.cc** -- making music by writing code in the browser

::: notes
Mention the live regex demo that comes in Week 2. strudel.cc is worth showing live if internet allows.
:::

## Why build a DSL at all?

- When a general-purpose language is **too much**:
  - too verbose for the job
  - too hard for the people who need to write it
- A DSL says *exactly* what the task needs, in the task's own terms
- The classic trade-off from ch 1: reuse an existing one... or build your own when nothing fits

::: notes
Domain experts (here: water engineers) shouldn't need a CS degree to express their problem.
:::

## Languages are great exercise

- Implementing a language is a *real* test of programming skill
- Recursion, trees, graphs, dynamic arrays, hash tables -- all from scratch
- "Rise to it, and you'll come away a stronger programmer"

::: notes
From ch 1 "Languages are great exercise".
:::

## There's no magic

- Languages feel magical -- until you build one
- "There is no magic at all. It's just code, and the people who hack on languages are just people." -- ch 1
- By the end of this unit you'll *be* one of those people

::: notes
The demystifying pitch. A couple of techniques are new, but nothing harder than obstacles already overcome.
:::

## The pipeline -- a teaser

- A language implementation transforms source text step by step
- The three stages we build this semester:

  **Scanner** $\rightarrow$ **Parser** $\rightarrow$ **Interpreter**

- Today, just the names. We build each in turn from Week 4.

::: notes
Ch 2's mountain metaphor: source text at the bottom, climb to where the code's meaning is clear, descend to something the machine can run. Our first interpreter is a *tree-walk* interpreter -- climb partway, then evaluate the tree directly.
:::

## Source text becomes tokens

`var average = (min + max) / 2;`

\vspace{0.5em}

\includegraphics[width=0.8\textwidth]{text/site/image/a-map-of-the-territory/tokens.png}

*The scanner chunks characters into tokens.*

::: notes
Scanning (lexing): the linear stream of characters becomes words/tokens. Whitespace and comments are discarded.
:::

## Tokens become a tree

\includegraphics[width=0.75\textwidth]{text/site/image/a-map-of-the-territory/ast.png}

*The parser builds an abstract syntax tree from the flat token stream.*

::: notes
Parsing gives the syntax a grammar -- the ability to compose larger expressions from smaller parts, mirroring the nested structure of the language.
:::

## The mountain, in full

\includegraphics[width=0.9\textwidth]{text/site/image/a-map-of-the-territory/mountain.png}

- Not every implementation walks the whole mountain
- Our interpreter: **scan, parse, evaluate** -- a tree-walk interpreter
- Later topics (Ch 11) add a static-analysis pass before evaluating

::: notes
Ch 2's map: scanning, parsing, static analysis, optimization, code generation, VM, runtime. We take the tree-walk route this semester.
:::

## Wrap-up and Week 2 prep

- Today's reading: **Chapters 1--2** of *Crafting Interpreters*
- **Before next class**: read those chapters and complete the Week 2 iRAT
- Next week: little languages in more depth, and the *full* pipeline picture
- Reminder: form your team and write your team contract today

::: notes
Next lecture covers the pipeline in full plus regular expressions as a worked DSL. iRAT is done individually before class, every week from now on.
:::
