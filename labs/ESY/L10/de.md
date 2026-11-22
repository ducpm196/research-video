# Lab ESY L10 — Mô phỏng lập lịch ưu tiên cố định so với hạn sớm nhất EDF trên chu kỳ 16 ms

Mô phỏng từng nhịp `1 ms` từ `t = 0..15` cho hai tác vụ `(C=4, T=8)` (chỉ số 0) và `(C=2, T=4)` (chỉ số 1) có tổng độ dùng `U = 1.0` theo hai luật: ưu tiên cố định (luôn chọn tác vụ chỉ số 0 nếu sẵn sàng) và hạn sớm nhất (`EDF`, luôn chọn tác vụ có hạn chót `dl` nhỏ hơn). Đếm số lần trễ hạn của mỗi luật.
In đúng 1 dòng `U=... fixed_misses=... edf_misses=...` (1 chữ số thập phân cho `U`).

Chấm tự động:
```bash
bash labs/cham.sh ESY L10 duong_dan/bai_cua_ban.py
```
