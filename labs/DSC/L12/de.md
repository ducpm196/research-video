# Lab DSC L12 — Đa cộng tuyến: hệ số phóng đại phương sai VIF

Đọc `stdin` `r=<float>`. Tính hệ số phóng đại phương sai `VIF = 1 / (1 - r^2)` và độ phình sai số chuẩn `sqrt(VIF)`.

In 1 dòng: `r=<.1f> VIF=<.2f> se_inflation=<.2f>x`.
Chấm tự động: `bash labs/cham.sh DSC L12 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
