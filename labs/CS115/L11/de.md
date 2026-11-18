# Lab CS115 L11 — Một bước Newton so với Gradient Descent

Cần: Python 3 (không cần thư viện ngoài), `from fractions import Fraction`. Tạo tệp `newton.py`. Hàm bậc hai `f(w) = 1/2 * w^T A w - b^T w` (số minh hoạ, khác ví dụ trong bài) với `A = [[4, 1], [1, 3]]`, `b = [1, 2]`. Gradient là `A nhân w trừ b`, Hessian là `A` ở mọi điểm. Xuất phát `w = [0, 0]`.

1. Kiểm hàm lồi: Hessian có `a = 4 > 0` và định thức `4*3 - 1*1 = 11 > 0`. In `ham loi: True`.
2. Một bước Newton: `w_mới = w - (nghịch đảo A) nhân (gradient)`. Giải hệ `A nhân p = gradient` bằng nghịch đảo 2 × 2 với `Fraction`. In `Newton 1 buoc: w = [x, y]` (mỗi số là phân số `a/b`).
3. In `gradient sau Newton: [<gx>, <gy>]` (gradient tại điểm mới; số nguyên).
4. Gradient Descent `w_mới = w - 0.2 * gradient`, đúng 3 bước. In `GD eta=0.2 sau 3 buoc: [x, y]` và `gradient sau GD: [gx, gy]` (mỗi số làm tròn 4 chữ số thập phân bằng `round(..., 4)`).

Danh sách in đúng như `print` của Python.

Chạy: `python newton.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L11 newton.py`.
