import re

WHITESPACE = b"\x00\x09\x0A\x0C\x0D\x20"
DELIMS = b"()<>[]{}/%"


class Tokenizer:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def eof(self) -> bool:
        return self.pos >= len(self.data)

    def skip_ws(self) -> None:
        while not self.eof():
            b = self.data[self.pos]
            if b in WHITESPACE:
                self.pos += 1
                continue
            if b == 0x25:
                while not self.eof() and self.data[self.pos] not in b"\r\n":
                    self.pos += 1
                continue
            break

    def next_token(self):
        self.skip_ws()
        if self.eof():
            return None
        c = self.data[self.pos:self.pos + 1]
        if c == b"/":
            return self._name()
        if c == b"(":
            return self._literal()
        if c == b"<":
            if self.data[self.pos:self.pos + 2] == b"<<":
                self.pos += 2
                return "<<"
            return self._hex()
        if c == b">" and self.data[self.pos:self.pos + 2] == b">>":
            self.pos += 2
            return ">>"
        if c in (b"[", b"]"):
            self.pos += 1
            return c.decode()
        m = re.match(rb"[^\s\(\)<>\[\]\{\}/%]+", self.data[self.pos:])
        if not m:
            self.pos += 1
            return c.decode(errors="ignore")
        self.pos += len(m.group(0))
        tok = m.group(0).decode("latin-1")
        if tok == "true":
            return True
        if tok == "false":
            return False
        if tok == "null":
            return None
        try:
            if "." in tok or tok.startswith(("+", "-")) and tok[1:].isdigit() or tok.isdigit():
                return float(tok) if "." in tok else int(tok)
        except ValueError:
            pass
        return tok

    def _name(self):
        self.pos += 1
        start = self.pos
        while not self.eof() and self.data[self.pos] not in WHITESPACE + DELIMS:
            self.pos += 1
        raw = self.data[start:self.pos].decode("latin-1")
        raw = re.sub(r"#([0-9A-Fa-f]{2})", lambda m: chr(int(m.group(1), 16)), raw)
        return "/" + raw

    def _literal(self):
        self.pos += 1
        depth = 1
        out = bytearray()
        while not self.eof() and depth > 0:
            b = self.data[self.pos]
            self.pos += 1
            if b == 0x5C and not self.eof():
                out.append(self.data[self.pos])
                self.pos += 1
                continue
            if b == 0x28:
                depth += 1
            elif b == 0x29:
                depth -= 1
                if depth == 0:
                    break
            out.append(b)
        return out.decode("latin-1", errors="replace")

    def _hex(self):
        self.pos += 1
        start = self.pos
        while not self.eof() and self.data[self.pos:self.pos + 1] != b">":
            self.pos += 1
        raw = re.sub(rb"\s+", b"", self.data[start:self.pos])
        self.pos += 1
        if len(raw) % 2:
            raw += b"0"
        return bytes.fromhex(raw.decode("ascii", errors="ignore")).decode("latin-1", errors="replace")
