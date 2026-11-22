# Lab ESY L09 — Phân tích mức dùng bộ xử lý (CPU), cận Liu–Layland và phép lặp thời gian đáp ứng (RTA)

Cho ba tác vụ ưu tiên cố định từ cao xuống thấp `[(C1=1, T1=5), (C2=2, T2=8), (C3=2, T3=16)]` (đơn vị `ms`). Tính tổng độ sử dụng `U` (3 chữ số `:.3f`), cận Liu–Layland `3*(2^(1/3) - 1)` (4 chữ số `:.4f`) và lặp phương trình `R = C3 + sum(ceil(R/Ti)*Ci)` tìm thời gian đáp ứng xấu nhất `R3` của tác vụ 3.
In đúng 1 dòng `U=... LL_bound=... exact_R3=...`.

Chấm tự động:
```bash
bash labs/cham.sh ESY L09 duong_dan/bai_cua_ban.py
```
