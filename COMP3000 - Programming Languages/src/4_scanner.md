
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

# FAT

## Development Cycle <tex-essay>
question: |
  Our first task this week is to make sure every group member has a working Lox scanner.  All the code we need is in the textbook.  You will work together as a team to fix any issues that any group members have until \emph{everyone} has a working scanner.  

  Once you have that working, come up with a \emph{development cycle} for working on Lox extensions.  This semester we will be adding extra features to the Lox code-base in the textbook, so you will spend lots of time working on that code base.  An important part of working on a code-base in a team is to have a development cycle that everyone agrees on.  This is not a formal process, but it is important that you all agree on how you will work together.

  Note: This is not to do with \emph{teamwork} in the way you might think.  This is about making sure that, as each individual does work on their own computer, they can communicate with others in the team because the whole team is working the same way.  Your aim is \emph{to find a shared point of view and to codify it}.

  As semester goes on, the work you are doing in your teams is going to directly contribute to your assignment submission. You need a way to be a part of that team that allows you to make use of the work \emph{without copy-pasting just before the due date} since that will get you sanctioned!

  You are probably used to a development cycle that looks like this:
  \begin{enumerate}
    \item Have source code and test code.
    \item Test code is written in JUnit
    \item If the tests are green, your code is working.
  \end{enumerate}
  That won't be enough for compiler/interpreter development.  Think about answers to the following questions to help you come up with a development cycle that will work for you:
  \begin{enumerate}
    \item Think critically about the relative importance of testing individual methods (unit tests) vs testing the whole system (system tests).
    \item What is the output of the program you are testing?  Is this a nice form to help testing?
    \item What are the inputs to the program you are testing?  Can you link inputs to outputs in an easy way?
    \item Should you use testing machinery from JUnit or make your own?
    \item Don't neglect how you will be sharing these files between each other.  You will probably use git, are you sure you all know how that will work and can get the files when you need them?
    \item How much can you achieve just with smart use of file and folders?
  \end{enumerate}
  \subsection*{Discussion}
  At the end of class, share your development cycle with the rest of the class.  Listen carefully to the other groups, some will have had better ideas than you.  The class should vote on which sounds most sensible.  The teacher will also tell you which one they think is best.  

  \newpage
answer: |
  \begin{note}
  This "answer" is only a suggestion, there are many possible correct approaches.
  \end{note}
  I decided to focus on what might be called "system tests".  I might turn to unit tests when I have a particularly troublesome thing to debug.
  
  For each test, I write an input file (which is a lox program) and then I add another file which has the output I expect from compiling that program.  I can use file extensions to indicate the output of different compiler phases.  For example, for this week I have input files with the extension \verb|.lox| and output files with the extension \verb|.scan|.  The \verb|.scan| files contain the output of the scanner.  I can then run my scanner on the input file and compare the output to the expected output.  If they match, I know my scanner is working correctly.  If I just use files, I can also share the input and output files with my team members via git so they can run the same tests on their scanners.  This way we can all be sure that our scanners are working correctly.  As later phases of the interpreter are added, I might make new output files for the different phases.

  \subsection*{Controlling Phases}
  The Lox interpreter we are building will always run \emph{all} the defined phases.  We only have the scanning phase for now, but later we will add more.  I quite like being able to see \emph{all the phase outputs} so I have adjusted my own Lox interpreter to save the result of each phase to a file so I can compare them to what I expect and test as needed.  There are some issues to deal with here, all around organisation.  Here are all the files I need to track in my approach:
  \begin{enumerate}
  \item The input test files (\verb|.lox|)
  \item The expected output for each phase:
  \begin{enumerate}
  \item the expected scanner output (\verb|.scan|)
  \item the expected parser output (\verb|.parse|)
  \item the expected interpretation output (\verb|.out|)
  \end{enumerate}
  \item The actual output for each phase:
  \begin{enumerate}
  \item the actual scanner output (\verb|.scan|)
  \item the actual parser output (\verb|.parse|)
  \item the actual interpretation output (\verb|.out|)
  \end{enumerate}
  \end{enumerate}
  
  I need a good way to organise these so my tests can run and I can easily look around them during debugging. I've chosen a little hierarchy for each test.  For every \verb|.lox| file I have, I have two folders \verb|expected| and \verb|actual|.  If I have test output for that file it goes in \verb|expected| and I can write a little script that compares all the expecteds to actuals.

  To make this work perfectly, I just need to adjust my Lox interpreter so it generates the \verb|actual| files while interpreting.

  \subsection*{Faking Unit Tests}
  If the system test is a very simple program which only has one feature, it works a bit like a unit test!  I have found this completely sufficient for my purposes so I don't even have JUnit imported in my project.  I'm a bit of an outlier though.  I tend to do a bit of \href{https://en.wiktionary.org/wiki/yak_shaving#/media/File:Yak_shaving.jpg}{Yak shaving} just for fun.

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
    =A variable name like `x`.
    ~A syntax error found in the source code.
    ~An optimization rule applied during compilation.
    ~The entire source code as a string.
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

## Add another type of comment <scanner>
question: |
  Write a scanner that will support new types of comments.  These comments should start with `#` and proceed to the end of the line only.
  We have populated the answer box with an empty scanner (`QScanner`) which inherits from the lox scanner described in the text.  The test code uses this scanner.  Override whatever methods you need to achieve the desired result
answer_template: |
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
answer: |
  import static com.craftinginterpreters.lox.TokenType.*; // [static-import]

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
tests:
  - Lox.scan(new QScanner("print \"hi\";"), false): |
      PRINT print null
      STRING "hi" hi
      SEMICOLON ; null
      EOF  null
  - Lox.scan(new QScanner("print \"hi\";#commend"), false): |
      PRINT print null
      STRING "hi" hi
      SEMICOLON ; null
      EOF  null
  - Lox.scan(new QScanner("print 5;"), false): |
      PRINT print null
      NUMBER 5 5.0
      SEMICOLON ; null
      EOF  null
  - Lox.scan(new QScanner("#commend\nprint 5;"), false): |
      PRINT print null
      NUMBER 5 5.0
      SEMICOLON ; null
      EOF  null

## write a coffee parser <scanner>
question: |
  Write a scanner for scanning coffee orders into tokens.  Your can assume a CoffeeToken enum has been defined for you with the following tokens:
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
  For most tokens, a single character (given above) is used to encode them in the coffee language. but shot and sugar might be followed by a number which can be any number up to 9.  Write a scanner to for the coffee langauge.  Some example orders and their token stream are:
    * "sf" `SKIM FLATWHITE`
    * "ol*3` `OAT LATTE SHOT 3`
    * "yp-2~ `SOY PICCOLO SUGAR 2`
answer_template: |
  still to do
answer: |
  still do to
tests:
  - none: none

