package variants.example_a2;

import java.util.List;

class LoxDam implements LoxCallable {
  private final Token name;
  private final List<Stmt> body;
  private final Environment closure;

  LoxDam(Token name, List<Stmt> body, Environment closure) {
    this.name = name;
    this.body = body;
    this.closure = closure;
  }

  @Override
  public Flow call(Interpreter interpreter,
                     List<Flow> arguments) {
    Flow upstream = arguments.get(0);
    double level = 0.0;
    double[] output = new double[10];

    for (int i = 0; i < 10; i++) {
      Environment env = new Environment(closure);
      env.define("inflow", new Number(upstream.prediction[i]));
      env.define("level", new Number(level));

      try {
        interpreter.executeBlock(body, env);
      } catch (Return returnValue) {
        if (returnValue.value instanceof Number) {
          output[i] = ((Number)returnValue.value).value;
        } else if (returnValue.value instanceof Flow) {
          output[i] = ((Flow)returnValue.value).prediction[0];
        }
      }
      level += upstream.prediction[i] - output[i];
    }

    return new Flow(output);
  }

  @Override
  public int arity() {
    return 1;
  }

  @Override
  public String toString() {
    return "<dam " + name.lexeme + ">";
  }
}
