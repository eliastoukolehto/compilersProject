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
      b: Any = interpret(node.right, symtab)
      if node.op == '+':
        return a + b
      if node.op == '<':
        return a < b
      raise Exception(f"Unknown operator: {node.op}")

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

  raise Exception("Unknown node type")
