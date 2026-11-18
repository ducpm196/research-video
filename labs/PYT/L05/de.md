# Lab PYT L05 — Đọc CSV giao dịch, ghi JSON báo cáo

Cần: Python 3.11 trở lên. Tạo `bao_cao.py`. Dòng đầu chương trình **ghi sẵn** tệp `gd.csv` bằng `Path("gd.csv").write_text(..., encoding="utf-8")` với nội dung (minh hoạ, khác ví dụ trong bài):

```
ma,loai,tai_khoan,so_tien
1,rut,A02,500000
2,chuyen,A01,1200000
3,nap,A03,3000000
4,chuyen,A02,250000
5,rut,A01,700000
6,chuyen,A03,90000
```

1. Đọc bằng `csv.DictReader`; tính **tổng tiền theo loại** (số nguyên) và **số giao dịch**.
2. Ghi `bao_cao.json` dạng `{"so_giao_dich": …, "tong_theo_loai": {…}}` với `sort_keys=True`, `ensure_ascii=False`.
3. Đọc lại tệp; in **nội dung tệp** (một dòng) rồi dòng `<so_giao_dich> <tổng loại nap>`.

Chạy: `python bao_cao.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L05 bao_cao.py`.
