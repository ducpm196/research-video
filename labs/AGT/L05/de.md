# Lab AGT L05 — Tự kiểm tra: tỉ lệ câu đúng thật sau bộ kiểm chứng

Đọc `stdin` chuỗi `base=<f> tpr=<f> fpr=<f>` (trong đó `base` là tỉ lệ câu đúng ban đầu `p`, `tpr` là tỉ lệ nhận đúng của bộ kiểm chứng, `fpr` là tỉ lệ nhận nhầm câu sai). Tính `TP = base * tpr`, `FP = (1 - base) * fpr` và xác suất đúng hậu nghiệm `TP / (TP + FP) * 100`.

In 1 dòng: `accepted_true_pct=<.1f>%`.
Chấm tự động: `bash labs/cham.sh AGT L05 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
