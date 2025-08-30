## Week Overview

This week we turn our focus to adding statements to our interpreter

## Goals

By the end of this week you should:

    * Be able to parse and represent non-variable statements
    * Be able to execute non-variable statements
    * Be able to parse and represent variable declaration and assingment

## Preparation
  * Read Sections 8.1 and 8.2 of chapter 8 of "Crafting Interpreters"
  * Watch the following echo360 videos
    - Generating Statements
    - Parsing Statements
    - Grammar tracing
    - Adding variables to expressions

**bindings**: Ask the internet what a _variable binding_ is and you will get all sorts of different answers.  Some say it is the binding of a variable to a scope.  Others say it is the binding of a variable to a location in memory, others say it is the binding of a value to a variable.  It can mean any of these things, but I think the second is closest for us.  The important thing about bindings is that once they exists, they persist.  That means we need to keep track of bindings.  So, they are always related to whats in a variable and always need tracking by an interpreter.

**side effect**: Anything a program does that is not _creating a value_ is called a side-effect.  _Creating_ a value is understood generously, you might think `+` only _changes_ values but it actually takes two existing values and creates a new one.  So anything that returns, creates, computes a value is excluded from this discussion.  Everything _else_ has a side-effect.  The side-effect of a variable declaration is the creation of a new binding.  The side-effect of a `print` statement is that the console output changes.  The side-effect of assignment is that a variable location changes. On and on it goes.  Statements have side-effects, expressions have values.

# The Grammar of Statements

## class

### try a simpler grammer <essay>
question: |
  *NB: This question is prompting you to understand the system you have built.  The change is less important than knowing where the changes occur, why they occur there and why they don't occur in other places*

  Nystrom is looking ahead a little with his new grammar.  It is not _actually_ necessary at this point to have a separate `declaration` production.  I.e. the following grammar for statments will work (you need to fold in your own expression productions)
  ```
  program -> statement* EOF;
  statement -> varDecl
            |  exprStmt
            |  printStmt;
  ```
    Write out the full grammar using this approach and adjust your week 7 code so that is conforms to this grammar. Hint: Since the `Parser` is your implementation of the grammar, that will need to change.  Since your Interpreter walks the result of the parser, that will need to change as well.  Oh, and the AST was partly reflective of the grammar - That probably won't need to change because that detail of the grammar didn't make it to our AST.  Draw a diagram showing the classes your new AstGenerator is generating just to be sure.
answer: |
  ```
  program   -> statement* EOF;
  statement -> varDecl
            |  exprStmt
            |  printStmt;
  exprStmt  -> expression ";";
  printStmt -> "print" expression ";";
  varDecl   -> "var" IDENTIFIER ( "=" expression )? ";"; 
  expression     -> equality;
  equality       -> comparison (("!=" |"==" ) comparison )* ;
  comparison     -> term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
  term           -> factor ( ( "-" | "+" ) factor )* ;
  factor         -> unary ( ( "/" | "*" ) unary )* ;
  unary          -> ( "!" | "-" ) unary
                 | primary ;
  primary        -> NUMBER | STRING | "true" | "false" | "nil"
                 | "(" expression ")" i
                 | IDENTIFIER;
  ```
  Here is my diagram
  <img src="7_ast_classes.jpeg"/>
  Because I didn't end up with a `declaration` production, I also didn't end up with a `declaration` function, but it all fit just fine in the `statement` function.  I did have to think about the error catching though
  ```
  private Stmt statement() {
    try {
      if (match(PRINT)) return printStatement();
      if (match(VAR)) return varDeclaration();
      return expressionStatement();
    } catch (ParseError error) {
      synchronize();
      return null;
    }
  }
  ```

### complete the evaluator<essay>
question: |
  Without environments (next week) we can't correctly evaluate variables, but you can fill-in _stubs_ for those methods that just return null.  Do this and check your interpreter is working from end-to-end by running these programs.  When I went through this, I _think_ I found an ommission in the text.  I didn't notice any suggestion in this chapter that I need to update my AstPrinter.  But I really should since I've changed the methods in the `Expr.Visitor`, right?
answer: |
  I just needed two stubs in my `Interpreter`
  ```
  @Override
  public Object visitVariableExpr(Expr.Variable expr) {
      return null;
  }
  ```
  and
  ```
    @Override
    public Void visitVarStmt(Stmt.Var stmt) {
     return null;
    }
  ```

### Add our own statement <essay>
question: |
  Add a new type of statement to Lox.  The statement is `exit` and it should stop execution of the current program immediately.  You will need to touch most parts of the interpreter to make this work.  I will the attached answer is a full zip of the Lox interpreter as of week seven _and_ with the changes from the other class questions applied.  Note that _you_ will need to make decisions about how this new statement works.  The statments "stops execution immediately" seems clear but there are levels of detail unsaid.  Should it stop the interpreter as well?  Should it stop by throwing an error or some other mechanism?  As you implement your answer you should think about where you making these decisions and what you decided. 
answer: |
  There is a minor "trick" here - the exit statement is a terminal with no interesting data in it (i.e no fields are needed).  However, the AST code generation assumes there will be at least one, so we need to fix that.  You will see it in my diff below.  I know presenting an answer like this as a diff is not great, I will try and improve on it, but it is there for now
  <code src="java/variants/week7_with_exit/diff"/>

## practice
### variable decls
In the following code, which lines contain _variable declarations_.  Don't include variable _uses_ in your answer<br/>
```
var x = 1;
print x;
var y = 3;
print x + y;
```
{
  ~1 only
  =1 and 3
  ~2 only
  ~1, 2, and 4
  ~3 only
  ~none
}

### variable uses
In the following code, which lines contain _variable uses_.  Don't include variable _declarations_ in your answer<br/>
```
var x = 1;
print x;
var y = 3;
print x + y;
```
{
  ~1 only
  ~2 and 3
  ~2 only
  =2 and 4
  ~3 only
  ~none
}

## pass

### variable decls
In the following code, which lines contain _variable declarations_.  Don't include variable _uses_ in your answer<br/>
```
var x = 1;
print x;
print x + 1;
```
{
  =1 only
  ~2 and 3
  ~2 only
  ~1, 2, and 3
  ~3 only
  ~none
}

### variable uses
In the following code, which lines contain _variable uses.  Don't include variable _declarations_ in your answer<br/>
```
var x = 1;
print x;
print x + 1;
```
{
  ~1 only
  =2 and 3
  ~2 only
  ~1, 2, and 3
  ~3 only
  ~none
}


## distinction

### where are uses <essay>
question: |
  Explain, using a concrete example, where _variable uses_ are encoded in the following grammar
  ```
  program   -> statement* EOF;
  statement -> varDecl
            |  exprStmt
            |  printStmt;
  exprStmt  -> expression ";";
  printStmt -> "print" expression ";";
  varDecl   -> "var" IDENTIFIER ( "=" expression )? ";"; 
  expression     -> equality;
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
answer: |
  It is on the very last line.  Variable uses appear as an indentifier in an expression.  The identifier in the `varDecl` production is not a variable use, it is the variable declaration.  As a concrete example, consider the parse of the following program
  ```
  var x  = 3;
  print x;
  ```
  Will be
  ```
  program -> [ statement -> varDecl  -> "var" IDENTIFIER "x"
                                        ( "=" expression   -> equality -> comparison -> term -> factor -> unary -> primary -> NUMBER -> 3
                                        ) ";"
               statement -> printStmt -> "print" expression -> equaliy -> comparison -> term -> factor -> unary -> primary -> IDENTIFIER "x"
                                         ";"
             ]
  ```