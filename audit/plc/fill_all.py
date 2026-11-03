"""Sinh lại hình (figs.py) rồi điền mọi tệp mẫu của PLC thành bài trong lessons/plc/ (fill_tpl.py, mỗi {{TÊN}} = một hình một dòng).
Chạy: .venv/Scripts/python audit/plc/fill_all.py — sửa mẫu hoặc hình thì chạy lại, không sửa tay tệp bài sinh ra."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
F = "audit/plc/fig/"
JOBS = {
    "L02_dequy_xuong": {"TREE": "tree_123"},
    "L03_cay_cu_phap": {"LR": "tree_left_right"},
    "L08_bo_nho": {"HEAP": "heap"},
    "L11_toi_uu": {"FOLD": "tree_fold"},
}
subprocess.run([PY, "audit/plc/figs.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
for stem, figs in JOBS.items():
    args = [f"{k}={F}{v}.svg" for k, v in figs.items()]
    subprocess.run([PY, "audit/cs112/fill_tpl.py", f"audit/plc/src/{stem}.tpl.yaml", f"lessons/plc/{stem}.yaml", *args], cwd=ROOT, check=True)
