from dataclasses import dataclass

@dataclass
class SymTab:
  locals: dict
  parent: 'SymTab | None'
