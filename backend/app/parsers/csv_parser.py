import csv

def parse_csv(file_path: str) -> dict:
    rows = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    text = "\n".join([", ".join(f"{k}: {v}" for k, v in row.items()) for row in rows])
    return {
        "content_type": "spreadsheet",
        "text": text,
        "row_count": len(rows),
    }