"""Sinh lại hình (figs.py) rồi điền mọi tệp mẫu của ESY thành bài trong lessons/esy/ (fill_tpl.py, mỗi {{TÊN}} = một hình một dòng).
Chạy: .venv/Scripts/python audit/esy/fill_all.py — sửa mẫu hoặc hình thì chạy lại, không sửa tay tệp bài sinh ra."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
F = "audit/esy/fig/"
JOBS = {
    "L02_ngat_chong_doi": {"DEBOUNCE": "debounce"},
    "L03_dinh_thoi_pwm": {"PWM": "pwm"},
    "L04_adc": {"ADC": "adc"},
    "L05_loc_so": {"EMA": "ema"},
    "L09_lap_lich_rm": {"GANTT": "rm_rta"},
    "L10_edf_dao_uu_tien": {"RM": "rm_miss", "EDF": "edf_ok"},
    "L13_nang_luong": {"SLEEP": "sleep"},
}
subprocess.run([PY, "audit/esy/figs.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
for stem, figs in JOBS.items():
    args = [f"{k}={F}{v}.svg" for k, v in figs.items()]
    subprocess.run([PY, "audit/cs112/fill_tpl.py", f"audit/esy/src/{stem}.tpl.yaml", f"lessons/esy/{stem}.yaml", *args], cwd=ROOT, check=True)
