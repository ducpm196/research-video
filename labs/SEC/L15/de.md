# Lab SEC L15 — Tính biên tràn đọc Heartbleed 2 byte và kiểm chứng kiểm biên

Đọc `stdin` `bits=<int> claimed=<int> actual=<int>`. Tính ngưỡng bộ đếm `2^bits`, số byte bộ nhớ bị đọc tràn khi không kiểm biên và kiểm tra hàm `safe_heartbeat(claimed, actual)`.

In đúng 3 dòng: `max_u16_bytes=<d>`, `leaked_bytes=<d>`, `safe_check_rejected=<0|1>`.
Chấm tự động: `bash labs/cham.sh SEC L15 duong_dan/bai_cua_ban.py`
