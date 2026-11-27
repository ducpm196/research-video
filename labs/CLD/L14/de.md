# Lab CLD L14 — Bù trừ nhả tài nguyên trong Saga đặt vé

Đọc `stdin` `avail=<int> reserve=<int>`. Thực hiện giữ `reserve` ghế rồi nhả lại đúng `reserve` ghế khi thanh toán thất bại.

In 2 dòng: `after_reserve=<d>`, `after_compensate=<d>`.
Gợi ý Python: `import sys; kv = dict(t.split('=') for t in sys.stdin.read().split())`; ép `int(...)` và trừ rồi cộng trả lại `reserve`.
Chấm tự động: `bash labs/cham.sh CLD L14 duong_dan/bai_cua_ban.py`
