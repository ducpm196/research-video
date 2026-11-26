import glob, re, sys, yaml
sys.path.insert(0, "tools")
import lv

bad = 0
for c in ("cs115", "aif", "irs", "agt", "llm", "rln", "cvi"):
    for f in sorted(glob.glob(f"lessons/{c}/L*.yaml")):
        if c == "cs115":
            m = re.search(r"L(\d+)_", f)
            if not m or int(m.group(1)) < 22:
                continue
        spec = yaml.safe_load(open(f, encoding="utf-8"))
        r = lv.lint(spec, quiet=True)
        if r.errors or r.warnings:
            bad += 1
            print(f, "E:", r.errors, "W:", r.warnings, flush=True)
print("TOTAL S9 FILES WITH LINT E/W:", bad, flush=True)
