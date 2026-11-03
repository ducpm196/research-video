"""Sinh lại hình (figs.py) rồi điền mọi tệp mẫu của DSY thành bài trong lessons/dsy/ (fill_tpl.py, mỗi {{TÊN}} = một hình một dòng).
Chạy: .venv/Scripts/python audit/dsy/fill_all.py — sửa mẫu hoặc hình thì chạy lại, không sửa tay tệp bài sinh ra."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
F = "audit/dsy/fig/"
JOBS = {
    "L01_dong_ho_lamport": {"LAMPORT": "lamport"},
    "L02_dong_ho_vector": {"VECTOR": "vector"},
    "L06_bam_nhat_quan": {"RING": "ring"},
    "L09_xu_ly_luong": {"WIN": "windows"},
}
subprocess.run([PY, "audit/dsy/figs.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
for stem, figs in JOBS.items():
    args = [f"{k}={F}{v}.svg" for k, v in figs.items()]
    subprocess.run([PY, "audit/cs112/fill_tpl.py", f"audit/dsy/src/{stem}.tpl.yaml", f"lessons/dsy/{stem}.yaml", *args], cwd=ROOT, check=True)
