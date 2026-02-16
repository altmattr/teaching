package weeks.nine;


import java.util.List;
import static weeks.nine.TokenType.*;

public class LoxPlusIncrement extends Lox{
  public static void main(String[] args){
    new LoxPlusIncrement().run("var x = 0; x++; print(x);");
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
    @Override
    Expr assignment() {
      Expr expr = or();

      if (match(EQUAL)) {
        Token equals = previous();
        Expr value = assignment();

        if (expr instanceof Expr.Variable) {
          Token name = ((Expr.Variable)expr).name;
          return new Expr.Assign(name, value);
        }

        error(equals, "Invalid assignment target."); 
      }
      System.out.println("we found an expression, now looking for PLUS");
      if (match(PLUS)){
        System.out.println("we found a PLUS, now looking for another PLUS");
        if (match(PLUS)){
          if (expr instanceof Expr.Variable) {
            Token plus = previous();
            Token name = ((Expr.Variable)expr).name;
            return new Expr.Assign(name,
                                   new Expr.Binary(new Expr.Variable(name),
                                                   plus,
                                                   new Expr.Literal(1)
                                                  )
                                   );
          }
        }
      }
      System.out.println("passed over assignment");
      return expr;
    }

  }

  private class AdjustedInterpreter extends Interpreter{
  }
}
