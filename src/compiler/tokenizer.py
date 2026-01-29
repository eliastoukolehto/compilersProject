import re
from re import Pattern
from compiler.Loc import Loc
from compiler.Token import Token

identifier_r = re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*")
int_literal_r = re.compile(r"[0-9]+")
operator_r = re.compile(r"==|<=|>=|!=|>|<|-|\+|\*|\/|%|=")
punctuation_r = re.compile(r"\(|\)|{|}|,|;")


newline_r = re.compile(r"\n")
comment_r = re.compile(r"\/\/.*|#.*")

regexes: list[Pattern[str]] = [identifier_r, int_literal_r, operator_r, punctuation_r]
types = ['identifier', 'int_literal', 'operator', 'punctuation']


def find_token(source_code: str, i: int) -> tuple[str, str] | None:
  for j, t_type in enumerate(types):
    match = regexes[j].match(source_code, i)
    if match:
      return (t_type, match[0])
  return None


def tokenize(source_code: str) -> list:
  line = 0
  col = 0
  token_list = []
  i = 0
  while i < len(source_code):
    comment_match = comment_r.match(source_code, i)
    if comment_match is not None:
      i += len(comment_match[0])
      continue
    if newline_r.match(source_code, i) is not None:
      line += 1
      col = 0
      i += 1
      continue
    token = find_token(source_code, i)
    if token:
      token_list.append(Token(Loc(line, col), token[0], token[1]))
      col += len(token[1])
      i += len(token[1])
      continue

    col += 1
    i += 1
  return token_list
