# Lab SEC L15 — Tính biên tràn đọc Heartbleed 2 byte (64 KB) và kiểm chứng kiểm biên

Viết chương trình Python mô phỏng khung Heartbeat có tải thực `5 B` nhưng trường độ dài 16 bit báo `65 535 B`: tính số byte rò rỉ bộ nhớ nếu không kiểm biên và viết hàm `safe_heartbeat(claimed, actual)` chặn lỗi này, in đúng 3 dòng:
1. `max_u16_bytes=65536`
2. `leaked_bytes=65530`
3. `safe_check_rejected=1`

Chấm tự động:
```bash
bash labs/cham.sh SEC L15 duong_dan/bai_cua_ban.py
```
