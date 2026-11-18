"""fix6 CS112 L23 (đợt 4): cắt nốt vài từ về ≤ 2300. Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l23d.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen  # noqa

T = tpl("L23")
edit(T, "Sau mỗi lần phân hoạch, tự kiểm ba điều, vì sai một chỉ số là cả mảng hỏng.", "Sau mỗi lần phân hoạch, tự kiểm ba điều.")
edit(T, "Mỗi ô từ 0 đến 4 so với chốt đúng một lần, nên tốn 5 phép so sánh.", "Năm ô đầu so với chốt đúng một lần, nên tốn 5 phép so sánh.")
regen("L23")
