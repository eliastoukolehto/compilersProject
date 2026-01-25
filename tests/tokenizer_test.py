from compiler.tokenizer import tokenize
from compiler.Loc import Loc
from compiler.Token import Token

def test_tokenizer_basics() -> None:
  assert tokenize("if 3\nwhile") == [Token(loc=Loc(0,0), type="identifier", text="if"),
                                     Token(loc=Loc(0,3), type="int_literal", text="3"),
                                     Token(loc=Loc(1,0), type="identifier", text="while")]
