import random, pathlib, json, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8")
root = pathlib.Path(r"D:/research-video/lessons")
courses = sorted(p for p in root.iterdir() if p.is_dir())
def pick(seed, exclude, cs):
    r = random.Random(seed); out = {}
    for c in cs:
        ls = [p for p in sorted(c.glob("L*.yaml")) if (c.name, p.name) not in exclude]
        if ls: out[c.name] = r.choice(ls)
    return out
old = [c for c in courses if c.name != "bnx"]          # C/D/E were drawn before BNX existed
C = pick(20261109, set(), old)
D = pick(20261110, {(k, v.name) for k, v in C.items()}, old)
ex = {(k, v.name) for k, v in C.items()} | {(k, v.name) for k, v in D.items()}
E = pick(20261111, ex, old)
ex |= {(k, v.name) for k, v in E.items()}
LS1_FULL = {"jva", "bnk", "int", "acb", "dms", "cs112"}
for p in root.glob("cs115/L*.yaml"):
    n = int(p.name[1:3])
    if n <= 21 or n == 44: ex.add(("cs115", p.name))
pop = [c for c in courses if c.name not in LS1_FULL]
F = pick(20261112, ex, pop)
r2 = random.Random(20261113)
F2 = r2.choice([p for p in sorted((root/"bnx").glob("L*.yaml")) if p != F["bnx"]])
rows = [(k, v) for k, v in F.items()] + [("bnx", F2)]
popsize = sum(1 for c in pop for p in c.glob("L*.yaml") if (c.name, p.name) not in ex)
print("C:", " ".join(f"{k.upper()} {v.name[:3]}" for k, v in C.items()))
print("population (unsampled, outside LS1):", popsize, "| sample F:", len(rows))
out = []
for k, v in rows:
    h = hashlib.sha256(v.read_bytes()).hexdigest()[:16]
    out.append({"course": k.upper(), "lesson": v.name[:3], "path": str(v).replace("\\", "/"), "sha16": h})
    print(k.upper(), v.name, h)
json.dump(out, open(pathlib.Path(__file__).parent / "sample_f.json", "w", encoding="utf-8"), indent=1)
