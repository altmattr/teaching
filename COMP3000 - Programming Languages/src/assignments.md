
Over the semester, you will be creating a programming language to \emph{model} and \emph{simulate} water flows in river systems.  This project is the central thread of COMP3000: everything you learn about scanning, parsing, representing code, and evaluating programs will be applied to building a real domain-specific language.

Modelling rivers involves taking (as input) rainfall data and simulating what water flows result from that rainfall over a period of time.  This type of modelling is vital to environmental management and public safety; floods can be predicted, mitigation methods designed, and water managers can experiment with different dam strategies to maximise safety.  River system modelling is normally done with general-purpose simulation software, but it could be done better with a \emph{custom programming language} designed specifically for the domain.

\emph{Your task is to build that language}.  Starting from the Lox codebase you develop through the textbook, you will extend and adapt it into a language capable of describing river systems, computing flows over multiple days, and simulating the behaviour of human-controlled dams.  You are not being pushed towards a single solution, you are exploring possibilities and making design decisions as language designers.

The project has two submission points:

\begin{description}
\item[Submission One:] A parser for your water flow language.  You will design a grammar capable of representing river systems and implement a Lox-style parser for it.  You will also produce three example programs and a document explaining your language and parser.
\item[Submission Two:] An interpreter for your language.  Building on your parser, you will add evaluation so that programs in your language produce meaningful output, the predicted flows in a river system over time.  You will also add support for dams, which allow human-controlled adjustment of water flows.
\end{description}

Each submission is graded against a rubric that rewards both technical achievement and the quality of your language design.  The two submissions are weighted equally, and together they make up the assignment component of your final mark.  You are free to build on your team's workshop work, but each submission must be your own.  Uniqueness and creativity are rewarded, the best submissions will be those that go beyond what was done in class.

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
    A \emph{river system} is a series of connected rivers.  Your domain specific language must be capable of representing a river system.  Executing a program in this domain specific language will compute the flows in every river at each day given a certain rainfall.  For now you can ignore the complication of representing the rainfall and focus on a language which is capable of describing the river system itself.

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
    \item Dam 2 drains to lower molongolo\footnote{FYI: Dam 2 forms lake Burley Griffin in Canberra, you may have been there!}
    \item The output of the entire river system is the output of lower molongolo
    \end{itemize}

    Note that the examples in the \emph{Language Features in the Exemplar} section below use a different (fictional) set of creeks (joes, mahers, and devlins, which are local to Macquarie University) than this Canberra example.  The two systems are independent illustrations: the Canberra system is used to situate the domain, and the feature examples are used to show the language constructs.

    We make the following simplifying assumptions:
    \begin{enumerate}
    \item The rainfall across a whole \emph{river system} can be described with one number (in mm).
    \item The rainfall across the whole river system is provided at run time by "magic".  I.e. we can just assume for now that such a number exists and can be accessed.
    \item The flow into one river is the sum of the flows out of its feeding rivers.
    \item The flow out of a river is the flow in plus the water that has made its way into the river on that day.
    \item All water that gets into a river will also flow out of it.
    \item All water that falls from the sky will (within 10 days) make its way into the river.
    \item Rivers never split into two or more rivers.
    \end{enumerate}

    \subsubsection*{Language Features in the Exemplar}

    The exemplar models a river system as a network of creeks and dams.  Here are the key features:

    \emph{Flow literals} describe how water flows past a point over 10 days:
    \begin{verbatim}
    var joes = [1 ~ 1]@4;
    \end{verbatim}
    The three numbers are start day, spread (how drawn out the flow is), and magnitude (total volume).

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

    \emph{The \texttt{<-} operator} connects a dam or river to its upstream source:
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
    \item and a completed rubric explanation (the file \verb+a1_rubric.md+) where you provide answers to specific questions to help your marker complete the rubric.
    \end{itemize}

    The document is your chance to explain your decisions and implementation to your marker, writing a good one will help your marker give you grades for the other files as well.  For example, your marker won't know how to compile your parser unless you tell them so you can't get parser marks unless you clearly describe that in your document.  If your intention is not clear from the documents you submit, you won't be allocated grades, even for work that is ultimately correct.  It is your responsibility to communicate clearly everything your marker needs in your submission.  Your marker will be one of the class teachers, so you can assume they are familiar with anything from class.

    \begin{note}
    There is ambiguity left in this description by design.  You are aiming to make \emph{the best possible domain specific language for waterflows} but we clarify a great deal to support grading your work.  Imagination is needed to complete this task and experimentation is strongly encouraged.
    \end{note}

    \subsubsection*{Rubric Explanation}
    Your zip file must include a completed rubric explanation: the template file \verb+a1_rubric.md+ provided on iLearn.  Please add your answers below each question text in markdown format.  The first set of questions in that file --- the basic questions --- is graded directly and is worth 10\% of your marks.  The rubric below lists all the rubric items; use it as your checklist.  If the answer to any of the basic questions isn't clear from your a1\_rubric.md, your marker may not be able to award you the marks for the work you've done.

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
    Basic questions in a1\_rubric.md (10\%) & None answered accurately & 2 or more answered accurately & 6 or more answered accurately & All answered accurately \\ \hline
    Log-book submissions (10\%) & No logbook submitted or no entries & Some entries but inconsistent across the semester & Regular entries throughout the semester & Complete entries throughout the semester. \\ \hline
    Grammar given in the document in Nystrom's notation (20\%) & No grammar or substantially broken grammar in the document & A grammar with small errors & A grammar that can model rivers systems & A grammar that can model river systems and an explanation of how each example program parses according the grammar \\ \hline
    Three example programs (20\%) & No program or the programs don't model river system correctly & Three programs of some form & \emph{pass} and the example programs all match the given grammar & \emph{credit} and the Lox-like parser can actually parse the programs \\ \hline
    Parser written in Java based on Lox codebase (20\%) & None or not in Java & Code is based on the Lox from chapter 6 of text & Code is based on the Lox from chapter 6 and your additions fit with the style & If there is any improvement to the Chapter 6 Lox code with an explanation in the document, you will get this grade. \\ \hline
    Uniqueness and Creativity (20\%) & A direct submission of in-class work & minor modifications to in-class work & substantial improvement on in-class work & a unique submission showing creativity \\
    \hline
    \end{tabular}
    \subsubsection*{Examples for Uniqueness Rubric}
    Below I give total contribution to the final assignment grade for certain scenarios:
    \begin{description}
    \item[0\%] You have been working with your team all semester and you take the solutions your team came up with, add \emph{your own} document and submit it as-is.
    \item[14\%]  You have been working with your team all semester and they also met outside class hour to try out other things. You take the solutions your team came up with, add \emph{your own} document and submit it as-is.
    \item[20\%]  You have been working with your team all semester. You take the solutions your team came up with and make some adjustments of your own to make it even better.  You add \emph{your own} document and submit.
    \item[20\%] You have been the main person doing all the work for your team and you submit that work, with a document of your own.
    \end{description}
    \newpage
