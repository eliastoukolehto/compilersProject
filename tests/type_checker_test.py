from compiler.type_checker import typecheck
from compiler.ast import BinaryOp, Literal
from compiler.symtab import SymTab
from compiler.Loc import L
from compiler.type import Int, Unit, Bool

TopLevel = SymTab({}, None)

def test_tc_literals() -> None:
  ast1 = Literal(L, value=2)
  ast2 = Literal(L, value=False)
  ast3 = Literal(L, value=None)
  assert typecheck(ast1, TopLevel) == Int
  assert typecheck(ast2, TopLevel) == Bool
  assert typecheck(ast3, TopLevel) == Unit
