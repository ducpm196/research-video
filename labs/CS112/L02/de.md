# Lab CS112 L02 — "Lần đầu hơn" và "mãi mãi hơn" khác nhau

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `xep_hang.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó.

Với hai hàm `a(n)` và `b(n)` (số nguyên), có hai câu hỏi khác nhau, cho `n` từ 1 đến 300:
- `lan_dau`: `n` **nhỏ nhất** có `a(n) > b(n)`;
- `mai_mai`: `n` **nhỏ nhất** sao cho `a(n) > b(n)` đúng với **mọi** `n` từ đó đến 300 (cho `n` chạy lùi từ 300 về 1, nhớ `n` cuối còn đúng, dừng ở `n` đầu tiên sai).

Viết hàm `so_sanh(ten, a, b)` tính hai số trên rồi in một dòng, đúng chữ không dấu: `<ten>: lan dau <lan_dau>, mai mai tu <mai_mai>`. Truyền hàm vào hàm bằng `lambda`, ví dụ `lambda n: 2 ** n` là hàm nhận `n` trả `2` mũ `n` (`**` là phép lũy thừa); giai thừa lấy bằng `math.factorial(n)` sau `import math`.

Gọi `so_sanh` cho bốn cặp, theo thứ tự (số liệu minh hoạ, **khác ví dụ trong bài**):
1. `"2^n va n^5"`: `2 ** n` và `n ** 5`
2. `"2^n va n^10"`: `2 ** n` và `n ** 10`
3. `"n! va 3^n"`: `math.factorial(n)` và `3 ** n`
4. `"4^n va 1000*2^n"`: `4 ** n` và `1000 * 2 ** n`

Chạy: `python xep_hang.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L02 xep_hang.py`.
