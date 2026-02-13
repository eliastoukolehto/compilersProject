from compiler.parser import parse
from compiler.Token import Token
from compiler.Loc import L
from compiler.ast import BinaryOp, Literal, Identifier, IfStatement, Function, Unary, Block, Var

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

def test_if_statement() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='bar'),
    Token(loc=L, type='identifier', text='else'),
    Token(loc=L, type='identifier', text='baz')
  ]
  assert parse(tokens) == IfStatement(cond=Identifier(name='foo'), then=Identifier(name='bar'), els=Identifier(name='baz'))

def test_if_no_else() -> None: 
  tokens = [
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='bar'),
  ]
  assert parse(tokens) == IfStatement(cond=Identifier(name='foo'), then=Identifier(name='bar'), els = None)

def test_if_fails_correctly() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='identifier', text='else'),
    Token(loc=L, type='identifier', text='baz')
  ]
  try:
    parse(tokens)
  except Exception as e:
    assert e.args[0] == "(0, 0): expected \"then\""

def test_nested_if() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='bar'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='baz')
  ]
  assert parse(tokens) == IfStatement(cond=IfStatement(cond=Identifier(name='foo'), then=Identifier(name='bar'), els = None), then=Identifier(name='baz'), els = None)

def test_if_as_expression() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='bar'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='baz')
  ]
  assert parse(tokens) == BinaryOp(left=Identifier(name='foo'), op='+', right=IfStatement(cond=Identifier(name='bar'), then=Identifier(name='baz'), els = None))

def test_function() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='f'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='identifier', text='x'),
    Token(loc=L, type='punctuation', text=','),
    Token(loc=L, type='identifier', text='y'),
    Token(loc=L, type='operatror', text='+'),
    Token(loc=L, type='identifier', text='z'),
    Token(loc=L, type='punctuation', text=')'),
  ]
  assert parse(tokens) == Function(name=Identifier(name='f'), args=[Identifier(name='x'), BinaryOp(left=Identifier(name='y'), op='+', right=Identifier(name='z'))]) 


def test_unary_operators() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='identifier', text='and'),
    Token(loc=L, type='identifier', text='not'),
    Token(loc=L, type='identifier', text='bar')
  ]
  assert parse(tokens) == BinaryOp(left=Identifier(name='foo'), op='and', right=Unary(op='not', right=Identifier(name='bar')))

def test_rigt_associative_assignment() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='c')
  ]
  assert parse(tokens) == BinaryOp(left=Identifier(name='a'), op='=', right=BinaryOp(left=Identifier(name='b'), op='=', right=Identifier(name='c')))

def test_code_block() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='f'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text=')'),
    Token(loc=L, type='punctuation', text=';'),
    Token(loc=L, type='identifier', text='x'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='y'),
    Token(loc=L, type='punctuation', text=';'),
    Token(loc=L, type='identifier', text='f'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='identifier', text='x'),
    Token(loc=L, type='punctuation', text=')'),
    Token(loc=L, type='punctuation', text='}'),
  ]
  assert parse(tokens) == Block(statements=[
    Function(name=Identifier(name='f'), args=[Identifier(name='a')]),
    BinaryOp(left=Identifier(name='x'), op='=', right=Identifier(name='y'))
    ],
    result=Function(name=Identifier(name='f'), args=[Identifier(name='x')]))

def test_block_result_none() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='punctuation', text=';'),
    Token(loc=L, type='identifier', text='bar'),
    Token(loc=L, type='punctuation', text=';'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='punctuation', text=';')
  ]
  assert parse(tokens) == Block(statements=[Identifier(name='foo'), Identifier(name='bar')], result=None)

def test_block_missing_semicolon() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='identifier', text='bar'),
    Token(loc=L, type='punctuation', text=';'),
    Token(loc=L, type='punctuation', text='}'),
  ]
  try:
    parse(tokens)
  except Exception as e:
    assert e.args[0] == "(0, 0): expected \"(\", an integer literal or an identifier"


def test_var_in_beginning() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='var'),
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='bar')
  ]
  assert parse(tokens) == Var(val=Identifier(name='foo'), init=Identifier(name='bar'))

def test_invalid_var_placement() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='var'),
    Token(loc=L, type='identifier', text='bar'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='baz')
  ]
  try:
    parse(tokens)
  except Exception as e:
    assert e.args[0] == "(0, 0): \"var\" is only allowed directly inside blocks {} and in top-level expressions"


