# Week 9 + 10 Combined Lecture Plan
*For COMP3000 Programming Languages - Single Lecture (100 minutes)*

## Time Budget

| Section | Time | Focus |
|---|---|---|
| Recap + Bridge | 0-10 min | Quick recap of Week 8 (statements/vars). Bridge: to evaluate `if`, `while`, `for`, and nested blocks, we need a way to track bindings - environments. |
| Environments Core | 10-30 min | What environments are (name→value), scope chains, blocks create new environments, shadowing. Use cactus diagrams. |
| Environment Demo | 30-40 min | Live demo: show environment chain for nested blocks/vars. Focus on get/set/define and how resolution walks up the chain. |
| Control Flow Basics | 40-55 min | if/else, truthiness (non-bool values), while loops. Keep it concrete with Lox examples. |
| for + desugaring | 55-65 min | Teach `for` as syntactic sugar over `while`. Show grammar → desugared while. |
| Logical ops & short-circuit | 65-75 min | `and`/`or` with short-circuit evaluation. Demonstrate with side-effect examples. |
| Combined Demo | 75-90 min | Run a single example that uses blocks+shadowing + if/while/for + short-circuit in the interpreter. |
| Wrap-up + Q&A | 90-100 min | Summarise, point to readings, flag common pitfalls. |

---

## 1. Recap + Bridge (0-10 min)

- **Recap (Week 8):** Variable declarations (`var x = value;`), statements vs expressions, assignment and L-values.
- **Bridge:** Control flow constructs (`if`, `while`, `for`) and blocks (`{ ... }`) introduce the need for local scopes. To track bindings correctly (and support shadowing), we need an environment structure.
- **Key point:** Environments are the scoping mechanism that makes blocks and control flow behave as expected.

---

## 2. Environments Core (10-30 min)

Focus on the essential concepts:

- **Environment:** A mapping from identifiers (names) to values, plus a reference to an enclosing (parent) environment.
- **Scope chain:** When resolving a variable, walk from current environment up to enclosing until found (or error).
- **Blocks create new environments:** Entering `{ ... }` creates a new child environment; exiting restores parent.
- **Shadowing:** An inner binding hides an outer binding with the same name.
- **Assignment vs declaration:** Declaration defines in current environment; assignment looks up the variable in scope chain (L-value resolution).
- **L-values vs R-values:** Distinguish where variables are written to vs read from.

**Visual:** Use cactus (environment diagram) notation to show nested scopes clearly.

---

## 3. Environment Demo (30-40 min)

**Example 1 - Nested blocks and shadowing:**
```lox
{
  var x = 1;
  {
    var x = 2;
    print x;  // Should print 2
  }
  print x;    // Should print 1
}
```

**Demonstrate:**
1. Create global/root environment.
2. Enter outer block → new environment (child of global), define x=1.
3. Enter inner block → new environment (child of outer), define x=2 (shadows). Look up x → finds 2.
4. Exit inner block → back to outer. Look up x → finds 1.
5. Show environment chain walking on get/set.

**Key methods to highlight:** `define(name, value)`, `get(name)`, `assign(name, value)` - and that `get/assign` walk up the enclosing chain.

---

## 4. Control Flow Basics (40-55 min)

Introduce control flow in Lox (Chapter 9):

- **if/else:** Grammar form `if (expr) stmt (else stmt)?`. Evaluate condition, then branch. 
- **Truthiness:** In Lox, non-boolean values have truthiness rules (only `false` and `nil` are falsy; everything else is truthy). Emphasise this differs from some languages.
- **while loops:** `while (cond) stmt`. Evaluate condition each iteration; if true, execute body. Body can mutate state or create blocks.
- **Blocks with control flow:** Bodies are statements (possibly blocks), so they naturally work with environments.

**Quick examples:**
```lox
var x = 5;
if (x > 3) {
  print "greater";
} else {
  print "not";
}

var i = 0;
while (i < 3) {
  print i;
  i = i + 1;
}
```

---

## 5. for + Desugaring (55-65 min)

**Key teaching point:** `for` is syntactic sugar over `while`. This is a core design principle (desugaring reduces language surface area).

**Lox for loop grammar (from source):**
```
forStmt -> "for" "(" ( varDecl | exprStmt | ";" )
                   expression? ";"
                   expression? ")" statement ;
```

**Desugaring example:** Show how
```lox
for (var i = 0; i < 3; i = i + 1) {
  print i;
}
```

desugars to:
```lox
{
  var i = 0;
  while (i < 3) {
    {
      print i;
    }
    i = i + 1;
  }
}
```

Note: the body may be wrapped in a block in the desugared form to properly scope any declarations inside (and to be precise about execution order). Emphasise: desugaring is a clean implementation strategy (parse `for` into equivalent AST using `while` + blocks).

---

## 6. Logical Operators & Short-Circuit (65-75 min)

**Operators:** `and`, `or` in Lox. These are control-flow operators (not just boolean combinators).

**Short-circuit evaluation:** 
- `A and B`: evaluate A; if falsy, return A (short-circuit, B not evaluated). If truthy, evaluate and return B.
- `A or B`: evaluate A; if truthy, return A (short-circuit, B not evaluated). If falsy, evaluate and return B.

**Crucial example with side effects (matches exam/gift concept):**
```lox
var x = true;
print x or (print "nope");  // prints true; RHS never evaluated
```
```lox
var x = false;
print x or (print "yep");   // prints "yep"; RHS evaluated
```

```lox
var y = false;
print y and (print "nope"); // prints false; RHS not evaluated
```
```lox
var y = true;
print y and (print "yep");  // prints "yep"; RHS evaluated
```

This directly exercises the idea tested in `short circuit side effect <gift>` (src/10_control_flow.md).

---

## 7. Combined Demo (75-90 min)

Tie both weeks together in one live example that uses blocks, shadowing, environments, and multiple control flow features.

**Suggested combined example:**
```lox
{
  var total = 0;
  for (var i = 1; i <= 5; i = i + 1) {
    if (i == 3) {
      var msg = "skip";
      print msg; // shadowing example
    } else {
      total = total + i;
    }
  }
  print total; // should be 1+2+4+5 = 12
}
```

Or extend with short-circuiting:
```lox
{
  var count = 0;
  var running = true;
  while (running and count < 3) {
    count = count + 1;
    print count;
    running = (count < 3); // becomes false at end
  }
  print "done";
}
```

**Demonstrate live:** Trace environment creation on block entry, show scope chain during lookups, and show how control flow jumps affect execution (not just evaluation). Show short-circuit prevents RHS evaluation when appropriate.

---

## 8. Wrap-up + Q&A (90-100 min)

- **Key takeaways:** Environments + blocks = lexical scoping. Control flow + environments work together naturally. Desugaring (`for` → `while`) simplifies implementation. Short-circuiting is control flow, not just boolean logic.
- **Readings:** Chapter 8 remainder (environments, blocks, scope) + Chapter 9 (control flow, logical ops, truthiness).
- **Common pitfalls:** Forgetting to create new env on block entry, walking chain incorrectly on assignment vs definition, implementing `and`/`or` as eager functions instead of short-circuiting, getting `for` desugaring order wrong (init runs once, condition checked, increment runs after body).
- **Exam note:** Focus on scope chain walking, blocks creating environments, shadowing, and short-circuit evaluation order (these map directly to common gift questions like "automarked environment", "short circuit side effect", and grammar questions for control flow).
