# Lab BNX L38 — Hàng đợi có giao dịch và lệnh chuyển xuyên mảnh

Oracle không có trong bộ chấm, nên lab dùng **sqlite** (có sẵn trong Python) để luyện đúng ý của bài: gửi vào hàng đợi nằm trong giao dịch (hoàn tác thì thông điệp mất), nhận ra theo thứ tự vào trước ra trước, và đếm lệnh chuyển xuyên mảnh. Số liệu là số minh hoạ.

Viết `mau.py`:
1. Bảng `hang_doi (id INTEGER PRIMARY KEY AUTOINCREMENT, ma_gd INTEGER, so_tien INTEGER)`; mở kết nối bằng `sqlite3.connect(":memory:", isolation_level=None)` để tự quản lý giao dịch (`BEGIN`, `COMMIT`, `ROLLBACK`).
2. Hàm `gui(ma, tien, chot)`: trong một giao dịch, chèn một dòng; `chot` đúng thì `COMMIT`, sai thì `ROLLBACK`.
3. Hàm `nhan()`: trong một giao dịch, lấy dòng có `id` nhỏ nhất, xoá nó, `COMMIT`, trả về dòng đó (hàng trống thì trả `None`).
4. Gửi lần lượt `(201, 750000)` chốt, `(202, 300000)` hoàn tác, `(203, 120000)` chốt, `(204, 900000)` chốt. In `sau gui: <số dòng> thong diep`. Nhận hai lần, mỗi lần in `nhan: <ma_gd> <so_tien>`. In `con lai: <số dòng>`.
5. Mảnh của một tài khoản = mã chia lấy dư cho 4. Với năm lệnh chuyển `(3, 8)`, `(4, 9)`, `(7, 11)`, `(10, 14)`, `(6, 13)`, in `xuyen manh: <số lệnh xuyên mảnh>/5`.

In đúng năm dòng:
```
sau gui: <số> thong diep
nhan: <ma_gd> <so_tien>
nhan: <ma_gd> <so_tien>
con lai: <số>
xuyen manh: <số>/5
```
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L38 mau.py`.

## Phần thêm trên Oracle thật (tuỳ chọn)
Khi có container `bnx-ora`, chạy `bash labs/BNX/L38/oracle/chay.sh` (tệp `labs/BNX/L38/oracle/thu.sql`) để chạy hàng đợi giao dịch thật `DBMS_AQ` (`ENQUEUE`/`COMMIT`/`ROLLBACK`/`DEQUEUE`) trên Oracle; lab `sqlite` ở trên là đường lùi bắt buộc mặc định.
