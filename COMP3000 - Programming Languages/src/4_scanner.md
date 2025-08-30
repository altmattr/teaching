
## Overview

This week we turn our focus to turning a stream of characters into a stream of tokens, aka Scanning

## Goals

By the end of this week you should:
    * Know what scanning is
    * Be able to analyse the operation of scanner given as a prose description
    * Discuss scanner look-ahead based on concrete examples
    * Be able to write a scanner in the style of lox.

## Preparation
  * Read Chapter 4 of "Compiling Interpreters"
  * Watch the following lecture videos on echo360
    - scanning part 1
    - scanning part 2
    - making changes to a scanner
  * Ensure you have started your own Lox interpreter.  I.e. not the one you were using last week (which will be complete), but one that follows along with the book.
  * Re-read the unit preamble, where we explain the EPIC learning style and how it applied to COMP3000.

# FAT

## Thinking about water flows <tex-essay>
question: |
  Over the remainder of semester, we will be creating a programming language to \emph{model} and \emph{simulate} water flows in rivers.  This main task will scaffold your application exercises and your assignment submissions.

  Modelling rivers involves taking rainfall data and simulating what water levels will result from that rainfall over a period of time.  This type of modelling is vital to environmental management and public safety. Floods can be predicted and mitigation methods can be designed.  It also allows water managers to experiment with different dam strategies to maximise safety.

  River system modelling is normally done with simulation software but it could be done better if it was done with a \emph{custom programming language} instead.  COMP3000 2025 students will use what they are learning to create just such a language.

  \begin{note}
  Over semester your team will make the best river modelling language you can.  You are not being pushed towards a certain solution, you are exploring possibilities.  The textbook will help you implement the language you come up with, but your general knowledge and imagination will guide the language.  If you need to ask "domain questions" of an expert in the domain, ask your class teacher or post in the forums.  We've chosen this problem because you all know how water and rivers work in at least some way.
  \end{note}

  Solving this problem is \emph{a real contribution to the science of waterflow management}.  Your team is taking on a real-world problem, you will need to bring your A-game.

  \subsubsection*{Co-Design}
  As students work through their workshops, unit staff will adjust future work to account for the directions students are taking and their choices.  In this way the course is \emph{co=designed} with each cohort of students.

  \subsubsection*{A guide}
  \begin{figure}
  \includegraphics[width=0.588\textwidth]{src/6_simplified_act.jpg}
  \includegraphics[width=0.512\textwidth]{src/6_situated_act.jpg}
  \caption{An example watershed.  On the left is a stylised map and on the right is all the draining rivers and dams on a map to help situate the watershed.}
  \label{fig:act_watershed}
  \end{figure}

  I have done this task already to prove (to myself) it is a good idea.  I will give you a little tour of \emph{my} solution to help guide you on your way.  My solution is a programming language based on Lox (I called it "mattlock").  I added a few new features (beyond what is covered in the text book) to support modelling water flows.  When I execute a program in this language it computes all the waterflows in every river for me.  You will be familiar with programs that only output the things you told it to print, but why be so constrained?  In my case I made the output of the program \emph{the final state of all the variables in the program, all wrapped up in a table} and that ended up being just what I needed!  I created different programs written in that language to model different river systems.  I have so far done the Canberra river system (which is in Figure \ref{fig:act_watershed}), the full ACT river system, the Lane Cove River system to Chatswood, and the Berowra River system all the way to Marramarra creek (that is a long program but really shows off how much you can say when you have the right notation to do it in). Thus my repository of mattlock programs is:
  \begin{itemize}
  \item \verb+canberra.mattlock+ (40 lines of mattlock code)
  \item \verb+act.mattlock+ (50 lines of mattlock code)
  \item \verb|lane_cove.mattlock| (180 lines of mattlock code)
  \item \verb|berowra.mattlock| (473 lines of mattlock code)
  \end{itemize}

  And here is an example run of one of my water modelling programs.  The river system it is simulating is shown in Figure \ref{fig:act_watershed}.
  \begin{lstlisting}[basicstyle=\footnotesize\ttfamily]
  > java mattlock.Lox canberra.mattlock
  This system assumes that the rainfall all over the river system is the same and can 
  be described with one number per day.
  
  Rainfall (mm) per day:
  ----------------------
              0    1    2    3    4    5    6    7    8    9    10   11
  rainfall  11.4  0.0  0.4  0.0  0.0  2.0  0.2  0.2  0.2  0.0  0.0  8.3

  Running the model computes the flow in each watershed on each day.

  Flows (L/second)
  ----------------
                    0     1     2    3    4     5      6     7     8    9    10      11 
  upper_molo     57.00   0.0  2.00  0.0  0.0  10.0   1.00  1.00  1.00  0.0  0.0   41.50 
  googong       114.00   0.0  4.00  0.0  0.0  20.0   2.00  2.00  2.00  0.0  0.0   83.00 
  quean          31.40  20.0  0.40  0.0  0.0  22.0  20.20  0.20  0.20  0.0  0.0   28.30 
  jerra          22.80   0.0  0.80  0.0  0.0   4.0   0.40  0.40  0.40  0.0  0.0   16.60 
  central_molo  145.40  20.0  4.40  0.0  0.0  42.0  22.20  2.20  2.20  0.0  0.0  111.30 
  lower_molo      9.12   0.0  0.32  0.0  0.0   1.6   0.16  0.16  0.16  0.0  0.0    6.64 
  \end{lstlisting}

  I can't show you my programming language - I want each team to be creative and come up with new exciting ideas - but I can give a little hint.  In the Canberra river system, central molongolo is made up of all the water coming from upper molongolo, all the water from queanbeyan, all the water from jerrabomberra, and the water that fell over that area.  I represent this in my program as
  \begin{lstlisting}
  central_molo = upper_molo + quean + jerra + central_molo_rainfall
  \end{lstlisting}
  but I have put some magic into that \verb+central_molo_rainfall+ variable.  It is \emph{not} just a number, it somehow captures the way rain makes its way into a creek in the days after the rainfall event.  It is a simple solution with powerful effects\footnote{\emph{This} is super-power of programming based solutions to this problem}.


  \subsubsection*{Your team's task}

  This week I want you to:
  \begin{itemize}
  \item Brainstorm how this whole process even works.  
  \item Brainstorm what sort of forms that \verb+central_molo_rainfall+ could take.
  \end{itemize}

  The second task might require you to think about any special \emph{literals} we might need.  Recall that a literal is a way of writing a value in your language which communicates its type and its value.  Numbers, strings, and True/False are literals you will be familiar with.  When creating our own language for a particular domain, there may be domain concepts that need added to the language as literals.  Note that this week's class will involve lots of brainstorming, head-scratching, exploration, and inspiration.  You might choose to make additions to your scanner based on what you decide, but that is a secondary concern.
  
  \subsubsection*{Water flows}
  When it rains, water flows into the local creek/river.  It hits the ground and, over time, goes down under gravity.  It doesn't happen instantaneously and water may still be flowing into a creek/river up to 10 days after a rainfall event. 

  I will add a few simplifying assumptions to help:
  \begin{enumerate}
  \item The rainfall across a whole \emph{catchment} can be described with one number (in mm).
  \item The flow out of one creek is exactly the flow into the next creek.
  \item All water that gets into a creek/river will also flow out of it.
  \item All water that falls from the sky will (within 10 days) make its way into the creek/river.
  \item Each catchment has one creek/river which drains it.
  \end{enumerate}
  \newpage

answer: |
  \begin{note}
  This "answer" is only a suggestion, there are many possible correct approaches.  I've even discussed a different suggestion in a video posted to iLearn.
  \end{note}

  If the water flows over 10 days, I need 10 numbers between 0 and 1 representing the percentage that gets into the creek that day.  Lot of languages have literal forms that can do that:
  \begin{description}
  \item[arrays] \verb|{0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.0}|
  \item[lists] \verb|[0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.0]|
  \item[dictionaries] \verb|[1: 0.2, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1, 6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1, 10: 0.0]|
  \end{description}
  Any of these would work.  Because lox already uses curly braces but does not use square brackets, I think list syntax works best for me (dictionaries are just longer than they need to be).  Even then, this literal form is quite long, I wish I could have something shorter. I'm used to nice short literals!
  \subsubsection*{Even better}
  If fact the 10 numbers will probably follow a fairly standard distribution, like normal, chi-squared, F, etc

  \includegraphics{src/5_distros.jpg}
  
  I think it might be better to pick one of those and have a literal to describe \emph{that}.  I'm going with a log-normal distribution because it "looks right to me".  A log-normal distribution is fully described by two numbers, the mean $\mu$ and the standard deviation $\sigma$ so I need a literal form to hold two numbers.  While there are some that exist in other languages, I think I will make up my own.
  $$
  lognorm[\mu,\sigma]
  $$
  for example \verb|lognorm[3,2]| would be a distribution where most of the rain drains on the third day.

  Note, I've used square brackets because I want to make it as simple as possible for my scanner to know that it is not a function call (which we will learn to scan later).

  Then I changed my mind and went with a symbol between two numbers.  A squiggle kind of looks like a distribution plot
  \begin{lstlisting}
  2 ~ 3
  \end{lstlisting}
  is the log normal distribution with a mean of 2 and standard deviation of 3.

  I really like this form, so I am going with it.

  \subsubsection*{Scanner changes}
  I need to make my scanner accept this literal.  Recall that scanners only deal with tokens.  What new token(s) have I introduced?  Just one!  The \verb|~| is my only new token.  Here are the changes that are needed:
  \begin{itemize}
  \item Add a new \verb+TokenType+ for \verb|DISTRO|.  I could use \verb|SQUIGGLE| or \verb|TILDE| just as well, it is up to me.
  \item Adjust \verb|Scanner| method \verb|scanToken| to add a new case \verb|    case '~': addToken(DISTRO); break; |
  \end{itemize}

  \begin{note}
  There is a general software engineering principal that pops up here.  I put \emph{meaning} into my token by calling it \verb|DISTRO| rather than \verb|TILDE|.  Was this the right choice?  Overall, it is a 50/50 decision I would say but since I am adding to an existing codebase I should match what happens there.  If we look at the existing token types, the non-meaning option is being used.  For example \verb|SLASH| not \verb|DIVIDE| and \verb|STAR| not \verb|MULTIPLY| so I think, on balance, \verb|TILDE| is better in this case.  Choosing \verb|DISTRO| won't break anything at all, it just creates a tiny inconsistency in the codebase.  These are harmless on their own but tend to accumulate and grow and so programmers spend quite a lot of time thinking about these things.
  \end{note}

# RAT

## How much lookahead <gift>
How much lookahead is needed if our scanner is concerned with only the following tokens: `)` (right parens), `(` (left parens), `[` (left square), and `]` (right square).  I.e. these are the only 4 tokens that might validly appear in a program.{
  =0
  ~1
  ~2
  ~3
}

## scanner purpose <gift>
What is the primary purpose of the scanner (lexical analyzer) in a compiler or interpreter? {
    ~To parse the syntax of the source code.
    ~To optimize the source code for performance.
    =To convert the source code into a series of tokens.
    ~To execute the source code directly.
}

## token examples <gift>
Which of the following is an example of a token in the scanning process? {
    =A variable name like `3x`.
    ~A syntax error found in the source code.
    ~A function call like `foo(5)`.
    ~A computation like `x + 3`.
}

## scanning errors <gift>
Which of the following is a common type of error detected during scanning? {
    ~Syntax errors caused by incorrect grammar rules.
    =Lexical errors caused by unexpected or invalid characters.
    ~Semantic errors caused by invalid logic in the code.
    ~Runtime errors caused by division by zero.
}

## scanning input and output <gift>
What is the primary input and output of the scanning process? {
    ~Input: Abstract Syntax Tree (AST), Output: Bytecode.
    =Input: Source code, Output: Tokens.
    ~Input: Tokens, Output: Machine code.
    ~Input: Syntax rules, Output: Variable bindings.
}

# SSE

## Lookahead <essay>
question: |
  Lox needs just 2 "lookahead".  What part of the syntax is that lookahead needed for?
answer: |
  Single lookahead is needed in lots of places.  Strings look ahead to know they stop on `"`.  Identifiers look ahead to see if the next character is still part of the identifier.  Just about every multi-character token needs to look ahead at least one to know whether it continues to advance or if it stops and returns a value.  For decimals we need to look two ahead because when we see a period one in front we need to look ahead _again_ to decide if we advance or stop.  
  
## Triple Lookahead <essay>
question: |
  Can you think of a syntax that would need more than two lookahead?  Ruby might give you inspiration.
answer: |
  Strings in Ruby will need more lookahead.  Ruby supports strings that begin/end with single inverted commas, which require one lookahead.  However, it also support triple-quoted strings and to determine when you have one of these rather than a single-quoted string you would need to lookahead twice more.

## Switch to a single peek method <essay>
question: |
  As suggested in the text, switch to a single `peek` method that will peek however far ahead you ask it to.
answer: |
  We also need to adjust `isAtEnd` to have the same parameterisation if this is to be consistent.  Note that I don't want to change too much of the code so I overload `isAtEnd` to keep the no-parameter version but have it call a parameterised version.
  `````
  // old version commented out
  // private boolean isAtEnd() {
  //   return current >= source.length();
  // }
  // new version
  private boolean isAtEnd(){return isAtEnd(0);}
  private boolean isAtEnd(int howFar){
    return current + howFar >= source.length();
  }
  `````
  and here are the changes to `peek` and `peekNext`. I do the same overriding trick so I can keep the old version working.
  `````
    // // private char peek() {
  // //   if (isAtEnd()) return '\0';
  // //   return source.charAt(current);
  // // }

  // private char peekNext() {
  //   if (current + 1 >= source.length()) return '\0';
  //   return source.charAt(current + 1);
  // } 
  private char peek(int howFar){
    if (isAtEnd(howFar)) return '\0';
    return source.charAt(current + howFar);
  }
  `````
  Of course, I also need to find all the calls to `peekNext` and adjust them to `peek(1)`.

## Add a read operation <essay>
question: |
  Lox only has `print` but it sure would be nice to get input from the user.  Add a `read` operation.  This includes adding a token for it, having that token identified as a keyword, then creating a test file with a test output to prove it worked.
answer: |
  My test file looks like
  `````
  var x = read
  print x;
  `````
  and it will scan just fine with no changes but that will give me the following output
  `````
  VAR var null
  IDENTIFIER x null
  EQUAL = null
  IDENTIFIER read null
  PRINT print null
  IDENTIFIER x null
  SEMICOLON ; null
  EOF  null
  `````
  That's not what I want because the `read` has been scanned as an identifier instead of a keyword.  I've had to add `READ` to `TokenType.java` and add `    keywords.put("read",   READ);` to the static block in `Scanner.java`.  When I do that, I get what I really want
  `````
  VAR var null
  IDENTIFIER x null
  EQUAL = null
  READ read null
  PRINT print null
  IDENTIFIER x null
  SEMICOLON ; null
  EOF  null
  `````

## Better hash <essay>
question: |
  If you understand how the `identifier` function works _and_ you know about [getOrDefault](https://docs.oracle.com/javase/8/docs/api/java/util/Map.html#getOrDefault-java.lang.Object-V-) then you can shrink the `identifier` function to just 3 lines.  Do it.
answer: |
  New version with old version commented out for clarity
  `````
  private void identifier() {
    while (isAlphaNumeric(peek())) advance();
    String text = source.substring(start, current);
    addToken(keywords.getOrDefault(text, IDENTIFIER));
  }
  `````
  I can't think of a reason _not_ to use `getOrDefault` except that perhaps Nystrom wanted to keep to an even earlier version of Java.  `getOrDefault` was introduced in Java 8.

## Oct numbers <essay>
question: |
  Write a code for lox that can scan _oct numbers_.  Oct numbers start with a "o" and can include any digit from 0 to 7.  You should assume the presence of the following functions which work exactly as they do in the text.  Oct numbers never have a fractional part.
  `````
  bool isOctalDigit(); // returns true for 0 - 7 only
  char advance();
  char peek();
  char peekNext();
  Double octConv(String s); // converts the octal string s to a double.
  `````
  You may also assume the main scanning method is given below.  Your answer should explain what code you add here and give complete definitions of any functions you choose to use.
  `````
    private void scanToken() {
    char c = advance();
    switch (c) {
      case '(': addToken(LEFT_PAREN); break;
      case ')': addToken(RIGHT_PAREN); break;
      case '{': addToken(LEFT_BRACE); break;
      case '}': addToken(RIGHT_BRACE); break;
      case ',': addToken(COMMA); break;
      case '.': addToken(DOT); break;
      case '-': addToken(MINUS); break;
      case '+': addToken(PLUS); break;
      case ';': addToken(SEMICOLON); break;
      case '*': addToken(STAR); break; 
      case '!':
        addToken(match('=') ? BANG_EQUAL : BANG);
        break;
      case '=':
        addToken(match('=') ? EQUAL_EQUAL : EQUAL);
        break;
      case '<':
        addToken(match('=') ? LESS_EQUAL : LESS);
        break;
      case '>':
        addToken(match('=') ? GREATER_EQUAL : GREATER);
        break;
      case '/':
        if (match('/')) {
          // A comment goes until the end of the line.
          while (peek() != '\n' && !isAtEnd()) advance();
        } else {
          addToken(SLASH);
        }
        break;
      // ignore whitespace
      case ' ':
      case '\r':
      case '\t':
        break;
      case '\n':
        line++;
        break;
      // string literals
      case '"': string(); break;
      default : 
        if (isDigit(c)){
          number();
        } else if (isAlpha(c)) {
          identifier();
        } else {
          MLox.error(line, "Unexpected character.");
        }
        break;
    }
  }
  `````
answer: |
  This one is a little tricky.  When we see an "o", it might be an identifier, or it might be an octal number.  We can add a little lookahead to help us decide.
  `````
  } else if (isAlpha(c)){
    if (c == "o" && isOctDigit(peek())){
      octal()
    } else {
      identifier();
    }
  }   
  `````
  and define `octal` as
  `````
  private void octal(){
    while (isOctDigit(peek())) advance();
    addToken(NUMBER, octConv(source.substring(start, current)));
  `````
  Here is a test file you can try it out with
  `````
  var x = 3 + o34;
  print x;
  `````

## Hex numbers <essay>
question: |
  Write a code for lox that can scan _hex numbers_.  Hex numbers start with a "#" and can include any digit or any letter from "A", "B", "C", "D", "E", "F" (capitals only).  You should assume the presence of the following functions which work exactly as they do in the text.  Hex numbers never have a fractional part.
  `````
  bool isDigit();
  char advance();
  char peek();
  char peekNext();
  Double hexConv(String s); // converts the hex string s to a double.
  `````
  You may also assume the main scanning method is given below.  Your answer should explain what code you add here and give complete definitions of any functions you choose to use.
  `````
    private void scanToken() {
    char c = advance();
    switch (c) {
      case '(': addToken(LEFT_PAREN); break;
      case ')': addToken(RIGHT_PAREN); break;
      case '{': addToken(LEFT_BRACE); break;
      case '}': addToken(RIGHT_BRACE); break;
      case ',': addToken(COMMA); break;
      case '.': addToken(DOT); break;
      case '-': addToken(MINUS); break;
      case '+': addToken(PLUS); break;
      case ';': addToken(SEMICOLON); break;
      case '*': addToken(STAR); break; 
      case '!':
        addToken(match('=') ? BANG_EQUAL : BANG);
        break;
      case '=':
        addToken(match('=') ? EQUAL_EQUAL : EQUAL);
        break;
      case '<':
        addToken(match('=') ? LESS_EQUAL : LESS);
        break;
      case '>':
        addToken(match('=') ? GREATER_EQUAL : GREATER);
        break;
      case '/':
        if (match('/')) {
          // A comment goes until the end of the line.
          while (peek() != '\n' && !isAtEnd()) advance();
        } else {
          addToken(SLASH);
        }
        break;
      // ignore whitespace
      case ' ':
      case '\r':
      case '\t':
        break;
      case '\n':
        line++;
        break;
      // string literals
      case '"': string(); break;
      default : 
        if (isDigit(c)){
          number();
        } else if (isAlpha(c)) {
          identifier();
        } else {
          MLox.error(line, "Unexpected character.");
        }
        break;
    }
  }
  `````
answer: |
  We need to add a new alternative in the default case after the
  `````
  } else if (isAlpha(c)){
  `````
  branch.  We add
  `````
  } else if (c == '#'){
    hex();
  }
  `````
  and define `hex` as
  `````
  private void hex(){
    char c = peek();
    while(isDigit(c) || c == "A" || c == "B" || c == "C" || c == "D" || c == "F"){
      advance();
      c = peek();
    }
    addToken(NUMBER, hexConv(source.substring(start, current)));
  `````


# Exam

## Add another type of comment <essay>
question: |
  Write a scanner that will support new types of comments.  These comments should start with `#` and proceed to the end of the line only.
  We have populated the answer box with an empty scanner (`QScanner`) which inherits from the lox scanner described in the text.  The test code uses this scanner.  Override whatever methods you need to achieve the desired result
  
  Here is a template to get you started
  `````
  import static com.craftinginterpreters.lox.TokenType.*; // [static-import]

  class QScanner  extends Scanner{
    public QScanner(String source) {
      super(source);
    }

    public void scanToken() {
      char c = advance();
      switch (c) {
        case '(': addToken(LEFT_PAREN); break;
        case ')': addToken(RIGHT_PAREN); break;
        case '{': addToken(LEFT_BRACE); break;
        case '}': addToken(RIGHT_BRACE); break;
        case ',': addToken(COMMA); break;
        case '.': addToken(DOT); break;
        case '-': addToken(MINUS); break;
        case '+': addToken(PLUS); break;
        case ';': addToken(SEMICOLON); break;
        case '*': addToken(STAR); break; // [slash]
        case '!':
          addToken(match('=') ? BANG_EQUAL : BANG);
          break;
        case '=':
          addToken(match('=') ? EQUAL_EQUAL : EQUAL);
          break;
        case '<':
          addToken(match('=') ? LESS_EQUAL : LESS);
          break;
        case '>':
          addToken(match('=') ? GREATER_EQUAL : GREATER);
          break;
        case '/':
          if (match('/')) {
            // A comment goes until the end of the line.
            while (peek() != '\n' && !isAtEnd()) advance();
          } else {
            addToken(SLASH);
          }
          break;
        case ' ':
        case '\r':
        case '\t':
          // Ignore whitespace.
          break;

        case '\n':
          line++;
          break;
        case '"': string(); break;
        default:
          if (isDigit(c)) {
            number();
          } else if (isAlpha(c)) {
            identifier();
          } else {
            Lox.error(line, "Unexpected character.");
          }
          break;
      }
    }
  }
  `````
answer: |
  `````
  import static com.craftinginterpreters.lox.TokenType.*; 

  class QScanner  extends Scanner{
    public QScanner(String source) {
      super(source);
    }

    public void scanToken() {
      char c = advance();
      switch (c) {
        case '#': while(peek() != '\n' && !isAtEnd()) advance(); break;
        case '(': addToken(LEFT_PAREN); break;
        case ')': addToken(RIGHT_PAREN); break;
        case '{': addToken(LEFT_BRACE); break;
        case '}': addToken(RIGHT_BRACE); break;
        case ',': addToken(COMMA); break;
        case '.': addToken(DOT); break;
        case '-': 
            if (match('-')) {
                while (peek() != '\n' && isAtEnd()) advance();
            } else {
                addToken(MINUS);
            }
            break;
        case '+': addToken(PLUS); break;
        case ';': addToken(SEMICOLON); break;
        case '*': addToken(STAR); break; // [slash]
        case '!':
          addToken(match('=') ? BANG_EQUAL : BANG);
          break;
        case '=':
          addToken(match('=') ? EQUAL_EQUAL : EQUAL);
          break;
        case '<':
          addToken(match('=') ? LESS_EQUAL : LESS);
          break;
        case '>':
          addToken(match('=') ? GREATER_EQUAL : GREATER);
          break;
        case '/':
          if (match('/')) {
            // A comment goes until the end of the line.
            while (peek() != '\n' && !isAtEnd()) advance();
          } else {
            addToken(SLASH);
          }
          break;
        case ' ':
        case '\r':
        case '\t':
          // Ignore whitespace.
          break;

        case '\n':
          line++;
          break;
        case '"': string(); break;
        default:
          if (isDigit(c)) {
            number();
          } else if (isAlpha(c)) {
            identifier();
          } else {
            Lox.error(line, "Unexpected character.");
          }
          break;
      }
    }
  }
  `````

## write a coffee parser <gift>
Imagine you are writing a scanner for scanning coffee orders into tokens.  Your can assume a CoffeeToken enum has been defined for you with the following tokens:
    * SKIM ('s')
    * OAT ('o')
    * SOY ('y')
    * FLATWHITE ('f')
    * CAPPUCCINO ('c')
    * LATE ('l')
    * BLACK ('b')
    * PICCOLO ('p')
    * SUGAR ('-')
    * NUMBER
    * SHOT ('*')
For most tokens, a single character (given above) is used to encode them in the coffee language. but shot and sugar might be followed by a number which can be any number up to 9.  Some example orders and their token stream are:
    * `sf` `SKIM FLATWHITE`
    * `ol*3` `OAT LATTE SHOT 3`
    * `yp-2` `SOY PICCOLO SUGAR 2`
If you were writing a scanner for coffee orders, how much _lookahead_ would the scanner need?{
  =0
  ~1
  ~2
  ~3
}

## scanner purpose <gift>
Which of the following best describes the primary purpose of a scanner in the context of an interpreter? {
    ~ To evaluate expressions in the source code.
    = To convert the source code into a sequence of tokens.
    ~ To parse the tokens into an abstract syntax tree (AST).
    ~ To optimize the source code for performance.
}

## scanner strategy <gift>
What is the most common strategy used by a scanner to handle multi-character tokens, such as identifiers or string literals? {
    = Reading the source code character by character in a single pass and grouping characters into tokens based on matching patterns.
    ~ Using a predefined dictionary to directly map substrings of the source code to tokens.
    ~ Performing a binary search on the source code to identify tokens.
    ~ Applying a brute-force algorithm to test all possible token combinations.
}

## edge cases in scanners <gift>
When designing a scanner, which of the following edge cases is typically the hardest to handle? {
    = Nested comments in languages that support them.
    ~ Single-character tokens like `+` or `-`.
    ~ White spaces between tokens.
}