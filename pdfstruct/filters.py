import base64
import zlib


def asciihex_decode(data: bytes) -> bytes:
    cleaned = b"".join(data.split()).rstrip(b">")
    if len(cleaned) % 2:
        cleaned += b"0"
    return bytes.fromhex(cleaned.decode("ascii", errors="ignore"))


def runlength_decode(data: bytes) -> bytes:
    out = bytearray()
    i = 0
    while i < len(data):
        length = data[i]
        i += 1
        if length == 128:
            break
        if length < 128:
            out.extend(data[i:i + length + 1])
            i += length + 1
        else:
            b = data[i]
            i += 1
            out.extend([b] * (257 - length))
    return bytes(out)


def apply_filters(data: bytes, filters: list[str] | None) -> tuple[bytes, list[str]]:
    warnings: list[str] = []
    out = data
    for f in filters or []:
        name = f.lstrip("/")
        if name in {"FlateDecode", "Fl"}:
            out = zlib.decompress(out)
        elif name == "ASCIIHexDecode":
            out = asciihex_decode(out)
        elif name == "ASCII85Decode":
            out = base64.a85decode(out, adobe=True)
        elif name == "RunLengthDecode":
            out = runlength_decode(out)
        else:
            warnings.append(name)
    return out, warnings