answer: |
    A good submission includes a Lox-style parser written in Java (based on the Chapter 6 code), three example programs that all parse successfully, and a completed a1\_rubric.md.  The basic questions in a1\_rubric.md are graded directly, so answer them accurately: your starting chapter, working folder, and compile commands, your flow literal syntax, your combining operator, and whether your language has statements.  The remaining questions point your marker to the grammar, the example programs, your parser additions, and anything unique or creative, which makes it much easier for your marker to award you the marks your work deserves.

# Submission Two

## Evaluation and Dams <tex-essay>
question: |
    Your task in this assignment is to add \emph{evaluation} and \emph{dams} to your language.

    \subsubsection*{Evaluation}
    Submission One left off with an expression language.  Many of you added statements because it really made sense.  From wherever you left off you need to add \emph{statements}, \emph{evaluation}, and \emph{dams}.  Evaluation means implementing an interpreter which evaluates expressions to some value. The value may be a single number or a sequence of numbers or anything else that makes sense for your language.  You should ensure this value is output in some way so your marker can see it.  We have set two levels of achievement in the rubric depending on the capabilities of your interpreter.  You will almost certainly need to add statements and variables to achieve these things and we have provided an example solution for these in the exemplar.

    \subsubsection*{Dams}
    Dams are human controlled flow adjustment mechanisms.  Sometimes they allow all the flow through, sometimes they increase the flow, sometimes they stop or reduce the flow.  Your task is to add a syntax and evaluation for dams into your language.  The rubric specifies what grades will be given for different levels of achievement in this item.

    \subsubsection*{Starting Point}

    You may build your submission from your team's work, from the exemplar, or from your own work in workshops.  You are free to use your team's code, grammar, and design decisions as much as you like.  A worked example of a complete river system language (the exemplar) is described in the introduction to this document.

    \subsubsection*{The Structure of your submission}
    You will submit a single zip file at the link  available in the "Assessments" section.  The zip should contain \emph{all of}:
    \begin{itemize}
    \item your interpreter,
    \item your example programs, and
    \item your completed rubric evidence document with instructions for your marker
    \end{itemize}

    \subsubsection*{A rubric evidence document}
    Your zip file must include a completed rubric evidence document: the template file \verb+a2_rubric.md+ provided on iLearn.  Please add your answers below each question text in markdown format.  The rubric below lists all the rubric items; use it as your checklist.  There is one section for each rubric item where you explain how you meet or achieve that rubric item and give any help your marker might need to compile, run, and understand your language.  Most sections include a linked video where we show \emph{our solution in action} as a guide for you in putting together your own solution.  You don't need to follow these but it provides one option you can follow if you like.

    The rubric evidence document is your chance to explain your decisions and implementation to your marker, writing clearly and concisely will help your marker award you grades.  For example, your marker won't know how dams work in your language unless you tell them so you can't get dam marks unless you clearly describe that in your rubric evidence document.  If your intention is not clear from your rubric evidence document, you won't be awarded grades, even for work that is ultimately correct.  It is your responsibility to communicate clearly everything your marker needs in your rubric evidence document.  Your marker will be one of the class teachers, so you can assume they are familiar with anything from class.  I.e. there is no need to explain any class concepts.

    We recommend you point your marker to the example program you submitted which demonstrates this rubric item as the simplest way to demonstrate you have achieved it.

    \subsubsection*{Use of Generative AI}
    An ability to use Generative AI is not a learning outcome of this course but GenAI is a tool you may choose to use along your journey.  If your submission is primarily AI generated, you will likely find yourself in the bottom of each rubric item.  Lox and Nystrom's notation are not well represented in AI training sets and Gen AIs are generally bad at language design.  We value, and give grades for, your contribution to the solution since it is you (not the GenAI vendor) who is earning the grade.

    \begin{note}
    You are free to use any and everything from your team's work on this task.  You may not use other team's work directly or solicit for solutions.  These remain contraventions of academic integrity.  The work of the team belongs to all team members, so they can submit that without contravening academic integrity.  However, this is your own submission.  You can, and should, improve upon your team's work as much as possible.  We have included a "similarity/creativity" score in the rubric so we can reward solutions that go beyond what was done in class.  Note that \emph{the document must be your own work}.  It can heavily reference the team's work, but you should write it from scratch yourself.

    You are also free to use any of the example solutions given by unit staff without referencing them.
    \end{note}

    \subsubsection*{Rubric}
    The rubric has a total of 16 marks which are scaled up to 25\% of your final mark for the unit.

    \begin{tabular}{p{0.7\textwidth}|r}
    Rubric item & max marks for this item \\
    \hline
    Your language must be able to interpret an expression which describes simple river flows.  The interpreter must output something when it is finished indicating at least one of the flows in the system.  We recommend outputting all named flows, but you could have a special output expression in which case you will output just that expression.  \newline Rainfall and river catchment size should be user-definable. & 2 \\ \hline
    Your language can model the flow over multiple days and the output of your interpreter shows the predicted flows on all those days.  As with the last item, you may output just one flow, or all named flows, or whatever makes most sense for your language.  \newline Flows should carry over between days --- predicted flows depend on previous days' water, not just today's rainfall. & 2 \\ \hline
    Your language has a syntax to support dams.  Dams don't always let all or none of the flow through, they run some "algorithm" to decide how much flow to let through.  Provide example programs demonstrating your dam syntax and your parser can successfully parse those programs.  Your marker may write their own program so please include a full grammar here.  \newline Grammar should be complete and match your example programs, so the marker can write their own. & 2 \\ \hline
    The interpreter can run the dam's algorithm accurately and downstream river flows reflect its behaviour.  \newline Sensible behaviour for no-flow, half-flow, and full-flow dams; check the release fraction doesn't exceed 1; dam parameters should be user-settable. & 2 \\ \hline
    The output from a dam can depend on at least two of the following: the flow into the dam, today's rain, the dam level. You may add others if you like.  \newline Explain your design decisions and implementation steps --- this explanation is worth half of this item's marks. & 2 \\ \hline
    Log-book entries showing workshop engagement throughout the semester.  No logbook = 0 marks.  Complete and entries = full marks. & 2 \\ \hline
    How well does this language express the underlying concepts.  I.e. have you chosen sensible keywords and syntax structures and have you implemented an interesting language overall.  & 2 \\ \hline
    Uniqueness and creativity.  You can present your work in the week 13 class to guarantee full marks for this rubric item & 2 \\ \hline
    \end{tabular}

    \newpage
answer: |
  None provided
