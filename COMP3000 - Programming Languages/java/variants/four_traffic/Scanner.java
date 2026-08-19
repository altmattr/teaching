package variants.four_traffic;

import static variants.four_traffic.TokenType.*;

import java.util.ArrayList;
import java.util.List;

class Scanner {
  private final String source;
  private final boolean debug;
  private boolean firstDebug = true;
  private final List<Token> tokens = new ArrayList<>();
  private int start = 0;
  private int current = 0;
  private int line = 1;

  Scanner(String source) {
    this(source, false);
  }

  Scanner(String source, boolean debug) {
    this.source = source;
    this.debug = debug;
  }

  List<Token> scanTokens() {
    if (debug) System.out.println(source);
    while (!isAtEnd()) {
      start = current;
      scanToken();
    }

    tokens.add(new Token(EOF, "", line));                             debugPrint("scanning complete, emitting EOF");
    return tokens;
  }

  private void scanToken() {
    char c = advance();                                             debugPrint("I advanced character and consumed it, it was:" + c);
    switch (c) {
      case '>':                                                     debugPrint("found >, need to peek ahead");
        if (match('>')) {                                           debugPrint("I got what I needed! :)");
          addToken(MERGE);
        } else {                                                    debugPrint("I got the wrong thing :/");
          Lox.error(line, "Unexpected character: >");
        }
        break;
      case '-':                                                     debugPrint("found -, need to peek ahead");
        if (match('>')) {                                           debugPrint("I got what I needed! :)");
          addToken(ROUTE);
        } else {                                                    debugPrint("I got the wrong thing :/");
          Lox.error(line, "Unexpected character: -");
        }
        break;
      case '@':                                                     debugPrint("found @, single character token"); addToken(INTERSECTION); break;
      case '|':                                                     debugPrint("found |, single character token"); addToken(LANE); break;
      case '(':                                                     debugPrint("found (, single character token"); addToken(LPAREN); break;
      case ')':                                                     debugPrint("found ), single character token"); addToken(RPAREN); break;

      case ' ':                                                     debugPrint("whitespace, skipping");
      case '\r':
      case '\t':
        break;

      case '\n':                                                    debugPrint("newline, line now " + (line+1));
        line++;
        break;

      default:                                                      debugPrint("I'm in idenfier since nothing else worked, so just soak them all up");
        if (isAlpha(c)) {
          identifier();
        } else {
          Lox.error(line, "Unexpected character: " + c);
        }
        break;
    }
  }

  private void identifier() {
    while (isAlphaNumeric(peek())) {
        advance();
        debugPrint("identifier continues, consumed " + source.charAt(current-1));
    }
    String text = source.substring(start, current);
    addToken(IDENTIFIER, text);
  }

  private boolean match(char expected) {
    if (isAtEnd()) return false;
    if (source.charAt(current) != expected) return false;
    current++;
    return true;
  }

  private char peek() {
    if (isAtEnd()) return '\0';
    return source.charAt(current);
  }

  private boolean isAlpha(char c) {
    return (c >= 'a' && c <= 'z') ||
           (c >= 'A' && c <= 'Z') ||
            c == '_';
  }

  private boolean isAlphaNumeric(char c) {
    return isAlpha(c) || isDigit(c);
  }

  private boolean isDigit(char c) {
    return c >= '0' && c <= '9';
  }

  private boolean isAtEnd() {
    return current >= source.length();
  }

  private char advance() {
    return source.charAt(current++);
  }

  private void addToken(TokenType type) {
    addToken(type, source.substring(start, current));
  }

  private void addToken(TokenType type, String lexeme) {
    debugPrint(type + " \"" + lexeme + "\"");
    tokens.add(new Token(type, lexeme, line));
  }

  private void debugPrint(String info) {
    if (!debug) return;
    System.out.print("\r\033[2K" + " ".repeat(start) + "^" + ((current != start) ? "-".repeat(current-start-1)+" ":" ") + info);
    System.out.flush();
    try { System.in.read(); } catch (Exception e) {}
    System.out.print("\033[1A");
  }
}
