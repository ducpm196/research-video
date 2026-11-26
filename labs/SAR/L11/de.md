# Lab SAR L11 — Khoá tài khoản báo cáo ở chế độ chỉ đọc trên SQLite

Đọc `stdin` `amt=<int> read_only=<0|1>` (tuỳ chọn `expect=<int>`). Nạp bảng `invoices` với giá trị `amt`, bật `PRAGMA query_only = ON` nếu `read_only=1` rồi kiểm tra giá trị đọc khớp `expect` và thử `DELETE`.

In 3 dòng: `read_allowed=<0|1>`, `write_blocked=<0|1>`, `blast_contained=<0|1>`.
Chấm tự động: `bash labs/cham.sh SAR L11 duong_dan/bai_cua_ban.py`
