"""fix10 CS112 L24: tiêu đề cột ngắn để cột 2 không gập dòng (cảnh scale vừa khung). Chạy một lần."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen  # noqa

T = tpl("L24")
edit(T, "<th>nới mọi cạnh, dừng khi không đổi (tối đa $n - 1$ vòng)</th>", "<th>nới mọi cạnh (tối đa $n - 1$ vòng)</th>")
edit(T, "để thử giảm $d[v]$; đồ thị ngẫu nhiên theo công thức cố định, trọng số 1–20;", "để thử giảm $d[v]$; nới mọi cạnh thì dừng khi không còn đổi; đồ thị ngẫu nhiên theo công thức cố định, trọng số 1–20;")
regen("L24")
