# Lab CS112 L12 — Tra định lý thợ trên giấy, kiểm bằng tỉ số

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Ba hệ thức (số liệu minh hoạ, **khác ví dụ trong bài**), cả ba có `T(1) = 1` và `n` là lũy thừa của `b`:
- (a) `T(n) = 4·T(n/2) + n²` — kiểm ở `n = 1024`;
- (b) `T(n) = 9·T(n/3) + n` — kiểm ở `n = 3^9 = 19683`;
- (c) `T(n) = T(n/2) + n` — kiểm ở `n = 1024`.

1. **Trên giấy**, với mỗi hệ thức: tính `n^(log_b a)`, so với `f(n)`, chọn trường hợp (TH1, TH2 hay TH3; với TH3 kiểm điều kiện đều đặn `a·f(n/b) ≤ c·f(n)` với `c < 1`), rồi ghi đáp án bậc (`n²`, `n² log₂ n`, `n`...).
2. Viết hàm đệ quy `T(n, a, b, f)` (`T(1) = 1`; `f` là hàm truyền vào, ví dụ `lambda n: n * n`; `n // b` là phép chia lấy phần nguyên). Cần `import math` (`math.log2`).
3. Tạo `dinh_ly_tho.py` in ba dòng, đúng chữ không dấu, mỗi dòng có dạng `<hệ thức>: <TH>, T(<n>)/(<đáp án>) = <tỉ số>`. `<hệ thức>` viết `4T(n/2)+n^2`, `9T(n/3)+n`, `T(n/2)+n` (không dấu cách); `<TH>` là `TH1`, `TH2` hoặc `TH3` bạn đã chọn; `<đáp án>` là đáp án bậc bạn tìm được, viết dạng `n^a` hoặc `n^a log2 n` (với `a` nguyên; khi `a = 1` chỉ viết `n`); `<tỉ số>` là `T(n)` chia cho giá trị của đáp án tại `n` (với `log2` là `math.log2`), in bằng `f"{x:.3f}"` (ba chữ số thập phân). Tỉ số gần một hằng số nghĩa là đáp án đúng bậc.

Chạy: `python dinh_ly_tho.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L12 dinh_ly_tho.py`.
