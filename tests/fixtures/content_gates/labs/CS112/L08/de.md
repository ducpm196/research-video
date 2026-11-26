# Lab CS112 L08 — Thế ngược trên giấy, kiểm bằng chương trình

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện. Lời giải giấy bút nằm ở bước 1; chương trình chỉ để **kiểm** đáp số của bạn.

Hai hệ thức truy hồi (số liệu minh hoạ, **khác ví dụ trong bài**):
- A: `A(1) = 1`, `A(n) = 2·A(n − 1) + 3` với `n ≥ 2`.
- B: `B(1) = 1`, `B(n) = B(n − 1) + 2n − 1` với `n ≥ 2`.

1. **Trên giấy**: thế ngược mỗi hệ thức hai ba bước, nhìn quy luật sau `i` bước, dừng ở `n − i = 1` (điều kiện đầu đã cho), rồi dùng tổng `1 + 2 + … + 2^(i−1) = 2^i − 1` và tổng `1 + 3 + 5 + … + (2n − 1)` (tổng `n` số lẻ đầu tiên bằng `n²`: bài 0 đã dạy; hãy tự kiểm bằng số nhỏ) để ra công thức đóng của `A(n)` và của `B(n)`. Hãy tự làm ra nháp trước khi kiểm.
2. Viết hai hàm đệ quy `A(n)` và `B(n)` đúng như hệ thức (trường hợp `n == 1` trả `1`).
3. Tạo `the_nguoc.py` in, đúng chữ không dấu:
   - với `n` từ 1 đến 6, một dòng `n = <n>: A = <A(n)>, B = <B(n)>`;
   - `A(10) theo cong thuc dong: <số>` (tính bằng công thức đóng của bạn);
   - `B(50) theo cong thuc dong: <số>` (tính bằng công thức đóng của bạn);
   - `khop voi de quy tu n = 1 den 20: dung` nếu với **mọi** `n` từ 1 đến 20 cả `A(n)` và `B(n)` bằng công thức đóng của bạn (dùng `all(... for n in range(1, 21))`), ngược lại in `sai`.

Chạy: `python the_nguoc.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L08 the_nguoc.py`.
