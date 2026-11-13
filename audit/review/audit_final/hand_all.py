"""Với mỗi khoá: asr_flags → asr_hand_gen → asr_hand_insert → asr_review_dms → lv.py asr (chỉ bài có mục mới). In tóm tắt."""
import re, subprocess, sys, os
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("D:/research-video")
PY = str(ROOT / ".venv/Scripts/python.exe")
S = Path(sys.argv[1])
env = dict(os.environ, PYTHONIOENCODING="utf-8")


def run(args, **kw):
    return subprocess.run([PY, "-B"] + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env, **kw)


for C in sys.argv[2:]:
    _r = run(["audit/review/asr_flags.py", C])
    fl = _r.stdout + chr(10) + _r.stderr
    m = re.search(rf"{C}: (\d+) câu chưa xem xét", fl)
    n = int(m.group(1)) if m else -1
    shorts = [l for l in fl.splitlines() if "NGẮN" in l or "THIẾU" in l]
    print(f"== {C}: chưa xem xét {n}; ngắn/thiếu {len(shorts)}")
    for l in shorts:
        print("   ", l[:150])
    if n <= 0:
        continue
    label = f"{C} AF2 rà ASR (2026-11-13)"
    out = S / f"hand_{C}.txt"
    g = run(["audit/review/asr_hand_gen.py", C, label, str(out)])
    ins = run(["audit/review/asr_hand_insert.py", str(out), label])
    print("   insert:", ins.stdout.strip()[-40:], ins.stderr.strip()[-200:])
    lessons = sorted({l.split("\t")[0] for l in fl.splitlines() if re.match(r"^L\d\d\t", l)})
    ap = run(["audit/dms/asr_review_dms.py", "--course", C] + lessons)
    changed = [x.split()[0] for x in ap.stdout.splitlines() if "mục →" in x]
    print("   áp dụng:", len(changed), "bài;", ap.stderr.strip()[-200:])
    for l in changed:
        f = next((ROOT / "lessons" / C.lower()).glob(l + "_*.yaml"))
        r = run(["tools/lv.py", "asr", str(f)])
        print("    ", l, [x for x in r.stdout.splitlines() if x.startswith("asr:")][:1])
