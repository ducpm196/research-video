# Lab DBS L05 — SQLite thật: đối chiếu tách không mất thông tin vs tách mất (sinh dòng ma)

Viết tập lệnh SQLite cho bảng `DK(mssv, lop, mon)` gồm `3` dòng `('S1','K1','DB'), ('S2','K1','OS'), ('S1','K1','AI')`: chiếu tách đúng qua `mssv` cho lại `3` dòng; chiếu tách sai theo `lop` rồi `JOIN` lại sinh dòng ma, in đúng 3 dòng:
1. `orig_rows=3`
2. `good_join_rows=3`
3. `bad_join_rows=6`

Chấm tự động:
```bash
bash labs/cham.sh DBS L05 duong_dan/bai_cua_ban.sql
```
