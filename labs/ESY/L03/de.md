# Lab ESY L03 — Tính tần số bộ định thời và độ rộng xung PWM từ f_clk, hệ số chia và TOP

Trên bộ định thời xung nhịp `f_clk = 16_000_000 Hz`, chọn hệ số chia `presc = 8`, giá trị đỉnh `TOP = 999` và ngưỡng so sánh `CMP = 250` (chân ra mức cao khi `counter < CMP`). Tính tần số `f_clk / (presc * (TOP + 1))` và chu kỳ nhiệm vụ `CMP / (TOP + 1) * 100%`.
In đúng 1 dòng `pwm_hz=... duty_pct=...%`.

Chấm tự động:
```bash
bash labs/cham.sh ESY L03 duong_dan/bai_cua_ban.py
```
