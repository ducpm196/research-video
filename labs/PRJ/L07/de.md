# Dự án PRJ L07 — Đường ống Outbox, Consistent Hashing & Circuit Breaker

Viết chương trình Python: (1) ghi 1 đơn thành công và 1 đơn rollback vào cặp bảng SQLite `ord`/`outb`; (2) đếm số khoá trong 500 khoá dời chỗ khi tăng từ 4 lên 5 nút theo SHA-256 trên vòng băm (< 150 khoá); (3) mở ngắt mạch `OPEN` sau 3 lỗi, in đúng 3 dòng:
1. `outbox_atomic_match=1`
2. `ch_moved_lt_150=1`
3. `cb_after_3fails=OPEN`

Chấm tự động:
```bash
bash labs/cham.sh PRJ L07 duong_dan/bai_cua_ban.py
```
