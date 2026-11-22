import glob, re, sys, yaml
sys.path.insert(0, "tools")
import lv

for c in ("evt", "den", "cld", "clc", "sar"):
    for p in sorted(glob.glob(f"lessons/{c}/L*.yaml")):
        txt = open(p, encoding="utf-8").read()
        d = yaml.safe_load(txt)
        w = sum(len(str(st.get("say") or "").split()) for sc in d["scenes"] for st in sc["steps"])
        r = lv.lint(d, quiet=True)
        rec = [sc for sc in d["scenes"] if sc["id"] == "recap"]
        rec1 = rec[0]["steps"][1] if rec and len(rec[0]["steps"]) > 1 else {}
        has_hmqm_show = "Hai mức quy mô" in str(rec1.get("show") or "")
        has_hmqm_say = ("quy mô" in str(rec1.get("say") or "").lower() or "hai mức" in str(rec1.get("say") or "").lower())
        vs_hits = len(re.findall(r"\bvs\b", txt, re.I))
        print(f"{c.upper()} {d['id']}: w={w} hmqm_show={has_hmqm_show} hmqm_say={has_hmqm_say} focus={rec1.get('focus')} vs={vs_hits} E={r.errors} W={r.warnings}", flush=True)
