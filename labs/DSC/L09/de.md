# Lab DSC L09 — Báo giả toàn họ FWER và hiệu chỉnh Bonferroni

Đọc `stdin` `tests=<int> alpha=<float>`. Tính xác suất báo nhầm FWER gốc `1 - (1 - alpha)^tests`, ngưỡng chia đều `alpha / tests` và FWER sau hiệu chỉnh Bonferroni.

In 1 dòng: `raw_fwer=<.3f> bonf_alpha=<.4f> fwer_bonf=<.3f>`.
Chấm tự động: `bash labs/cham.sh DSC L09 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
