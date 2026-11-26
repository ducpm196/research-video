"""Lint 6 layout-fixed lessons, sync_tpl, screen_code, and re-run layout_scan asserting 0 errors."""
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")

FILES = [
    ("AIF", "lessons/aif/L13_tong_hop.yaml"),
    ("IRS", "lessons/irs/L02_tf_idf.yaml"),
    ("MLO", "lessons/mlo/L03_kiem_thu_he_ml.yaml"),
    ("DEN", "lessons/den/L12_kho_du_lieu.yaml"),
    ("CLC", "lessons/clc/L07_csdl_duoc_quan_ly.yaml"),
    ("SAR", "lessons/sar/L13_hanh_trinh_twitter.yaml"),
]

for c, rel in FILES:
    print(">>> LINT", rel, flush=True)
    r = subprocess.run([PY, "-B", "tools/lv.py", "lint", rel], cwd=ROOT)
    assert r.returncode == 0, f"lint failed: {rel}"

for c, _ in FILES:
    for cmd in [
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "-u", "audit/layout_scan.py", c],
    ]:
        print(">>> RUN", c, Path(cmd[-2] if cmd[-1] == c else cmd[-2]).name, flush=True)
        r = subprocess.run(cmd, cwd=ROOT)
        assert r.returncode == 0, f"failed {c}: {cmd}"
    tsv = ROOT / f"audit/layout_{c}.tsv"
    assert tsv.exists() and not tsv.read_text("utf-8").strip(), f"layout still has errors in {c}:\n{tsv.read_text('utf-8')}"

print("ALL 6 LAYOUT FIXES LINT + SYNC_TPL + SCREEN_CODE + LAYOUT_SCAN 0 ERRORS PASS!", flush=True)
