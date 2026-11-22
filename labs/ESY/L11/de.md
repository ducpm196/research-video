# Lab ESY L11 — Mô phỏng hàng đợi giữa ngắt ISR và tác vụ nền tránh mất byte

Tạo hàng đợi vòng (`collections.deque`) độ dài tối đa `8` nhận từng byte của chuỗi `b'TEMP:42\n'` từ hàm ngắt, đếm số byte bị tràn không đẩy vào được (`overflows`), rồi tác vụ nền lấy toàn bộ phần tử còn trong hàng đợi giải mã thành chuỗi và in dạng `repr` giữ nguyên dấu nháy (`{msg!r}`).
In đúng 1 dòng `queued=... overflows=... decoded=...`.

Chấm tự động:
```bash
bash labs/cham.sh ESY L11 duong_dan/bai_cua_ban.py
```
