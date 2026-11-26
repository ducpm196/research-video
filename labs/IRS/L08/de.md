# Lab IRS L08 — Lấy mẫu âm mũ 0.75 và bù trừ lôgarit

Đọc từ đầu vào chuẩn (`stdin`, dạng `khoá=giá_trị`) `a=<int> b=<int> q=<float>` (trong đó `a`, `b` là số nguyên tần suất hai mục, `q` là xác suất xuất hiện trong lô của công thức `-ln(q)` tương ứng `p` trong bài). Tính xác suất lấy mẫu âm cho `b` theo tần suất thô, theo mũ `0.75` và hệ số bù `-ln(q)`.

In 1 dòng đúng nhãn (`<.3f>` làm tròn 3 chữ số thập phân): `raw_B=<.3f> pow075_B=<.3f> logq_corr=<.3f>`.
Chấm tự động: `bash labs/cham.sh IRS L08 duong_dan/bai_cua_ban.py`
