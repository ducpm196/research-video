# Lab DAN L07 — Dự báo đường cơ sở: MAE và bẫy chia 0 của MAPE

Đọc `stdin` `act=<v1,v2,...> pred=<v1,v2,...>`. Tính sai số tuyệt đối trung bình `MAE` và phát hiện xem thực tế có phần tử bằng `0` làm vô định `MAPE` hay không.

In 1 dòng: `mae=<.2f> mape_undefined=<0|1>`.
Chấm tự động: `bash labs/cham.sh DAN L07 duong_dan/bai_cua_ban.py`

> Gợi ý đọc `stdin`: `kv = dict(t.split("=") for t in sys.stdin.read().split())`; dùng `any(a == 0 for a in act)` (đã giới thiệu ở màn hình bài) để phát hiện chia 0.
