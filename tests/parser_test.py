from compiler.parser import parse
from compiler.tokenizer import tokenize
from compiler.ast import BinaryOp, Literal, Identifier

def test_parser_expression() -> None:
  tokens = tokenize('3+4')
  assert parse(tokens) == BinaryOp(left=Literal(value=3), op='+', right=Literal(value=4))
  tokens = tokenize('4-7')
  assert parse(tokens) == BinaryOp(left=Literal(value=4), op='-', right=Literal(value=7))

def test_parser_term() -> None:
  tokens = tokenize('foo*4')
  assert parse(tokens) == BinaryOp(left=Identifier(name='foo'), op='*', right=Literal(value=4))
  tokens = tokenize('3/bar')
  assert parse(tokens) == BinaryOp(left=Literal(value=3), op='/', right=Identifier(name='bar'))