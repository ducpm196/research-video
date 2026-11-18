# Lab PYT L00 — Lãi tiết kiệm sáu tháng

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Nếu máy báo không tìm thấy `python`: tải bản cài từ python.org, **tích ô thêm Python vào PATH** khi cài, rồi mở lại Git Bash và kiểm lại. Không cần cài thêm thư viện nào.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `lai_tk.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó (mở thư mục đó trong File Explorer, chuột phải vào chỗ trống, chọn *Open Git Bash here*; Windows 11: chọn *Show more options* trước). Kiểm: gõ `pwd` (in thư mục đang đứng) và `ls` (phải thấy `labs/`). Đang đứng sai chỗ thì dùng `cd tên_thư_mục` để đi vào, `cd ..` để lùi ra. Các bài sau chỉ nhắc "mở Git Bash ở thư mục gốc của bộ khoá": làm đúng như vậy.

Tạo `lai_tk.py`. Đặt ba biến (số minh hoạ, **khác ví dụ trong bài**):

```python
so_du = 25000000      # đồng
lai_suat = 0.084      # 8,4% một năm
thang = 6
```

Rồi in **đúng bốn dòng**, theo thứ tự (dùng chuỗi có chỗ điền `f"…{biến}…"`; `:,` ngăn hàng nghìn):
1. `So du goc: <số dư, có dấu phẩy ngăn hàng nghìn>`
2. `Lai 6 thang: <lãi làm tròn thành số nguyên, có dấu phẩy ngăn hàng nghìn>` — lãi = `so_du * lai_suat * thang / 12`, rồi `round(...)`
3. `Tong nhan duoc: <gốc + lãi đã làm tròn, có dấu phẩy ngăn hàng nghìn>`
4. `Kieu cua lai: <tên kiểu của lãi TRƯỚC khi làm tròn>` (gợi ý: `type(lai).__name__` — dấu chấm lấy thuộc tính của giá trị, `__name__` là tên kiểu bằng chữ, ví dụ `type(5).__name__` là `int`)

Chạy: `python lai_tk.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L00 lai_tk.py`.
