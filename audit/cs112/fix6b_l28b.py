"""fix6 CS112 L28 (đợt 2): câu nhắc bài sau về độ dài hợp lệ; cắt thêm lời về ≤ 2300 từ. Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l28b.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson  # noqa

P = lesson("L28")
edit(P, "Ở bài sau, bài 29, bài cuối của khoá, ta đi theo dòng thời gian của một thuật toán sắp xếp thật, từ năm 2002 tới khi",
     "Ở bài sau, bài 29, bài cuối của khoá, ta đi theo dòng thời gian của một thuật toán sắp xếp thật. Hành trình đi từ năm 2002 tới khi")
edit(P, '''        focus: [1, "2.2", "2.3", "2.4"]
        say: "Mã giả của ví dụ có ba cách viết cần đọc trước. Hai dấu bằng liền nhau là phép so sánh cho đúng hoặc sai, còn lệnh trả về thoát khỏi hàm ngay.''',
     '''        focus: ["2.2", "2.3", "2.4"]
        say: "Mã giả của ví dụ dùng ba cách viết: hai dấu bằng liền nhau là phép so sánh cho đúng hoặc sai, còn lệnh trả về thoát khỏi hàm ngay.''')
edit(P, "Hàm ví dụ trên, làm n bước rồi gọi hai nửa, tốn đúng n lôgarit cơ số 2 của n bước,", "Hàm ví dụ trên tốn đúng n lôgarit cơ số 2 của n bước,")
edit(P, "Hệ thức giảm 1 thì thế ngược như bài Tháp Hà Nội, hoặc dùng hàm sinh gói cả dãy vào một biểu thức.", "Hệ thức giảm 1 thì thế ngược, hoặc dùng hàm sinh gói cả dãy vào một biểu thức.")
edit(P, "Bảng quy hoạch động lưu d của a, số đồng ít nhất để đổi a, bằng 1 cộng số nhỏ nhất trong ba ô lùi lại 1, 4 và 5.", "Ô d của a, số đồng ít nhất để đổi a, bằng 1 cộng số nhỏ nhất trong ba ô lùi lại 1, 4 và 5.")
edit(P, "Mỗi tầng tiếp theo có thêm hộp nhưng kích thước nhỏ đi, cộng lại vẫn là 8,", "Mỗi tầng tiếp theo có thêm hộp nhưng nhỏ đi, cộng lại vẫn là 8,")
edit(P, "Điều kiện đó đòi một hằng c nhỏ hơn 1, sao cho a nhân f của n chia b không vượt quá c nhân f của n.", "Điều kiện đó đòi một hằng c nhỏ hơn 1, để a nhân f của n chia b không vượt quá c nhân f của n.")
