"""fix10 CS112 L28, L29 (đợt cắt lời 2). Chạy một lần."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson  # noqa

p = lesson("L28")
for o, n in [
    ("từ 5 đến 3 ra âm 1 thay vì 0.", "từ 5 đến 3 ra âm 1."),
    ("hãy đọc to đủ hai vế của lời hứa.", "hãy đọc đủ hai vế."),
    ("phải dừng đúng ở điều kiện đầu.", "phải dừng ở điều kiện đầu."),
    ("phép thử là cận dưới không được vượt chi phí một chu trình đã biết.", "cận dưới không được vượt chi phí một chu trình đã biết."),
    ("Cuối cùng là bốn cái bẫy của phần sắp xếp, đồ thị và độ khó.", "Cuối cùng là bốn bẫy về sắp xếp, đồ thị và độ khó."),
    ("Trước khi giải ví dụ, hãy nhìn cây đệ quy", "Hãy nhìn cây đệ quy"),
    ("Giờ ta xem cả khoá gom lại thế nào khi n lớn dần.", "Giờ ta xem cả khoá gom lại khi n lớn dần."),
    ("Áp dụng cho ví dụ vừa rồi, ba đường độc lập phải cho cùng một con số ở n bằng 8.", "Với ví dụ vừa rồi, ba đường độc lập phải cho cùng một số ở n bằng 8."),
    ("Sau đó là năm cái bẫy tiếp theo.", "Tiếp theo là năm bẫy nữa."),
]:
    edit(p, o, n)
p = lesson("L29")
for o, n in [
    ("tệp mô tả hiện hành của ngôn ngữ gốc kể lại rằng bản đầu", "tệp mô tả hiện hành kể lại rằng bản đầu"),
    ("Thực hành rút ra là mã lõi", "Thực hành rút ra: mã lõi"),
    ("được sửa cùng cách trong một bản sửa mã ngày 25 tháng 2 năm 2015.", "được sửa cùng cách ngày 25 tháng 2 năm 2015."),
    ("kể rằng mất một thời gian dài mới nhận ra 32 không tốt với mọi n.", "kể rằng phải lâu mới nhận ra 32 không tốt với mọi n."),
    ("Điều cần mang theo, như bài tổng ôn đã nói, mỗi kết luận cần một lập luận và một phép thử.", "Điều cần mang theo, mỗi kết luận cần một lập luận và một phép thử."),
    ("Tư duy: như bài tổng ôn đã nói, mỗi kết luận", "Tư duy: mỗi kết luận"),
]:
    edit(p, o, n)
