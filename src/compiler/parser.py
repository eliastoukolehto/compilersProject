from compiler.Token import Token
from compiler import ast

precedence_levels = [
  ['='],
  ['or'],
  ['and'],
  ['==', '!='],
  ['<', '<=', '>', '>='],
  ['+', '-'],
  ['*', '/', '%'],
]

MAX_LEVEL = len(precedence_levels)-1

right_associative_binary_operators = ['=']

unary_operators = ['not', '-']

def parse(tokens: list[Token]) -> ast.Expression:
  # This keeps track of which token we're looking at.
  pos = 0

  def peek() -> Token:
    if pos < len(tokens):
      return tokens[pos]
    return Token(
      loc=tokens[-1].loc,
      type="end",
      text="",
      )

  def consume(expected: str | list[str] | None = None) -> Token:
    nonlocal pos # Python's "nonlocal" lets us modify `pos`
                  # without creating a local variable of the same name.
    token = peek()
    if isinstance(expected, str) and token.text != expected:
      raise Exception(f'{token.loc}: expected "{expected}"')
    if isinstance(expected, list) and token.text not in expected:
      comma_separated = ", ".join([f'"{e}"' for e in expected])
      raise Exception(f'{token.loc}: expected one of: {comma_separated}')
    pos += 1
    return token

  # This is the parsing function for integer literals.
  # It checks that we're looking at an integer literal token,
  # moves past it, and returns a 'Literal' AST node
  # containing the integer from the token.
  def parse_int_literal() -> ast.Literal:
    if peek().type != 'int_literal':
      raise Exception(f'{peek().loc}: expected an integer literal')
    token = consume()
    return ast.Literal(int(token.text))

  def parse_identifier() -> ast.Expression:
    if peek().type != 'identifier':
      raise Exception(f'{peek().loc}: expected an identifier')
    token = consume()
    if peek().text == "(":
      func = parse_function(ast.Identifier(str(token.text)))
      return func
    return ast.Identifier(str(token.text))

  def parse_expression(level: int = 0) -> ast.Expression:
    if level >= MAX_LEVEL:
      left = parse_factor()
    else:
      left = parse_expression(level+1)
    while level <= MAX_LEVEL and peek().text in precedence_levels[level]:
      operator_token = consume()
      operator = operator_token.text


      if operator in right_associative_binary_operators:
        right = parse_expression()
      else:
        right = parse_expression(level+1)

      left = ast.BinaryOp(
        left,
        operator,
        right
      )
    return left

  def parse_factor() -> ast.Expression:
    if peek().text == '(':
      return parse_parenthesized()
    if peek().text == 'if':
      return parse_if_statement()
    if peek().text in unary_operators:
      return parse_unary()
    if peek().text == '{':
      return parse_block()
    if peek().type == 'int_literal':
      return parse_int_literal()
    if peek().type == 'identifier':
      return parse_identifier()

    raise Exception(f'{peek().loc}: expected "(", an integer literal or an identifier')

  def parse_if_statement() -> ast.Expression:
    consume('if')
    cond = parse_expression()
    consume('then')
    then = parse_expression()
    if peek().text == 'else':
      consume('else')
      els = parse_expression()
    else:
      els = None
    return ast.IfStatement(
      cond,
      then,
      els
    )

  def parse_unary() -> ast.Unary:
    token = consume()
    op = token.text
    right = parse_expression()
    return ast.Unary(
      op,
      right,
    )

  def parse_block() -> ast.Block:
    statements = []
    result = None
    consume('{')

    while True:
      if peek().text == '}':
        consume('}')
        if peek().text == ';':
          consume(';')
        break
      expr = parse_expression()
      if peek().text == ';':
        consume(';')
        statements.append(expr)
      else:
        result = expr

    return ast.Block(
      statements,
      result
    )

  def parse_function(identifier: ast.Identifier) -> ast.Expression:
    args = []
    consume('(')
    while True:
      expr = parse_expression()
      args.append(expr)
      if peek().text == ',':
        consume(',')
      else:
        consume(')')
        break
    return ast.Function(
      name=identifier,
      args=args
    )

  def parse_parenthesized() -> ast.Expression:
    consume('(')
    # Recursively call the top level parsing function
    # to parse whatever is inside the parentheses.
    expr = parse_expression()
    consume(')')
    return expr

  def start_parser() -> ast.Expression:
    if len(tokens) == 0:
      raise Exception("expected non-empty token list")

    expression = parse_expression()

    if pos < len(tokens):
      raise Exception(f'{peek().loc}: token was not parsed')
    return expression

  return start_parser()
