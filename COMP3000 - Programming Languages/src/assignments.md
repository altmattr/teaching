
Over the semester, you will be creating a programming language to \emph{model} and \emph{simulate} water flows in river systems.  This project is the central thread of COMP3000: everything you learn about scanning, parsing, representing code, and evaluating programs will be applied to building a real domain-specific language.

Modelling rivers involves taking rainfall data and simulating what water levels result from that rainfall over a period of time.  This type of modelling is vital to environmental management and public safety --- floods can be predicted, mitigation methods designed, and water managers can experiment with different dam strategies to maximise safety.  River system modelling is normally done with general-purpose simulation software, but it could be done better with a \emph{custom programming language} designed specifically for the domain.

Your task is to build that language.  Starting from the Lox interpreter you develop through the textbook, you will extend and adapt it into a language capable of describing river systems, computing flows over multiple days, and simulating the behaviour of human-controlled dams.  You are not being pushed towards a single solution --- you are exploring possibilities and making design decisions as language designers.

The project has two submission points:

\begin{description}
\item[Submission One:] A parser for your water flow language.  You will design a grammar capable of representing river systems and implement a Lox-style parser for it.  You will also produce three example programs and a document explaining your language and parser.
\item[Submission Two:] An interpreter for your language.  Building on your parser, you will add evaluation so that programs in your language produce meaningful output --- the predicted flows in a river system over time.  You will also add support for dams, which allow human-controlled adjustment of water flows.
\end{description}

Each submission is graded against a rubric that rewards both technical achievement and the quality of your language design.  You are free to build on your team's workshop work, but each submission must be your own.  Uniqueness and creativity are rewarded --- the best submissions will be those that go beyond what was done in class.

