from typing import Dict, Any


def parse_txt(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        text = file.read()

    return {
        "content_type": "document",
        "text": text.strip(),
        "character_count": len(text),
    }