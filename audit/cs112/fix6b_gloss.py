"""fix6 CS112 (đợt 2): định nghĩa tại chỗ các thuật ngữ còn lại: L16 đống, L22 đỉnh kề, L23 ngăn xếp (chữ trên màn hình), L24 tiêu đề cảnh,
L26 tổng tập con, L29 JDK. Chạy: .venv/Scripts/python -B audit/cs112/fix6b_gloss.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson, tpl, regen  # noqa

# L16: đống
P = lesson("L16")
edit(P, "Dựng đống (hàng đợi ưu tiên, bài 6) rồi lấy từng món", "Dựng <b>đống</b> (cấu trúc luôn lấy ra nhanh phần tử ưu tiên nhất, bài 6) rồi lấy từng món")
edit(P, "Khi đó ta dựng đống, tức hàng đợi ưu tiên của bài 6, rồi lấy từng món", "Khi đó ta dựng đống, tức cấu trúc luôn lấy ra nhanh phần tử ưu tiên nhất ở bài 6, rồi lấy từng món")

# L22: đỉnh kề (chỉ chữ trên màn hình; câu lời đọc nằm trong asr_reviewed)
P = lesson("L22")
edit(P, "mỗi bước sang một <b>đỉnh kề</b> có $z$ <b>tốt hơn</b>", "mỗi bước sang một <b>đỉnh kề</b> (nối với đỉnh hiện tại bằng một cạnh của miền) có $z$ <b>tốt hơn</b>")

# L23 (mẫu): ngăn xếp
T = tpl("L23")
edit(T, "báo lỗi tràn ngăn xếp từ $n = 2\,000$", "báo lỗi tràn <b>ngăn xếp</b> (nơi máy nhớ các lời gọi đang chạy dở) từ $n = 2\,000$")
regen("L23")

# L24 (mẫu): tiêu đề cảnh không dùng thuật ngữ chưa giảng
T = tpl("L24")
edit(T, 'title: "Tự kiểm: mọi cạnh phải thoả bất đẳng thức tam giác"', 'title: "Tự kiểm: không cạnh nào còn nới được"')
regen("L24")

# L26 (mẫu): tổng tập con
T = tpl("L26")
edit(T, "chu trình qua mọi đỉnh, tổng tập con.</td>", "chu trình qua mọi đỉnh, tổng tập con (chọn một số trong dãy để tổng bằng số cho trước).</td>")
regen("L26")

# L29: JDK
P = lesson("L29")
edit(P, "<p><b>Quy mô:</b> JDK 7 phát hành ngày 28/7/2011.", "<p><b>Quy mô:</b> JDK 7 (bộ phát triển Java, bản 7) phát hành ngày 28/7/2011.")
