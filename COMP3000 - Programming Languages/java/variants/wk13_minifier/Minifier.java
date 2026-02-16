package variants.wk13_minifier;
import java.util.HashMap;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;

// the minifier takes the ast and returns a new ast with names minimised
class Minifier implements Expr.Visitor<Expr>, Stmt.Visitor<Stmt> {
    public List<Stmt> minify(List<Stmt> ast){
        List<Stmt> newAst = new ArrayList<Stmt>();
        for (Stmt statement : ast){
            newAst.add(statement.accept(this));
        }
        return newAst;
    }

    Map<String, String> nameMap =  new HashMap<String, String>();
    int nameCounter = 0;
    public String nextName(){
        String name = "v" + nameCounter;
        nameCounter += 1;
        return name;
    }

    public Stmt visitBlockStmt(Stmt.Block stmt)          {return passToParts();}
    public Stmt visitExpressionStmt(Stmt.Expression stmt){return passToParts();}
    public Stmt visitFunctionStmt(Stmt.Function stmt)    {return passToParts();}
    public Stmt visitIfStmt(Stmt.If stmt)                {return passToParts();}
    public Stmt visitPrintStmt(Stmt.Print stmt)          {return passToParts();}
    public Stmt visitReturnStmt(Stmt.Return stmt)        {return passToParts();}
    public Stmt visitVarStmt(Stmt.Var stmt)              {
        String newName = nextName();
        nameMap.put(stmt.name.lexeme, newName);
        stmt.name.lexeme = newName;
        return stmt.accept(this);
    }
    public Stmt visitWhileStmt(Stmt.While stmt)          {return passToParts();}

    public Expr visitAssignExpr(Expr.Assign expr)        {return passToParts();}
    public Expr visitBinaryExpr(Expr.Binary expr)        {return passToParts();}
    public Expr visitCallExpr(Expr.Call expr)            {return passToParts();}
    public Expr visitLogicalExpr(Expr.Logical expr)      {return passToParts();}
    public Expr visitGroupingExpr(Expr.Grouping expr)    {return passToParts();}
    public Expr visitLiteralExpr(Expr.Literal expr)      {return passToParts();}
    public Expr visitUnaryExpr(Expr.Unary expr)          {return passToParts();}
    public Expr visitVariableExpr(Expr.Variable expr)    {
        expr.name.lexeme = nameMap.get(expr.name);
        return expr.accept(this);
    }
} 
