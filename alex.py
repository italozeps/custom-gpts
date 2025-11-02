#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
alex.py — statiskas HTML lapas ģenerators no CSV, ar LLM pogām un dublikātu atmešanu.

Atbalsta:
- Konfigurāciju no alex_config.yaml (lists: [title, subtitle, src, out_html, prompt])
- CSV (UTF-8) ar kolonnām: title,url,note
- Dublikātu atmešana pēc normalizēta URL (http→https, noņem beigu '/' un lowercase)
- LLM pogas:
    * Perplexity  — atver ar ?q= (prefill)
    * Claude      — atver čatu + automātiski iekopē promptu
    * Gemini      — atver čatu + automātiski iekopē promptu
    * Mistral     — atver čatu + automātiski iekopē promptu
    * DeepSeek    — atver čatu + automātiski iekopē promptu
    # (ja gribi, var pievienot arī ChatGPT)

Lietošana lokāli:
    python alex.py --config alex_config.yaml --root .

GitHub Actions gadījumā pietiek iestumt izmaiņas alex_config.yaml / data/*.csv,
workflow to palaidīs automātiski un ieliks docs/… HTML.
"""

import argparse
import csv
import html
import json
import os
import re
from pathlib import Path
from urllib.parse import quote_plus
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    raise SystemExit("Missing dependency pyyaml. Install it with: pip install pyyaml")


# ---------- Palīgfunkcijas: I/O ----------

def read_csv(path: Path):
    """Nolasa CSV (UTF-8) ar kolonnām title,url,note."""
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            title = (r.get("title") or "").strip()
            url = (r.get("url") or "").strip()
            note = (r.get("note") or "").strip()
            if not url:
                continue
            if not title:
                title = url
            rows.append({"title": title, "url": url, "note": note})
    return rows


def ensure_parent_dir(out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)


# ---------- Palīgfunkcijas: URL normalizācija un dublikāti ----------

def norm_url(u: str) -> str:
    """Normalizē URL salīdzināšanai: https, bez beigu '/', lower-case."""
    if not u:
        return u
    u = u.strip()
    if u.startswith("http://"):
        u = "https://" + u[len("http://"):]
    u = re.sub(r"/+$", "", u)
    return u.lower()


def dedupe_rows(rows):
    """Atmet dublikātus pēc normalizēta URL; patur pirmo sastapto ierakstu."""
    seen = set()
    out = []
    dropped = 0
    for r in rows:
        nu = norm_url(r.get("url", ""))
        if not nu:
            continue
        if nu in seen:
            dropped += 1
            continue
        seen.add(nu)
        r["url"] = nu  # saglabā normalizēto URL arī izvadē
        out.append(r)
    return out, dropped


# ---------- Palīgfunkcijas: LLM pogas un HTML ----------

def escape(s: str) -> str:
    return html.escape(s or "", quote=True)


def build_llm_links(url: str, prompt: str):
    """
    Atgriež sarakstu ar (label, href, needs_copy, full_message).
      - Perplexity: ?q={message}, needs_copy=False
      - Claude/Gemini/Mistral/DeepSeek: atver čatu, needs_copy=True (copy to clipboard)
    """
    full = prompt.replace("{URL}", url) if "{URL}" in prompt else f"{prompt} {url}"

    links = [
        ("Perplexity", f"https://www.perplexity.ai/search?q={quote_plus(full)}", False, full),
        ("Claude",     "https://claude.ai/new",                                     True,  full),
        ("Gemini",     "https://gemini.google.com/app",                             True,  full),
        ("Mistral",    "https://chat.mistral.ai/chat",                              True,  full),
        ("DeepSeek",   "https://chat.deepseek.com/",                                True,  full),
        # Ja gribi, atkomentē arī ChatGPT:
        # ("ChatGPT",    "https://chat.openai.com/",                                  True,  full),
    ]
    return links


def render_html(title: str, subtitle: str, prompt: str, items):
    """Atgriež gatavu HTML virkni vienai lapai."""
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    prompt_show = escape(prompt).replace("{", "&#123;").replace("}", "&#125;")

    head = f"""<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>{escape(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
function copyPrompt(txt) {{
  if (!navigator.clipboard) return;
  navigator.clipboard.writeText(txt).then(() => {{
    const n = document.createElement('div');
    n.textContent = 'Prompt copied. Paste in the chat (Ctrl+V).';
    n.style.position='fixed'; n.style.bottom='16px'; n.style.right='16px';
    n.style.background='#111'; n.style.color='#fff'; n.style.padding='8px 12px';
    n.style.borderRadius='8px'; n.style.opacity='0.95'; n.style.zIndex='9999';
    document.body.appendChild(n);
    setTimeout(() => n.remove(), 1800);
  }}).catch(()=>{{}});
}}
</script>
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
        btns = []
        for (label, href, needs_copy, full_msg) in build_llm_links(it["url"], prompt):
            if needs_copy:
                # Droši ieliekam pilno promptu JS funkcijā (JSON-escapots)
                js_arg = json.dumps(full_msg)
                btns.append(
                    f'<a class="btn" href="{escape(href)}" target="_blank" rel="noopener noreferrer" '
                    f'onclick="copyPrompt({escape(js_arg)});">{escape(label)}</a>'
                )
            else:
                btns.append(
                    f'<a class="btn" href="{escape(href)}" target="_blank" rel="noopener noreferrer">{escape(label)}</a>'
                )
        buttons_html = " ".join(btns)

        parts.append(f"""
  <div class="card">
    <h3>{escape(it['title'])}</h3>
    <p class="note">{escape(it.get('note',''))}</p>
    <p class="link"><a href="{escape(it['url'])}" target="_blank" rel="noopener noreferrer">{escape(it['url'])}</a></p>
    <div class="btns">{buttons_html}</div>
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

        src_path = (root / src_rel).resolve()
        out_path = (root / out_rel).resolve()

        if not src_path.exists():
            print(f"[warn] Source not found: {src_path}")
            continue

        # Pašlaik atbalstām CSV
        if src_path.suffix.lower() != ".csv":
            print(f"[warn] Unsupported source type (only .csv supported now): {src_path.name}")
            continue

        rows = read_csv(src_path)
        rows, dropped = dedupe_rows(rows)
        if not rows:
            print(f"[warn] No rows in {src_path}")
            continue
        if dropped:
            print(f"[info] Dropped {dropped} duplicate URLs from {src_path}")

        html_str = render_html(title, subtitle, prompt, rows)
        ensure_parent_dir(out_path)
        out_path.write_text(html_str, encoding="utf-8")
        print(f"Wrote HTML -> {out_path}")

if __name__ == "__main__":
    main()
