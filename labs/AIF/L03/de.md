# Lab AIF L03 — Giải hệ số nhánh hiệu dụng b* bằng chia đôi

Đọc `stdin` `N=<float> d=<int> lo=<float> hi=<float>`. Tìm `b*` trên `[lo, hi]` thỏa `sum(b^k, k=0..d) == N + 1` qua 50 bước chia đôi.

In 1 dòng: `b_star=<.4f> sum_val=<.2f>`.
Chấm tự động: `bash labs/cham.sh AIF L03 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
