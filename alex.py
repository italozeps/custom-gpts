#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
alex.py — ģenerē statisku HTML ar 5 LLM pogām (Perplexity, Claude, Gemini, Mistral, DeepSeek)
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
from urllib.parse import quote_plus, urlparse
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    raise SystemExit("Missing dependency pyyaml. Install it with: python -m pip install pyyaml")

# ---------- LLM pogu konfigurācija ----------

LLMS = [
    ("Perplexity", "https://www.perplexity.ai/search?q={Q}", False),
    ("Claude",     "https://claude.ai/new",                  True),
    ("Gemini",     "https://gemini.google.com/app",          True),
    ("Mistral",    "https://chat.mistral.ai/chat",           True),
    ("DeepSeek",   "https://chat.deepseek.com/",             True),
]

# ---------- Palīgfunkcijas ----------

def esc(s: str) -> str:
    return html.escape(s or "", quote=True)

def normalize_url(u: str) -> str:
    """Ja URL trūkst http/https, pievieno https://; atgriež sakoptu URL."""
    u = (u or "").strip()
    if not u:
        return u
    # noņem iesp. apkārtējos <> vai pēdiņas
    if u.startswith("<") and u.endswith(">"):
        u = u[1:-1].strip()
    p = urlparse(u)
    if not p.scheme:
        u = "https://" + u
        print(f"[warn] URL without scheme, assumed https:// -> {u}")
    return u

def read_csv(path: Path):
    items = []
    with path.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            raw = (r.get("url") or "").strip()
            url = normalize_url(raw)
            if raw and not raw.lower().startswith(("http://","https://")):
                print(f"[warn] CSV URL without scheme -> {raw}  ==>  {url}")
            if not url:
                continue
            title = (r.get("title") or "").strip() or url
            note  = (r.get("note")  or "").strip()
            items.append({"title": title, "url": url, "note": note})
    print(f"[info] CSV rows: {len(items)} from {path}")
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
function toast(msg) {{
  const n = document.createElement('div');
  n.textContent = msg;
  n.style.position='fixed'; n.style.bottom='16px'; n.style.right='16px';
  n.style.background='#111'; n.style.color='#fff'; n.style.padding='8px 12px';
  n.style.borderRadius='8px'; n.style.opacity='0.95'; n.style.zIndex='9999';
  document.body.appendChild(n);
  setTimeout(() => n.remove(), 1800);
}}

// Kopē → tad atver. Ja clipboard nav pieejams, atver un parādi promptu ar alert.
function openLLM(href, txt, ev) {{
  try {{
    if (ev && ev.preventDefault) ev.preventDefault();
    if (!navigator.clipboard || window.isSecureContext === false) {{
      // file:// vai nesecure – tomēr atver čatu un parādi lietotājam promptu
      window.open(href, '_blank', 'noopener');
      setTimeout(() => {{
        try {{ window.focus(); }} catch (_e) {{}}
        alert('Paste this into the chat (Ctrl+V):\\n\\n' + txt);
      }}, 50);
      return false;
    }}
    return navigator.clipboard.writeText(txt).then(() => {{
      toast('Prompt copied. Paste in the chat (Ctrl+V).');
      setTimeout(() => window.open(href, '_blank', 'noopener'), 50);
      return false;
    }}).catch((_e) => {{
      window.open(href, '_blank', 'noopener');
      setTimeout(() => alert('Paste this into the chat (Ctrl+V):\\n\\n' + txt), 50);
      return false;
    }});
  }} catch (_e) {{
    window.open(href, '_blank', 'noopener');
    setTimeout(() => alert('Paste this into the chat (Ctrl+V):\\n\\n' + txt), 50);
    return false;
  }}
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
  code.prompt {{ white-space: pre-wrap; }}
</style>
<h1>{esc(title)}</h1>
<p class="muted">{esc(subtitle)}</p>
<div class="grid">
"""
    parts = [head]

    for r in rows:
        # DEFENSĪVA normalizācija arī renderēšanas brīdī
        url_norm = normalize_url(r["url"])
        fp = full_prompt(prompt, url_norm)
        q  = quote_plus(fp)

        btns = []
        for label, base, needs_copy in LLMS:
            if "{Q}" in base:
                href = base.replace("{Q}", q)
                btns.append(f'<a class="btn" href="{esc(href)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>')
            else:
                js_arg = json.dumps(fp)
                btns.append(
                    f'<a class="btn" href="{esc(base)}" target="_blank" rel="noopener noreferrer" '
                    f'onclick="copyPrompt({esc(js_arg)})">{esc(label)}</a>'
                )

        # “Original link” un parādītais URL – vienmēr ar normalizēto
        parts.append(f"""
  <div class="card">
    <h3>{esc(r["title"])}</h3>
    <p class="note">{esc(r["note"])}</p>
    <p class="link"><a href="{esc(url_norm)}" target="_blank" rel="noopener noreferrer">{esc(url_norm)}</a></p>
    <div class="btns">{' '.join(btns)} <a class="btn" href="{esc(url_norm)}" target="_blank" rel="noopener noreferrer">Original link</a></div>
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

    try:
        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        raise SystemExit(f"[error] YAML parse failed: {e}")

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

        print(f"[info] Writing to: {out}")
        out.parent.mkdir(parents=True, exist_ok=True)
        html_str = render_html(title, subtitle, prompt, rows)
        out.write_text(html_str, encoding="utf-8")
        print(f"Wrote HTML -> {out}")

if __name__ == "__main__":
    main()
