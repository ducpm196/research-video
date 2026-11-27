# Lab CLC L06 — Chi phí GB-giây của hàm Serverless

Đọc `stdin` `calls=<int> mem1=<f> ms1=<f> mem2=<f> ms2=<f>`. Tính tổng GB-giây ở hai cấu hình RAM và kiểm tra hai tổng có bằng nhau hay không.

In 3 dòng: `gb_sec_512mb=<d>`, `gb_sec_1gb=<d>`, `same_gb_sec=<0|1>`.
Chấm tự động: `bash labs/cham.sh CLC L06 duong_dan/bai_cua_ban.py`
Gợi ý Python: `import sys; kv = dict(t.split('=') for t in sys.stdin.read().split())`; dùng `int(...)`/`float(...)`, chú ý giữ nguyên 2 tên khoá đầu ra `gb_sec_512mb`, `gb_sec_1gb`.
