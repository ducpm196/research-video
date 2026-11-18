# Lab CS112 L13 — Euclid, sắp xếp chèn đếm so sánh, và kiểm trùng bằng sắp xếp trước

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `giam_de_tri.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó. Số liệu minh hoạ, **khác ví dụ trong bài**.

1. `euclid(a, b)`: lặp `while b != 0:` đổi `(a, b)` thành `(b, a % b)` và đếm `buoc` (số lần chia); trả `(a, buoc)`.
2. `chen(a)`: sắp xếp chèn trên **bản sao** `a = list(a)`; với `i` từ 1: `j = i`, rồi `while j > 0:` cộng 1 vào `dem` (một lần so sánh `a[j-1]` với `a[j]`), nếu `a[j-1] <= a[j]` thì `break`, ngược lại đổi chỗ hai phần tử và giảm `j`. Trả `(mảng đã sắp, dem)`.
3. `co_trung(a)`: sắp xếp bằng `chen`, rồi so từng cặp kề `b[i]`, `b[i+1]` với `i` từ 0 (đếm `so_sanh`), dừng và trả `(True, so_sanh)` khi gặp hai số bằng nhau, hết mảng thì trả `(False, so_sanh)`.

In đúng chữ không dấu, theo thứ tự:
- `gcd(1071, 462) = <ước> sau <số bước> buoc chia`;
- với ba mảng `("giam dan, n = 8", [8, 7, …, 1])`, `("da sap, n = 8", [0, 1, …, 7])`, `("lan xon", [7, 3, 9, 1, 5])`, mỗi mảng một dòng `chen <tên>: <dem> lan so sanh, ket qua <mảng đã sắp>` (mảng in bằng `print` của chính danh sách, ví dụ `[1, 3, 5, 7, 9]`);
- với hai mảng `[9, 4, 7, 1, 4, 8]` và `[9, 4, 7, 1, 5, 8]`, mỗi mảng một dòng `co trung <mảng gốc>` hoặc `khong trung <mảng gốc>`.

Chạy: `python giam_de_tri.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L13 giam_de_tri.py`.
