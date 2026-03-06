from compiler.interpreter import interpret
from compiler.Loc import L
from compiler.ast import BinaryOp, Literal, Identifier, IfStatement, Unary, Block, Var, While
from compiler.symtab import TopLevel

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
    right=(Unary(L, op='not', right=BinaryOp(L, left=Literal(L, value=2), op='>=', right=Literal(L, value=3)))))
  assert interpret(ast, TopLevel) is True

def test_boolean_operators_2() -> None:
  ast = BinaryOp(L,
    left=(BinaryOp(L, left=Literal(L, value=True), op='and', right=Literal(L, value=False))),
    op='or',
    right=(BinaryOp(L, left=Literal(L, value=True), op='and', right=Literal(L, value=True))))
  assert interpret(ast, TopLevel) is True

def test_shortcircuit() -> None:
  ast = Block(L, statements=[
    Var(L, init=Literal(L, value=False), val=Identifier(L, name='x')),
    BinaryOp(L, left=Literal(L, value=True), op="or", right=Block(L, statements=[
      BinaryOp(L, left=Identifier(L, name='x'), op='=', right=(Literal(L, value=True)))], result=(Literal(L, value=True)))
    )], result=(Identifier(L, name='x')))
  assert interpret(ast, TopLevel) is False

def test_if_then_else() -> None:
  ast = IfStatement(L, cond=(BinaryOp(L, left=Literal(L, value=2), op='==', right=Literal(L, value=3))), then=(Literal(L, value=False)), els=Literal(L, value=True))
  assert interpret(ast, TopLevel) is True

def test_interpret_variable_reassign() -> None:
  ast = Block(L, statements=[Var(L, val=Identifier(L, name='x'), init=Literal(L, value=4)), BinaryOp(L, left=Identifier(L, name='x'),  op='=', right=Literal(L, value=3))], result=Identifier(L, name='x'))
  assert interpret(ast, TopLevel) == 3

def test_while() -> None:
  ast = Block(L, statements=[
    Var(L, val=Identifier(L, name='x'), init=Literal(L, value=1)),
    While(L,
      cond=BinaryOp(L, left=Identifier(L, name='x'), op='<', right=Literal(L, value=10)),
      then=BinaryOp(L, left=Identifier(L, name='x'), op='=', right=BinaryOp(L, left=Identifier(L, name='x'), op='+', right=Literal(L, value=1)))
    )],
    result=Identifier(L, name='x'))
  assert interpret(ast, TopLevel) == 10

def test_while_no_return() -> None:
  ast = Block(L, statements=[Var(L, val=Identifier(L, name='x'), init=Literal(L, value=1)),],
    result=While(L,
      cond=BinaryOp(L, left=Identifier(L, name='x'), op='<', right=Literal(L, value=10)),
      then=BinaryOp(L, left=Identifier(L, name='x'), op='=', right=BinaryOp(L, left=Identifier(L, name='x'), op='+', right=Literal(L, value=1)))
    ))
  assert interpret(ast, TopLevel) is None
