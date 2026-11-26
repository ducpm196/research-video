# Lab DVO L10 — Độ sẵn sàng MTBF / (MTBF + MTTR) khi giảm MTTR

Đọc `stdin` `mtbf=<float> mttr_slow=<float> mttr_fast=<float>`. Tính phần trăm sẵn sàng ở hai mức thời gian khôi phục và hệ số rút ngắn downtime.

In đúng 3 dòng: `avail_1h=<.3f>%`, `avail_15m=<.3f>%`, `downtime_cut_factor=<.1f>x`.
Chấm tự động: `bash labs/cham.sh DVO L10 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
