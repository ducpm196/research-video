# Lab PYT L01 — Phân loại giao dịch theo mức tiền

Cần: Python 3.11 trở lên. Tạo `phan_loai.py`. Danh sách giao dịch (chép nguyên, số minh hoạ — khác ví dụ trong bài):

```python
giao_dich = [250000, 3200000, 75000000, 1800000, 64000000, 900000, 5000000, 120000]
```

1. Với **mỗi** giao dịch (vòng `for`) in một dòng `<số tiền> <mức>`:
   `nho` nếu dưới 2 000 000; `vua` nếu dưới 60 000 000; còn lại `lon`.
2. Sau vòng lặp in `Tong: <tổng tiền>` và `Nho, vua, lon: <a> <b> <c>` (số giao dịch của từng mức, cách nhau một dấu cách).

Chạy: `python phan_loai.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L01 phan_loai.py`.
