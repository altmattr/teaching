
## WEEK OVERVIEW

This week we turn our focus to control flow which includes conditional statements and loops.

## GOALS

By the end of this week you should:

  * Have if statements, while, and for loops added to your lox compiler
  * Understand how the underlying Runtime control flow interacts with Lox control flow
  * Have a strong and reliable understanding of how to add new features to the Lox compiler.

## Preparation
  * Read Chapter 9 of "Crafting Interpreters"
  * Watch the following videos on echo360:
    - Mathematical foundations of computation
    - Conditions
    - Loops

# RAT
## Which new grammar a <gift>
The following is the grammar we used to parse logical expressions but the _and_ and _or_ parts are missing
```
  program   -> declaration* EOF;
  declaration -> varDecl
              |  statement;
  statement -> exprStmt
            |  forStmt
            |  ifStmt
            |  printStmt
            |  whileStmt
            |  block;
  block     -> "\{" definition* "\}"
  exprStmt  -> expression ";";
  forStmt   -> "for" "(" ( varDecl | exprStmt | ";" )
                 expression? ";"
                 expression? ")" statement ;
  ifStmt    -> "if" "(" expression ")" statement
               ( "else" statement )? ;
  printStmt -> "print" expression ";";
  whileStmt -> "while" "(" expression ")" statement ;
  varDecl   -> "var" IDENTIFIER ( "=" expression )? ";"; 
  expression     -> assignment;
  assignment     -> IDENTIFIER "=" assignment
                 | logic_or;
  logic_or       -> ??? ;
  logic_and      -> ???;
  equality       -> comparison (("!=" |"==" ) comparison )* ;
  comparison     -> term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
  term           -> factor ( ( "-" | "+" ) factor )* ;
  factor         -> unary ( ( "/" | "*" ) unary )* ;
  unary          -> ( "!" | "-" ) unary
                 | primary ;
  primary        -> NUMBER | STRING | "true" | "false" | "nil"
                 | "(" expression ")" 
                 | IDENTIFIER;
```
Which of the following ways to fill-in the missing parts will give a grammar where _the and operator_ is given as an infix `&&` and _the or operator_ is given as an infix `||` as in C.  _The and operator_ must have higher precedence than _the or operator_.{
    ~  `logic_or -> logic_and ( "or" logic_and)* ;logic_and -> equality ( "and" equality)*;`
    ~  `logic_or -> equality ( "or" equality)* ;logic_and -> logic_or ( "and" logic_or)*;`
    =  `logic_or -> logic_and ( "||" logic_and)* ;logic_and -> equality ( "&&" equality)*;`
    ~  `logic_or -> equality ( "||" equality)* ;logic_and -> logic_or ( "&&" logic_or)*;`
}

## short-circut <gift>
What type of short-circuiting behavior do logical operators like `and` and `or` exhibit in Lox?
{
~They always evaluate both operands, regardless of the first operand's value.
=They evaluate the second operand only if the first operand doesn’t determine the outcome.
~They never evaluate the second operand, regardless of the context.
~They evaluate as if they were the negation of the opposite operator.
}

## how to implement short-circut <gift>
Which of the following statements best describes how short-circut evaluation is implemented in the Lox interpreter?{
    ~It is hard-coded into the `visitIfExpr` `Interpreter` visitor
    ~It is done by Java without the Lox interpreter writer needing to do it explicitly
    ~It is done in Java by using Java's OR and AND
    =It is hard coded into the `visitLogicalExpr` `Interpreter` visitor
}

## interpreting loops <gift>
When implementing a `while` loop in the interpreter, what is the general approach?{
~Convert the loop to a conditional and a statement block.
~The interpreter evaluates the loop body first, and then checks the condition after each iteration.
~The loop body and condition are both converted into a single block of code and executed together without repetition.
=The interpreter repeatedly evaluates the condition expression, and if it is true, executes the loop body.
}

# FAT

## Environments and Control Flow <tex-essay>
question: |
    We left our interpreters with variables and statements, but we didn't grapple with how different scopes will affect how we track variables.  As soon as we introduce control flow we really do need to deal with that.

    However, we don't have any particular need for control flow or nested scoped in this particular domain.  We were very happy to get variables, but I don't think any of you were really hanging out for loops or conditions.

    So this week we are going to motivate these two features more than we are going to directly implement them.  The motivation is \emph{dams}.  Dams are managed by humans.  The outlet can be opened or closed at will depending on how much water is in the dam and how much rain has occurred and even how much rain is predicted.

    Your team's task this week is to design the syntax and parser which you will need to support dams.  We will hold off on adjusting the interpreter for now.

    \subsubsection*{An example}
    To give your imagination a prompt, here is the language I've been building up in my own investigations\footnote{I've become quite fond of Devlin's creek, but it has no dams, so I will have to demonstrate with Googong}
    \begin{lstlisting}
    var googong_river = 12R;
    var googong_dam = ???;
    var googong_complete = googong_river + googong_dam;
    var queanbeyan_complete = 2R + googong_dam;
    \end{lstlisting}
    Googong dam \emph{does not} just release the same water that comes into it.  The dam lets out no water sometimes, a little water at other times, and lots of water sometimes.  That means there will be some \emph{decisions} made in determining the output, i.e. some type of \emph{computation}.  Something like a block maybe?

    \begin{lstlisting}
    var googong_river = 12R;
    var googong_dam = {
        if (googong_river < 5)
        return 0;
        else
        return 10;
    };
    var googong_complete = googong_river + googong_dam;
    var queanbeyan_complete = 2R + googong_dam;
    \end{lstlisting}

    There are problems with this, but it gives you an idea of a direction you can go in.  Flesh this out, come up with a better form.  I encourage you to consider functions while doing so.  Even though we haven't done parsing of functions yet, it won't be long.
    \newpage
