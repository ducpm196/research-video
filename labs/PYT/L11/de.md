# Lab PYT L11 — Vẽ một biểu đồ cột và mô tả đúng bằng số liệu vẽ

**cần: pip install -r labs/requirements-py.txt** (trong môi trường ảo của bài 8). Tạo `ve_bieu_do.py`. Ba dòng đầu:

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
```

Dữ liệu (số minh hoạ; khác ví dụ trong bài): `kenh = ["atm", "app", "quay"]`, `tong = [4200, 6100, 1500]` (nghìn đồng).

1. Vẽ biểu đồ cột (`ax.bar`), tiêu đề **`Tong tien theo kenh (nghin dong)`**, nhãn trục y; lưu `bieu_do.png`.
2. In năm dòng, **đọc lại từ chính biểu đồ** (`ax.patches`, `ax.get_ylim()`, `ax.get_title()`):
   `Ve xong: <True/False>` (tệp tồn tại) · `Do cao cot: [..]` (số nguyên) · `Truc y bat dau tu 0: <True/False>` · `Tieu de: …` · `Lon nhat: <kênh> - gap <x> lan nho nhat` (làm tròn 1 chữ số).

Lab kiểm **số liệu vẽ**, không so ảnh. Chạy: `python ve_bieu_do.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L11 ve_bieu_do.py` (trên máy chấm của khoá dùng `labs/.venv-pyt`).
