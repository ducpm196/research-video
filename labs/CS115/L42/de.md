# Lab CS115 L42 — VAE KL(N(mu, sigma^2) || N(0, 1)) và điểm tối ưu trò chơi GAN

Tính độ lệch `KL = 0.5 * (sigma^2 + mu^2 - 1 - ln(sigma^2))` tại `(mu = 1.0, sigma = 2.0)` và xác định bộ phân biệt tối ưu `D*` cùng giá trị trò chơi tại **cân bằng Nash** của GAN khi mật độ thật `p_real = 0.25` và mật độ giả `p_fake = 0.25`.

Định dạng đầu ra (2 dòng):
`vae_kl=<4 chữ số>`
`gan_nash_d=<2 chữ số> val=<4 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L42 duong_dan/bai_cua_ban.py
```
