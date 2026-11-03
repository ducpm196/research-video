"""Sinh lại hình (figs.py) rồi điền mọi tệp mẫu của CLD thành bài trong lessons/cld/ (fill_tpl.py, mỗi {{TÊN}} = một hình một dòng).
Chạy: .venv/Scripts/python audit/cld/fill_all.py — sửa mẫu hoặc hình thì chạy lại, không sửa tay tệp bài sinh ra."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
F = "audit/cld/fig/"
JOBS = {
    "L06_xep_lich_pod": {"BP": "binpack"},
    "L09_can_bang_tai": {"LB": "lb_loads"},
    "L10_hang_doi": {"LC": "latency_curve"},
}
subprocess.run([PY, "audit/cld/figs.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
for stem, figs in JOBS.items():
    if not (ROOT / f"audit/cld/src/{stem}.tpl.yaml").exists():
        continue
    args = [f"{k}={F}{v}.svg" for k, v in figs.items()]
    subprocess.run([PY, "audit/cs112/fill_tpl.py", f"audit/cld/src/{stem}.tpl.yaml", f"lessons/cld/{stem}.yaml", *args], cwd=ROOT, check=True)
