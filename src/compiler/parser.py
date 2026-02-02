from compiler.Token import Token
from compiler import ast

def parse(tokens: list[Token]) -> ast.Expression:
  # This keeps track of which token we're looking at.
  pos = 0

  # 'peek()' returns the token at 'pos',
  # or a special 'end' token if we're past the end
  # of the token list.
  # This way we don't have to worry about going past
  # the end elsewhere.
  def peek() -> Token:
    if pos < len(tokens):
      return tokens[pos]
    return Token(
      loc=tokens[-1].loc,
      type="end",
      text="",
      )

    # 'consume()' returns the token at 'pos'
    # and increments 'pos' by one.
    #
    # If the optional parameter 'expected' is given,
    # it checks that the token being consumed has that text.
    # If 'expected' is a list, then the token must have
    # one of the texts in the list.
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

  def parse_identifier() -> ast.Identifier:
    if peek().type != 'identifier':
      raise Exception(f'{peek().loc}: expected an identifier')
    token = consume()
    if peek().text == "(":
      func = parse_function(ast.Identifier(str(token.text)))
      return func
    return ast.Identifier(str(token.text))

  # This is our main parsing function for this example.
  # To parse "integer + integer" expressions,
  # it uses `parse_int_literal` to parse the first integer,
  # then it checks that there's a supported operator,
  # and finally it uses `parse_int_literal` to parse the
  # second integer.
  def parse_expression() -> ast.Expression:
    # Parse the first term.
    left = parse_term()

    # While there are more `+` or '-'...
    while peek().text in ['+', '-']:
      # Move past the '+' or '-'.
      operator_token = consume()
      operator = operator_token.text

      # Parse the operator on the right.
      right = parse_term()

      # Combine it with the stuff we've
      # accumulated on the left so far.
      left = ast.BinaryOp(
        left,
        operator,
        right
      )


    return left


  def parse_term() -> ast.Expression:
    # Same structure as in 'parse_expression',
    # but the operators and function calls differ.
    left = parse_factor()
    while peek().text in ['*', '/']:
      operator_token = consume()
      operator = operator_token.text
      right = parse_factor()
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
