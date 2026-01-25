from compiler.tokenizer import tokenize
from compiler.Loc import L, Loc
from compiler.Token import Token

def test_tokenizer_basics() -> None:
  assert tokenize("if 3\nwhile") == [Token(L, type="identifier", text="if"),
                                     Token(L, type="int_literal", text="3"),
                                     Token(L, type="identifier", text="while")]

def test_tokenizer_loc() -> None:
  assert tokenize("if 3\nwhile") == [Token(Loc(0,0), type="identifier", text="if"),
                                     Token(Loc(0,3), type="int_literal", text="3"),
                                     Token(Loc(1,0), type="identifier", text="while")]
