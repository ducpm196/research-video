import subprocess
import sys
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "audit" / "s9_11"))
import common  # noqa: E402

sol = (ROOT / "labs" / "hci" / "L10" / "loi_giai.py").read_text(encoding="utf-8")
common.sync_practice_run_blocks("HCI", "L10", sol)

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for fp in (
    "lessons/hci/L09_truy_cap.yaml",
    "lessons/hci/L10_chong_loi.yaml",
    "lessons/hci/L12_hanh_trinh_wcag.yaml",
):
    r = subprocess.run([PY, "-B", "tools/lv.py", "lint", fp], cwd=ROOT)
    assert r.returncode == 0, f"lint failed: {fp}"

for cmd in (
    [PY, "-B", "audit/review/sync_tpl_from_lesson.py", "HCI", "--write"],
    [PY, "-B", "audit/review/screen_code.py", "check", "--course", "HCI"],
    [PY, "-B", "audit/review/lab_gate.py", "HCI"],
    [PY, "-B", "audit/layout_scan.py", "HCI"],
):
    print(">>> RUN:", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT)
    assert r.returncode == 0, f"FAILED: {cmd}"
print("HCI FINAL CLEANUP & LAYOUT PASSED!", flush=True)
