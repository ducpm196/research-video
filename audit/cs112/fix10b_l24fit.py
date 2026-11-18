"""fix10 CS112 L24: thu gọn cảnh scale cho vừa khung sau khi thêm "(tối đa n − 1 vòng)" vào tiêu đề cột. Chạy một lần."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen  # noqa

T = tpl("L24")
edit(T, "để thử giảm $d[v]$; đồ thị ngẫu nhiên sinh bằng công thức cố định, trọng số 1 đến 20;", "để thử giảm $d[v]$; đồ thị ngẫu nhiên theo công thức cố định, trọng số 1–20;")
edit(T, "<td>ngẫu nhiên, 1 000 đỉnh, 5 000 cạnh</td>", "<td>ngẫu nhiên: $n = 1\,000$, $m = 5\,000$</td>")
edit(T, "<td>ngẫu nhiên, 10 000 đỉnh, 50 000 cạnh</td>", "<td>ngẫu nhiên: $n = 10\,000$, $m = 50\,000$</td>")
edit(T, "<tr><td>chuỗi 1 000 đỉnh</td>", "<tr><td>chuỗi: $n = 1\,000$</td>")
edit(T, "<tr><td>chuỗi 100 000 đỉnh</td>", "<tr><td>chuỗi: $n = 100\,000$</td>")
regen("L24")
