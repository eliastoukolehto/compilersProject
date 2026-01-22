import re


vars_regex = r"[a-zA-Z_][a-zA-Z_0-9]*"
ints_regrex = r"[0-9]+"

regex_list = [vars_regex, ints_regrex]
r = re.compile('|'.join(regex_list))

def tokenize(source_code: str) -> list:
  return r.findall(source_code)
