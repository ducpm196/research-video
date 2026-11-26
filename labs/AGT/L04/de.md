# Lab AGT L04 — Truy vấn lặp và kiểm chứng trích dẫn nguyên văn

Đọc `stdin` `init_hit=<f> gain=<f> rounds=<int>`, dòng 2 `src=<văn bản>`, dòng 3 `quote=<câu trích>`. Tính độ phủ tích lũy sau `1 + rounds` vòng và kiểm tra `quote` xuất hiện nguyên văn trong `src`.

In 1 dòng: `recall_after_3=<.1f>% matched_quote=<0|1>`.
Chấm tự động: `bash labs/cham.sh AGT L04 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: đọc từng dòng bằng `sys.stdin.read().splitlines()`; tách dòng 1 bằng `split()`, còn dòng 2 và dòng 3 tách bằng `ln.split('=', 1)` để giữ nguyên dấu cách trong chuỗi.
