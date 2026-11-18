# Lab CS115 L09 — Gradient Descent: tốc độ học và chi phí mỗi bước

Cần: Python 3 (không cần thư viện ngoài). Tạo tệp `gd.py`. Hàm `f(w) = 3 * (w - 2)**2` (số minh hoạ, khác ví dụ trong bài); đạo hàm `6 * (w - 2)`; xuất phát `w = 10.0` (số thực, để in ra `10.0`).

1. Chạy Gradient Descent `w_mới = w - eta * đạo hàm` với `eta = 0.1`, ghi lại `w` từ bước 0 đến bước 4. In `eta=0.1: [..]` (mỗi số làm tròn 4 chữ số thập phân bằng `round(..., 4)`).
2. Làm lại với `eta = 0.4`, ghi `w` từ bước 0 đến bước 3, in `eta=0.4: [..]`. Rồi in `phan ky: True` nếu khoảng cách tới đáy (`abs(w - 2)`) ở bước 3 lớn hơn ở bước 0.
3. Chi phí mỗi bước: `N = 1000000` mẫu, `D = 100` trọng số, một lô nhỏ `B = 100` mẫu. Một bước Gradient Descent cả lô tốn `N * D` phép nhân, một bước SGD tốn `B * D`. In `GD 1 buoc: <N*D> phep; SGD 1 buoc: <B*D> phep; buoc SGD moi epoch: <N // B>`.

Danh sách in đúng như `print` của Python (dấu phẩy và một khoảng trắng).

Chạy: `python gd.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L09 gd.py`.
