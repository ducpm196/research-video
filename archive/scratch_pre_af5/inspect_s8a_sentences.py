import glob, re, sys, yaml
sys.path.insert(0, "tools")
import lv

for c in ("dan", "dsc", "mlo"):
    for p in sorted(glob.glob(f"lessons/{c}/L*.yaml")):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        r = lv.lint(d, quiet=True)
        if r.errors or r.warnings:
            print(f"=== {p} ===")
            for e in r.errors + r.warnings:
                print(" ", e)
            for sc in d["scenes"]:
                for idx, st in enumerate(sc["steps"]):
                    say = str(st.get("say") or "")
                    for s in re.split(r"(?<=[.!?])\s+", say.strip()):
                        if len(s) > 155 or len(s.split()) > 35:
                            print(f"  [{sc['id']}.{idx}] ({len(s)}c/{len(s.split())}w): {s}")
