#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, base64, csv, html, json, sys
from pathlib import Path
from urllib.parse import quote_plus, urlparse
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    raise SystemExit("Missing dependency pyyaml. Install: pip install pyyaml")

# 5 LLM pogas: 4x prefill (?q=) + 1x clipboard (NotebookLM)
LLMS = [
    ("Perplexity", "https://www.perplexity.ai/search?q={Q}", False),
    ("You.com",    "https://you.com/search?q={Q}",           False),
    ("Kagi",       "https://kagi.com/search?q={Q}",          False),
    ("Phind",      "https://www.phind.com/search?q={Q}",     False),
    ("Claude",     "https://www.claude.ai/new?q={Q}",         False)
]

def esc(s): return html.escape(s or "", quote=True)

def normalize_url(u: str) -> str:
    u = (u or "").strip()
    if not u:
        return u
    if u.startswith("<") and u.endswith(">"):
        u = u[1:-1].strip()
    p = urlparse(u)
    if not p.scheme:
        u = "https://" + u
    return u

def read_csv(path: Path):
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        # gaidām title,url,note
        for r in rdr:
            url = normalize_url((r.get("url") or "").strip())
            if not url:
                continue
            title = (r.get("title") or "").strip() or url
            note  = (r.get("note")  or "").strip()
            rows.append({"title": title, "url": url, "note": note})
    if not rows:
        print(f"[warn] No rows in {path}", file=sys.stderr)
    else:
        print(f"[info] CSV rows: {len(rows)} from {path}")
    return rows

def render_html(title: str, subtitle: str, prompt: str, items):
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    prompt_show = esc(prompt).replace("{", "&#123;").replace("}", "&#125;")

    head = """<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>{TITLE}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
function toast(msg){
  const n=document.createElement('div');
  n.textContent=msg;
  Object.assign(n.style,{position:'fixed',bottom:'16px',right:'16px',
    background:'#111',color:'#fff',padding:'8px 12px',borderRadius:'8px',zIndex:9999,opacity:0.95});
  document.body.appendChild(n);setTimeout(()=>n.remove(),1800);
}
function b64decode(b64){
  try { return decodeURIComponent(escape(atob(b64))); }
  catch(e){ try { return atob(b64); } catch(_){ return ''; } }
}
document.addEventListener('click',function(e){
  const a=e.target.closest('a[data-llm="1"]'); if(!a) return;
  e.preventDefault();
  const href=a.getAttribute('href');
  const b64=a.getAttribute('data-prompt-b64')||'';
  const txt=b64decode(b64);
  const win=window.open(href,'_blank','noopener'); // tieši uz mērķi, bez about:blank
  if(!navigator.clipboard || window.isSecureContext===false){
    setTimeout(()=>alert('Paste (Ctrl+V):\\n\\n'+txt),50); return;
  }
  navigator.clipboard.writeText(txt)
    .then(()=>toast('Prompt copied. Paste (Ctrl+V).'))
    .catch(()=>setTimeout(()=>alert('Paste (Ctrl+V):\\n\\n'+txt),50));
}, true);
</script>
<style>
  body{{font-family:system-ui,Arial,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;}}
  h1{{margin:0 0 .25rem 0;font-size:1.5rem;}}
  .muted{{color:#6b7280;}}
  .grid{{display:grid;grid-template-columns:1fr;gap:1rem;}}
  @media(min-width:760px){{.grid{{grid-template-columns:1fr 1fr;}}}}
  .card{{border:1px solid #e5e7eb;border-radius:12px;padding:1rem;}}
  .btn{{display:inline-block;padding:.4rem .6rem;border:1px solid #d1d5db;border-radius:.5rem;text-decoration:none;}}
  .btn:hover{{background:#f5f5f5;}}
  footer{{margin-top:2rem;font-size:.9rem;color:#6b7280;}}
</style>
<h1>{TITLE}</h1>
<p class="muted">{SUBTITLE}</p>
<div class="grid">"""
    head = head.replace("{TITLE}", esc(title)).replace("{SUBTITLE}", esc(subtitle))

    parts = [head]
    for it in items:
        url = normalize_url(it["url"])
        full_prompt = (prompt.replace("{URL}", url) if "{URL}" in prompt else f"{prompt} {url}").strip()
        q = quote_plus(full_prompt)
        btns = []
        for label, base, needs_copy in LLMS:
            if "{Q}" in base:
                href = base.replace("{Q}", q)
                btns.append(f'<a class="btn" href="{esc(href)}" rel="noopener noreferrer">{esc(label)}</a>')
            else:
                b64 = base64.b64encode(full_prompt.encode("utf-8")).decode("ascii")
                btns.append(f'<a class="btn" href="{esc(base)}" rel="noopener noreferrer" data-llm="1" data-prompt-b64="{esc(b64)}">{esc(label)}</a>')
        parts.append(f"""
  <div class="card">
    <h3>{esc(it['title'])}</h3>
    <p class="muted">{esc(it.get('note',''))}</p>
    <p><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(url)}</a></p>
    <div>{" ".join(btns)}</div>
  </div>""")

    parts.append(f"""</div>
<footer>
  <p><strong>Prompt:</strong> <code>{prompt_show}</code></p>
  <p>Updated {updated}</p>
</footer>
</html>""")
    return "".join(parts)

