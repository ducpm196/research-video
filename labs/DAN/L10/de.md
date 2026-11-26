# Lab DAN L10 — Khoảng tin cậy Wilson 95% trên mẫu nhỏ và lớn

Đọc `stdin` `a=<k1,n1> b=<k2,n2>`. Tính khoảng tin cậy Wilson 95% (`z = 1.96`, làm tròn 3 chữ số) cho hai cặp `(k, n)`.

In 1 dòng: `A_3_3= (<lo>, <hi>) B_120_800= (<lo>, <hi>)`.
Chấm tự động: `bash labs/cham.sh DAN L10 duong_dan/bai_cua_ban.py`

> Gợi ý đọc `stdin`: `kv = dict(t.split("=") for t in sys.stdin.read().split())`; hàm Wilson cần `import math` với `math.sqrt(...)`.
