from compiler.type_checker import typecheck
from compiler.ast import Literal, Var, Identifier, Block, BinaryOp, Unary, IfStatement, While, Function
from compiler.symtab import TopType
from compiler.Loc import L
from compiler.type import Int, Unit, Bool

def test_tc_literals() -> None:
  ast1 = Literal(L, value=2)
  ast2 = Literal(L, value=False)
  ast3 = Literal(L, value=None)
  assert typecheck(ast1, TopType) == Int
  assert typecheck(ast2, TopType) == Bool
  assert typecheck(ast3, TopType) == Unit

def test_var_init() -> None:
  ast = Var(L, val=Identifier(L, name='x'), init=Literal(L, value=2))
  assert typecheck(ast, TopType) == Unit

def test_var_print() -> None:
  ast = Block(L, statements=[Var(L, val=Identifier(L, name='x'), init=Literal(L, value=2))], result=Identifier(L, name='x'))
  assert typecheck(ast, TopType) == Int

def test_var_assign() ->  None:
  ast = Block(L, statements=[Var(L, val=Identifier(L, name='x'), init=Literal(L, value=4)), BinaryOp(L, left=Identifier(L, name='x'),  op='=', right=Literal(L, value=3))], result=Identifier(L, name='x'))
  assert typecheck(ast, TopType) == Int

def test_var_assign_mismatch() -> None:
  ast = Block(L, statements=[Var(L, val=Identifier(L, name='x'), init=Literal(L, value=4)), BinaryOp(L, left=Identifier(L, name='x'),  op='=', right=Literal(L, value=True))], result=Identifier(L, name='x'))

  try:
    typecheck(ast, TopType)
  except Exception as e:
    assert e.args[0] == "Error: (0, 0): Assignment requires both sides to have the same type, but left side was Type(name=<class 'int'>) and right side was Type(name=<class 'bool'>)"

def test_match_req_ops() -> None:
  ast1 = BinaryOp(L, left=Literal(L, value=1), op='==', right=Literal(L, value=2))
  ast2 = BinaryOp(L, left=Literal(L, value=1), op='!=', right=Literal(L, value=2))
  ast3 = BinaryOp(L, left=Literal(L, value=1), op='==', right=Literal(L, value=True))
  ast4 = BinaryOp(L, left=Literal(L, value=1), op='!=', right=Literal(L, value=True))
  assert typecheck(ast1, TopType) == Bool
  assert typecheck(ast2, TopType) == Bool
  try:
    typecheck(ast3, TopType)
  except Exception as e:
    assert e.args[0] == "Error: (0, 0): Operator == requires both sides to have the same type, but left side was Type(name=<class 'int'>) and right side was Type(name=<class 'bool'>)"
  try:
    typecheck(ast4, TopType)
  except Exception as e:
    assert e.args[0] == "Error: (0, 0): Operator != requires both sides to have the same type, but left side was Type(name=<class 'int'>) and right side was Type(name=<class 'bool'>)"

def test_funtypes() -> None:
  ast1 = BinaryOp(L, left=Literal(L, value=1), op='/', right=Literal(L, value=2))
  ast2 = BinaryOp(L, left=Literal(L, value=1), op='>=', right=Literal(L, value=2))
  ast3 = BinaryOp(L, left=Literal(L, value=False), op='and', right=Literal(L, value=True))
  ast4 = BinaryOp(L, left=Literal(L, value=False), op='or', right=Literal(L, value=True))
  assert typecheck(ast1, TopType) == Int
  assert typecheck(ast2, TopType) == Bool
  assert typecheck(ast3, TopType) == Bool
  assert typecheck(ast4, TopType) == Bool

def test_unaries() -> None:
  ast1 = Unary(L, op='-', right=Literal(L, value=2))
  ast2 = Unary(L, op='not', right=Literal(L, value=False))
  ast3 = Unary(L, op='not', right=Literal(L, value=2))
  assert typecheck(ast1, TopType) == Int
  assert typecheck(ast2, TopType) == Bool
  try:
    typecheck(ast3, TopType)
  except Exception as e:
    assert e.args[0] == "Error: (0, 0): Operator \"unary_not\" left side expected Type(name=<class 'bool'>), got Type(name=<class 'int'>)"

def test_if_else() -> None:
  ast1 = IfStatement(L, cond=(BinaryOp(L, left=Literal(L, value=2), op='==', right=Literal(L, value=3))), then=(Literal(L, value=False)), els=Literal(L, value=True))
  ast2 = IfStatement(L, cond=(BinaryOp(L, left=Literal(L, value=2), op='==', right=Literal(L, value=3))), then=(Literal(L, value=1)), els=Literal(L, value=True))
  assert typecheck(ast1, TopType) == Bool
  try:
    typecheck(ast2, TopType)
  except Exception as e:
    assert e.args[0] == "Error: (0, 0): Operator \"unary_not\" left side expected Type(name=<class 'bool'>), got Type(name=<class 'int'>)"


def test_if_no_else() -> None:
  ast = IfStatement(L, cond=(BinaryOp(L, left=Literal(L, value=2), op='==', right=Literal(L, value=3))), then=(Literal(L, value=False)), els=Literal(L, value=None))
  assert typecheck(ast, TopType) == Bool

def test_while() -> None:
  ast = Block(L, statements=[Var(L, val=Identifier(L, name='x'), init=Literal(L, value=1)),],
  result=While(L,
    cond=BinaryOp(L, left=Identifier(L, name='x'), op='<', right=Literal(L, value=10)),
    then=BinaryOp(L, left=Identifier(L, name='x'), op='=', right=BinaryOp(L, left=Identifier(L, name='x'), op='+', right=Literal(L, value=1)))
  ))
  assert typecheck(ast, TopType) == Unit

def test_builtin_functions() -> None:
  ast1 = Function(L, args=[Literal(L, value=1)],  name=Identifier(L, name='print_int'))
  ast2 = Function(L, args=[Literal(L, value=True)],  name=Identifier(L, name='print_bool'))
  ast3 = Function(L, args=[],  name=Identifier(L, name='read_int'))
  assert typecheck(ast1, TopType) == Unit
  assert typecheck(ast2, TopType) == Unit
  assert typecheck(ast3, TopType) == Int

def test_function_too_many_args() -> None:
  ast = Function(L, args=[Literal(L, value=1), Literal(L, value=2)],  name=Identifier(L, name='print_int'))
  try:
    typecheck(ast, TopType)
  except Exception as e:
    assert e.args[0] == "Error: (0, 0): Function \"print_int\" expects 1 parameters, but 2 were given"

def test_func_wrong_type() -> None:
  ast = Function(L, args=[Literal(L, value=False)],  name=Identifier(L, name='print_int'))
  try:
    typecheck(ast, TopType)
  except Exception as e:
    assert e.args[0] == "Error: (0, 0): Function \"print_int\" parameter 0 expects Type(name=<class 'int'>), but Type(name=<class 'bool'>) was given"

def test_invalid_func() -> None:
  ast = Function(L, args=[Literal(L, value=False)],  name=Identifier(L, name='noninit_func'))
  try:
    typecheck(ast, TopType)
  except Exception as e:
    assert e.args[0] == "Error: (0, 0): Unknown function: \"noninit_func\""
