"""Chạy đủ cổng AF2 cho một hay nhiều bài BNK và in tóm tắt gọn (không chạy build/tts/asr):
gen.py → lv.py lint → lv.py render → screen_gen.py + screen_code.py check --course BNK → lab_gate.py BNK → verify_bnk.py
Dùng: .venv/Scripts/python -B audit/bnk/af2_gate.py L01 [L02 …]"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
sys.stdout.reconfigure(encoding="utf-8")


def run(*a):
    p = subprocess.run([PY, "-B", *a], cwd=ROOT, env=ENV, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout + p.stderr


for lid in [a.upper() for a in sys.argv[1:]]:
    rc, o = run("audit/bnk/gen.py", lid)
    if rc:
        print(lid, "GEN LỖI\n", o[-1500:])
        continue
    f = next((ROOT / "lessons" / "bnk").glob(lid + "_*.yaml")).relative_to(ROOT)
    rc, o = run("tools/lv.py", "lint", str(f))
    bad = [l for l in o.splitlines() if l.startswith(("[FAIL]", "[WARN]"))]
    last = [l for l in o.splitlines() if l.startswith("lint:")]
    mins = [l.split("≈")[1].split("phút")[0].strip() + "ph" for l in o.splitlines() if "ước lượng thời lượng" in l]
    print(lid, "lint:", last[0] if last else o[-300:], "| thời lượng", mins)
    for l in bad:
        print("   ", l[:400])
    rc, o = run("tools/lv.py", "render", str(f))
    print(lid, "render:", [l for l in o.splitlines() if l.startswith("render:")][:1] or o[-300:])
    for l in o.splitlines():
        if "tràn" in l or "đè" in l or "cắt" in l or l.startswith("  ") and "khung" in l:
            print("   ", l[:300])
rc, o = run("audit/bnk/screen_gen.py")
print(o.strip().splitlines()[0])
rc, o = run("audit/review/screen_code.py", "check", "--course", "BNK")
for l in o.splitlines():
    if l.startswith(("FAIL", "STALE", "MISSING", "ORPHAN", "WARN", "screen_code:")):
        print("  ", l[:300])
rc, o = run("audit/review/lab_gate.py", "BNK")
print([l for l in o.splitlines() if "lab_gate" in l or "FAIL" in l])
rc, o = run("audit/bnk/verify_bnk.py")
print(o.strip().splitlines()[-1])
