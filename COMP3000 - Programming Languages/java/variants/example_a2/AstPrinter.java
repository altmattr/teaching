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
  public String visitDamDeclStmt(Stmt.DamDecl stmt) {
    return parenthesize("dam " + stmt.name.lexeme );
  }

  @Override
  public String visitIfStmt(Stmt.If stmt) {
    StringBuilder builder = new StringBuilder();
    builder.append(parenthesize("if", stmt.condition)).append("\n");
    builder.append("  then: ").append(stmt.thenBranch != null ? stmt.thenBranch.accept(this) : "null").append("\n");
    if (stmt.elseBranch != null) {
      builder.append("  else: ").append(stmt.elseBranch.accept(this));
    }
    return builder.toString().trim();
  }

  @Override
  public String visitReturnStmt(Stmt.Return stmt) {
    return parenthesize("return", stmt.value);
  }

  @Override
  public String visitBlockStmt(Stmt.Block stmt) {
    StringBuilder builder = new StringBuilder("[block");
    for (Stmt s : stmt.statements) {
      builder.append("\n  ").append(s.accept(this));
    }
    builder.append("\n]");
    return builder.toString();
  }

  @Override
  public String visitNumberExpr(Expr.Number expr) {
    return Double.toString(expr.value);
  }

  @Override
  public String visitBoolExpr(Expr.Bool expr) {
    return Boolean.toString(expr.value);
  }

  @Override
  public String visitInflowExpr(Expr.Inflow expr) {
    return "inflow";
  }

  @Override
  public String visitLevelExpr(Expr.Level expr) {
    return "level";
  }

}