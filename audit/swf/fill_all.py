"""Sinh lại hình (figs.py) rồi điền mọi tệp mẫu của SWF thành bài trong lessons/swf/ (fill_tpl.py, mỗi {{TÊN}} = một hình một dòng).
Chạy: .venv/Scripts/python audit/swf/fill_all.py — sửa mẫu hoặc hình thì chạy lại, không sửa tay tệp bài sinh ra."""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1])); import _frozen  # noqa: E402,F401
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
F = "audit/swf/fig/"
JOBS = {
    "L07_bat_bien_cau_truc": {"BST": "bst_bad"},
}
subprocess.run([PY, "audit/swf/figs.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
for stem, figs in JOBS.items():
    args = [f"{k}={F}{v}.svg" for k, v in figs.items()]
    subprocess.run([PY, "audit/cs112/fill_tpl.py", f"audit/swf/src/{stem}.tpl.yaml", f"lessons/swf/{stem}.yaml", *args], cwd=ROOT, check=True)
