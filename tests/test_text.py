from pdfstruct import PDFParser

def test_text_extract():
    d = PDFParser('tests/fixtures/text_simple.pdf').parse().to_dict()
    assert 'Hello world' in d['pages'][0]['text']
