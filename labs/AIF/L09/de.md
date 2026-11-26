# Lab AIF L09 — Suy diễn tiến trên tập luật Horn

Đọc `stdin` `facts=<f1,f2,...> rules=<pre1+pre2>res,...>`. Chạy suy diễn tiến chọn luật đầu tiên có tiền đề nằm trong tập sự kiện cho tới điểm bất động.

In 1 dòng: `derived=<list>`.
Chấm tự động: `bash labs/cham.sh AIF L09 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
