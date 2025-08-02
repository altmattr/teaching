  
##  WEEK OVERVIEW

This week we turn our focus to the Lox programming language, which we will implement over the rest of the semester.  We also do a whistle-stop tour of Ruby, the first if our LoFNs

## GOALS

By the end of this week you should:

    Be able to program in Lox
    Understand some basic Lox design decisions
    Have a high-level understanding of Ruby
    Understand some Ruby design decisions

## Glossary

**call stack**: In many programming languages, the variables accessible to a function are on the call stack.  The "call stack" is a stack of functions that have been called to get to this point. How each "stack frame" is structured is a whole topic we don't cover here, but it sure is interesting.

**instances**: An instance is always built from a class.  Thus the instances we are used to are objects.

**inheritance chain**: When a class inherits from another, there is a chain of classes that might store any particular method you try to call.  The _class_ is responsible for maintaining this, not the instance (aka object).

**static**: done at compile time.

**dynamic**: done at run time.

**virtual methods**: in a language which has the option of static dispatch, the word "virtual" is used to identify which methods are looked up in this way.  In languages like Java and Lox, all methods are virtual, you don't even think about non-virtual methods.

**REPL**: Stands for Read Eval Print Loop which is a program that will take one line of code at a time and respond to each one with some indication of what that line did.  Works best with "everything is an expression" languages.

**yield**: used for a number of things in different programming languages.  In Ruby it is used to run the current block.  If you are in a function, it will run the block that was given to that function (if there is one).

**API**: Application Programming Interface.  A fancy way to say "library" or "module" but it does imply a certain _composability_.

***DSL**: A "Domain Specific Language".  In some uses it is synonymous with "little language" from Nystrom but it implies the language is embedded in another - more general purpose - language (though this is not necessary!).

# FAT 
## Turtle Graphics <tex-essay>
question: |
    \begin{wrapfigure}{R}{0.33\textwidth}\begin{aside}
    The idea that one program might generate another program is powerful but a little strange.  Be sure you have your head around this idea before you begin. If the \emph{only} thing you get from this class is an intuition for generating programs from other programs, you will still have made a bit step forward in your understanding of programming languages.  This concept is key and will come up again very soon.  If you don't get it now, you will struggle later.
    \end{aside}\end{wrapfigure}


    A fun little language is logo (aka "turtle graphics").  It is a language designed for kids to learn programming.  It has a very simple syntax and a very simple set of commands.  The idea is that you can use it to draw pictures on the screen.  Check out the language this online implementations:
    \begin{itemize}
    \item \url{https://www.calormen.com/jslogo/}
    \end{itemize}
    In this task we will write a lox program which generates logo programs!  To make it interesting, we need to restrict ourselves to using \emph{only} the following logo commands:
    \begin{enumerate}
    \item \lstinline|clearscreen|: clear the screen
    \item \lstinline|fd n|: move the turtle forward n units
    \item \lstinline|rt n|: turn the turtle right n degrees
    \item \lstinline|pu|: lift the pen up
    \item \lstinline|pd|: put the pen down
    \end{enumerate}

    At the end of class you will share (for either the first task, or your second task) the following:
    \begin{enumerate}
    \item The turtle program that was generated
    \item The lox program that generated it.
    \end{enumerate}


    First, write a lox program which generates a logo program to draw the following picture.  You can use the online logo interpreter to check your generated program.

    \includegraphics{src/3_first.jpg}

    Once you have achieved this, try to write a lox program which generates this version.  If using only the commands above, this is a very long program which you don't want to write by hand.  You will \emph{need} to generate this program!

    \includegraphics{src/3_second.jpg}

    Once you have this done, go have some fun with logo and with generating logo programs.  If you have time to come up with a really fun generated program, please share the lox program that generated it with the class.
    \newpage
answer:
    Discussion released later

# RAT

## output of program <gift>
What will be the output of the following lox program
<pre>
>    var foo \= 4;
>    fun simple()\{
>        foo \= 6;
>    \}
>    simple();
>    print foo;
</pre>
{
    =6
    ~4
    ~compile error due to missing semi colon
    ~compile error due to wrong keyword
}

# SSE

## dynamic types <essay>
question:
  The text describes what _dynamic typing_ means.  Give a definition _in your own words_ of that concept.
answer: |
    It means the type of a _variable_ can change during program execution.  It is the opposite of _static_ typing where a variable is given a type and it must stay that type.  Note that dynamic normally means you don't declare a type, but that is not strictly necessary!


## more general not more better <essay>
question:
  In the text, the author identifies a language feature which is _simpler_ and _more general_ than the alternative.  Normally we would think of this an obvious win, but they say it is not.  What feature is this and what reason do they give?
answer:
    Choosing classes vs prototyping.  They say humans just _seem_ to prefer working with classes.  This is n important lession for any language designer - generality and simplicty are _normally_ best, but not alwasys.  You can only find out with empirical evidence


## compile-time vs run-time <essay>
question:
  What is _compile time_ and what is _run time_.  Be precise
answer: |
    "compile time" is the time between the programmer hitting "compile" and the compiler generating a program.  "run time" is the time between a program starting and the (maybe) program finishing.


## hello world <essay>
question:
  Write a lox program to print "hello world"
answer:
  print "hello world;"

## why dynamic <essay>
question:
  Give a reason dynamic typing might cause more run-time errors than static typing.
answer:
    The text says that "If you try to perform an operation on values of the wrong type—say, dividing a number by a string—then the error is detected and reported at runtime".  Other languages could detect this error at compile time.

## types of garbage collection <essay>
question: 
  Give the name of _one_ of the types of garbage collection described in the text.
answer:
    _reference counting_ and _tracing_


# RAT

## binary <gift>
"binary" operators are so-called because{
    =They have two arguments
    ~They work on binary data
    ~They generate binary data
    ~They do arithmetic operations
}

## infix <gift>
"infix" operators belong where?{
    =between the arguments
    ~infix the arguments
    ~within the one argument
    ~after the arguments
}

## statement vs expression <gift>
Match the language feature with its job{
    =statement -> produce an effect
    =expression -> produce a value
}

# SSE

## from book lox prog <essay>
question:
    Write some sample Lox programs and run them (you can use the implementations of Lox in my repository). Try to come up with edge case behavior I didn’t specify here. Does it do what you expect? Why or why not?
answer:
    still to do

## square <essay>
question:
    Write a lox program to print the first 50 square numbers.
answer:
    still to do

## prime <essay>
question:
    Write a lox program to print the first 50 prime numbers.
answer:
    still to do

## print to console <essay>
question: |
    Write a lox program which draws a triangle to the console.  The first line must be
    <pre>
    |    var size = 6
    </pre>
    and the `size` variable must be used to determine the number of characters on the longest side.  For example, `size` of 6 prints out
    <pre>
    |    ******
    |    *****
    |    ****
    |    ***
    |    **
    |    *
    </pre>
answer:
    still to do


# SSE

## from book tiny <essay>
question:
    Lox is a pretty tiny language. What features do you think it is missing that would make it annoying to use for real programs? (Aside from the standard library, of course.)
answer:
    still to do

## square
Write a lox program to print the first 50 square numbers that uses no loops at all.{}

## prime
Write a lox program to print the first 50 prime numbers that uses no loops at all.{}

## function <essay>
question: 
  Write a lox function `foo` which will take in a parameter and return triple that value
answer: |
  `````
  def foo(val){
      return val*3;
  }
  `````


## repeat <essay>
question:
  Write a lox function `repeat` which will take in two parameters.  The first is a string and the second is a number (n).  The function should return the character repeated n times.
answer: |
  `````
  fun repeat(char, times){
      if (times == 0){
          return "";
      }
      return (char + repeat(char, times-1));
  }
  `````
## simple function <essay>
question:
    Write a lox function which takes in a number and returns double that number
answer:
    <pre>
    fun double(a) {
        return a + a;
    }
    </pre>
    I was tricky and used `+`. in little languages like lox, never assume the operator you want is there (though `*` is there :) )

