# Lab RBM L10 — Sai số xác lập điều khiển P và PI

Đọc `K_P Kp_PI Ki_PI steps` từ stdin (ví dụ `3.0 1.2 1.5 150`). Tính sai số xác lập khâu P `1 / (1 + K_P)` và mô phỏng bộ PI bám đích `r = 1` trên hệ `y' = -y + u` từ `y(0) = 0` với bước Euler `dt = 0.05` (`e = 1 - y`, `integ += e * dt`, `u = Kp_PI * e + Ki_PI * integ`, `y += dt * (-y + u)`).
In đúng 1 dòng `P_steady_err=<4 chữ số> PI_final_err=<4 chữ số>`.
