# Lab DVO L07 — Tính tỉ lệ lỗi canary và xác suất p nhị thức

Đọc `stdin` `n=<int> p=<float> obs=<int>`. Tính số lỗi kỳ vọng `n * p`, xác suất đuôi `P(X >= obs)` theo phân phối nhị thức và ra quyết định rollback khi `< 0.01`.

In đúng 3 dòng: `expected_errors=<d>`, `tail_prob_ge20=<.4f>`, `rollback_triggered=<0|1>`.
Chấm tự động: `bash labs/cham.sh DVO L07 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
