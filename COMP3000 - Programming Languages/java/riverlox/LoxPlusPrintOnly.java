package riverlox;


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
