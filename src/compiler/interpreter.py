from typing import Any
from compiler import ast

type Value = int | bool | None

def interpret(node: ast.Expression) -> Value:
  match node:
    case ast.Literal():
      return node.value

    case ast.BinaryOp():
      a: Any = interpret(node.left)
      b: Any = interpret(node.right)
      if node.op == '+':
        return a + b
      if node.op == '<':
        return a < b
      raise Exception(f"Unknown operator: {node.op}")

    case ast.IfStatement():
      if interpret(node.cond):
        return interpret(node.then)
      if node.els is None:
        return None
      return interpret(node.els)

  raise Exception("Unknown node type")
