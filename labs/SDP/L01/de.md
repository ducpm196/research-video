# Lab SDP L01 — Xử lý lỗi tường minh: thất bại sớm thay vì trả kết quả sai âm thầm

Viết chương trình Python cài `parse_strict(s)` chỉ nhận chuỗi toàn chữ số (sai ném `ValueError`) so với `parse_naive(s)` dừng ở `'12a'` và trả nhầm `12`, in đúng 3 dòng:
1. `naive_12a=12`
2. `strict_42=42`
3. `strict_12a_raised=1`

Chấm tự động:
```bash
bash labs/cham.sh SDP L01 duong_dan/bai_cua_ban.py
```
