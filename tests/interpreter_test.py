from compiler.interpreter import interpret
from compiler.Token import Token
from compiler.Loc import L, Loc
from compiler.ast import BinaryOp, Literal, Identifier, IfStatement, Function, Unary, Block, Var
from compiler.symtab import SymTab, TopLevel

def test_interpret_expression() -> None:
  ast = BinaryOp(L, left=Literal(L, value=2), op='+', right=Literal(L, value=3))

  assert interpret(ast, TopLevel) == 5

def test_intrepret_variable() -> None:
  ast = Var(L, val=Identifier(L, name='x'), init=Literal(L, value=3))
  assert interpret(ast, TopLevel) is None

def test_interpret_variable_in_operation() -> None:
  ast = Block(L, statements=[Var(L, val=Identifier(L, name='x'), init=Literal(L, value=4))], result=BinaryOp(L, left=Identifier(L, name='x'),  op='+', right=Literal(L, value=3)))
  assert interpret(ast, TopLevel) == 7

def test_variables_addition() -> None:
  ast = Block(L, statements=[
    Var(L, val=Identifier(L, name='x'), init=Literal(L, value=4)),
    Var(L, val=Identifier(L, name='y'), init=Literal(L, value=3))],
    result=BinaryOp(L, left=Identifier(L, name='x'),  op='+', right=Identifier(L, name='y')))
  assert interpret(ast, TopLevel) == 7

def test_unary_addition() -> None:
  ast = BinaryOp(L, left=Literal(L, value=2), op='+', right=Unary(L, op='-', right=Literal(L, value=5)))
  assert interpret(ast, TopLevel) == -3

def test_boolean_operations() -> None:
  ast = BinaryOp(L,
    left=(BinaryOp(L, left=Literal(L, value=2), op='==', right=Literal(L, value=3))),
    op='or',
    right=(Unary(L, op='not', right=BinaryOp(L, left=Literal(L, value=2), op='<=', right=Literal(L, value=3)))))
  assert interpret(ast, TopLevel) is False
