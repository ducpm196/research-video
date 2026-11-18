# Lab CS112 L00 — Đếm số lần so sánh của hai vòng lặp lồng nhau

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `dem_vong.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó.

Cho hai vòng lặp lồng nhau (số liệu minh hoạ, **khác ví dụ trong bài**):

```
for (i = 1; i <= n; i++)
    for (j = i + 1; j <= n; j++)
        thân vòng trong
```

Trong Python, vòng `j` chạy từ `i + 1` đến `n` viết là `for j in range(i + 1, n + 1):` (số cuối của `range` không được chạy tới, nên phải ghi `n + 1`).

1. Viết hàm `dem(n)` chạy đúng hai vòng lặp trên, đếm **số lần chạy thân vòng trong** (cộng 1 vào một biến đếm mỗi lần thân chạy). Rồi tính **số lần so sánh điều kiện** `j <= n` của vòng trong: mỗi giá trị `i` có thêm đúng một lần so sánh cho kết quả sai để vòng thoát (như bài đã dạy: thân chạy `k` lần thì so sánh `k + 1` lần). Hàm trả về hai số: `(số lần chạy thân, số lần so sánh)`.
2. Với mỗi `n` trong `(8, 20)` in hai dòng, đúng chữ không dấu:
   - `n = <n> so lan chay than: <số>`
   - `n = <n> so lan so sanh: <số>`
3. In dòng cuối: `cong thuc n(n+1)/2 voi n = 20: <số>`, trong đó số tính bằng công thức `20 * 21 // 2` (phép chia số nguyên `//` bỏ phần lẻ). Bạn sẽ thấy số này trùng với số lần so sánh của `n = 20`.

Chạy: `python dem_vong.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L00 dem_vong.py`.
