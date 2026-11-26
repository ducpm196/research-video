# Lab BNX L06 — Giao dịch chuyển tiền: hoàn tác khi vi phạm ràng buộc số dư

Oracle không có trong bộ chấm, nên lab dùng **sqlite** (có sẵn trong Python, không cần cài thêm) để luyện đúng ý của bài: nhóm câu lệnh cùng thành công hoặc cùng bị huỷ, và tổng tiền giữ nguyên. Số liệu là số minh hoạ. `isolation_level=None` nghĩa là Python không tự mở giao dịch hộ, ta tự gõ `BEGIN` và `COMMIT`. Trong câu SQL, dấu `?` là chỗ điền giá trị (`db.execute("… + ? WHERE id = ?", (tien, b))` điền `tien` rồi `b`); `try … except sqlite3.IntegrityError` thử làm, nếu ràng buộc bị vi phạm thì chạy phần `except`.

Dựng bảng bằng đoạn sau (cho sẵn):

```python
import sqlite3
db = sqlite3.connect(":memory:", isolation_level=None)   # tự quản lý giao dịch
db.executescript('''
CREATE TABLE tk (id INTEGER PRIMARY KEY, so_du INTEGER CHECK (so_du >= 0));
INSERT INTO tk VALUES (1, 500), (2, 400), (3, 300);
''')
```
Viết `mau.py` có hàm `chuyen(a, b, tien)` làm đúng theo thứ tự **cộng tài khoản nhận trước, rồi trừ tài khoản gửi** trong MỘT giao dịch (`BEGIN` … `COMMIT`). Nếu ràng buộc `CHECK` bị vi phạm (sqlite ném `sqlite3.IntegrityError`) thì `ROLLBACK` để phần cộng đã làm cũng bị huỷ, và hàm trả chữ `loi so du khong du`; thành công thì trả `OK`.

Chạy bốn lệnh `(1, 2, 300)`, `(2, 3, 900)`, `(3, 1, 50)`, `(1, 3, 250)` theo thứ tự, mỗi lệnh in một dòng, rồi in tổng tiền sau cùng:
```
chuyen <a>-><b> <tien>: <OK | loi so du khong du>
tong tien: <số>
```
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L06 mau.py`.

## Phần thêm trên Oracle thật (tuỳ chọn)
Khi có container `bnx-ora`, chạy `bash labs/BNX/L06/oracle/chay.sh` (tệp `labs/BNX/L06/oracle/thu.sql`) để thực hành thủ tục PL/SQL có `SAVEPOINT` và `ROLLBACK` khi vi phạm `CHECK (so_du >= 0)` trên Oracle thật; lab `sqlite` ở trên là đường lùi bắt buộc mặc định.
