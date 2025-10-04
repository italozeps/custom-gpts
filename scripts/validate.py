import os, sys, csv, yaml

errors = []

# 0) Palīglīdzeklis
def err(msg): 
    errors.append(msg)

# 1) Saknes gpts.csv obligāts
if not os.path.exists("gpts.csv"):
    err("Missing gpts.csv in repo root")
else:
    # savācam slugus no reģistra
    slugs = []
    with open("gpts.csv", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        if rdr.fieldnames != ['slug','name','purpose','status','owner','last_edit','openai_link','dataset_link','notes']:
            err("gpts.csv: header must be exactly: slug,name,purpose,status,owner,last_edit,openai_link,dataset_link,notes")
        for r in rdr:
            s = (r.get("slug") or "").strip()
            if s: slugs.append(s)

    if not slugs:
        err("gpts.csv has no rows")

# 2) gpts/<slug> struktūra
if not os.path.isdir("gpts"):
    err("Missing directory 'gpts'")
else:
    for s in slugs:
        base = os.path.join("gpts", s)
        if not os.path.isdir(base):
            err(f"Missing folder: gpts/{s}")
            continue
        cfg = os.path.join(base, "config.yaml")
        prm = os.path.join(base, "prompt.md")
        if not os.path.exists(cfg): err(f"Missing: gpts/{s}/config.yaml")
        if not os.path.exists(prm): err(f"Missing: gpts/{s}/prompt.md")
        # pārbaudām, ka config.yaml slug sakrīt ar mapes nosaukumu
        if os.path.exists(cfg):
            try:
                with open(cfg, encoding="utf-8") as f:
                    y = yaml.safe_load(f) or {}
                yslug = (y.get("slug") or "").strip()
                if yslug and yslug != s:
                    err(f"config.yaml slug='{yslug}' does not match folder '{s}'")
            except Exception as e:
                err(f"YAML error in gpts/{s}/config.yaml: {e}")

if errors:
    print("Validation FAILED:\n" + "\n".join("- " + e for e in errors))
    sys.exit(1)
else:
    print("Validation OK")
