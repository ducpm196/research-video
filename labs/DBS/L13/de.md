# Lab DBS L13 — SQLite thật: phát hiện bế tắc trên đồ thị chờ (Wait-For Graph) T1<->T2

Viết tập lệnh SQLite lưu bảng giữ khoá `Held(res TEXT, tx INT)` và bảng chờ `Wait(tx INT, res TEXT)` cho `T1 giữ A chờ B; T2 giữ B chờ A`, JOIN tạo đồ thị chờ `T1 -> T2 -> T1` và kết luận cần huỷ 1 giao dịch nạn nhân, in đúng 3 dòng:
1. `wait_edges=2`
2. `deadlock_detected=1`
3. `victim_needed=1`

Chấm tự động:
```bash
bash labs/cham.sh DBS L13 duong_dan/bai_cua_ban.sql
```
