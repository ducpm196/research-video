# Lab SEC L10 — Tính ngưỡng 50% va chạm ngày sinh của hàm băm

Đọc `stdin` `bits=<int>`. Tính số lượng khóa `k = sqrt(2 * 2^bits * ln(2))` đạt ngưỡng 50% va chạm ngày sinh, số bit bảo mật chống va chạm `bits // 2` và tỉ số `round(k / 2^(bits // 2))` so với ngưỡng va chạm `2^(bits/2)` (giữ tên khoá đầu ra cố định `ratio_vs_32bit_hash` theo chuẩn bộ chấm).

In đúng 3 dòng: `birthday_50pct_billions=<.2f>`, `bit_security_collision=<d>`, `ratio_vs_32bit_hash=<d>`.
Chấm tự động: `bash labs/cham.sh SEC L10 duong_dan/bai_cua_ban.py`
