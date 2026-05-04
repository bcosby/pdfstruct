from pdfstruct import PDFParser

def test_parse_minimal():
    doc = PDFParser('tests/fixtures/minimal.pdf').parse().to_dict()
    assert doc['version'] == '1.4'
    assert len(doc['pages']) >= 1
