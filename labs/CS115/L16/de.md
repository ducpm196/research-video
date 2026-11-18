# Lab CS115 L16 — PCA bằng tay cho năm điểm trong mặt phẳng

Cần: Python 3 (không cần thư viện ngoài), `from fractions import Fraction`. Tạo tệp `pca.py`. Năm điểm `(4, 2), (3, 5), (5, 5), (5, 7), (8, 6)` (số minh hoạ, khác ví dụ trong bài). Chia cho `N = 5`.

1. Trung bình hai toạ độ, in `trung binh: <mx> <my>`; trừ trung bình để có năm vector lệch.
2. Ma trận hiệp phương sai `S` (trung bình của `d nhân d chuyển vị`): in `ma tran hiep phuong sai: [[a, b], [b, a]]` (số `Fraction`, ví dụ `14/5`).
3. Hai số trên đường chéo của `S` bằng nhau (`a`) nên trị riêng là `a + b` (vector riêng `[1, 1]`) và `a - b` (vector riêng `[1, -1]`). In `tri rieng: <lớn> va <nhỏ>` và `vector rieng thu nhat: [1, 1]`.
4. Tỉ lệ phương sai giữ lại khi chỉ giữ một thành phần: trị riêng lớn chia tổng hai trị riêng. In `ti le phuong sai giu lai (1 thanh phan): <phân số>`.
5. Hệ số của mỗi vector lệch trên hướng thứ nhất `u = [1, 1]` là `(d nhân u) / (u nhân u)` (như phép chiếu ở bài 1). In `he so tren huong 1: [..]`.
6. Khôi phục mỗi điểm từ một thành phần: `trung bình + hệ số nhân u`. In `tong binh phuong sai khi khoi phuc: <số>` = tổng bình phương khoảng cách giữa điểm thật và điểm khôi phục (phải bằng `N` nhân trị riêng nhỏ).

Chạy: `python pca.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L16 pca.py`.
