from dataclasses import dataclass

@dataclass
class Type:
  type: type

Int = Type(int)
Unit = Type(None)
Bool = Type(bool)
