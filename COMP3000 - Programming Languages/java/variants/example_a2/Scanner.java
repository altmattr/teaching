package variants.example_a2;

import static variants.example_a2.TokenType.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Scanner {
  private final String source;
  private final List<Token> tokens = new ArrayList<>();
  private int start = 0;
  private int current = 0;
  private int line = 1;
  private static final Map<String, TokenType> keywords;

  static {
    keywords = new HashMap<>();
    keywords.put("else",   ELSE);
    keywords.put("if",     IF);
    keywords.put("return", RETURN);
    keywords.put("var",    VAR);
    keywords.put("plot",   PLOT);
    keywords.put("dam",    DAM);
    keywords.put("when",   WHEN);
    keywords.put("default", DEFAULT);
    keywords.put("inflow", INFLOW);
    keywords.put("level",  LEVEL);
    keywords.put("true",   TRUE);
    keywords.put("false",  FALSE);
  }

  Scanner(String source){
    this.source = source;
  }

  List<Token> scanTokens() {
    while (!isAtEnd()) {
      start = current;
      scanToken();
    }

    tokens.add(new Token(EOF, "", null, line));
    return tokens;
  }

  private boolean isAtEnd(){return isAtEnd(0);}
  private boolean isAtEnd(int howFar){
    return current + howFar >= source.length();
  }

  private void scanToken() {
    char c = advance();
    switch (c) {
      case '(': addToken(LEFT_PAREN); break;
      case ')': addToken(RIGHT_PAREN); break;
      case '[': addToken(LEFT_SQUARE); break;
      case ']': addToken(RIGHT_SQUARE); break;
      case '{': addToken(LEFT_BRACE); break;
      case '}': addToken(RIGHT_BRACE); break;
      case ';': addToken(SEMICOLON); break;
      case ':': addToken(COLON); break;
      case '+': addToken(PLUS); break;
      case '@': addToken(AT); break;
      case '~': addToken(TILDE); break;
      case '=':
        addToken(match('=') ? EQUAL_EQUAL : EQUAL);
        break;
      case '<':
        addToken(match('-') ? LEFT_ARROW : LESS);
        break;
      case '>':
        addToken(match('=') ? GREATER_EQUAL : GREATER);
        break;
      case '!':
        if (match('=')) {
          addToken(BANG_EQUAL);
        } else {
          Lox.error(line, "Unexpected character.");
        }
        break;
      case '/':
        if (match('/')) {
          while (peek() != '\n' && !isAtEnd()) advance();
        } else {
          Lox.error(line, "Unexpected character.");
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
      default:
        if (isDigit(c)){
          number();
        } else if (c == 'o' && isOctDigit(peek())){
          octal();
        } else if (isAlpha(c)) {
          identifier();
        } else {
          Lox.error(line, "Unexpected character.");
        }
        break;
    }
  }

  private char advance() {
    return source.charAt(current++);
  }

  private void addToken(TokenType type) {
    addToken(type, null);
  }

  private void addToken(TokenType type, Object literal) {
    String text = source.substring(start, current);
    tokens.add(new Token(type, text, literal, line));
  }

  private boolean match(char expected) {
    if (isAtEnd()) return false;
    if (source.charAt(current) != expected) return false;

    current++;
    return true;
  }

  private char peek(){ return peek(0);}
  private char peek(int howFar){
    if (isAtEnd(howFar)) return '\0';
    return source.charAt(current + howFar);
  }

  private boolean isDigit(char c) {
    return c >= '0' && c <= '9';
  }
  private boolean isOctDigit(char c) {
    return c >= '0' && c <= '7';
  }

  private void number() {
    while (isDigit(peek())) advance();

    if (peek() == '.' && isDigit(peek(1))) {
      advance();
      while (isDigit(peek())) advance();
    }

    addToken(NUMBER,
        Double.parseDouble(source.substring(start, current)));
  }

  private void octal() {
    while (isOctDigit(peek())) advance();
    addToken(NUMBER, Integer.parseInt(source.substring(start+1, current), 8));
  }

  private void identifier() {
    while (isAlphaNumeric(peek())) advance();
    String text = source.substring(start, current);
    addToken(keywords.getOrDefault(text, IDENTIFIER));
  }

  private boolean isAlpha(char c) {
    return (c >= 'a' && c <= 'z') ||
           (c >= 'A' && c <= 'Z') ||
            c == '_';
  }

  private boolean isAlphaNumeric(char c) {
    return isAlpha(c) || isDigit(c);
  }
}
