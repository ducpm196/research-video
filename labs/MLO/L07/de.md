# Lab MLO L07 — Phát hành chạy bóng: đếm số yêu cầu lệch nhãn

Đọc `stdin` `old=<p1,p2,...> new=<p1,p2,...> thr=<float>`. Với ngưỡng phân loại `thr`, giữ phục vụ bằng `old` và đếm số mẫu hai mô hình cho nhãn khác nhau.

In 1 dòng: `served=old disagree=<d>/<n>`.
Chấm tự động: `bash labs/cham.sh MLO L07 duong_dan/bai_cua_ban.py`
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
