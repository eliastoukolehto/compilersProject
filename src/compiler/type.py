from dataclasses import dataclass

@dataclass
class Type:
  type: type | None

Int = Type(int)
Unit = Type(None)
Bool = Type(bool)
