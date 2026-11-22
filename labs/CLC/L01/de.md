# Lab CLC L01 — Độ sẵn sàng song song đa vùng sẵn sàng (AZ)

Mỗi vùng sẵn sàng (AZ: Availability Zone) độc lập có độ sẵn sàng `99,0%` (`xác suất hỏng p = 0,01`). Tính độ sẵn sàng khi chạy song song trên `2` vùng và `3` vùng (`1 - p^k`), cùng số phút ngừng kỳ vọng mỗi năm (`525 600` phút) ở mức 2 vùng.

Định dạng đầu ra (3 dòng):
`az2_avail_pct=<4 chữ số>%`
`az3_avail_pct=<4 chữ số>%`
`az2_downtime_min_year=<1 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CLC L01 duong_dan/bai_cua_ban.py
```
