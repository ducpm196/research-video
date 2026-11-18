# Lab CS115 L10 — Adagrad và RMSprop trên thung lũng dẹt

Cần: Python 3 (chỉ `import math`). Tạo tệp `thichnghi.py`. Hàm `f(x, y) = x**2 + 16 * y**2` (số minh hoạ, khác ví dụ trong bài), gradient `(2*x, 32*y)`, xuất phát `(x, y) = (1.0, 1.0)`. Mỗi bộ tối ưu chạy đúng 3 bước.

1. SGD thường: `w = w - eta * g` cho từng toạ độ, `eta = 0.03`.
2. Adagrad: mỗi toạ độ có một tổng `G` (bắt đầu 0). Mỗi bước: `G = G + g**2`, `w = w - eta * g / (math.sqrt(G) + 1e-8)`, `eta = 0.1`.
3. RMSprop: mỗi toạ độ có một trung bình trượt `s` (bắt đầu 0). Mỗi bước: `s = 0.9 * s + 0.1 * g**2`, `w = w - eta * g / (math.sqrt(s) + 1e-8)`, `eta = 0.1`.

Mỗi bộ in một dòng dạng `SGD: x=<x> y=<y> f=<f>` (tên, `x`, `y` và `f(x, y)` sau 3 bước, mỗi số làm tròn 4 chữ số thập phân bằng `round(..., 4)`), với tên là `SGD`, `Adagrad`, `RMSprop`. Cuối cùng in dòng `buoc dau Adagrad moi toa do: <số>` (độ dài bước đầu của một toạ độ, làm tròn 4 chữ số).

Danh sách in đúng như `print` của Python.

Chạy: `python thichnghi.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L10 thichnghi.py`.
