# Lab CS112 L14 — Quay lui liệt kê hoán vị không có phần tử đứng yên, có và không cắt tỉa

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `quay_lui.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó. Số liệu minh hoạ, **khác ví dụ trong bài**.

Bài toán: liệt kê các hoán vị `x` của `1…n` mà **không phần tử nào đứng yên**, tức `x[i] != i + 1` với mọi vị trí `i` (đếm vị trí từ 0). Với `n = 3` các nghiệm là `2 3 1` và `3 1 2`.

Viết hàm `liet_ke(n, cat_tia)` trả về `(số nghiệm, số nút của cây trạng thái)` bằng quay lui đúng khung của bài:
- `x = []` (dãy đang xây), `da_dung = [False] * (n + 1)`; hai bộ đếm đặt trong một danh sách `ket_qua = [0, 0]` (nghiệm, nút) để hàm đệ quy bên trong cộng vào được.
- Hàm đệ quy `thu(i)` (viết ngay trong `liet_ke`): cộng 1 vào số nút; nếu `i == n` thì kiểm `all(x[k] != k + 1 for k in range(n))`, đúng thì cộng 1 vào số nghiệm, rồi `return`; ngược lại, với `j` từ 1 đến `n`: bỏ qua `j` đã dùng; **khi `cat_tia` là `True`** thì bỏ qua cả `j == i + 1` (cắt nhánh ngay, trước khi đi sâu); còn lại thì **đánh dấu** `da_dung[j] = True`, `x.append(j)`, gọi `thu(i + 1)`, rồi **trả lại dấu** `x.pop()`, `da_dung[j] = False`.
- Gọi `thu(0)` rồi trả `(ket_qua[0], ket_qua[1])`.

In, cho `n` trong `(4, 5, 6)`, một dòng đúng chữ không dấu: `n = <n>: <nghiệm> nghiem, <nút có tỉa> nut khi cat tia, <nút không tỉa> nut khi khong cat, cung so nghiem: dung` (hoặc `sai` nếu số nghiệm hai lần chạy khác nhau).

Chạy: `python quay_lui.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L14 quay_lui.py`.
