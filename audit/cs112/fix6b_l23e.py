"""fix6 CS112 L23 (đợt 5): rút gọn bảng đọc mã giả cho vừa khung. Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l23e.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen  # noqa

T = tpl("L23")
edit(T, "<p>Mã giả gồm hai hàm, nhận mảng <code>a</code> và một đoạn từ vị trí <code>lo</code> tới <code>hi</code>; đọc các dòng chính trước:</p>",
     "<p>Mã giả gồm hai hàm, nhận mảng <code>a</code> và đoạn từ vị trí <code>lo</code> tới <code>hi</code>:</p>")
edit(T, "<code>a[hi]</code> là phần tử ở vị trí hi của mảng (đếm từ 0); gán nó làm chốt p; i = lo − 1 nghĩa là vùng số nhỏ lúc đầu rỗng</td><td>a = [4, 7, 2, 6, 1, 5], hi = 5: p = 5</td>",
     "<code>a[hi]</code> là phần tử ở vị trí hi (đếm từ 0), làm chốt p; i = lo − 1: vùng số nhỏ lúc đầu rỗng</td><td>a = [4, 7, 2, 6, 1, 5]: p = 5</td>")
edit(T, "<td>a[j] = 2, i thành 1: đổi a[1] = 7 với a[2] = 2</td>", "<td>a[j] = 2: i thành 1, đổi a[1] với a[2]</td>")
edit(T, "chỉ làm khi đoạn còn ít nhất hai phần tử; hàm tự gọi lại chính nó (<b>đệ quy</b>) cho đoạn trái và đoạn phải của chốt q</td><td>đoạn 6 phần tử, q = 3: gọi cho 3 phần tử bên trái, 2 bên phải</td>",
     "chỉ làm khi đoạn có ít nhất hai phần tử; hàm tự gọi lại chính nó (<b>đệ quy</b>) cho hai bên chốt q</td><td>6 phần tử, q = 3: 3 bên trái, 2 bên phải</td>")
regen("L23")
