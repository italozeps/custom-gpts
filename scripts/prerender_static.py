#!/usr/bin/env python3
import json, html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/"docs"
mods=json.loads((DOCS/"index.json").read_text(encoding="utf-8")) if (DOCS/"index.json").exists() else []
def esc(s): return html.escape((s or "").strip())
rows=[]
for m in mods:
    slug=m.get("slug",""); name=m.get("name",""); purpose=m.get("purpose",""); status=m.get("status","")
    repo=f"https://github.com/italozeps/custom-gpts/tree/main/gpts/{slug}"
    prompt=f"https://raw.githubusercontent.com/italozeps/custom-gpts/main/gpts/{slug}/prompt.md"
    rows.append(f"<tr><td>{esc(slug)}</td><td>{esc(name)}</td><td>{esc(purpose)}</td><td>{esc(status)}</td><td><a href='{repo}'>repo</a> · <a href='{prompt}'>prompt</a></td></tr>")
html_doc=f"""<!doctype html><meta charset="utf-8">
<title>Custom GPTs — statiskais indekss (No-JS)</title>
<link rel="alternate" type="application/json" href="api.json">
<body style="font-family:system-ui,Segoe UI,Arial,sans-serif; padding:16px;">
<h1>Custom GPTs — statiskais indekss</h1>
<p>Šī ir statiska (No-JS) versija. API: <a href="api.json">api.json</a>.</p>
<table border="1" cellpadding="6" cellspacing="0">
<thead><tr><th>Slug</th><th>Nosaukums</th><th>Mērķis</th><th>Statuss</th><th>Linki</th></tr></thead>
<tbody>{''.join(rows) if rows else '<tr><td colspan=5>Nav datu.</td></tr>'}</tbody></table>
</body>"""
(DOCS/"index_noscript.html").write_text(html_doc, encoding="utf-8")
print(f"[static] {len(mods)} moduļi -> docs/index_noscript.html")