## The Exemplar <tex-essay>
question: |
    A worked example of a complete river system language is available on iLearn.  We call this the exemplar.  It is one possible design.  Your language will be different.  That's the point.

    The exemplar README describes the language in detail: its syntax, semantics, design decisions, and possible extensions.

    \subsubsection*{The Domain}

    We wish to develop a domain specific language for the \emph{modelling} and \emph{simulation} of water flows in river systems.  A river system is a series of rivers.  Each river is either 
    \begin{enumerate}
    \item A root river or 
    \item The combination of the output of multiple other rivers or
    \item The last river in the system is identified as the \emph{output river}.
    \end{enumerate}
    A \emph{river system} is a series of connected rivers.  Your domain specific language must be capable of representing a river system.  Executing a program in this domain specific language will compute the flows in every river at each day given a certain rainfall.  For now you can ignore the complication of representing the rainfall and focus on a language which is capable of describing the river itself.

    \subsubsection*{An Example}

    You are free to build your examples from any real or imagined river system.  Here we describe one example river system which makes a relatively easy example to show off all the features of your language which you can choose to use.

    \begin{figure}
    \includegraphics[width=0.588\textwidth]{src/6_simplified_act.jpg}
    \includegraphics[width=0.512\textwidth]{src/6_situated_act.jpg}
    \caption{An example river system.  On the left is a stylised map and on the right is all the draining rivers and dams on a map to help situate the river system.}
    \label{fig:act_watershed}
    \end{figure}

    Figure \ref{fig:act_watershed} shows a river system situated near Canberra.   The following statements are true of this river system:
    \begin{itemize}
    \item The root rivers in this system are googong, jerrabombarra, and upper molongolo.  
    \item Googong drains to dam 1
    \item Dam 1 drains to queanbeyan
    \item Central molongolo is the combination of queanbeyan, upper molongolo, and jerrabombarra
    \item Central molongolo drains to dam 2
    \item Dam 2 drains to lower molongolo\footnote{FYI: Dam 2 dams lake Burly Griffith in Canberra, you may have been there!}
    \item The output of the entire river system is the output of lower molongolo
    \end{itemize}

    We make the following simplifying assumptions:
    \begin{enumerate}
    \item The rainfall across a whole \emph{river system} can be described with one number (in mm).
    \item The rainfall across the whole river system is provided at run time by "magic".  I.e. we can just assume for now that such a number exists and can be accessed.
    \item The flow into one river is the sum of the flows out of its feeding rivers.
    \item The flow out of a river is the flow in plus the water that has made it way into the river on that day.
    \item All water that gets into a river will also flow out of it.
    \item All water that falls from the sky will (within 10 days) make its way into the river.
    \item The outflow of a dam is exactly the inflow to the dam\footnote{We will relax this assumption later and have great fun controlling water flow with dams}.
    \item Rivers never split into two or more rivers.
    \end{enumerate}

    \subsubsection*{Language Features in the Exemplar}

    The exemplar models a river system as a network of creeks and dams.  Here are the key features:

    \emph{Flow literals} describe how water flows past a point over 10 days:
    \begin{verbatim}
    var joes = [1 ~ 1]@4;
    \end{verbatim}
    The three numbers are start day, spread (decay rate), and magnitude (total volume).

    \emph{Combining flows} uses the \verb=+= operator, which adds element-wise:
    \begin{verbatim}
    var result = joes + mahers;
    \end{verbatim}

    \emph{Dams} are declared with \verb=dam= and use \verb=when= rules to decide how much flow to release:
    \begin{verbatim}
    dam smart_dam {
      when level > 100: inflow + inflow;
      when level < 2: [1~1]@0;
      default: [1~10]@2;
    }
    \end{verbatim}
    The keyword \verb=inflow= refers to today's incoming flow.  The keyword \verb=level= refers to the dam's accumulated water level, which starts at zero and increases by inflow minus outflow each day.  Rules are checked in order; the first matching rule determines the output.

    \emph{The \texttt{<=} operator} connects a dam to its upstream source:
    \begin{verbatim}
    var joes_creek = lower_joes_creek <- (upper_joes + mahers);
    \end{verbatim}
    For flows, \verb=<-= delays the upstream flow by one day and adds it to the downstream flow.  For dams, \verb=<-= applies the dam to the upstream flow.

    \subsubsection*{Design Rationale}

    The exemplar makes several deliberate design choices:
    \begin{itemize}
    \item \emph{10-day window with geometric decay.}  Water arrives on a start day and decays at a constant fraction each day.
    \item \emph{Dams as functions.}  A dam takes an upstream flow and returns a transformed flow.  The \verb=when= syntax is syntactic sugar for if/else in the dam body.
    \item \emph{Level computed locally.}  Each dam tracks its own water level as it processes the 10-day array day by day.
    \item \emph{Rainfall is external.}  The language describes river structure, not rainfall data.
    \end{itemize}

    The exemplar README explains each of these decisions in detail, along with possible extensions such as dam behaviours as functions, external rainfall input, multiple rainfall events, and real-time simulation.
answer: |
  None provided

# Submission One

