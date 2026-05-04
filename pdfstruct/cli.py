import argparse
import json
from .parser import PDFParser


def main() -> None:
    ap = argparse.ArgumentParser(prog="pdfstruct")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p_parse = sp.add_parser("parse")
    p_parse.add_argument("input")
    p_parse.add_argument("--output")
    p_parse.add_argument("--no-objects", action="store_true")
    p_parse.add_argument("--no-streams", action="store_true")
    p_parse.add_argument("--text-only", action="store_true")
    p_parse.add_argument("--max-stream-bytes", type=int, default=1048576)
    for name in ["inspect", "text", "objects", "pages"]:
        p = sp.add_parser(name); p.add_argument("input")
    ns = ap.parse_args()
    doc = PDFParser(ns.input).parse(getattr(ns, "no_objects", False), getattr(ns, "no_streams", False), getattr(ns, "text_only", False), getattr(ns, "max_stream_bytes", 1048576)).to_dict()
    if ns.cmd == "parse":
        out = json.dumps(doc, indent=2)
        if ns.output:
            open(ns.output, "w", encoding="utf-8").write(out)
        else:
            print(out)
    elif ns.cmd == "inspect":
        print(f"PDF version: {doc['version']}")
        print(f"file size: {doc['file']['size']}")
        print(f"number of objects: {len(doc['objects'])}")
        print(f"number of pages: {len(doc['pages'])}")
        print(f"encryption status: {doc['encrypted']}")
        print(f"trailer keys: []")
        print(f"metadata keys: {list(doc['metadata'].keys())}")
        print("xref mode: table/unknown")
    elif ns.cmd == "text":
        for i, p in enumerate(doc["pages"]):
            print(f"--- page {i+1} ---")
            print(p["text"])
    elif ns.cmd == "objects":
        print(json.dumps(doc["objects"], indent=2))
    elif ns.cmd == "pages":
        for p in doc["pages"]:
            print(f"page {p['index']}: {p['width']}x{p['height']} media={p['media_box']}")

if __name__ == "__main__":
    main()
