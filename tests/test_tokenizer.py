from pdfstruct.tokenizer import Tokenizer

def test_tokenizer_cases():
    t = Tokenizer(b"(hello \\(world\\)) (a (nested) string) <48656C6C6F> /Name#20With#20Spaces")
    assert t.next_token() == "hello (world)"
    assert t.next_token() == "a (nested) string"
    assert t.next_token() == "Hello"
    assert t.next_token() == "/Name With Spaces"