## Specification <tex-essay>
question: |
    Your task is to create
    \begin{itemize} 
    \item a Lox-style\footnote{Please don't start a custom parser/interpreter from scratch or use any language other than Java as your implementation language.  Your marker will need to be familiar with the basics of your approach - assume they are \emph{only} familiar with the Lox parser.} parser for programs simulating water flows, 
    \item three example programs, 
    \item and a document explaining your language and parser.
    \end{itemize}

    The document is your chance to explain your decisions and implementation to your marker, writing a good one will help your marker give you grades for the other files as well.  For example, your marker won't know how to compile your parser unless you tell them so you can't get parser marks unless you clearly describe that in your document.  If your intention is not clear from the documents you submit, you won't be allocated grades, even for work that is ultimately correct.  It is your responsibility to communicate clearly everything your marker needs in your submission.  Your marker will be one of the class teachers, so you can assume they are familiar with anything from class.

    \begin{note}
    There is ambiguity left in this description by design.  You are aiming to make \emph{the best possible domain specific language for waterflows} but we clarify a great deal to support grading your work.  Imagination is needed to complete this task and experimentation is strongly encouraged.
    \end{note}

    \subsubsection*{Table A}
    To get you started, 20\% of your marks are available just for completing the following table and including it in your document.  It will help your markers follow along with your explanations.

    \begin{tabular}{|p{0.5\textwidth}|p{0.3\textwidth}|}
    \hline
    What literal in your language represents a river that gets 10L/s of flow on the first day after 1mm of rainfall? & \\ \hline
    What symbol in your language is used to show two rivers combine? & \\ \hline
    Is the above symbol a "unary", "binary", or "literal"? & \\ \hline
    What folder is the "working folder" to compile your parser? & \\ \hline
    What command(s) will compile your parser? & \\ \hline
    In your language, how long does it take all the water to work through a river system after 1 day of rain? & \\ \hline
    Does your language include statements or is it an expression language? & \\ \hline
    Which chapter of the book have you used as the starting point for your solution? & \\ \hline
    \end{tabular}

    \subsubsection*{Use of Generative AI}
    An ability to use Generative AI is not a learning outcome of this course but GenAI is a tool you may choose to use along your journey.  If your submission is primarily AI generated, you will likely find yourself in the bottom of each rubric item.  Lox and Nystrom's notation are not well represented in AI training sets and Gen AIs are generally bad at language design.  We value, and give grades for, your contribution to the solution since it is you (not the GenAI vendor) who is earning the grade.

    \begin{note}
    You are free to use any and everything from your team's work on this task.  You may not use other team's work directly or solicit for solutions.  These remain contraventions of academic integrity.  The work of the team belongs to all team members, so they can submit that without contravening academic integrity.  However, this is your own submission.  You can, and should, improve upon your team's work as much as possible.  We have included a "similarity/creativity" score in the rubric so we can reward solutions that go beyond what was done in class.  Note that \emph{the document must be your own work}.  It can heavily reference the team's work, but you should write it from scratch yourself.

    You are also free to use any of the example solutions given by unit staff without referencing them.
    \end{note}
    \subsubsection*{Rubric}
    \begin{tabular}{|p{0.18\textwidth}|p{0.18\textwidth}|p{0.18\textwidth}|p{0.18\textwidth}|p{0.18\textwidth}|}
    \hline
    \textbf{Rubric item} & Fail (0) & Pass (50) & Credit (70) & Distinction (100) \\
    \hline
    Complete Table A (10\%) & None answers accurately & 2 or more answered accurately & 6 or more answered accurately & All answered accurately \\ \hline
    Log-book submissions (10\%) & No logbook submitted or no entries & Some entries but inconsistent across the semester & Regular entries throughout the semester, seen by teacher & Complete, timely entries throughout the semester, seen by teacher \\ \hline
    Grammar given in the document in Nystrom's notation (20\%) & No grammar or substantially broken grammar in the document & A grammar with small errors & A grammar that can model rivers systems & A grammar that can model river systems and an explanation of how each example program parses according the grammar \\ \hline
    Three example programs (20\%) & No program or the programs don't model river system correctly & Three programs of some form & \emph{pass} and the example programs all match the given grammar & \emph{credit} and the Lox-like parser can actually parse the programs \\ \hline
    Parser written in Java based on Lox codebase (20\%) & None or not in Java & Code is based on the Lox from chapter 6 of text & Code is based on the Lox from chapter 6 and your additions fit with the style & If there is any improvement to the Chapter 6 Lox code with an explanation in the document, you will get this grade. \\ \hline
    Uniquness and Creativity (20\%) & A direct submission of in-class work & minor modifications to in-class work & substantial improvement on in-class work & a unique submission showing creativity \\
    \hline
    \end{tabular}
    \subsubsection*{Examples for Uniqueness Rubric}
    Below I give total contribution tot he final assignment grade for certain scenarios:
    \begin{description}
    \item[0\%] You have been working with your team all semester and you take the solutions your team came up with, add \emph{your own} document and submit it as-is.
    \item[14\%]  You have been working with your team all semester and they also met outside class hour to try out other things. You take the solutions your team came up with, add \emph{your own} document and submit it as-is.
    \item[20\%]  You have been working with your team all semester. You take the solutions your team came up with and make some adjustments of your own to make it even better.  You add \emph{your own} document and submit.
    \item[20\%] You have been the main person doing all the work for your team and you submit that work, with a document of your own.
    \item
    \end{description}
    \newpage
answer: |
     Still to do

# Submission Two

## Evaluation and Dams <tex-essay>
question: |
    Your task in this assignment is to add \emph{evaluation} and \emph{dams} to your language.

    \subsubsection*{Evaluation}
    Submission One left off with an expression language.  Many of you added statements because it really made sense.  From this starting point you should add evaluation for your expression language.  Evaluation means implementing an interpreter which evaluates expressions to some value. The value may be a single number or a sequence of numbers or anything else that makes sense for your language.  You should ensure this value is output in some way so your marker can see it.  We have set two levels of achievement in the rubric depending on the capabilities of your interpreter.  You will almost certainly need to add statements and variables to achieve these things and we have provided an example solution for these in the exemplar.
    
    Explanation vids have been provided for each rubric item to show you an example of what this can look like.

    \subsubsection*{Dams}
    Dams are human controlled flow adjustment mechanisms.  Sometime they allow all the flow through, sometimes they increase the flow, sometimes they stop or reduce the flow.  Your tasks is to add a syntax and evaluation for dams into your language.  The rubric specifies what grades will be given for different levels of achievement in this item.

    Explanation vids have been provided for each rubric item to show you an example of what this can look like.

    \subsubsection*{The output of a program}
    If you take a look at the rubric evidence document, you will see examples of how our example solution outputs values after a program runs.  You have some flexibility here but we suggest the following:
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
    \end{itemize}
    The \emph{catchment size} --- the area of land that drains into the river --- should also be user-definable; your marker will check for it.



    \subsubsection*{Starting Point}

    You may build your submission from your team's work, from the exemplar, or from your own work in workshops.  You are free to use your team's code, grammar, and design decisions as much as you like.  A worked example of a complete river system language (the exemplar) is described in the introduction to this document.

    \subsubsection*{The Structure of your submission}
    You will submit a single zip file (url is \verb+https://ilearn.mq.edu.au/mod/assign/view.php?id=8940558+) available in the "Assessments" section.  The zip should contain \emph{both}:
    \begin{itemize}
    \item your interpreter and example programs, and
    \item your completed rubric evidence document with instructions for your marker
    \end{itemize}

    You should structure your zip in the same way as the exemplar zip is structured.  That is there should be two directories, one for the code in your language (in the exemplar this directory is  called \verb+lox+) and one for the java source (in the exemplar this directory called \verb+exemplar+ because that is the package name).  See figure \ref{fig:example}.  As well, please include a compile script and a run script which show how to compile and run your program.  If possible, these should be scripts which can be run by your marker - the scripts in the exemplar will guide you and should work on most operating systems.  If you must diverge from this setup, you can put build and run instructions in your rubric evidence document.

    \begin{figure}
    \includegraphics{src/11_example.png}
    \caption{Example zip file structure}
    \label{fig:example}
    \end{figure}

    \subsubsection*{A rubric evidence document}
    As part of your submission you will complete a rubric evidence document and include it in your zip.  There is one section for each rubric item where you explain how you meet or achieve that rubric item and give any help your marker might need to compile, run, and understand your language.  Each section includes a linked video where we show \emph{our solution in action} as a guide for you in putting together your own solution.  You don't need to follow these but it provides one option you can follow if you like.

    The rubric evidence document is your chance to explain your decisions and implementation to your marker, writing clearly and concisely will help your marker award you grades.  For example, your marker won't know how dams work in your language unless you tell them so you can't get dam marks unless you clearly describe that in your rubric evidence document.  If your intention is not clear from your rubric evidence document, you won't be awarded grades, even for work that is ultimately correct.  It is your responsibility to communicate clearly everything your marker needs in your rubric evidence document.  Your marker will be one of the class teachers, so you can assume they are familiar with anything from class.  I.e. there is no need to explain any class concepts.

    We recommend you point your marker to the example program you submitted which demonstrates this rubric item as the simplest way to demonstrate you have achieved it.

    You can update and adjust your rubric evidence document right up to the due date.

    \subsubsection*{Use of Generative AI}
    An ability to use Generative AI is not a learning outcome of this course but GenAI is a tool you may choose to use along your journey.  If your submission is primarily AI generated, you will likely find yourself in the bottom of each rubric item.  Lox and Nystrom's notation are not well represented in AI training sets and Gen AIs are generally bad at language design.  We value, and give grades for, your contribution to the solution since it is you (not the GenAI vendor) who is earning the grade.

    \begin{note}
    You are free to use any and everything from your team's work on this task.  You may not use other team's work directly or solicit for solutions.  These remain contraventions of academic integrity.  The work of the team belongs to all team members, so they can submit that without contravening academic integrity.  However, this is your own submission.  You can, and should, improve upon your team's work as much as possible.  We have included a "similarity/creativity" score in the rubric so we can reward solutions that go beyond what was done in class.  Note that \emph{the document must be your own work}.  It can heavily reference the team's work, but you should write it from scratch yourself.

    You are also free to use any of the example solutions given by unit staff without referencing them.
    \end{note}

    \subsubsection*{Rubric}
    The rubric has a total of 16 marks which are scaled up to the 25\% of the assignment contribution to your final mark.

    \begin{tabular}{p{0.7\textwidth}|r}
    functionality & max marks for this item \\
    \hline
    Your language must be able to interpret an expression which describes simple river flows.  The interpreter must output something when it is finished indicating at least one of the flows in the system.  We recommend outputting all named flows, but you could have a special output expression in which case you will output just that expression.  \newline Rainfall and river catchment size should be user-definable. & 2 \\ \hline
    Your language can model the flow over multiple days and the output of your interpreter shows the predicted flows on all those days.  As with the last item, you may output just one flow, or all named flows, or whatever makes most sense for your language.  \newline Flows should carry over between days --- predicted flows depend on previous days' water, not just today's rainfall. & 2 \\ \hline
    Your language has a syntax to support dams.  Dams don't always let all or none of the flow through, they run some "algorithm" to decide how much flow to let through.  Provide example programs demonstrating your dam syntax and your parser can successfully parse those programs.  Your marker may write their own program so please include a full grammar here.  \newline Grammar should be complete and match your example programs, so the marker can write their own. & 2 \\ \hline
    The interpreter can run the dam's algorithm accurately and downstream river flows reflect its behaviour.  \newline Sensible behaviour for no-flow, half-flow, and full-flow dams; check the release fraction doesn't exceed 1; dam parameters should be user-settable. & 2 \\ \hline
    The output from a dam can depend on at least two of the following: the flow into the dam, today's rain, the dam level. You may add others if you like.  \newline Explain your design decisions and implementation steps --- this explanation is worth half of this item's marks. & 2 \\ \hline
    Log-book entries showing consistent workshop engagement throughout the semester.  No logbook = 0 marks.  Complete and timely entries = full marks. & 2 \\ \hline
    How well does this language express the underlying concepts.  I.e. have you chosen sensible keywords and syntax structures and have your implemented an interesting language overall.  & 2 \\ \hline
    Uniqueness and creativity.  You can present your work in the week 13 class to guarantee full marks for this rubric item & 2 \\ \hline
    \end{tabular}
    Note the rubric evidence document does expand upon these rubric descriptions to aid in your submission.

    \newpage
answer: |
  None provided