def render_md(title: str, subtitle: str, prompt: str, items):
    lines = [f"# {title}", "", f"_{subtitle}_", "", f"**Prompt:** {prompt}", ""]
    for it in items:
        lines += [f"- **{it['title']}** — {it.get('note','')}".rstrip(),
                  f"  - {it['url']}", ""]
    return "\n".join(lines)

def ensure_parent(p: Path): p.parent.mkdir(parents=True, exist_ok=True)

def handle_lists(cfg, root: Path):
    lists = cfg.get("lists") or []
    for b in lists:
        src = (root / b["src"]).resolve()
        if not src.exists():
            print(f"[warn] Source not found: {src}", file=sys.stderr); continue
        rows = read_csv(src)
        if not rows: continue
        title = b.get("title","Untitled")
        subtitle = b.get("subtitle","")
        prompt = b.get("prompt","For ({URL}): summarize.")
        html_s = render_html(title, subtitle, prompt, rows)
        out_html = (root / b["out_html"]).resolve()
        ensure_parent(out_html)
        out_html.write_text(html_s, encoding="utf-8")
        print(f"Wrote HTML -> {out_html}")
        out_md = b.get("out_md")
        if out_md:
            md_s = render_md(title, subtitle, prompt, rows)
            out_md_p = (root / out_md).resolve()
            ensure_parent(out_md_p)
            out_md_p.write_text(md_s, encoding="utf-8")
            print(f"Wrote MD   -> {out_md_p}")

def handle_projects(cfg, root: Path):
    projs = cfg.get("projects") or []
    for p in projs:
        el = p.get("elements", {}) or {}
        if (el.get("type") or "csv").lower() != "csv":
            print(f"[skip] project {p.get('name','?')}: only CSV elements supported for now")
            continue
        src = (root / el["src"]).resolve()
        if not src.exists():
            print(f"[warn] Source not found: {src}", file=sys.stderr); continue
        rows = read_csv(src)
        if not rows: continue
        pr = p.get("prompts", {}) or {}
        mode = (pr.get("mode") or "single").lower()
        if mode != "single":
            print(f"[warn] project {p.get('name','?')}: only prompts.mode=single supported in this build; using 'single'")
        prompt = pr.get("single") or "For ({URL}): summarize."
        title = p.get("title","Untitled")
        subtitle = p.get("subtitle","")
        html_s = render_html(title, subtitle, prompt, rows)
        out = p.get("output", {}) or {}
        out_html = out.get("html")
        out_md   = out.get("md")
        if out_html:
            out_html_p = (root / out_html).resolve()
            ensure_parent(out_html_p)
            out_html_p.write_text(html_s, encoding="utf-8")
            print(f"Wrote HTML -> {out_html_p}")
        if out_md:
            md_s = render_md(title, subtitle, prompt, rows)
            out_md_p = (root / out_md).resolve()
            ensure_parent(out_md_p)
            out_md_p.write_text(md_s, encoding="utf-8")
            print(f"Wrote MD   -> {out_md_p}")
def render_md(title: str, subtitle: str, prompt: str, items):
    lines = [f"# {title}", "", f"_{subtitle}_", "", f"**Prompt:** {prompt}", ""]
    for it in items:
        lines += [f"- **{it['title']}** — {it.get('note','')}".rstrip(),
                  f"  - {it['url']}", ""]
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to alex_config.yaml")
    ap.add_argument("--root", default=".", help="Project root (paths are relative to this)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    cfg_path = (root / args.config).resolve()
    if not cfg_path.exists():
        raise SystemExit(f"Config file not found: {cfg_path}")

    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    had = False
    if cfg.get("lists"):
        handle_lists(cfg, root); had = True
    if cfg.get("projects"):
        handle_projects(cfg, root); had = True
    if not had:
        raise SystemExit("alex_config.yaml must contain 'lists:' or 'projects:'")

if __name__ == "__main__":
    main()
