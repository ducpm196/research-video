# Lab CS115 L18 — Phương trình chuẩn cho bốn điểm

Cần: Python 3 (không cần thư viện ngoài), `from fractions import Fraction`. Tạo tệp `hoiquy.py`. Bốn điểm `x = [0, 1, 2, 3]`, `y = [1, 2, 4, 5]` (số minh hoạ, khác ví dụ trong bài). Mô hình `y_hat = w0 + w1 * x`; ma trận `X` có cột số 1 và cột `x`.

1. Dựng `X` (4 hàng, 2 cột). Tính `X^T X` và `X^T y`. In `X^T X: [[..], [..]]` và `X^T y: [..]`.
2. In `dinh thuc: <định thức của X^T X>` (nghịch đảo hai nhân hai: đổi chỗ, đổi dấu, chia định thức).
3. Giải phương trình chuẩn `X^T X w = X^T y` bằng nghịch đảo hai nhân hai, dùng `Fraction`. In `w: [w0, w1]`.
4. Dự đoán `X nhân w`, in `du doan: [..]`; sai số trung bình bình phương (MSE, chia `n = 4`), in `MSE: <số>`.
5. Kiểm gradient: `X^T (X w - y)` phải bằng vector không. In `X^T (Xw - y): [0, 0]` (mỗi thành phần in bằng `int`).

Số `Fraction` in bằng `str` (ví dụ `9/10`), danh sách đúng như `print`/ghép của Python (dấu phẩy và một khoảng trắng).

Chạy: `python hoiquy.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L18 hoiquy.py`.
