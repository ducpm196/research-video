# Lab SWF L00 — Đặc tả hợp đồng: tiền điều kiện và hậu điều kiện

Viết chương trình Python cài hàm `bsearch_checked(a, x)` kiểm tra tiền điều kiện mảng `a` đã sắp tăng (nếu chưa sắp ném `ValueError`), tìm vị trí `x`, kiểm hậu điều kiện `a[i] == x` và chạy thử trên `[2, 5, 8, 12]` (tìm 8) và `[5, 2]` (bắt lỗi), in đúng 3 dòng:
1. `found_idx=2`
2. `missing_idx=-1`
3. `unsorted_rejected=1`

Chấm tự động:
```bash
bash labs/cham.sh SWF L00 duong_dan/bai_cua_ban.py
```
