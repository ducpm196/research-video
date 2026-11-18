# Lab BNX L24 — Đếm câu SQL: một cộng N so với nối bảng

Cơ sở dữ liệu nhỏ (sqlite, không cần cài thêm gì) có bảng `khach(id, ten)` (12 khách) và bảng `the(id, khach_id, han_muc)` (mỗi khách 3 thẻ, `khach_id` là khoá ngoại). Dựng dữ liệu bằng đoạn sau (cho sẵn, không cần viết lại):

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE khach (id INTEGER PRIMARY KEY, ten TEXT)")
db.execute("CREATE TABLE the (id INTEGER PRIMARY KEY, khach_id INTEGER, han_muc INTEGER)")
for i in range(1, 13):
    db.execute("INSERT INTO khach VALUES (?, ?)", (i, f"K{i}"))
    for j in range(1, 4):
        db.execute("INSERT INTO the VALUES (?, ?, ?)", (i * 10 + j, i, 2000000 * j))
db.commit()
```
Số liệu là số minh hoạ. Viết chương trình Python (`mau.py`) làm hai cách và **đếm số câu SQL thật** bằng `db.set_trace_callback(hàm)`
(thư viện sqlite3 gọi hàm đó mỗi lần chạy một câu). Đăng ký hàm này SAU khi đã nạp dữ liệu, để các câu tạo bảng và nạp dữ liệu không bị đếm:

1. Cách 1: một câu lấy danh sách khách, rồi với MỖI khách một câu lấy thẻ của khách đó. Cộng tổng số thẻ.
2. Cách 2: một câu `JOIN` hai bảng lấy mọi cặp (khách, thẻ).

In đúng hai dòng: `Cach 1: <số câu> cau, tong so the <n>` và `Cach 2: <số câu> cau, tong so the <n>`.
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L24 mau.py`.