answer: |
    still to come

# SSE

## Disallow single line <essay>
question: |
    Get your Lox compiler up to date so that is can interpret conditional statements.  To be convinced you have it working, show that it works on this Lox program
    ```
    var x = 5;
    var y = 10;

    x = x + 7;

    if (x > y) print("addition works");
    if (x <y) print ("addition is broken");
    else print("addition still works");
    if (x == y and x > y){
        print("something has gone horribly wrong");
    } else {
        print("don't worry, all is in order");
    }
    ```
    Make a copy of this interpreter and adjust this copy so that _single line if statements without braces are not allowed_.  I.e. the following program would not be allowed
    ```
    var x = 5;
    if (x > 3)
      print("x is big");
    ```
    and would need to be written as
    ```
    var x = 5;
    if (x > 3) {
      print("x is big");
    }
    ```
    Part of your job in completing this task is to have a good development setup for managing these versions.
answer: |
    still to do

## prove the opening parenthesis is not necessary <essay>
question: |
    Nystrom claims that the opening parenthesis in `if (condition){` is not necessary.  By this he means that in the existing grammar it is necessary, but it is possible to create a different grammar where it is not and that grammar will be parsable with no difficulty.  Explain why with reference to how the parser is operating.  Write some exaple Lox programs in this style.  Do you like them?  Why or why not?
answer: |
    still to do.

## or production <essay>
question: |
    The `logic_or` grammar production looks like this
    ```
    logic_or       -> logic_and ( "or" logic_and )* ;
    ```
    A friend of yours asks you "Why is that a `*` instead of a `+`? Surely every "or" expression has at least one or in it?".  Explain why the `*` is used instead of `+`.
answer: |
    The `logic_or` is not a production for when there _is_ an or.  It is a production for where there _could be_ an or.  Many expressions don't have any ors in them but that production rule is still part of the chain of rules that are checked and thus it needs to allow an empty list of ors.  In this case the parser drops to the next rule and looks to see _if_ there are any `and`s in the expression, but there might not be.

## sweet or sour <essay>
question: |
    You've seen how desugaring can be just as hard to implement as full parsing and interpreting.  However, there are other reasons to like desugaring as an approach to language design.  Can you think of one one?  Explain the benefit.
answer: |
    I think having a simple "base" language makes it easier for programmers to understand sugared features.  Instead of needing to learn everything about them in detail, you only need to know what they desugar to. That cognitive load is much lower for me at least.

## sugar for do-until <essay>
question: |
    We are going to add a new type of loop to Lox.  The loop is a "do-until" loop with the following characteristics.  The grammar for a do-until statement is `doUntil -> "do" " statement "until" (" expression ")";`.  The loop always executes once, then repeats as long as the expression is false.  Explain, with details, how you would implement this in your Lox interpreter as _syntactic sugar_.  Provide enough detail that the reader could interpret your instructions to add a "do until" loop to their own Lox interpreter.
answer: |
    still to do

# Exams
## Which new grammar b <gift>
The following is the grammar we used to parse logical expressions but the _and_ and _or_ parts are missing
```
  program   -> declaration* EOF;
  declaration -> varDecl
              |  statement;
  statement -> exprStmt
            |  forStmt
            |  ifStmt
            |  printStmt
            |  whileStmt
            |  block;
  block     -> "\{" definition* "\}"
  exprStmt  -> expression ";";
  forStmt   -> "for" "(" ( varDecl | exprStmt | ";" )
                 expression? ";"
                 expression? ")" statement ;
  ifStmt    -> "if" "(" expression ")" statement
               ( "else" statement )? ;
  printStmt -> "print" expression ";";
  whileStmt -> "while" "(" expression ")" statement ;
  varDecl   -> "var" IDENTIFIER ( "=" expression )? ";"; 
  expression     -> assignment;
  assignment     -> IDENTIFIER "=" assignment
                 | logic_or;
  logic_or       -> ??? ;
  logic_and      -> ???;
  equality       -> comparison (("!=" |"==" ) comparison )* ;
  comparison     -> term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
  term           -> factor ( ( "-" | "+" ) factor )* ;
  factor         -> unary ( ( "/" | "*" ) unary )* ;
  unary          -> ( "!" | "-" ) unary
                 | primary ;
  primary        -> NUMBER | STRING | "true" | "false" | "nil"
                 | "(" expression ")" 
                 | IDENTIFIER;
```
Which of the following ways to fill-in the missing parts will give a grammar where _the and operator_ is given as an infix `&&` and _the or operator_ is given as an infix `||` as in C.  _The and operator_ must have higher precedence than _the or operator_.{
    ~  `logic_or -> logic_and ( "or" logic_and)* ;logic_and -> equality ( "and" equality)*;`
    ~  `logic_or -> equality ( "or" equality)* ;logic_and -> logic_or ( "and" logic_or)*;`
    ~  `logic_or -> logic_and ( "||" logic_and)* ;logic_and -> equality ( "&&" equality)*;`
    =  `logic_or -> equality ( "||" equality)* ;logic_and -> logic_or ( "&&" logic_or)*;`
}



