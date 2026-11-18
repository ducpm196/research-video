# Lab CS115 L15 — Hiệp phương sai, ma trận Σ và khoảng cách theo độ trải

Cần: Python 3 (không cần thư viện ngoài), `from fractions import Fraction`. Tạo tệp `hiep.py`. Bốn học sinh, điểm Toán `x = [1, 2, 4, 5]` và điểm Lý `y = [2, 1, 5, 4]` (số minh hoạ, khác ví dụ trong bài). Chia cho `n = 4` (không chia `n - 1`).

1. In `trung binh: <mean x> <mean y>` và `phuong sai: <var x> <var y>` (phương sai = trung bình bình phương độ lệch). Mọi số dùng `Fraction` rồi in bằng `print` của Python, ví dụ `5/2`.
2. Hiệp phương sai = trung bình tích hai độ lệch. In `hiep phuong sai: <số>`. Vì hai phương sai bằng nhau nên hệ số tương quan bằng hiệp phương sai chia phương sai: in `tuong quan: <số>`.
3. Ma trận hiệp phương sai `[[var x, cov], [cov, var y]]`: in `ma tran: [[..], [..]]` và `dinh thuc: <số>`.
4. Hai điểm mới có độ lệch so với trung bình là `d = (2, 2)` (điểm `(5, 5)`) và `d = (2, -2)` (điểm `(5, 1)`). Khoảng cách theo độ trải bình phương là `d` chuyển vị nhân nghịch đảo của ma trận nhân `d` (nghịch đảo 2 × 2: đổi chỗ, đổi dấu, chia định thức). In `khoang cach theo do trai^2 cua (5, 5): <số>` và `khoang cach theo do trai^2 cua (5, 1): <số>`, rồi `khoang cach thang^2 cua ca hai: <bình phương độ dài của d>`.

Chạy: `python hiep.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L15 hiep.py`.
