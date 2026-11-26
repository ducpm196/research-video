import glob, re, yaml

for c in ("evt", "den", "cld", "clc", "sar"):
    for p in sorted(glob.glob(f"lessons/{c}/L*.yaml")):
        txt = open(p, encoding="utf-8").read()
        for i, l in enumerate(txt.splitlines(), 1):
            if re.search(r"\bvs\b", l, re.I) or "->" in l and "show:" not in l and "-->" not in l and "→" not in l:
                if "http" not in l and "# " not in l[:4]:
                    print(f"[VS/ARROW] {p}:{i}: {l.strip()[:140]}")
        d = yaml.safe_load(txt)
        rec = next((sc for sc in d["scenes"] if sc["id"] == "recap"), None)
        if rec and len(rec["steps"]) > 1:
            r1 = rec["steps"][1]
            print(f"[REC1] {c.upper()} {d['id']} w_show={len(str(r1.get('show') or ''))} focus={r1.get('focus')}\n  SHOW: {str(r1.get('show') or '').strip()}\n  SAY: {str(r1.get('say') or '').strip()}")
