# Lab RLN L09 — Tối ưu chính sách gần kề (PPO): cắt tỉ số an toàn

Áp dụng công thức `min(rho * A, clip(rho, 1 - eps, 1 + eps) * A)` với `eps = 0.2` cho hai trường hợp: lợi thế dương `(rho = 1.4, A = 3.0)` (bị cắt trần) và lợi thế âm `(rho = 0.6, A = -3.0)`.

Định dạng đầu ra (1 dòng):
`pos_clipped=<1 chữ số> neg_unclipped=<1 chữ số>`
