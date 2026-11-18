"""fix6 CS112 L23 (đợt 3): rút gọn thêm lời đọc về ≤ 2300 từ. Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l23c.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen  # noqa

T = tpl("L23")

# cost.1: bỏ câu cuối (số liệu n = 6 đã ở trên màn hình) và mục focus tương ứng
edit(T, ' Với n bằng 6, trung bình là 10 phẩy 3, so với 15 ở trường hợp tệ nhất."', '"')
edit(T, '        focus: [1, 1, 2, 2, 2, 3]\n        say: "Còn trung bình thì sao?', '        focus: [1, 1, 2, 2, 2]\n        say: "Còn trung bình thì sao?')

# idea.1: ba câu thay vì bốn
edit(T, "Hai ô xanh 4 và 2 là vùng số không lớn hơn chốt, kết thúc ở vị trí i. Ô đỏ 7 là vùng số lớn hơn chốt. Các ô xám",
     "Hai ô xanh 4 và 2 là vùng số không lớn hơn chốt, còn ô đỏ 7 là vùng số lớn hơn chốt. Các ô xám")
edit(T, "        focus: [1, 1, 1, 1]\n        say: \"Hình này chụp đoạn", "        focus: [1, 1, 1]\n        say: \"Hình này chụp đoạn")

edit(T, "Kết quả, chốt 5 về chỉ số 3, bên trái là 4, 2, 1 đều không lớn hơn 5, bên phải là 7, 6 đều lớn hơn 5. Đoạn 6 phần tử tốn đúng 5 phép so sánh, tức n trừ 1. Đệ quy tiếp, đoạn 4, 2, 1 với chốt 1 tốn 2 phép so sánh, rồi đoạn 2, 4 tốn 1, còn đoạn 7, 6 tốn 1.",
     "Kết quả, chốt 5 về chỉ số 3, bên trái là 4, 2, 1 đều không lớn hơn 5, bên phải là 7, 6 đều lớn hơn 5. Đoạn 6 phần tử tốn đúng 5 phép so sánh, tức n trừ 1. Đệ quy tiếp, đoạn 4, 2, 1 tốn 2 phép so sánh, đoạn 2, 4 tốn 1, và đoạn 7, 6 tốn 1.")
edit(T, "Số 3 không lớn hơn 5 nên i thành 0, còn 8 lớn hơn nên giữ nguyên.", "Số 3 không lớn hơn 5 nên i thành 0, số 8 giữ nguyên.")
edit(T, "Số phép so sánh là n trừ 1, cộng n trừ 2, cho tới 1, theo bài 0 bằng n nhân n trừ 1 chia 2, tức Theta của n bình phương.",
     "Số phép so sánh là n trừ 1, cộng n trừ 2, cho tới 1, bằng n nhân n trừ 1 chia 2, tức Theta của n bình phương.")

regen("L23")
