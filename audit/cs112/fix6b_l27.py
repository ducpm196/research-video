"""fix6 CS112 L27: định nghĩa tại chỗ ms, KB, 'thông dịch', 'bậc tăng' (chữ trên màn hình) + chân trang chấm bài.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l27.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson, patch_cham  # noqa

P = lesson("L27")
edit(P, "Số đo của một máy, chạy bằng ngôn ngữ thông dịch; con số tuyệt đối sẽ khác ở máy khác, bậc tăng và thứ hạng thì ổn định.",
     "Số đo của một máy, chạy bằng ngôn ngữ thông dịch (đọc và chạy mã từng dòng một); ms là mili giây, một phần nghìn giây. Con số tuyệt đối sẽ khác ở máy khác, còn bậc tăng (cách thời gian lớn lên theo $n$, như $n^3$) và thứ hạng thì ổn định.")
edit(P, "424 KB do tính cả bộ nhớ giao diện; đo riêng còn 12,7 KB", "424 KB (nghìn byte) do tính cả bộ nhớ giao diện; đo riêng còn 12,7 KB")
patch_cham(P)
