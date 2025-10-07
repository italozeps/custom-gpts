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
        fieldnames = reader.fieldnames or []
        for row in reader:
            rec = { (k or "").strip(): (row.get(k, "") or "").strip()
                    for k in fieldnames }
            if not rec.get("slug"):
                rec["slug"] = slug_guess
            rows.append(rec)
    return rows

# ---------- MODULES ----------
def build_modules():
    src = ROOT / "gpts.csv"
    modules = []
    if src.exists():
        with src.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                modules.append({k: (row.get(k, "") or "").strip()
                                for k in (reader.fieldnames or [])})
    out = DOCS / "index.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(modules, f, ensure_ascii=False, indent=2)
    print(f"[build] modules: {len(modules)} ieraksti -> docs/index.json")

# ---------- TERMS ----------
def build_terms():
    terms = []
    for p in sorted(GPTS.rglob("terms.csv")):
        parts = p.parts
        slug_guess = ""
        if "gpts" in parts:
            i = parts.index("gpts")
            if i + 1 < len(parts):
                slug_guess = parts[i + 1]
        take = read_csv_rows(p, slug_guess)
        print(f"[scan] terms: {p} -> {len(take)}")
        terms += take

    root_terms = GPTS / "terms.csv"
    if root_terms.exists():
        take = read_csv_rows(root_terms, "")
        print(f"[scan] terms(root): {root_terms} -> {len(take)}")
        terms += take

    out = DOCS / "terms.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(terms, f, ensure_ascii=False, indent=2)
    print(f"[build] terms: {len(terms)} ieraksti -> docs/terms.json")

# ---------- ARTICLES (VISUS gpts/**/articles.csv + sakne, ja ir) ----------
def build_articles():
    articles = []
    for p in sorted(GPTS.rglob("articles.csv")):
        parts = p.parts
        slug_guess = ""
        if "gpts" in parts:
            i = parts.index("gpts")
            if i + 1 < len(parts):
                slug_guess = parts[i + 1]
        take = read_csv_rows(p, slug_guess)
        print(f"[scan] articles: {p} (slug={slug_guess}) -> {len(take)}")
        articles += take

    root_csv = GPTS / "articles.csv"
    if root_csv.exists():
        take = read_csv_rows(root_csv, "")
        print(f"[scan] articles(root): {root_csv} -> {len(take)}")
        articles += take

    out = DOCS / "articles.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump({"articles": articles}, f, ensure_ascii=False, indent=2)
    print(f"[build] articles: {len(articles)} ieraksti -> docs/articles.json")
    # parādām dažus ierakstus pārbaudei
    for rec in articles[:3]:
        print(f"[peek] {rec.get('slug','?')} | {rec.get('title','')} | {rec.get('year','')}")

def main():
    build_modules()
    build_terms()
    build_articles()

if __name__ == "__main__":
    main()
