---
title: "COMP3000 Week 2"
subtitle: "Little Languages + The Pipeline"
author: "COMP3000 Programming Languages"
date: ""
header-includes:
  - \input{slides/preamble_beamer.tex}
---

## Last week in 60 seconds

- A **domain-specific language** (DSL) is a little language built for one job
- Examples: SQL, regex, LaTeX, Make, CSS, shell
- When you can, **reuse an existing one** instead of rolling your own
- The big idea: you will **build your own** little language for water flows
- The pipeline, teased: **Scanner $\rightarrow$ Parser $\rightarrow$ Interpreter**

::: notes
Recap from Week 1. Today we turn the three-word pipeline teaser into the full picture, and we use regex as a worked example of a little language.
:::

## From teaser to full picture

- Last week: just the names -- Scanner, Parser, Interpreter
- The real pipeline has more stages than that
- Not every implementation walks the whole route
- Today: the **complete map**, then where our implementation stops

::: notes
Set up the arc of the lecture: the full mountain, then why "compiler or interpreter?" is the wrong question, then regex as a DSL that shows every idea in miniature.
:::

## Little languages, again

- Ch 1: "For every successful general-purpose language, there are a thousand successful niche ones"
- They are **pidgins tailor-built to a specific task**
- Small on purpose: restricted syntax, restricted features
- They lean on the machinery around them (their "host") for the hard parts

::: notes
The definition again, but deeper. A DSL deliberately gives up generality to speak precisely about one domain. Think of sed, or the command language in a game: it does one job well and leans on the surrounding environment.
:::

## Reuse... or roll your own?

- "When you can, good to reuse an existing one instead of rolling your own"
- Why: documentation, debuggers, editor support, syntax highlighting
- "Once you factor in all the other trappings, doing it yourself becomes a tall order"
- But when nothing fits your domain, building one is the right call -- that's this unit

::: notes
The trade-off from ch 1. Our domain (water flows) has no existing language, so we build one. But the default should always be to reuse.
:::

## The pipeline, in full

\begin{center}
\includegraphics[width=0.85\textwidth]{text/site/image/a-map-of-the-territory/mountain.png}
\end{center}

**Scan $\rightarrow$ Parse $\rightarrow$ Static Analysis $\rightarrow$ Optimise $\rightarrow$ Code Gen $\rightarrow$ VM $\rightarrow$ Runtime**

::: notes
Ch 2's map of the territory. Source text at the bottom, climb to where meaning is clear, descend to something the machine can run. We covered the first two last week; today we name the rest.
:::

## Front end, middle end, back end

- **Front end**: where source text becomes a structured representation
  - scanning and parsing
- **Middle end**: where we reason about the program
  - static analysis and optimisation
- **Back end**: where we produce something runnable
  - code generation, virtual machine, runtime

::: notes
The three traditional regions of a compiler. Our tree-walk interpreter only uses the front end and stops there -- it evaluates the tree directly.
:::

## Static analysis: seeing what the code does

- The parser knows the *syntax*; static analysis works out the *meaning*
- **Binding**: connecting each identifier to the variable or function it refers to
- **Type checking**: rejecting programs that don't make sense (in typed languages)
- Ch 2: "get a high-level view of what the code is doing"
- In Lox: a **resolver** pass walks the tree before we evaluate it

::: notes
Static analysis runs without executing anything. It's where a lot of errors get caught early. Our Lox interpreter adds this pass in the book's second part.
:::

## Optimisation: doing less work

- If an expression always gives the same value, compute it once at build time
- **Constant folding**:

\vspace{0.5em}

`pennyArea = 3.14159 * (0.75 / 2) * (0.75 / 2);`

becomes

`pennyArea = 0.4417860938;`

- "Optimization is a huge part of the programming language business"

::: notes
Constant folding from ch 2. We can do the arithmetic in the compiler and replace the expression with its result. Later the book pairs it with constant propagation.
:::

## Code generation: speaking the machine's language

- The back end converts our representation into runnable code
- **Native code**: instructions for a real chip (x86, ARM)
  - lightning fast, but tied to one architecture, and a lot of work
- **Bytecode**: instructions for a *virtual* machine
  - "a dense, binary encoding of the language's low-level operations"
  - portable across architectures

::: notes
The design decision at the bottom of the mountain. Wirth and Richards produced p-code for a hypothetical machine so one compiler could target many chips.
:::

