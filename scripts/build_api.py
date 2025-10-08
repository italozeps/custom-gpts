#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

def load(path, default):
    p = DOCS / path
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return default

modules = load("index.json", [])
terms   = load("terms.json", [])
artsraw = load("articles.json", [])
articles = artsraw if isinstance(artsraw, list) else artsraw.get("articles", [])

api = {"modules": modules, "terms": terms, "articles": articles}
(DOCS / "api.json").write_text(json.dumps(api, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[api] modules={len(modules)}, terms={len(terms)}, articles={len(articles)} -> docs/api.json")
