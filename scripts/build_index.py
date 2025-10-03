import os, csv, json, yaml

ROOT = "."
GPTS_DIR = os.path.join(ROOT, "gpts")
CSV_REG = os.path.join(ROOT, "gpts.csv")
DOCS_DIR = os.path.join(ROOT, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

# Reģistrs no gpts.csv
reg = {}
if os.path.exists(CSV_REG):
    with open(CSV_REG, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            slug = (r.get("slug") or "").strip()
            if slug:
                reg[slug] = r

modules, terms, articles = [], [], []

# Katrs modulis
if os.path.isdir(GPTS_DIR):
    for slug in sorted(d for d in os.listdir(GPTS_DIR) if os.path.isdir(os.path.join(GPTS_DIR, d))):
        base = os.path.join(GPTS_DIR, slug)
        cfg_path    = os.path.join(base, "config.yaml")
        prompt_path = os.path.join(base, "prompt.md")
        terms_path  = os.path.join(base, "terms.csv")
        arts_path   = os.path.join(base, "articles.csv")

        cfg, prompt = {}, ""
        if os.path.exists(cfg_path):
            with open(cfg_path, encoding="utf-8") as f: cfg = yaml.safe_load(f) or {}
        if os.path.exists(prompt_path):
            with open(prompt_path, encoding="utf-8") as f: prompt = f.read()

        modules.append({
            "slug": slug,
            "name": cfg.get("name") or reg.get(slug, {}).get("name") or slug,
            "languages": cfg.get("languages") or [],
            "domains": cfg.get("domains") or [],
            "purpose": reg.get(slug, {}).get("purpose") or "",
            "status":  reg.get(slug, {}).get("status") or "",
            "owner":   reg.get(slug, {}).get("owner") or "",
            "last_edit": reg.get(slug, {}).get("last_edit") or "",
            "openai_link": reg.get(slug, {}).get("openai_link") or "",
            "dataset_link": reg.get(slug, {}).get("dataset_link") or "",
            "notes":   reg.get(slug, {}).get("notes") or "",
            "prompt":  prompt
        })

        if os.path.exists(terms_path):
            with open(terms_path, encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    r = {k:(v or "") for k,v in r.items()}
                    r["slug"] = slug
                    terms.append(r)

        if os.path.exists(arts_path):
            with open(arts_path, encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    r = {k:(v or "") for k,v in r.items()}
                    r["slug"] = slug
                    articles.append(r)

# Izvada uz docs/
with open(os.path.join(DOCS_DIR, "index.json"), "w", encoding="utf-8") as f:
    json.dump({"modules": modules}, f, ensure_ascii=False)
with open(os.path.join(DOCS_DIR, "terms.json"), "w", encoding="utf-8") as f:
    json.dump({"terms": terms}, f, ensure_ascii=False)
with open(os.path.join(DOCS_DIR, "articles.json"), "w", encoding="utf-8") as f:
    json.dump({"articles": articles}, f, ensure_ascii=False)

print(f"Built: {len(modules)} modules, {len(terms)} terms, {len(articles)} articles")
