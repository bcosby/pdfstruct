# pdfstruct

**A fast, dependency-free PDF parser that extracts document structure and content into JSON.**

Parse PDFs into structured JSON with zero dependencies.

## Why this exists
PDFs are not structured like HTML or Markdown. They are collections of indirect objects, cross-reference tables, streams, dictionaries, and drawing commands. `pdfstruct` reads those internals directly and exposes them as JSON so developers can inspect, index, debug, and process PDF documents without heavyweight dependencies.

## Installation
```bash
pip install -e .
```

## CLI
```bash
pdfstruct parse input.pdf --output output.json
pdfstruct inspect input.pdf
pdfstruct text input.pdf
pdfstruct objects input.pdf
pdfstruct pages input.pdf
```

## Python API
```python
from pdfstruct import PDFParser
parser = PDFParser("example.pdf")
doc = parser.parse()
print(doc.to_json(indent=2))
```

## Supported MVP
Header detection, classic objects, simple pages, basic streams, Flate/ASCIIHex/ASCII85/RunLength filters, content operators, pragmatic text extraction.

## Unsupported (currently)
Encrypted PDFs, object streams, xref streams, full unicode mapping, OCR/image decode, digital signatures.

## Roadmap
- Better xref parsing
- Better font/CMap support
- Object streams and xref stream support
- Improved recovery for malformed PDFs

## Contributing
Run tests with `pytest` and keep the package dependency-free.
