# Lab CS115 L43 — Diffusion: suy giảm tín hiệu alpha_bar qua T bước

Đọc `stdin` `T=<int> b0=<f> b1=<f>`. Chạy vòng lặp lịch tuyến tính `T` bước tính `alpha_bar = prod(1 - beta_t)` và hệ số nhiễu `sqrt(1 - alpha_bar)`.

In 2 dòng chuẩn: `alpha_bar_500=<.2e>`, `noise_scale=<.6f>`.
Chấm tự động: `bash labs/cham.sh CS115 L43 duong_dan/bai_cua_ban.py`
