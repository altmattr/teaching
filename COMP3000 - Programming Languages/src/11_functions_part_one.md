## Week Overview

This week we turn our focus to functions. Lox has first-class functions, so we spend some time thinking about these specifically.

## Goals

By the end of this week you should:

  * Be comfortable with the idea of expressions which evaluate to a function instead of values (or does that mean a function is a value?)
  * Be able to write Lox programs using these first-class functions
  * Have improved your Lox interpreter so it can evaluate calls to built-in functions

## Preparation

  * Read Chapter 10 of "Crafting Interpreters" up to section 10.3
  * Watch the following videos on echo360
    - Parsing function calls
    - Implementation mechanics
    - Functions as values

NB: function definitions is left until next week.

# RAT

## Handling Nested Functions <gift>
When parsing nested functions in Lox, how does the parser correctly manage scope and function boundaries? 
{
    ~It tracks function boundaries by resetting the parser state entirely for each nested function.
    =It uses recursion to parse nested function declarations, maintaining separate scopes for each.
    ~It parses nested functions in a single pass, merging their scopes into the parent function's scope.
    ~It prohibits nested functions in Lox to avoid scope management complexity.
}

## Error Recovery During Function Parsing <gift>
What strategy does the Lox parser use to recover from a syntax error encountered while parsing a function body? 
{
    ~It skips directly to the next top-level declaration, ignoring the rest of the function.
    ~It terminates parsing entirely until the error is manually corrected.
    =It synchronizes by skipping tokens until it finds the next statement boundary or closing brace.
    ~It rewinds to the beginning of the function and retries parsing using a fallback mechanism.
}

## anon church 1 <gift>
Given the following lox program, what is the output if the last line is replaced with `print(foo(bat)(0));`

<pre>
fun foo(z)\{
    fun lam(x)\{
        return x;
    \}
    return lam;
\}

fun bar(z)\{
    fun lam(x)\{
        return z(x);
    \}
    return lam;
\}

fun bat(x)\{
    return x+1;
\}

fun baz(m)\{
    fun lam1(n)\{
        fun lam2(f)\{
            fun lam3(x)\{
                return m(f)(n(f)(x));
            \}
            return lam3;
        \}
        return lam2;
    \}
    return lam1;
\}

print("last line");
</pre>
{
    =0
    ~1
    ~2
    ~a run time error
    ~"<native fn>"
}

## callable function 1 <gift>
What is the output of the following program if the last line is replaced with `print(functionOne(1));`

<pre>
fun functionOne(val)\{
    fun otherFunction(otherVal)\{
        print(val + otherVal);
    \}
\}

print("last line");
</pre>
{
    =nil
    ~1
    ~2
    ~error
}

## anon church 3 <gift>
Given the following lox program, what is the ouput if the last line is replaced with `print(baz(foo)(bar)(bat)(1));`

`````
fun foo(z)\{
    fun lam(x)\{
        return x;
    \}
    return lam;
\}

fun bar(z)\{
    fun lam(x)\{
        return z(x);
    \}
    return lam;
\}

fun bat(x)\{
    return x+1;
\}

fun baz(m)\{
    fun lam1(n)\{
        fun lam2(f)\{
            fun lam3(x)\{
                return m(f)(n(f)(x));
            \}
            return lam3;
        \}
        return lam2;
    \}
    return lam1;
\}

print("last line");
`````
{
    ~0
    ~1
    =2
    ~a run time error
    ~"<native fn>"
}

## anon church again <gift>
Given the following lox program, what is the output if the last line is replaced with `print(baz(foo)(bar)(bat)(0));`
<
`````
fun foo(z)\{
    fun lam(x)\{
        return x;
    \}
    return lam;
\}

fun bar(z)\{
    fun lam(x)\{
        return z(x);
    \}
    return lam;
\}

fun bat(x)\{
    return x+1;
\}

fun baz(m)\{
    fun lam1(n)\{
        fun lam2(f)\{
            fun lam3(x)\{
                return m(f)(n(f)(x));
            \}
            return lam3;
        \}
        return lam2;
    \}
    return lam1;
\}

print("last line");
`````
{
    ~0
    =1
    ~2
    ~a run time error
    ~"<native fn>"
}

# Assignment Two

