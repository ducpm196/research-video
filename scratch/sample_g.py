import hashlib
import json
import pathlib
import random
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(r"D:/research-video")

txt_c = (ROOT / "audit/review/sample_c/REPORT.md").read_text("utf-8")
ex = set(re.findall(r"^\|\s*([A-Z0-9]+)\s+(L\d+)\s*\|", txt_c, re.M))
line38 = next(ln for ln in txt_c.splitlines() if ln.startswith("25 bài còn lại"))
ex.update(re.findall(r"\b([A-Z0-9]+)\s+(L\d+)\b", line38))
ex.update(re.findall(r"\b([A-Z0-9]+)\s+(L\d+)\b", (ROOT / "audit/review/sample_d/REPORT.md").read_text("utf-8")))
for p in sorted((ROOT / "audit/review/sample_e").glob("part_*.md")):
    ex.update(re.findall(r"^\|\s*([A-Z0-9]+)\s+(L\d+)\s*\|", p.read_text("utf-8"), re.M))
for x in json.loads((ROOT / "audit/review/sample_f/sample_f.json").read_text("utf-8")):
    ex.add((x["course"], x["lesson"]))

cs = sorted(d.name.upper() for d in (ROOT / "lessons").iterdir() if d.is_dir())
r = random.Random(20261201)
out = []
for c in cs:
    cands = [p for p in sorted((ROOT / "lessons" / c.lower()).glob("L*.yaml")) if (c, p.name[:3]) not in ex]
    p = r.choice(cands)
    h = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    out.append({"course": c, "lesson": p.name[:3], "path": str(p).replace("\\", "/"), "sha16": h})

(ROOT / "scratch/sample_g.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(f"Excluded: {len(ex)} | Sample G: {len(out)}")
for row in out:
    print(row["course"], row["lesson"], row["sha16"], row["path"])
