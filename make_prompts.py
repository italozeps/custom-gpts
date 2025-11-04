from pathlib import Path
import csv

def make_prompts(txt_path: str, csv_path: str):
    inp = Path(txt_path)
    outp = Path(csv_path)
    lines = [ln.strip() for ln in inp.read_text(encoding="utf-8").splitlines() if ln.strip()]
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["prompt_id", "prompt"])
        for i, p in enumerate(lines, start=1):
            w.writerow([i, p])

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python make_prompts.py <input_txt> <output_csv>")
        raise SystemExit(1)
    make_prompts(sys.argv[1], sys.argv[2])
