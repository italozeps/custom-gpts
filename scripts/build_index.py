#!/usr/bin/env python3
# scripts/build_index.py
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
GPTS = ROOT / "gpts"
DOCS.mkdir(parents=True, exist_ok=True)

def read_csv_rows(path: Path, slug_guess: str = ""):
    rows = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rec = { (k or "").strip(): (row.get(k, "") or "").strip()
                    for k in (reader.fieldnames or []) }
            if "slug" not in rec or not rec["slug"]:
                rec["slug"] = slug_guess
            rows.append(rec)
    return rows

def build_modules():
    src = ROOT / "gpts.csv"
    modules = []
    if src.exists():
        with src.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                modules.append({k: (row.get(k, "") or "").strip()
                                for k in reader.fieldnames or []})
    out = DOCS / "index.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(modules, f, ensure_ascii=False, indent=2)
    print(f"[build] modules: {len(modules)} ieraksti -> docs/index.json")

def build_terms():
    terms = []
    for p in GPTS.rglob("terms.csv"):
        parts = p.parts
        slug_guess = ""
        if "gpts" in parts:
            i = parts.index("gpts")
            if i + 1 < len(parts):
                slug_guess = parts[i + 1]
        terms += read_csv_rows(p, slug_guess)
    root_terms = GPTS / "terms.csv"
    if root_terms.exists():
        terms += read_csv_rows(root_terms, "")
    out = DOCS / "terms.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(terms, f, ensure_ascii=False, indent=2)
    print(f"[build] terms: {len(terms)} ieraksti -> docs/terms.json")

def build_articles():
    articles = []
    for p in GPTS.rglob("articles.csv"):
        parts = p.parts
        slug_guess = ""
        if "gpts" in parts:
            i = parts.index("gpts")
            if i + 1 < len(parts):
                slug_guess = parts[i + 1]
        articles += read_csv_rows(p, slug_guess)
    root_csv = GPTS / "articles.csv"
    if root_csv.exists():
        articles += read_csv_rows(root_csv, "")
    out = DOCS / "articles.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump({"articles": articles}, f, ensure_ascii=False, indent=2)
    print(f"[build] articles: {len(articles)} ieraksti -> docs/articles.json")

def main():
    build_modules()
    build_terms()
    build_articles()

if __name__ == "__main__":
    main()
