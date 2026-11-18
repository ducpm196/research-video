# Lab PYT L10 — Thống kê giao dịch theo loại và theo ngày

**cần: pip install -r labs/requirements-py.txt** (trong môi trường ảo của bài 8). Tạo `thong_ke.py`. Dòng đầu chương trình **ghi sẵn** `gd.csv` bằng `Path("gd.csv").write_text(..., encoding="utf-8")` (số minh hoạ; khác ví dụ trong bài):

```
ma,ngay,loai,kenh,so_tien
1,2026-04-01,rut,atm,500000
2,2026-04-01,chuyen,app,1200000
3,2026-04-02,nap,quay,5000000
4,2026-04-02,chuyen,app,250000
5,2026-04-03,rut,atm,700000
6,2026-04-03,thanh_toan,pos,
7,2026-04-04,chuyen,web,90000
8,2026-04-04,nap,app,3000000
```

1. Đọc bằng `pd.read_csv("gd.csv", parse_dates=["ngay"])`. In `Thieu so_tien: <số ô thiếu>`.
2. Bỏ dòng thiếu `so_tien`; in bảng `count` và `sum` của `so_tien` **theo `loai`**.
3. In tổng `so_tien` **theo ngày trong tháng** (`sach["ngay"].dt.day`), rồi `Ngay nhieu nhat: <ngày> <tổng nguyên>`. `idxmax()` cho nhãn (ngày) của giá trị lớn nhất; tổng là số thực nên in bằng `int(...)` (ví dụ `5250000`, không phải `5250000.0`).

Chạy: `python thong_ke.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L10 thong_ke.py` (trên máy chấm của khoá dùng `labs/.venv-pyt`).
