from compiler.interpreter import interpret
from compiler.Token import Token
from compiler.Loc import L, Loc
from compiler.ast import BinaryOp, Literal, Identifier, IfStatement, Function, Unary, Block, Var
from compiler.symtab import SymTab

def test_interpret_expression() -> None:
  ast = BinaryOp(L, left=Literal(L, value=2), op='+', right=Literal(L, value=3))

  assert interpret(ast, SymTab({}, None)) == 5

def test_intrepret_variable() -> None:
  ast = Var(L, val=Identifier(L, name='x'), init=Literal(L, value=3))
  assert interpret(ast, SymTab({}, None)) is None

def test_interpret_variable_in_operation() -> None:
  ast = Block(L, statements=[Var(L, val=Identifier(L, name='x'), init=Literal(L, value=4))], result=BinaryOp(L, left=Identifier(L, name='x'),  op='+', right=Literal(L, value=3)))
  assert interpret(ast, SymTab({}, None)) == 7

def test_variables_addition() -> None:
  ast = Block(L, statements=[
    Var(L, val=Identifier(L, name='x'), init=Literal(L, value=4)),
    Var(L, val=Identifier(L, name='y'), init=Literal(L, value=3))],
    result=BinaryOp(L, left=Identifier(L, name='x'),  op='+', right=Identifier(L, name='y')))
  assert interpret(ast, SymTab({}, None)) == 7
