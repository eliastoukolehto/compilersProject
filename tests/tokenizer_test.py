from compiler.tokenizer import tokenize

def test_tokenizer_basics() -> None:
  assert tokenize("if 3\nwhile") == ['if', '3', 'while']
  assert tokenize("when foo_7 not 345") == ['when', 'foo_7', 'not', '345']
  assert tokenize("_secret __mystery_VAL is HaMbUrGeR") == ['_secret', '__mystery_VAL', 'is', 'HaMbUrGeR']
