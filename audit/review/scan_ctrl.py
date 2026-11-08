"""Quét mọi lessons/*/*.yaml: ký tự điều khiển trong show/say/title (dấu \\ của LaTeX bị YAML nháy kép hiểu thành escape:
\\t → TAB, \\b → BS, \\f → FF, \\v → VT, \\r → CR, \\a → BEL, \\n → xuống dòng trước 'eq|abla|u|ot|e |ewline|leq…')."""
import glob, re, sys, yaml
sys.stdout.reconfigure(encoding="utf-8")
CTRL = re.compile(r"[\x07\x08\x09\x0b\x0c\x0d]")
NL_TEX = re.compile(r"\n(eq|abla|u\b|ot\b|ewline|leq|geq|eg\b|i\b|otin|subseteq|ormalsize)")
hits = 0
for f in sorted(glob.glob("lessons/*/L*_*.yaml")):
    s = yaml.safe_load(open(f, encoding="utf-8"))
    def walk(x, path):
        global hits
        if isinstance(x, str):
            for m in CTRL.finditer(x):
                hits += 1
                print(f"{f} {path} ctrl={hex(ord(m.group(0)))} …{x[max(0, m.start()-15):m.start()+15]!r}")
            if path.endswith("show"):
                for m in NL_TEX.finditer(x):
                    if "$" in x[max(0, m.start()-80):m.start()] or "\\" in x[max(0, m.start()-80):m.start()]:
                        hits += 1
                        print(f"{f} {path} NEWLINE-TEX …{x[max(0, m.start()-20):m.start()+12]!r}")
        elif isinstance(x, dict):
            for k, v in x.items():
                walk(v, f"{path}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f"{path}[{i}]")
    walk(s, "")
print("hits:", hits)
