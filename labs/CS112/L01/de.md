# Lab CS112 L01 — Tìm hằng số c và ngưỡng n₀ bằng máy

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `nguong.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó.

Hàm mới (số liệu minh hoạ, **khác ví dụ trong bài**): `f(n) = 2n² + 10n + 30`. Trong Python viết `2 * n * n + 10 * n + 30` (dấu `*` là phép nhân).

1. Viết hàm `f(n)` như trên.
2. Viết hàm `nguong(c)`: trả về số `n0` **nhỏ nhất** sao cho `f(n) <= c * n * n` đúng với **mọi** `n` từ `n0` đến `2000`; trả về `None` nếu ngay `n = 2000` bất đẳng thức đã sai. Gợi ý: cho `n` chạy **lùi** từ 2000 về 1 (`for n in range(2000, 0, -1):`), nhớ `n` cuối cùng còn đúng, dừng (`break`) ở `n` đầu tiên sai.
3. Với mỗi `c` trong `(2, 3, 4, 5)` in một dòng, đúng chữ không dấu: `c = <c>: n0 = <số>`, hoặc `c = <c>: khong co n0` khi hàm trả `None`.
4. In dòng cuối: `ty so f(n)/n^2 voi n = 100000: <số>`, số là `f(100000) / 100000 ** 2` làm tròn đến 4 chữ số thập phân bằng `round(x, 4)` (`**` là phép lũy thừa).

Chạy: `python nguong.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L01 nguong.py`.
