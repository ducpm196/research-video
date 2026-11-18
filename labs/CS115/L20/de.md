# Lab CS115 L20 — Sigmoid, BCE, gradient ŷ − y và softmax không tràn số

Cần: Python 3 (chỉ `import math`). Tạo tệp `logistic.py` (số minh hoạ, khác ví dụ trong bài). Làm tròn mọi số thực 4 chữ số thập phân bằng `round(..., 4)`.

1. Hàm sigmoid `sigma(z) = 1 / (1 + math.exp(-z))`. In `sigmoid(0) = <số>`, `sigmoid(2) = <số>`, `sigmoid(-2) = <số>`.
2. Với `yhat = sigma(2)`: sai số BCE là `-(y * ln(yhat) + (1 - y) * ln(1 - yhat))`. In `BCE nhan 1, du doan 0.8808: <số>` (với `y = 1`) và `BCE nhan 0, du doan 0.8808: <số>` (với `y = 0`).
3. Gradient theo điểm số `z` bằng `yhat - y`. In `gradient yhat - y: nhan 1: <số>, nhan 0: <số>`.
4. Softmax `exp(z_i) / tong exp(z_j)`. In `softmax [2, 1, 0]: [..]` (danh sách bốn chữ số, in bằng `print` của Python).
5. Điểm lớn làm `math.exp` tràn số (`math.exp(1000)` báo lỗi). Cách chữa: trừ điểm lớn nhất khỏi mọi điểm trước khi lấy `exp` (kết quả softmax không đổi). In `softmax [1000, 1001] on dinh: [..]`.

Chạy: `python logistic.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L20 logistic.py`.
