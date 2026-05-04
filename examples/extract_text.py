from pdfstruct import PDFParser
for p in PDFParser('tests/fixtures/text_simple.pdf').parse().to_dict()['pages']:
    print(p['text'])
