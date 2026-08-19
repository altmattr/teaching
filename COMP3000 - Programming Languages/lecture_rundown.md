# COMP3000 Lecture Run-Down

13 lectures, 110 minutes each. Timestamps are offset from start.

---

## Week 1 — Team Based Learning + Domain-Specific Languages

Textbook: Chapters 1–2

- (0:00) EPIC / COMP3000 overview: What the unit is about
- (0:25) What is TBL: Structure: iRAT, tRAT, FAT, SSE
- (0:50) What is a domain-specific language: Definition, contrast with general-purpose
- (1:00) Examples of DSLs: SQL, regex, Dream Maker, Make, LaTeX, https://strudel.cc/
- (1:15) Why build a DSL: When a GP language is too much.
- (1:25) The pipeline — teaser: Scanner → Parser → Interpreter — names only
- (1:40) Wrap-up: Week 2 prep

---

## Week 2 — Little Languages

Textbook: Chapters 1–2

- (0:00) Recap: DSLs, the pipeline: Week 1 teaser → full picture
- (0:10) What is a little language: Revisited with more depth
- (0:25) The pipeline (full): Scanner, parser, static analysis, optimiser, code gen
- (0:45) Compilers vs interpreters: Distinction applies to implementations, not languages
- (1:00) Regular expressions as a DSL: Live exploration on regexr.com
- (1:20) Language completeness: Turing view (vars, conditions, loops) vs Church view (vars, functions)
- (1:40) Wrap-up: Read Ch 3 for Week 3

---

## Week 3 — Lox

Textbook: Chapter 3

- (0:00) Recap: the pipeline
- (0:10) Introducing Lox: Why Lox: simple, Java-based, from the book
- (0:25) Lox features: Dynamic typing, classes + prototypes, functions, closures
- (0:45) Expressions vs statements: Values vs side effects
- (1:05) Turtle graphics demo: Lox program generating Logo output
- (1:40) Wrap-up: Read Ch 4, start your own Lox interpreter

---

## Week 4 — Scanning

Textbook: Chapter 4

- (0:00) Recap: Lox
- (0:10) What is scanning: Characters → tokens
- (0:25) Tokens, keywords, literals: Token types, the scanner's job
- (0:40) Lookahead: Single vs double (Lox needs 2)
- (0:55) Demo: traffic
- (1:20) Scanner in action: `cd java && javac variants/four_traffic/*.java && java variants.four_traffic.Lox --debug variants/four_traffic/traffic_lang/demo.traffic_lang`
- (1:35) Semester project intro: What we're building, the river system domain
- (1:50) Wrap-up: Read Ch 5

---

## Week 5 — Abstract Syntax Trees and Grammars

Textbook: Chapter 5

- (0:00) Recap: scanning
- (0:10) ASTs: Expressions as trees, evaluation as tree traversal
- (0:25) Context-free grammars: Terminals, non-terminals, metasyntax
- (0:40) Grammar notation: Nystrom's notation, generating strings
- (0:55) Demo: GenerateAst tool: Visitor pattern, metaprogramming
- (1:15) Grammar for river combining: `+` and `<-` operators as grammar rules
- (1:40) Wrap-up: Read Ch 6

---

## Week 6 — Parsing

Textbook: Chapter 6

- (0:00) Recap: ASTs, grammars
- (0:10) Recursive descent parsing: Grammar → Java methods
- (0:25) Ambiguity: Finding and removing it
- (0:35) Precedence and associativity: How grammar structure enforces these
- (0:45) Left recursion: Why it breaks recursive descent, workarounds
- (0:55) Demo: parser for water flow: On-paper grammar first, then Java
- (1:20) Assignment One guidance: What's due, rubric, examples
- (1:40) Wrap-up: Read Ch 7

---

## Week 7 — Evaluation of Expressions

Textbook: Chapter 7

- (0:00) Recap: parsing
- (0:10) Values vs expressions: Parser creates expressions, interpreter creates values
- (0:25) Tree-walking evaluation: Traversing the AST
- (0:40) Visitor pattern for evaluation: One evaluator, methods per node type
- (0:55) Demo: evaluating water flows: Run the interpreter on water flow expressions
- (1:20) Truthiness and errors: Non-boolean values, exception-based error handling
- (1:40) Wrap-up: Read Ch 8.1–8.2

---

## Week 8 — Statements

Textbook: Chapter 8 (sections 8.1–8.2)

- (0:00) Recap: evaluation
- (0:10) Statements vs expressions: Effects vs values
- (0:25) Variable declarations: `var x = value;` grammar and parsing
- (0:40) Assignment: L-values, side effects
- (0:55) Demo: adding variables: End-to-end: scanner → parser → AST → interpreter
- (1:20) Grammar extensions: New productions: declaration, statement, varDecl
- (1:40) Wrap-up: Read rest of Ch 8

---

## Week 9 — Statements (Environments)

Textbook: Chapter 8 (remainder)

- (0:00) Recap: statements
- (0:10) Environments: Name → value mappings, enclosing scope links
- (0:25) Environment diagrams: Cactus notation
- (0:40) Local scope and shadowing: Block-level scoping, inner hides outer
- (0:55) Demo: environment chain: Live trace of nested scopes
- (1:20) L-values vs R-values: Which positions variables occupy
- (1:40) Wrap-up: Read Ch 9

---

## Week 10 — Control Flow

Textbook: Chapter 9

- (0:00) Recap: environments
- (0:10) If/else: Grammar, parsing
- (0:20) While and for loops: Grammar, desugaring for → while
- (0:35) Logical operators: `and`, `or`, short-circuit evaluation
- (0:50) Syntactic sugar: Desugaring as a design principle
- (1:05) Demo: control flow: Live: if/while/for in the interpreter
- (1:25) Bridge: dam syntax: Conditionals → dam decision logic
- (1:40) Wrap-up: Read Ch 10 (up to 10.3)

---

## Week 11 — Functions Part 1

Textbook: Chapter 10 (up to 10.3)

- (0:00) Recap: control flow
- (0:10) First-class functions: Functions as values, expressions evaluating to functions
- (0:25) Function calls: Parsing, the call stack
- (0:40) Church encoding: Numbers as functions (theoretical interlude)
- (0:55) Demo: Church numerals in Lox: Live: zero, one, plus, incr
- (1:20) Native functions: LoxCallable interface, arity, built-ins
- (1:40) Wrap-up: Read rest of Ch 10

---

## Week 12 — Functions Part 2

Textbook: Chapter 10 (remainder)

- (0:00) Recap: first-class functions
- (0:10) Function definitions: The Function object, body not executed immediately
- (0:25) Return statements: Returning without value → nil
- (0:40) Closures: Inner functions capturing outer environments
- (0:55) Demo: makeCounter, local functions: Live: closure patterns
- (1:15) SKI combinator calculus: Advanced example of local functions
- (1:40) Wrap-up: Read Ch 11

---

## Week 13 — Resolving

Textbook: Chapter 11

- (0:00) Recap: closures
- (0:10) The closure variable problem: Variable changes between calls
- (0:25) Lexical vs dynamic scoping: Why it matters
- (0:40) Static analysis: name resolution: A phase between parsing and execution
- (0:55) Demo: resolveLocal, scope chain: Live: walking the scope chain
- (1:15) Minifier as static analysis: Renaming variables as a worked example
- (1:40) Wrap-up: Semester review
