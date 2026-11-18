# Lab CS115 L06 — Gradient: công thức và bước nhỏ

Cần: Python 3 (không cần thư viện ngoài). Tạo tệp `grad.py`. Hàm (số minh hoạ, khác ví dụ trong bài): `f(x, y) = 3*x**2 + x*y - 2*y**2`, tại điểm `(2, 1)`.

1. Đạo hàm riêng theo `x` giữ `y` đứng yên là `6*x + y`, theo `y` giữ `x` đứng yên là `x - 4*y`. In `gradient bang cong thuc: [<theo x>, <theo y>]` (số nguyên).
2. Kiểm bằng bước nhỏ: với `h = 0.0001`, độ dốc theo `x` là `(f(x + h, y) - f(x - h, y)) / (2 * h)`, theo `y` tương tự. In `gradient bang buoc nho: [<a>, <b>]` với mỗi số làm tròn 4 chữ số thập phân bằng `round(..., 4)`.
3. In `do dai gradient: <số>` (căn bậc hai của tổng bình phương hai thành phần, làm tròn 4 chữ số thập phân).
4. Đi NGƯỢC gradient một bước `0.01`: điểm mới là `(x - 0.01 * gx, y - 0.01 * gy)`. In `f(2,1) = <f tại điểm đầu>; sau buoc nguoc gradient 0.01: <f tại điểm mới, làm tròn 4 chữ số>`, rồi dòng `f giam: True` nếu f ở điểm mới nhỏ hơn.

Chạy: `python grad.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L06 grad.py`.
