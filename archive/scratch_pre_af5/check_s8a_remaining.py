import glob, re, sys, yaml
sys.path.insert(0, "tools")
import lv

print("=== BATCH 8A WORD COUNTS < 1670 ===")
for c in ("dan", "dsc", "mlo"):
    for f in sorted(glob.glob(f"lessons/{c}/L*.yaml")):
        d = yaml.safe_load(open(f, encoding="utf-8"))
        w = sum(len(str(st.get("say") or "").split()) for sc in d["scenes"] for st in sc["steps"])
        r = lv.lint(d, quiet=True)
        if w < 1670 or r.errors or r.warnings:
            print(f"{c.upper()} {d['id']}: w={w} need={max(0, 1675-w)} E={r.errors} W={r.warnings}", flush=True)
print("DONE S8A SCAN", flush=True)
