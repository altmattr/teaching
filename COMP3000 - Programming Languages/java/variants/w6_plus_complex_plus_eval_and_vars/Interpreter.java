package variants.w6_plus_complex_plus_eval_and_vars;

import java.util.List;
import java.util.Map;

class Interpreter implements Expr.Visitor<Flow>,
                             Stmt.Visitor<Void> {
  private Environment environment = new Environment();

  private Flow evaluate(Expr expr) {
    return expr.accept(this);
  }

  private void execute(Stmt stmt){
    stmt.accept(this);
  }

  Map<String,Flow> interpret(List<Stmt> program) { 
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
  public Void visitVarStmt(Stmt.Var stmt) {
    Flow value = null;
    if (stmt.initializer != null) {
      value = evaluate(stmt.initializer);
    }

    environment.define(stmt.name.lexeme, value);
   return null;
  }

  @Override
  public Flow visitGroupingExpr(Expr.Grouping expr) {
    return evaluate(expr.expression);
  }

  private boolean isTruthy(Object object) {
    if (object == null) return false;
    if (object instanceof Boolean) return (boolean)object;
    return true;
  }

  @Override
  public Flow visitUnaryExpr(Expr.Unary expr) {
    Flow right = evaluate(expr.right);
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
  public Flow visitBinaryExpr(Expr.Binary expr) {
    Flow left = evaluate(expr.left);
    Flow right = evaluate(expr.right); 

    switch (expr.operator.type) {
      case PLUS:
        return left.plus((Flow)right);
      case LEFT_ARROW:
        return left.addUpstream((Flow)right);
    }
    // Unreachable.
    return null;
  }

  @Override
  public Flow visitVariableExpr(Expr.Variable expr) {
    return environment.get(expr.name);
  }

  @Override
  public Flow visitAssignExpr(Expr.Assign expr){
    Flow value = evaluate(expr.value);
    environment.assign(expr.name, value);
    return value;
  }    

  @Override
  public Flow visitFlowExpr(Expr.Flow expr) {
    // this is where all the action is, well we actually hide it in Flow.java but once we force that, we work our way through everything else
    return new Flow(expr.mean, expr.variance, expr.magnitude);
  }
}
