# Lab EVT L05 — Mô hình tách ghi-đọc (CQRS) và độ trễ chiếu

Đọc `stdin` `w=<int> p=<int> secs=<int>`. Tính số sự kiện tồn đọng khi ghi `w/s` nhanh hơn chiếu `p/s` trong `secs` giây, độ trễ dữ liệu và thời gian xả với `2` bộ chiếu song song.

In 3 dòng: `backlog=<d>`, `data_lag_s=<.1f>`, `drain_with_2_s=<.1f>`.
Chấm tự động: `bash labs/cham.sh EVT L05 duong_dan/bai_cua_ban.py`
