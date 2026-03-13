from dataclasses import fields
from compiler import ir, intrinsics


class Locals:
  """Knows the memory location of every local variable."""
  _var_to_location: dict[ir.IRVar, str]
  _stack_used: int

  def __init__(self, variables: list[ir.IRVar]) -> None:
    self._var_to_location = {}
    self._stack_used = 8 * len(variables)
    l = -8
    for var in variables:
      self._var_to_location[var] = f'{l}(%rbp)'
      l += -8
    #print(self._var_to_location)

  def get_ref(self, v: ir.IRVar) -> str:
    """Returns an Assembly reference like `-24(%rbp)`
    for the memory location that stores the given variable"""
    return self._var_to_location[v]

  def stack_used(self) -> int:
    """Returns the number of bytes of stack space needed for the local variables."""
    return self._stack_used



def get_all_ir_variables(instructions: list[ir.Instruction]) -> list[ir.IRVar]:
  result_list: list[ir.IRVar] = []
  result_set: set[ir.IRVar] = set()

  def add(v: ir.IRVar) -> None:
    if v not in result_set:
      result_list.append(v)
      result_set.add(v)

  for insn in instructions:
    for field in fields(insn):
      value = getattr(insn, field.name)
      if isinstance(value, ir.IRVar):
        add(value)
      elif isinstance(value, list):
        for v in value:
          if isinstance(v, ir.IRVar):
            add(v)
  return result_list



def generate_assembly(instructions: list[ir.Instruction]) -> str:
  lines = []
  def emit(line: str) -> None: lines.append(line)


  locals = Locals(
    variables=get_all_ir_variables(instructions)
  )

  #Initial declarations and stack setup

  emit('.extern print_int')
  emit('.extern print_bool')
  emit('.extern read_int')
  emit('.global main')
  emit('.type main, @function')
  emit('.section .text')

  emit('main:')
  emit('pushq %rbp')
  emit('movq %rsp, %rbp')
  emit(f'subq ${locals.stack_used()}, %rsp')

  for insn in instructions:
    emit('\n# ' + str(insn))
    match insn:
      case ir.Label():
        emit("")
        # ".L" prefix marks the symbol as "private".
        # This makes GDB backtraces look nicer too:
        # https://stackoverflow.com/a/26065570/965979
        emit(f'.L{insn.name}:')
      case ir.LoadIntConst():
        if -2**31 <= insn.value < 2**31:
          emit(f'movq ${insn.value}, {locals.get_ref(insn.dest)}')
        else:
          # Due to a quirk of x86-64, we must use
          # a different instruction for large integers.
          # It can only write to a register,
          # not a memory location, so we use %rax
          # as a temporary.
          emit(f'movabsq ${insn.value}, %rax')
          emit(f'movq %rax, {locals.get_ref(insn.dest)}')
      case ir.Jump():
        emit(f'jmp .L{insn.label.name}')

      case ir.LoadBoolConst():
        if insn.value is True:
          emit(f'movq $1, {locals.get_ref(insn.dest)}')
        else:
          emit(f'movq $0, {locals.get_ref(insn.dest)}')

      case ir.Copy():
        emit(f'movq {locals.get_ref(insn.source)}, %rax')
        emit(f'movq %rax, {locals.get_ref(insn.dest)}')

      case ir.CondJump():
        emit(f'cmpq $0, {locals.get_ref(insn.cond)}')
        emit(f'jne .L{insn.then_label.name}')
        emit(f'jmp .L{insn.else_label.name}')

      case ir.Call():
        regs = ['%rdi','%rsi','%rdx','%rcx','r8','r9']
        all_ins_names = intrinsics.all_intrinsics.keys()
        if insn.fun.name in all_ins_names:
          arg_refs = []
          for arg in insn.args:
            arg_refs.append(locals.get_ref(arg))

          intrinsics.all_intrinsics['+'](intrinsics.IntrinsicArgs(
              arg_refs=arg_refs,
              result_register='%rax',
              emit=emit
          ))
        else:
          for i, arg in enumerate(insn.args):
            if i > len(regs):
              emit(f'pushq {locals.get_ref(arg)}')
            else:
              emit(f'movq {locals.get_ref(arg)}, {regs[i]}')
          emit(f'callq {insn.fun.name}')
        emit(f'movq %rax, {locals.get_ref(insn.dest)}')


  #restore stack
  emit('\n#Return(None)')
  emit('movq $0, %rax')
  emit('movq %rbp, %rsp')
  emit('popq %rbp')
  emit('ret')

  return '\n'.join(lines)
