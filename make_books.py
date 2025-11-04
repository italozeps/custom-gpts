from pathlib import Path
import csv

input_path = Path("C:/python.lab/books.txt")
output_path = Path("C:/python.lab/make_books.csv")

rows = []
with input_path.open(encoding="utf-8") as f:
    for line in f:
        parts = [p.strip() for p in line.strip().split(",")]
        if len(parts) >= 3:
            title = ", ".join(parts[:-2])
            url = parts[-2]
            note = parts[-1]
            rows.append([title, url, note])

output_path.parent.mkdir(parents=True, exist_ok=True)
with output_path.open("w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["title", "url", "note"])
    writer.writerows(rows)
