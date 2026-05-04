from pdfstruct import PDFParser
print(PDFParser('tests/fixtures/minimal.pdf').parse().to_json(indent=2))
