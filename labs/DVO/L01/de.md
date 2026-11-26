# Lab DVO L01 — Tính xác suất xung đột hợp nhất nhánh dài vs nhánh ngắn

Đọc `stdin` `total=<int> hot=<int> k_long=<int> k_short=<int>`. Tính xác suất ít nhất một lần chạm vào `hot` trong `total` tệp cho `k_long` và `k_short` thay đổi.

In đúng 3 dòng: `p_conflict_40=<.1f>%`, `p_conflict_5=<.1f>%`, `shorter_branch_safer=<0|1>`.
Chấm tự động: `bash labs/cham.sh DVO L01 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
