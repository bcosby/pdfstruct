from pdfstruct import PDFParser
import json
print(json.dumps(PDFParser('tests/fixtures/minimal.pdf').parse().to_dict()['objects'], indent=2))
