# Lab CS112 L10 — Đếm lời gọi đệ quy và kiểm hệ thức bằng chương trình

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `dem_loi_goi.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó.

Số liệu minh hoạ, **khác ví dụ trong bài**. Viết ba hàm đệ quy (phép chia lấy phần nguyên viết `n // 2`):
1. `F(n)`: `F(1) = 0`; với `n ≥ 2`: `F(n) = 2·F(n // 2) + 5`. (Hai lời gọi con, mỗi lần gọi làm thêm 5 việc.)
2. `Q(n)`: `Q(1) = 1`; với `n ≥ 2`: `Q(n) = Q(n // 2) + 1`. (Một lời gọi con.)
3. `tim(A, l, r, x, dem)`: tìm kiếm nhị phân trong mảng tăng `A`; đầu hàm cộng 1 vào `dem[0]` (đếm lời gọi, `dem` là danh sách một phần tử `[0]`); nếu `l > r` trả `-1`; `m = (l + r) // 2`; `A[m] == x` thì trả `m`; `x < A[m]` thì gọi lại với `r = m - 1`, ngược lại gọi lại với `l = m + 1`.

Rồi in đúng chữ không dấu, theo thứ tự (các danh sách in bằng `" ".join(map(str, danh_sach))`):
- `F(n) cho n = 1, 2, 4, ..., 64: <F của 1, 2, 4, …, 64>` (các `n = 2 ** k`, `k` từ 0 đến 6);
- `5n - 5 cho cac n do: <5*n - 5 cho các n đó>` (tự suy ra bằng quy nạp: phần dư bằng 0);
- `Q(n) cho n = 1, 2, 4, ..., 1024: <Q của 1, 2, 4, …, 1024>` (`k` từ 0 đến 10);
- với `n` trong `(100, 5000)`: gọi `tim(list(range(n)), 0, n - 1, n, dem)` (khoá `n` **không có** trong mảng `0…n-1`, trường hợp tệ nhất) rồi in `tim nhi phan, khoa thieu, n = <n>: <số lời gọi> loi goi`;
- `khop: dung` nếu ba điều đều đúng: `F` khớp `5n - 5`; `Q(2**k)` bằng `k + 1` với mọi `k` từ 0 đến 10; số lời gọi của hai lần tìm bằng `[8, 14]`; ngược lại in `khop: sai`.

Gợi ý lý thuyết (làm trên giấy trước): `F` có hệ số 2, thế ngược ra `F(n) = 5n − 5`; `Q` có hệ số 1, ra `log₂ n + 1`; tìm nhị phân tệ nhất `⌊log₂ n⌋ + 2` lời gọi.

Chạy: `python dem_loi_goi.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L10 dem_loi_goi.py`.
