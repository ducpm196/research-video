# Lab DSC L01 — Thang khoảng độ C vs thang tỉ lệ Kelvin

Đọc `stdin` `c1=<float> c2=<float>`. So sánh tỉ lệ chia sai trên độ C `c1 / c2` với tỉ lệ đúng trên thang Kelvin `(c1 + 273.15) / (c2 + 273.15)`.

In 1 dòng: `celsius_fake=<.1f>x kelvin_real=<.3f>x`.
Chấm tự động: `bash labs/cham.sh DSC L01 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
