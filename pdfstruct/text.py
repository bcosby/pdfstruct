def extract_text_and_spans(operators: list[dict]) -> tuple[str, list[dict]]:
    text_parts = []
    spans = []
    x, y = 0.0, 0.0
    font, size = None, None
    for op in operators:
        name = op["op"]
        args = op["args"]
        if name == "Tf" and len(args) >= 2:
            font = str(args[0]).lstrip("/")
            size = float(args[1])
        elif name in {"Td", "TD"} and len(args) >= 2:
            x += float(args[0]); y += float(args[1])
        elif name == "Tm" and len(args) >= 6:
            x, y = float(args[4]), float(args[5])
        elif name == "T*":
            y -= size or 12
        elif name == "Tj" and args:
            txt = str(args[0]); text_parts.append(txt)
            spans.append({"text": txt, "x": x, "y": y, "font": font, "font_size": size})
        elif name == "TJ" and args and isinstance(args[0], list):
            txt = "".join(str(v) for v in args[0] if isinstance(v, str)); text_parts.append(txt)
            spans.append({"text": txt, "x": x, "y": y, "font": font, "font_size": size})
    return "\n".join(text_parts), spans
