from pdfstruct.content import parse_content_stream
from pdfstruct.tokenizer import NULL_TOKEN, Tokenizer

def test_tokenizer_cases():
    t = Tokenizer(b"(hello \\(world\\)) (a (nested) string) <48656C6C6F> /Name#20With#20Spaces")
    assert t.next_token() == "hello (world)"
    assert t.next_token() == "a (nested) string"
    assert t.next_token() == "Hello"
    assert t.next_token() == "/Name With Spaces"


def test_null_token_is_distinct_from_eof():
    t = Tokenizer(b"null /After")
    assert t.next_token() is NULL_TOKEN
    assert t.next_token() == "/After"


def test_content_parse_continues_after_null_token():
    ops = parse_content_stream(b"null 12 0 Td")
    assert ops == [{"op": "Td", "args": [NULL_TOKEN, 12, 0]}]
