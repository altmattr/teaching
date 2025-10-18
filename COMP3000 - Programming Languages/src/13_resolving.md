## WEEK OVERVIEW

This week we cut in on the dance between static and dynamic in our interpreter. We recognise and then fix an issue with closures. 

## GOALS

By the end of this week you should:

    Be fully comfortable with closures in lox
    Be able to demonstrate the problem of scope change in blocks with closures
    Be able to fix the problem of scope change in blocks with closures.
    Be able to add new static analysis phases to your compiler

## Preparation

# RAT

## max visits <gift>
What is the maximum number of visits an AST node could recieve during a static analysis like resolution?{
    ~0
    =1
    ~2
    ~infinite
    ~more than one but not infinite
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
    The two things that make an interpreter take a long time are loops and recursive functions.  Without them, all programs would be fast. Any analysis we do that _chooses_ not to go into function call and _chooses_ not to loop loops is certain to execute in a fixed, relatively small time.  These analyis are the ones we call static analysis.  The comparison in why some people call static analysis "partial interpretation".

## Write a new static analysis phase <essay>
question: |
    Write a static analysis phase for your interpreter which will rename all variables to the shortest possible name.  This is a type of minifier.  The first variable should be renamed to "a", the second to "b", etc until the 27th which is renamed "aa" and the 28th which is "ab".
answer: |
    still to do.

# Exam