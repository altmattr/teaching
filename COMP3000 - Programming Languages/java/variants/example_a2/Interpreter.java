package variants.example_a2;

import java.util.List;
import java.util.Map;

class Interpreter implements Expr.Visitor<Value>,
                             Stmt.Visitor<Void> {
  private Environment environment = new Environment();

  private Value evaluate(Expr expr) {
    return expr.accept(this);
  }

  private void execute(Stmt stmt){
    stmt.accept(this);
  }

  Map<String,Value> interpret(List<Stmt> program) { 
    try {
      for (Stmt statement: program){
        statement.accept(this); // execute statement
      }
      return environment.values;
    } catch (RuntimeError error) {
      Lox.runtimeError(error);
      return environment.values;
    }
  }

  private String stringify(Object object) {
    if (object == null) return "nil";

    if (object instanceof Double) {
      String text = object.toString();
      if (text.endsWith(".0")) {
        text = text.substring(0, text.length() - 2);
      }
      return text;
    }

    return object.toString();
  }

  @Override
  public Void visitExpressionStmt(Stmt.Expression stmt) {
    evaluate(stmt.expression);
    return null;
  }

  @Override
  public Void visitPlotStmt(Stmt.Plot stmt){
    Value value = evaluate(stmt.expression);
    if (value instanceof Flow){
    for (double flow: ((Flow)value).prediction){
      for(int i = 0; i < flow; i++){
        System.out.print(" ");
      }
      System.out.println("*");
    }
    }
    return null;
  }

  @Override
  public Void visitPrintStmt(Stmt.Print stmt){
    Value value = evaluate(stmt.expression);
    System.out.println(stringify(value));
    return null;
  }
  
  @Override
  public Void visitVarStmt(Stmt.Var stmt) {
    Value value = null;
    if (stmt.initializer != null) {
      value = evaluate(stmt.initializer);
    }

    environment.define(stmt.name.lexeme, value);
   return null;
  }

  @Override
  public Value visitGroupingExpr(Expr.Grouping expr) {
    return evaluate(expr.expression);
  }

  private boolean isTruthy(Object object) {
    if (object == null) return false;
    if (object instanceof Boolean) return (boolean)object;
    if (object instanceof Bool) return ((Bool)object).value;
    return true;
  }

  @Override
  public Value visitUnaryExpr(Expr.Unary expr) {
    Value right = evaluate(expr.right);
    return right;

  }
  
  private boolean isEqual(Object a, Object b) {
    if (a == null && b == null) return true;
    if (a == null) return false;

    return a.equals(b);
  }

  private void checkNumberOperand(Token operator, Object operand) {
    if (operand instanceof Double) return;
    throw new RuntimeError(operator, "Operand must be a number.");
  }

  private void checkNumberOperands(Token operator,
                                   Object left, Object right) {
    if (left instanceof Double && right instanceof Double) return;
    
    throw new RuntimeError(operator, "Operands must be numbers.");
  }

  @Override
  public Value visitBinaryExpr(Expr.Binary expr) {
    Value left = evaluate(expr.left);
    Value right = evaluate(expr.right); 

    switch (expr.operator.type) {
      case GREATER:
      System.out.println(((Number)left).value + " " + ((Number)right).value);
        return new Bool(((Number)left).value > ((Number)right).value);
      case LESS:
        return new Bool(((Number)left).value < ((Number)right).value);
      case PLUS:
        return ((Flow)left).plus((Flow)right);
      case LEFT_ARROW:
        if (left instanceof Flow){
         return ((Flow)left).addUpstream((Flow)right);
        }
        if (left instanceof LoxFunction){
          return ((LoxFunction)left).call(this, List.of((Flow)right));
        }
    }
    // Unreachable.
    return null;
  }

  @Override
  public Value visitVariableExpr(Expr.Variable expr) {
    return environment.get(expr.name);
  }

  @Override
  public Value visitAssignExpr(Expr.Assign expr){
    Value value = evaluate(expr.value);
    environment.assign(expr.name, value);
    return value;
  }    

  @Override
  public Flow visitFlowExpr(Expr.Flow expr) {
    // this is where all the action is, well we actually hide it in Flow.java but once we force that, we work our way through everything else
    return new Flow(expr.mean, expr.variance, expr.magnitude);
  }

  @Override
  public Void visitFunctionStmt(Stmt.Function stmt) {
    LoxFunction function = new LoxFunction(stmt, environment);
    environment.define(stmt.name.lexeme, function);
    environment.define(stmt.name.lexeme+"_level", new Number(0));
    return null;
  }

  @Override
  public Void visitBlockStmt(Stmt.Block stmt) {
    executeBlock(stmt.statements, new Environment(environment));
    return null;
  }
  void executeBlock(List<Stmt> statements,
                    Environment environment) {
    Environment previous = this.environment;
    try {
      this.environment = environment;

      for (Stmt statement : statements) {
        execute(statement);
      }
    } finally {
      this.environment = previous;
    }
  }
  @Override
  public Void visitIfStmt(Stmt.If stmt) {
    if (isTruthy(evaluate(stmt.condition))) {
      execute(stmt.thenBranch);
    } else if (stmt.elseBranch != null) {
      execute(stmt.elseBranch);
    }
    return null;
  }

  @Override
  public Void visitReturnStmt(Stmt.Return stmt) {
    Value value = null;
    if (stmt.value != null) value = evaluate(stmt.value);

    throw (new Return(value));
  }

  @Override
  public Value visitNumberExpr(Expr.Number expr) {
    return new Number(expr.value);
  }

  @Override
  public Value visitBoolExpr(Expr.Bool expr) {
    return new Bool(expr.value);
  }
}
