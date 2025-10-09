#!/usr/bin/env python3
# scripts/build_jsonld.py
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

# ---- palīgfunkcijas ----
def load_json(name, default):
    p = DOCS / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

def split_authors(s):
    s = (s or "").strip()
    if not s:
        return []
    # šķeļ pēc ';' vai ',' — Zenodo/CSV stili dažādi
    parts = [x.strip() for x in re.split(r';|,', s) if x.strip()]
    # atmet pārāk īsus trokšņus
    return [p for p in parts if len(p) > 1]

def tags_list(s):
    s = (s or "").strip()
    if not s:
        return []
    # atbalstām “a;b;c” vai “a, b, c”
    raw = re.split(r';|,', s)
    return [t.strip() for t in raw if t.strip()]

def best_url(url, venue):
    u = (url or "").strip()
    if u:
        return u
    # ja DOI iekš venue, pielīmē doi.org
    if venue and "10." in venue:
        doi = venue.strip()
        # rupjš DOI detektors
        m = re.search(r'(10\.\d{4,9}/\S+)', doi)
        if m:
            return f"https://doi.org/{m.group(1)}"
    return None

# ---- ielādē datus no iepriekšējiem indeksiem ----
modules = load_json("index.json", [])
terms   = load_json("terms.json", [])
artsraw = load_json("articles.json", [])
articles = artsraw if isinstance(artsraw, list) else artsraw.get("articles", [])

# ---- Articles → JSON-LD saraksts (CreativeWork / ScholarlyArticle) ----
jsonld_articles = []
for rec in articles:
    title   = (rec.get("title") or rec.get("key") or "").strip()
    authors = split_authors(rec.get("authors", ""))
    year    = (rec.get("year") or "").strip()
    venue   = (rec.get("venue") or "").strip()
    url     = best_url(rec.get("url", ""), venue)
    slug    = (rec.get("slug") or "").strip()
    keywords = tags_list(rec.get("tags", ""))

    # min targetType: ScholarlyArticle, ja ir akad. pazīmes
    typ = "ScholarlyArticle" if any(k.lower() in {"journal","conference","preprint","thesis"} for k in keywords) or venue else "CreativeWork"

    obj = {
      "@context": "https://schema.org",
      "@type": typ,
      "name": title or None,
      "author": [{"@type":"Person","name": a} for a in authors] or None,
      "datePublished": year or None,
      "isPartOf": {
          "@type": "CreativeWorkSeries",
          "name": slug or None,
          "url": f"https://italozeps.github.io/custom-gpts/#mod-{slug}" if slug else None
      } if slug else None,
      "url": url or None,
      "keywords": keywords or None
    }
    # notīri None laukus
    obj = {k:v for k,v in obj.items() if v not in (None, [], {})}
    jsonld_articles.append(obj)

(DOCS/"articles.jsonld").write_text(
    json.dumps(jsonld_articles, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
print(f"[jsonld] articles: {len(jsonld_articles)} -> docs/articles.jsonld")

# ---- Modules → JSON-LD saraksts (CreativeWorkSeries) ----
jsonld_modules = []
for m in modules:
    slug = (m.get("slug") or "").strip()
    name = (m.get("name") or slug or "Module").strip()
    purpose = (m.get("purpose") or "").strip()
    langs = (m.get("languages") or m.get("lang") or "").strip()
    domains = (m.get("domains") or "").strip()

    obj = {
      "@context": "https://schema.org",
      "@type": "CreativeWorkSeries",
      "name": name,
      "alternateName": slug or None,
      "description": purpose or None,
      "inLanguage": [x for x in re.split(r'[,\s]+', langs) if x] or None,
      "about": [x for x in re.split(r'[,\s]+', domains) if x] or None,
      "url": f"https://italozeps.github.io/custom-gpts/#mod-{slug}" if slug else "https://italozeps.github.io/custom-gpts/"
    }
    obj = {k:v for k,v in obj.items() if v not in (None, [], {})}
    jsonld_modules.append(obj)

(DOCS/"modules.jsonld").write_text(
    json.dumps(jsonld_modules, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
print(f"[jsonld] modules: {len(jsonld_modules)} -> docs/modules.jsonld")
