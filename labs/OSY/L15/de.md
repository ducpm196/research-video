# Lab OSY L15 — Đối chiếu bộ lập lịch Linux O(n), CFS và EEVDF

Đọc `stdin` `procs=<int> hz=<int> w1=<int> w2=<int> s1=<int> s2=<int> total_ms=<int>`. Tính số lượt kiểm mỗi giây, tỉ lệ chia CPU theo trọng số và mô phỏng EEVDF: ở mỗi bước tính thời gian ảo trung bình `avg = (v['A'] + v['B']) / 2`, lọc các tác vụ đủ điều kiện có độ trễ hưởng `avg - v[k] >= 0`, rồi chọn bên có `v[k] + slice[k]` nhỏ nhất (hoà chọn `A`).

In đúng 3 dòng (giữ nguyên tên khoá cố định): `on_checks_per_sec=<d>`, `cfs_share_2048_vs_1024=<.1f>%,<.1f>%`, `eevdf_ms_36ms=<d>,<d> first=<A|B>`.
Chấm tự động: `bash labs/cham.sh OSY L15 duong_dan/bai_cua_ban.py`
