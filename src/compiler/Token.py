from dataclasses import dataclass
from compiler.Loc import Loc


@dataclass
class Token:
  loc: Loc
  type: str
  text: str
