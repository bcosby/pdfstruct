from dataclasses import dataclass


@dataclass(slots=True)
class PDFRef:
    obj: int
    gen: int

    def as_key(self) -> str:
        return f"{self.obj} {self.gen}"


@dataclass(slots=True)
class PDFName:
    value: str


@dataclass(slots=True)
class PDFStream:
    dictionary: dict
    raw: bytes
    decoded: bytes | None = None
    filters: list[str] | None = None


@dataclass(slots=True)
class PDFObject:
    obj: int
    gen: int
    value: object
    offset: int
