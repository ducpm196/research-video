# Lab DAN L01 — Trung bình có trọng số và bẫy trung bình của hai trung bình

Đọc `stdin` `na=<int> ma=<float> nb=<int> mb=<float>`. So sánh trung bình gộp sai `(ma + mb) / 2` với trung bình có trọng số đúng `(na*ma + nb*mb) / (na + nb)`.

In 1 dòng: `naive=<.2f> weighted=<.2f>`.
Chấm tự động: `bash labs/cham.sh DAN L01 duong_dan/bai_cua_ban.py`

> Gợi ý đọc `stdin`: `kv = {k: float(v) for k, v in (t.split("=") for t in sys.stdin.read().split())}`.
