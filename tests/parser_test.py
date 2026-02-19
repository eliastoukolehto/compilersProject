from compiler.parser import parse
from compiler.Token import Token
from compiler.Loc import L, Loc
from compiler.ast import BinaryOp, Literal, Identifier, IfStatement, Function, Unary, Block, Var

def test_parser_expression() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='3'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='4')
  ]
  assert parse(tokens) == BinaryOp(L, left=Literal(L, value=3), op='+', right=Literal(L, value=4))
  tokens = [
    Token(loc=L, type='int_literal', text='4'),
    Token(loc=L, type='operator', text='-'),
    Token(loc=L, type='int_literal', text='7')
  ]
  assert parse(tokens) == BinaryOp(L, left=Literal(L, value=4), op='-', right=Literal(L, value=7))

def test_parser_term() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='operator', text='*'),
    Token(loc=L, type='int_literal', text='4')
  ]
  assert parse(tokens) == BinaryOp(L,left=Identifier(L,name='foo'), op='*', right=Literal(L,value=4))
  tokens = [
    Token(loc=L, type='int_literal', text='3'),
    Token(loc=L, type='operator', text='/'),
    Token(loc=L, type='identifier', text='bar')
  ]
  assert parse(tokens) == BinaryOp(L,left=Literal(L,value=3), op='/', right=Identifier(L,name='bar'))

def test_parser_three() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='3'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='4'),
    Token(loc=L, type='operator', text='*'),
    Token(loc=L, type='int_literal', text='5')
  ]
  assert parse(tokens) == BinaryOp(L,left=Literal(L,value=3), op='+', right=BinaryOp(L,left=Literal(L,value=4), op='*', right=Literal(L,value=5)))
  tokens = [
    Token(loc=L, type='int_literal', text='3'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='4'),
    Token(loc=L, type='operator', text='-'),
    Token(loc=L, type='int_literal', text='5')
  ]
  assert parse(tokens) == BinaryOp(L,left=BinaryOp(L,left=Literal(L,value=3), op='+', right=Literal(L,value=4)), op='-', right=Literal(L,value=5))

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
  assert parse(tokens) == BinaryOp(L,left=Literal(L,value=3), op='+', right=BinaryOp(L,left=Literal(L,value=4), op='-', right=Literal(L,value=5)))

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
  assert parse(tokens) == IfStatement(L,cond=Identifier(L,name='foo'), then=Identifier(L,name='bar'), els=Identifier(L,name='baz'))

def test_if_no_else() -> None: 
  tokens = [
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='bar'),
  ]
  assert parse(tokens) == IfStatement(L,cond=Identifier(L,name='foo'), then=Identifier(L,name='bar'), els = None)

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
  assert parse(tokens) == IfStatement(L,cond=IfStatement(L,cond=Identifier(L,name='foo'), then=Identifier(L,name='bar'), els = None), then=Identifier(L,name='baz'), els = None)

def test_if_as_expression() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='bar'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='baz')
  ]
  assert parse(tokens) == BinaryOp(L,left=Identifier(L,name='foo'), op='+', right=IfStatement(L,cond=Identifier(L,name='bar'), then=Identifier(L,name='baz'), els = None))

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
  assert parse(tokens) == Function(L,name=Identifier(L,name='f'), args=[Identifier(L,name='x'), BinaryOp(L,left=Identifier(L,name='y'), op='+', right=Identifier(L,name='z'))]) 


def test_unary_operators() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='identifier', text='and'),
    Token(loc=L, type='identifier', text='not'),
    Token(loc=L, type='identifier', text='bar')
  ]
  assert parse(tokens) == BinaryOp(L,left=Identifier(L,name='foo'), op='and', right=Unary(L,op='not', right=Identifier(L,name='bar')))

def test_rigt_associative_assignment() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='c')
  ]
  assert parse(tokens) == BinaryOp(L,left=Identifier(L,name='a'), op='=', right=BinaryOp(L,left=Identifier(L,name='b'), op='=', right=Identifier(L,name='c')))

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
  assert parse(tokens) == Block(L,statements=[
    Function(L,name=Identifier(L,name='f'), args=[Identifier(L,name='a')]),
    BinaryOp(L,left=Identifier(L,name='x'), op='=', right=Identifier(L,name='y'))
    ],
    result=Function(L,name=Identifier(L,name='f'), args=[Identifier(L,name='x')]))

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
  assert parse(tokens) == Block(L,statements=[Identifier(L,name='foo'), Identifier(L,name='bar')], result=None)

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
    assert e.args[0] == "(0, 0): expected \";\""


def test_var_in_beginning() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='var'),
    Token(loc=L, type='identifier', text='foo'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='bar')
  ]
  assert parse(tokens) == Var(L,val=Identifier(L,name='foo'), init=Identifier(L,name='bar'))

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

#optional semicolon tests

#allowed cases

def test_allowed_1() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='punctuation', text='}')
  ]
  assert parse(tokens) == Block(L,statements=[Block(L,statements=[], result=Identifier(L,name='a'))], result=Block(L,statements=[], result=Identifier(L,name='b')))

