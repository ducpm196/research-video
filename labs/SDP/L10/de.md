# Lab SDP L10 — Mẫu hành vi: Observer (3 người nghe x 4 sự kiện) và Command undo

Viết chương trình Python mô phỏng Observer thông báo `4` sự kiện tới `3` listener (`12` lần gọi) và chuỗi Command trên `val=10`: `(+5), (*2), (-3)` rồi `undo()` 1 bước cuối, in đúng 3 dòng:
1. `observer_notifications=12`
2. `cmd_after_3=27`
3. `cmd_after_undo1=30`

Chấm tự động:
```bash
bash labs/cham.sh SDP L10 duong_dan/bai_cua_ban.py
```
