import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")

SCRIPTS = [
    ("DEN", "audit/den/af2/upgrade_den.py"),
    ("CLD", "audit/cld/af2/upgrade_cld.py"),
    ("CLC", "audit/clc/af2/upgrade_clc.py"),
    ("SAR", "audit/sar/af2/upgrade_sar.py"),
]

for course, script in SCRIPTS:
    print(f">>> UPGRADE {course}: {script}", flush=True)
    p = subprocess.run([PY, "-B", "-u", script], cwd=ROOT)
    if p.returncode != 0:
        sys.exit(p.returncode)

for course in ("EVT", "DEN", "CLD", "CLC", "SAR"):
    for cmd in [
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", course],
        [PY, "-B", "audit/review/lab_gate.py", course],
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{course.lower()}.yaml"],
        [PY, "-B", f"audit/{course.lower()}/verify_{course.lower()}.py"],
    ]:
        print(f">>> RUN: {' '.join(cmd)}", flush=True)
        p = subprocess.run(cmd, cwd=ROOT)
        if p.returncode != 0:
            sys.exit(p.returncode)

print("BATCH 8B UPGRADERS + INITIAL GATES DONE!", flush=True)
