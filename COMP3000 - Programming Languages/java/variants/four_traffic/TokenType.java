package variants.four_traffic;

enum TokenType {
  MERGE,        // >>
  ROUTE,        // ->
  INTERSECTION, // @
  LANE,         // |
  LPAREN,       // (
  RPAREN,       // )
  IDENTIFIER,
  EOF
}
