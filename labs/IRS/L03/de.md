# Lab IRS L03 — Truy hồi dày IVF: phép so theo cụm và tăng tốc

Đọc từ đầu vào chuẩn (`stdin`, dạng `khoá=giá_trị`) ba số nguyên `N=<int> clusters=<int> probe=<int>`. Tính tổng số phép so IVF `ivf = clusters + probe * (N // clusters)` và hệ số tăng tốc `N / ivf` so với quét thẳng.

In 1 dòng đúng nhãn (`<d>` là số nguyên, `<.1f>` làm tròn 1 chữ số thập phân): `ivf_ops=<d> speedup=<.1f>x`.
Chấm tự động: `bash labs/cham.sh IRS L03 duong_dan/bai_cua_ban.py`
