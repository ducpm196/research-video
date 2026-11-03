"""Sinh lại hình (fsm_svg.py) rồi điền mọi tệp mẫu của TOC thành bài trong lessons/toc/ (fill_tpl.py, mỗi {{TÊN}} = một hình một dòng).
Chạy: .venv/Scripts/python audit/toc/fill_all.py — sửa mẫu hoặc hình thì chạy lại, không sửa tay tệp bài sinh ra."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
F = "audit/toc/fig/"
JOBS = {
    "L01_dfa": {"DFA3": "dfa3"},
    "L02_nfa_tap_con": {"NFA01": "nfa01", "DFA01": "dfa01"},
    "L05_toi_thieu_hoa": {"DFA01": "dfa01"},
    "L06_van_pham_phi_ngu_canh": {"TREE0011": "tree0011"},
    "L07_mo_ho_phan_tich": {"TREE_MUL_TOP": "tree_mul_top", "TREE_ADD_TOP": "tree_add_top"},
    "L09_may_turing": {"TM0": "tm_inc_0", "TM1": "tm_inc_1", "TM2": "tm_inc_2", "TMEND": "tm_inc_end"},
}
subprocess.run([PY, "audit/toc/fsm_svg.py"], cwd=ROOT, check=True)
for stem, figs in JOBS.items():
    args = [f"{k}={F}{v}.svg" for k, v in figs.items()]
    subprocess.run([PY, "audit/cs112/fill_tpl.py", f"audit/toc/src/{stem}.tpl.yaml", f"lessons/toc/{stem}.yaml", *args], cwd=ROOT, check=True)
