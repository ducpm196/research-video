# Lab RLN L06 — Xấp xỉ hàm và mạng Q sâu (DQN)

Cho `r = 2.0`, `gamma = 0.95`. Tính mục tiêu hồi quy của mạng Q sâu `r + gamma * max Q_target` ở bước trung gian (trong đó `max Q_target = 8.0` là giá trị cực đại ước lượng từ mạng mục tiêu giữ ổn định) và giá trị khi là bước kết thúc lượt (`y = r`).

Định dạng đầu ra (1 dòng):
`dqn_target=<1 chữ số> terminal_target=<1 chữ số>`
