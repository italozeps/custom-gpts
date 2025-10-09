#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/"docs"; DOCS.mkdir(exist_ok=True)
def load(name, default): 
    p=DOCS/name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default
mods=load("index.json", []); terms=load("terms.json", [])
artsraw=load("articles.json", []); arts=artsraw if isinstance(artsraw, list) else artsraw.get("articles", [])
out={"modules":mods, "terms":terms, "articles":arts}
(DOCS/"api.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[api] modules={len(mods)}, terms={len(terms)}, articles={len(arts)} -> docs/api.json")
