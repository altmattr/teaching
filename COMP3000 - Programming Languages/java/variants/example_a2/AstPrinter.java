package variants.example_a2;

import java.util.List;

class AstPrinter implements Expr.Visitor<String>, Stmt.Visitor<String> {
  String print(List<Stmt> program) {
    String ret = "";
    for (Stmt stmt : program){
      ret = ret + stmt.accept(this)+"\n";
    }
    return ret;
  }

  @Override
  public String visitExpressionStmt(Stmt.Expression stmt){
    return parenthesize(";", stmt.expression);
  }

  @Override 
  public String visitVarStmt(Stmt.Var stmt){
    if (stmt.initializer != null) {
      return parenthesize("var " + stmt.name.lexeme + " =", stmt.initializer);
    }
    return parenthesize("var " + stmt.name.lexeme); 
  }

  @Override
  public String visitPlotStmt(Stmt.Plot stmt){
    return parenthesize("plot", stmt.expression);
  }


  @Override
  public String visitPrintStmt(Stmt.Print stmt){
    return parenthesize("print", stmt.expression);
  }
  @Override
  public String visitAssignExpr(Expr.Assign expr) {
    return parenthesize(expr.name.lexeme + " : " , expr.value);
  }

  @Override
  public String visitBinaryExpr(Expr.Binary expr) {
    return parenthesize(expr.operator.lexeme,
                        expr.left, expr.right);
  }

  @Override
  public String visitGroupingExpr(Expr.Grouping expr) {
    return parenthesize("group", expr.expression);
  }


  @Override
  public String visitFlowExpr(Expr.Flow expr) {
    return "[" + Double.toString(expr.mean) + "~" + Double.toString(expr.variance) + "]@" + Double.toString(expr.magnitude);
  }

  @Override
  public String visitUnaryExpr(Expr.Unary expr) {
    return parenthesize(expr.operator.lexeme, expr.right);
  }

  @Override
  public String visitVariableExpr(Expr.Variable expr) {
    return expr.name.lexeme;
  }

  private String parenthesize(String name, Expr... exprs) {
    StringBuilder builder = new StringBuilder();

    builder.append("(").append(name);
    for (Expr expr : exprs) {
      builder.append(" ");
      builder.append(expr.accept(this));
    }
    builder.append(")");

    return builder.toString();
  }

  @Override
  public String visitFunctionStmt(Stmt.Function stmt) {
    return parenthesize("fun " + stmt.name.lexeme );
  }

  @Override
  public String visitIfStmt(Stmt.If stmt) {
    return parenthesize("if", stmt.condition);// TODO: you can't see the then and else branches here but that's ok or the ast printout is too big
  }

  @Override
  public String visitReturnStmt(Stmt.Return stmt) {
    return parenthesize("return", stmt.value);
  }

  @Override
  public String visitBlockStmt(Stmt.Block stmt) {
    return "block of some variety";
  }

  @Override
  public String visitNumberExpr(Expr.Number expr) {
    return Double.toString(expr.value);
  }

  @Override
  public String visitBoolExpr(Expr.Bool expr) {
    return Boolean.toString(expr.value);
  }

}