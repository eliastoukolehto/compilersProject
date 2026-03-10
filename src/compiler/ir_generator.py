# src/compiler/ir_generator.py
from compiler import ast, ir, Loc
from compiler.ir import IRVar
from compiler.symtab import SymTab
from compiler.type import Bool, Int


def generate_ir(
    # 'reserved_names' should contain all global names
    # like 'print_int' and '+'. You can get them from
    # the global symbol table of your interpreter or type checker.
    reserved_names: set[str],
    root_expr: ast.Expression
) -> list[ir.Instruction]:
  var_index = 1
  label_index = 1

    # 'var_unit' is used when an expression's type is 'Unit'.
  var_unit = IRVar('unit')

  def new_var() -> IRVar:
    # Create a new unique IR variable
    nonlocal var_index
    name = 'x'
    if var_index > 1:
      name = f'x{var_index}'
    var_index += 1
    return IRVar(name)

  def new_label(loc: Loc.Loc) -> ir.Label:
    nonlocal label_index
    index = f'L{label_index}'
    label_index += 1
    return ir.Label(loc, index)


  # We collect the IR instructions that we generate
  # into this list.
  ins: list[ir.Instruction] = []

  # This function visits an AST node,
  # appends IR instructions to 'ins',
  # and returns the IR variable where
  # the emitted IR instructions put the result.
  #
  # It uses a symbol table to map local variables
  # (which may be shadowed) to unique IR variables.
  # The symbol table will be updated in the same way as
  # in the interpreter and type checker.
  def visit(st: SymTab[IRVar], expr: ast.Expression) -> IRVar:
    loc = expr.loc

    match expr:
      case ast.Literal():
        # Create an IR variable to hold the value,
        # and emit the correct instruction to
        # load the constant value.
        match expr.value:
          case bool():
            var = new_var()
            ins.append(ir.LoadBoolConst(
            loc, expr.value, var))
          case int():
            var = new_var()
            ins.append(ir.LoadIntConst(
                  loc, expr.value, var))
          case None:
            var = var_unit
          case _:
            raise Exception(f"{loc}: unsupported literal: {type(expr.value)}")

            # Return the variable that holds
            # the loaded value.
        return var

      case ast.Identifier():
        # Look up the IR variable that corresponds to
        # the source code variable.
        return st.require(expr.name)

      case ast.BinaryOp():
        # Ask the symbol table to return the variable that refers
        # to the operator to call.
        var_op = st.require(expr.op)
        # Recursively emit instructions to calculate the operands.
        var_left = visit(st, expr.left)
        var_right = visit(st, expr.right)
        # Generate variable to hold the result.
        var_result = new_var()
        # Emit a Call instruction that writes to that variable.
        ins.append(ir.Call(
            loc, var_op, [var_left, var_right], var_result))
        return var_result

      case ast.IfStatement():
        if expr.els is None:
          # Create (but don't emit) some jump targets.
          l_then = new_label(loc)
          l_end = new_label(loc)

          # Recursively emit instructions for
          # evaluating the condition.
          var_cond = visit(st, expr.cond)
          # Emit a conditional jump instruction
          # to jump to 'l_then' or 'l_end',
          # depending on the content of 'var_cond'.
          ins.append(ir.CondJump(loc, var_cond, l_then, l_end))

          # Emit the label that marks the beginning of
          # the "then" branch.
          ins.append(l_then)
          # Recursively emit instructions for the "then" branch.
          visit(st, expr.then)

          # Emit the label that we jump to
          # when we don't want to go to the "then" branch.
          ins.append(l_end)

          # An if-then expression doesn't return anything, so we
          # return a special variable "unit".
          return var_unit
        else:
          l_then = new_label(loc)
          l_else = new_label(loc)
          l_end = new_label(loc)

          var_cond = visit(st, expr.cond)

          ins.append(ir.CondJump(loc, var_cond, l_then, l_else))

          ins.append(l_then)
          visit(st, expr.then)
          ins.append(ir.Jump(loc, l_end))

          ins.append(l_else)
          visit(st, expr.els)

          ins.append(l_end)

          return var_unit
      case _:
        raise Exception('unknown Expression')
  # We start with a SymTab that maps all available global names
  # like 'print_int' to IR variables of the same name.
  # In the Assembly generator stage, we will give
  # actual implementations for these globals. For now,
  # they just need to exist so the variable lookups work,
  # and clashing variable names can be avoided.
  root_symtab = SymTab[IRVar]({}, None)
  for name in reserved_names:
    root_symtab.add_local(name, IRVar(name))

  # Start visiting the AST from the root.
  var_final_result = visit(root_symtab, root_expr)

  # Add IR code to print the result, based on the type assigned earlier
  # by the type checker.
  if root_expr.type == Int:
    print_int = root_symtab.require('print_int')
    ins.append(ir.Call(root_expr.loc, print_int, [var_final_result], var_unit))

  elif root_expr.type == Bool:
    print_bool = root_symtab.require('print_bool')
    ins.append(ir.Call(root_expr.loc, print_bool, [var_final_result], var_unit))
  return ins
