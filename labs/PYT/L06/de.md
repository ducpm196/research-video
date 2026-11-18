# Lab PYT L06 — Lớp TaiKhoan có nạp, rút, thấu chi

Cần: Python 3.11 trở lên. Tạo `tai_khoan.py` với lớp `TaiKhoan(ma, so_du=0, thau_chi=0)` (`thau_chi` = thấu chi: mức số dư được phép âm; số minh hoạ, khác ví dụ trong bài):

- `nap(tien)`: nếu `tien <= 0` trả `False`, không đổi gì; ngược lại cộng vào số dư và trả `True`.
- `rut(tien)`: trả `False` (không đổi gì) nếu `tien <= 0` **hoặc** số dư sau khi rút sẽ nhỏ hơn `-thau_chi`; ngược lại trừ và trả `True`.
- `__repr__`: trả chuỗi `TaiKhoan(<ma>, <so_du>)`.

Rồi thêm **đúng đoạn thử này** vào cuối tệp:

```python
a = TaiKhoan("B07", 2000000, thau_chi=500000)
print(a.rut(2400000), a)
print(a.rut(200000), a)
print(a.nap(600000), a)
print(a.nap(-5), a)
b = TaiKhoan("B08")
print(b)
```

**Phần đo** (lab chấm *hình dạng* kết quả, không chấm số byte tuyệt đối vì mỗi máy một khác): thêm tiếp, sau đoạn thử, `import sys` và `import tracemalloc`; tạo `so = [i for i in range(1000)]` và `chuoi = ["x" * 100 + str(i) for i in range(1000)]`.

- In `getsizeof hai danh sach: bang nhau` nếu `sys.getsizeof(so) == sys.getsizeof(chuoi)`, ngược lại `getsizeof hai danh sach: khac nhau`.
- Với mỗi danh sách, `tracemalloc.start()`, tạo danh sách (viết lại câu tạo trong một hàm), lấy `tracemalloc.get_traced_memory()[0]` rồi `tracemalloc.stop()`. In `tracemalloc hai danh sach: chuoi lon hon` nếu số byte của danh sách chuỗi lớn hơn, ngược lại `tracemalloc hai danh sach: so lon hon`.

Chạy: `python tai_khoan.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L06 tai_khoan.py`.
