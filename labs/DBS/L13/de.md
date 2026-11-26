# Lab DBS L13 — SQLite: phát hiện bế tắc trên đồ thị chờ (Wait-For Graph)

Cơ sở dữ liệu có sẵn `Held(r, tx)` và `Wait(tx, r)`. Tạo khung nhìn đồ thị chờ `CREATE VIEW WFG AS ...` từ phép nối `Wait` với `Held` theo tài nguyên rồi dùng `WITH RECURSIVE` (giới hạn `d < 8`) kiểm tra có chu trình bế tắc không.

In đúng 3 dòng: `wait_edges=<d>`, `deadlock_detected=<0|1>`, `victim_needed=<0|1>`.
Chấm tự động: `bash labs/cham.sh DBS L13 duong_dan/bai_cua_ban.sql`
