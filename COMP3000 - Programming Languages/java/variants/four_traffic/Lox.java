package variants.four_traffic;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class Lox {
  static boolean hadError = false;

  public static void main(String[] args) throws IOException {
    boolean debug = false;
    String path = null;

    for (String arg : args) {
      if (arg.equals("--debug")) {
        debug = true;
      } else {
        path = arg;
      }
    }

    if (path != null) {
      runFile(path, debug);
    } else {
      runPrompt(debug);
    }
  }

  private static void runFile(String path, boolean debug) throws IOException {
    byte[] bytes = Files.readAllBytes(Paths.get(path));
    run(new String(bytes, Charset.defaultCharset()), debug);
    if (hadError) System.exit(65);
  }

  private static void runPrompt(boolean debug) throws IOException {
    InputStreamReader input = new InputStreamReader(System.in);
    BufferedReader reader = new BufferedReader(input);

    for (;;) {
      System.out.print("> ");
      String line = reader.readLine();
      if (line == null) break;
      run(line, debug);
      hadError = false;
    }
  }

  private static void run(String source, boolean debug) {
    Scanner scanner = new Scanner(source, debug);
    List<Token> tokens = scanner.scanTokens();

    for (Token token : tokens) {
      System.out.println(token);
    }
  }

  static void error(int line, String message) {
    System.err.println("[line " + line + "] Error: " + message);
    hadError = true;
  }
}
