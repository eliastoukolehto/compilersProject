from typing import Any
from dataclasses import dataclass
from compiler.type import FunType, Int, Unit, Bool


@dataclass
class SymTab[Given_Type]:
  locals: dict[Any, Given_Type]
  parent: 'SymTab | None'

  def require(self, op:str) -> Given_Type:
    current_tab = self
    while True:
      if op not in current_tab.locals.keys():
        if current_tab.parent:
          current_tab = current_tab.parent
        else:
          ## should never trigger
          raise Exception(f'Error: Unknown operator: \"{op}\"')
      else:
        return current_tab.locals[op]

  def add_local(self, name: str, func: Any) -> None:
    self.locals[name] = func

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

def op_print(a: int | bool) -> None:
  print(a)

def op_read_int(a:str) -> int:
  return int(a)


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
    'unary_-': op_unary_minus,
    'print_int': op_print,
    'print_bool': op_print,
    'read_int': op_read_int
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
  'unary_-': FunType((Int,Unit), Int),
  'print_int': FunType((Int,), Unit),
  'print_bool': FunType((Bool,), Unit),
  'read_int': FunType((), Int)
}, None)

names = set(TopLevel.locals.keys())
