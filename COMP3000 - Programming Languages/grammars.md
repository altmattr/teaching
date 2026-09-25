# Simplest

expr -> expr op expr
     | number;
op   -> + | - | / | *;

## Parse trees for `1 + 2 + 3`

Our grammar is ambiguous, so `1 + 2 + 3` has two valid parse trees. It all depends on which `+` sits at the root.

### Left-associative: `(1 + 2) + 3`

```text
                 expr
          ┌──────┼──────┐
        expr      op    expr
      ┌──┼──┐     │      │
   expr  op expr  "+"   "3"
    │    │    │
  "1"  "+"  "2"
```

This tree matches the leftmost derivation:

### Right-associative: `1 + (2 + 3)`

```text
                expr
          ┌──────┼──────┐
        expr      op    expr
         │        │    ┌──┼──┐
        "1"      "+"  expr op expr
                       │    │   │
                      "2"  "+" "3"
```


Both derivations end up producing the same string of terminals, which is exactly why the grammar is ambiguous. If you want the parser to behave predictably you need to break the tie, for example by layering the grammar into precedence levels.

## Associativity only

If you want to fix the associativity ambiguity but keep a single precedence level, rewrite `expr` so it recurs on the left:

```
expr   -> expr op primary | primary;
op     -> + | - | / | *;
primary-> number;
```

The right operand of an `op` is now always a `primary`, so it can't swallow another operator. `1 + 2 + 3` has exactly one parse tree:

```text
                    expr
           ┌───────────┬───────┐
         expr           op    primary
  ┌───────┬───────┐     │       │
 expr    op    primary "+"     "3" 
   │      │       │              
primary  "+"     "2"        
   │              
  "1"          
```

Notice the right child at the top is a `primary "3"`, not another `expr`, so `2 + 3` can never become the right operand. Only `(1 + 2) + 3` is derivable.

The trade-off is that everything shares one precedence level, so mixed operators also group left-to-right: `1 + 2 * 3` reads as `(1 + 2) * 3`. In BNF, associativity and precedence are coupled; fixing one pins down the other.

### What about `1 + 2 * 3`?

Since the grammar has a single precedence level, `*` gets exactly the same treatment as `+`. The parse tree for `1 + 2 * 3` mirrors the one for `1 + 2 + 3`: the root `op` is `*`, the left child holds `1 + 2`, and the right child is a bare `primary "3"`.

```text
                      expr
           ┌───────────┬───────┐
         expr          op    primary
  ┌───────┬───────┐     │       │
 expr    op    primary "*"     "3" 
   │      │       │             
primary  "+"      "2"         
   │               
  "1"             
```

By arithmetic convention `*` should bind tighter than `+`, so the grouping we want is `1 + (2 * 3)` — and that tree isn't even derivable here, because the right operand of `+` is forced to be a `primary`, not an `expr`. So this grammar produces the wrong parse tree for mixed operators, and we need the layered `term`/`factor` version to get it right.

## Precedence

Putting a separate rule in for each level of precedence, with each level left-associative, gives the grammar no choice at all about how to parse:

```
expr   -> expr + term | expr - term | term;
term   -> term * factor | term / factor | factor;
factor -> number;
```

`term` and `factor` sit one level below `expr`, so `*` and `/` bind tighter than `+` and `-`. The lower levels are reached through `term` and `factor` rather than `expr`, so the right operand of `+` can now be `2 * 3`, while the left-associativity trick from `## Associativity only` is preserved.

Now `1 + 2 * 3` parses the way arithmetic convention wants:

```text
                    expr
              ┌──────┼───────┐
            expr     "+"    term
             │            ┌──┼──┐
           term        term  *  factor
             │            │       │
          factor       factor   "3"
             │            │
           "1"          "2"
```

The same expression that came out as `(1 + 2) * 3` in the single-level grammar now parses as `1 + (2 * 3)`.

## Summary

Two ideas are baked into the shape of the grammar rules:

`depth = precedence`. Operators that bind tighter appear lower in the hierarchy. `+` and `-` live in `expr`, so their operands are `term`s, and a `term` can contain `*` or `/`. But `*` and `/` live in `term`, so their operands are `factor`s (bare `number`s) and can never sneak in a `+` or `-`. Trees are built down from `expr`, so the `*`/`/` nodes end up inside the operands of the `+`/`-` nodes, which is exactly what "binds tighter" means.

`direction of recursion = associativity`. Each rule writes `expr -> expr + term` and `term -> term * factor`: the recursion is on the left, and the right-hand side is a single lower-level nonterminal. For `1 + 2 + 3` the right operand of the top `+` must be just a `term`, so it can't swallow a second `+`; only `(1 + 2) + 3` is derivable. The same trick at the `term` level makes `*` and `/` left-associative too. `1 * 2 * 3` can only be `(1 * 2) * 3`.

With both ideas in place, the grammar has no ambiguity left:

```
expr   -> expr + term | expr - term | term;
term   -> term * factor | term / factor | factor;
factor -> number;
```
