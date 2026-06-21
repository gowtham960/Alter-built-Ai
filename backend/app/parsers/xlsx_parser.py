from typing import Dict, Any
import pandas as pd


def parse_xlsx(file_path: str) -> Dict[str, Any]:
    workbook = pd.read_excel(file_path, sheet_name=None)
    sheets = {}
    text_parts = []

    for sheet_name, df in workbook.items():
        df = df.fillna("")
        rows = df.to_dict(orient="records")

        sheets[sheet_name] = {
            "columns": list(df.columns),
            "row_count": len(rows),
            "rows": rows,
        }

        text_parts.append(f"Sheet: {sheet_name}")
        for i, row in enumerate(rows, start=1):
            row_text = ", ".join(f"{key}: {value}" for key, value in row.items())
            text_parts.append(f"Row {i}: {row_text}")

    return {
        "content_type": "spreadsheet",
        "sheet_count": len(sheets),
        "sheets": sheets,
        "text": "\n".join(text_parts),
    }