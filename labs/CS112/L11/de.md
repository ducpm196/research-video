# Lab CS112 L11 — Đổi biến trên giấy, kiểm công thức bằng chương trình

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Hệ thức mới (số liệu minh hoạ, **khác ví dụ trong bài**), với `n` là `4, 16, 256, 65536, …` (luôn lấy căn được số nguyên): `W(2) = 6`, `W(n) = √n · W(√n) + 3n`.

1. **Trên giấy**, làm đúng các bước của bài: đặt `n = 2^m`, `S(m) = W(2^m)`; chia hai vế cho `2^m`; đặt `U(m) = S(m) / 2^m` để ra một hệ thức theo `U(m/2)`; thế ngược; đổi ngược để ra công thức đóng của `W(n)` theo `log₂ log₂ n`. Điều kiện đầu: `W(2) = 6`.
2. Tạo `doi_bien.py` (`import math` đầu tệp; `math.isqrt(n)` là căn bậc hai nguyên của `n`, `math.log2(x)` là lôgarit cơ số 2):
   - `W(n)` đệ quy đúng hệ thức (`W(2)` trả `6`);
   - `cong_thuc(n)`: công thức đóng của bạn; gợi ý `m = int(math.log2(n))`, `k = int(math.log2(m))` (với `n = 2^(2^k)`).
3. In đúng chữ không dấu, theo thứ tự:
   - với `n` trong `(4, 16, 256, 65536)`: `n = <n>: he thuc <W(n)>, cong thuc <cong_thuc(n)>`;
   - `n = 2^32: he thuc <W(2 ** 32)> - cong thuc <cong_thuc(2 ** 32)>`;
   - `khop: dung` nếu mọi cặp trên (kể cả `2 ** 32`) bằng nhau, ngược lại `khop: sai`.

Chạy: `python doi_bien.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L11 doi_bien.py`.