## Evaluation and Dams <tex-essay>
question: |
    Your task in this assignment is to add \emph{evaluation} and \emph{dams} to your language.

    \subsubsection*{Evaluation}
    Assignment one left off with an expression language.  Many of you added statements because it really made sense.  From this starting point you should add evaluation for your expression langauge.  Evaluation means implementing an interpreter which evaluates expressions to some value. The value may be a single number or a sequence of numbers or anything else that makes sense for your language.  You should ensure this value is output in some way so your marker can see it.  We have set two levels of achievement in the rubric depending on the capabilities of your interpreter.  You will almost certainly need to add statements and variables to achieve these things and we have provided an example solution for these in the exemplar.
    
    Explanation vids have been provided for each rubric item to show you an example of what this can look like.

    \subsubsection*{Dams}
    Dams are human controlled flow adjustment mechanisms.  Sometime they allow all the flow through, sometimes they increase the flow, sometimes they stop or reduce the flow.  Your tasks is to add a syntax and evaluation for dams into your langauge.  The rubric specifies what grades will be given for different levels of achievement in this item.

    Explanation vids have been provided for each rubric item to show you an example of what this can look like.

    \subsubsection*{The output of a program}
    If you take a look at the rubric quiz, you will see examples of how our example solution outputs values after a program runs.  You have some flexibility here but we suggest the following:
    \begin{enumerate}
    \item either your language includes a print statement \emph{and} your example programs use it, or
    \item your interpreter outputs something by default that will help your marker.
    \end{enumerate}
    In my example solution I output the value of every variable at the end of the program, this proved very helpful in debugging and showing off what my example programs were doing.  It would not work for large programs, but we don't need large programs for this submission.

    \subsubsection*{The input to the program}
    My example language does the computation assuming 1mm of rainfall.  You are free to do what works for you but be sure to communicate clearly to your marker for each example program.  Good options are:
    \begin{itemize}
    \item The language has a statement that sets the rainfall for the program execution
    \item The rainfall is given as an argument to the program running script
    \item The interpreter has some default rainfall built-in.  This is what mine did with a default of 1mm.
    \end{enumerate}



    \subsubsection*{Starting Point}
    We recommend you build your assignment submission from your team's work or from your own work that you have been doing in workshops.  If you worry that is not a good starting point or you struggled in assignment one, you can start from our published solution which is provided on iLearn (which we will call the exemplar).  This exemplar is a reasonable answer to assignment one which you are free to build off.

    \subsubsection*{The Structure of your submission}
    You will submit two things - both of which are iLearn items available in the "Assessemnts" section:
    \begin{itemize}
    \item A zip file containing your interpreter and example programs\\ (url is \verb+https://ilearn.mq.edu.au/mod/assign/view.php?id=8940558)
    \item A completed quiz with instructions for your marker\\ (url is  \verb+https://ilearn.mq.edu.au/mod/quiz/view.php?id=8997793+)
    \end{itemize}

    You should structure your zip in the same way as the exemplar zip is structured.  That is there should be two directories, one for the code in your language (in the exemplar this directory is  called \verb+lox+) and one for the java source (in the exemplar this directory called \verb+exemplar+ because that is the package name).  See figure \ref{fig:example}.  As well, please include a compile script and a run script which show how to compile and run your program.  If possible, these should be scripts which can be run by your marker - the scripts in the exemplar will guide you and should work on most operating systems.  If you must diverge from this setup, you can put build and run instructions in \emph{each} of your answers in the quiz.

    \begin{figure}
    \includegraphics{src/11_example.png}
    \caption{Example zip file structure}
    \label{fig:example}
    \end{figure}

    \subsubsection*{A quiz instead of a document}
    In this submission you will use a quiz, linked from the iLearn page, to explain how your language works.  There is one question for each rubric item and you can use the text box to explain how you meet or achieve that rubric item and give any help your marker might need to compile, run, and understand your language.  Your grades and feedback will be given directly via that quiz.  Each question includes a linked video where we show \emph{our solution in action} as a guide for you in putting together your own solution.  You don't need to follow these but it provides one option you can follow if you like.

    The quiz is your chance to explain your decisions and implementation to your marker, writing clear and concise answers will help your marker award you grades.  For example, your marker won't know how dams work in your language unless you tell them so you can't get dam marks unless you clearly describe that in your quiz answer.  If your intention is not clear from the answers you submit, you won't be awarded grades, even for work that is ultimately correct.  It is your responsibility to communicate clearly everything your marker needs in your quiz answer.  Your marker will be one of the class teachers, so you can assume they are familiar with anything from class.  I.e. there is no need to explain any class concepts.

    We recommend you point your marker to the example program you submitted which demonstrates this rubric item as the simplest way to demonstrate you have achieved it.

    The quiz has no time limit and multiple attempts are allowed so you can update/adjust your answers right up to the due date.

    \subsubsection*{Use of Generative AI}
    An ability to use Generative AI is not a learning outcome of this course but GenAI is a tool you may choose to use along your journey.  If your submission is primarily AI generated, you will likely find yourself in the bottom of each rubric item.  Lox and Nystrom's notation are not well represented in AI training sets and Gen AIs are generally bad at language design.  We value, and give grades for, your contribution to the solution since it is you (not the GenAI vendor) who is earning the grade.

    \subsubsection*{Rubric}
    The rubric has a total of 12 marks which are scaled up to the 25\% of the assignment constribution to your final mark.

    \begin{tabular}{p{0.7\textwidth}|r}
    functionality & max marks for this item \\
    \hline
    Your language must be able to interpret an expression which describes simple river flows.  The interpreter must output something when it is finished indicating at least one of the flows in the system.  We recommend outputting all named flows, but you could have a special output expression in which case you will output just that expression. & 2 \\ \hline
    Your language can model the flow over multiple days and the output of your interpreter shows the predicted flows on all those days.  As with the last item, you may output just one flow, or all named flows, or whatever makes most sense for your language. & 2 \\ \hline
    Your language has a syntax to support dams.  Dams don't always let all or none of the flow through, they run some "algorithm" to decide how much flow to let through.  Provide example programs demonstrating your dam syntax and your parser can successfully parse those programs.  Your marker may write their own program so please include a full grammar here. & 2 \\ \hline
    The interpreter can run the dam's algorithm accurately and downstream river flows reflect its behaviour. & 2 \\ \hline
    The output from a dam can depend on at least two of the following: the flow into the dam, today's rain, the dam level. You may add others if you like. & 2 \\ \hline
    How well does this language express the underlying concepts.  I.e. have you chosen sensible keywords and syntax structures and have your implemented an interesting language overall.  & 1 \\ \hline
    Uniqueness and creativity.  You can present your work in the week 13 class to guarantee full marks for this rubric item & 1 \\ \hline
    \end{tabular}
    Note the quiz (which you can view any time) does expand upon these rubric descritions to aid in your submission.

    \newpage
answer: |
  None provided

# FAT

## dam semantics <tex-essay>
question: |
    Dams are human-controlled things.  A water manager can decide to let water out depending on the circumstances.  In fact, water managers will have a kind of "algorithm" they apply to help them make that decision consistently. 
    
    In a water management language, that "algorithm" would be expressed as a block of code with some input parameters and some output value.

    With a water management language we can experiment with different dam management algorithms to see how they will affect water flow.

    This week we would like your team to demonstrate \emph{three versions of the same dam} implemented in your language.  For example, if we were defining Googong dam I would like at least the following versions written in your language (in separate source files):\begin{itemize}
    \item Googong dam blocks exactly half the water that flows into it.
    \item Googong dam blocks exactly half the water that flows into it unless the rain that day was greater than 10mm.
    \item Googong dam blocks half the water that flows into it unless the flow into it is greater than 10L/s, in which case it blocks 75% of the flow.
    \end{itemize}

    Because the flow out of a dam depends on the flow into the dam, we suggest a function-like syntax will be most appropriate.  You will also need a way to find out today's rainfall which has so-far been implicit.  When you wrote your evaluator, you probably made some decision about how ti would appear - you may need to adjust that now.

    Once you have these three sorted, explore what other things you would want to represent in your language and how you will go about doing it.

    Your output for this week should be multiple code files in your language, each describing a different dam management choice.

    \begin{note}
    This task will be part of assignment two, but you will need to extend it to get full marks so take this opportunity to brainstorm ideas with your team-mates
    \end{note}

# SSE

## trace a lox program <essay>
question: |
    Trace the execution of the following Lox program to explain how "there" appears on the console
    ```
    fun foo(i){
        if (i == 0){
            fun ret(){
                return "hi";
            }
            return ret;
        }
        if (i == 1){
            fun ret(){
                return "there";
            }
            return ret;
        } else {
            fun ret(){
                return "mate";
            }
            return ret;
        }
    }
    print(foo(1)());
    ```
answer: |
    The first 27 lines are a definition and don't "run". The final line is the program.  It is a call to `print` whose sole paramter is `foo(1)()`.  Just from the syntax we know that `foo` is a function because it has parenthesis after it.  We also know that `foo(1)` must also be a function because _that_ has parenthesis after it as well.  If we call `foo(1)` we see that line 10 is false but line 16 is true, thus the following code is the body of `foo(1)`
    ```
    fun ret(){
        return "there";
    }
    return ret;
    ```
    Just like any other return statement, the result of the body is thus `ret`.  But what is `ret`?  It is a function definition - which is something we can call by adding parenthesis to it!  This is perfect, because that is exactly what we are doing.  It's a bit like the program has now evaluated to
    ```
    fun ret(){
        return "there";
    }
    print(ret());
    ```
    Which we can easily see will print "there" to the console.

## church <essay>
question: |
    Trace the execution of the following lox program to work out what it outputs.  I strongly suggest you make sure you know this answer very well\footnote{The end of semester exam really likes this lox program}.
    `````
    fun zero(z){
        fun lam(x){
            return x;
        }
        return lam;
    }

    fun one(z){
        fun lam(x){
            return z(x);
        }
        return lam;
    }

    fun incr(x){
        return x+1;
    }

    fun plus(m){
        fun lam1(n){
            fun lam2(f){
                fun lam3(x){
                    return m(f)(n(f)(x));
                }
                return lam3;
            }
            return lam2;
        }
        return lam1;
    }

    print(zero(incr)(0));
    print(one(incr)(0));
    print(plus(zero)(one)(incr)(0));
    `````
answer: |
    The answer is 
    ```
    0
    1
    1
    ```
    but the important question is why?  Let's trace the evaluation of `zero(incr)(0)` as an example.  Note that I am making up my own notation for this trace.  Green is the step number, black is the expression, orange is notes on the function call.
    <img width="100%" src="11_zero_trace.jpeg"/>

## add a new global function <essay>
question: |
    I've been annoyed by this `print` operation all semester.  It always puts a new line and there are heaps of times I don't want one! Add a global function called `printonly` which will print the string it is given without adding a new line.
answer: |
    I've found a fun way to make a modified interpreter.  I've had to get rid of all the `private` modifiers in my interpreter, but once I do, I can define a modified lox interpreter by subclassing the existing classes.  Here is how I did it in this case
    `````
    package weeks.ten;


    import java.util.List;

    public class LoxPlusPrintOnly extends Lox{
        public static void main(String[] args){
            new LoxPlusPrintOnly().run("var x = 0; printonly(x);");
            new LoxPlusPrintOnly().run("var x = 100; printonly(\"you are \"); printonly(x); print(\" years old!\");");
        }

        void run(String source){
            List<Token> tokens = new AdjustedScanner(source).scanTokens();
            System.out.println("-- tokens --");
            for(Token t: tokens){
            System.out.println(t);
            }
            List<Stmt> ast = new AdjustedParser(tokens).parse();
            System.out.println("-- ast --");
            for(Stmt s: ast){
            System.out.println(s);
            }
            new AdjustedInterpreter().interpret(ast);
        }

        private class AdjustedScanner extends Scanner{
            AdjustedScanner(String source){super(source);}
        }
        private class AdjustedParser extends Parser{
            AdjustedParser(List<Token> tokens){super(tokens);}
        }

        private class AdjustedInterpreter extends Interpreter{
            AdjustedInterpreter(){
                super();
                globals.define("printonly", new LoxCallable(){
                    @Override
                    public int arity(){return 1;}
                    @Override
                    public Object call(Interpreter interpreter, List<Object> arguments){
                        System.out.print(stringify(arguments.get(0)));
                        return null;
                    }
                    @Override
                    public String toString(){return "<native fn>";}
                });
            }
        }
    }
    `````
    Add this to your week 11 package and prove you can make it work too.


# Exam

## anon church 2 <gift>
Given the following lox program, what is the output if the last line is replaced with `print(one(bat)(0));`

`````
fun foo(z)\{
    fun lam(x)\{
        return x;
    }
    return lam;
}

fun bar(z)\{
    fun lam(x)\{
        return z(x);
    }
    return lam;
}

fun bat(x)\{
    return x+1;
}

fun baz(m)\{
    fun lam1(n)\{
        fun lam2(f)\{
            fun lam3(x)\{
                return m(f)(n(f)(x));
            }
            return lam3;
        }
        return lam2;
    }
    return lam1;
}

print("last line");
`````
{
    ~0
    =1
    ~2
    ~a run time error
    ~"<native fn>"
}

## callable function 2 <gift>
What is the output of the following program if the last line is replaced with `print(functionOne(1)(1));`
`````
fun functionOne(val)\{
    fun otherFunction(otherVal)\{
        print(val + otherVal);
    }
}

print("last line");
`````
{
    ~nil
    ~1
    =2
    ~error
}

## basic parser <gift>
What is the correct sequence of steps to parse a function header in Lox? 
{
    =Parse the function name, then the parameter list, followed by a block for the body.
    ~Parse the function name, then the return type, followed by the block for the body.
    ~Parse the parameter list, then the function name, followed by a block for the body.
    ~Parse the block for the body first, then the function name, followed by the parameter list.
}