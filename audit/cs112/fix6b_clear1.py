"""fix6 CS112 L15–L22: thêm `clear: true` sau mỗi step bảng đọc mã mới chèn (tránh TRÀN bảng khi render). Chạy: .venv/Scripts/python -B audit/cs112/fix6b_clear1.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import clear_next, lesson, tpl, regen  # noqa

clear_next(lesson("L15"), "ví dụ hai số một và hai cho hai bộ")
clear_next(lesson("L16"), "Dòng thoát cho vòng lặp dừng ngay, không xét món còn lại.")
clear_next(lesson("L16"), "ví dụ chọn hai từ ba số cho ba cặp.")
T = tpl("L17")
clear_next(T, "Dòng chọn thêm sự kiện vào kết quả rồi đặt lại giờ kết thúc vừa chọn.")
clear_next(T, "ví dụ chọn hai từ ba số cho ba cặp.")
regen("L17")
T = tpl("L18")
clear_next(T, "Vòng lặp cho i chạy từ 2 tới n, mỗi ô bằng tổng hai ô liền trước.")
clear_next(T, "còn một dấu bằng là gán.")
regen("L18")
clear_next(lesson("L19"), "ví dụ ba số đầu là 10, 30, 5 cho 1500.")
T = tpl("L21")
clear_next(T, "và các phép tính giữa chúng vẫn ra phân số.")
clear_next(T, "Lấy tử số chia cho định thức ra số x của giao điểm, ví dụ chín phần hai.")
regen("L21")
P = lesson("L22")
clear_next(P, "nên phép xoay không mất độ chính xác.")
clear_next(P, "thực chất cộng ba lần hàng ra.")
