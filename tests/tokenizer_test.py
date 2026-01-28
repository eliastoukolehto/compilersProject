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

def test_tokenizer_op() -> None:
  assert tokenize("3 == 4 + 7") == [Token(L, type="int_literal", text="3"),
                                     Token(L, type="operator", text="=="),
                                     Token(L, type="int_literal", text="4"),
                                     Token(L, type="operator", text="+"),
                                     Token(L, type="int_literal", text="7")]

def test_tokenizer_punc() -> None:
  assert tokenize("{3,4,(7)}") == [Token(L, type="punctuation", text="{"),
                                     Token(L, type="int_literal", text="3"),
                                     Token(L, type="punctuation", text=","),
                                     Token(L, type="int_literal", text="4"),
                                     Token(L, type="punctuation", text=","),
                                     Token(L, type="punctuation", text="("),
                                     Token(L, type="int_literal", text="7"),
                                     Token(L, type="punctuation", text=")"),
                                     Token(L, type="punctuation", text="}")]
  
def test_tokenizer_comment_loc() -> None:
  assert tokenize("3 #comment\n4//comment 5\n#6\n7") == [Token(Loc(0,0), type="int_literal", text="3"),
                                     Token(Loc(1,0), type="int_literal", text="4"),
                                     Token(Loc(3,0), type="int_literal", text="7")]