# Lab RBM L07 — Giải ODE x' = -2x bằng Euler

Đọc `x0 h steps` từ stdin (ví dụ `1.0 0.05 20`). Chạy `steps` bước Euler và đối chiếu `x0 * exp(-2 * h * steps)`.
In đúng 1 dòng `euler=<4 chữ số> exact=<4 chữ số> err=<4 chữ số>`.
