from dataclasses import dataclass
import json


@dataclass(slots=True)
class PDFDocument:
    data: dict

    def to_dict(self) -> dict:
        return self.data

    def to_json(self, indent: int | None = None) -> str:
        return json.dumps(self.data, indent=indent, ensure_ascii=False)
