import re
from re import Pattern
from compiler.Loc import Loc
from compiler.Token import Token

identifier_r = re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*")
int_literal_r = re.compile(r"[0-9]+")

newline_r = re.compile(r"\n")

regexes: list[Pattern[str]] = [identifier_r, int_literal_r]
types = ['identifier', 'int_literal']


def tokenize(source_code: str) -> list:
  line = 0
  col = 0
  token_list = []
  i = 0
  while i < len(source_code):
    for j, t_type in enumerate(types):
      match = regexes[j].match(source_code, i)
      if match:
        token_list.append(Token(Loc(line, col), t_type, match[0]))
        col += len(match[0])
        i += len(match[0])
        break
    if newline_r.match(source_code, i) is not None:
      line += 1
      col = 0
    else:
      col += 1
    i += 1
    continue
  return token_list
