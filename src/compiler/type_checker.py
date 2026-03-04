from compiler import ast
from compiler.type import Type, Bool, Unit, Int
from compiler.symtab import SymTab

def typecheck(node: ast.Expression, symtab: SymTab) -> Type:
  match node:
    case ast.Literal():
      return Int
      #Gotta fix parser oopsie

    case ast.IfStatement():
      t1 = typecheck(node.cond, symtab)
      if t1 is not Bool:
        raise Exception(f'Error: {node.loc}: if-clause condition expected boolen, got: \"{t1.type}\"')
      t2 = typecheck(node.then, symtab)
      t3 = typecheck(node.els, symtab)
      if t2 != t3 and t3.type is not None:
        raise Exception(f'Error: {node.loc}: if-clause branches must have the same type, got: \"{t2.type}\" and \"{t3.type}\" ')
      return t3 #maybe?

    case ast.Var():
      identifier = node.val.name
      t_expr = typecheck(node.init, symtab)
      symtab.locals[identifier] = t_expr
      return None
