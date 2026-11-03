"""Sinh lại hình (figs.py) rồi điền mọi tệp mẫu của DBS thành bài trong lessons/dbs/ (fill_tpl.py, mỗi {{TÊN}} = một hình một dòng).
Chạy: .venv/Scripts/python audit/dbs/fill_all.py — sửa mẫu hoặc hình thì chạy lại, không sửa tay tệp bài sinh ra."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
F = "audit/dbs/fig/"
JOBS = {
    "L06_thiet_ke_er": {"ER": "er"},
    "L08_cay_b_cong": {"BPLUS": "bplus", "BPLUS45": "bplus45", "BPLUS_RNG": "bplus_rng"},
    "L12_tuan_tu_hoa": {"PREC_CYCLE": "prec_cycle", "PREC_OK": "prec_ok"},
    "L16_ngoai_quan_he": {"FRIENDS": "friends"},
}
subprocess.run([PY, "audit/dbs/figs.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
for stem, figs in JOBS.items():
    args = [f"{k}={F}{v}.svg" for k, v in figs.items()]
    subprocess.run([PY, "audit/cs112/fill_tpl.py", f"audit/dbs/src/{stem}.tpl.yaml", f"lessons/dbs/{stem}.yaml", *args], cwd=ROOT, check=True)
