# Lab CLD L13 — Rò rỉ bí mật trong các lớp ảnh bất biến

Đọc `stdin` `secret=<str> l1=<f1,f2> l2=<f1,f2> l3=<f1,f2>`. Kiểm tra tệp `secret` còn nhìn thấy ở lớp cuối `l3` không và có tồn tại trong bất kỳ lớp lịch sử nào không.

In 2 dòng: `in_final_view=<0|1>`, `leaked_in_layers=<0|1>`.
Gợi ý Python: `import sys; kv = dict(t.split('=') for t in sys.stdin.read().split())`; tách danh sách bằng `.split(',')` và dùng `set(...)`.
Chấm tự động: `bash labs/cham.sh CLD L13 duong_dan/bai_cua_ban.py`
