package variants.example_a2;

import java.util.ArrayList;
import java.util.List;

import static variants.example_a2.TokenType.*;

/**
 * implements the following grammar
 * program   -> declaration* EOF;
 * declaration -> varDecl
 *             |  plotDecl
 *             |  funDecl
 *             |  statement;
 * statement -> exprStmt
 *           |  returnStmt
 *           |  ifStmt
 * exprStmt  -> expression ";";
 * ifStmt    -> "if" "(" expression ")" statement
               ( "else" statement )? ;
 * varDecl   -> "var" IDENTIFIER ( "=" expression )? ";"; 
 * plotDecl  -> "plot" expression ";";  
 * expression     -> assignment;
 * assignment     -> IDENTIFIER "=" assignment
 *                | logic_or;
 * 
 * expression -> mini_term (op mini_term)*;
 * op -> PLUS | LEFT_ARROW | GREATER_THAN | LESS_THAN | EQUAL_EQUAL | BANG_EQUAL;
 * mini_term  -> flow | "(" expression ")" ;
 * flow -> "[" NUMBER "~" NUMBER "]" "@" NUMBER
 *      |  IDENTIFIER
 *      |  NUMBER
 *      |  STRING
 *      |  "true" | "false" | "nil" ;
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
      if (match(VAR)) return varDeclaration();
      if (match(PLOT))return plotDeclaration();
      if (match(FUN)) return function("function");
      return statement();
    } catch (ParseError error) {
      synchronize();
      return null;
    }
  }

   Stmt.Function function(String kind) {
    Token name = consume(IDENTIFIER, "Expect " + kind + " name.");
    consume(LEFT_PAREN, "Expect '(' after " + kind + " name.");
    List<Token> parameters = new ArrayList<>();
    if (!check(RIGHT_PAREN)) {
      do {
        if (parameters.size() >= 255) {
          error(peek(), "Can't have more than 255 parameters.");
        }

        parameters.add(
            consume(IDENTIFIER, "Expect parameter name."));
      } while (match(COMMA));
    }
    consume(RIGHT_PAREN, "Expect ')' after parameters.");
    consume(LEFT_BRACE, "Expect '{' before " + kind + " body.");
    List<Stmt> body = block();
    return new Stmt.Function(name, parameters, body);
  }

  Stmt statement() {
    try{
      if (match(IF)) return ifStatement();
      if (match(RETURN)) return returnStatement();
      if (match(LEFT_BRACE)) return new Stmt.Block(block());
      return expressionStatement();
    } catch (ParseError error) {
      synchronize();
      return null;
    }
  }

  Stmt ifStatement() {
    consume(LEFT_PAREN, "Expect '(' after 'if'.");
    Expr condition = expression();
    consume(RIGHT_PAREN, "Expect ')' after if condition."); 

    Stmt thenBranch = statement();
    Stmt elseBranch = null;
    if (match(ELSE)) {
      elseBranch = statement();
    }

    return new Stmt.If(condition, thenBranch, elseBranch);
  }

   List<Stmt> block() {
    List<Stmt> statements = new ArrayList<>();

    while (!check(RIGHT_BRACE) && !isAtEnd()) {
      statements.add(declaration());
    }

    consume(RIGHT_BRACE, "Expect '}' after block.");
    return statements;
  }
  private Stmt returnStatement() {
    Token keyword = previous();
    Expr value = null;
    if (!check(SEMICOLON)) {
      value = expression();
    }

    consume(SEMICOLON, "Expect ';' after return value.");
    return new Stmt.Return(keyword, value);
  }
  Stmt expressionStatement() {
    Expr expr = expression();
    consume(SEMICOLON, "Expect ';' after expression.");
    return new Stmt.Expression(expr);
  }

  Stmt plotDeclaration() {
    Expr expr = expression();
    consume(SEMICOLON, "Expect ';' after plot statement.");
    return new Stmt.Plot(expr);
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
      while(match(PLUS, LEFT_ARROW, GREATER, GREATER_EQUAL, LESS, LESS_EQUAL, EQUAL_EQUAL, BANG_EQUAL)){
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
      if (match(NUMBER)){
          return new Expr.Number(Double.parseDouble(previous().lexeme));
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