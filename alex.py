#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
alex.py — ģenerē statisku HTML ar 5 LLM pogām:
Perplexity, You.com, Kagi, Phind (prefill ?q=), un NotebookLM (kopē → atver)
"""

import argparse
import base64
import csv
import html
from pathlib import Path
from urllib.parse import quote_plus, urlparse
from datetime import datetime, timezone
import yaml

LLMS = [
    ("Perplexity", "https://www.perplexity.ai/search?q={Q}", False),
    ("You.com",    "https://you.com/search?q={Q}",           False),
    ("Kagi",       "https://kagi.com/search?q={Q}",          False),
    ("Phind",      "https://www.phind.com/search?q={Q}",     False),
    ("NotebookLM", "https://notebooklm.google.com/",          True),
]

def esc(s): return html.escape(s or "", quote=True)

def normalize_url(u):
    u = (u or "").strip()
    if not u: return u
    if u.startswith("<") and u.endswith(">"): u = u[1:-1].strip()
    p = urlparse(u)
    if not p.scheme:
        u = "https://" + u
        print(f"[warn] URL without scheme -> assumed https://{u}")
    return u

def read_csv(path: Path):
    items = []
    with path.open(newline="", encoding="utf-8") as f:
        import csv
        rdr = csv.DictReader(f)
        for r in rdr:
            url = normalize_url(r.get("url") or "")
            if not url: continue
            title = (r.get("title") or "").strip() or url
            note  = (r.get("note")  or "").strip()
            items.append({"title": title, "url": url, "note": note})
    print(f"[info] loaded {len(items)} rows from {path}")
    return items

def render_html(title, subtitle, prompt, rows):
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    prompt_show = esc(prompt).replace("{", "&#123;").replace("}", "&#125;")

    head = f"""<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>{esc(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
function toast(msg){{
  const n=document.createElement('div');
  n.textContent=msg;
  Object.assign(n.style,{{position:'fixed',bottom:'16px',right:'16px',
    background:'#111',color:'#fff',padding:'8px 12px',borderRadius:'8px',zIndex:9999,opacity:0.95}});
  document.body.appendChild(n);setTimeout(()=>n.remove(),1800);
}}
function b64decode(b64){{try{{return decodeURIComponent(escape(atob(b64)));}}catch(e){{return atob(b64);}}}}
document.addEventListener('click',function(e){{
  const a=e.target.closest('a[data-llm="1"]');if(!a)return;
  e.preventDefault();
  const href=a.getAttribute('href'),b64=a.getAttribute('data-prompt-b64')||'',txt=b64decode(b64);
  const win=window.open('about:blank','_blank','noopener');const finish=()=>{{if(win)win.location=href;}};
  if(!navigator.clipboard||!window.isSecureContext){{finish();setTimeout(()=>alert('Paste (Ctrl+V):\\n\\n'+txt),50);return;}}
  navigator.clipboard.writeText(txt).then(()=>{{toast('Prompt copied. Paste (Ctrl+V).');finish();}})
  .catch(()=>{{finish();setTimeout(()=>alert('Paste (Ctrl+V):\\n\\n'+txt),50);}});
}},true);
</script>
<style>
  body{{font-family:system-ui,Arial,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;}}
  .grid{{display:grid;grid-template-columns:1fr;gap:1rem;}}
  @media(min-width:760px){{.grid{{grid-template-columns:1fr 1fr;}}}}
  .card{{border:1px solid #e5e7eb;border-radius:12px;padding:1rem;}}
  .btn{{display:inline-block;padding:.4rem .6rem;border:1px solid #d1d5db;border-radius:.5rem;text-decoration:none;}}
  .btn:hover{{background:#f5f5f5;}}
  footer{{margin-top:2rem;font-size:.9rem;color:#6b7280;}}
</style>
<h1>{esc(title)}</h1>
<p style="color:#6b7280">{esc(subtitle)}</p>
<div class="grid">
"""
    parts = [head]
    for r in rows:
        url = normalize_url(r["url"])
        fp = prompt.replace("{URL}", url) if "{URL}" in prompt else f"{prompt} {url}"
        q = quote_plus(fp)
        btns = []
        import base64
        for label, base, needs_copy in LLMS:
            if "{Q}" in base:
                href = base.replace("{Q}", q)
                btns.append(f'<a class="btn" href="{esc(href)}" rel="noopener noreferrer">{esc(label)}</a>')
            else:
                b64 = base64.b64encode(fp.encode("utf-8")).decode("ascii")
                btns.append(f'<a class="btn" href="{esc(base)}" rel="noopener noreferrer" data-llm="1" data-prompt-b64="{esc(b64)}">{esc(label)}</a>')
        parts.append(f"""
  <div class="card">
    <h3>{esc(r['title'])}</h3>
    <p style="color:#6b7280">{esc(r['note'])}</p>
    <p><a href="{esc(url)}" target="_blank">{esc(url)}</a></p>
    <div>{" ".join(btns)}</div>
  </div>
""")
    parts.append(f"""</div>
<footer>
  <p><strong>Prompt:</strong> <code>{prompt_show}</code></p>
  <p>Updated {updated}</p>
</footer>
</html>""")
    return "".join(parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    cfg = yaml.safe_load((root / args.config).read_text(encoding="utf-8"))
    for b in cfg.get("lists", []):
        src = root / b["src"]; out = root / b["out_html"]
        rows = read_csv(src)
        html = render_html(b["title"], b.get("subtitle",""), b["prompt"], rows)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print(f"[ok] {out}")

if __name__ == "__main__":
    main()
