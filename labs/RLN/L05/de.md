# Lab RLN L05 — Q-learning (ngoài chính sách) và SARSA (theo chính sách)

Từ `Q = 1.5`, thưởng `r = -1.0`, `gamma = 0.9`, tốc độ học `alpha = 0.2`: áp dụng quy tắc cập nhật `Q_moi = Q + alpha * (r + gamma * đích - Q)` cho ngoài chính sách (dùng `max Q(s') = 6.0`) và theo chính sách thật vừa chọn (`Q(s', a') = 2.0`).

Định dạng đầu ra (1 dòng):
`q_learning=<2 chữ số> sarsa=<2 chữ số>`
