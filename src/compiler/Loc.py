from dataclasses import dataclass

@dataclass
class Loc:
  def __init__(self, line: int, col: int, test_object: bool =False):
    self.line = line
    self.col = col
    self.test_object = test_object

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Loc):
      return False

    if self.test_object or other.test_object:
      return True

    return self.line == other.line and self.col == other.col

  def __str__(self) -> str:
    return f"({self.line}, {self.col})"

L = Loc(0,0,True)
