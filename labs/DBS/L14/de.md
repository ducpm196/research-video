# Lab DBS L14 — SQLite thật: mô phỏng WAL (ghi nhật ký trước) và pha REDO (làm lại) / UNDO (huỷ)

Viết tập lệnh SQLite kiểm chứng bảng nhật ký `WAL(lsn INT, tx INT, act TEXT, delta INT)` (WAL = ghi nhật ký trước; điểm kiểm tra checkpoint) gồm `T1` đã ghi nhận `COMMIT (+50)` cần làm lại (`REDO`) và `T2` chưa ghi nhận `(+99)` cần huỷ (`UNDO`) trên giá trị gốc `100`: tổng hợp giá trị đúng sau phục hồi (`150`), in đúng 3 dòng:
1. `redo_applied_tx=1`
2. `undo_reverted_tx=1`
3. `recovered_val=150`

Chấm tự động:
```bash
bash labs/cham.sh DBS L14 duong_dan/bai_cua_ban.sql
```
