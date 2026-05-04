from pdfstruct import PDFParser

def test_parse_minimal():
    doc = PDFParser('tests/fixtures/minimal.pdf').parse().to_dict()
    assert doc['version'] == '1.4'
    assert len(doc['pages']) == 1


def test_parse_excludes_pages_tree_nodes_from_page_count():
    sample = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Count 1 /Kids [3 0 R] >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>
endobj
"""
    doc = PDFParser(sample).parse().to_dict()
    assert len(doc['pages']) == 1
