from typing import Any
from compiler import ast
from compiler.symtab import SymTab

type Value = int | bool | None

def interpret(node: ast.Expression, symtab: SymTab) -> Value:
  match node:
    case ast.Literal():
      return node.value

    case ast.Identifier():
      current_tab = symtab
      while True:
        if node.name not in current_tab.locals.keys():
          if current_tab.parent:
            current_tab = current_tab.parent
          else:
            raise Exception(f'Error: {node.loc}: Variable not found: \"{node.name}\"')
        else:
          return current_tab.locals[node.name]

    case ast.BinaryOp():
      a: Any = interpret(node.left, symtab)

      if node.op == "or" and a is True:
        return True

      if node.op == "and" and a is False:
        return False

      b: Any = interpret(node.right, symtab)

      current_tab = symtab
      while True:
        if node.op not in current_tab.locals.keys():
          if current_tab.parent:
            current_tab = current_tab.parent
          else:
            raise Exception(f'Error: {node.loc}: Unknown operator: \"{node.op}\"')
        else:
          return current_tab.locals[node.op](a,b)

    case ast.IfStatement():
      if interpret(node.cond, symtab):
        return interpret(node.then, symtab)
      if node.els is None:
        return None
      return interpret(node.els, symtab)

    case ast.Var():
      identifier = node.val.name
      expr = interpret(node.init, symtab)
      symtab.locals[identifier] = expr
      return None

    case ast.Block():
      block_tab = SymTab({}, symtab)
      for statement in node.statements:
        interpret(statement, block_tab)
      if node.result is None:
        return None
      return interpret(node.result, block_tab)

    case ast.Unary():
      c: Any = interpret(node.right, symtab)
      current_tab = symtab
      while True:
        if f"unary_{node.op}" not in current_tab.locals.keys():
          if current_tab.parent:
            current_tab = current_tab.parent
          else:
            raise Exception(f'Error: {node.loc}: Unknown operator: \"{node.op}\"')
        else:
          return current_tab.locals[f"unary_{node.op}"](c)


  raise Exception("Unknown node type")
