package variants.example_a2;

enum TokenType {
  // Single-character tokens.
  LEFT_PAREN, RIGHT_PAREN, LEFT_SQUARE, RIGHT_SQUARE, LEFT_BRACE, RIGHT_BRACE,
  SEMICOLON, AT, TILDE, COLON, PLUS,

  // One or two character tokens.
  BANG_EQUAL,
  EQUAL, EQUAL_EQUAL,
  GREATER, GREATER_EQUAL,
  LESS, LESS_EQUAL, LEFT_ARROW,

  // Literals.
  IDENTIFIER, NUMBER,

  // Keywords.
  ELSE, IF, RETURN, VAR, PLOT,
  DAM, WHEN, DEFAULT, INFLOW, LEVEL,
  TRUE, FALSE,

  EOF

}