def test_allowed_2() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='true'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='punctuation', text='}')
  ]
  assert parse(tokens) == Block(L,statements=[IfStatement(L,cond=Identifier(L,name='true'), then=Block(L,statements=[], result=Identifier(L,name='a')), els=None)], result=Identifier(L,name='b')) 

def test_allowed_3() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='true'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='punctuation', text=';'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='punctuation', text='}')
  ]
  assert parse(tokens) == Block(L,statements=[IfStatement(L,cond=Identifier(L,name='true'), then=Block(L,statements=[], result=Identifier(L,name='a')), els=None)], result=Identifier(L,name='b')) 

def test_allowed_4() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='true'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='punctuation', text=';'),
    Token(loc=L, type='identifier', text='c'),
    Token(loc=L, type='punctuation', text='}')
  ]
  assert parse(tokens) == Block(L,statements=[IfStatement(L,cond=Identifier(L,name='true'), then=Block(L,statements=[], result=Identifier(L,name='a')), els=None), Identifier(L,name='b')], result=Identifier(L,name='c'))

def test_allowed_5() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='true'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='identifier', text='else'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='identifier', text='c'),
    Token(loc=L, type='punctuation', text='}')
  ]
  assert parse(tokens) == Block(L,statements=[IfStatement(L,cond=Identifier(L,name='true'), then=Block(L,statements=[], result=Identifier(L,name='a')), els=Block(L,statements=[], result=Identifier(L,name='b')))], result=Identifier(L,name='c'))

def test_allowed_6() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='x'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='f'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text=')'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='punctuation', text='}')
  ]
  assert parse(tokens) == BinaryOp(L,left=Identifier(L,name='x'), op='=', right=Block(L,statements=[Block(L,statements=[], result=Function(L,name=Identifier(L,name='f'), args=[Identifier(L,name='a')]))], result=Block(L,statements=[], result=Identifier(L,name='b'))))

def test_not_allowed_1() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='punctuation', text='}')
  ]
  try:
    parse(tokens)
  except Exception as e:
    assert e.args[0] == "(0, 0): expected \";\""

def test_not_allowed_2() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='true'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='identifier', text='c'),
    Token(loc=L, type='punctuation', text='}')
  ]
  try:
    parse(tokens)
  except Exception as e:
    assert e.args[0] == "(0, 0): expected \";\""

def test_location_test() -> None:
  tokens = [
    Token(Loc(0,0), type='identifier', text='x'),
    Token(Loc(0,2), type='operator', text='='),
    Token(Loc(0,4), type='punctuation', text='{'),
    Token(Loc(0,5), type='identifier', text='f'),
    Token(Loc(0,6), type='punctuation', text='('),
    Token(Loc(0,7), type='identifier', text='a'),
    Token(Loc(0,8), type='punctuation', text=')'),
    Token(Loc(0,9), type='punctuation', text=';'),
    Token(Loc(0,11), type='identifier', text='b'),
    Token(Loc(0,12), type='punctuation', text='}')
  ]
  assert parse(tokens) == BinaryOp(loc=Loc(0,2), left=Identifier(loc=Loc(0,0), name='x'), op='=', right=Block(loc=Loc(0,4), statements=[Function(loc=Loc(0,6), name=Identifier(loc=Loc(0,5), name='f'), args=[Identifier(loc=Loc(0,7), name='a')])], result=Identifier(loc=Loc(0,11), name='b')))

def test_multiline_location() -> None:
  tokens = [
    Token(Loc(0,0), type='punctuation', text='{'),
    Token(Loc(0,1), type='identifier', text='x'),
    Token(Loc(0,3), type='operator', text='='),
    Token(Loc(0,5), type='identifier', text='foo'),
    Token(Loc(0,6), type='punctuation', text=';'),
    Token(Loc(1,0), type='identifier', text='y'),
    Token(Loc(1,2), type='operator', text='='),
    Token(Loc(1,4), type='identifier', text='bar'),
    Token(Loc(1,5), type='punctuation', text=';'),
    Token(Loc(2,0), type='identifier', text='z'),
    Token(Loc(2,2), type='operator', text='='),
    Token(Loc(2,4), type='identifier', text='baz'),
    Token(Loc(2,5), type='punctuation', text=';'),
    Token(Loc(2,6), type='punctuation', text='}'),
  ]
  assert parse(tokens) == Block(loc=Loc(0,0), statements=[
    BinaryOp(loc=Loc(0,3), left=Identifier(loc=Loc(0,1), name='x'), op='=', right=Identifier(loc=Loc(0,5), name='foo')), 
    BinaryOp(loc=Loc(1,2), left=Identifier(loc=Loc(1,0), name='y'), op='=', right=Identifier(loc=Loc(1,4), name='bar')), 
    BinaryOp(loc=Loc(2,2), left=Identifier(loc=Loc(2,0), name='z'), op='=', right=Identifier(loc=Loc(2,4), name='baz'))], 
    result=None)
