# Lab CS112 L09 — Hàm sinh trên giấy, kiểm hệ số bằng chương trình

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện. Phần giải trên giấy ở bước 1; chương trình chỉ để **kiểm**.

Hệ thức mới (số liệu minh hoạ, **khác ví dụ trong bài**): `T(1) = 1`, `T(n) = 4·T(n − 1) + 1` với `n ≥ 2`.

1. **Trên giấy**, làm đúng các bước của bài: gọi `G(x) = T(1)x + T(2)x² + …`; nhân hệ thức với `x^n` rồi cộng mọi `n ≥ 2`; đổi chỉ số; giải ra `G(x)` (mẫu số sẽ là `(1 − x)(1 − 4x)`); tách thành tổng hai phân thức đơn giản; đọc hệ số của `x^n` để được công thức đóng của `T(n)`.
2. **Kiểm bằng cách nhân với mẫu số**: `(1 − x)(1 − 4x) = 1 − 5x + 4x²`, nên `G(x) · (1 − 5x + 4x²) = x`. So sánh hệ số của `x^n` ở hai vế được `c[n] − 5·c[n−1] + 4·c[n−2] = 1` khi `n = 1`, và `= 0` khi `n ≥ 2` (với `c[n]` là hệ số của `x^n` trong `G`, và `c[0] = c[-1] = 0`). Dùng một từ điển `c = {-1: 0, 0: 0}` rồi tính `c[n]` cho `n` từ 1 đến 10 bằng công thức đó.
3. Viết hàm đệ quy `T(n)` đúng hệ thức (`T(1) = 1`).
4. Tạo `ham_sinh.py` in, đúng chữ không dấu:
   - dòng cố định: `mau so: (1 - x)(1 - 4x) = 1 - 5x + 4x^2`;
   - `he so 1..6 tu G: <c[1] … c[6] cách nhau một dấu cách>`;
   - `he so 1..6 tu T: <T(1) … T(6)>`;
   - `cong thuc dong voi n = 10: <số>` (công thức đóng bạn tìm được, tính ở `n = 10`);
   - `khop tu n = 1 den 10: dung` nếu với mọi `n` từ 1 đến 10 cả ba giá trị `c[n]`, `T(n)`, công thức đóng của bạn bằng nhau, ngược lại `sai` (dùng `all(...)`).

Chạy: `python ham_sinh.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L09 ham_sinh.py`.
