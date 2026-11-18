# Lab BNX L07 — JSON có ràng buộc kiểm hợp lệ, truy vấn theo trường

Oracle không có trong bộ chấm, nên lab dùng **sqlite** (có sẵn trong Python; cần bản sqlite từ 3.38, có sẵn hàm JSON) để luyện ý của bài: cột JSON có ràng buộc `IS JSON` bên Oracle tương ứng `CHECK (json_valid(...))` bên sqlite (`json_valid` trả đúng khi chuỗi là JSON hợp lệ), và lấy trường trong JSON bằng `json_extract` (lấy một trường theo đường dẫn như `'$.tien'`) hoặc toán tử `->>`. Số liệu là số minh hoạ.

Viết `mau.py`:
1. Bảng `gd (id INTEGER PRIMARY KEY, chi_tiet TEXT CHECK (json_valid(chi_tiet)))`.
2. Chèn lần lượt năm dòng sau; dòng nào vi phạm `CHECK` (sqlite ném `sqlite3.IntegrityError`) thì in `dong <id>: tu choi (JSON hong)` và bỏ qua:
```python
DONG = [(1, '{"kenh":"atm","may":"A7","tien":500000}'),
        (2, '{"kenh":"app","thiet_bi":"d9","tien":200000}'),
        (3, '{"kenh":"atm","may":"B2"'),
        (4, '{"kenh":"app","thiet_bi":"d1","tien":900000}'),
        (5, '{"kenh":"atm","may":"A7","tien":300000}')]
```
3. In tổng `tien` của kênh `atm`, số giao dịch của kênh `app`, và số giao dịch của máy `A7` (lấy trường bằng `json_extract(chi_tiet, '$.tien')` hoặc toán tử `->>`).

Trong Python, `try … except sqlite3.IntegrityError` thử làm và chạy phần `except` khi ràng buộc bị vi phạm; dấu `?` trong câu SQL là chỗ điền giá trị (`db.execute("INSERT INTO gd VALUES (?, ?)", (i, js))`).

In đúng bốn dòng:
```
dong 3: tu choi (JSON hong)
tong tien kenh atm: <số>
so giao dich kenh app: <số>
may A7: <số> giao dich
```
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L07 mau.py`.

**Làm thêm trên Oracle thật (không chấm tự động):** dựng Oracle Free bằng Docker theo bài, dán lại khối tạo bảng, nạp 3 650 dòng và chạy kế hoạch của tháng ba; bạn phải thấy `PARTITION RANGE SINGLE` với Pstart = Pstop = 3.
