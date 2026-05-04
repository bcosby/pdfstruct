import mmap
import os
import re
from .content import parse_content_stream
from .document import PDFDocument
from .text import extract_text_and_spans
from .tokenizer import Tokenizer


class PDFParser:
    def __init__(self, path: str | bytes):
        self.path = path if isinstance(path, str) else None
        self.raw = None if isinstance(path, str) else path

    def _read(self) -> bytes:
        if self.raw is not None:
            return self.raw
        with open(self.path, "rb") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                return mm[:]

    def parse(self, no_objects: bool = False, no_streams: bool = False, text_only: bool = False, max_stream_bytes: int = 1048576) -> PDFDocument:
        data = self._read()
        version = re.search(rb"%PDF-(\d\.\d)", data)
        doc = {
            "version": version.group(1).decode() if version else None,
            "file": {"path": self.path, "size": len(data)},
            "encrypted": b"/Encrypt" in data,
            "metadata": {k: None for k in ["title","author","subject","creator","producer","creation_date","modification_date"]},
            "catalog": {"object": None, "type": "Catalog"},
            "pages": [], "outlines": [], "objects": {}, "warnings": []
        }
        for m in re.finditer(rb"(\d+)\s+(\d+)\s+obj(.*?)endobj", data, re.S):
            oid, gen, body = int(m.group(1)), int(m.group(2)), m.group(3).strip()
            key = f"{oid} {gen}"
            if b"stream" in body and b"endstream" in body:
                head, rest = body.split(b"stream", 1)
                stream_raw = rest.split(b"endstream", 1)[0].strip(b"\r\n")
                if len(stream_raw) > max_stream_bytes:
                    doc["warnings"].append({"code": "stream_too_large", "message": "stream skipped", "offset": m.start()})
                    stream_raw = b""
                if not no_streams:
                    obj_val = {"type": "stream", "dict": head.decode("latin-1", "replace"), "length": len(stream_raw)}
                else:
                    obj_val = {"type": "stream", "length": len(stream_raw)}
            else:
                tok = Tokenizer(body)
                parsed = []
                while True:
                    t = tok.next_token()
                    if t is None:
                        break
                    parsed.append(t)
                obj_val = {"type": "tokens", "value": parsed}
            if not no_objects and not text_only:
                doc["objects"][key] = obj_val
        pages = list(re.finditer(rb"<<[^>]*?/Type\s*/Page[^>]*?>>", data, re.S))
        for idx, pm in enumerate(pages):
            d = pm.group(0)
            media = [0,0,612,792]
            mm = re.search(rb"/MediaBox\s*\[(.*?)\]", d, re.S)
            if mm:
                nums = [float(x) for x in re.findall(rb"-?\d+\.?\d*", mm.group(1))]
                if len(nums) == 4: media = nums
            text = ""
            spans = []
            ops = []
            if b"BT" in data:
                start = data.find(b"BT", pm.end())
                end = data.find(b"ET", start)
                if start != -1 and end != -1:
                    ops = parse_content_stream(data[start:end+2])
                    text, spans = extract_text_and_spans(ops)
            doc["pages"].append({"index": idx,"object": None,"width": media[2]-media[0],"height": media[3]-media[1],"media_box": media,"crop_box": media,"rotate":0,"text": text,"text_spans": spans,"content": {"streams": [], "operators": ops},"resources": {"fonts": {}, "images": []},"annotations": []})
        return PDFDocument(doc)
