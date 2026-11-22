# Lab ESY L02 — Chống dội phím bằng máy trạng thái đếm mẫu liên tiếp

Cho chuỗi lấy mẫu `1 ms/lần`: `[0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1]`. Cài máy trạng thái chống dội chỉ đổi trạng thái ngõ ra từ `0 -> 1` khi gặp đúng `5` mẫu giống nhau liên tiếp; đồng thời đếm số lần đổi chiều trên tín hiệu thô vs tín hiệu đã lọc.
In đúng 1 dòng `accepted_at_ms=... raw_edges=... clean_edges=...`.

Chấm tự động:
```bash
bash labs/cham.sh ESY L02 duong_dan/bai_cua_ban.py
```
