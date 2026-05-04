from .tokenizer import Tokenizer

OPS = {"BT","ET","Tf","Td","TD","Tm","T*","Tj","TJ","'",'"'}

def parse_content_stream(data: bytes) -> list[dict]:
    t = Tokenizer(data)
    args = []
    ops = []
    while True:
        tok = t.next_token()
        if tok is None:
            break
        if isinstance(tok, str) and tok in OPS:
            ops.append({"op": tok, "args": args})
            args = []
        else:
            args.append(tok)
    return ops
