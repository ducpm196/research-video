"""fix6 CS112 L29: định nghĩa tại chỗ cờ + lát cắt (gợi ý Tự làm), bỏ ký hiệu O(n) trên màn hình, cắt vài từ để bù chân trang.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l29.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson, patch_cham  # noqa

P = lesson("L29")

edit(P, "chép O(n) phần tử chỉ để đặt 64 phần tử", "chép cỡ n phần tử chỉ để đặt 64 phần tử")
edit(P, "nên viết một hàm gộp có cờ. Phép <code>s[n:n + 2] = [s[n] + s[n + 1]]</code> gộp hai phần tử liền kề. Lời giải ở",
     "nên viết một hàm gộp có <b>cờ</b> (một đối số đúng/sai để bật hay tắt điều kiện thêm). Phép <code>s[n:n + 2] = [s[n] + s[n + 1]]</code> gộp hai phần tử liền kề: <code>s[n:n + 2]</code> là <b>lát cắt</b>, hai phần tử ở vị trí n và n + 1; gán vào đó một danh sách một phần tử thì hai phần tử bị thay bằng một. Ví dụ s = [30, 20, 10], n = 1 thì s thành [30, 30]. Lời giải ở")

# cắt lời để bù (không đụng câu nằm trong asr_reviewed)
edit(P, "và trộn hai dãy 4 phần tử cần nhiều nhất 7 phép so sánh.", "hai dãy 4 phần tử cần nhiều nhất 7 phép so sánh.")
edit(P, "trong dãy 31 phần tử với nhiều nhất 5 phép so sánh.", "trong dãy 31 phần tử, nhiều nhất 5 phép so sánh.")
edit(P, "Bước một, mảng 8 phần tử gồm hai đoạn 4 và 4 có điểm giữa", "Bước một, hai đoạn 4 và 4 có điểm giữa")
edit(P, "Bước hai, với ba đoạn 2, 2, 4, chỗ nối đầu có điểm giữa", "Bước hai, ba đoạn 2, 2, 4 có chỗ nối đầu với điểm giữa")
edit(P, "Cách xử lý của nhóm tác giả là sửa gốc, xét bất biến", "Nhóm tác giả sửa gốc, xét bất biến")
edit(P, "điểm nghẽn còn lại là quy tắc chọn độ dài tối thiểu cũ tránh được ca tệ nhất, nhưng", "điểm nghẽn còn lại là quy tắc chọn độ dài tối thiểu cũ tránh ca tệ nhất, nhưng")

patch_cham(P)
