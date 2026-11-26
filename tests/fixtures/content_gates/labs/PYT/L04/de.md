# Lab PYT L04 — Trích mã và số tiền từ nhật ký

Cần: Python 3.11 trở lên. Tạo `trich_log.py`. Dữ liệu (chép nguyên; minh hoạ, khác ví dụ trong bài):

```python
nhat_ky = [
    "10:15:02 GD#A0731 chuyen 1.250.000 VND tu A01 den A02",
    "10:15:09 GD#A0732 rut 500.000 VND tu A03",
    "10:16:40 GD#A0733 nap 12.000.000 VND vao A01",
    "10:17:01 LOI GD#A0734 timeout",
    "10:17:30 GD#A0735 chuyen 75.000 VND tu A02 den A03",
]
```

1. Với mỗi dòng **có** số tiền (mẫu `[\d.]+ VND`): in `<mã> <số tiền>` — mã là phần sau `GD#`, số tiền là **số nguyên** (bỏ dấu chấm ngăn hàng nghìn). Dòng lỗi (không có `VND`) thì bỏ qua.
2. Cuối cùng in `Tong: <tổng>`.

Dùng `import re`. Chạy: `python trich_log.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L04 trich_log.py`.
