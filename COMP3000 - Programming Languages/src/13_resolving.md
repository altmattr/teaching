## WEEK OVERVIEW

This week we cut in on the dance between static and dynamic in our interpreter. We recognise and then fix an issue with closures. 

## GOALS

By the end of this week you should:

    Be fully comfortable with closures in lox
    Be able to demonstrate the problem of scope change in blocks with closures
    Be able to fix the problem of scope change in blocks with closures.
    Be able to add new static analysis phases to your compiler

## Preparation

  * Read chapter 11 of "Crafting Interpreters"
  * Watch the following echo360 videos:
    - The closure scoping problem
    - The closure scoping solution

# RAT

## max visits <gift>
What is the maximum number of visits an AST node could receive during a static analysis like resolution?{
    ~0
    =1
    ~2
    ~infinite
    ~more than one but not infinite
}

## main challenge <gift>
When resolving variable names in the presence of closures, what is the main challenge that needs to be addressed?  
{  
~ The need to distinguish between global and local variables.  
~ Ensuring variables declared in one function are completely inaccessible from another.  
= Maintaining access to variables in the enclosing scope after the enclosing function has returned.  
~ Guaranteeing that all variables in the closure are automatically copied into the function's arguments.  
}

## undeclared <gift>
What happens if a variable is referenced in a closure but has not been declared in any enclosing scope?  
{  
~ The variable is treated as a global variable by default.  
~ The resolver automatically creates the variable in the nearest enclosing scope.  
~ The variable is considered undefined but will not throw an error until it is assigned a value.  
= A runtime error occurs because the variable cannot be resolved.  
}

## resolve local <gift>
What is the purpose of the `resolveLocal()` function in *Crafting Interpreters*?  
{  
~ To execute the bytecode for variables in the local scope.  
= To determine the specific scope in which a variable resides during name resolution.  
~ To remove variables from the stack of scopes when a function call ends.  
~ To optimize variable lookups by caching their memory addresses.  
}

## scope chain <gift>
How does the scope chain resolve variable references when a closure is called in Lox?{
~By searching only in the global scope
~By searching for the variable in the most recent scope, then upwards through recent scopes in order
=A separate structure maintains information about the lexical scope which is used instead of the dynamic scopes.
~By resolving all variables during the function's definition
}

# FAT

## easier way <essay>
question: |
    There has to be an easier way to do this.  Brainstorm possiblities in class and try them out to see if they work.
answer: |
    I can't provide you a ready-made answer to this one but your discussion should include

      * Whether the solution works in practice
      * What would need to change in the interpreter to implement it.
    
    I do have a suggestion not given in the book, which is to add a phantom block for every variable declaration.  Will that work?

# SSE

## write a troublesome program <essay>
question: |
    Write your own program which will trigger the error in the week eleven code base.  The most "natural" (i.e. least contrived) example will .  Is it possible to trigger this error without a local function?
answer: |
    I think it is not possible because the error comes from the way closures operate.  You need a closure within a non-global scope.  That does raise the question, what is different about the global scope?

## not evaluation <essay>
question: |
    If semantic analysis is done with an AST visitor, what stops it from being "just another interpreter"?
answer: |
    The two things that make an interpreter take a long time are loops and recursive functions.  Without them, all programs would be fast. Any analysis we do that _chooses_ not to go into function call and _chooses_ not to loop loops is certain to execute in a fixed, relatively small time.  These analyis are the ones we call static analysis.  The comparison is why some people call static analysis "partial interpretation".

## Write a new static analysis phase <essay>
question: |
    Write a static analysis phase for your interpreter which will rename all variables to the shortest possible name.  This is a type of minifier.  The first variable should be renamed to "v1", the second to "v2", etc.
answer: |
    This was a very instructive exercise.  For most AST nodes, the transformation did nothing but I still had to pull apart the node, `accept` on each subpart, then put back together.  In the solution below I have just put `passToParts()` for that and left it out or the solution would be massive.  This is the very pain of the Visitor pattern and one reason people started getting very excited about Functors.  You can look them up if you like.

    The parts where I had to do something, I simply chose a new name at declaration and put it in a map, then looked up the map for every variable use.
    `````
    package variants.wk13_minifier;
    import java.util.HashMap;
    import java.util.Map;
    import java.util.List;
    import java.util.ArrayList;

    // the minifier takes the ast and returns a new ast with names minimised
    class Minifier implements Expr.Visitor<Expr>, Stmt.Visitor<Stmt> {
        public List<Stmt> minify(List<Stmt> ast){
            List<Stmt> newAst = new ArrayList<Stmt>();
            for (Stmt statement : ast){
                newAst.add(statement.accept(this));
            }
            return newAst;
        }

        Map<String, String> nameMap =  new HashMap<String, String>();
        int nameCounter = 0;
        public String nextName(){
            String name = "v" + nameCounter;
            nameCounter += 1;
            return name;
        }

        public Stmt visitBlockStmt(Stmt.Block stmt)          {return passToParts();}
        public Stmt visitExpressionStmt(Stmt.Expression stmt){return passToParts();}
        public Stmt visitFunctionStmt(Stmt.Function stmt)    {return passToParts();}
        public Stmt visitIfStmt(Stmt.If stmt)                {return passToParts();}
        public Stmt visitPrintStmt(Stmt.Print stmt)          {return passToParts();}
        public Stmt visitReturnStmt(Stmt.Return stmt)        {return passToParts();}
        public Stmt visitVarStmt(Stmt.Var stmt)              {
            String newName = nextName();
            nameMap.put(stmt.name.lexeme, newName);
            stmt.name.lexeme = newName;
            return stmt.accept(this);
        }
        public Stmt visitWhileStmt(Stmt.While stmt)          {return passToParts();}

        public Expr visitAssignExpr(Expr.Assign expr)        {return passToParts();}
        public Expr visitBinaryExpr(Expr.Binary expr)        {return passToParts();}
        public Expr visitCallExpr(Expr.Call expr)            {return passToParts();}
        public Expr visitLogicalExpr(Expr.Logical expr)      {return passToParts();}
        public Expr visitGroupingExpr(Expr.Grouping expr)    {return passToParts();}
        public Expr visitLiteralExpr(Expr.Literal expr)      {return passToParts();}
        public Expr visitUnaryExpr(Expr.Unary expr)          {return passToParts();}
        public Expr visitVariableExpr(Expr.Variable expr)    {
            expr.name.lexeme = nameMap.get(expr.name);
            return expr.accept(this);
        }
    } 
    `````

# Exam

## which needs lexical scoping <gift>
Only one of the following programs would have an error if we had not fixed the name resolution to account for lexical scopes.  Which one?{
    ~```
    var a = 5;
    {
        fun foo(a) {
            return a + a;
        }

        print(foo(a));
        var a = 2;
        print(foo(a));
    }```
    =```
    var a = 5;
    {
        fun foo() {
            return a + a;
        }

        print(foo());
        var a = 2;
        print(foo());
    }```
    ~```
    var a = 5;
    {
        fun foo(a) {
            return a + a;
        }

        print(foo(a));
        var b = 2;
        print(foo(b));
    }```
    ~```
    var a = 5;
    {
        fun foo() {
            return a + a;
        }

        print(foo());
        var b = 2;
        print(foo());
    }```

}