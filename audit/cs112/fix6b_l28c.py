"""fix6 CS112 L28 (đợt 3). Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l28c.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson  # noqa

P = lesson("L28")
edit(P, "T của 8 bằng 2 nhân 8 cộng 8, bằng 24, khớp 8 nhân 3, đúng 8 nhân lôgarit cơ số 2 của 8.", "T của 8 bằng 2 nhân 8 cộng 8, bằng 24, khớp 8 nhân 3.")
