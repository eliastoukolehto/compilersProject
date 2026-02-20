from compiler.interpreter import interpret
from compiler.Token import Token
from compiler.Loc import L, Loc
from compiler.ast import BinaryOp, Literal, Identifier, IfStatement, Function, Unary, Block, Var

def test_interpret_expression() -> None:
  ast = BinaryOp(L, left=Literal(L, value=2), op='+', right=Literal(L, value=3))

  assert interpret(ast) == 5
