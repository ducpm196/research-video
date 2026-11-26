# Lab CS115 L31 — NMF X ≈ A*B: quy tắc nhân giữ mọi phần tử không âm

Đọc `stdin` `x=<x0,x1> a0=<a00,a01> a1=<a10,a11> b=<b0,b1> steps=<int>`. Chạy `steps` vòng cập nhật nhân `B <- B * (A^T X) / (A^T A B)` và in kết quả từng bước.

In mỗi bước 1 dòng: `step<i> B=<list4> err=<.4f>`.
Chấm tự động: `bash labs/cham.sh CS115 L31 duong_dan/bai_cua_ban.py`
