# Lab DSY L02 — So sánh đồng hồ Vector (happens-before vs concurrent)

Đọc `stdin` `u1=<a,b,c> v1=<a,b,c> u2=<a,b,c> v2=<a,b,c>`. Cài hàm `rel(u, v)` trả `'before'`, `'after'`, `'equal'` hoặc `'concurrent'`.

In đúng 3 dòng: `v100_vs_v201=<rel>`, `v201_vs_v120=<rel>`, `partial_order_ok=<0|1>` (`1` khi `u1,v1` có quan hệ nhân quả trước/sau/bằng và `u2,v2` là `concurrent`; ngược lại `0`).
Chấm tự động: `bash labs/cham.sh DSY L02 duong_dan/bai_cua_ban.py`
