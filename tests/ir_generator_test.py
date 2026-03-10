from compiler import symtab
from compiler.ast import Literal, BinaryOp
from compiler.Loc import L
from compiler.ir_generator import generate_ir
from compiler.type import Int
from compiler.ir import LoadIntConst, IRVar, Call

def test_ir_binaryop() -> None:
  ast = BinaryOp(L, left=Literal(L, value=1, type=Int), op='+',
                 right=BinaryOp(L, left=Literal(L, value=2, type=Int), op='*', right=Literal(L, value=3, type=Int)),
                 type=Int)
  assert generate_ir(symtab.names, ast) == [
    LoadIntConst(L, value=1, dest=IRVar(name='x')),
    LoadIntConst(L, value=2, dest=IRVar(name='x2')),
    LoadIntConst(L, value=3, dest=IRVar(name='x3')),
    Call(L, fun=IRVar(name='*'), args=[IRVar(name='x2'), IRVar(name='x3')], dest=IRVar(name='x4')),
    Call(L, fun=IRVar(name='+'), args=[IRVar(name='x'), IRVar(name='x4')], dest=IRVar(name='x5')),
    Call(L, fun=IRVar(name='print_int'), args=[IRVar(name='x5')], dest=IRVar(name='unit'))]
