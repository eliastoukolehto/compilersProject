from compiler.parser import parse
from compiler.Token import Token
from compiler.Loc import L
from compiler.ast import BinaryOp, Literal, Identifier

def test_parser_expression() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='3'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='4')
  ]
  assert parse(tokens) == BinaryOp(left=Literal(value=3), op='+', right=Literal(value=4))
  tokens = [
    Token(loc=L, type='int_literal', text='4'),
    Token(loc=L, type='operator', text='-'),
    Token(loc=L, type='int_literal', text='7')
  ]
  assert parse(tokens) == BinaryOp(left=Literal(value=4), op='-', right=Literal(value=7))

def test_parser_term() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='operator', text='*'),
    Token(loc=L, type='int_literal', text='4')
  ]
  assert parse(tokens) == BinaryOp(left=Identifier(name='foo'), op='*', right=Literal(value=4))
  tokens = [
    Token(loc=L, type='int_literal', text='3'),
    Token(loc=L, type='operator', text='/'),
    Token(loc=L, type='identifier', text='bar')
  ]
  assert parse(tokens) == BinaryOp(left=Literal(value=3), op='/', right=Identifier(name='bar'))

def test_parser_three() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='3'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='4'),
    Token(loc=L, type='operator', text='*'),
    Token(loc=L, type='int_literal', text='5')
  ]
  assert parse(tokens) == BinaryOp(left=Literal(value=3), op='+', right=BinaryOp(left=Literal(value=4), op='*', right=Literal(value=5)))
  tokens = [
    Token(loc=L, type='int_literal', text='3'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='4'),
    Token(loc=L, type='operator', text='-'),
    Token(loc=L, type='int_literal', text='5')
  ]
  assert parse(tokens) == BinaryOp(left=BinaryOp(left=Literal(value=3), op='+', right=Literal(value=4)), op='-', right=Literal(value=5))

def test_parser_junk() -> None:
  try:
    tokens = [
      Token(loc=L, type='int_literal', text='3'),
      Token(loc=L, type='operator', text='+'),
      Token(loc=L, type='int_literal', text='4'),
      Token(loc=L, type='int_literal', text='5')
    ]
    assert parse(tokens)
  except Exception as e:
    assert e.args[0] == "(0, 0): token was not parsed"

def test_empty_list() -> None:
  try:
    tokens: list[Token] = []
    assert parse(tokens)
  except Exception as e:
    assert e.args[0] == "expected non-empty token list"

def test_parser_parentheses() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='3'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='int_literal', text='4'),
    Token(loc=L, type='operator', text='-'),
    Token(loc=L, type='int_literal', text='5'),
    Token(loc=L, type='punctuation', text=')')
  ]
  assert parse(tokens) == BinaryOp(left=Literal(value=3), op='+', right=BinaryOp(left=Literal(value=4), op='-', right=Literal(value=5)))

def test_incomplete_parentheses() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='int_literal', text='4'),
    Token(loc=L, type='operator', text='-'),
    Token(loc=L, type='int_literal', text='5')
  ]
  try:
    parse(tokens) 
  except Exception as e:
    assert e.args[0] == "(0, 0): expected \")\""

def test_double_operator() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='4'),
    Token(loc=L, type='operator', text='-'),
    Token(loc=L, type='operator', text='-'),
    Token(loc=L, type='int_literal', text='5')
  ]
  try:
    parse(tokens)
  except Exception as e:
    assert e.args[0] == "(0, 0): expected \"(\", an integer literal or an identifier"
