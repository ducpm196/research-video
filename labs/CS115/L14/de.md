# Lab CS115 L14 — Phân phối chuẩn: chuẩn hoá z, diện tích bằng tổng các cột hẹp

Cần: Python 3 (chỉ `import math`). Tạo tệp `chuan.py`. Chiều cao một nhóm người tuân theo phân phối chuẩn với tâm `mu = 50` và phương sai `64` (số minh hoạ, khác ví dụ trong bài).

1. In `sigma: <độ lệch chuẩn>` (căn của phương sai), `z(58): <z>`, `z(34): <z>` với `z = (x - mu) / sigma`; in bằng `print` của Python (ví dụ `1.0`).
2. Xác suất `P(42 < X < 58)` tương ứng `z` từ `-1` đến `1`. Mật độ chuẩn tắc `phi(z) = exp(-z*z/2) / sqrt(2*pi)`. Chia đoạn `[-1, 1]` thành `k` cột bằng nhau, chiều cao mỗi cột lấy tại GIỮA cột, tổng diện tích các cột. In `xap xi 10 cot: <số>` và `xap xi 100 cot: <số>`, làm tròn 4 chữ số thập phân.
3. Giá trị chính xác `math.erf(1 / math.sqrt(2))`, in `chinh xac: <số>` (4 chữ số).
4. Quy tắc hai xích ma: `P(|X - mu| < 2*sigma) = math.erf(2 / math.sqrt(2))`, in `2 sigma: <số>` (4 chữ số).
5. Mật độ có thể lớn hơn 1: với `sigma = 0.1`, mật độ tại tâm là `1 / (sigma * sqrt(2*pi))`. In `mat do tai tam (sigma=0.1): <số>` (4 chữ số) rồi dòng `lon hon 1: True`.

Chạy: `python chuan.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L14 chuan.py`.
