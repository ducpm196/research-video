import glob, yaml

for c in ["evt", "den", "cld", "clc", "sar"]:
    for p in sorted(glob.glob(f"lessons/{c}/L*.yaml")):
        txt = open(p, encoding="utf-8").read()
        for i, line in enumerate(txt.splitlines(), 1):
            if "càng " in line:
                print(f"{p}:{i}: {line.strip()[:160]}")
