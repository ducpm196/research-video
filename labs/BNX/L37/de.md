# Lab BNX L37 — Chống chèn mã: ghép chuỗi so với tham số hoá

SQL Server không có trong bộ chấm, nên lab dùng **sqlite** (có sẵn trong Python) để luyện đúng ý của bài: chuỗi người dùng gõ phải đi vào câu lệnh như một **giá trị**, không như một phần **câu lệnh**. Số liệu là số minh hoạ.

Dựng bảng bằng đoạn sau (cho sẵn):

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE tk (ten TEXT, so_du INTEGER)")
db.executemany("INSERT INTO tk VALUES (?, ?)",
               [("An", 500), ("Binh", 700), ("Chi", 900), ("Dung", 100)])
```

Viết `mau.py` có hai hàm tìm theo tên, mỗi hàm trả danh sách dòng `SELECT ten FROM tk WHERE ten = …`:
1. `ghep(ten)`: **ghép chuỗi** `ten` thẳng vào câu lệnh (cách sai, để thấy lỗi);
2. `tham_so(ten)`: truyền `ten` qua dấu `?` (cách đúng).

Với ba chuỗi sau (dòng 2 và 3 là chuỗi tấn công; trong chuỗi 3, `--` mở đầu chú thích SQL nên phần sau nó bị bỏ qua), đánh số từ 1, in mỗi chuỗi một dòng:
```python
CHUOI = ("An", "X' OR '1'='1", "B' OR so_du > 600 --")
```
```
chuoi <số thứ tự>: ghep <số dòng> dong, tham so <số dòng> dong
```
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L37 mau.py`.
