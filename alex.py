#!/usr/bin/env python3
import argparse, csv, json, os, sys, urllib.parse, pathlib
from typing import List, Dict, Any

try:
    import yaml  # pyyaml
except Exception:
    yaml = None

DEFAULT_PROMPT = "Summarize and briefly comment on this source ({URL}). Give 3 bullet takeaways and a 1-paragraph context. Note any obvious biases or missing angles."

def perplexity_link(url: str, prompt: str) -> str:
    p = prompt.replace("{URL}", url)
    return "https://www.perplexity.ai/search?q=" + urllib.parse.quote(p, safe="")

def claude_link(url: str, prompt: str) -> str:
    p = prompt.replace("{URL}", url)
    return "https://claude.ai/new?q=" + urllib.parse.quote(p, safe="")

def read_csv(path: str) -> List[Dict[str, str]]:
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            title = (r.get("title") or "").strip()
            url = (r.get("url") or "").strip()
            note = (r.get("note") or "").strip()
            if not title or not url:
                continue
            out.append({"title": title, "url": url, "note": note})
    return out

def emit_html(title: str, subtitle: str, prompt: str, rows: List[Dict[str,str]], out_path: str):
    from datetime import datetime, timezone
    def html_escape(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
    def build_item(r):
        note = f"<blockquote>{html_escape(r['note'])}</blockquote>" if r.get('note') else ""
        return f'''<div class="card">
  <div class="title">{html_escape(r['title'])}</div>
  {note}
  <div class="btns">
    <a class="btn" href="{perplexity_link(r['url'], prompt)}" target="_blank">Open in Perplexity</a>
    <a class="btn" href="{claude_link(r['url'], prompt)}" target="_blank">Open in Claude</a>
    <a class="btn link" href="{r['url']}" target="_blank">Original link</a>
  </div>
</div>'''
    items = "\n".join(build_item(r) for r in rows)
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html_escape(title)}</title>
<style>
body{{font-family:system-ui;background:#0f172a;color:#e5e7eb;margin:0;padding:2rem}}
.card{{background:#111827;border-radius:12px;padding:1rem;margin-bottom:1rem;border:1px solid #1f2937}}
.title{{font-weight:700;font-size:18px;margin-bottom:.5rem}}
.btns{{display:flex;gap:8px;flex-wrap:wrap}}
a.btn{{padding:6px 10px;border-radius:8px;background:#1f2937;text-decoration:none;color:#e5e7eb}}
a.btn:hover{{background:#374151}}
blockquote{{margin:.5rem 0;color:#9ca3af;border-left:3px solid #334155;padding-left:.5rem}}
</style></head>
<body>
<h1>{html_escape(title)}</h1>
<p>{html_escape(subtitle)}</p>
{items}
<footer><small>Prompt: {html_escape(prompt)}<br>Updated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</small></footer>
</body></html>"""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f: f.write(html)
    print(f"Wrote HTML -> {out_path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    if yaml is None:
        print("Missing dependency pyyaml. Install it with: pip install pyyaml")
        sys.exit(2)
    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    for lst in cfg.get("lists", []):
        csv_path = os.path.join(args.root, lst["src"])
        rows = read_csv(csv_path)
        emit_html(lst["title"], lst.get("subtitle",""), lst["prompt"], rows,
                  os.path.join(args.root, lst["out_html"]))

if __name__ == "__main__":
    main()

