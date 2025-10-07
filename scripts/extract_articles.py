#!/usr/bin/env python3
import re, csv, os, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]  # repo sakne
GPTS = ROOT / "gpts"

HDR = ["key","title","authors","year","venue","url","tags"]

HDR_PAT = re.compile(r'^\s{0,3}#{1,6}\s*(Literatūras norādes|Literatūra|References)\b', re.I)
ITEM_PAT = re.compile(r'^\s*(?:[-*]|\d+[.)\]])\s+(.*)')  # markdown punkts
YEAR_PAT = re.compile(r'\b(1[6-9]\d{2}|20\d{2}|21\d{2})\b')
URL_PAT  = re.compile(r'(https?://\S+)')

def parse_items(block:str):
    items = []
    buf = []
    for line in block.splitlines():
        m = ITEM_PAT.match(line)
        if m:
            if buf:
                items.append(" ".join(buf).strip())
                buf = []
            buf.append(m.group(1).strip())
        else:
            # turpinājuma rinda (atkāpe)
            if line.strip()=="" and not buf:
                continue
            if buf:
                buf.append(line.strip())
    if buf: items.append(" ".join(buf).strip())
    return items

def split_to_fields(txt:str):
    # URL
    url = None
    mu = URL_PAT.search(txt)
    if mu:
        url = mu.group(1).rstrip(').,;')
        txt = txt.replace(mu.group(1), '').strip()

    # Year
    year = None
    my = YEAR_PAT.search(txt)
    if my:
        year = my.group(1)

    # Mēģinām autori — nosaukums: dalām pēc " — " vai " - "
    authors, title = None, txt
    for sep in [' — ', ' – ', ' - ']:
        if sep in txt:
            parts = [p.strip() for p in txt.split(sep, 1)]
            if len(parts) == 2:
                authors, title = parts[0], parts[1]
                break

    # Ja nosaukums iekavās/iekavās ar kursīvu zvaigznēm, noņemam zīmes
    title = title.strip().strip('*').strip('_').strip('“”"\'')
    return authors or "", title, year or "", "", url or "", ""

def extract_for_slug(slug_dir:pathlib.Path):
    prompt = slug_dir / "prompt.md"
    if not prompt.exists(): return 0
    text = prompt.read_text(encoding="utf-8", errors="ignore")

    # atrodam sadaļu no virsraksta līdz nākamajam virsrakstam vai EOF
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if HDR_PAT.match(line):
            start = i + 1
            break
    if start is None: return 0

    end = len(lines)
    for j in range(start, len(lines)):
        if HDR_PAT.match(lines[j]) or re.match(r'^\s{0,3}#{1,6}\s+\S', lines[j]):
            end = j
            break

    block = "\n".join(lines[start:end])
    items = parse_items(block)
    if not items: return 0

    rows = []
    slug = slug_dir.name
    for idx, it in enumerate(items, 1):
        authors, title, year, venue, url, tags = split_to_fields(it)
        key = f"{slug}-{idx:02d}"
        rows.append([key, title, authors, year, venue, url, tags])

    out = slug_dir / "articles.csv"
    wrote = False
    if not out.exists() or True:
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(HDR)
            w.writerows(rows)
        wrote = True
    return len(rows) if wrote else 0

def main():
    total = 0
    for slug_dir in sorted(p for p in GPTS.iterdir() if p.is_dir()):
        n = extract_for_slug(slug_dir)
        if n:
            print(f"[extract] {slug_dir.name}: {n} ieraksti")
            total += n
    print(f"Kopā izvilkts: {total}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
