#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
alex.py — īsais variants: ģenerē statisku HTML ar 5 LLM pogām.
CSV (UTF-8): kolonnas title,url,note
Konfigurācija (YAML): lists: [title, subtitle, src, out_html, prompt]
- Perplexity: ?q=… (prefill)
- Claude/Gemini/Mistral/DeepSeek: atver čatu un AUTOCOPY promptu ar URL
"""

import argparse
import csv
import html
import json
from pathlib import Path
from urllib.parse import quote_plus
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    raise SystemExit("Missing dependency pyyaml. Install it with: pip install pyyaml")

# ---------- Palīgfunkcijas ----------

LLMS = [
    ("Perplexity", "https://www.perplexity.ai/search?q={Q}", False),
    ("Claude",     "https://claude.ai/new",                  True),
    ("Gemini",     "https://gemini.google.com/app",          True),
    ("Mistral",    "https://chat.mistral.ai/chat",           True),
    ("DeepSeek",   "https://chat.deepseek.com/",             True),
]

def esc(s: str) -> str:
    return html.escape(s or "", quote=True)

def read_csv(path: Path):
    items = []
    with path.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            url = (r.get("url") or "").strip()
            if not url:
                continue
            title = (r.get("title") or "").strip() or url
            note  = (r.get("note")  or "").strip()
            items.append({"title": title, "url": url, "note": note})
    return items

def full_prompt(prompt: str, url: str) -> str:
    return prompt.replace("{URL}", url) if "{URL}" in prompt else f"{prompt} {url}"

# ---------- HTML ģenerēšana ----------

def render_html(title: str, subtitle: str, prompt: str, rows):
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    prompt_show = esc(prompt).replace("{", "&#123;").replace("}", "&#125;")

    head = f"""<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>{esc(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
function copyPrompt(txt){{
  if(!navigator.clipboard) return;
  navigator.clipboard.writeText(txt).then(()=>{
    const n=document.createElement('div');
    n.textContent='Prompt copied. Paste in the chat (Ctrl+V).';
    n.style.position='fixed'; n.style.bottom='16px'; n.style.right='16px';
    n.style.background='#111'; n.style.color='#fff'; n.style.padding='8px 12px';
    n.style.borderRadius='8px'; n.style.opacity='0.95'; n.style.zIndex='9999';
    document.body.appendChild(n); setTimeout(()=>n.remove(),1800);
  }});
}}
</script>
<style>
  :root {{ --maxw: 950px; --border:#e5e7eb; --muted:#6b7280; }}
  body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin:2rem auto; max-width:var(--maxw); padding:0 1rem; }}
  h1 {{ margin:0 0 .25rem 0; font-size:1.6rem; }}
  .muted {{ color:var(--muted); margin:0 0 1rem 0; }}
  .grid {{ display:grid; grid-template-columns:1fr; gap:1rem; }}
  @media (min-width:760px) {{ .grid {{ grid-template-columns:1fr 1fr; }} }}
  .card {{ border:1px solid var(--border); border-radius:12px; padding:1rem; }}
  .card h3 {{ margin:.1rem 0 .5rem 0; font-size:1.05rem; }}
  .note {{ margin:0 0 .5rem 0; color:var(--muted); }}
  .link a {{ word-break:break-all; }}
  .btns {{ display:flex; flex-wrap:wrap; gap:.5rem; margin-top:.6rem; }}
  .btn {{ display:inline-block; padding:.4rem .6rem; border-radius:.5rem; text-decoration:none; border:1px solid #d1d5db; }}
  .btn:hover {{ background:#f5f5f5; }}
  footer {{ margin-top:2rem; font-size:.9rem; color:var(--muted); }}
  code.prompt {{ white-space:pre-wrap; }}
</style>
<h1>{esc(title)}</h1>
<p class="muted">{esc(subtitle)}</p>
<div class="grid">
"""
    parts = [head]

    for r in rows:
        fp = full_prompt(prompt, r["url"])
        q  = quote_plus(fp)
        btns = []
        for label, base, needs_copy in LLMS:
            if "{Q}" in base:  # Perplexity ar prefill
                href = base.replace("{Q}", q)
                btns.append(f'<a class="btn" href="{esc(href)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>')
            else:
                # Atver čatu + kopē promptu
                js_arg = json.dumps(fp)  # droši JS stringā
                btns.append(
                    f'<a class="btn" href="{esc(base)}" target="_blank" rel="noopener noreferrer" '
                    f'onclick="copyPrompt({esc(js_arg)})">{esc(label)}</a>'
                )
        # Oriģinālā saite kā atsevišķa poga
        btns.append(f'<a class="btn" href="{esc(r["url"])}" target="_blank" rel="noopener noreferrer">Original link</a>')

        parts.append(f"""
  <div class="card">
    <h3>{esc(r["title"])}</h3>
    <p class="note">{esc(r["note"])}</p>
    <p class="link"><a href="{esc(r["url"])}" target="_blank" rel="noopener noreferrer">{esc(r["url"])}</a></p>
    <div class="btns">{' '.join(btns)}</div>
  </div>
""")

    parts.append(f"""</div>
<footer>
  <p><strong>Prompt:</strong> <code class="prompt">{prompt_show}</code></p>
  <p>Updated {updated}</p>
</footer>
</html>
""")
    return "".join(parts)

# ---------- Galvenais ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to alex_config.yaml")
    ap.add_argument("--root", default=".", help="Project root (paths in config are relative to this)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    cfg_path = (root / args.config).resolve()
    if not cfg_path.exists():
        raise SystemExit(f"Config file not found: {cfg_path}")

    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    lists = cfg.get("lists") or []
    if not lists:
        raise SystemExit("No 'lists' found in alex_config.yaml")

    for block in lists:
        title    = block.get("title", "Untitled")
        subtitle = block.get("subtitle", "")
        src_rel  = block.get("src")
        out_rel  = block.get("out_html")
        prompt   = block.get("prompt", "For ({URL}): summarize in 3 key points and 1-line significance.")

        if not src_rel or not out_rel:
            print(f"[skip] Missing 'src' or 'out_html' in block titled: {title}")
            continue

        src = (root / src_rel).resolve()
        out = (root / out_rel).resolve()
        if not src.exists():
            print(f"[warn] Source not found: {src}")
            continue
        if src.suffix.lower() != ".csv":
            print(f"[warn] Unsupported source type (only .csv supported): {src.name}")
            continue

        rows = read_csv(src)
        if not rows:
            print(f"[warn] No rows in {src}")
            continue

        html_str = render_html(title, subtitle, prompt, rows)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html_str, encoding="utf-8")
        print(f"Wrote HTML -> {out}")

if __name__ == "__main__":
    main()
