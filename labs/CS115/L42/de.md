# Lab CS115 L42 — VAE KL và điểm tối ưu trò chơi GAN

Đọc `stdin` `mu=<f> sig=<f> pr=<f> pf=<f>`. Tính phân kỳ `KL` của bộ mã hóa biến phân và bộ phân biệt cân bằng Nash `D* = pr / (pr + pf)` cùng giá trị trò chơi GAN.

In 2 dòng chuẩn: `vae_kl=<.4f>`, `gan_nash_d=<.2f> val=<.4f>`.
Chấm tự động: `bash labs/cham.sh CS115 L42 duong_dan/bai_cua_ban.py`
