import random, pathlib, json
root = pathlib.Path(r"D:/research-video/lessons")
courses = sorted(p for p in root.iterdir() if p.is_dir())


def pick(seed, exclude):
    r = random.Random(seed)
    out = {}
    for c in courses:
        ls = sorted(c.glob("L*.yaml"))
        ls2 = [p for p in ls if (c.name, p.name) not in exclude]
        out[c.name] = r.choice(ls2)
    return out


C = pick(20261109, set())
D = pick(20261110, {(k, v.name) for k, v in C.items()})
ex = {(k, v.name) for k, v in C.items()} | {(k, v.name) for k, v in D.items()}
E = pick(20261111, ex)
for n, s in (("C", C), ("D", D), ("E", E)):
    print(n + ":", " ".join(f"{k.upper()} {v.name[:3]}" for k, v in s.items()))
json.dump({k: str(v) for k, v in E.items()}, open(pathlib.Path(__file__).parent / "sample_e.json", "w"), indent=1)
