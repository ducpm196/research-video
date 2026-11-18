"""fix6 CS112 L24 (đợt 2): sửa ô bảng (LaTeX ngoài <code>) và cắt thêm lời để ≤ 2300 từ.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l24b.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen  # noqa

T = tpl("L24")
edit(T, "<td><code>while còn đỉnh chưa chốt có d &lt; ∞:</code></td>", r'''<td><code>while</code> còn đỉnh chưa chốt có d &lt; $\infty$:</td>''')
edit(T, "Nếu có chu trình tổng âm, như A tới B dài 1, B quay về A dài âm 3, tổng là âm 2, thì cứ đi thêm",
     "Nếu có chu trình tổng âm, như A tới B dài 1 và B về A dài âm 3, thì cứ đi thêm")
edit(T, "Hàng trên tính d của u cộng trọng số cho cả bảy cạnh, được 4, 1, 3, 4, 6, 7, 9. Hàng dưới là d của đỉnh cuối, và ở cả bảy cột, số dưới không lớn hơn số trên.",
     "Hàng trên là d của u cộng trọng số cho bảy cạnh: 4, 1, 3, 4, 6, 7, 9. Hàng dưới là d của đỉnh cuối, và ở cả bảy cột số dưới không lớn hơn số trên.")
edit(T, "Giờ thử một đồ thị có cạnh âm, cạnh từ B tới A dài âm 2, chẳng hạn một khoản được hoàn tiền. Thuật toán",
     "Giờ thử một đồ thị có cạnh âm, cạnh từ B tới A dài âm 2. Thuật toán")
edit(T, "Mỗi đỉnh nhớ cạnh cuối cùng đã làm nó giảm, các cạnh xanh đó", "Mỗi đỉnh nhớ cạnh cuối đã làm nó giảm, các cạnh xanh đó")
edit(T, "Ở bài 6, đống nhị phân là một cây luôn giữ", "Ở bài 6, đống nhị phân là cây luôn giữ")
edit(T, "và luôn phải chứng minh vì sao đúng.", "và phải chứng minh vì sao đúng.")
regen("L24")
