# Lab PYT L09 — Trung bình, độ lệch chuẩn, chuẩn hoá cột

**cần: pip install -r labs/requirements-py.txt** (trong môi trường ảo của bài 8). Tạo `chuan_hoa.py` (số minh hoạ; khác ví dụ trong bài):

```python
import numpy as np
so_lieu = np.array([[120, 4000], [150, 5200], [90, 3100], [200, 6100], [140, 4600]], dtype=float)
# cột 0: số giao dịch/ngày; cột 1: doanh thu (nghìn đồng)
```

In lần lượt (dùng `np.round`):
1. `Trung binh:` rồi trung bình từng cột, làm tròn 2 chữ số;
2. `Do lech chuan:` rồi độ lệch chuẩn từng cột (`std`, mặc định chia $n$), tròn 2 chữ số;
3. mảng đã chuẩn hoá `(x - trung bình) / độ lệch chuẩn` từng cột, tròn 3 chữ số;
4. `Trung binh cot sau chuan hoa ~ 0:` rồi `np.allclose(chuan.mean(axis=0), 0)`;
5. `Do lech chuan cot sau chuan hoa:` rồi độ lệch chuẩn từng cột mới, tròn 6 chữ số.

Chạy: `python chuan_hoa.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L09 chuan_hoa.py` (trên máy chấm của khoá dùng `labs/.venv-pyt`).
