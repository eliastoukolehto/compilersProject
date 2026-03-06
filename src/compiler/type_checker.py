from compiler import ast
from compiler.type import Type, Bool, Unit, Int, FunType
from compiler.symtab import SymTab

ops_req_match = ['==', '!=']

def typecheck(node: ast.Expression, symtab: SymTab) -> Type:
  match node:
    case ast.Literal():
      if isinstance(node.value, bool):
        return Bool
      if isinstance(node.value, int):
        return Int
      if node.value is None:
        return Unit
      raise Exception('unknown literal type')

    case ast.IfStatement():
      t1 = typecheck(node.cond, symtab)
      if t1 is not Bool:
        raise Exception(f'Error: {node.loc}: if-clause condition expected boolen, got: \"{t1}\"')
      t2 = typecheck(node.then, symtab)
      t3 = typecheck(node.els, symtab)
      if t3.name is not Unit:
        return t2
      if t2 != t3:
        raise Exception(f'Error: {node.loc}: if-clause branches must have the same type, got: \"{t2}\" and \"{t3}\" ')
      return t2

    case ast.Var():
      identifier = node.val.name
      t_expr = typecheck(node.init, symtab)
      symtab.locals[identifier] = t_expr
      return Unit

    case ast.Identifier():
      current_tab = symtab
      identifier = node.name
      while True:
        if identifier not in current_tab.locals.keys():
          if current_tab.parent:
            current_tab = current_tab.parent
          else:
            raise Exception(f'Error: {node.loc}: Variable not found: \"{identifier}\"')
        else:
          return current_tab.locals[identifier]

    case ast.Block():
      block_tab = SymTab({}, symtab)
      for statement in node.statements:
        typecheck(statement, block_tab)
      return typecheck(node.result, block_tab)

    case ast.BinaryOp():
      t1 = typecheck(node.left, symtab)
      t2 = typecheck(node.right, symtab)

      if node.op == '=':
        if t1 == t2:
          return t2
        raise Exception(f'Error: {node.loc}: Assignment requires both sides to have the same type, but left side was {t1} and right side was {t2}')

      if node.op in ops_req_match:
        if t1 == t2:
          return Bool
        raise Exception(f'Error: {node.loc}: Operator {node.op} requires both sides to have the same type, but left side was {t1} and right side was {t2}')

      current_tab = symtab
      while True:
        if node.op not in current_tab.locals.keys():
          if current_tab.parent:
            current_tab = current_tab.parent
          else:
            raise Exception(f'Error: {node.loc}: Unknown operator: \"{node.op}\"')
        else:
          funtype: FunType = current_tab.locals[node.op]
          if funtype.params[0] != t1:
            raise Exception(f'Error: {node.loc}: Operator \"{node.op}\" left side expected {funtype.params[0]}, got {t1}')
          if funtype.params[1] != t2:
            raise Exception(f'Error: {node.loc}: Operator \"{node.op}\" left side expected {funtype.params[0]}, got {t1}')

          return funtype.ret

    case ast.Unary():
      t = typecheck(node.right, symtab)
      current_tab = symtab
      while True:
        if f"unary_{node.op}" not in current_tab.locals.keys():
          if current_tab.parent:
            current_tab = current_tab.parent
          else:
            raise Exception(f'Error: {node.loc}: Unknown operator: \"unary_{node.op}\"')
        else:
          funtype2: FunType = current_tab.locals[f"unary_{node.op}"]
          if funtype2.params[0] != t:
            raise Exception(f'Error: {node.loc}: Operator \"unary_{node.op}\" left side expected {funtype2.params[0]}, got {t}')
          return funtype2.ret

    case ast.While():
      t = typecheck(node.cond, symtab)
      if t != Bool:
        raise Exception(f'Error: {node.loc}: while-loop condition expected boolean, got {t}')
      return Unit

  raise Exception("Unknown node type")
