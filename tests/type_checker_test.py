from compiler.type_checker import typecheck
from compiler.ast import Literal, Var, Identifier, Block, BinaryOp, Unary, IfStatement, While
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
