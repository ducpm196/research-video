"""fix6 CS112 L24 (đợt 3): cắt vài từ. Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l24c.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen  # noqa

T = tpl("L24")
edit(T, "Chốt A vì 1 nhỏ nhất, B nhận số nhỏ hơn giữa 4 và 1 cộng 2", "Chốt A, B nhận số nhỏ hơn giữa 4 và 1 cộng 2")
regen("L24")
