"""fix10 (tiếp): clear sau bước bit của L26, rồi sinh lại các bài mẫu. Chạy: .venv/Scripts/python -B audit/cs112/fix10b_items2.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import tpl, regen, clear_next  # noqa
clear_next(tpl("L26"), "Một số W cần khoảng lôgarit cơ số 2 của W bit")
for lid in ("L17", "L18", "L23", "L24", "L25", "L26"):
    regen(lid)
