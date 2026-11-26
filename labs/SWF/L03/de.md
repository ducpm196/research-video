# Lab SWF L03 — Lỗi lệch một và tràn số (lo + hi)//2 trên 32 bit

Đọc `stdin` `lo=<int> hi=<int> max32=<int>`. So sánh `(lo + hi)` có vượt `max32` hay không với công thức an toàn `lo + (hi - lo) // 2`.

In đúng 3 dòng: `naive_sum_overflows=<0|1>`, `safe_mid=<d>`, `in_bounds=<0|1>`.
Chấm tự động: `bash labs/cham.sh SWF L03 duong_dan/bai_cua_ban.py`
