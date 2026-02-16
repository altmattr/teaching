package variants.example_a2;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Map;

public class Lox {
  static boolean hadError = false;
  static boolean hadRuntimeError = false;


  public static void main(String[] args) throws IOException {
    if (args.length > 1) {
      System.out.println("Usage: Lox [script]");
      System.exit(64);
    } else if (args.length == 1) {
      runFile(args[0]);
      System.exit(0);
    } else {
      runPrompt();
    }

  }

  private static void runFile(String path) throws IOException {
    byte[] bytes = Files.readAllBytes(Paths.get(path));
    run(new String(bytes, Charset.defaultCharset()));
  }

  private static void runPrompt() throws IOException {
    InputStreamReader input = new InputStreamReader(System.in);
    BufferedReader reader = new BufferedReader(input);

    for (;;) {
      System.out.print("> ");
      String line = reader.readLine();
      if (line == null) break;
      run(line);
      hadError = false;
    }
  }

  private static void run(String source){
    Scanner scanner = new Scanner(source);
    List<Token> tokens = scanner.scanTokens();
    //System.out.println("-- tokens --");
    //System.out.println(tokens);
    Parser parser = new Parser(tokens);
    List<Stmt> program = parser.parse();
    if (hadError) return;
    System.out.println("-- AST --");
    System.out.println(new AstPrinter().print(program));
    System.out.println("-- Interpreter Output --");
    Map<String, Value> result = new Interpreter().interpret(program);
    // System.out.print("\033[2J");
    // for(int i = 0; i < 10; i++){
    //   System.out.print("\033[2J");
    //   for (String var: result.keySet()){
    //     System.out.print(String.format("%1$20s", var) + ": ");
    //     for (int j = 0; j < result.get(var).prediction[i]; j++){
    //       System.out.print(" ");
    //     }
    //     System.out.println("*");
    //   }
    //   try {
    //     Thread.sleep(500);
    //   } catch (InterruptedException e) {
    //     e.printStackTrace();
    //   }
    // }

    System.out.println("\n-- Result --");
    for (String var: result.keySet()){
      System.out.println(String.format("%1$20s", var) + ": " + result.get(var));
    }
  }

  public static void scan(String source, Scanner scanner){
    scanner.scanTokens().forEach(token -> System.out.println(token));
  }

  static void error(int line, String message) {
    report(line, "", message);
  }

  static void error(Token token, String message) {
    if (token.type == TokenType.EOF) {
      report(token.line, " at end", message);
    } else {
      report(token.line, " at '" + token.lexeme + "'", message);
    }
  }

  static void runtimeError(RuntimeError error) {
    System.err.println(error.getMessage() +
        "\n[line " + error.token.line + "]");
    hadRuntimeError = true;
  }


  private static void report(int line, String where,
                             String message) {
    System.err.println(
        "[line " + line + "] Error" + where + ": " + message);
    hadError = true;
  }
}
