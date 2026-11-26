import sys
from pathlib import Path
import yaml

sys.path.insert(0, "tools")
import lv  # noqa: E402

txt = Path("audit/s9_11/up_s10.py").read_text(encoding="utf-8")
covs = eval(txt.split("COVERS = ")[1].split("\nDATA = ")[0])
do_v = tuple(lv.AF2_DO_VERBS)
do_k = set(lv.AF2_DO_SCENES)

bad = 0
for key, pairs in covs.items():
    c, lid = key.split(":")
    yp = next(Path("lessons", c.lower()).glob(f"{lid}_*.yaml"))
    d = yaml.safe_load(yp.read_text(encoding="utf-8"))
    sk = {s["id"]: s.get("kind", "") for s in d["scenes"]}
    objs = d["objectives"]
    for oi, sid in pairs:
        o = objs[oi - 1].strip().lower()
        k = sk.get(sid, "MISSING")
        if sid not in sk or (o.startswith(do_v) and k not in do_k):
            bad += 1
            ds = [s["id"] for s in d["scenes"] if s.get("kind") in do_k]
            print(f"E51 FAIL: {key} obj{oi} ({objs[oi-1][:45]}...) -> {sid}({k}) | do_scenes={ds}")
print(f"Checked {len(covs)} Stage 10 lessons: E51 mismatches={bad}")
