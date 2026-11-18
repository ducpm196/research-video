# Lab CS115 L19 — Phạt L2 làm ma trận khả nghịch; phạt L1; chia dữ liệu K phần

Cần: Python 3 (không cần thư viện ngoài), `from fractions import Fraction`. Tạo tệp `chinhquy.py` (số minh hoạ, khác ví dụ trong bài).

1. Hai đặc trưng trùng nhau: `X = [[1, 1], [2, 2], [3, 3]]`, `y = [2, 4, 6]`. Tính `A = X^T X` (ma trận 2 × 2) và `b = X^T y`. In `dinh thuc X^T X: <định thức>` (sẽ là 0: không nghịch đảo được).
2. Thêm phạt L2 với `lambda = 1`: `A + lambda * I`. In `dinh thuc X^T X + 1*I: <số>`. Giải `(A + lambda*I) w = b` bằng nghịch đảo hai nhân hai và `Fraction`; in `w (lambda=1): [..]`. Làm lại với `lambda = 1/10` và in `w (lambda=1/10): [..]`.
3. Phạt L1 một hệ số: nghiệm của "làm nhỏ `(w - a)**2 + lambda * |w|`" là `0` nếu `|a| <= lambda / 2`, ngược lại là `a - lambda / 2` (nếu `a > 0`) hoặc `a + lambda / 2` (nếu `a < 0`). Với `lambda = 2` và `a` lần lượt `3, 1/2, -2`, in một dòng `L1 lambda=2: a=3 -> <w>, a=1/2 -> <w>, a=-2 -> <w>`.
4. Kiểm định chéo 4 phần cho 12 mẫu: mỗi lượt để riêng một phần cùng cỡ để kiểm định. In `kiem dinh cheo 4 phan, 12 mau: moi luot huan luyen <số>, kiem dinh <số>`.

Số `Fraction` in bằng `str`, danh sách ghép bằng dấu phẩy và một khoảng trắng.

Chạy: `python chinhquy.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L19 chinhquy.py`.
