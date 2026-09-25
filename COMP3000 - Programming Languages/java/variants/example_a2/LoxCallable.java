package variants.example_a2;

import java.util.List;

interface LoxCallable extends Value{
  int arity();
  Flow call(Interpreter interpreter, List<Flow> arguments);
}