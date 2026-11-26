# Lab MLO L05 — Lệch huấn luyện-phục vụ khi không dùng chung chuẩn hoá

Đọc `stdin` `x=<f> std=<f> m_tr=<f> m_sv=<f>`. Tính z-score theo trung bình huấn luyện `m_tr` và khi phục vụ viết nhầm trung bình `m_sv`.

In 1 dòng: `z_train=<.1f> z_serve_skew=<.1f>`.
Chấm tự động: `bash labs/cham.sh MLO L05 duong_dan/bai_cua_ban.py`
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Ghi chú: giá trị chuẩn hoá `z` còn gọi là `z-score`.
