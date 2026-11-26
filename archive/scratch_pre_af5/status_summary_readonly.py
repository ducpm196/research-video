import json
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

tracks = yaml.safe_load((ROOT / "curriculum/tracks.yaml").read_text("utf-8"))
course_stage = {}
for st in tracks.get("stages", []):
    sid = st.get("id") or st.get("stage")
    for c in st.get("courses", []):
        cid = c if isinstance(c, str) else c.get("id")
        if cid:
            course_stage[str(cid).upper()] = str(sid)

rows = []
for p in sorted((ROOT / "curriculum").glob("*.yaml")):
    if p.stem in ("tracks",):
        continue
    d = yaml.safe_load(p.read_text("utf-8"))
    c = str(d.get("course", p.stem)).upper()
    st = str(d.get("stage") or course_stage.get(c, "?"))
    lessons = [x["id"] for x in d.get("lessons", [])]
    fresh = dur_ok = asr_clean = 0
    for lid in lessons:
        spec_hits = sorted((ROOT / "lessons" / c.lower()).glob(f"{lid}_*.yaml"))
        sp = lv.load_spec(spec_hits[0])
        sd = lv.spec_digest(sp)
        br = ROOT / "out" / c / lid / "build_report.json"
        if br.exists():
            j = json.loads(br.read_text("utf-8"))
            if float(j.get("timeline_seconds", 0)) >= 540:
                dur_ok += 1
            if j.get("spec_sha256") == sd:
                fresh += 1
        ar = ROOT / "out" / c / lid / "asr_report.json"
        if ar.exists():
            aj = json.loads(ar.read_text("utf-8"))
            if isinstance(aj, list):
                unrev = [x for x in aj if x.get("diff") and not x.get("reviewed")]
                if not unrev:
                    asr_clean += 1
    rows.append((st, c, str(d.get("status", "?")), len(lessons), fresh, dur_ok, asr_clean))

def skey(r):
    st = r[0]
    if st.startswith("S") and st[1:].isdigit():
        return (int(st[1:]), r[1])
    return (99, r[1])

tot = [0, 0, 0, 0]
cur_st = None
for st, c, status, n, fresh, dur_ok, asr_clean in sorted(rows, key=skey):
    if st != cur_st:
        cur_st = st
        print(f"\n=== {st} ===")
    print(f"  {c:6s} status={status:7s} n={n:2d} fresh={fresh:2d} >=540s={dur_ok:2d} asr_clean={asr_clean:2d}")
    tot[0] += n; tot[1] += fresh; tot[2] += dur_ok; tot[3] += asr_clean
print(f"\nTOTAL: lessons={tot[0]} fresh={tot[1]} >=540s={tot[2]} asr_clean={tot[3]}")
