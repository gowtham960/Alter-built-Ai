from pathlib import Path
from typing import Any, Dict

from app.parsers.pdf_parser import parse_pdf
from app.parsers.csv_parser import parse_csv
from app.parsers.xlsx_parser import parse_xlsx
from app.parsers.docx_parser import parse_docx
from app.parsers.txt_parser import parse_txt


SUPPORTED_EXTENSIONS = {
    ".pdf": "PDF document",
    ".csv": "CSV spreadsheet",
    ".xlsx": "Excel spreadsheet",
    ".docx": "Word document",
    ".txt": "Plain text file",
}


def parse_file(file_path: str, original_filename: str) -> Dict[str, Any]:
    extension = Path(original_filename).suffix.lower()

    if extension == ".pdf":
        parsed = parse_pdf(file_path)
    elif extension == ".csv":
        parsed = parse_csv(file_path)
    elif extension == ".xlsx":
        parsed = parse_xlsx(file_path)
    elif extension == ".docx":
        parsed = parse_docx(file_path)
    elif extension == ".txt":
        parsed = parse_txt(file_path)
    else:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported types are: {', '.join(SUPPORTED_EXTENSIONS.keys())}"
        )

    return {
        "filename": original_filename,
        "extension": extension,
        "file_type": SUPPORTED_EXTENSIONS[extension],
        "parsed": parsed,
    }