from typing import Dict, Any, List
from pypdf import PdfReader


def parse_pdf(file_path: str) -> Dict[str, Any]:
    reader = PdfReader(file_path)
    pages: List[Dict[str, Any]] = []

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append({
            "page_number": index,
            "text": text.strip()
        })

    combined_text = "\n\n".join(page["text"] for page in pages if page["text"])

    return {
        "content_type": "document",
        "page_count": len(pages),
        "pages": pages,
        "text": combined_text,
    }