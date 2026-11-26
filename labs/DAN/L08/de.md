# Lab DAN L08 — Phân bố lệch và tỉ trọng nhóm 20% khách hàng đầu

Đọc `stdin` `rev=<r1,r2,...>`. Tính trung bình, trung vị và phần trăm đóng góp của 20% phần tử lớn nhất (mảng đã sắp giảm dần).

In 1 dòng: `mean=<.1f> median=<.1f> top20=<.1f>%`.
Chấm tự động: `bash labs/cham.sh DAN L08 duong_dan/bai_cua_ban.py`

> Gợi ý đọc `stdin`: `rev = sorted([float(x) for x in sys.stdin.read().strip().split("=", 1)[1].split(",")], reverse=True)`.
