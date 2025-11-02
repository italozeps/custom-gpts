#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
alex.py — statiskas HTML lapas ģenerators no CSV saraksta, ar LLM pogām.

Atbalsta:
- Konfigurāciju no alex_config.yaml (lists: [title, subtitle, src, out_html, prompt])
- CSV (UTF-8) ar kolonnām: title,url,note
- LLM pogas: Perplexity, Claude, Gemini, Mistral, DeepSeek, (opc.) ChatGPT

Lietošana (lokāli):
    python alex.py --config alex_config.yaml --root .

GitHub Actions gadījumā pietiek iestumt izmaiņas alex_config.yaml / data/*.csv,
workflow to palaidīs automātiski un ielikts docs/… HTML.
"""

import argparse
import csv
import html
import os
from pathlib import Path
from urllib.parse import quote_plus
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    raise SystemExit("Missing dependency pyyaml. Install it with: pip install pyyaml")


# ---------- Palīgfunkcijas ----------

def read_csv(path: Path):
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for i, r in enumerate(rdr, 1):
            title = (r.get("title") or "").strip()
            url = (r.get("url") or "").strip()
            note = (r.get("note") or "").strip()
            if not url:
                # ignorē tukšu rindu
                continue
            # ja nav title, izmanto URL
            if not title:
                title = url
            rows.append({"title": title, "url": url, "note": note})
    return rows


def ensure_parent_dir(out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)


def build_llm_links(url: str, prompt: str):
    """
    Veido (label, href) sarakstu visām LLM pogām.
    Ja prompt satur {URL}, aizstāj to; citādi pievieno URL teikuma beigās.
    """
    msg = prompt.replace("{URL}", url) if "{URL}" in prompt else f"{prompt} {url}"

    links = [
        ("Perplexity", f"https://www.perplexity.ai/search?q={quote_plus(msg)}"),
        ("Claude",     f"https://claude.ai/new?prompt={quote_plus(msg)}"),
        ("Gemini",     f"https://gemini.google.com/app?q={quote_plus(msg)}"),
        ("Mistral",    f"https://chat.mistral.ai/chat?message={quote_plus(msg)}"),
        ("DeepSeek",   f"https://chat.deepseek.com/?q={quote_plus(msg)}"),
        # Ja gribi, atkomentē arī ChatGPT:
        # ("ChatGPT",    "https://chat.openai.com/"),
    ]
    return links


def escape(s: str) -> str:
    """Drošības pēc HTML-escape (arī lai { } neradītu problēmas)."""
    return html.escape(s, quote=True)


def render_html(title: str, subtitle: str, prompt: str, items: list[dict]):
    head = f"""<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>{escape(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {{
    --maxw: 980px;
    --border: #e9e9e9;
    --muted: #6b7280;
  }}
  body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 2rem auto; max-width: var(--maxw); padding: 0 1rem; }}
  h1 {{ margin: 0 0 .25rem 0; font-size: 1.6rem; }}
  .muted {{ color: var(--muted); margin: 0 0 1rem 0; }}
  .grid {{ display: grid; grid-template-columns: 1fr; gap: 1rem; }}
  @media (min-width: 740px) {{ .grid {{ grid-template-columns: 1fr 1fr; }} }}
  .card {{ border: 1px solid var(--border); border-radius: 12px; padding: 1rem; }}
  .card h3 {{ margin: 0 0 .5rem 0; font-size: 1.05rem; }}
  .note {{ margin: 0 0 .5rem 0; color: var(--muted); }}
  .link a {{ word-break: break-all; }}
  .btns {{ display:flex; flex-wrap:wrap; gap:.5rem; margin-top:.6rem; }}
  .btn {{ display:inline-block; padding:.4rem .6rem; border-radius:.5rem; text-decoration:none; border:1px solid #d1d5db; }}
  .btn:hover {{ background:#f5f5f5; }}
  footer {{ margin-top: 2rem; font-size: .9rem; color: var(--muted); }}
  code.prompt {{ white-space: pre-wrap; }}
</style>
<h1>{escape(title)}</h1>
<p class="muted">{escape(subtitle)}</p>
<div class="grid">
"""
    parts = [head]

    for it in items:
        # LLM pogas
        btns = []
        for label, href in build_llm_links(it["url"], prompt):
            btns.append(f'<a class="btn" href="{href}" target="_blank" rel="noopener noreferrer">{escape(label)}</a>')
        buttons_html = " ".join(btns)

        parts.append(f"""
  <div class="card">
    <h3>{escape(it['title'])}</h3>
    <p class="note">{escape(it.get('note',''))}</p>
    <p class="link"><a href="{escape(it['url'])}" target="_blank" rel="noopener noreferrer">{escape(it['url'])}</a></p>
    <div class="btns">{buttons_html}</div>
  </div>
""")

    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    prompt_show = escape(prompt).replace("{", "&#123;").replace("}", "&#125;")
    parts.append(f"""</div>
<footer>
  <p><strong>Prompt:</strong> <code class="prompt">{prompt_show}</code></p>
  <p>Updated {updated}</p>
</footer>
</html>
""")
    return "".join(parts)


# ---------- Galvenais cikls ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to alex_config.yaml")
    ap.add_argument("--root", default=".", help="Project root (paths in config are relative to this)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    cfg_path = (root / args.config).resolve()

    if not cfg_path.exists():
        raise SystemExit(f"Config file not found: {cfg_path}")

    with cfg_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    lists = cfg.get("lists") or []
    if not lists:
        raise SystemExit("No 'lists' found in alex_config.yaml")

    for block in lists:
        title = block.get("title", "Untitled")
        subtitle = block.get("subtitle", "")
        src_rel = block.get("src")
        out_rel = block.get("out_html")
        prompt = block.get("prompt", "For ({URL}): summarize in 3 key points and 1-line significance.")

        if not src_rel or not out_rel:
            print(f"[skip] Missing 'src' or 'out_html' in block titled: {title}")
            continue

        csv_path = (root / src_rel).resolve()
        out_path = (root / out_rel).resolve()

        if not csv_path.exists():
            print(f"[warn] Source not found: {csv_path}")
            continue

        # CSV (UTF-8)
        rows = read_csv(csv_path)
        if not rows:
            print(f"[warn] No rows in {csv_path}")
            continue

        html_str = render_html(title, subtitle, prompt, rows)
        ensure_parent_dir(out_path)
        out_path.write_text(html_str, encoding="utf-8")
        print(f"Wrote HTML -> {out_path}")

if __name__ == "__main__":
    main()
