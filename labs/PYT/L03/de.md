# Lab PYT L03 — Đếm tần suất và gộp theo khoá

Cần: Python 3.11 trở lên. Tạo `gop_khoa.py`. Dữ liệu (chép nguyên; số minh hoạ, khác ví dụ trong bài):

```python
giao_dich = [("A02", 500000), ("A01", 200000), ("A03", 950000), ("A02", 150000), ("A01", 700000), ("A02", 50000)]
ten = {"A01": "Hoa", "A02": "Nam", "A03": "Linh"}
```

1. Dùng hai từ điển đếm số giao dịch và cộng tiền theo mã. Với mỗi mã **theo thứ tự mã** in `<mã> <số giao dịch> <tổng tiền>`.
2. Rồi in `<tên> <tổng tiền>` cho mỗi mã, **theo tổng giảm dần**.

Chạy: `python gop_khoa.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L03 gop_khoa.py`.
