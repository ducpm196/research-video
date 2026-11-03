"""Sinh lại hình (figs.py) rồi điền mọi tệp mẫu của DSC thành bài trong lessons/dsc/ (fill_tpl.py, mỗi {{TÊN}} = một hình một dòng).
Chạy: .venv/Scripts/python audit/dsc/fill_all.py — sửa mẫu hoặc hình thì chạy lại, không sửa tay tệp bài sinh ra."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
F = "audit/dsc/fig/"
JOBS = {
    "L05_truc_quan_trung_thuc": {"TZ": "trunc_vs_zero"},
    "L06_tuong_quan": {"SC": "scatter_outlier"},
}
subprocess.run([PY, "audit/dsc/figs.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
for stem, figs in JOBS.items():
    args = [f"{k}={F}{v}.svg" for k, v in figs.items()]
    subprocess.run([PY, "audit/cs112/fill_tpl.py", f"audit/dsc/src/{stem}.tpl.yaml", f"lessons/dsc/{stem}.yaml", *args], cwd=ROOT, check=True)
