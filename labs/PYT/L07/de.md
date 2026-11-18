# Lab PYT L07 — Sửa chương trình hỏng, bắt đúng loại ngoại lệ

Cần: Python 3.11 trở lên. Chương trình hỏng (chết ngay ở `"n/a"` với `ValueError`):

```python
def doc_so_tien(chuoi):
    return int(chuoi.replace(".", ""))

giao_dich = ["2.500.000", "75.000", "n/a", "", "-30.000", "1.000.000"]
tong = 0
for chuoi in giao_dich:
    tong = tong + doc_so_tien(chuoi)
print("Tong:", tong)
```

Viết `sua_loi.py` (số minh hoạ; khác ví dụ trong bài):

1. Định nghĩa `class SoTienAm(Exception)`. `doc_so_tien` bỏ dấu chấm, đổi sang số nguyên và **ném** `SoTienAm(chuoi)` nếu số âm.
2. Trong vòng lặp: `except ValueError` in `Bo qua (dinh dang): <repr(chuoi)>`; `except SoTienAm` in `Bo qua (am): <chuoi>`.
3. Dùng `finally` tăng biến đếm `da_xu_ly` mỗi giao dịch. Sau vòng lặp in `Tong: …` rồi `Da xu ly: …`.

Chạy: `python sua_loi.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L07 sua_loi.py`.
