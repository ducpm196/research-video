# Lab CS115 L43 — Diffusion: suy giảm tín hiệu alpha_bar = prod(1 - beta_t) qua 500 bước

Với lịch tuyến tính mới `T = 500` bước từ `beta_0 = 0.0002` tới `beta_{T-1} = 0.015`, chạy vòng lặp tính `alpha_bar = prod(1 - beta_t)` và tính hệ số tỉ lệ độ lệch nhiễu `sqrt(1 - alpha_bar)`.

Định dạng đầu ra (2 dòng):
`alpha_bar_500=<2 chữ số dạng e>`
`noise_scale=<6 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L43 duong_dan/bai_cua_ban.py
```