## print to console <essay>
question: |
    Write a lox program which draws a triangle to the console without using any loops!  The first line must be
    <pre>
    |    var size = 6
    </pre>
    and the `size` variable must be used to determine the number of characters on the longest side.  For example, `size` of 6 prints out
    <pre>
    |    ******
    |    *****
    |    ****
    |    ***
    |    **
    |    *
    </pre>
    Tip: recursion is your friend
answer:
    still to do


# RAT
## types of inheritance <gift>
Which of the following approaches to OO language design did the text book author choose for Lox? _Note you may recieve negative marks for picking a wrong option_.{
  =50%classes
  =50%prototyps
  ~-33%objects
  ~-33%sharing
  ~-33%inheritance
}

# SSE

## from book informal <essay>
question:
    This informal introduction leaves a lot unspecified. List several open questions you have about the language’s syntax and semantics. What do you think the answers should be?
answer:
    still to do


## your reason <essay>
question: |
    Give _your reason_ for wanting to have OO in your language.  If you hate OO, put yourself in someone else's shoes and think of _their_ reason.  OO is good enough that you can come up with _something!_.
answer:
    still to do

# Exam

## differences <essay>
question: |
    Describe two differences between the syntax of Java and the syntax of Lox as described in the book "Crafting Interpreters".   Be precise with your terms and explain the differences in some detail for full marks.
answer: |
    There are many you could point out, here are the two I have chosen.  Lox used the `fun` keyword to introduce a function definition while Java uses the return type followed by function name and parameters.  I realise Java actually relies on the full signature which I guess is a tougher parsing job than Lox has - it just sees `fun` and knows to parse a function definition.  Lox also has no real standard library whereas Java has a substantial runtime.  Lox supports just a `print` function and the run-time is compiled into every program. In Java the run-time is distributed separately in the JDK and not included in the compiled program.