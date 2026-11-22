# Lab SWF L03 — Lỗi lệch một và tràn số (lo + hi)//2 trên 32 bit

Viết chương trình Python mô phỏng số nguyên có dấu 32 bit (`INT32_MAX = 2**31 - 1`): với `lo = 2_000_000_000, hi = 2_100_000_000`, tính điểm giữa bằng `(lo + hi) // 2` bị tràn có dấu so với `lo + (hi - lo) // 2`, in đúng 3 dòng:
1. `naive_sum_overflows=1`
2. `safe_mid=2050000000`
3. `in_bounds=1`

Chấm tự động:
```bash
bash labs/cham.sh SWF L03 duong_dan/bai_cua_ban.py
```
