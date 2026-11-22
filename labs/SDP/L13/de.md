# Lab SDP L13 — Tái cấu trúc an toàn: kiểm thử tương đương & ca biên quên max(0, km-5)

Viết hàm `fee_old(tien, km)` (thuế 10%, phí giao 15 000 + `max(0, km - 5) * 4000` khi `tien < 500 000`) và bản tách sạch `fee_new(tien, km)`. Dùng `random.Random(1)` quét 10 000 cặp `(tien, km)` (`randrange(0, 1000001, 1000)`, `randrange(0, 31)`) đối chiếu `fee_old` với `fee_new` và bản lỗi `fee_bug` quên `max(0, km - 5)`, cùng ca biên `tien = 500 000, km = 3`, in đúng 3 dòng:
1. `new_mismatches=0`
2. `bug_mismatches=817`
3. `edge_500k_3km=550000`

Chấm tự động:
```bash
bash labs/cham.sh SDP L13 duong_dan/bai_cua_ban.py
```
