# Lab CS115 L07 — Ma trận Jacobian và quy tắc chuỗi

Cần: Python 3 (không cần thư viện ngoài). Tạo tệp `jac.py`. Hàm hai đầu vào, ba đầu ra (số minh hoạ, khác ví dụ trong bài): `f(x, y) = (x*y, x**2 - y, x + y**2)`, tại điểm `(2, 3)`.

1. Lập ma trận Jacobian (mỗi hàng là một đầu ra, mỗi cột là một đầu vào) bằng đạo hàm riêng viết tay. In `J = [[..], [..], [..]]`.
2. Cho `x` tăng `0.1` và `y` giảm `0.1`. Dự đoán thay đổi của ba đầu ra bằng `J` nhân bước; in `du doan: [..]`. Tính thay đổi thật `f(2.1, 2.9) - f(2, 3)`; in `thuc te: [..]`. Mỗi số làm tròn 4 chữ số thập phân bằng `round(..., 4)`.
3. Hàm ngoài `h(a, b, c) = a**2 + b*c`. Jacobian ngoài (một hàng) tại `(a, b, c) = f(2, 3) = (6, 1, 11)` là `[2*a, c, b]`; in `Jacobian ngoai: [..]`. Nhân hàng này với `J` (ngoài trước, trong sau) để được gradient của hàm lồng `h(f(x, y))`; in `gradient hop (J ngoai nhan J): [..]`.
4. Kiểm bằng bước nhỏ: với `H(x, y) = h(*f(x, y))`, `e = 0.00001`, độ dốc theo `x` là `(H(x + e, y) - H(x - e, y)) / (2 * e)`, theo `y` tương tự, làm tròn 2 chữ số thập phân; in `gradient truc tiep (buoc nho): [..]`.

Danh sách in đúng như `print` của Python (dấu phẩy và một khoảng trắng).

Chạy: `python jac.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L07 jac.py`.
