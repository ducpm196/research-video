import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")

# 1. Lint the 5 touched Stage 9 files
for rel in [
    "lessons/llm/L07_sinh_van_ban.yaml",
    "lessons/rln/L03_ke_cuop_nhieu_tay.yaml",
    "lessons/rln/L13_hanh_trinh_atari.yaml",
    "lessons/cvi/L05_ransac.yaml",
    "lessons/cvi/L10_dich_chuyen_mien.yaml",
]:
    print(">>> LINT", rel, flush=True)
    r = subprocess.run([PY, "-B", "tools/lv.py", "lint", rel], cwd=ROOT)
    assert r.returncode == 0, f"lint failed: {rel}"

# 2. All Stage 9 non-browser gates
for c in ("CS115", "AIF", "IRS", "AGT", "LLM", "RLN", "CVI"):
    cmds = [
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c.lower()}.yaml"],
        [PY, "-B", "audit/review/arith_scan.py", c],
    ]
    if c == "CS115":
        cmds.append([PY, "-B", "audit/verify_cs115_tex.py"])
    else:
        cmds.append([PY, "-B", f"audit/{c.lower()}/verify_{c.lower()}.py"])
    for cmd in cmds:
        print(">>> RUN:", " ".join(cmd[2:5]), flush=True)
        r = subprocess.run(cmd, cwd=ROOT)
        assert r.returncode == 0, f"failed: {cmd}"

# 3. Sequential layout_scan on all 7 Stage 9 courses
for c in ("CS115", "AIF", "IRS", "AGT", "LLM", "RLN", "CVI"):
    print(">>> LAYOUT SCAN", c, flush=True)
    r = subprocess.run([PY, "-B", "-u", "audit/layout_scan.py", c], cwd=ROOT)
    assert r.returncode == 0, f"layout_scan failed: {c}"

print("STAGE 9 ALL 106 LESSONS GATES + LAYOUT SCAN 100% PASS!", flush=True)
