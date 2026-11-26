# Lab DAN L00 — Định nghĩa chỉ số chặt: đăng nhập và thao tác

Đọc `stdin` `logs=<l1:a1,l2:a2,...>`. Đếm số người dùng hoạt động theo chuẩn nới lỏng (`login > 0`) và chuẩn chặt (`actions > 0`).

In 1 dòng: `active_login=<d> active_action=<d>`.
Chấm tự động: `bash labs/cham.sh DAN L00 duong_dan/bai_cua_ban.py`

> Gợi ý đọc `stdin`: `pairs = [tuple(map(int, p.split(":"))) for p in input().split("=", 1)[1].split(",")]`.
