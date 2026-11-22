# Lab IRS L07 — Phân rã ma trận bằng dốc ngẫu nhiên (SGD)

Với `p = [1.5, 0.5]`, `q = [1.0, 2.0]`, điểm thật `r = 4.0`, tốc độ học `eta = 0.2`, tính sai số dự đoán `err = r - dot(p, q)` (với `dot` là tích vô hướng `sum(a*b)`) và áp dụng quy tắc cập nhật `p_i <- p_i + eta * (err * q_i - lam * p_i)` cho hai trường hợp `lam = 0` và `lam = 0.05` (mọi toạ độ làm tròn `round(..., 4)`).

Định dạng đầu ra (1 dòng):
`err=<1 chữ số> p_raw=[<4 chữ số>, <4 chữ số>] p_reg=[<4 chữ số>, <4 chữ số>]`
