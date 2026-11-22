# Lab RLN L07 — Gradient chính sách REINFORCE và đường cơ sở giảm phương sai

Với `N = 2` hành động đồng xác suất, mẫu gradient có dạng `g_i = grad_i * (G_i - b)`: hành động 1 có `(G_1 = 8, grad_1 = +0.5)` và hành động 2 có `(G_2 = 14, grad_2 = -0.5)`. Tính kỳ vọng và **phương sai tổng thể** (chia cho `N = len(vals) = 2`) khi chưa trừ đường cơ sở (`b = 0`) so với sau khi trừ đường cơ sở `b = 11`.

Định dạng đầu ra (1 dòng):
`mean=<2 chữ số> raw_var=<2 chữ số> bas_var=<2 chữ số>`
