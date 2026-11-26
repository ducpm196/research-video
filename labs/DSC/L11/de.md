# Lab DSC L11 — Tỉ lệ nền, độ nhạy, đặc hiệu và PPV

Đọc `stdin` `n=<int> prev=<float> sens=<float> spec=<float>`. Tính số dương thật `tp`, dương giả `fp` và giá trị dự đoán dương `PPV = tp / (tp + fp)`.

In 1 dòng: `tp=<.1f> fp=<.1f> ppv=<.3f>`.
Chấm tự động: `bash labs/cham.sh DSC L11 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
