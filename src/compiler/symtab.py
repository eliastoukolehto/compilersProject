from dataclasses import dataclass
from compiler.type import FunType, Int, Unit, Bool

@dataclass
class SymTab:
  locals: dict
  parent: 'SymTab | None'

def op_plus(a:int , b:int) -> int:
  return a + b

def op_minus(a:int,b:int) -> int:
  return a - b

def op_asterisk(a:int,b:int) -> int:
  return a * b

def op_slash(a:int,b:int) -> int:
  return int(a / b)

def op_modulo(a:int,b:int) -> int:
  return a % b

def op_eq(a:int|bool,b:int|bool) -> bool:
  return a == b

def op_not_eq(a:int|bool,b:int|bool) -> bool:
  return a != b

def op_lt(a:int,b:int) -> bool:
  return a < b

def op_lteq(a:bool,b:bool) -> bool:
  return a <= b

def op_gt(a:bool,b:bool) -> bool:
  return a > b

def op_gteq(a:bool,b:bool) -> bool:
  return a >= b

def op_and(a:bool,b:bool) -> bool:
  return a and b

def op_or(a:bool,b:bool) -> bool:
  return a or b

def op_not(a:bool) -> bool:
  return not a

def op_unary_minus(a:int) -> int:
  return -a

TopLevel = SymTab({
    '+': op_plus,
    '-': op_minus,
    '*': op_asterisk,
    '/': op_slash,
    '%': op_modulo,
    '==': op_eq,
    '!=': op_not_eq,
    '<': op_lt,
    '<=': op_lteq,
    '>': op_gt,
    '>=': op_gteq,
    'and': op_and,
    'or': op_or,
    'unary_not': op_not,
    'unary_-': op_unary_minus
  }, None)

TopType = SymTab({
  '+': FunType((Int, Int), Int),
  '-': FunType((Int, Int), Int),
  '*': FunType((Int, Int), Int),
  '/': FunType((Int, Int), Int),
  '%': FunType((Int, Int), Int),
  '<': FunType((Int, Int), Bool),
  '<=': FunType((Int, Int), Bool),
  '>': FunType((Int, Int), Bool),
  '>=': FunType((Int, Int), Bool),
  'and': FunType((Bool, Bool), Bool),
  'or': FunType((Bool, Bool), Bool),
  'unary_not': FunType((Bool,Unit), Bool),
  'unary_-': FunType((Int,Unit), Int)
}, None)
