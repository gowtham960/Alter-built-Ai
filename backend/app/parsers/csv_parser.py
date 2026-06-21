from typing import Dict, Any
import pandas as pd


def parse_csv(file_path: str) -> Dict[str, Any]:
    df = pd.read_csv(file_path)
    rows = df.fillna("").to_dict(orient="records")

    text_rows = []
    for i, row in enumerate(rows, start=1):
        row_text = ", ".join(f"{key}: {value}" for key, value in row.items())
        text_rows.append(f"Row {i}: {row_text}")

    return {
        "content_type": "table",
        "columns": list(df.columns),
        "row_count": len(rows),
        "rows": rows,
        "text": "\n".join(text_rows),
    }