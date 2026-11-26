# Lab ESY L11 — Hàng đợi vòng ISR và phát hiện tràn

Đọc `cap|chuỗi` từ stdin (ký tự `\n` viết dạng hai ký tự `\\n`; ví dụ `8|TEMP:42\n`). Đẩy từng byte vào hàng đợi sức chứa `cap` và giải mã phần nhận được.
In đúng 1 dòng `queued=<int> overflows=<int> decoded=<repr>`.
