package variants.w6_plus_complex_plus_eval_and_vars;

import java.util.ArrayList;
import java.util.List;

import static variants.w6_plus_complex_plus_eval_and_vars.TokenType.*;

/**
 * implements the following grammar
 * program   -> declaration* EOF;
 * declaration -> varDecl
 *             |  statement;
 * statement -> exprStmt
 * exprStmt  -> expression ";";
 * varDecl   -> "var" IDENTIFIER ( "=" expression )? ";"; 
 * expression     -> assignment;
 * assignment     -> IDENTIFIER "=" assignment
 *                | expression;
 * expression -> mini_term (op mini_term)*;
 * op -> PLUS | LEFT_ARROW;
 * mini_term  -> flow | "(" expression ")" ;
 * flow -> "[" NUMBER "~" NUMBER "]" "@" NUMBER
 *      | IDENTIFIER;
 */

class Parser {
  private static class ParseError extends RuntimeException {}
  private final List<Token> tokens;
  private int current = 0;
  
  Parser(List<Token> tokens){
      this.tokens = tokens;
  }
  
  List<Stmt> parse() {
    List<Stmt> statements = new ArrayList<Stmt>();
    while (!isAtEnd()) {
      statements.add(declaration());
    }

    return statements; 
  }

  Stmt declaration() {
    try {
      if (match(VAR)) 
        return varDeclaration();
      return statement();
    } catch (ParseError error) {
      synchronize();
      return null;
    }
  }

  Stmt statement() {
    return expressionStatement();
  }

  Stmt expressionStatement() {
    Expr expr = expression();
    consume(SEMICOLON, "Expect ';' after expression.");
    return new Stmt.Expression(expr);
  }

  Stmt varDeclaration() {
    Token name = consume(IDENTIFIER, "Expect variable name.");

    Expr initializer = null;
    if (match(EQUAL)) {
      initializer = expression();
    }

    consume(SEMICOLON, "Expect ';' after variable declaration.");
    return new Stmt.Var(name, initializer);
  }

  private Expr expression(){
      Expr expr = mini_term();
      while(match(PLUS, LEFT_ARROW)){
          Token operator = previous();
          Expr right = mini_term();
          expr = new Expr.Binary(expr, operator, right);
      }
      return expr;
  }

  private Expr mini_term(){
      if (match(LEFT_PAREN)){
          Expr expr = expression();
          consume(RIGHT_PAREN, "Expect ')' after expression.");
          return new Expr.Grouping(expr);
      } else {
          return flow();
      }
  }

  private Expr flow(){
      if (match(LEFT_SQUARE)){
          double mean = Double.parseDouble(consume(NUMBER, "Expect mean after '['.").lexeme);
          consume(TILDE, "Expect '~' after mean.");
          double variance = Double.parseDouble(consume(NUMBER, "Expect variance after '~'.").lexeme);
          consume(RIGHT_SQUARE, "Expect ']' after variance.");
          consume(AT, "Expect '@' after ']'.");
          double magnitude = Double.parseDouble(consume(NUMBER, "Expect magnitude after '@'.").lexeme);
          return (new Expr.Flow(mean, variance, magnitude));
      }
      if (match(IDENTIFIER)){
          return new Expr.Variable(previous());
      }
      throw error(peek(), "Expect flow expression.");
  }

  private boolean match(TokenType... types) {
    for (TokenType type : types) {
      if (check(type)) {
        advance();
        return true;
      }
    }

    return false;
  }

  private boolean check(TokenType type) {
    if (isAtEnd()) return false;
    return peek().type == type;
  }

  private Token advance() {
    if (!isAtEnd()) current++;
    return previous();
  }

  private boolean isAtEnd() {
    return peek().type == EOF;
  }

  private Token peek() {
    return tokens.get(current);
  }

  private Token previous() {
    return tokens.get(current - 1);
  }

  private Token consume(TokenType type, String message) {
    if (check(type)) return advance();

    throw error(peek(), message);
  }

  private ParseError error(Token token, String message) {
    Lox.error(token, message);
    return new ParseError();
  }

  private void synchronize() {
    advance();

    while (!isAtEnd()) {
      if (previous().type == SEMICOLON) return;

      switch (peek().type) {
        case CLASS:
        case FUN:
        case VAR:
        case FOR:
        case IF:
        case WHILE:
        case PRINT:
        case RETURN:
          return;
      }

      advance();
    }
  }
}