## Virtual machines and the runtime

- A **VM** emulates a hypothetical chip; it runs the bytecode at runtime
- Slower than native code, but simple and portable
  - "Implement your VM in C, and you can run your language on any platform with a C compiler"
- The **runtime** provides services while a program runs:
  - garbage collection, and tracking object types at runtime

::: notes
Language VMs (like Java's JVM, or Python's) vs system VMs (like VirtualBox). Our second interpreter in this unit is a bytecode VM.
:::

## Where our journey stops

- Our first interpreter is a **tree-walk interpreter**: scan, parse, evaluate
  - no static analysis, no code generation, no VM -- it walks the tree directly
- Later in the unit we add the static-analysis pass
- So we climb part of the mountain, and evaluate from the top

::: notes
Reassure students: we don't build the whole mountain. We take the tree-walk route, and the book's second half adds a bytecode VM. The other stages are context.
:::

## Compilers and interpreters

- "What's the difference?" is like asking the difference between a fruit and a vegetable
- **Fruit** is a *botanical* term; **vegetable** is *culinary*
- Neither implies the negation of the other
- Tomatoes are both; apples are fruit but not vegetables; carrots are vegetables but not fruit

\begin{center}
\includegraphics[width=0.55\textwidth]{text/site/image/a-map-of-the-territory/plants.png}
\end{center}

::: notes
The ch 2 analogy. "Compiled" and "interpreted" are not two sides of a binary -- they are different ways of describing an implementation, and both can apply at once.
:::

## Compiling is an implementation technique

- **Compiling**: translating source to some other, usually lower-level, form
  - bytecode, machine code, or even another high-level language (transpiling)
- A **compiler** translates source but doesn't execute it -- you run the output yourself
- An **interpreter** takes source and executes it directly, "from source"

::: notes
Three crisp definitions from ch 2. These are properties of *implementations*, not of languages.
:::

## It's not about the language

- **CPython**: runs your program from source (an interpreter), and it *has* a compiler -- it parses and compiles to bytecode internally
- **Go**: `go build` compiles and stops; `go run` compiles *then* executes -- it both *is* and *has* a compiler
- So "is Java compiled or interpreted?" is not meaningful
- We can only answer for **particular implementations**

\begin{center}
\includegraphics[width=0.6\textwidth]{text/site/image/a-map-of-the-territory/venn.png}
\end{center}

::: notes
The overlapping region of the Venn diagram: interpreters that compile internally. Our second interpreter lives there too. Most "scripting" languages work this way.
:::

## Regex: a DSL for text

- **Regular expressions** are a little language for pattern matching in text
- Match a pattern against a string, e.g. `\d{4}-\d{2}-\d{2}` matches a date
- Look at its features and it is suspiciously like a general-purpose language:
  - **variables**: capture groups, reused later
  - **loops**: the `*` and `+` quantifiers
  - **conditions**: the `?` operator... sort of

::: notes
Regex is the worked DSL of the lecture. The features list here sets up the completeness discussion at the end.
:::

## Live on regexr.com

- Head to \textbf{regexr.com} and try it yourself
- Try:
  - an exact string, e.g. "my presence"
  - one of two strings, e.g. "my presence" or "my friends"
  - a repeated letter, e.g. repeated p's or g's
  - capture the first word of each character's dialogue

::: notes
Live demo on regexr.com. This mirrors the Week 2 workshop activity, where you do the same exploration and then write up your own example in the FAT.
:::

## What makes a language complete?

- A language is **complete** if it can express all possible computations
- All complete languages have equivalent expressive power
- The **Turing view**: variables, conditions, and loops -- like a Turing machine
- The **Church view**: variables and functions -- like the lambda calculus
- "This dual nature of computing is one of the most fascinating aspects of programming language theory"

::: notes
The completeness test from the workshop. Knowing for sure takes real maths, but these two feature tests are a good approximation.
:::

## Wrap-up and Week 3 prep

- Today's reading: **Chapters 1--2** (re-read if needed)
- **Before next class**: read **Chapter 3** and complete the Week 3 iRAT
- Next week: **Lox** -- the language we build, and its features
- Preview: a Lox program that drives turtle graphics

::: notes
Next week introduces Lox and the first real implementation work. Chapter 3 is short -- the iRAT will draw directly on it.
:::
