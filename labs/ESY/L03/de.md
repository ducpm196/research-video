# Lab ESY L03 — Tần số PWM và chu kỳ nhiệm vụ

Đọc `f_clk presc TOP CMP` từ stdin (ví dụ `16000000 8 999 250`). Tính tần số `f_clk / (presc * (TOP + 1))` và `%` mức cao.
In đúng 1 dòng `pwm_hz=<int> duty_pct=<1 chữ số>%`.
