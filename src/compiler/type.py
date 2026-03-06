from dataclasses import dataclass

@dataclass
class Type:
  name: type | None

@dataclass
class FunType:
  params: tuple
  ret: Type

Int = Type(int)
Unit = Type(None)
Bool = Type(bool)
