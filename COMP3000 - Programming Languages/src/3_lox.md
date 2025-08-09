  
##  WEEK OVERVIEW

This week we turn our focus to the Lox programming language, which we will implement over the rest of the semester. 

## GOALS

By the end of this week you should:
  * Be able to program in Lox
  * Understand some basic Lox design decisions

## Preparation
  * Read chapter 3 of "Crafting Interpreters" (the Lox book).
  * Watch lox lectures on echo360:
    - High level features, types, expressions, and statements.
    - Functions and OO features
    - Lox live coding session
  * Ensure you have a working lox implementation on your computer.
  * Experiment with lox programs.

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
answer: |
    I'm going to start with a lox program that outputs the string "fd 10" which is the logo program for going forward 10 units.
    \begin{lstlisting}
    print "fd 10"
    \end{lstlisting}

    Ok, that was simple.  The program for the star is
    \begin{lstlisting}
    fd 100
    rt 144
    fd 100
    rt 144
    fd 100
    rt 144
    fd 100
    rt 144
    fd 100
    \end{lstlisting}

    So the following lox program will generate this program, but in an unsatisfactory way
    \begin{lstlisting}
    print "fd 100";
    print "rt 144";
    print "fd 100";
    print "rt 144";
    print "fd 100";
    print "rt 144";
    print "fd 100";
    print "rt 144";
    print "fd 100";
    \end{lstlisting}

    But we can do way better than that because lox can do the looping for you

    \begin{lstlisting}
    for (var i = 1; i < 5; i = i + 1) {
      print "fd 100";
      print "rt 144";
    }
    \end{lstlisting}
    
    That version spits out an extra right turn, but that doesn't break the image.   I could get tricker to remove it if I wanted.  To do the dotted line version, I need another "pen up/pen down" look during the `fd 100`.

    \begin{lstlisting}
    for (var i = 0; i < 5; i = i + 1) {
        for (var j = 0; j < 100; j = j + 20) {
            print "pd";
            print "fd 10";
            print "pu";
            print "fd 10";
        }
        print "rt 144";
    }    
    \end{lstlisting}

    Testing all this requires a lox implementation, which was given in iLearn.  I stored my lox program for this in `lox/turtle` and I can run lox programs with this command (I also put my `lox.jar` in that same place).  The output program is really long, so I couldn't easily grab it from my console output. Instead I sent the output to a file that I could copy from later.

    \begin{lstlisting}
    java -jar lox/lox.jar lox/turtle/main.lox > lox/turtle/main.out
    \end{lstlisting}

    I then have to take the output from that and pop it in the turtle graphics program to see the output, but it works!

    \includegraphics[width=0.5\textwidth]{src/3_dotted.png}

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

## types of inheritance <gift>
Which of the following approaches to OO language design did the text book author choose for Lox? _Note you may recieve negative marks for picking a wrong option_.{
  =50%classes
  =50%prototyps
  ~-33%objects
  ~-33%sharing
  ~-33%inheritance
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


## square <essay>
question:
    Write a lox program to print the first 50 square numbers.
answer: |
    `````
    for (var i = 0; i < 50; i = i + 1){
        print (i * i);
    }
    `````

## print to console <essay>
question: |
    Write a lox program which draws a triangle to the console.  The first line must be
    `````
    |    var size = 6
    `````
    and the `size` variable must be used to determine the number of characters on the longest side.  For example, `size` of 6 prints out
    `````
    |    ******
    |    *****
    |    ****
    |    ***
    |    **
    |    *
    `````
answer: |
    This is not as easy as we would like to think.  Lox has no way to print a string without printing a newline right after it!  This is one example where having a tiny run-time (or none at all) is a problem.  In this case though we can get around it by building up the string before printing the whole line.
    `````
    var size = 6;

    fun line(len){
        if (len == 0){
            return "";
        } else {
            return ("*" + line(len-1));
        }
    }

    for(var i = size; i > 0; i = i -1){
        print(line(i));
    }
    `````

## from book tiny <essay>
question:
    Lox is a pretty tiny language. What features do you think it is missing that would make it annoying to use for real programs? (Aside from the standard library, of course.)
answer:
    I actually really like tiny languages.  There are less things to remember.  That said, I love switch statements and Lox has none, so I would have to do big long `if` statements with lots of `else if` and I really don't like that.  The functional features help a lot though, without them I think I would have much more to complain about.

## square recursion <essay>
question: |
    Write a lox program to print the first 50 square numbers that uses no loops at all.
answer: |
    `````
    fun square(i){
        if (i > 50){
            return;
        }
        print(i * i);
        square(i+1);
    }

    square(0);
    `````

## triple <essay>
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
## double <essay>
question:
    Write a lox function which takes in a number and returns double that number
answer: |
    `````
    fun double(a) {
        return a + a;
    }
    `````
    I was tricky and used `+`. in little languages like lox, never assume the operator you want is there (though `*` is there :) 

## triangle recursion <essay>
question: |
    Write a lox program which draws a triangle to the console without using any loops!  The first line must be
    `````
    |    var size = 6
    `````
    and the `size` variable must be used to determine the number of characters on the longest side.  For example, `size` of 6 prints out
    `````
    |    ******
    |    *****
    |    ****
    |    ***
    |    **
    |    *
    `````
    Tip: recursion is your friend
answer: |
    ```
    var size = 6;

    fun line(len){
        if (len == 0){
            return "";
        } else {
            return ("*" + line(len-1));
        }
    }

    fun tri(width){
        if (width == 0){
            return;
        } else {
            print(line(width));
            tri(width-1);
        }
    }

    tri(size);
    ```

## your reason <essay>
question: |
    Give _your reason_ for wanting to have OO in your language.  If you hate OO, put yourself in someone else's shoes and think of _their_ reason.  OO is good enough that you can come up with _something!_.
answer: |
    It is just much easier to think of functions being _attached_ to the data they work on.  It is a form of intellectual discipline that pays off after a while.  When the program is small though, you probably don't need that discipline and thus people tend not to feel the need for OO in scripting languages.

# Exam

## differences <essay>
question: |
    Describe two differences between the syntax of Java and the syntax of Lox as described in the book "Crafting Interpreters".   Be precise with your terms and explain the differences in some detail for full marks.
answer: |
    There are many you could point out, here are the two I have chosen.  Lox used the `fun` keyword to introduce a function definition while Java uses the return type followed by function name and parameters.  I realise Java actually relies on the full signature which I guess is a tougher parsing job than Lox has - it just sees `fun` and knows to parse a function definition.  Lox also has no real standard library whereas Java has a substantial runtime.  Lox supports just a `print` function and the run-time is compiled into every program. In Java the run-time is distributed separately in the JDK and not included in the compiled program.