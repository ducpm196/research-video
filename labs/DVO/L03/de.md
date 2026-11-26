# Lab DVO L03 — Xác suất đường ống CI đỏ vì test chập chờn (flaky)

Đọc `stdin` `tests=<int> p1=<float> p2=<float>`. Tính xác suất thất bại của cả đường ống ở hai mức tỉ lệ lỗi giả `p1` và `p2` cùng xác suất toàn xanh ở mức `p1`.

In đúng 3 dòng: `flaky_fail_pct_300=<.1f>%`, `flaky_fail_pct_p0005=<.1f>%`, `pipeline_always_green_pct=<.1f>%`.
Chấm tự động: `bash labs/cham.sh DVO L03 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
